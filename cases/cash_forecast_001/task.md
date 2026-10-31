# Cash Forecast 001: Thirteen-Week Liquidity Forecast

Status: output contract v0.2. The project owner reviewed the financial specification and reference solution. The artifact grader is implemented; model execution and process isolation are not yet implemented. Version 0.2 adds explicit artifact limits and scoring details without changing financial rules.

## Business assignment

You are the treasury analyst for a fictional distributor, Meridian Distribution. Prepare a consolidated thirteen-week cash forecast using only the supplied inputs and the rules below. Identify liquidity shortfalls, apply the specified revolving-credit policy, and explain the main cash-flow drivers using source records.

This is a synthetic, deterministic treasury exercise. It does not require external research, accounting-standard interpretation, or predictions about customer behavior. All dates and contractual conventions below are benchmark assumptions.

## Forecast scope

- Currency: USD. All input monetary amounts have two decimal places.
- Forecast as-of date: Sunday, January 3, 2027, after all activity for that day.
- Week 1: January 4–10, 2027. Week 13: March 29–April 4, 2027.
- Weeks run Monday through Sunday, with both boundary dates included.
- Opening balances are available cash, excluding restricted cash and credit availability.
- Consolidate all supplied bank accounts. Internal transfers do not create consolidated receipts or payments.
- Include events on their supplied cash dates. Do not move dates for weekends or holidays.
- Exclude cash events outside the forecast horizon and report their record IDs and reasons.
- Minimum required closing cash: USD 50,000.00 each week.
- This exercise evaluates weekly closing liquidity, not intraday liquidity or optimal borrowing decisions.

## Input contract

The input bundle will contain these five files. CSVs use UTF-8, a header row, ISO dates (`YYYY-MM-DD`), and unformatted decimal amounts. Amounts must be nonnegative; direction is represented by the record type.

### opening_balances.csv

Columns: `account_id`, `as_of_date`, `available_balance`.

Each account appears exactly once. All dates equal the forecast as-of date. Sum `available_balance` to determine week 1 opening cash. Opening debt is supplied separately and must not be subtracted from bank cash.

### receivables.csv

Columns: `record_id`, `invoice_id`, `customer_id`, `invoice_amount`, `paid_before_as_of`, `expected_receipt_date`.

One canonical row per invoice. Collect `invoice_amount - paid_before_as_of` in full on `expected_receipt_date`; this date is an explicit scenario assumption, not a date the agent must infer. Previously paid amounts are already reflected in opening cash. Zero outstanding amounts contribute no receipt. No discounts, taxes, currency conversion, or additional defaults apply.

### payables.csv

Columns: `record_id`, `obligation_id`, `category`, `gross_amount`, `paid_before_as_of`, `payment_date`.

Allowed categories: `supplier`, `tax`, `other_external`, `internal_transfer`. Pay the outstanding amount on `payment_date`. Previously paid amounts are already reflected in opening cash. Exclude internal transfers from consolidated receipts and payments regardless of their amount; report them as exclusions. No payable overlaps a recurring expense.

### recurring_expenses.csv

Columns: `record_id`, `expense_id`, `category`, `cash_date`, `amount`.

Each row is one dated payment occurrence, not a recurrence instruction. Allowed categories: `payroll`, `rent`, `other_recurring`. Include each unique occurrence once. Do not generate additional payments. No row overlaps a payable.

### credit_facility.json

Required fields and fixed values for this case:

```json
{
  "currency": "USD",
  "credit_limit": "200000.00",
  "opening_principal": "60000.00",
  "weekly_interest_rate": "0.002000",
  "minimum_cash": "50000.00",
  "interest_basis": "opening_week_principal",
  "interest_payment": "end_of_each_week",
  "fees": "0.00"
}
```

Interest is a simple contractual weekly rate, not an annual rate requiring conversion. Opening principal is outstanding debt, not additional cash. There are no fees, minimum draw sizes, or repayment penalties. Repaid principal restores availability for later weeks. No intraweek redraw or repayment is modeled.

## Duplicate and invalid-record handling

- `record_id` is unique within each event file except for intentional exact duplicate rows.
- For exact duplicates with the same `record_id` and identical fields, retain one occurrence and report the number discarded.
- Matching amounts or dates alone are not sufficient grounds to remove a record.
- Different `record_id` values with the same business identifier are invalid within that file: `invoice_id`, `obligation_id`, or `expense_id`, respectively.
- Conflicting rows with the same `record_id`, missing required fields, invalid dates, negative amounts, overpaid invoices/obligations, or invalid opening balances are input errors. Do not silently repair them.
- A positive outstanding receivable/payable with a cash date on or before January 3, 2027 is invalid, because the stated opening balances and payment assumptions would be ambiguous.
- The scored v0.1 case will contain valid inputs and exact duplicates only. Invalid-input detection will be tested separately; those tests are not forecasts with invented repairs.

## Mandatory weekly financing policy

Use decimal arithmetic. Round weekly interest to cents using ROUND_HALF_UP. Do not round intermediate arithmetic other than interest.

For each week, define:

- `C`: opening consolidated cash.
- `D`: opening principal.
- `R`: eligible receipts.
- `P`: eligible supplier, tax, other external, and recurring payments, excluding interest and principal.
- `M`: minimum cash (50,000.00).
- `L`: credit limit (200,000.00).

Apply these operations in order:

1. Interest: `I = round_half_up(D * 0.002000, 2)`.
2. Cash before financing: `B = C + R - P - I`.
3. Credit draw: `X = min(max(M - B, 0), L - D)`.
4. Repayment: `A = min(max(B - M, 0), D)`. Never draw and repay in the same week.
5. Closing cash: `E = B + X - A`.
6. Closing principal: `F = D + X - A`.
7. Remaining credit: `L - F`.
8. Minimum-cash shortfall: `max(M - E, 0)`.
9. Unfunded cash deficit: `max(-E, 0)`.

Next week's opening cash and principal equal this week's closing amounts. New draws accrue interest beginning the next week; principal repaid at week end still incurs that week's interest.

If the credit limit is insufficient, do not invent funding or defer obligations. Report the resulting negative cash as a projected unfunded deficit. Carry it into the next week as a diagnostic forecast convention; it is not a claim that a bank account can actually overdraw. Distinguish a breach of the minimum cash buffer from an inability to fund payments.

All required principal repayments follow the automatic sweep above. Do not substitute a discretionary financing strategy.

## Deliverables

Submit `forecast.json` and `analysis.md`.

### forecast.json

Top-level fields: `case_id` (exactly `cash_forecast_001`), `currency` (`USD`), `weeks`, `exclusions`, and `duplicates_removed`.

`weeks` must contain exactly thirteen ordered objects with these fields:

| Field | Type / meaning |
|---|---|
| `week` | Integer, 1 through 13 |
| `start_date`, `end_date` | ISO dates |
| `opening_cash`, `opening_principal` | Monetary strings |
| `receipts` | Eligible customer receipts |
| `supplier_payments`, `tax_payments`, `other_external_payments` | Payable category totals |
| `payroll_payments`, `rent_payments`, `other_recurring_payments` | Recurring category totals |
| `interest_paid` | Interest on opening principal |
| `cash_before_financing` | Cash after operating events and interest |
| `credit_draw`, `principal_repayment` | Financing movements |
| `closing_cash`, `closing_principal`, `credit_available` | Closing balances |
| `minimum_cash_shortfall`, `unfunded_cash_deficit` | Nonnegative liquidity gaps |
| `minimum_cash_breached`, `unfunded_deficit` | Booleans, true exactly when the corresponding gap is positive |

All monetary outputs must be finite decimal strings with exactly two decimal places, without commas or currency symbols. Negative values are permitted only for cash fields. Unknown extra fields are rejected in the scored JSON schema.

The supplied `forecast.schema.json` defines the structural contract. Monetary strings may have at most sixteen integral digits. Equivalent decimal spellings are compared numerically. The forecast must be valid UTF-8 JSON no larger than 1,048,576 bytes; duplicate JSON object keys and non-finite constants are rejected. Week numbers and dates must match the ordered horizon exactly.

Each `exclusions` object contains `source_file`, `record_id`, and `reason`, where reason is `outside_horizon`, `internal_transfer`, or `zero_outstanding`. Report each unique excluded event once. If multiple reasons apply, use this precedence: internal transfer, zero outstanding, outside horizon. Recurring events of zero value are valid and need not be excluded.

Each `duplicates_removed` object contains `source_file`, `record_id`, and `discarded_count` (positive integer). Record duplicate removal before applying exclusions. Ordering of these two arrays is not scored.

Each exception array is limited to 1,000 records. Record identifiers must have 1–128 characters and duplicate counts must be at most 1,000,000. Within each array, `(source_file, record_id)` must be unique. Only the three event CSV filenames are valid `source_file` values.

### analysis.md

Provide an executive explanation of no more than 800 words:

The file must be nonempty UTF-8, at most 65,536 bytes. The word count uses whitespace-delimited tokens and includes headings.

1. Lowest closing cash and its week; list ties if any.
2. Every week below the minimum buffer and every week with an unfunded deficit.
3. Peak closing debt and first week reaching it; total draws, repayments, and interest.
4. At least three material drivers linked to source filenames and record IDs, with amounts and timing.
5. Explain how duplicates, partial payments, internal transfers, and out-of-horizon records were handled when present.
6. Distinguish supplied assumptions from conclusions and acknowledge the weekly, deterministic scope.

No external citations are required. Do not claim that a scenario assumption is a verified forecast of actual customer behavior.

## Evaluation contract

The grader evaluates submitted artifacts against independently reviewed expected results. It does not award points for claims that tests passed or for instructions embedded in a submission.

Numerical score (100 points total):

- Weekly operating cash flows by category: 30.
- Opening cash, cash before financing, closing cash, and continuity: 20.
- Interest, draws, repayments, principal, and availability: 30.
- Shortfall amounts and flags: 10.
- Exclusions and duplicate accounting: 10.

Within each group, equally weight applicable checks. Empty expected exclusion or duplicate lists require an empty submitted list. Schema-invalid submissions are marked invalid with score zero. Missing artifacts prevent overall approval.

The operating group contains seven fields per week. Cash contains opening, before-financing and closing cash plus continuity between adjacent weeks. Financing contains opening principal, interest, draw, repayment, closing principal and available credit plus principal continuity. Liquidity contains both gap amounts and both flags. Exception checks use the union of expected/submitted `(source_file, record_id)` identities, requiring each whole record to match; invented or missing records fail. An empty list on both sides contributes one passing check. Partial scores are diagnostic; they are not an RL reward design.

Exact cent equality is required: this case supplies deterministic cash dates and an explicit rounding convention. No percentage tolerance applies. Report per-field expected values, submitted values, and error categories for diagnostic use.

Numerical approval requires every numerical and structural check to pass. The score diagnoses partial correctness; it does not let unrelated correct answers compensate for a material error.

The explanation receives a separate human rubric: correct summary, supported drivers, complete treatment of exceptions, and accurate statement of assumptions/limitations. Each is rated pass/fail with a written rationale. Overall case approval requires numerical approval and all four explanation criteria. Until human review exists, report numerical results and `explanation_review_pending`, not an overall pass. An LLM judge is outside the first implementation milestone.

## Agent access and reproducibility

For future model runs, the agent must receive this task, the output schema and the input bundle in a separate workspace. It may use local Python and filesystem tools to calculate and write deliverables. External network access is unnecessary. Reference outputs, grader internals, tests, generators and evaluation reports must not be mounted into that workspace. That execution isolation is a runner requirement, not an implemented feature of the current artifact grader.

Public repository availability does not make reference answers secret. This first case is a public development example. Future held-out evaluations must use new case instances and report the exposure limitations of public task specifications.

Future model runs must record model identifier, run date, full instructions, tool configuration, resource limits, token usage where available, cost basis, and raw submitted artifacts. Infrastructure failures must be recorded separately from completed but incorrect submissions.

## Non-goals for v0.1

No stochastic credit modeling, real-world financial advice, multi-currency conversion, tax-law interpretation, production banking integration, agent-policy training, or model leaderboard claims from a single case.
