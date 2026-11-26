# Exploratory evaluation results

## Calibration battery

Eight submitted artifacts were evaluated against four pre-specified synthetic cases, and all eight achieved exact numerical agreement. Six explanations met the published 800-word limit; two Claude-labelled submissions contained 802 and 801 whitespace-delimited words. Those two retain 100/100 numerical scores but are incomplete submissions and were not eligible for formal explanation review. The six eligible explanations have all received formal human review; every review resulted in `explanation_fail`, so none is recorded as fully approved.

| Case | GPT run | Claude run | Checks per artifact |
|---|---|---|---:|
| 003 | [A](../runs/cal-v1-bb_rounding_003-A/grade.json) | [B](../runs/cal-v1-bb_rounding_003-B/grade.json) | 126 |
| 004 | [A](../runs/cal-v1-bb_customer_004-A/grade.json) | [B](../runs/cal-v1-bb_customer_004-B/grade.json) | 140 |
| 005 | [A](../runs/cal-v1-bb_cure_005-A/grade.json) | [B](../runs/cal-v1-bb_cure_005-B/grade.json) | 128 |
| 006 | [A](../runs/cal-v1-bb_release_006-A/grade.json) | [B](../runs/cal-v1-bb_release_006-B/grade.json) | 124 |

## Formal explanation review

| Run | Words | Final status | Human review record | Final grader report |
|---|---:|---|---|---|
| 003-A | 545 | `explanation_fail` | [review](../reviews/human/cal-v1-bb_rounding_003-A-review.json) | [report](../reports/human/bb_rounding_003-A-reviewed.json) |
| 003-B | 802 | `incomplete_submission` | Not eligible | [grade](../runs/cal-v1-bb_rounding_003-B/grade.json) |
| 004-A | 636 | `explanation_fail` | [review](../reviews/human/cal-v1-bb_customer_004-A-review.json) | [report](../reports/human/bb_customer_004-A-reviewed.json) |
| 004-B | 751 | `explanation_fail` | [review](../reviews/human/cal-v1-bb_customer_004-B-review.json) | [report](../reports/human/bb_customer_004-B-reviewed.json) |
| 005-A | 561 | `explanation_fail` | [review](../reviews/human/cal-v1-bb_cure_005-A-review.json) | [report](../reports/human/bb_cure_005-A-reviewed.json) |
| 005-B | 789 | `explanation_fail` | [review](../reviews/human/cal-v1-bb_cure_005-B-review.json) | [report](../reports/human/bb_cure_005-B-reviewed.json) |
| 006-A | 559 | `explanation_fail` | [review](../reviews/human/cal-v1-bb_release_006-A-review.json) | [report](../reports/human/bb_release_006-A-reviewed.json) |
| 006-B | 801 | `incomplete_submission` | Not eligible | [grade](../runs/cal-v1-bb_release_006-B/grade.json) |

A single reviewer is identified in the six formal review records; no independent second review is recorded. The two over-length submissions remain incomplete and were not reviewed for final approval.



Run folders retain the submitted content, original numerical grades, execution metadata, and separate preliminary AI reviews. Human-review reports are bound to the hashes recorded in the original grades. For the 004-A, 004-B, and 006-A final regrades, CRLF-to-LF normalization was performed in isolated copies without changing those local source folders. During the earlier 005-B regrade, the local working submission's line endings were normalized to LF to match its registered hashes; no financial or explanatory content changed. The reported shortening of the case-006 explanation did not bring its delivered text below the limit.

## Interpretation

The battery demonstrates traceable grading of financial workflows and separation of numerical correctness from delivery compliance. It did not demonstrate differences in numerical capability between the received submissions. Two length violations are descriptive observations, not a statistically supported model ranking.

Model names and conditions are operator-reported. The case-004 Claude record explicitly states that the configured model may differ from the model that actually responded. There is no independent model-identity attestation. Tools, reasoning modes, memory settings, attempt counts and browsing were not uniformly documented; missing values remain unknown rather than inherited across runs. No comparable cost or latency measurements are available.

These are four related public development scenarios, with one received artifact per service per case. They are not held-out tasks, repeated-trial reliability estimates or representative coverage of professional finance. Field-level checks are correlated. Both reference implementations were AI-assisted; owner reference review is not an independent code audit.

## Earlier pilots and historical records

Four earlier submissions on cases 001 and 002 also passed their numerical checks. They are separate exploratory pilots, not additional trials of the calibration battery. One mixed case-001 instructions with case-002 materials. See the [pilot report](../reports/manual-pilot-004-pt.md) and per-run addenda.

Historical design documents describe the state when authored and may say that a stage was pending. Later review records and execution addenda provide the updates; the current README and final reports summarize the latest state. Reference approval does not approve submitted explanations automatically.

## Next work

The planned model runs and formal human reviews of all six eligible explanations are complete. All six human reviews resulted in `explanation_fail`; the two over-length submissions remain incomplete. Remaining work is repository presentation/publication. Additional cases would require a new, prospectively specified evaluation version; current results must not be replaced or rescored to produce a preferred outcome.