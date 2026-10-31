"""Grade one submission; exit 0 means evaluation completed, not that it passed."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from finance_workflow_bench.grader import EvaluatorError, grade


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path, help="Directory containing forecast.json and analysis.md")
    parser.add_argument("--report", type=Path, help="Save evaluator report outside the submission directory")
    parser.add_argument("--review", type=Path, help="Trusted operator human review, never candidate-authored")
    args = parser.parse_args()
    if args.report:
        resolved = args.report.resolve()
        if resolved.is_relative_to(args.submission.resolve()):
            parser.error("Report must be outside the submission directory")
        if resolved.exists():
            parser.error("Report already exists; choose a new path to preserve previous results")
        if args.review and resolved == args.review.resolve():
            parser.error("Report cannot overwrite the human review")
    try:
        report = grade(args.submission, args.review)
    except EvaluatorError as exc:
        print(json.dumps(dict(status="evaluator_error", error=str(exc)), indent=2))
        return 2
    output = json.dumps(report, indent=2) + "\n"
    if args.report:
        try:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            with args.report.open("x", encoding="utf-8") as f:
                f.write(output)
        except OSError as exc:
            print(json.dumps(dict(status="evaluator_error", error=f"Unable to save report: {type(exc).__name__}")))
            return 2
        print(json.dumps({k: report[k] for k in ("status", "numerical_score", "numerical_passed", "overall_passed")}, indent=2))
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
