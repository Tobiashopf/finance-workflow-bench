# Meridian Distribution — 13-Week Cash Forecast (Jan 4 – Apr 4, 2027)

## Summary

- Opening consolidated cash: USD 80,000.00 (BANK-OPERATING 65,000.00 + BANK-COLLECTIONS 15,000.00). Opening revolver principal: 60,000.00.
- **Lowest closing cash: −39,945.80 in week 6 (Feb 8–14).** No ties.
- **Weeks below the 50,000.00 minimum buffer:** week 5 (closing 48,454.20; shortfall 1,545.80) and week 6 (closing −39,945.80; shortfall 89,945.80).
- **Weeks with an unfunded deficit:** week 6 only (39,945.80). Week 5 is a buffer breach only: payments are funded, but cash ends below the minimum because the facility is fully drawn.
- **Peak closing debt: 200,000.00 (the full limit), first reached in week 5** and held through week 6.
- Totals over 13 weeks: draws 175,797.64 (weeks 2, 4, 5); repayments 235,797.64 (weeks 1, 3, 7–11); interest 1,862.89. The revolver is fully repaid in week 11, and closing cash rises to 126,137.11 by week 13.

## Material drivers

1. **Late-January supplier and payroll cluster (week 4, Jan 25–31).** `payables.csv` AP-04 pays 80,000.00 on Jan 29 (gross 95,000.00 less 15,000.00 already paid), plus FREIGHT-04 5,000.00 (Jan 25); `recurring_expenses.csv` PAYROLL-04 24,000.00 and OTHER_RECURRING-04 2,000.00 (Jan 29). Against receipts of only 40,000.00 (`receivables.csv` AR-04-A and AR-04-B, Jan 27), cash before financing falls to −21,070.53, requiring a 71,070.53 draw and lifting principal to 106,333.13.
2. **Large supplier payment exhausts the facility (week 5, Feb 1–7).** `payables.csv` AP-05 pays 120,000.00 on Feb 5, with RENT-05 8,000.00 and OTHER_RECURRING-05 2,000.00. Receipts are 35,000.00 (AR-05-A/B, Feb 3). The required draw of 95,212.67 exceeds remaining availability of 93,666.87, so the facility hits its 200,000.00 limit and closing cash is 48,454.20.
3. **Funding gap with no remaining credit (week 6, Feb 8–14).** `payables.csv` AP-06 75,000.00 (Feb 12), TAX-06 12,000.00 (Feb 11) and FREIGHT-06 5,000.00 (Feb 8), plus PAYROLL-06 24,000.00 and OTHER_RECURRING-06 2,000.00 (Feb 12), total 118,000.00 against receipts of 30,000.00 (AR-06-A/B, Feb 10) and 400.00 interest. With no credit available, closing cash is −39,945.80.
4. **Recovery from concentrated collections (weeks 7–8).** `receivables.csv` AR-07-A and AR-07-B (90,000.00 each, Feb 17) and AR-08-A and AR-08-B (80,000.00 each, Feb 24) bring 340,000.00 in two weeks. The sweep repays 52,654.20 and 93,705.31, and the liquidity position never breaches again.
5. **Early drawdown (week 2, Jan 11–17).** AP-02 40,000.00 and PAYROLL-02 24,000.00 (Jan 15) exceed AR-02-A/B receipts of 55,000.00 (Jan 13), triggering an 11,060.24 draw after a 29,880.00 repayment in week 1.

## Exceptions handling

- **Exact duplicates** (identical rows, same `record_id`) were removed before exclusions: `receivables.csv` AR-03-A (2 discarded) and AR-FUTURE (1); `payables.csv` TAX-03 (1); `recurring_expenses.csv` OTHER_RECURRING-01 (1). Records with matching amounts or dates but different IDs, such as the paired customer A/B invoices, were kept.
- **Partial payments:** only outstanding amounts were forecast. AR-03-A collects 32,500.00 (42,500.00 less 10,000.00) on Jan 20, and AP-04 pays 80,000.00. Prior payments are treated as already reflected in opening cash.
- **Internal transfers:** TRANSFER-01 (25,000.00, Feb 5) and TRANSFER-FUTURE (15,000.00, Apr 5) were excluded as `internal_transfer`. They do not change consolidated cash.
- **Zero outstanding:** AR-PAID and AP-PAID are fully paid and were excluded as `zero_outstanding`. Under the precedence rule, this applies to AR-PAID even though its date (Apr 5) is also outside the horizon.
- **Outside horizon:** AR-FUTURE (42,000.00), AP-FUTURE (30,000.00) and RENT-FUTURE (8,000.00) all fall on Apr 5, 2027, one day after week 13. They were excluded and would affect the week after the forecast.
- All inputs passed validation. There were no conflicting IDs, duplicate business identifiers, negative amounts, overpayments or dates on or before the as-of date.

## Assumptions versus conclusions

**Supplied assumptions (not verified):** opening balances; the expected receipt dates and amounts, which are scenario inputs, not predictions of customer behavior; payment dates with no weekend or holiday adjustment; the facility terms (200,000.00 limit, 0.2% simple weekly interest on opening principal, paid weekly, no fees); the 50,000.00 minimum; and the mandatory automatic draw and repayment sweep.

**Conclusions (derived by calculation):** the week 5 buffer breach, the week 6 unfunded deficit of 39,945.80, full use of the facility in weeks 5–6, and full repayment by week 11. The negative week 6 balance is a diagnostic convention carried into week 7. It does not mean an account can actually be overdrawn, and it shows that funding beyond the facility, or rescheduled payments, would be needed. This forecast does not propose either.

**Scope:** the forecast is deterministic and weekly. It measures liquidity at each week's close, not intraday. Exposure within a week may differ from the weekly close. Interest is rounded half-up to cents each week; all other arithmetic is exact decimal. The forecast does not test optimal borrowing, model stochastic risk, or give financial advice.
