"""Small executable design checks; not the production reference or a model evaluation."""
import json
from decimal import Decimal as D, ROUND_DOWN, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENT = D("0.01")


def eligibility(amount, days_past_due, disputed=False, related=False):
    if disputed:
        return "disputed"
    if related:
        return "related_party"
    if days_past_due > 60:
        return "over_60_days"
    if amount == 0:
        return "zero_balance"
    return "eligible"


def simulate():
    # Values are already-eligible customer aggregates for hand-checkable examples.
    scenarios = [
        ([150000, 90000, 60000], 20000, 30000),
        ([120000, 40000, 40000], 30000, 40000),
        ([120000, 100000, 100000, 80000], 80000, 20000),
        ([], 20000, 90000),
    ]
    cash, debt = D(60000), D(150000)
    rows = []
    for week, (customers, receipt, payment) in enumerate(scenarios, 1):
        gross = sum(map(D, customers), D(0))
        cap = (gross * D("0.25")).quantize(CENT, rounding=ROUND_DOWN)
        recognized = sum((min(D(v), cap) for v in customers), D(0))
        base = (recognized * D("0.80")).quantize(CENT, rounding=ROUND_DOWN)
        limit = min(D(200000), base)
        interest = (debt * D("0.002")).quantize(CENT, rounding=ROUND_HALF_UP)
        before = cash + D(receipt) - D(payment) - interest
        required = max(debt - limit, D(0))
        cure = min(required, max(before, D(0)))
        remaining_cash, remaining_debt = before - cure, debt - cure
        draw = D(0) if remaining_debt > limit else min(max(D(50000) - remaining_cash, D(0)), max(limit - remaining_debt, D(0)))
        sweep = min(max(remaining_cash - D(50000), D(0)), remaining_debt)
        close_cash, close_debt = remaining_cash + draw - sweep, remaining_debt + draw - sweep
        row = dict(week=week, eligible=gross, concentration_threshold=cap, recognized=recognized,
                   borrowing_base=base, effective_limit=limit, opening_cash=cash, opening_debt=debt,
                   receipts=D(receipt), payments=D(payment), interest=interest, cash_before_financing=before,
                   required_cure=required, actual_cure=cure, draw=draw, voluntary_repayment=sweep,
                   closing_cash=close_cash, closing_debt=close_debt,
                   overadvance=max(close_debt - limit, D(0)), buffer_shortfall=max(D(50000) - close_cash, D(0)),
                   cash_deficit=max(-close_cash, D(0)))
        rows.append({k: f"{v:.2f}" if isinstance(v, D) else v for k, v in row.items()})
        cash, debt = close_cash, close_debt
    return rows


def main():
    rows = simulate()
    # Fixed hand-calculated checkpoints, not generated from the simulation.
    checkpoints = [
        dict(effective_limit="168000.00", interest="300.00", draw="300.00", closing_cash="50000.00", closing_debt="150300.00", overadvance="0.00"),
        dict(effective_limit="104000.00", interest="300.60", required_cure="46300.00", actual_cure="39699.40", closing_cash="0.00", closing_debt="110600.60", overadvance="6600.60"),
        dict(effective_limit="200000.00", interest="221.20", voluntary_repayment="9778.80", closing_cash="50000.00", closing_debt="100821.80", overadvance="0.00"),
        dict(effective_limit="0.00", interest="201.64", actual_cure="0.00", closing_cash="-20201.64", closing_debt="100821.80", overadvance="100821.80"),
    ]
    checks = 0
    for row, expected in zip(rows, checkpoints):
        for field, value in expected.items():
            if row[field] != value:
                raise AssertionError(f"Week {row['week']}: {field} {row[field]} != {value}")
            checks += 1
    for arguments, expected in [((D(100), 60), "eligible"), ((D(100), 61), "over_60_days"),
                                 ((D(100), 0, True, True), "disputed"), ((D(100), 61, False, True), "related_party"),
                                 ((D(0), 0), "zero_balance")]:
        if eligibility(*arguments) != expected:
            raise AssertionError("Eligibility boundary mismatch")
        checks += 1
    report = dict(kind="design_examples_not_model_results", status="passed", checks=checks,
                  review_status="project_owner_review_pending", weeks=rows,
                  limitation="Toy examples with customer aggregates, not the complete invoice-level case or independent financial validation")
    (ROOT / "reports/borrowing-base-design-checks.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
