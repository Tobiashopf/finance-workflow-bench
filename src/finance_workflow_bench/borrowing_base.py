"""Invoice-level Decimal reference and fixed output contract for case 002."""
import csv
import json
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal as D, ROUND_DOWN, ROUND_HALF_UP
from pathlib import Path

from .reference import money, iso_date
from .schemas import object_schema, validate_subset

ROOT = Path(__file__).resolve().parents[2]
CASE = "borrowing_base_002"
INPUTS = ROOT / "cases" / CASE / "inputs"
DATES = [(date(2027, 1, 10) + timedelta(weeks=i)).isoformat() for i in range(4)]
CENT = D("0.01")
COLLATERAL = ["eligible"]
CONCENTRATION = ["concentration_threshold", "recognized", "borrowing_base", "effective_limit"]
CASH = ["opening_cash", "opening_debt", "receipts", "payments", "interest", "cash_before_financing",
        "required_cure", "actual_cure", "draw", "voluntary_repayment", "closing_cash", "closing_debt", "unused_credit"]
VIOLATIONS = ["unpaid_cure", "overadvance", "buffer_shortfall", "cash_deficit"]
FLAGS = ["overadvance_present", "buffer_breached", "unfunded_deficit"]
MONEY = COLLATERAL + CONCENTRATION + CASH + VIOLATIONS
REASONS = ["eligible", "disputed", "related_party", "over_60_days", "zero_balance"]


def read_csv(folder, filename, fields):
    with (folder / filename).open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != fields.split():
            raise ValueError(f"Unexpected CSV header: {filename}")
        rows = list(reader)
    if any(None in r or any(v in (None, "") for v in r.values()) for r in rows):
        raise ValueError(f"Missing or extra fields in {filename}")
    return rows


def reason(amount, age, disputed, related):
    if disputed:
        return "disputed"
    if related:
        return "related_party"
    if age > 60:
        return "over_60_days"
    return "zero_balance" if amount == 0 else "eligible"


def concentration(amounts):
    total = sum(amounts, D(0))
    threshold = (total * D("0.25")).quantize(CENT, rounding=ROUND_DOWN)
    recognized = sum((min(v, threshold) for v in amounts), D(0))
    base = (recognized * D("0.80")).quantize(CENT, rounding=ROUND_DOWN)
    return total, threshold, recognized, base, min(D(200000), base)


def waterfall(cash, debt, receipts, payments, limit):
    interest = (debt * D("0.002")).quantize(CENT, rounding=ROUND_HALF_UP)
    before = cash + receipts - payments - interest
    required = max(debt - limit, D(0))
    cure = min(required, max(before, D(0)))
    c1, d1 = before - cure, debt - cure
    unpaid = max(d1 - limit, D(0))
    draw = D(0) if unpaid else min(max(D(50000) - c1, D(0)), max(limit - d1, D(0)))
    sweep = min(max(c1 - D(50000), D(0)), d1)
    end_cash, end_debt = c1 + draw - sweep, d1 + draw - sweep
    return dict(opening_cash=cash, opening_debt=debt, receipts=receipts, payments=payments, interest=interest,
                cash_before_financing=before, required_cure=required, actual_cure=cure, unpaid_cure=unpaid,
                draw=draw, voluntary_repayment=sweep, closing_cash=end_cash, closing_debt=end_debt,
                unused_credit=max(limit-end_debt, D(0)), overadvance=max(end_debt-limit, D(0)),
                buffer_shortfall=max(D(50000)-end_cash, D(0)), cash_deficit=max(-end_cash, D(0)),
                overadvance_present=end_debt > limit, buffer_breached=end_cash < 50000, unfunded_deficit=end_cash < 0)


def formatted(row):
    return {k: f"{v:.2f}" if isinstance(v, D) else v for k, v in row.items()}


def solve(folder=INPUTS, *, case_id=CASE, opening_contract=None):
    folder = Path(folder)
    opening = json.loads((folder / "opening_position.json").read_text(encoding="utf-8"))
    contract = opening_contract if opening_contract is not None else dict(as_of_date="2027-01-03", currency="USD", cash="60000.00", debt="150000.00")
    if opening != contract:
        raise ValueError("Opening position differs from fixed case contract")
    facility = json.loads((folder / "facility.json").read_text(encoding="utf-8"))
    expected_facility = dict(currency="USD", contractual_ceiling="200000.00", minimum_cash="50000.00",
                             weekly_interest_rate="0.002", max_days_past_due=60, concentration_rate="0.25", advance_rate="0.80",
                             collateral_rounding="ROUND_DOWN_to_cent", interest_rounding="ROUND_HALF_UP_to_cent",
                             cure_priority="before_minimum_cash", fees="0.00")
    if facility != expected_facility:
        raise ValueError("Facility differs from fixed case contract")
    snapshots = read_csv(folder, "snapshot_dates.csv", "snapshot_date")
    if sorted(r["snapshot_date"] for r in snapshots) != DATES:
        raise ValueError("Four unique snapshot dates are required")
    flows = [dict(receipts=D(0), payments=D(0)) for _ in DATES]
    seen = set()
    for r in read_csv(folder, "cash_events.csv", "record_id cash_date direction amount description"):
        if r["record_id"] in seen:
            raise ValueError("Duplicate cash event")
        seen.add(r["record_id"])
        index = (iso_date(r["cash_date"]) - date(2027, 1, 4)).days // 7
        if not 0 <= index < 4 or r["direction"] not in ("receipt", "payment"):
            raise ValueError("Cash event outside horizon or invalid direction")
        flows[index][r["direction"] + "s"] += money(r["amount"])
    customers = {d: defaultdict(lambda: D(0)) for d in DATES}
    checks, identities = [], set()
    for r in read_csv(folder, "receivables_snapshots.csv", "snapshot_date invoice_id customer_id due_date outstanding_amount disputed related_party"):
        key = (r["snapshot_date"], r["invoice_id"])
        if key in identities or r["snapshot_date"] not in DATES:
            raise ValueError("Duplicate invoice observation or unknown snapshot")
        identities.add(key)
        if r["disputed"] not in ("true", "false") or r["related_party"] not in ("true", "false"):
            raise ValueError("Invalid boolean flag")
        amount = money(r["outstanding_amount"])
        age = max((iso_date(r["snapshot_date"]) - iso_date(r["due_date"])).days, 0)
        decision = reason(amount, age, r["disputed"] == "true", r["related_party"] == "true")
        eligible = amount if decision == "eligible" else D(0)
        customers[r["snapshot_date"]][r["customer_id"]] += eligible
        checks.append(formatted(dict(snapshot_date=r["snapshot_date"], invoice_id=r["invoice_id"], customer_id=r["customer_id"],
                                     days_past_due=age, outstanding_amount=amount, eligible_amount=eligible, reason=decision)))
    weeks, customer_checks = [], []
    cash, debt = money(opening["cash"]), money(opening["debt"])
    for i, snapshot in enumerate(DATES):
        total, threshold, recognized, base, limit = concentration(list(customers[snapshot].values()))
        for customer, amount in sorted(customers[snapshot].items()):
            value = min(amount, threshold)
            customer_checks.append(formatted(dict(snapshot_date=snapshot, customer_id=customer, eligible_amount=amount,
                                                  concentration_threshold=threshold, recognized_amount=value, concentration_deduction=amount-value)))
        row = dict(week=i+1, snapshot_date=snapshot, eligible=total, concentration_threshold=threshold, recognized=recognized,
                   borrowing_base=base, effective_limit=limit, **waterfall(cash, debt, flows[i]["receipts"], flows[i]["payments"], limit))
        cash, debt = row["closing_cash"], row["closing_debt"]
        weeks.append(formatted(row))
    result = dict(case_id=case_id, currency="USD", weeks=weeks,
                  invoice_checks=sorted(checks, key=lambda r: (r["snapshot_date"], r["invoice_id"])), customer_checks=customer_checks)
    if validate(result, case_id=case_id):
        raise ValueError(f"Reference schema error: {validate(result, case_id=case_id)}")
    return result


def schema(case_id=CASE):
    text = dict(type="string", minLength=1, maxLength=128)
    day = dict(type="string", enum=DATES)
    monetary = lambda signed=False: dict(type="string", pattern=r"^-?[0-9]{1,16}\.[0-9]{2}$" if signed else r"^[0-9]{1,16}\.[0-9]{2}$")
    week = dict(week=dict(type="integer", minimum=1, maximum=4), snapshot_date=day)
    week.update({k: monetary(k in ("opening_cash", "cash_before_financing", "closing_cash")) for k in MONEY})
    week.update({k: dict(type="boolean") for k in FLAGS})
    invoice = dict(snapshot_date=day, invoice_id=text, customer_id=text, days_past_due=dict(type="integer", minimum=0, maximum=4000000),
                   outstanding_amount=monetary(), eligible_amount=monetary(), reason=dict(type="string", enum=REASONS))
    customer = dict(snapshot_date=day, customer_id=text, **{k: monetary() for k in ("eligible_amount", "concentration_threshold", "recognized_amount", "concentration_deduction")})
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": "Borrowing Base 002", **object_schema(dict(
        case_id=dict(type="string", const=case_id), currency=dict(type="string", const="USD"),
        weeks=dict(type="array", minItems=4, maxItems=4, items=object_schema(week)),
        invoice_checks=dict(type="array", maxItems=1000, items=object_schema(invoice)),
        customer_checks=dict(type="array", maxItems=1000, items=object_schema(customer))))}


def validate(candidate, *, case_id=CASE):
    errors = validate_subset(candidate, schema(case_id))
    if errors:
        return errors
    for i, r in enumerate(candidate["weeks"]):
        if r["week"] != i+1 or r["snapshot_date"] != DATES[i]:
            errors.append(dict(path=f"weeks[{i}]", message="Week/date order mismatch"))
    for key, identity in [("invoice_checks", "invoice_id"), ("customer_checks", "customer_id")]:
        seen = set()
        for i, r in enumerate(candidate[key]):
            ident = (r["snapshot_date"], r[identity])
            if ident in seen:
                errors.append(dict(path=f"{key}[{i}]", message="Duplicate snapshot identity"))
            seen.add(ident)
    return errors


if __name__ == "__main__":
    destination = ROOT / "reference" / CASE
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "forecast.json").write_text(json.dumps(solve(), indent=2)+"\n", encoding="utf-8")
    (ROOT / "schemas/borrowing_base_002.schema.json").write_text(json.dumps(schema(), indent=2)+"\n", encoding="utf-8")
    print("Case 002 reference and schema written.")
