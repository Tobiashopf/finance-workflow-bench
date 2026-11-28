# Exploratory evaluation results

## Calibration battery

Eight submitted artifacts were evaluated against four pre-specified synthetic cases, and all eight achieved exact numerical agreement. Six explanations met the published 800-word limit; two Claude-labelled submissions contained 802 and 801 whitespace-delimited words. Those two retain 100/100 numerical scores but are incomplete submissions and were not eligible for formal explanation review. The six eligible explanations first received human reviews that all resulted in `explanation_fail`. A second external audit was received on 27 November; by operator decision on 28 November, its verdicts were adopted unchanged as the current adjudication: four `passed`, two `explanation_fail`. The second reviewer states that the protected reference was unavailable; the 006-A form has an unidentified reviewer label. See the [operational log](../reports/human/calibration-v1-review-log.md) for these limitations and the disagreement record.

| Case | GPT run | Claude run | Checks per artifact |
|---|---|---|---:|
| 003 | [A](../runs/cal-v1-bb_rounding_003-A/grade.json) | [B](../runs/cal-v1-bb_rounding_003-B/grade.json) | 126 |
| 004 | [A](../runs/cal-v1-bb_customer_004-A/grade.json) | [B](../runs/cal-v1-bb_customer_004-B/grade.json) | 140 |
| 005 | [A](../runs/cal-v1-bb_cure_005-A/grade.json) | [B](../runs/cal-v1-bb_cure_005-B/grade.json) | 128 |
| 006 | [A](../runs/cal-v1-bb_release_006-A/grade.json) | [B](../runs/cal-v1-bb_release_006-B/grade.json) | 124 |

## Human explanation review and adjudication

The first review round, completed on 26 November, recorded `explanation_fail` for all six eligible submissions. The second reviewer returned forms on 27 November. The operator adopted the second review unchanged as the controlling adjudication on 28 November; the initial records remain available for comparison.

| Run | Words | Initial result | Second-review verdict | Adopted result | Initial review | External review | Adjudicated report |
|---|---:|---|---|---|---|---|---|
| 003-A | 545 | `explanation_fail` | `passed` | `passed` | [review](../reviews/human/cal-v1-bb_rounding_003-A-review.json) | [review](../reviews/human/second/cal-v1-bb_rounding_003-A-review.json) | [report](../reports/human/adjudicated/bb_rounding_003-A-adjudicated.json) |
| 003-B | 802 | `incomplete_submission` | Not reviewed | `incomplete_submission` | Not eligible | — | [grade](../runs/cal-v1-bb_rounding_003-B/grade.json) |
| 004-A | 636 | `explanation_fail` | `passed` | `passed` | [review](../reviews/human/cal-v1-bb_customer_004-A-review.json) | [review](../reviews/human/second/cal-v1-bb_customer_004-A-review.json) | [report](../reports/human/adjudicated/bb_customer_004-A-adjudicated.json) |
| 004-B | 751 | `explanation_fail` | `explanation_fail` | `explanation_fail` | [review](../reviews/human/cal-v1-bb_customer_004-B-review.json) | [review](../reviews/human/second/cal-v1-bb_customer_004-B-review.json) | [report](../reports/human/adjudicated/bb_customer_004-B-adjudicated.json) |
| 005-A | 561 | `explanation_fail` | `passed` | `passed` | [review](../reviews/human/cal-v1-bb_cure_005-A-review.json) | [review](../reviews/human/second/cal-v1-bb_cure_005-A-review.json) | [report](../reports/human/adjudicated/bb_cure_005-A-adjudicated.json) |
| 005-B | 789 | `explanation_fail` | `explanation_fail` | `explanation_fail` | [review](../reviews/human/cal-v1-bb_cure_005-B-review.json) | [review](../reviews/human/second/cal-v1-bb_cure_005-B-review.json) | [report](../reports/human/adjudicated/bb_cure_005-B-adjudicated.json) |
| 006-A | 559 | `explanation_fail` | `passed`* | `passed`* | [review](../reviews/human/cal-v1-bb_release_006-A-review.json) | [review](../reviews/human/second/cal-v1-bb_release_006-A-review.json) | [report](../reports/human/adjudicated/bb_release_006-A-adjudicated.json) |
| 006-B | 801 | `incomplete_submission` | Not reviewed | `incomplete_submission` | Not eligible | — | [grade](../runs/cal-v1-bb_release_006-B/grade.json) |

* The 006-A reviewer field is the supplied label `Auditor(a) — Revisão 6`; the actual reviewer identity is not established.

The first-round reviewer was Tobias Hopf de Souza. The external reviewer is recorded as Davi Hopf in forms 01–05. The audit notes say no protected reference was available for any of the six cases. The operator accepted the audit unchanged despite that procedural departure. The six `supported_drivers` verdicts differ from the first round; `assumptions_and_limitations` also differs for 004-B. In 004-A, the submitted forecast SHA-256 equals the registered reference SHA-256; the origin of that match is unknown. See the [operational log](../reports/human/calibration-v1-review-log.md).


Run folders retain the submitted content, original numerical grades, execution metadata, and separate preliminary AI reviews. Human-review reports are bound to the hashes recorded in the original grades. For the 004-A, 004-B, and 006-A final regrades, CRLF-to-LF normalization was performed in isolated copies without changing those local source folders. During the earlier 005-B regrade, the local working submission's line endings were normalized to LF to match its registered hashes; no financial or explanatory content changed. The reported shortening of the case-006 explanation did not bring its delivered text below the limit.

## Interpretation

The battery demonstrates traceable grading of financial workflows and separation of numerical correctness from delivery compliance. It did not demonstrate differences in numerical capability between the received submissions. Two length violations are descriptive observations, not a statistically supported model ranking.

Model names and conditions are operator-reported. The case-004 Claude record explicitly states that the configured model may differ from the model that actually responded. There is no independent model-identity attestation. Tools, reasoning modes, memory settings, attempt counts and browsing were not uniformly documented; missing values remain unknown rather than inherited across runs. No comparable cost or latency measurements are available.

These are four related public development scenarios, with one received artifact per service per case. They are not held-out tasks, repeated-trial reliability estimates or representative coverage of professional finance. Field-level checks are correlated. Both reference implementations were AI-assisted; owner reference review is not an independent code audit.

## Earlier pilots and historical records

Four earlier submissions on cases 001 and 002 also passed their numerical checks. They are separate exploratory pilots, not additional trials of the calibration battery. One mixed case-001 instructions with case-002 materials. See the [pilot report](../reports/manual-pilot-004-pt.md) and per-run addenda.

Historical design documents describe the state when authored and may say that a stage was pending. Later review records and execution addenda provide the updates; the current README and final reports summarize the latest state. Reference approval does not approve submitted explanations automatically.

## Next work

The planned model runs and both review rounds of the six eligible explanations are complete. The operator adopted the external audit as supplied: four explanations are recorded as `passed` and two as `explanation_fail`; the two over-length submissions remain incomplete. The audit's lack of protected-reference access, the unidentified 006-A reviewer label, and the 004-A reference-hash match are disclosed in the operational log. Additional cases would require a new, prospectively specified evaluation version; the original submissions and numerical grades remain unchanged.