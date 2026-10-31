# Artifact grading, version 0.1.0

## Trust boundaries

The candidate supplies `forecast.json` and `analysis.md`. The operator runs the grader outside the candidate's execution environment. No candidate code, paths mentioned inside JSON, or instructions inside the explanation are executed. Extra files are ignored.

The reference is loaded from the evaluator's fixed project path and verified against a pinned SHA-256 digest. The CLI exposes no reference override. Reference corruption or an invalid operator review produces an `evaluator_error`, not an agent score of zero. A fingerprint is not a security boundary if the agent can modify the evaluator or its source: process/filesystem isolation remains future work.

The reference's financial scenario and computed results were reviewed by the project owner. See `reference/review-record.json`. This does not automatically approve any submitted explanation, nor constitute an external independent audit.

## Output validation

`schemas/forecast.schema.json` is an exported JSON Schema (2020-12). `schemas.py` implements a dependency-free validator for the specific keywords in that schema; it is not a general-purpose JSON Schema engine. Additional semantic validation enforces the exact thirteen dates/week numbers and unique `(source_file, record_id)` identities within each exception array.

- Strict UTF-8 JSON, without duplicate JSON keys or NaN/Infinity constants.
- Exactly the documented fields, thirteen ordered weeks, and real booleans.
- Money as decimal strings, exactly two fractional digits, at most sixteen integral digits. Negative signs only in cash fields. Numeric comparison allows equivalent forms such as `045000.00` and `45000.00`.
- No executable formulas or interpreted file references.
- Maximum forecast size: 1,048,576 bytes; maximum explanation size: 65,536 bytes.
- Explanation must have 1–800 whitespace-delimited words, including headings.
- Maximum 1,000 records in either exception array, identifiers 1–128 characters, positive duplicate counts at most 1,000,000.
- File symlinks are rejected; regular file reading is bounded. These protections do not provide process isolation or an adversarial filesystem sandbox.

Invalid forecast artifacts receive `invalid_submission` with score zero and a diagnostic. Missing or invalid explanations preserve a valid numerical diagnostic, but produce `incomplete_submission` and cannot pass overall.

## Exact score definition

| Group | Weight | Checks for the reference example |
|---|---:|---|
| Operating | 30 | 7 flow categories × 13 weeks = 91 |
| Cash | 20 | Opening, before financing and closing cash × 13, plus 12 cash continuity checks = 51 |
| Financing | 30 | Opening principal, interest, draw, repayment, closing principal and available credit × 13, plus 12 debt continuity checks = 90 |
| Liquidity | 10 | Two gap amounts and two flags × 13 = 52 |
| Exceptions | 10 | 7 exclusions and 4 duplicate identities = 11 |

Each group's score is its weight times the fraction of correct checks. Exception checks cover the union of expected and submitted identities; a missing or invented record fails its check. An identity matches only when the whole record matches. Array order is ignored. If both expected and submitted lists are empty, that list contributes one passing check. Repeated identities are schema-invalid, rather than counted repeatedly.

Cash/debt continuity compares the submitted opening amount with the preceding submitted closing amount. Values are also checked against the reference, so internally consistent but incorrect trajectories cannot pass.

Fraction arithmetic is used to sum weighted scores; reports display four decimal places. Monetary equality is exact to cents and has no relative tolerance.

**Numerical approval requires every check to pass, not a rounded score threshold.** Partial credit is diagnostic, not a validated RL reward. Many zeros are legitimately correct, so an all-zero forecast earns some partial credit but is rejected. Any future RL reward design must explicitly address that issue.

Each mismatch contains group, field path, expected and submitted values, error category and, for monetary comparisons, the signed difference (`submitted - expected`). Exception diagnostics include complete records.

## Human explanation review

The operator reviews four criteria, each with `pass` or `fail` and a written rationale:

1. `correct_summary`: minimum cash/week, all buffer breaches and deficits, peak debt/first week, and totals agree with the forecast.
2. `supported_drivers`: at least three material drivers cite real input filenames/record IDs, correct amounts and timing, and explain their financial significance.
3. `complete_exceptions`: duplicates, partial payments, internal transfers and horizon exclusions are explained correctly when present.
4. `assumptions_and_limitations`: supplied assumptions are distinguished from conclusions; weekly scope and the diagnostic treatment of negative cash are acknowledged.

A valid numerical answer with a bounded, nonempty explanation is `explanation_review_pending` until reviewed. The grader intentionally does not infer correctness from persuasive prose or keyword presence.

The report contains `human_review_template`. Copy that object to a separate operator-controlled file, fill in reviewer, verdicts and rationales, then run:

```sh
python scripts/grade.py path/to/submission --review path/to/operator-review.json --report reports/reviewed-run.json
```

The review file must be outside the submission directory. Its forecast hash, analysis hash and grader version must match; changes to either artifact require re-review. A candidate-authored review inside its directory is ignored and rejected if explicitly passed as the operator review. File location alone does not authenticate a reviewer: selecting the external file is a trusted operator action.

The software's positive/negative human-review unit tests use explicitly synthetic test decisions. They are not evidence that a real human approved those test submissions.

## Result states

| Status | Meaning |
|---|---|
| `invalid_submission` | Forecast absent, malformed or schema-invalid; numerical score zero |
| `numerical_fail` | Forecast structurally valid but at least one check failed |
| `incomplete_submission` | Explanation missing, empty, too long or invalid; numeric result retained |
| `explanation_review_pending` | All numeric checks pass, explanation awaits operator review |
| `explanation_fail` | All numeric checks pass, human rubric fails |
| `passed` | All numerical checks and four human criteria pass |
| `evaluator_error` | Trusted reference/review or evaluation infrastructure problem; no scored result |

Explanations on numerically failing answers may also be reviewed, but can never override numerical failures. `incomplete_submission` takes display precedence over `numerical_fail`; inspect `numerical_passed`, `artifact_errors` and mismatches to see both problems.

The CLI exits 0 when evaluation completes, even for a rejected or pending submission. Exit 2 indicates an evaluator/input-operation problem. A new report path is required for each saved run; existing reports are not overwritten. `overall_passed`, not process exit code or numerical score alone, is the final approval signal.

## Reproduce controlled demonstrations

```sh
python scripts/build_grader_demo.py
```

This writes fixtures to `examples/submissions/` and reports to `reports/grader-demo/`. These are controlled mutations, not model executions. Do not interpret their success rate as model performance or comprehensive resistance to every possible attack.
