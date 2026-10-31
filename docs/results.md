# Exploratory evaluation results

## Calibration battery

Eight submitted artifacts were evaluated against four pre-specified synthetic cases. All eight achieved exact numerical agreement. Six explanations met the published 800-word limit; two Claude-labelled submissions contained 802 and 801 whitespace-delimited words. These two retain 100/100 numerical scores but are incomplete submissions. The remaining six await human explanation review; none is recorded as fully approved.

| Case | GPT run | Claude run | Checks per artifact |
|---|---|---|---:|
| 003 | [A](../runs/cal-v1-bb_rounding_003-A/grade.json) | [B](../runs/cal-v1-bb_rounding_003-B/grade.json) | 126 |
| 004 | [A](../runs/cal-v1-bb_customer_004-A/grade.json) | [B](../runs/cal-v1-bb_customer_004-B/grade.json) | 140 |
| 005 | [A](../runs/cal-v1-bb_cure_005-A/grade.json) | [B](../runs/cal-v1-bb_cure_005-B/grade.json) | 128 |
| 006 | [A](../runs/cal-v1-bb_release_006-A/grade.json) | [B](../runs/cal-v1-bb_release_006-B/grade.json) | 124 |

All submitted files were preserved without editing. Each run folder also contains execution metadata and a preliminary AI content review. Internal drafting changes before submission are distinguished from revisions after evaluation. The reported shortening of the case-006 explanation did not bring its delivered text below the limit.

## Interpretation

The battery demonstrates traceable grading of financial workflows and separation of numerical correctness from delivery compliance. It did not demonstrate differences in numerical capability between the received submissions. Two length violations are descriptive observations, not a statistically supported model ranking.

Model names and conditions are operator-reported. The case-004 Claude record explicitly states that the configured model may differ from the model that actually responded. There is no independent model-identity attestation. Tools, reasoning modes, memory settings, attempt counts and browsing were not uniformly documented; missing values remain unknown rather than inherited across runs. No comparable cost or latency measurements are available.

These are four related public development scenarios, with one received artifact per service per case. They are not held-out tasks, repeated-trial reliability estimates or representative coverage of professional finance. Field-level checks are correlated. Both reference implementations were AI-assisted; owner reference review is not an independent code audit.

## Earlier pilots and historical records

Four earlier submissions on cases 001 and 002 also passed their numerical checks. They are separate exploratory pilots, not additional trials of the calibration battery. One mixed case-001 instructions with case-002 materials. See the [pilot report](../reports/manual-pilot-004-pt.md) and per-run addenda.

Historical design documents describe the state when authored and may say that a stage was pending. Later review records and execution addenda provide the updates; the current README and final reports summarize the latest state. Reference approval does not approve submitted explanations automatically.

## Next work

The planned model runs are complete. Remaining work is human explanation review and repository presentation/publication. Additional cases would require a new, prospectively specified evaluation version; current results must not be replaced or rescored to produce a preferred outcome.