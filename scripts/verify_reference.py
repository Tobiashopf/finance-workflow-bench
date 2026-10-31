"""Second calculation using integer cents, daily aggregation and a net-position identity.

Does not import the reference calculator. It provides computational cross-checking,
not independent expert review. Assertions intentionally fail on any disagreement.
"""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "cases/cash_forecast_001/inputs"
OUTPUT = ROOT / "reference/cash_forecast_001"


def cents(value):
    negative = value.startswith("-")
    dollars, fraction = value.lstrip("-").split(".")
    assert len(fraction) == 2
    return (-1 if negative else 1) * (int(dollars) * 100 + int(fraction))


def formatted(value):
    return f"{'-' if value < 0 else ''}{abs(value) // 100}.{abs(value) % 100:02d}"


def check():
    forecast = json.loads((OUTPUT / "forecast.json").read_text(encoding="utf-8"))
    start, finish = date(2027, 1, 4), date(2027, 4, 4)
    daily = defaultdict(lambda: defaultdict(int))
    excluded, repeated = [], []
    for filename, date_column, amount_column in [
        ("receivables.csv", "expected_receipt_date", "invoice_amount"),
        ("payables.csv", "payment_date", "gross_amount"),
        ("recurring_expenses.csv", "cash_date", "amount"),
    ]:
        with (INPUTS / filename).open(encoding="utf-8", newline="") as f:
            raw = list(csv.DictReader(f))
        counts = Counter(r["record_id"] for r in raw)
        repeated.extend(dict(source_file=filename, record_id=k, discarded_count=v - 1) for k, v in counts.items() if v > 1)
        # Whole-row deduplication is intentionally different from the reference's ID map.
        distinct = {tuple(r.items()) for r in raw}
        for packed in distinct:
            row = dict(packed)
            when = date.fromisoformat(row[date_column])
            amount = cents(row[amount_column]) - cents(row.get("paid_before_as_of", "0.00"))
            category = row.get("category", "receipts")
            if category == "internal_transfer":
                reason = "internal_transfer"
            elif amount == 0 and "paid_before_as_of" in row:
                reason = "zero_outstanding"
            elif when < start or when > finish:
                reason = "outside_horizon"
            else:
                reason = None
            if reason:
                excluded.append(dict(source_file=filename, record_id=row["record_id"], reason=reason))
            else:
                daily[when][category if category == "receipts" else category + "_payments"] += amount
    with (INPUTS / "opening_balances.csv").open(encoding="utf-8", newline="") as f:
        cash = sum(cents(r["available_balance"]) for r in csv.DictReader(f))
    assert cash == 8000000
    debt, minimum, limit = 6000000, 5000000, 20000000
    fields = ["receipts", "supplier_payments", "tax_payments", "other_external_payments", "payroll_payments", "rent_payments", "other_recurring_payments"]
    expected_receipts = [45000, 55000, 65000, 40000, 35000, 30000, 180000, 160000, 90000, 80000, 75000, 100000, 95000]
    expected_payments = [45000, 66000, 59000, 111000, 130000, 118000, 37000, 66000, 67000, 76000, 42000, 83000, 42000]
    assert forecast["case_id"] == "cash_forecast_001" and forecast["currency"] == "USD"
    assert len(forecast["weeks"]) == 13
    for index, actual in enumerate(forecast["weeks"]):
        monday = start + timedelta(days=7 * index)
        totals = {key: sum(daily[monday + timedelta(days=d)][key] for d in range(7)) for key in fields}
        assert totals["receipts"] == expected_receipts[index] * 100
        payments = sum(totals[k] for k in fields[1:])
        assert payments == expected_payments[index] * 100
        # For nonnegative cents, debt * 0.002 rounded half-up is (debt + 250) // 500.
        interest = (debt + 250) // 500
        before = cash + totals["receipts"] - payments - interest
        # Financing does not change net cash minus debt. Solve for the target debt
        # directly, rather than computing draw and repayment using the reference formula.
        net = before - debt
        new_debt = max(0, min(limit, minimum - net))
        closing = net + new_debt
        expected = dict(week=index + 1, start_date=monday.isoformat(), end_date=(monday + timedelta(days=6)).isoformat())
        numeric = dict(opening_cash=cash, opening_principal=debt, **totals, interest_paid=interest,
                       cash_before_financing=before, credit_draw=max(new_debt - debt, 0),
                       principal_repayment=max(debt - new_debt, 0), closing_cash=closing,
                       closing_principal=new_debt, credit_available=limit - new_debt,
                       minimum_cash_shortfall=max(minimum - closing, 0), unfunded_cash_deficit=max(-closing, 0))
        expected.update({k: formatted(v) for k, v in numeric.items()})
        expected.update(minimum_cash_breached=closing < minimum, unfunded_deficit=closing < 0)
        assert actual == expected, f"Week {index + 1}: integer and decimal calculations disagree"
        cash, debt = closing, new_debt
    key = lambda r: (r["source_file"], r["record_id"])
    assert sorted(forecast["exclusions"], key=key) == sorted(excluded, key=key)
    assert sorted(forecast["duplicates_removed"], key=key) == sorted(repeated, key=key)
    assert len(excluded) == 7 and sum(r["discarded_count"] for r in repeated) == 5
    weeks = forecast["weeks"]
    assert any(w["minimum_cash_breached"] and not w["unfunded_deficit"] for w in weeks)
    assert any(w["unfunded_deficit"] for w in weeks)
    manifest = {str(p.relative_to(ROOT)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(INPUTS.iterdir())}
    manifest["reference/cash_forecast_001/forecast.json"] = hashlib.sha256((OUTPUT / "forecast.json").read_bytes()).hexdigest()
    review = json.loads((ROOT / "reference/review-record.json").read_text(encoding="utf-8"))
    human_status = "project_owner_confirmed" if review["forecast_sha256"] == manifest["reference/cash_forecast_001/forecast.json"] else "re_review_required"
    report = dict(status="passed", method="Integer cents, daily aggregation, net-position financing; no reference imports", weeks_compared=13, exclusions_compared=len(excluded), duplicate_rows_removed=5, human_domain_review=human_status, external_independent_review=False, sha256=manifest)
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports/reference-verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("PASS: all 13 complete weekly records, seven exclusions and five duplicate removals agree.")
    for w in weeks:
        print(w["week"], w["receipts"], formatted(sum(cents(w[k]) for k in fields[1:])), w["interest_paid"], w["credit_draw"], w["principal_repayment"], w["closing_cash"], w["closing_principal"])


if __name__ == "__main__":
    check()

