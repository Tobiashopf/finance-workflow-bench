# Manual execution and artifact import

## Implemented scope

The run tooling packages allowed input files, prepares an immutable initial run record,
and imports operator-supplied artifacts. It **does not** call a provider, execute model
code, enforce a time/token budget, or create an OS/container sandbox. The first selected
route is an existing subscription chat with manual upload and download.

An empty provider or `not_run` outcome is allowed in a template but rejected during
import. A prepared run is not evidence that a model was executed.

## Commands

```sh
python scripts/run.py package packages/cash_forecast_001-v0.2
python scripts/run.py prepare packages/cash_forecast_001-v0.2 runs/manual-pilot-001
python scripts/run.py import runs/manual-pilot-001 path/to/downloads path/to/operator-execution.json
```

Package and run destinations must not already exist. No secrets or API credentials
are needed. A prepared folder contains a byte-identical package, package manifest,
initial record and execution-record template. Copy and complete the template in an
operator-controlled file after the actual attempt; do not replace unknowns with guesses.

## Package contract

The ZIP is built from a literal allowlist of eight files. Fixed archive timestamps,
stable ordering and stored compression make identical source files produce identical
archives. The manifest lives outside the archive and contains per-file and whole-archive
SHA-256 values. Archive members are validated without extracting arbitrary paths.

The package is verified against current project sources at preparation. Any changes to
the case inputs/schema/instructions invalidate an old prepared run for import with the
current case. Preserve the old project version if evaluating an older package.

The task/schema/instructions are the full intended prompt contract. The operator should
paste the included instructions verbatim in a fresh conversation and record any deviation.
Do not upload the project directory or evaluator reports.

## Execution record

`kind` is `model_run` or `pipeline_smoke_test`; smoke tests must never appear as model
performance. Record provider, UI model label and exact model version if available.
Unknown version, timestamps, token usage and per-run cost remain null. Known cost must
include its basis (`provider_reported` or `operator_estimate`); `no_model_call` is only
valid for a smoke test.

`tools_used` contains observed tool names; `settings` records known settings only.
`operator_notes` should state fresh-conversation status, number of attempts, intervention,
and whether browsing was disabled, merely requested off, or unknown. Metadata is
operator-reported and is not a provider attestation.

Timestamps, if supplied, must include UTC and be ordered. Elapsed time is derived only
from two supplied timestamps. A copied transcript is optional and its absence is recorded.

`outcome` must be completed, provider_error, tool_error, timeout or cancelled. Non-completed
attempts require a description and are recorded with no model grade. Do not mark a completed
but incorrect financial answer as a provider error. Unsupported downloading or tool failures
must be described, so later analysis can distinguish capability and infrastructure limits.

## Import behavior

The importer copies only literal `forecast.json`, `analysis.md` and optional `transcript.txt`.
Artifacts are copied byte-for-byte with bounded reads and recorded hashes. It does not execute
or repair them. Missing answer files from a completed attempt are graded as missing/invalid;
oversized or linked files cause an import error rather than silent truncation. No input
archive extraction or dynamic file paths from candidate content are used.

The original prepared record is retained. `result.json` is the final state for an imported
run; `execution.json` records the supplied metadata, `submission/` holds snapshots, and
`grade.json` holds the grader output when the attempt completed. A second import is refused.
An interrupted partial import is preserved for inspection; prepare a new run to retry.

Evaluator failures have no numerical grade and are labeled separately. A valid financial
answer still needs its own explanation review. Final approval remains the grader's
`overall_passed` flag, not import success or a numerical score alone.

## Threat model and limitations

The operator and project source files are trusted. Hashes detect accidental changes; they
are not signatures and do not protect against an attacker rewriting both manifests and
code. Copying allowed materials does not verify a provider's filesystem isolation, memory,
network restrictions or lack of prior benchmark exposure. No live local isolation runtime
has been tested. Untrusted model code must not be run on the host through this workflow.

This public single-case pilot is descriptive evidence, not a held-out benchmark or a
statistically supported model ranking. Preserve unsuccessful attempts, use the same protocol,
and disclose tool/configuration differences before comparing runs.
