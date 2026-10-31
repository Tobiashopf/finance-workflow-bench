# bb_release_006 — Collateral-Constrained Treasury Analysis

## Numerical summary (USD)

| Week (close) | S eligible | T | H | BB | L | Interest | B (pre-financing) | Cure Q / U | Draw | Vol. repay | Close cash | Close debt | Unused |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 (2027-01-10) | 400,000.00 | 100,000.00 | 400,000.00 | 320,000.00 | 200,000.00 | 300.00 | 50,000.00 | 0.00 / 0.00 | 0.00 | 0.00 | 50,000.00 | 150,000.00 | 50,000.00 |
| 2 (2027-01-17) | 400,000.00 | 100,000.00 | 400,000.00 | 320,000.00 | 200,000.00 | 300.00 | 50,000.00 | 0.00 / 0.00 | 0.00 | 0.00 | 50,000.00 | 150,000.00 | 50,000.00 |
| 3 (2027-01-24) | 400,000.00 | 100,000.00 | 400,000.00 | 320,000.00 | 200,000.00 | 300.00 | 50,000.00 | 0.00 / 0.00 | 0.00 | 0.00 | 50,000.00 | 150,000.00 | 50,000.00 |
| 4 (2027-01-31) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 300.00 | 219,700.00 | 150,000.00 / 150,000.00 | 0.00 | 0.00 | 69,700.00 | 0.00 | 0.00 |

No week closes with an overadvance, a minimum-cash shortfall or an unfunded cash deficit; all three flags are false in every week, and unpaid cure is zero throughout.

## Material drivers

1. **Weeks 1–3 collateral is ceiling-bound, not base-bound.** Each of the snapshots 2027-01-10, 2027-01-17 and 2027-01-24 contains invoices A-1, B-1, C-1 and D-1 (customers A–D), each USD 100,000.00, due 2027-02-28 (days past due 0), not disputed, not related-party. All twelve observations are `eligible`. S = 400,000.00, so T = floor(0.25 × 400,000.00) = 100,000.00. Each customer is exactly at the threshold, so every concentration deduction is 0.00 and H = 400,000.00. BB = 320,000.00, but L is capped at the 200,000.00 contractual ceiling.

2. **Week 1 cash lands exactly on the buffer.** Payment record `bb_release_006-W1-payment` (9,700.00) plus interest of 300.00 (0.002 × 150,000.00), with zero receipts (`bb_release_006-W1-receipt` = 0.00), take cash from 60,000.00 to exactly 50,000.00. Cash above minimum is zero, so there is no voluntary repayment, and no draw is needed. Weeks 2 and 3 repeat this: receipts `bb_release_006-W2-receipt` and `bb_release_006-W3-receipt` (300.00 each) exactly offset interest of 300.00.

3. **Week 4 collateral collapse.** Snapshot 2027-01-31 is listed in `snapshot_dates.csv` but has no rows in `receivables_snapshots.csv`. Under the rules this is a valid empty snapshot: zero collateral, not permission to carry forward the 2027-01-24 balances. S, T, H, BB and L all become 0.00, so the full 150,000.00 opening debt becomes a required collateral cure. No customer or invoice records are reported for that date because none exist.

4. **Week 4 funding priority.** Receipt `bb_release_006-W4-receipt` (210,000.00), less payment `bb_release_006-W4-payment` (40,000.00) and interest 300.00, gives B = 219,700.00. The mandatory cure ranks ahead of the minimum-cash buffer and is fully payable: U = 150,000.00, leaving post-cure cash 69,700.00 and debt 0.00. No draw is permitted or needed (L − D1 = 0). Voluntary repayment is 0.00 because no debt remains. Closing cash of 69,700.00 is 19,700.00 above the minimum.

## Collateral versus receipts

The receivables snapshots measure *eligible collateral* at each close and are used only for the borrowing base. They are not cash. The disappearance of A-1 through D-1 from the 2027-01-31 snapshot does **not** establish that USD 400,000.00 was collected. Cash comes only from `cash_events.csv`, where week 4 receipts total 210,000.00. Likewise, the USD 320,000.00 borrowing base in weeks 1–3 was not available liquidity beyond the 200,000.00 ceiling, and unused credit was only 50,000.00.

## Violations, stated separately

- **Buffer breach:** none. Cash is exactly 50,000.00 at weeks 1–3, which is not below the minimum.
- **Unfunded deficit:** none. Cash is never negative.
- **Debt above the permitted limit:** a 150,000.00 cure obligation arises at 2027-01-31 (required cure > 0). It is fully paid within the week from scheduled receipts, so the closing overadvance and unpaid cure are 0.00. The obligation existed and was material even though no closing violation remains.

## Eligibility and concentration exceptions

No invoice is disputed, related-party, over 60 days past due, or zero-balance. No concentration deduction occurs: each customer sits exactly at T, the boundary case where `min(E, T)` equals E. The concentration rule would bind if any customer's share rose above 25% of S.

## Assumptions and limitations

- Interest is charged on opening debt and paid at week end. The cure is computed against the same week's closing-snapshot limit.
- All cash events fall inside their dated weeks. Inputs passed validation: no duplicate keys, no invalid flags, dates or amounts.
- Week 1–3 cash is exactly at the floor, so any unscheduled outflow would trigger a buffer breach or a draw. The week 4 outcome depends entirely on the 210,000.00 receipt landing before the cure is assessed. If it slipped, the cure would be largely unpaid.
- Synthetic rules applied as written; no external conventions.
