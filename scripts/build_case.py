"""Rebuild the original synthetic fixture; no external data or randomness."""
import csv
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "cases/cash_forecast_001/inputs"
START = date(2027, 1, 4)


def write_csv(name, fields, rows):
    with (DEST / name).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields.split())
        writer.writeheader()
        writer.writerows(rows)


def build():
    DEST.mkdir(parents=True, exist_ok=True)
    write_csv("opening_balances.csv", "account_id as_of_date available_balance", [
        dict(account_id="BANK-OPERATING", as_of_date="2027-01-03", available_balance="65000.00"),
        dict(account_id="BANK-COLLECTIONS", as_of_date="2027-01-03", available_balance="15000.00"),
    ])
    receipts = [45000, 55000, 65000, 40000, 35000, 30000, 180000, 160000, 90000, 80000, 75000, 100000, 95000]
    suppliers = [35000, 40000, 45000, 80000, 120000, 75000, 35000, 40000, 45000, 50000, 40000, 45000, 40000]
    ar, ap, recurring = [], [], []
    for week, (receipt, supplier) in enumerate(zip(receipts, suppliers), 1):
        monday = START + timedelta(weeks=week - 1)
        # First and last horizon dates are deliberately represented.
        receipt_date = monday if week == 1 else monday + timedelta(days=6 if week == 13 else 2)
        for suffix in ("A", "B"):
            partial = 10000 if week == 3 and suffix == "A" else 0
            ar.append(dict(record_id=f"AR-{week:02d}-{suffix}", invoice_id=f"INV-{week:02d}-{suffix}",
                           customer_id=f"CUSTOMER-{suffix}", invoice_amount=f"{receipt // 2 + partial:.2f}",
                           paid_before_as_of=f"{partial:.2f}", expected_receipt_date=receipt_date.isoformat()))
        partial = 15000 if week == 4 else 0
        ap.append(dict(record_id=f"AP-{week:02d}", obligation_id=f"SUP-{week:02d}", category="supplier",
                       gross_amount=f"{supplier + partial:.2f}", paid_before_as_of=f"{partial:.2f}",
                       payment_date=(monday + timedelta(days=4)).isoformat()))
        if week in (3, 6, 9, 12):
            ap.append(dict(record_id=f"TAX-{week:02d}", obligation_id=f"TAX-DUE-{week:02d}", category="tax",
                           gross_amount="12000.00", paid_before_as_of="0.00", payment_date=(monday + timedelta(days=3)).isoformat()))
        if week in (4, 6):
            ap.append(dict(record_id=f"FREIGHT-{week:02d}", obligation_id=f"FREIGHT-DUE-{week:02d}", category="other_external",
                           gross_amount="5000.00", paid_before_as_of="0.00", payment_date=monday.isoformat()))
        for category, amount in [("other_recurring", 2000)] + ([("payroll", 24000)] if week % 2 == 0 else []) + ([("rent", 8000)] if week in (1, 5, 9) else []):
            recurring.append(dict(record_id=f"{category.upper()}-{week:02d}", expense_id=f"EXP-{category}-{week:02d}",
                                  category=category, cash_date=(monday + timedelta(days=4)).isoformat(), amount=f"{amount:.2f}"))
    ar.extend([
        dict(record_id="AR-PAID", invoice_id="INV-PAID", customer_id="CUSTOMER-C", invoice_amount="9000.00", paid_before_as_of="9000.00", expected_receipt_date="2027-04-05"),
        dict(record_id="AR-FUTURE", invoice_id="INV-FUTURE", customer_id="CUSTOMER-C", invoice_amount="42000.00", paid_before_as_of="0.00", expected_receipt_date="2027-04-05"),
    ])
    ap.extend([
        dict(record_id="TRANSFER-01", obligation_id="TRANSFER-INTERNAL-01", category="internal_transfer", gross_amount="25000.00", paid_before_as_of="0.00", payment_date="2027-02-05"),
        dict(record_id="TRANSFER-FUTURE", obligation_id="TRANSFER-INTERNAL-02", category="internal_transfer", gross_amount="15000.00", paid_before_as_of="0.00", payment_date="2027-04-05"),
        dict(record_id="AP-PAID", obligation_id="SUP-PAID", category="supplier", gross_amount="7000.00", paid_before_as_of="7000.00", payment_date="2027-01-08"),
        dict(record_id="AP-FUTURE", obligation_id="SUP-FUTURE", category="supplier", gross_amount="30000.00", paid_before_as_of="0.00", payment_date="2027-04-05"),
    ])
    recurring.append(dict(record_id="RENT-FUTURE", expense_id="EXP-RENT-FUTURE", category="rent", cash_date="2027-04-05", amount="8000.00"))
    # Exact duplicates, including an excluded event; equal-value distinct invoices remain legitimate.
    ar.extend([dict(ar[4]), dict(ar[4]), dict(ar[-1])])
    ap.append(dict(ap[3]))
    recurring.append(dict(recurring[0]))
    write_csv("receivables.csv", "record_id invoice_id customer_id invoice_amount paid_before_as_of expected_receipt_date", ar)
    write_csv("payables.csv", "record_id obligation_id category gross_amount paid_before_as_of payment_date", ap)
    write_csv("recurring_expenses.csv", "record_id expense_id category cash_date amount", recurring)
    (DEST / "credit_facility.json").write_text(json.dumps(dict(currency="USD", credit_limit="200000.00", opening_principal="60000.00", weekly_interest_rate="0.002000", minimum_cash="50000.00", interest_basis="opening_week_principal", interest_payment="end_of_each_week", fees="0.00"), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
    print("Created five synthetic input files.")
