# bb_customer_004 — Collateral-Constrained Treasury Forecast

## Numerical summary (USD)

| Week (close) | S eligible | T | H recognized | BB | Limit L | Interest | Cure U | Draw X | Vol. repay A | Closing cash | Closing debt | Unused | Buffer shortfall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 (2027-01-10) | 240,000.00 | 60,000.00 | 180,000.00 | 144,000.00 | 144,000.00 | 300.00 | 6,000.00 | 0.00 | 0.00 | 43,700.00 | 144,000.00 | 0.00 | 6,300.00 |
| 2 (2027-01-17) | 240,000.00 | 60,000.00 | 160,000.00 | 128,000.00 | 128,000.00 | 288.00 | 16,000.00 | 0.00 | 0.00 | 17,412.00 | 128,000.00 | 0.00 | 32,588.00 |
| 3 (2027-01-24) | 360,000.00 | 90,000.00 | 330,000.00 | 264,000.00 | 200,000.00 | 256.00 | 0.00 | 0.00 | 17,156.00 | 50,000.00 | 110,844.00 | 89,156.00 | 0.00 |
| 4 (2027-01-31) | 240,000.00 | 60,000.00 | 240,000.00 | 192,000.00 | 192,000.00 | 221.69 | 0.00 | 40,221.69 | 0.00 | 50,000.00 | 151,065.69 | 40,934.31 | 0.00 |

Violations, reported separately:

- **Minimum-cash buffer breach:** weeks 1 and 2 only (shortfalls 6,300.00 and 32,588.00).
- **Unfunded cash deficit:** none; closing cash never goes negative.
- **Debt above permitted limit (overadvance / unpaid cure):** none at any close. Required cures in weeks 1 and 2 were fully paid from available cash.

## Material collateral drivers

1. **Customer A concentration (2027-01-10, 2027-01-17, 2027-01-24).** Invoices A-1, A-2 and A-3 (40,000.00 each) give A 120,000.00 of eligible collateral. T is 25% of S: 60,000.00 in weeks 1–2, so A is cut by 60,000.00; 90,000.00 in week 3, cutting A by 30,000.00. In week 1 this is the only deduction: H = 180,000.00, BB = 144,000.00, below opening debt of 150,000.00, so a 6,000.00 cure is required.
2. **D-1 zero balance and B-1 increase (2027-01-17).** D-1 is reported at 0.00 and is excluded with reason `zero_balance`; customer D still appears with zero eligible/recognized amounts and the shared T. B-1 rises to 80,000.00, but B is capped at 60,000.00 (deduction 20,000.00). S stays at 240,000.00, yet H falls to 160,000.00 because more of the pool sits in capped customers. L falls to 128,000.00 and forces a 16,000.00 cure.
3. **Collateral expansion (2027-01-24).** C-1 and D-1 each show 80,000.00. S = 360,000.00, T = 90,000.00, and only A is capped. BB = 264,000.00 exceeds the contractual ceiling, so L = 200,000.00.
4. **Diversified, uncapped pool (2027-01-31).** All balances fall (A invoices 20,000.00 each; B-1, C-1, D-1 60,000.00 each). Every customer equals T = 60,000.00 exactly, so there are no concentration deductions; H = S = 240,000.00 and L = 192,000.00.

No invoice is disputed, related-party or past due (all due 2027-02-28, so days past due are 0). The only exclusion of the 24 invoice observations is D-1 on 2027-01-17.

## Funding priorities

- **Week 1:** B = 60,000 + 20,000 (bb_customer_004-W1-receipt) − 30,000 (W1-payment) − 300 interest = 49,700.00. The mandatory cure (6,000.00) is paid before the buffer, leaving 43,700.00. Debt equals L, so no draw is possible; the buffer is breached by 6,300.00.
- **Week 2:** B = 33,412.00 after W2 receipt/payment and 288.00 interest. The 16,000.00 cure again has priority, leaving 17,412.00; no headroom to draw, so a 32,588.00 shortfall.
- **Week 3:** The 60,000.00 W3 receipt lifts B to 67,156.00. No cure is required; cash above 50,000.00 (17,156.00) is applied as voluntary repayment.
- **Week 4:** The 50,000.00 W4 payment drops B to 9,778.31. A draw of 40,221.69 restores the minimum, within 81,156.00 of headroom.

## Collateral versus receipts

Receivables snapshots are independent closing balances used only to size the borrowing base. Cash moves only through `cash_events.csv`. D-1 dropping to 0.00 on 2027-01-17 was not treated as a receipt, and the lower 2027-01-31 balances do not create cash; week-4 receipts are only the 10,000.00 in bb_customer_004-W4-receipt. Snapshots were not carried forward or summed into cash.

## Assumptions and limitations

- I applied the contractual rules in `task.md` exactly. Collateral amounts are floored to the cent, and interest uses round-half-up on opening debt.
- Inputs were validated: there are no duplicate keys or invalid flags, all four snapshot dates are present, and all cash dates fall within the horizon.
- Concentration deductions are not write-offs. Eligibility does not imply collectability.
- The week-1 and week-2 buffer breaches are real liquidity covenant gaps, even though the facility stayed within its limit and cash later recovered. The forecast does not model waivers, refinancing, payment deferral or penalties.
- Synthetic data; not lending or legal advice.
