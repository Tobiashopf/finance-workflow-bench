# bb_rounding_003 — Collateral-Constrained Treasury Forecast

## Numerical summary (USD)

| Week (close) | S eligible | T | H recognized | BB | Limit L | Interest | Cure U | Draw X | Vol. repay A | Close cash | Close debt | Unused | Buffer shortfall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 (2027-01-10) | 240,000.06 | 60,000.01 | 180,000.03 | 144,000.02 | 144,000.02 | 300.01 | 6,002.48 | 0.00 | 0.00 | 43,697.51 | 144,000.02 | 0.00 | 6,302.49 |
| 2 (2027-01-17) | 240,000.12 | 60,000.03 | 180,000.08 | 144,000.06 | 144,000.06 | 288.00 | 0.00 | 0.04 | 0.00 | 33,409.55 | 144,000.06 | 0.00 | 16,590.45 |
| 3 (2027-01-24) | 400,000.10 | 100,000.02 | 400,000.07 | 320,000.05 | 200,000.00 | 288.00 | 0.00 | 0.00 | 33,121.55 | 50,000.00 | 110,878.51 | 89,121.49 | 0.00 |
| 4 (2027-01-31) | 210,000.06 | 52,500.01 | 155,000.05 | 124,000.04 | 124,000.04 | 221.76 | 0.00 | 13,121.53 | 0.00 | 22,899.77 | 124,000.04 | 0.00 | 27,100.23 |

Violations, kept separate:

- **Minimum-cash buffer breaches** (closing cash < 50,000.00): weeks 1, 2 and 4.
- **Unfunded cash deficits** (closing cash < 0): none.
- **Debt above the permitted limit**: a USD 6,002.48 overadvance existed at the week-1 test (opening debt 150,002.50 vs L 144,000.02); it was fully cured from available cash, so unpaid cure and closing overadvance are zero in every week.

## Material drivers

1. **Week 1 limit cut forces a cure (snapshot 2027-01-10, invoices A-1, B-1, C-1).** All three invoices are eligible (due 2027-02-28, 0 days past due, no flags); S = 240,000.06. T = floor(0.25 × S) = 60,000.01, so customer A (A-1, 100,000.03) is capped with a 40,000.02 deduction and B (B-1, 80,000.02) with 20,000.01; C (60,000.01) is fully recognized. BB = floor(0.80 × 180,000.03) = 144,000.02, below opening debt. Cure priority over the buffer meant the 6,002.48 repayment came from cash of 49,699.99, pushing cash to 43,697.51 and opening a 6,302.49 buffer shortfall. After the cure debt equals L, so no draw was possible.
2. **Week 2 rounding-level headroom (2027-01-17).** Balances of the same three invoices tick up by cents (A-1 100,000.07, B-1 80,000.03, C-1 60,000.02). T becomes 60,000.03 and L rises by 0.04 to 144,000.06. The draw is limited to that 0.04 headroom, so the buffer gap widens to 16,590.45 after the net operating outflow (receipt bb_rounding_003-W2-receipt 10,000.00 vs payment bb_rounding_003-W2-payment 20,000.00).
3. **Week 3 collateral expansion and ceiling (2027-01-24).** A new customer D (D-1, 100,000.04) appears and B-1/C-1 rise to about 100,000. With four near-equal customers, T = 100,000.02 trims only cents (B 0.00, C 0.01, D 0.02 deducted; A at 100,000.01 is under T). BB = 320,000.05, but L is capped at the 200,000.00 contractual ceiling. The large receipt bb_rounding_003-W3-receipt (60,000.00) lifts cash before financing to 83,121.55; the 33,121.55 above minimum is applied as a voluntary repayment, restoring cash to exactly 50,000.00.
4. **Week 4 contraction (2027-01-31).** D-1 is absent from the snapshot and contributes zero; its absence is not treated as a receipt. A-1 (90,000.01), B-1 (70,000.02) and C-1 (50,000.03) give S = 210,000.06 and T = 52,500.01, deducting 37,500.00 from A and 17,500.01 from B. L falls to 124,000.04. Debt (110,878.51) is below L, so no cure; the payment bb_rounding_003-W4-payment (50,000.00) drops cash before financing to 9,778.24 and the draw is capped by headroom at 13,121.53, leaving a 27,100.23 buffer shortfall with zero unused credit.

## Eligibility and concentration exceptions

No invoice in any snapshot is disputed, related-party, over 60 days past due or zero balance; all 13 observations are `eligible` with 0 days past due. Every collateral reduction therefore comes from the shared concentration threshold (applied once with the original S) and the 80% advance rate, both floored to the cent, plus the 200,000.00 ceiling in week 3. Deductions are not write-offs.

## Collateral versus receipts

Receipts and payments come only from `cash_events.csv` (eight records, one receipt and one payment per week). Receivables snapshots are independent closing states used solely to size the borrowing base; changes between snapshots (e.g., D-1 disappearing, A-1 falling 10,000.00 in week 4) were not converted into cash, and no snapshot was carried forward.

## Funding priorities applied

Interest (0.002 × opening debt, half-up) → mandatory cure from available non-negative cash (ahead of the buffer) → draw to restore the buffer only within headroom and only if no unpaid cure → voluntary repayment of cash above minimum.

## Assumptions and limitations

- Interest paid in cash at week end; no fees.
- Each week's waterfall uses that week's closing snapshot limit.
- All cash events fall on Sundays within the horizon; inputs passed validation (no duplicate keys, invalid flags, negative amounts or dates).
- Repeated buffer breaches signal a liquidity need the facility cannot fund at current collateral; the model does not resolve it.
