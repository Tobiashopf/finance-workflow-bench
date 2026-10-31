"""Grade a case chosen by the operator, never by candidate-supplied paths."""
import argparse
import json
from pathlib import Path
from grade_borrowing_base import ROOT, grade_registered, EvaluatorError

CASES = ("bb_rounding_003", "bb_customer_004", "bb_cure_005", "bb_release_006")


def grade(case_id, folder):
    if case_id not in CASES:
        raise EvaluatorError("Unknown calibration case")
    registry = json.loads((ROOT/"reference/calibration-v1-registry.json").read_text(encoding="utf-8"))
    # The registry is operator-controlled and outside all submission packages.
    result = grade_registered(folder, case_id, ROOT/"reference"/case_id/"forecast.json", registry[case_id]["reference_sha256"])
    result["grader_version"] = "calibration-1.0"
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_id", choices=CASES)
    parser.add_argument("submission", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists() or args.report.resolve().is_relative_to(args.submission.resolve()):
        parser.error("Report must be new and outside submission")
    try:
        result = grade(args.case_id, args.submission)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with args.report.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2)
        print(json.dumps({k:result[k] for k in ("status","numerical_score","overall_passed")}))
    except (EvaluatorError, OSError, ValueError, KeyError) as exc:
        print(json.dumps(dict(status="evaluator_error", message=str(exc))))
        raise SystemExit(2)
