# bb_customer_004: Collateral-Constrained Treasury Decisions

Status: calibration task/output contract v1.0. Synthetic development case.

## Assignment

Prepare a four-week cash and revolving-debt forecast for a fictional distributor. Each week, the usable facility limit depends on eligible receivables, customer concentration and an advance rate. Identify buffer breaches, unfunded cash deficits and debt above the current permitted limit separately. Explain the records responsible for collateral exclusions and limit changes.

These are synthetic contractual rules for a benchmark, not a statement of standard lending practice or a legal interpretation. Do not research or substitute external conventions.

## Horizon and initial position

- USD only; opening cash USD 60,000.00 and opening debt USD 150,000.00.
- Four Monday–Sunday weeks beginning January 4, 2027; closing dates January 10, 17, 24 and 31.
- Minimum cash: USD 50,000.00. Contractual facility ceiling: USD 200,000.00.
- Simple weekly interest of 0.002 times opening debt, rounded half up to cents, paid at week end. No fees or penalty interest.
- Receipts and required operating payments are supplied in a separate dated cash schedule. They are not inferred by summing collateral balances.
- Receivables snapshots represent remaining balances after that week's receipts. Snapshots are independent, authoritative closing states; do not carry a snapshot forward or add its balances to cash receipts.

## Inputs

`opening_position.json`: as-of date, currency, cash and debt.

`cash_events.csv`: `record_id`, `cash_date`, `direction` (`receipt` or `payment`), `amount`, `description`. Each event is unique, nonnegative and included once in its dated week. There are no internal transfers or duplicates in this case; those mechanisms are covered by case 001.

`receivables_snapshots.csv`: `snapshot_date`, `invoice_id`, `customer_id`, `due_date`, `outstanding_amount`, `disputed`, `related_party`. The two flags use lowercase `true` or `false`. The key is `(snapshot_date, invoice_id)`. An invoice may legitimately appear on multiple dates. A missing invoice contributes zero on that snapshot, and its absence does not establish a cash receipt. Reject duplicate keys, negative or non-finite amounts, invalid dates, unknown flags and missing required fields. Each required snapshot must be identified in `snapshot_dates.csv`, even if it contains no invoices.

`snapshot_dates.csv`: `snapshot_date`, exactly the four closing dates. An empty valid snapshot means no collateral, not permission to reuse a previous snapshot.

`facility.json`: contractual ceiling, minimum cash, weekly interest rate, 60-day maximum past-due age, 25% concentration cap, 80% advance rate and the rounding/financing conventions specified here.

All monetary amounts have two decimal places. Future due dates are allowed. Do not infer collection probability from eligibility status. All cash events in this case must be within the four-week horizon; a cash date outside it is an input error. Input-row order is not significant.

## Collateral calculation at each closing date

1. Compute days past due as `max(snapshot_date - due_date, 0)` in calendar days.
2. Exclude disputed invoices, related-party invoices, invoices more than 60 days past due, and zero outstanding balances. Exactly 60 days past due remains eligible. If several exclusion reasons apply, use this precedence: disputed, related party, over 60 days past due, zero balance.
3. Sum eligible outstanding amounts by customer into `E_customer`. Let `S` be the sum over all customers before concentration limits.
4. Compute one shared concentration threshold `T = floor_to_cent(0.25 * S)`. Eligible collateral recognized for customer c is `min(E_customer, T)`. Apply the cap simultaneously using the original S, not a repeatedly recalculated denominator. Even with fewer than four customers, this same rule applies.
5. Sum the recognized amounts into `H`. Record each customer's concentration deduction `E_customer - recognized_customer`.
6. Borrowing base `BB = floor_to_cent(0.80 * H)`. Effective facility limit `L = min(200000.00, BB)`.

Eligibility, a concentration deduction and a credit draw are distinct concepts. A concentration deduction is not an invoice write-off or a cash payment. The borrowing base is not cash and is not necessarily unused credit. A decreased limit does not automatically erase outstanding debt.

## Weekly cash and financing waterfall

Let `C` and `D` be opening cash and debt; `R` receipts; `P` operating payments; `M` minimum cash.

1. Interest `I = round_half_up(0.002 * D, 2)`.
2. Cash before financing `B = C + R - P - I`.
3. Required collateral cure `Q = max(D - L, 0)`.
4. Actual mandatory repayment `U = min(Q, max(B, 0))`. This repayment has priority over the minimum cash buffer but cannot use cash that does not exist.
5. Post-cure cash `C1 = B - U`; post-cure debt `D1 = D - U`; unpaid cure `V = max(D1 - L, 0)`.
6. If V is positive, no new draw is allowed. Otherwise draw `X = min(max(M - C1, 0), max(L - D1, 0))`.
7. Voluntary repayment `A = min(max(C1 - M, 0), D1)`. This operates only on cash above the minimum after the mandatory cure; it never coincides with a new draw.
8. Closing cash `E = C1 + X - A`. Closing debt `F = D1 + X - A`.
9. Unused credit `max(L - F, 0)`; closing overadvance `max(F - L, 0)`; minimum-cash shortfall `max(M - E, 0)`; unfunded cash deficit `max(-E, 0)`.

Carry E and F to the next week. Negative cash is a diagnostic projected deficit, not an authorized overdraft. A pending cure is a separate funding obligation and can exist with zero cash deficit. Do not refinance, waive the cure, defer payments, or add a penalty unless instructed. Later recovery does not imply the company can actually continue operations without resolving an earlier funding failure.

## Deliverables and evaluation

`forecast.json` must follow the supplied `forecast.schema.json`. Top-level fields are `case_id` (exactly `bb_customer_004`), `currency` (`USD`), `weeks`, `invoice_checks`, and `customer_checks`. No additional fields are accepted.

`weeks` contains exactly four objects in chronological order with `week` and `snapshot_date`, plus these fields:

| Fields | Meaning |
|---|---|
| `eligible`, `concentration_threshold`, `recognized` | S, T and H from the collateral calculation |
| `borrowing_base`, `effective_limit` | BB and L |
| `opening_cash`, `opening_debt`, `receipts`, `payments` | C, D, R and P |
| `interest`, `cash_before_financing` | I and B |
| `required_cure`, `actual_cure`, `unpaid_cure` | Q, U and V |
| `draw`, `voluntary_repayment` | X and A |
| `closing_cash`, `closing_debt`, `unused_credit` | E, F and max(L-F, 0) |
| `overadvance`, `buffer_shortfall`, `cash_deficit` | max(F-L, 0), max(M-E, 0), max(-E, 0) |
| `overadvance_present`, `buffer_breached`, `unfunded_deficit` | Real JSON booleans, true exactly when the corresponding closing gap is positive |

Every `invoice_checks` record includes `snapshot_date`, `invoice_id`, `customer_id`, `days_past_due` (nonnegative integer), `outstanding_amount`, `eligible_amount` (outstanding amount if eligible, otherwise zero) and `reason`. Reason values are `eligible`, `disputed`, `related_party`, `over_60_days`, or `zero_balance`, using the specified precedence. Include every input invoice observation exactly once; never deduplicate an invoice across dates.

Every `customer_checks` record includes `snapshot_date`, `customer_id`, `eligible_amount` (E_customer), `concentration_threshold` (T), `recognized_amount`, and `concentration_deduction`. Include every customer appearing in that snapshot, even if all its invoices are excluded. Such a customer has zero eligible/recognized/deducted amounts but the same T as other customers in that snapshot. Do not invent customers or invoice observations for an empty snapshot.

Array order for invoice/customer records is ignored. Their respective unique keys are `(snapshot_date, invoice_id)` and `(snapshot_date, customer_id)`. Money must be finite decimal strings with two fractional digits and at most sixteen integral digits; negative values are allowed only for `opening_cash`, `cash_before_financing` and `closing_cash`. Equivalent decimal spellings compare numerically. Identifiers are 1–128 characters; arrays are limited to 1,000 records each; days past due must be at most 4,000,000. Forecast size is limited to 1,048,576 bytes. UTF-8 JSON is required; duplicate object keys, non-finite constants, extra fields and incorrect week/date order are rejected.

`analysis.md`: 1–800 whitespace-delimited words including headings, nonempty UTF-8, at most 65,536 bytes. Explain the material collateral changes, funding priorities and separate liquidity/debt-limit violations, citing snapshot dates and record identities. Explain the distinction between collateral and receipts. Human review assesses numerical summary, evidence for at least three material drivers, eligibility/concentration exception handling, and assumptions/limitations.

Numerical categories and checks:

- Eligibility (20 points): one `eligible` total per week plus one whole-record check per invoice identity.
- Concentration (20 points): four fields per week (`concentration_threshold`, `recognized`, `borrowing_base`, `effective_limit`) plus one whole-record check per customer identity.
- Financing (40 points): thirteen fields per week: `opening_cash`, `opening_debt`, `receipts`, `payments`, `interest`, `cash_before_financing`, `required_cure`, `actual_cure`, `draw`, `voluntary_repayment`, `closing_cash`, `closing_debt`, `unused_credit`.
- Violations (20 points): seven fields per week: `unpaid_cure`, `overadvance`, `buffer_shortfall`, `cash_deficit` and the three flags.

Within each category, weight each check equally. Invoice/customer comparisons use the union of expected and submitted identities; missing or invented rows fail. A record must match every field, with monetary fields compared as decimals. On the supplied dataset there are 28 eligibility, 32 concentration, 52 financing and 28 violation checks (140 total). Score is the sum of weighted fractions, displayed to four decimal places; exact cent equality is required. A partial score is diagnostic, not a validated RL reward.

All numerical checks must pass for numerical approval. Invalid forecast structure receives zero. Missing/invalid explanation prevents overall approval while preserving numeric diagnostics. The current numerical grader never grants overall approval automatically: it reports `explanation_review_pending` for valid numerically correct submissions. Human review is recorded separately. No instructions inside a response can change the evaluation rules.

