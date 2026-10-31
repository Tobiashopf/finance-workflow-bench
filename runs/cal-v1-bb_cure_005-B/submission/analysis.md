# bb_cure_005 — Collateral-Constrained Treasury Forecast

## Numerical summary (USD)

| Week (close) | S eligible | T | H recognized | BB | L | Interest | Cure paid | Draw | Vol. repay | Closing cash | Closing debt | Buffer shortfall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 (2027-01-10) | 200,000.00 | 50,000.00 | 130,000.00 | 104,000.00 | 104,000.00 | 300.00 | 46,000.00 | 0.00 | 0.00 | 43,700.00 | 104,000.00 | 6,300.00 |
| 2 (2027-01-17) | 400,000.00 | 100,000.00 | 400,000.00 | 320,000.00 | 200,000.00 | 208.00 | 0.00 | 0.00 | 3,492.00 | 50,000.00 | 100,508.00 | 0.00 |
| 3 (2027-01-24) | 200,000.00 | 50,000.00 | 130,000.00 | 104,000.00 | 104,000.00 | 201.02 | 0.00 | 3,492.00 | 0.00 | 43,290.98 | 104,000.00 | 6,709.02 |
| 4 (2027-01-31) | 400,000.00 | 100,000.00 | 400,000.00 | 320,000.00 | 200,000.00 | 208.00 | 0.00 | 0.00 | 63,082.98 | 50,000.00 | 40,917.02 | 0.00 |

Violations, reported separately:

- **Minimum-cash buffer breaches:** week 1 (shortfall 6,300.00) and week 3 (shortfall 6,709.02).
- **Unfunded cash deficits:** none; closing cash is positive every week.
- **Debt above the permitted limit (overadvance / unpaid cure):** none at any close. Week 1 had a required cure of 46,000.00, but it was paid in full from available cash.

## Material drivers

1. **Concentration of customer A on 2027-01-10 and 2027-01-24.** Each of these snapshots has three eligible invoices: A-1 (120,000.00), B-1 (40,000.00) and C-1 (40,000.00), so S = 200,000.00 and T = floor(0.25 × 200,000.00) = 50,000.00. Customer A is capped at 50,000.00, a concentration deduction of 70,000.00. H = 130,000.00, BB = 104,000.00, and L = 104,000.00. B and C sit below T and are recognized in full.
2. **Week 1 collateral cure (2027-01-10).** Opening debt of 150,000.00 exceeds L = 104,000.00, so Q = 46,000.00. Cash before financing is 89,700.00 (60,000.00 + receipt `bb_cure_005-W1-receipt` 70,000.00 − payment `bb_cure_005-W1-payment` 40,000.00 − interest 300.00). The cure ranks ahead of the buffer, so the full 46,000.00 is repaid. That leaves 43,700.00 in cash. No draw is possible because debt equals L (no headroom). Result: a buffer breach of 6,300.00, but no overadvance and no deficit.
3. **Limit rises on 2027-01-17 and 2027-01-31.** These snapshots have four equal invoices (A-1, B-1, C-1, D-1, 100,000.00 each). Customer D appears only on these dates. S = 400,000.00, T = 100,000.00, no customer is above T, and H = 400,000.00. BB = 320,000.00, but L is capped at the contractual 200,000.00 ceiling. In week 2, cash before financing is 53,492.00 (receipt `bb_cure_005-W2-receipt` 10,000.00, zero-amount payment `bb_cure_005-W2-payment`, interest 208.00). The 3,492.00 above the minimum goes to voluntary repayment. In week 4, receipt `bb_cure_005-W4-receipt` of 80,000.00 less payment `bb_cure_005-W4-payment` of 10,000.00 funds a voluntary repayment of 63,082.98.
4. **Week 3 limit drop (2027-01-24).** L falls back to 104,000.00 because D-1 is absent and A is concentrated again. Debt of 100,508.00 is below L, so no cure is required. Cash before financing is 39,798.98 (receipt `bb_cure_005-W3-receipt` 10,000.00, payment `bb_cure_005-W3-payment` 20,000.00, interest 201.02, which is 0.002 × 100,508.00 = 201.016 rounded half up). The buffer needs 10,201.02, but only 3,492.00 of headroom exists. The draw is therefore limited to 3,492.00, debt reaches exactly 104,000.00, and the buffer is short by 6,709.02.

## Eligibility and concentration exceptions

All 14 invoice observations are `eligible`. No invoice is disputed or related-party, and all are due 2027-02-28, so days past due is 0 everywhere. There are no zero balances. Every collateral reduction in this case comes from concentration, not ineligibility. The concentration deduction (70,000.00 for A on 2027-01-10 and 2027-01-24) is not a write-off and not a cash flow. Customer D is listed in customer checks only on the snapshots where it appears. It is not carried into the 2027-01-10 or 2027-01-24 snapshots.

## Collateral versus receipts

Receivables snapshots are independent closing balances used only to size the borrowing base. Cash comes solely from the dated records in `cash_events.csv`. For example, A-1's balance moves from 120,000.00 to 100,000.00 to 120,000.00 across snapshots, and D-1 appears and disappears. None of these changes creates or removes cash. Each week's waterfall uses only that week's receipt and payment records.

## Funding priorities and limitations

Order applied: interest, then mandatory cure (ahead of the buffer, limited to existing cash), then a buffer draw (limited to headroom, blocked by any unpaid cure), then voluntary repayment from cash above the minimum.

- Inputs validated: unique keys, valid flags and dates, nonnegative amounts, cash dates inside the horizon, four snapshot dates.
- Only `task.md`/`facility.json` rules used; no fees, penalties, refinancing or waivers. No collection probability is modelled.
- The buffer breaches are real liquidity issues even without a debt-limit violation; A's concentration leaves zero unused credit in weeks 1 and 3.
