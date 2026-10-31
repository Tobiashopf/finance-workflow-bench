"""Prepare allowed materials or import results. Never invokes a model or runs candidate code."""
import argparse
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from finance_workflow_bench.runs import build_package, prepare_run, finalize_run
from finance_workflow_bench.grader import EvaluatorError


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    bundle = commands.add_parser("package")
    bundle.add_argument("destination", type=Path)
    prepare = commands.add_parser("prepare")
    prepare.add_argument("package", type=Path)
    prepare.add_argument("destination", type=Path)
    finalize = commands.add_parser("import")
    finalize.add_argument("run", type=Path)
    finalize.add_argument("submission", type=Path)
    finalize.add_argument("execution_record", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "package":
            result = build_package(args.destination)
        elif args.command == "prepare":
            result = prepare_run(args.package, args.destination)
        else:
            result = finalize_run(args.run, args.submission, args.execution_record)
    except (ValueError, OSError, EvaluatorError, zipfile.BadZipFile) as exc:
        print(json.dumps(dict(status="operation_error", message=str(exc))))
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
