# bb_rounding_003 reference explanation



Synthetic four-week contractual forecast. Snapshots size collateral; only cash_events.csv supplies receipts and payments.



On 2027-01-10, eligible receivables total 240000.06, the customer cap is 60000.01, recognized collateral is 180000.03 and the effective limit is 144000.02. Events bb_rounding_003-W1-receipt and bb_rounding_003-W1-payment supply 20000.00 and 30000.00. Interest is 300.01. Required/paid cure: 6002.48/6002.48; draw 0.00; voluntary repayment 0.00. Closing cash/debt: 43697.51/144000.02; buffer gap 6302.49; overadvance 0.00; unfunded deficit 0.00.

On 2027-01-17, eligible receivables total 240000.12, the customer cap is 60000.03, recognized collateral is 180000.08 and the effective limit is 144000.06. Events bb_rounding_003-W2-receipt and bb_rounding_003-W2-payment supply 10000.00 and 20000.00. Interest is 288.00. Required/paid cure: 0.00/0.00; draw 0.04; voluntary repayment 0.00. Closing cash/debt: 33409.55/144000.06; buffer gap 16590.45; overadvance 0.00; unfunded deficit 0.00.

On 2027-01-24, eligible receivables total 400000.10, the customer cap is 100000.02, recognized collateral is 400000.07 and the effective limit is 200000.00. Events bb_rounding_003-W3-receipt and bb_rounding_003-W3-payment supply 60000.00 and 10000.00. Interest is 288.00. Required/paid cure: 0.00/0.00; draw 0.00; voluntary repayment 33121.55. Closing cash/debt: 50000.00/110878.51; buffer gap 0.00; overadvance 0.00; unfunded deficit 0.00.

On 2027-01-31, eligible receivables total 210000.06, the customer cap is 52500.01, recognized collateral is 155000.05 and the effective limit is 124000.04. Events bb_rounding_003-W4-receipt and bb_rounding_003-W4-payment supply 10000.00 and 50000.00. Interest is 221.76. Required/paid cure: 0.00/0.00; draw 13121.53; voluntary repayment 0.00. Closing cash/debt: 22899.77/124000.04; buffer gap 27100.23; overadvance 0.00; unfunded deficit 0.00.



A-1, B-1 and C-1 carry cents. Floor the shared cap before applying it, and floor the advance separately. Opening debt 150002.50 produces 300.005 interest, rounded half up to 300.01. D-1 enters in week 3, increasing collateral capacity; its absence in week 4 is not a cash receipt.



All nonzero invoices are future-due and neither disputed nor related-party. Concentration deductions are not write-offs or cash movements. No refinancing, waiver or discretionary deferral is assumed. Weekly closing balances do not establish intraday liquidity; negative cash, if present, is diagnostic rather than an authorized overdraft.
