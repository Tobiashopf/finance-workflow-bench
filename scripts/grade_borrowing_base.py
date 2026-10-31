"""Numerical-only case 002 grader; explanation approval remains human and separate."""
import argparse
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from finance_workflow_bench.borrowing_base import validate, COLLATERAL, CONCENTRATION, CASH, VIOLATIONS, FLAGS
from finance_workflow_bench.grader import read_bounded, parse_json, digest, SubmissionError, EvaluatorError

PIN = "5866698763960143cf69fca6190bded4ea50556db697aaea8d1a6c4fea723189"


def grade(folder):
    return grade_registered(folder, "borrowing_base_002", ROOT / "reference/borrowing_base_002/forecast.json", PIN)


def grade_registered(folder, case_id, reference_path, pin):
    """Operator-side API; callers must obtain paths/pins from a trusted registry."""
    try:
        raw = read_bounded(reference_path, 1048576)
    except SubmissionError as exc:
        raise EvaluatorError(f"Reference unavailable: {exc}") from exc
    if digest(raw) != pin:
        raise EvaluatorError("Reference fingerprint mismatch")
    try:
        expected = parse_json(raw)
    except SubmissionError as exc:
        raise EvaluatorError("Reference JSON invalid") from exc
    if validate(expected, case_id=case_id):
        raise EvaluatorError("Reference schema mismatch")
    result = dict(case_id=case_id, grader_version="bb-0.1.0", reference_sha256=pin, numerical_score=0, numerical_passed=False, overall_passed=False,
                  status="invalid_submission", errors=[], mismatches=[], groups={})
    try:
        submitted = read_bounded(Path(folder)/"forecast.json", 1048576)
        result["forecast_sha256"] = digest(submitted)
        actual = parse_json(submitted)
        result["errors"] = validate(actual, case_id=case_id)
        if result["errors"]:
            return result
    except SubmissionError as exc:
        result["errors"] = [str(exc)]
        return result
    checks = {name: [] for name in ("eligibility", "concentration", "financing", "violations")}

    def compare(group, path, a, b):
        monetary = isinstance(a, str) and isinstance(b, str)
        # Only weekly scalar monetary strings reach this branch. Records use exact
        # IDs but normalize their monetary fields before semantic comparison.
        if monetary:
            equal = Decimal(a) == Decimal(b)
        elif isinstance(a, dict) and isinstance(b, dict):
            fields = {"outstanding_amount", "eligible_amount", "concentration_threshold", "recognized_amount", "concentration_deduction"}
            normalized = lambda r: {k: Decimal(v) if k in fields else v for k, v in r.items()}
            equal = normalized(a) == normalized(b)
        else:
            equal = type(a) is type(b) and a == b
        checks[group].append(equal)
        if not equal:
            error = dict(group=group, path=path, expected=a, submitted=b)
            if monetary:
                error["difference"] = f"{Decimal(b)-Decimal(a):.2f}"
            result["mismatches"].append(error)

    for i, (a, b) in enumerate(zip(expected["weeks"], actual["weeks"])):
        for group, fields in [("eligibility", COLLATERAL), ("concentration", CONCENTRATION), ("financing", CASH), ("violations", VIOLATIONS+FLAGS)]:
            for key in fields:
                compare(group, f"weeks[{i}].{key}", a[key], b[key])
    for array, ident, group in [("invoice_checks", "invoice_id", "eligibility"), ("customer_checks", "customer_id", "concentration")]:
        a = {(r["snapshot_date"], r[ident]): r for r in expected[array]}
        b = {(r["snapshot_date"], r[ident]): r for r in actual[array]}
        for key in sorted(a.keys() | b.keys()):
            compare(group, f"{array}/{key}", a.get(key), b.get(key))
    weights = dict(eligibility=20, concentration=20, financing=40, violations=20)
    total = Fraction(0)
    displayed = lambda v: float((Decimal(v.numerator)/Decimal(v.denominator)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
    for group, values in checks.items():
        earned = Fraction(weights[group]*sum(values), len(values))
        total += earned
        result["groups"][group] = dict(passed=sum(values), checks=len(values), score=displayed(earned))
    result["numerical_score"] = displayed(total)
    result["numerical_passed"] = all(all(v) for v in checks.values())
    result["status"] = "explanation_review_pending" if result["numerical_passed"] else "numerical_fail"
    try:
        raw_analysis = read_bounded(Path(folder)/"analysis.md", 65536)
        result["analysis_sha256"] = digest(raw_analysis)
        explanation = raw_analysis.decode("utf-8")
        result["analysis_word_count"] = len(explanation.split())
        if not 1 <= len(explanation.split()) <= 800:
            raise SubmissionError("Explanation must contain 1 to 800 words")
    except (SubmissionError, UnicodeError) as exc:
        result["status"] = "incomplete_submission"
        result["errors"].append(str(exc))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.report and (args.report.exists() or args.report.resolve().is_relative_to(args.submission.resolve())):
        parser.error("Report must be new and outside the submission directory")
    try:
        report = grade(args.submission)
        output = json.dumps(report, indent=2)+"\n"
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            with args.report.open("x", encoding="utf-8") as f:
                f.write(output)
        print(output)
    except (EvaluatorError, OSError) as exc:
        print(json.dumps(dict(status="evaluator_error", message=str(exc))))
        raise SystemExit(2)

