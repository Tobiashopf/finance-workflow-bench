"""Original deterministic invoice-level fixture for borrowing_base_002."""
import csv
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "cases/borrowing_base_002/inputs"


def write_csv(name, fields, rows):
    with (DEST / name).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields.split())
        writer.writeheader()
        writer.writerows(rows)


def build():
    DEST.mkdir(parents=True, exist_ok=True)
    dates = [date(2027, 1, 10) + timedelta(weeks=i) for i in range(4)]
    write_csv("snapshot_dates.csv", "snapshot_date", [dict(snapshot_date=d.isoformat()) for d in dates])
    rows = []

    def invoice(week, identity, customer, amount, due, disputed=False, related=False):
        rows.append(dict(snapshot_date=dates[week - 1].isoformat(), invoice_id=identity, customer_id=customer,
                         due_date=due, outstanding_amount=f"{amount:.2f}", disputed=str(disputed).lower(), related_party=str(related).lower()))

    # Same invoice identity across snapshots is legitimate. A-EDGE crosses the aging threshold.
    for week in (1, 2, 3):
        invoice(week, "A-CORE", "A", 100000, "2027-02-10")
        invoice(week, "A-EDGE", "A", 50000, "2026-11-11")
        if week > 1:
            invoice(week, "A-NEW", "A", 20000, "2027-02-20")
        invoice(week, "B-CORE", "B", [90000, 40000, 100000][week - 1], "2027-02-01")
        invoice(week, "C-CORE", "C", [60000, 40000, 100000][week - 1], "2027-01-20")
        if week == 3:
            invoice(week, "D-NEW", "D", 80000, "2027-02-20")
        invoice(week, "X-DISPUTE", "X", 90000, "2027-02-01", disputed=True)
        invoice(week, "Y-RELATED", "Y", 70000, "2027-02-01", related=True)
        invoice(week, "Z-OLD", "Z", 40000, "2026-11-10")
        invoice(week, "Z-ZERO", "Z", 0, "2027-02-01")
        # Reason precedence: both flags true and overdue; disputed wins.
        invoice(week, "X-MULTI", "X", 12000, "2026-10-01", disputed=True, related=True)
        invoice(week, "Y-MULTI", "Y", 0, "2026-10-01", related=True)
    # The fourth snapshot is explicitly present in snapshot_dates but has no invoice rows.
    write_csv("receivables_snapshots.csv", "snapshot_date invoice_id customer_id due_date outstanding_amount disputed related_party", rows)
    cash_rows = []
    for week, (receipt, payment) in enumerate(zip([20000, 30000, 80000, 20000], [30000, 40000, 20000, 90000]), 1):
        monday = dates[week - 1] - timedelta(days=6)
        cash_rows.extend([
            dict(record_id=f"CASH-R-{week}", cash_date=(monday + timedelta(days=2)).isoformat(), direction="receipt", amount=f"{receipt:.2f}", description="Scheduled customer collections; use this cash event independently of collateral snapshots"),
            dict(record_id=f"CASH-P-{week}", cash_date=(monday + timedelta(days=4)).isoformat(), direction="payment", amount=f"{payment:.2f}", description="Required operating payments"),
        ])
    write_csv("cash_events.csv", "record_id cash_date direction amount description", cash_rows)
    opening = dict(as_of_date="2027-01-03", currency="USD", cash="60000.00", debt="150000.00")
    facility = dict(currency="USD", contractual_ceiling="200000.00", minimum_cash="50000.00",
                    weekly_interest_rate="0.002", max_days_past_due=60, concentration_rate="0.25", advance_rate="0.80",
                    collateral_rounding="ROUND_DOWN_to_cent", interest_rounding="ROUND_HALF_UP_to_cent",
                    cure_priority="before_minimum_cash", fees="0.00")
    for name, value in [("opening_position.json", opening), ("facility.json", facility)]:
        (DEST / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Created five inputs: {len(rows)} invoice observations and {len(cash_rows)} cash events.")


if __name__ == "__main__":
    build()
