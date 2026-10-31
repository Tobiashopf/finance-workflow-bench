import csv
import json
import shutil
import tempfile
import unittest
from decimal import Decimal as D
from pathlib import Path

from finance_workflow_bench.reference import financing, money, solve, unique_rows

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "cases/cash_forecast_001/inputs"


class ReferenceTests(unittest.TestCase):
    def test_manual_draw(self):
        result = financing(D("50000"), D("60000"), D("10000"), D("20000"), D("50000"), D("200000"), D("0.002"))
        self.assertEqual(result["interest_paid"], D("120"))
        self.assertEqual(result["credit_draw"], D("10120"))
        self.assertEqual(result["closing_cash"], D("50000"))
        self.assertEqual(result["closing_principal"], D("70120"))

    def test_manual_repayment(self):
        result = financing(D("50000"), D("60000"), D("40000"), D("10000"), D("50000"), D("200000"), D("0.002"))
        self.assertEqual(result["principal_repayment"], D("29880"))
        self.assertEqual(result["closing_principal"], D("30120"))

    def test_manual_insufficient_credit(self):
        result = financing(D("50000"), D("190000"), D("10000"), D("80000"), D("50000"), D("200000"), D("0.002"))
        self.assertEqual(result["credit_draw"], D("10000"))
        self.assertEqual(result["closing_cash"], D("-10380"))
        self.assertEqual(result["minimum_cash_shortfall"], D("60380"))
        self.assertEqual(result["unfunded_cash_deficit"], D("10380"))

    def test_half_cent_rounds_up(self):
        result = financing(D("50000"), D("2.50"), D("0"), D("0"), D("50000"), D("200000"), D("0.002"))
        self.assertEqual(result["interest_paid"], D("0.01"))

    def test_nonfinite_negative_and_imprecise_inputs(self):
        for value in ["NaN", "Infinity", "-1.00", "1.001", "1e2", "", "1,000.00"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                money(value)

    def test_conflicting_duplicates(self):
        with self.assertRaises(ValueError):
            unique_rows([dict(record_id="A", invoice_id="I", x="1"), dict(record_id="A", invoice_id="I", x="2")], "invoice_id", "test")

    def test_repeated_business_id(self):
        with self.assertRaises(ValueError):
            unique_rows([dict(record_id="A", invoice_id="I"), dict(record_id="B", invoice_id="I")], "invoice_id", "test")

    def test_full_case_invariants_and_trace(self):
        forecast, ledger = solve(INPUTS)
        self.assertEqual(sum(x["discarded_count"] for x in forecast["duplicates_removed"]), 5)
        self.assertEqual(len(forecast["exclusions"]), 7)
        # Identical amount/date does not make distinct invoices duplicates.
        self.assertEqual(forecast["weeks"][0]["receipts"], "45000.00")
        self.assertEqual(forecast["weeks"][-1]["receipts"], "95000.00")
        for week in forecast["weeks"]:
            n = week["week"]
            for field in {x["field"] for x in ledger}:
                total = sum((D(x["amount"]) for x in ledger if x["week"] == n and x["field"] == field), D(0))
                self.assertEqual(total, D(week[field]))
            self.assertFalse(D(week["credit_draw"]) > 0 and D(week["principal_repayment"]) > 0)
            self.assertLessEqual(D(week["closing_principal"]), D("200000"))
            if n > 1:
                self.assertEqual(week["opening_cash"], forecast["weeks"][n - 2]["closing_cash"])
                self.assertEqual(week["opening_principal"], forecast["weeks"][n - 2]["closing_principal"])

    def test_invalid_input_mutations(self):
        for field, bad in [("paid_before_as_of", "999999.00"), ("expected_receipt_date", "2027-01-03"), ("expected_receipt_date", "2027-02-30"), ("customer_id", "")]:
            with self.subTest(field=field, bad=bad), tempfile.TemporaryDirectory() as temp:
                destination = Path(temp) / "inputs"
                shutil.copytree(INPUTS, destination)
                path = destination / "receivables.csv"
                with path.open(encoding="utf-8", newline="") as f:
                    reader = csv.DictReader(f)
                    rows, fields = list(reader), reader.fieldnames
                rows[0][field] = bad
                with path.open("w", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(rows)
                with self.assertRaises(ValueError):
                    solve(destination)

    def test_zero_debt_does_not_force_cash_to_minimum(self):
        result = financing(D("90000"), D("0"), D("0"), D("0"), D("50000"), D("200000"), D("0.002"))
        self.assertEqual(result["closing_cash"], D("90000"))
        self.assertEqual(result["principal_repayment"], D("0"))


if __name__ == "__main__":
    unittest.main()

