"""Separate integer-cent oracle; does not import either case's reference calculator."""
import csv
import hashlib
import json
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "cases/borrowing_base_002/inputs"


def cents(text):
    whole, fraction = text.lstrip("-").split(".")
    return (-1 if text.startswith("-") else 1) * (int(whole)*100+int(fraction))


def cash(value):
    return f"{'-' if value < 0 else ''}{abs(value)//100}.{abs(value)%100:02d}"


def read(name, folder=INPUTS):
    with (folder / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def compute(folder=INPUTS, case_id="borrowing_base_002"):
    dates = [r["snapshot_date"] for r in read("snapshot_dates.csv", folder)]
    observations = read("receivables_snapshots.csv", folder)
    events = read("cash_events.csv", folder)
    customers, invoices = [], []
    weeks = []
    opening = json.loads((folder / "opening_position.json").read_text(encoding="utf-8"))
    balance, principal = cents(opening["cash"]), cents(opening["debt"])
    for index, snapshot in enumerate(dates):
        eligible_by_customer = defaultdict(int)
        for r in [x for x in observations if x["snapshot_date"] == snapshot]:
            amount = cents(r["outstanding_amount"])
            age = max(0, (date.fromisoformat(snapshot)-date.fromisoformat(r["due_date"])).days)
            flags = [r["disputed"] == "true", r["related_party"] == "true", age > 60, amount == 0]
            reasons = ["disputed", "related_party", "over_60_days", "zero_balance"]
            decision = next((name for flag, name in zip(flags, reasons) if flag), "eligible")
            eligible = amount if not any(flags) else 0
            eligible_by_customer[r["customer_id"]] += eligible
            invoices.append(dict(snapshot_date=snapshot, invoice_id=r["invoice_id"], customer_id=r["customer_id"], days_past_due=age,
                                 outstanding_amount=cash(amount), eligible_amount=cash(eligible), reason=decision))
        total = sum(eligible_by_customer.values())
        threshold = total // 4
        recognized = 0
        for customer, value in sorted(eligible_by_customer.items()):
            allowed = threshold if value > threshold else value
            recognized += allowed
            customers.append(dict(snapshot_date=snapshot, customer_id=customer, eligible_amount=cash(value),
                                  concentration_threshold=cash(threshold), recognized_amount=cash(allowed), concentration_deduction=cash(value-allowed)))
        base = recognized * 4 // 5
        limit = min(20000000, base)
        sunday = date.fromisoformat(snapshot)
        monday = sunday-timedelta(days=6)
        receipt = sum(cents(r["amount"]) for r in events if r["direction"] == "receipt" and monday <= date.fromisoformat(r["cash_date"]) <= sunday)
        payment = sum(cents(r["amount"]) for r in events if r["direction"] == "payment" and monday <= date.fromisoformat(r["cash_date"]) <= sunday)
        interest = (principal+250)//500
        before = balance+receipt-payment-interest
        required = max(0, principal-limit)
        # Solve final principal from net cash less principal, but constrain repayment
        # when an initial overadvance cannot be fully cured with available cash.
        net_position = before-principal
        if required > max(before, 0):
            cure = max(before, 0)
            final_debt = principal-cure
        else:
            cure = required
            final_debt = min(limit, max(0, 5000000-net_position))
        final_cash = net_position+final_debt
        after_cure_debt = principal-cure
        draw = max(final_debt-after_cure_debt, 0)
        voluntary = max(after_cure_debt-final_debt, 0)
        numeric = dict(eligible=total, concentration_threshold=threshold, recognized=recognized, borrowing_base=base, effective_limit=limit,
                       opening_cash=balance, opening_debt=principal, receipts=receipt, payments=payment, interest=interest, cash_before_financing=before,
                       required_cure=required, actual_cure=cure, unpaid_cure=max(after_cure_debt-limit, 0), draw=draw, voluntary_repayment=voluntary,
                       closing_cash=final_cash, closing_debt=final_debt, unused_credit=max(limit-final_debt, 0), overadvance=max(final_debt-limit, 0),
                       buffer_shortfall=max(5000000-final_cash, 0), cash_deficit=max(-final_cash, 0))
        weeks.append(dict(week=index+1, snapshot_date=snapshot, **{k: cash(v) for k, v in numeric.items()},
                          overadvance_present=final_debt > limit, buffer_breached=final_cash < 5000000, unfunded_deficit=final_cash < 0))
        balance, principal = final_cash, final_debt
    return dict(case_id=case_id, currency="USD", weeks=weeks,
                    invoice_checks=sorted(invoices, key=lambda r: (r["snapshot_date"], r["invoice_id"])), customer_checks=customers)


def verify():
    actual_path = ROOT / "reference/borrowing_base_002/forecast.json"
    actual = json.loads(actual_path.read_text(encoding="utf-8"))
    expected = compute()
    weeks, invoices, customers = expected["weeks"], expected["invoice_checks"], expected["customer_checks"]
    if actual != expected:
        raise AssertionError("Integer-cent oracle disagrees with reference")
    checkpoint = [("168000.00", "50000.00", "150300.00"), ("104000.00", "0.00", "110600.60"),
                  ("200000.00", "50000.00", "100821.80"), ("0.00", "-20201.64", "100821.80")]
    for row, values in zip(weeks, checkpoint):
        if tuple(row[k] for k in ("effective_limit", "closing_cash", "closing_debt")) != values:
            raise AssertionError("Financial design checkpoint mismatch")
    result = dict(status="passed", case_id="borrowing_base_002", weeks_compared=len(weeks), invoice_observations_compared=len(invoices),
                  customer_observations_compared=len(customers), reference_sha256=hashlib.sha256(actual_path.read_bytes()).hexdigest(),
                  input_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(INPUTS.iterdir())},
                  method="Integer cents, independent eligibility pipeline, net-position financing; no reference imports",
                  limitations="Both implementations authored in the same AI-assisted session. Rules reviewed by owner; detailed dataset/reference review pending.")
    (ROOT / "reports/borrowing-base-verification.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    verify()
