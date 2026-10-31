# Borrowing Base 002 — Four-Week Forecast (USD)

## Summary

| Close | S | T | H | Limit L | Interest | Cure paid/unpaid | Draw/vol. repay | Closing cash | Closing debt |
|---|---|---|---|---|---|---|---|---|---|
| 2027-01-10 | 300,000.00 | 75,000.00 | 210,000.00 | 168,000.00 | 300.00 | 0/0 | 300.00/0 | 50,000.00 | 150,300.00 |
| 2027-01-17 | 200,000.00 | 50,000.00 | 130,000.00 | 104,000.00 | 300.60 | 39,699.40/6,600.60 | 0/0 | 0.00 | 110,600.60 |
| 2027-01-24 | 400,000.00 | 100,000.00 | 380,000.00 | 200,000.00 | 221.20 | 0/0 | 0/9,778.80 | 50,000.00 | 100,821.80 |
| 2027-01-31 | 0.00 | 0.00 | 0.00 | 0.00 | 201.64 | 0/100,821.80 | 0/0 | −20,201.64 | 100,821.80 |

Receipts (CASH-R-1…4): 20,000 / 30,000 / 80,000 / 20,000. Payments (CASH-P-1…4): 30,000 / 40,000 / 20,000 / 90,000. Unused credit: 17,700.00 / 0.00 / 99,178.20 / 0.00.

## Material drivers

1. **2027-01-10 — age boundary and concentration.** A-EDGE (due 2026-11-11) is exactly 60 days past due and stays eligible. Z-OLD (due 2026-11-10, 61 days) is excluded. S = 300,000 (A 150,000; B 90,000; C 60,000). T = 75,000 caps A (deduction 75,000) and B (deduction 15,000), giving H = 210,000 and BB = 168,000. Cash before financing is 49,700.00, so the forecast draws 300.00 to restore the minimum.
2. **2027-01-17 — collateral contraction and partial cure.** A-EDGE ages to 67 days and is excluded. B-CORE and C-CORE fall to 40,000 each, and A-NEW (20,000) appears. T = 50,000 caps A (deduction 70,000). L = 104,000 against debt of 150,300.00 creates a required cure of 46,300.00. The cure ranks ahead of the cash buffer and uses all 39,699.40 of available cash. Closing cash is 0.00, and 6,600.60 of the cure is unpaid, which is also the overadvance. No draw is allowed.
3. **2027-01-24 — recovery.** B-CORE and C-CORE rise to 100,000 each, and D-NEW (80,000) appears. C-CORE is 4 days past due and remains eligible. A is capped at T = 100,000 (deduction 20,000), giving BB = 304,000, so the 200,000 ceiling binds. The overadvance clears because the limit rose, not because cash arrived. CASH-R-3 lifts cash before financing to 59,778.80; the 9,778.80 above the minimum repays debt voluntarily.
4. **2027-01-31 — empty snapshot.** This is a required snapshot date with no invoice rows, so collateral and the limit are zero. Earlier balances are not reused, and debt of 100,821.80 remains. CASH-P-4 drives cash before financing to −20,201.64. Negative cash cannot fund a cure, so the full 100,821.80 cure is unpaid.

## Eligibility and concentration exceptions

- X-DISPUTE and X-MULTI are `disputed`. X-MULTI is also related-party and over 60 days, but disputed takes precedence.
- Y-RELATED and Y-MULTI are `related_party`, which outranks Y-MULTI's age and zero balance.
- Z-OLD is `over_60_days` on every date. A-EDGE is `over_60_days` from 2027-01-17. Z-ZERO is `zero_balance`.
- Customers X, Y and Z are reported with zero eligible, recognized and deducted amounts and the shared T. Excluded invoices never enter S.
- The cap is applied once against the original S, not recursively. Concentration deductions are neither write-offs nor cash.

## Collateral versus receipts

Snapshots are closing receivable states used only to size the borrowing base. Cash comes only from `cash_events.csv`. B-CORE falling from 90,000 to 40,000 is not a 50,000 receipt. Its later rise is not an outflow, and the empty 2027-01-31 snapshot is not a collection. A higher base adds borrowing capacity, not cash.

## Separate violations

- **Unpaid cure / overadvance:** 6,600.60 (2027-01-17); 100,821.80 (2027-01-31).
- **Minimum-cash shortfall:** 50,000.00 (2027-01-17); 70,201.64 (2027-01-31).
- **Unfunded cash deficit:** 20,201.64 (2027-01-31 only). This is a projected deficit, not an authorized overdraft.

The 2027-01-17 cure failure is a funding failure. The week-3 recovery does not show that operations could have continued without resolving it.

## Assumptions and limitations

- All inputs passed validation: there were no duplicate keys, bad flags, negative amounts, missing fields or out-of-horizon cash dates. The empty 2027-01-31 snapshot is listed in `snapshot_dates.csv` and is treated as valid.
- Weeks run Monday–Sunday from 2027-01-04. Interest is 0.2% of opening debt, rounded half up. T and BB are floored to the cent.
- No refinancing, waivers, deferrals, fees or penalty interest are modeled.
- The execution note was titled "Cash Forecast 001", but the package's task, schema and inputs define `borrowing_base_002`, so that case was solved.
