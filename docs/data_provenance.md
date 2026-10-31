# Data provenance

All company names, account identifiers, customer identifiers, invoices, obligations, amounts and dates in this case were constructed synthetically for this project. No employer records, customer data, personal data, external datasets or paid market data were used.

The deterministic generator is `scripts/build_case.py`. It uses no random seed because it contains a fixed scenario schedule. Re-running it reproduces the five input files. Currency and interest parameters are exercise assumptions, not market observations.

The source files contain two opening account balances; 31 receivable rows (28 distinct); 24 payable rows (23 distinct); and 24 recurring-expense rows (23 distinct). The final count is checked against the generated files during milestone review. Five excess duplicate rows are intentionally present. Seven distinct event records are excluded according to the task rules.

Weekly receipts and supplier payments were selected to create a temporary concentration of liquidity pressure. They are scenario design choices, not samples from a real distribution. Results cannot be generalized to real business performance or model capability from this one case.

`reference/cash_forecast_001/source_ledger.json` maps each included unique event to a weekly category. It is not an agent input. `reports/reference-verification.json` records SHA-256 fingerprints of the five inputs and the numeric reference used in verification.

This milestone does not assert a third-party data license or a completed software licensing decision. Choose the project's code/data licensing before public release.

## Case 002

`scripts/build_borrowing_base_case.py` generates an original fixed synthetic fixture with five input files, 33 invoice observations over three populated snapshots, one explicitly empty fourth snapshot, and eight cash events. Repeated invoice IDs on different dates are intentional longitudinal observations, not duplicate rows. No external financial data is used. The rates, exclusion rules and concentration formula are fictional contract assumptions reviewed by the project owner. The inputs and computed reference are fingerprinted in `reports/borrowing-base-verification.json`. Detailed reference review remains separate from acceptance of those rules.
