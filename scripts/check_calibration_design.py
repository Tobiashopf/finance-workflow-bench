"""Check isolated calibration design examples, not complete cases or model runs."""
import json
import sys
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from finance_workflow_bench.borrowing_base import concentration, waterfall


def cents_waterfall(cash, debt, receipts, payments, limit):
    # Nonnegative opening debt; 0.2% interest, half-up in cents.
    interest = (debt + 250) // 500
    before = cash + receipts - payments - interest
    required = max(debt - limit, 0)
    cure = min(required, max(before, 0))
    remaining = debt - cure
    available = before - cure
    if remaining > limit:
        draw = 0
    else:
        draw = min(max(5000000 - available, 0), limit - remaining)
    repayment = min(max(available - 5000000, 0), remaining)
    end_cash = available + draw - repayment
    end_debt = remaining + draw - repayment
    return dict(interest=interest, cash_before_financing=before,
                required_cure=required, actual_cure=cure, draw=draw,
                voluntary_repayment=repayment, closing_cash=end_cash,
                closing_debt=end_debt, overadvance=max(end_debt-limit, 0),
                buffer_shortfall=max(5000000-end_cash, 0),
                cash_deficit=max(-end_cash, 0))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    rows = []
    for name, amounts, expected in [
        ("rounding", [10000003, 8000002, 6000001], [24000006, 6000001, 18000003, 14400002, 14400002]),
        ("customer_aggregation", [12000000, 4000000, 4000000, 4000000], [24000000, 6000000, 18000000, 14400000, 14400000]),
    ]:
        total = sum(amounts)
        cap = total // 4
        recognized = sum(min(x, cap) for x in amounts)
        base = recognized * 4 // 5
        integer = [total, cap, recognized, base, min(20000000, base)]
        decimal = [int(x * 100) for x in concentration([D(x)/100 for x in amounts])]
        require(integer == decimal == expected, name)
        rows.append(dict(check=name, result_cents=integer, passed=True))
    for name, args, expected in [
        ("full_cure_and_sweep", [6000000, 15000000, 8000000, 4000000, 10400000],
         dict(closing_cash=5000000, closing_debt=10030000, actual_cure=4600000, voluntary_repayment=370000)),
        ("full_cure_buffer_breach", [6000000, 15000000, 7000000, 4000000, 10400000],
         dict(closing_cash=4370000, closing_debt=10400000, actual_cure=4600000, buffer_shortfall=630000, overadvance=0, cash_deficit=0)),
        ("zero_collateral_solvent", [6000000, 15000000, 20000000, 4000000, 0],
         dict(closing_cash=6970000, closing_debt=0, actual_cure=15000000, buffer_shortfall=0, cash_deficit=0)),
        ("half_cent_interest", [6000000, 15000250, 0, 0, 20000000], dict(interest=30001)),
    ]:
        integer = cents_waterfall(*args)
        decimal = waterfall(*(D(x)/100 for x in args))
        require(all(D(value)/100 == decimal[key] for key, value in integer.items()), name + " cross-check")
        require(all(integer[key] == value for key, value in expected.items()), name + " checkpoint")
        rows.append(dict(check=name, result_cents=integer, passed=True))
    report = dict(kind="design_checks_not_model_results", status="passed", checks=rows,
                  limitations="Isolated examples only. Full cases, schemas, graders and packages remain to be built. Both implementations are AI-assisted, not independent human validation.")
    destination = ROOT / "reports" / "calibration-design-checks.json"
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(status="passed", design_examples=len(rows))))


if __name__ == "__main__":
    main()
