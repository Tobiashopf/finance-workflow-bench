"""Allowlisted agent packages and auditable manual result import. No model calls."""
import hashlib
import io
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from .grader import EvaluatorError, SubmissionError, grade, parse_json, read_bounded
from .schemas import MAX_FORECAST_BYTES, MAX_ANALYSIS_BYTES

ROOT = Path(__file__).resolve().parents[2]
FILES = {
    "task.md": "cases/cash_forecast_001/task.md",
    "forecast.schema.json": "schemas/forecast.schema.json",
    "agent_instructions.md": "prompts/agent_instructions.md",
    **{f"inputs/{name}": f"cases/cash_forecast_001/inputs/{name}" for name in (
        "opening_balances.csv", "receivables.csv", "payables.csv", "recurring_expenses.csv", "credit_facility.json")},
}
MAX_BUNDLE_BYTES = 8_388_608
EXECUTION_KEYS = {"kind", "provider", "model", "model_version", "outcome", "started_at_utc", "finished_at_utc",
                  "tools_used", "settings", "input_tokens", "output_tokens", "reported_cost_usd", "cost_basis",
                  "transfer_method", "failure_details", "operator_notes"}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    with path.open("x", encoding="utf-8") as f:
        f.write(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def now():
    return datetime.now(timezone.utc).isoformat()


def approved_payload():
    payload = {}
    for name, source in FILES.items():
        path = ROOT / source
        if not path.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError("Package source escapes the project")
        payload[name] = read_bounded(path, MAX_FORECAST_BYTES)
    return payload


def build_package(destination):
    destination = Path(destination)
    payload = approved_payload()
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, raw in sorted(payload.items()):
            entry = zipfile.ZipInfo(name, date_time=(2027, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, raw)
    raw = stream.getvalue()
    manifest = dict(format_version=1, case_id="cash_forecast_001", package_sha256=sha(raw),
                    files={name: sha(content) for name, content in sorted(payload.items())},
                    isolation="content_allowlist_only_not_process_isolation")
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "agent-package.zip").write_bytes(raw)
    save(destination / "manifest.json", manifest)
    return manifest


def verify_package(folder):
    folder = Path(folder)
    manifest = parse_json(read_bounded(folder / "manifest.json", MAX_ANALYSIS_BYTES))
    raw = read_bounded(folder / "agent-package.zip", MAX_BUNDLE_BYTES)
    if type(manifest) is not dict or manifest.get("package_sha256") != sha(raw):
        raise ValueError("Package fingerprint mismatch")
    expected = approved_payload()
    expected_hashes = {name: sha(data) for name, data in expected.items()}
    if manifest.get("files") != expected_hashes:
        raise ValueError("Package does not match the current allowlisted case")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if sorted(archive.namelist()) != sorted(FILES):
            raise ValueError("Unexpected, missing or duplicate archive members")
        for info in archive.infolist():
            if info.file_size > MAX_FORECAST_BYTES or info.compress_type != zipfile.ZIP_STORED:
                raise ValueError("Unexpected archive encoding or size")
            if archive.read(info) != expected[info.filename]:
                raise ValueError("Package content differs from approved source")
    return manifest, raw


def execution_template():
    return dict(kind="model_run", provider="", model="", model_version=None, outcome="not_run",
                started_at_utc=None, finished_at_utc=None, tools_used=[], settings={}, input_tokens=None,
                output_tokens=None, reported_cost_usd=None, cost_basis="unknown", transfer_method="",
                failure_details=None, operator_notes="Record the actual configuration; do not infer unavailable usage or cost.")


def prepare_run(package, destination):
    destination = Path(destination)
    manifest, raw = verify_package(package)
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "agent-package.zip").write_bytes(raw)
    save(destination / "package-manifest.json", manifest)
    save(destination / "execution-template.json", execution_template())
    run = dict(format_version=1, state="prepared", created_at_utc=now(), package_sha256=sha(raw),
               case_id="cash_forecast_001", model_execution="not_started", paid_calls_authorized=False,
               proposed_protocol=dict(attempts=1, fresh_conversation=True, feedback_during_attempt=False,
                                      browsing="not_requested", reference_access="not_provided"),
               enforcement="operator_reported_external_environment_not_verified")
    save(destination / "prepared.json", run)
    return run


def validate_execution(record):
    if type(record) is not dict or set(record) != EXECUTION_KEYS:
        raise ValueError("Execution record has missing or extra fields")
    if record["kind"] not in ("model_run", "pipeline_smoke_test"):
        raise ValueError("Unsupported run kind")
    if record["outcome"] not in ("completed", "provider_error", "tool_error", "timeout", "cancelled"):
        raise ValueError("Execution outcome must describe an actual attempt, not not_run")
    for field in ("provider", "model", "transfer_method", "operator_notes"):
        if not isinstance(record[field], str) or not record[field].strip():
            raise ValueError(f"Execution field requires text: {field}")
    if record["model_version"] is not None and not isinstance(record["model_version"], str):
        raise ValueError("Model version must be text or null")
    if not isinstance(record["tools_used"], list) or any(not isinstance(x, str) for x in record["tools_used"]):
        raise ValueError("tools_used must list observed tool names")
    if type(record["settings"]) is not dict:
        raise ValueError("settings must be an object; omit unknown settings")
    for field in ("input_tokens", "output_tokens"):
        if record[field] is not None and (type(record[field]) is not int or record[field] < 0):
            raise ValueError("Token counts must be nonnegative integers or null")
    cost = record["reported_cost_usd"]
    if cost is not None and (not isinstance(cost, str) or not re.fullmatch(r"[0-9]{1,12}\.[0-9]{2,6}", cost)):
        raise ValueError("Cost must be a nonnegative decimal string or null")
    if record["cost_basis"] not in ("unknown", "provider_reported", "operator_estimate", "no_model_call"):
        raise ValueError("Unknown cost basis")
    if (cost is None) != (record["cost_basis"] == "unknown"):
        raise ValueError("Unknown costs must be null; known costs require their basis")
    if record["kind"] == "model_run" and record["cost_basis"] == "no_model_call":
        raise ValueError("A model run cannot be marked no_model_call")
    times = []
    for field in ("started_at_utc", "finished_at_utc"):
        if record[field] is None:
            times.append(None)
            continue
        if not isinstance(record[field], str):
            raise ValueError("Timestamps must be ISO text or null")
        value = datetime.fromisoformat(record[field].replace("Z", "+00:00"))
        if value.utcoffset() is None or value.utcoffset().total_seconds() != 0:
            raise ValueError("Timestamps must include the UTC offset")
        times.append(value)
    if (times[0] is None) != (times[1] is None):
        raise ValueError("Provide both timestamps or leave both null")
    elapsed = None if times[0] is None else (times[1] - times[0]).total_seconds()
    if elapsed is not None and elapsed < 0:
        raise ValueError("Finish cannot precede start")
    if record["outcome"] != "completed" and (not isinstance(record["failure_details"], str) or not record["failure_details"].strip()):
        raise ValueError("Failed attempts require failure details")
    if record["outcome"] == "completed" and record["failure_details"] is not None:
        raise ValueError("Completed attempt must have null failure_details")
    return elapsed


def finalize_run(run_dir, submission, execution_file):
    run_dir, submission, execution_file = Path(run_dir), Path(submission), Path(execution_file)
    if execution_file.resolve().is_relative_to(submission.resolve()):
        raise ValueError("Execution metadata must be supplied by the operator outside the submission directory")
    if (run_dir / "result.json").exists() or (run_dir / "submission").exists():
        raise ValueError("Run already imported or incomplete import exists; preserve it and prepare a new run")
    prepared = parse_json(read_bounded(run_dir / "prepared.json", MAX_ANALYSIS_BYTES))
    manifest = parse_json(read_bounded(run_dir / "package-manifest.json", MAX_ANALYSIS_BYTES))
    raw_package = read_bounded(run_dir / "agent-package.zip", MAX_BUNDLE_BYTES)
    if sha(raw_package) != prepared.get("package_sha256") or prepared.get("package_sha256") != manifest.get("package_sha256"):
        raise ValueError("Prepared run package changed")
    if manifest.get("files") != {name: sha(data) for name, data in approved_payload().items()}:
        raise ValueError("Case changed after run preparation; create a new run")
    with zipfile.ZipFile(io.BytesIO(raw_package)) as archive:
        if sorted(archive.namelist()) != sorted(FILES):
            raise ValueError("Prepared archive contains unexpected members")
        for info in archive.infolist():
            if info.file_size > MAX_FORECAST_BYTES or info.compress_type != zipfile.ZIP_STORED:
                raise ValueError("Prepared archive encoding or size changed")
            if sha(archive.read(info)) != manifest["files"][info.filename]:
                raise ValueError("Prepared archive content does not match its manifest")
    raw_execution = read_bounded(execution_file, MAX_ANALYSIS_BYTES)
    execution = parse_json(raw_execution)
    elapsed = validate_execution(execution)
    # Read only literal expected filenames, never paths supplied by candidate JSON.
    artifacts = {}
    for name, maximum in (("forecast.json", MAX_FORECAST_BYTES), ("analysis.md", MAX_ANALYSIS_BYTES), ("transcript.txt", MAX_BUNDLE_BYTES)):
        path = submission / name
        if path.exists() or path.is_symlink():
            artifacts[name] = read_bounded(path, maximum)
    target = run_dir / "submission"
    target.mkdir()
    for name, raw in artifacts.items():
        (target / name).write_bytes(raw)
    (run_dir / "execution.json").write_bytes(raw_execution)
    result = dict(kind=execution["kind"], case_id="cash_forecast_001", package_sha256=prepared["package_sha256"],
                  imported_at_utc=now(), metadata_origin="operator_reported_not_independently_verified",
                  elapsed_seconds_operator_reported=elapsed, execution_sha256=sha(raw_execution),
                  artifact_sha256={name: sha(raw) for name, raw in artifacts.items()},
                  outcome=execution["outcome"], model_grade=None,
                  transcript_available="transcript.txt" in artifacts,
                  isolation="external_environment_not_verified")
    if execution["outcome"] == "completed":
        try:
            report = grade(target)
            save(run_dir / "grade.json", report)
            result["model_grade"] = {key: report[key] for key in ("status", "numerical_score", "numerical_passed", "overall_passed")}
        except EvaluatorError as exc:
            result["outcome"] = "evaluator_error"
            result["evaluator_error"] = str(exc)
    save(run_dir / "result.json", result)
    return result
