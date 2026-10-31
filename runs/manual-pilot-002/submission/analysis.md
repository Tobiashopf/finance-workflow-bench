# Borrowing Base 002 analysis

All amounts are USD. Calculations use only the five supplied inputs and the task's contractual waterfall. Forecast JSON conforms to the supplied schema.

| Closing date | Eligible | Recognized | Borrowing base | Effective limit | Closing cash | Closing debt |
|---|---:|---:|---:|---:|---:|---:|
| 2027-01-10 | 300,000.00 | 210,000.00 | 168,000.00 | 168,000.00 | 50,000.00 | 150,300.00 |
| 2027-01-17 | 200,000.00 | 130,000.00 | 104,000.00 | 104,000.00 | 0.00 | 110,600.60 |
| 2027-01-24 | 400,000.00 | 380,000.00 | 304,000.00 | 200,000.00 | 50,000.00 | 100,821.80 |
| 2027-01-31 | 0.00 | 0.00 | 0.00 | 0.00 | -20,201.64 | 100,821.80 |

On January 10, A-EDGE is exactly 60 days past due and remains eligible; Z-OLD is 61 days past due and excluded. Customer A has 150,000.00 eligible and B 90,000.00; the shared 75,000.00 threshold deducts 75,000.00 and 15,000.00 respectively. C's 60,000.00 is fully recognized. The simultaneous cap applies even with only three eligible customers.

On January 17, A-EDGE reaches 67 days and loses 50,000.00 of eligibility. A-NEW adds 20,000.00, while B-CORE falls from 90,000.00 to 40,000.00 and C-CORE from 60,000.00 to 40,000.00. Eligible collateral falls to 200,000.00. The 50,000.00 threshold deducts 70,000.00 from A, lowering the effective limit to 104,000.00.

On January 24, B-CORE and C-CORE each rise to 100,000.00; D-NEW adds 80,000.00. A-EDGE remains excluded at 74 days. The threshold rises to 100,000.00, with only A suffering a 20,000.00 deduction. The 304,000.00 borrowing base is constrained by the 200,000.00 contractual ceiling.

Across these three snapshots, X-DISPUTE and X-MULTI are excluded as disputed; X-MULTI's related-party and aging flags do not override that reason. Y-RELATED and Y-MULTI are excluded as related party, including Y-MULTI's zero balance and aging. Z-OLD is over-age and Z-ZERO is zero balance. Customers X, Y and Z retain zero-valued customer checks. January 31 is an explicitly declared empty snapshot: no prior collateral or invented customer rows carry forward.

Interest is 300.00, 300.60, 221.20 and 201.64. Week 1 draws 300.00 to restore the buffer, leaving 17,700.00 unused credit. Week 2 requires a 46,300.00 cure; all 39,699.40 available cash repays debt before protecting the buffer. The unpaid cure and overadvance are 6,600.60, the buffer shortfall is 50,000.00, and the cash deficit is zero. Further drawing is prohibited.

Week 3 voluntarily repays 9,778.80 and leaves 99,178.20 unused credit, with no closing violations. Week 4's negative pre-financing cash cannot fund a cure: debt and unpaid cure remain 100,821.80. The cash deficit is 20,201.64 and buffer shortfall 70,201.64; no new draw is allowed. Weeks 2 and 4 have zero unused credit.

CASH-R-1 through CASH-R-4 supply receipts of 20,000.00, 30,000.00, 80,000.00 and 20,000.00; CASH-P-1 through CASH-P-4 supply payments of 30,000.00, 40,000.00, 20,000.00 and 90,000.00. Snapshot changes are independent remaining balances, not receipts, write-offs or payments. Negative cash is a projected funding failure, not an authorized overdraft. No waiver, refinancing, payment deferral or additional penalty is assumed; later recovery does not resolve the earlier operational funding problem.
