"""Exercise packaging/import with the known reference, clearly labeled as a smoke test."""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from finance_workflow_bench.runs import build_package, prepare_run, finalize_run, execution_template

with tempfile.TemporaryDirectory() as temp:
    base = Path(temp)
    manifest = build_package(base / "package")
    prepare_run(base / "package", base / "run")
    metadata = execution_template()
    metadata.update(kind="pipeline_smoke_test", provider="none", model="none", outcome="completed",
                    transfer_method="known_reference_fixture", reported_cost_usd="0.00", cost_basis="no_model_call",
                    operator_notes="Automated pipeline exercise using the known reference. No model was invoked.")
    record = base / "operator-record.json"
    record.write_text(json.dumps(metadata), encoding="utf-8")
    result = finalize_run(base / "run", ROOT / "reference/cash_forecast_001", record)
    if not result["model_grade"]["numerical_passed"] or result["model_grade"]["overall_passed"]:
        raise RuntimeError("Unexpected smoke-test grade")
    report = dict(kind="pipeline_smoke_test", status="passed", model_called=False, package_file_count=len(manifest["files"]),
                  package_sha256=manifest["package_sha256"], result=result,
                  limitation="Known reference fixture; this is not an AI capability evaluation or OS isolation test")
    (ROOT / "reports/pipeline-smoke.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("Pipeline smoke test passed: eight permitted files; no model call; no automatic overall approval.")
