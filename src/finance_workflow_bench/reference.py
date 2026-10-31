"""Validated Decimal reference calculator for the fixed cash_forecast_001 contract."""
import csv
import json
import re
from collections import Counter
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

START = date(2027, 1, 4)
END = date(2027, 4, 4)
ZERO = Decimal("0.00")
PAYMENT_FIELDS = ["supplier_payments", "tax_payments", "other_external_payments", "payroll_payments", "rent_payments", "other_recurring_payments"]
FIELDS = {
    "opening_balances.csv": "account_id as_of_date available_balance",
    "receivables.csv": "record_id invoice_id customer_id invoice_amount paid_before_as_of expected_receipt_date",
    "payables.csv": "record_id obligation_id category gross_amount paid_before_as_of payment_date",
    "recurring_expenses.csv": "record_id expense_id category cash_date amount",
}


def money(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]+\.[0-9]{2}", value):
        raise ValueError(f"Invalid nonnegative monetary input: {value!r}")
    return Decimal(value)


def iso_date(value):
    result = date.fromisoformat(value)
    if result.isoformat() != value:
        raise ValueError("Dates must use YYYY-MM-DD")
    return result


def read_rows(folder, filename):
    with (folder / filename).open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != FIELDS[filename].split():
            raise ValueError(f"Unexpected header in {filename}")
        rows = list(reader)
    for row in rows:
        if None in row or any(value in (None, "") for value in row.values()):
            raise ValueError(f"Missing or extra CSV fields in {filename}")
    return rows


def unique_rows(rows, business_key, filename):
    seen, business, duplicates = {}, {}, Counter()
    for row in rows:
        rid = row["record_id"]
        if rid in seen:
            if seen[rid] != row:
                raise ValueError(f"Conflicting duplicate: {filename}/{rid}")
            duplicates[rid] += 1
        else:
            bid = row[business_key]
            if bid in business:
                raise ValueError(f"Repeated business identity: {filename}/{bid}")
            seen[rid] = row
            business[bid] = rid
    return list(seen.values()), [dict(source_file=filename, record_id=k, discarded_count=v) for k, v in duplicates.items()]


def financing(cash, debt, receipts, payments, minimum, limit, rate):
    interest = (debt * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    before = cash + receipts - payments - interest
    draw = min(max(minimum - before, ZERO), limit - debt)
    repayment = min(max(before - minimum, ZERO), debt)
    closing = before + draw - repayment
    closing_debt = debt + draw - repayment
    return dict(interest_paid=interest, cash_before_financing=before, credit_draw=draw,
                principal_repayment=repayment, closing_cash=closing, closing_principal=closing_debt,
                credit_available=limit - closing_debt, minimum_cash_shortfall=max(minimum - closing, ZERO),
                unfunded_cash_deficit=max(-closing, ZERO), minimum_cash_breached=closing < minimum, unfunded_deficit=closing < ZERO)


def solve(input_dir):
    folder = Path(input_dir)
    facility = json.loads((folder / "credit_facility.json").read_text(encoding="utf-8"))
    expected = dict(currency="USD", credit_limit="200000.00", opening_principal="60000.00", weekly_interest_rate="0.002000", minimum_cash="50000.00", interest_basis="opening_week_principal", interest_payment="end_of_each_week", fees="0.00")
    if facility != expected:
        raise ValueError("Facility does not match this fixed case contract")
    balances = read_rows(folder, "opening_balances.csv")
    if not balances or len({r["account_id"] for r in balances}) != len(balances):
        raise ValueError("Missing or repeated opening accounts")
    if any(iso_date(r["as_of_date"]) != START - timedelta(days=1) for r in balances):
        raise ValueError("Invalid opening balance date")
    cash = sum((money(r["available_balance"]) for r in balances), ZERO)
    debt, limit, minimum = (money(facility[k]) for k in ("opening_principal", "credit_limit", "minimum_cash"))
    rate = Decimal(facility["weekly_interest_rate"])
    buckets = [dict.fromkeys(["receipts"] + PAYMENT_FIELDS, ZERO) for _ in range(13)]
    exclusions, duplicates, ledger = [], [], []
    specs = [
        ("receivables.csv", "invoice_id", "expected_receipt_date", "invoice_amount"),
        ("payables.csv", "obligation_id", "payment_date", "gross_amount"),
        ("recurring_expenses.csv", "expense_id", "cash_date", "amount"),
    ]
    for filename, business_key, date_key, amount_key in specs:
        rows, removed = unique_rows(read_rows(folder, filename), business_key, filename)
        duplicates.extend(removed)
        for row in rows:
            when = iso_date(row[date_key])
            gross = money(row[amount_key])
            paid = money(row["paid_before_as_of"]) if "paid_before_as_of" in row else ZERO
            if paid > gross:
                raise ValueError(f"Overpaid record: {row['record_id']}")
            amount = gross - paid
            if "paid_before_as_of" in row and amount > ZERO and when < START:
                raise ValueError("Outstanding event predates the forecast")
            category = row.get("category", "receipts")
            allowed = {"supplier", "tax", "other_external", "internal_transfer"} if filename == "payables.csv" else {"payroll", "rent", "other_recurring"} if filename == "recurring_expenses.csv" else {"receipts"}
            if category not in allowed:
                raise ValueError(f"Unknown category: {category}")
            reason = "internal_transfer" if category == "internal_transfer" else "zero_outstanding" if "paid_before_as_of" in row and amount == ZERO else "outside_horizon" if not START <= when <= END else None
            if reason:
                exclusions.append(dict(source_file=filename, record_id=row["record_id"], reason=reason))
            else:
                index = (when - START).days // 7
                field = category if category == "receipts" else category + "_payments"
                buckets[index][field] += amount
                ledger.append(dict(source_file=filename, record_id=row["record_id"], week=index + 1, field=field, amount=f"{amount:.2f}"))
    weeks = []
    for number, flows in enumerate(buckets, 1):
        start = START + timedelta(weeks=number - 1)
        row = dict(week=number, start_date=start.isoformat(), end_date=(start + timedelta(days=6)).isoformat(), opening_cash=cash, opening_principal=debt, **flows)
        row.update(financing(cash, debt, flows["receipts"], sum((flows[k] for k in PAYMENT_FIELDS), ZERO), minimum, limit, rate))
        cash, debt = row["closing_cash"], row["closing_principal"]
        weeks.append({k: f"{v:.2f}" if isinstance(v, Decimal) else v for k, v in row.items()})
    return dict(case_id="cash_forecast_001", currency="USD", weeks=weeks, exclusions=exclusions, duplicates_removed=duplicates), ledger


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result, ledger = solve(args.inputs)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "forecast.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (args.output / "source_ledger.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print("Reference forecast and source ledger written.")
