# bb_release_006 reference explanation



Synthetic four-week contractual forecast. Snapshots size collateral; only cash_events.csv supplies receipts and payments.



On 2027-01-10, eligible receivables total 400000.00, the customer cap is 100000.00, recognized collateral is 400000.00 and the effective limit is 200000.00. Events bb_release_006-W1-receipt and bb_release_006-W1-payment supply 0.00 and 9700.00. Interest is 300.00. Required/paid cure: 0.00/0.00; draw 0.00; voluntary repayment 0.00. Closing cash/debt: 50000.00/150000.00; buffer gap 0.00; overadvance 0.00; unfunded deficit 0.00.

On 2027-01-17, eligible receivables total 400000.00, the customer cap is 100000.00, recognized collateral is 400000.00 and the effective limit is 200000.00. Events bb_release_006-W2-receipt and bb_release_006-W2-payment supply 300.00 and 0.00. Interest is 300.00. Required/paid cure: 0.00/0.00; draw 0.00; voluntary repayment 0.00. Closing cash/debt: 50000.00/150000.00; buffer gap 0.00; overadvance 0.00; unfunded deficit 0.00.

On 2027-01-24, eligible receivables total 400000.00, the customer cap is 100000.00, recognized collateral is 400000.00 and the effective limit is 200000.00. Events bb_release_006-W3-receipt and bb_release_006-W3-payment supply 300.00 and 0.00. Interest is 300.00. Required/paid cure: 0.00/0.00; draw 0.00; voluntary repayment 0.00. Closing cash/debt: 50000.00/150000.00; buffer gap 0.00; overadvance 0.00; unfunded deficit 0.00.

On 2027-01-31, eligible receivables total 0.00, the customer cap is 0.00, recognized collateral is 0.00 and the effective limit is 0.00. Events bb_release_006-W4-receipt and bb_release_006-W4-payment supply 210000.00 and 40000.00. Interest is 300.00. Required/paid cure: 150000.00/150000.00; draw 0.00; voluntary repayment 0.00. Closing cash/debt: 69700.00/0.00; buffer gap 0.00; overadvance 0.00; unfunded deficit 0.00.



A-1 through D-1 support the facility in weeks 1–3. The explicit final snapshot has no invoices; do not reuse prior collateral. The week-4 receipt event is 210000 and payment is 40000. After 300 interest, cash before financing is 219700: the 150000 mandatory cure fully repays debt and leaves 69700 cash. Zero collateral need not imply a deficit.



All nonzero invoices are future-due and neither disputed nor related-party. Concentration deductions are not write-offs or cash movements. No refinancing, waiver or discretionary deferral is assumed. Weekly closing balances do not establish intraday liquidity; negative cash, if present, is diagnostic rather than an authorized overdraft.
