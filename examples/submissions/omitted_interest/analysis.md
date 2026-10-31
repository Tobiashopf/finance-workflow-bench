# Reference financial analysis

Status: the project owner confirmed financial review; computed values also passed a second computational check. This is a reference artifact, not an evaluated model submission. A new submission requires its own explanation review.

The lowest weekly closing cash is **USD -39,945.80 in week 6** (February 8–14). Only weeks 5 and 6 breach the USD 50,000 minimum buffer. Week 5 closes at USD 48,454.20, a buffer shortfall of USD 1,545.80 without an unfunded cash deficit. Week 6 has both an unfunded deficit of USD 39,945.80 and a minimum-buffer shortfall of USD 89,945.80. These are different funding objectives.

Peak closing debt is USD 200,000.00, first reached in week 5 and maintained in week 6. Across the horizon, draws total USD 175,797.64, repayments USD 235,797.64, and interest USD 1,862.89. Repayments exceed draws by the USD 60,000.00 opening principal. Debt is extinguished in week 11; week 13 closes with USD 126,137.11 in cash.

## Material drivers

- `payables.csv / AP-04` requires an USD 80,000 payment on January 29, after subtracting USD 15,000 already paid from the USD 95,000 obligation. Together with payroll, freight and recurring expenses, week 4 operating payments total USD 111,000 against USD 40,000 in receipts.
- `payables.csv / AP-05` requires USD 120,000 on February 5. With `recurring_expenses.csv / RENT-05` (USD 8,000) and `OTHER_RECURRING-05` (USD 2,000), week 5 payments total USD 130,000. Receipts from `receivables.csv / AR-05-A` and `AR-05-B` total only USD 35,000. Available credit is exhausted.
- Week 6 includes `payables.csv / AP-06` (USD 75,000), `TAX-06` (USD 12,000), `FREIGHT-06` (USD 5,000), and `recurring_expenses.csv / PAYROLL-06` (USD 24,000) and `OTHER_RECURRING-06` (USD 2,000). With USD 30,000 receipts and USD 400 interest, the exhausted facility cannot prevent a projected deficit.
- `receivables.csv / AR-07-A` and `AR-07-B` deliver a combined USD 180,000 on February 17. Week 7 returns to the minimum cash buffer and repays USD 52,654.20. Week 8 receipts of USD 160,000 from `AR-08-A` and `AR-08-B` enable a further USD 93,705.31 repayment.

## Data treatment and assumptions

Five excess duplicate rows were removed: two copies of `AR-03-A` and one each of `AR-FUTURE`, `TAX-03`, and `OTHER_RECURRING-01`. Equal-value invoices with distinct identities were retained. `AR-03-A` contributes USD 32,500 after deducting USD 10,000 previously received. Previous settlements are already reflected in opening balances.

`payables.csv / TRANSFER-01` and `TRANSFER-FUTURE` have no consolidated cash effect. Fully settled `receivables.csv / AR-PAID` and `payables.csv / AP-PAID` are excluded. `AR-FUTURE`, `AP-FUTURE`, and `recurring_expenses.csv / RENT-FUTURE` occur after April 4 and are excluded. Exclusion-reason precedence follows the task contract.

Receipt dates, the 0.2% weekly interest rate, cash minimum and automatic financing policy are supplied synthetic assumptions, not empirical forecasts. The negative week 6 cash is carried forward for diagnostic projection only; subsequent recovery does not establish real-world operational feasibility without funding or renegotiation. The analysis assesses weekly closing liquidity, not daily solvency, default risk, or optimal financing.
