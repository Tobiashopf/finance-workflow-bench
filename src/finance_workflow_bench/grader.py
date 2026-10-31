"""Deterministic artifact grader. Candidate text is data, never executable code."""
import hashlib
import json
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from pathlib import Path

from .schemas import (OPERATING, CASH, FINANCING, LIQUIDITY_AMOUNTS, FLAGS, MONEY,
                      MAX_FORECAST_BYTES, MAX_ANALYSIS_BYTES, MAX_ANALYSIS_WORDS,
                      validate_forecast)

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "reference/cash_forecast_001/forecast.json"
# Pinned to the reference reviewed by the project owner. Do not refresh from a submission.
APPROVED_REFERENCE_SHA256 = "e0a1fa9abc309713b1cf15c55886d4a11165b7b9f281ae5c05eb67c5772e8747"
VERSION = "0.1.0"
CRITERIA = ["correct_summary", "supported_drivers", "complete_exceptions", "assumptions_and_limitations"]
WEIGHTS = dict(operating=30, cash=20, financing=30, liquidity=10, exceptions=10)


class SubmissionError(ValueError):
    pass


class EvaluatorError(RuntimeError):
    """Trusted reference/review or evaluator infrastructure failure, not agent failure."""


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_bounded(path, maximum):
    try:
        # Reject directory indirections and file links. Not a substitute for OS isolation.
        if path.is_symlink() or path.resolve().parent != path.parent.resolve():
            raise SubmissionError(f"Symbolic link not allowed: {path.name}")
        if not path.is_file():
            raise SubmissionError(f"Required regular file missing: {path.name}")
        with path.open("rb") as stream:
            raw = stream.read(maximum + 1)
        if len(raw) > maximum:
            raise SubmissionError(f"File exceeds {maximum} bytes: {path.name}")
        return raw
    except OSError as exc:
        raise EvaluatorError(f"Unable to read {path.name}: {type(exc).__name__}") from exc


def parse_json(raw):
    def pairs_hook(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise SubmissionError(f"Duplicate JSON key: {key}")
            obj[key] = value
        return obj

    def reject_constant(value):
        raise SubmissionError(f"Non-finite JSON constant: {value}")

    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs_hook, parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError) as exc:
        raise SubmissionError(f"Invalid UTF-8 JSON: {exc}") from exc


def trusted_reference(path=REFERENCE):
    try:
        raw = read_bounded(path, MAX_FORECAST_BYTES)
        if digest(raw) != APPROVED_REFERENCE_SHA256:
            raise EvaluatorError("Reviewed reference fingerprint mismatch; refusing to grade")
        expected = parse_json(raw)
        if validate_forecast(expected):
            raise EvaluatorError("Reviewed reference violates the output contract")
        return expected
    except SubmissionError as exc:
        raise EvaluatorError(f"Invalid trusted reference: {exc}") from exc


def review_template(forecast_hash, analysis_hash):
    return dict(grader_version=VERSION, forecast_sha256=forecast_hash, analysis_sha256=analysis_hash,
                reviewer="", criteria={k: dict(verdict="pending", rationale="") for k in CRITERIA})


def assess_review(path, submission_dir, forecast_hash, analysis_hash):
    # This option is an operator input. A review placed beside a candidate is never trusted.
    resolved = path.resolve()
    if resolved.is_relative_to(submission_dir.resolve()):
        raise EvaluatorError("Human review must be outside the submission directory")
    try:
        review = parse_json(read_bounded(path, MAX_ANALYSIS_BYTES))
    except SubmissionError as exc:
        raise EvaluatorError(f"Invalid operator review: {exc}") from exc
    expected_keys = {"grader_version", "forecast_sha256", "analysis_sha256", "reviewer", "criteria"}
    if type(review) is not dict or set(review) != expected_keys:
        raise EvaluatorError("Operator review has missing or unexpected fields")
    if review["grader_version"] != VERSION or review["forecast_sha256"] != forecast_hash or review["analysis_sha256"] != analysis_hash:
        raise EvaluatorError("Operator review is stale or belongs to different artifacts")
    if not isinstance(review["reviewer"], str) or not review["reviewer"].strip():
        raise EvaluatorError("Operator review requires a reviewer name")
    criteria = review["criteria"]
    if type(criteria) is not dict or set(criteria) != set(CRITERIA):
        raise EvaluatorError("Operator review requires all four rubric criteria")
    for value in criteria.values():
        if type(value) is not dict or set(value) != {"verdict", "rationale"}:
            raise EvaluatorError("Malformed human criterion")
        if value["verdict"] not in ("pass", "fail") or not isinstance(value["rationale"], str) or not value["rationale"].strip():
            raise EvaluatorError("Each criterion requires pass/fail and a written rationale")
    return dict(status="passed" if all(c["verdict"] == "pass" for c in criteria.values()) else "failed",
                reviewer=review["reviewer"], criteria=criteria)


def grade(submission_dir, review_path=None):
    expected = trusted_reference()
    directory = Path(submission_dir)
    report = dict(grader_version=VERSION, case_id="cash_forecast_001", reference_sha256=APPROVED_REFERENCE_SHA256,
                  status="invalid_submission", numerical_score=0.0, numerical_passed=False, overall_passed=False,
                  groups={}, mismatches=[], schema_errors=[], artifact_errors=[], explanation=dict(status="not_reviewable"))
    try:
        raw = read_bounded(directory / "forecast.json", MAX_FORECAST_BYTES)
        report["forecast_sha256"] = digest(raw)
        candidate = parse_json(raw)
        errors = validate_forecast(candidate)
        if errors:
            report["schema_errors"] = errors
            return report
    except SubmissionError as exc:
        report["artifact_errors"].append(str(exc))
        return report

    checks = {k: [] for k in WEIGHTS}

    def compare(group, path, wanted, got, category, monetary=False):
        equal = Decimal(wanted) == Decimal(got) if monetary else type(wanted) is type(got) and wanted == got
        checks[group].append(equal)
        if not equal:
            error = dict(group=group, path=path, category=category, expected=wanted, submitted=got)
            if monetary:
                error["difference"] = f"{Decimal(got) - Decimal(wanted):.2f}"
            report["mismatches"].append(error)

    for i, (wanted, got) in enumerate(zip(expected["weeks"], candidate["weeks"])):
        for group, fields in [("operating", OPERATING), ("cash", CASH), ("financing", FINANCING), ("liquidity", LIQUIDITY_AMOUNTS + FLAGS)]:
            for field in fields:
                compare(group, f"weeks[{i}].{field}", wanted[field], got[field], field, field in MONEY)
        if i:
            compare("cash", f"weeks[{i}].cash_continuity", candidate["weeks"][i - 1]["closing_cash"], got["opening_cash"], "cash_continuity", True)
            compare("financing", f"weeks[{i}].debt_continuity", candidate["weeks"][i - 1]["closing_principal"], got["opening_principal"], "debt_continuity", True)
    for name in ("exclusions", "duplicates_removed"):
        keyed = lambda rows: {(r["source_file"], r["record_id"]): r for r in rows}
        wanted, got = keyed(expected[name]), keyed(candidate[name])
        keys = sorted(wanted.keys() | got.keys())
        if not keys:
            compare("exceptions", name, [], [], name)
        for key in keys:
            compare("exceptions", f"{name}/{key[0]}/{key[1]}", wanted.get(key), got.get(key), name)
    total = Fraction(0)
    for group, values in checks.items():
        passed, count = sum(values), len(values)
        earned = Fraction(WEIGHTS[group] * passed, count)
        total += earned
        report["groups"][group] = dict(weight=WEIGHTS[group], checks=count, passed=passed,
                                      score=float((Decimal(earned.numerator) / Decimal(earned.denominator)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)))
    report["numerical_score"] = float((Decimal(total.numerator) / Decimal(total.denominator)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
    report["numerical_passed"] = all(all(values) for values in checks.values())
    report["status"] = "explanation_review_pending" if report["numerical_passed"] else "numerical_fail"
    try:
        analysis = read_bounded(directory / "analysis.md", MAX_ANALYSIS_BYTES)
        report["analysis_sha256"] = digest(analysis)
        try:
            text = analysis.decode("utf-8")
        except UnicodeError as exc:
            raise SubmissionError("analysis.md is not UTF-8") from exc
        words = len(text.split())
        report["analysis_word_count"] = words
        if not 1 <= words <= MAX_ANALYSIS_WORDS:
            raise SubmissionError("analysis.md must contain 1 to 800 whitespace-delimited words")
    except SubmissionError as exc:
        report["artifact_errors"].append(str(exc))
        report["status"] = "incomplete_submission"
        return report
    report["explanation"] = dict(status="explanation_review_pending")
    report["human_review_template"] = review_template(report["forecast_sha256"], report["analysis_sha256"])
    if review_path is not None:
        report["explanation"] = assess_review(Path(review_path), directory, report["forecast_sha256"], report["analysis_sha256"])
        if report["numerical_passed"]:
            report["status"] = "passed" if report["explanation"]["status"] == "passed" else "explanation_fail"
    report["overall_passed"] = report["status"] == "passed"
    return report
