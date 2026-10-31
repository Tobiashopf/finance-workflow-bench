# Meridian Distribution: thirteen-week cash forecast

All amounts are USD. Opening available cash is $80,000.00 across the two supplied accounts; opening debt of $60,000.00 is separate.

The lowest closing cash is **-$39,945.80 in week 6 (February 8–14, 2027)**, with no ties. Only weeks 5 and 6 breach the $50,000.00 minimum:

| Week | Closing cash | Minimum-cash shortfall | Unfunded deficit |
|---|---:|---:|---:|
| 5: February 1–7 | $48,454.20 | $1,545.80 | $0.00 |
| 6: February 8–14 | -$39,945.80 | $89,945.80 | $39,945.80 |

Week 5 has a buffer breach but no unfunded closing deficit. Week 6 is the only week with an unfunded deficit. Negative cash carries forward solely under the specified diagnostic convention; it does not represent authorized overdraft funding.

Peak closing debt is **$200,000.00**, first reached in week 5 and also present in week 6. Total draws are **$175,797.64**, repayments **$235,797.64**, and interest **$1,862.89**. Debt is fully repaid in week 11; week 13 ends with $126,137.11 cash and $200,000.00 available credit.

Material cash-flow drivers:

- Week 4: `payables.csv` AP-04 requires $80,000.00 on January 29 ($95,000.00 gross less $15,000.00 already paid); FREIGHT-04 adds $5,000.00 on January 25. `recurring_expenses.csv` PAYROLL-04 adds $24,000.00 on January 29. With $40,000.00 receipts and other recurring costs, the required draw is $71,070.53.
- Week 5: `payables.csv` AP-05 requires $120,000.00 on February 5. `recurring_expenses.csv` RENT-05 and OTHER_RECURRING-05 add $8,000.00 and $2,000.00 that day. `receivables.csv` AR-05-A and AR-05-B supply only $17,500.00 each on February 3. The remaining $93,666.87 facility capacity cannot fully restore the buffer.
- Week 6: `payables.csv` AP-06, TAX-06 and FREIGHT-06 require $75,000.00, $12,000.00 and $5,000.00 on February 12, 11 and 8 respectively. `recurring_expenses.csv` PAYROLL-06 and OTHER_RECURRING-06 add $24,000.00 and $2,000.00 on February 12. Receipts of $30,000.00 and $400.00 interest produce an $88,400.00 cash decline with no credit remaining.
- Recovery: `receivables.csv` AR-07-A/B provide $90,000.00 each on February 17, and AR-08-A/B provide $80,000.00 each on February 24. These receipts restore the buffer and support repayments of $52,654.20 and $93,705.31 in weeks 7 and 8.

Exact duplicates were removed before exclusions: two copies of receivables AR-03-A, one of receivables AR-FUTURE, one of payables TAX-03, and one of recurring OTHER_RECURRING-01. Distinct records with equal amounts and dates were retained. AR-03-A contributes only $32,500.00 on January 20 after its $10,000.00 prior payment; AP-04 is likewise net of prior payment. Previously paid amounts were not counted again.

Payables TRANSFER-01 ($25,000.00) and TRANSFER-FUTURE ($15,000.00) were excluded as internal transfers. AR-PAID and AP-PAID were excluded as zero outstanding. AR-FUTURE ($42,000.00), AP-FUTURE ($30,000.00), and RENT-FUTURE ($8,000.00) fall on April 5, beyond the horizon. Internal-transfer and zero-outstanding reasons take precedence over horizon exclusions. No invalid input records were identified.

Dates, collection in full, the minimum buffer, credit limit, and weekly rate are supplied assumptions, not verified predictions. This deterministic forecast measures weekly closing liquidity only. Interest uses opening principal, rounded half up to cents; draws and automatic repayments follow the prescribed policy. No additional recurring payments, date shifts, discretionary funding, or deferred obligations were introduced.
