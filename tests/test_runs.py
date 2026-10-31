import copy
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from finance_workflow_bench.grader import EvaluatorError
from finance_workflow_bench.runs import (FILES, ROOT, build_package, verify_package, prepare_run,
                                         finalize_run, execution_template, validate_execution)


class RunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.package = self.base / "package"
        build_package(self.package)

    def record(self, outcome="completed"):
        record = execution_template()
        record.update(kind="pipeline_smoke_test", provider="none", model="none",
                      outcome=outcome, transfer_method="synthetic_test_fixture", operator_notes="Unit test, not a model run.",
                      reported_cost_usd="0.00", cost_basis="no_model_call")
        if outcome != "completed":
            record["failure_details"] = "Simulated provider error, not a real outage."
        return record

    def prepare(self):
        run = self.base / "run"
        prepare_run(self.package, run)
        return run

    def save_record(self, record):
        path = self.base / "execution.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        return path

    def test_package_is_exact_allowlist_and_deterministic(self):
        second = self.base / "second"
        build_package(second)
        self.assertEqual((self.package / "agent-package.zip").read_bytes(), (second / "agent-package.zip").read_bytes())
        with zipfile.ZipFile(self.package / "agent-package.zip") as archive:
            self.assertEqual(set(archive.namelist()), set(FILES))
            self.assertEqual(len(archive.namelist()), 8)
            self.assertFalse(any("reference" in n or "grader" in n or "report" in n for n in archive.namelist()))
        verify_package(self.package)

    def test_package_tampering_rejected(self):
        with (self.package / "agent-package.zip").open("ab") as stream:
            stream.write(b"tampered")
        with self.assertRaises(ValueError):
            verify_package(self.package)

    def test_package_manifest_tampering_rejected(self):
        path = self.package / "manifest.json"
        record = json.loads(path.read_text())
        record["files"]["reference.json"] = "made-up"
        path.write_text(json.dumps(record))
        with self.assertRaises(ValueError):
            prepare_run(self.package, self.base / "bad")
        self.assertFalse((self.base / "bad").exists())

    def test_destinations_cannot_be_overwritten(self):
        with self.assertRaises(FileExistsError):
            build_package(self.package)
        run = self.prepare()
        with self.assertRaises(FileExistsError):
            prepare_run(self.package, run)

    def test_prepared_run_does_not_claim_model_execution(self):
        run = self.prepare()
        record = json.loads((run / "prepared.json").read_text())
        self.assertEqual(record["model_execution"], "not_started")
        self.assertFalse(record["paid_calls_authorized"])
        with self.assertRaises(ValueError):
            validate_execution(json.loads((run / "execution-template.json").read_text()))

    def test_import_correct_fixture_preserves_bytes_and_kind(self):
        run = self.prepare()
        source = ROOT / "reference/cash_forecast_001"
        result = finalize_run(run, source, self.save_record(self.record()))
        self.assertEqual(result["kind"], "pipeline_smoke_test")
        self.assertTrue(result["model_grade"]["numerical_passed"])
        self.assertFalse(result["model_grade"]["overall_passed"])
        self.assertEqual((run / "submission/forecast.json").read_bytes(), (source / "forecast.json").read_bytes())
        self.assertFalse((run / "submission/source_ledger.json").exists())
        self.assertIsNone(result["elapsed_seconds_operator_reported"])
        with self.assertRaises(ValueError):
            finalize_run(run, source, self.base / "execution.json")

    def test_model_metadata_preserves_unknown_cost_and_usage(self):
        record = self.record()
        record.update(kind="model_run", provider="test-provider", model="test-model-label", reported_cost_usd=None, cost_basis="unknown")
        validate_execution(record)
        run = self.prepare()
        result = finalize_run(run, self.base / "empty", self.save_record(record))
        stored = json.loads((run / "execution.json").read_text())
        self.assertIsNone(stored["input_tokens"])
        self.assertIsNone(stored["reported_cost_usd"])
        self.assertEqual(result["model_grade"]["status"], "invalid_submission")

    def test_provider_failure_is_not_model_score_zero(self):
        run = self.prepare()
        result = finalize_run(run, self.base / "absent", self.save_record(self.record("provider_error")))
        self.assertIsNone(result["model_grade"])
        self.assertEqual(result["outcome"], "provider_error")
        self.assertFalse((run / "grade.json").exists())

    def test_evaluator_failure_is_not_model_score_zero(self):
        run = self.prepare()
        with patch("finance_workflow_bench.runs.grade", side_effect=EvaluatorError("Synthetic failure")):
            result = finalize_run(run, ROOT / "reference/cash_forecast_001", self.save_record(self.record()))
        self.assertEqual(result["outcome"], "evaluator_error")
        self.assertIsNone(result["model_grade"])

    def test_altered_prepared_package_rejected(self):
        run = self.prepare()
        (run / "agent-package.zip").write_bytes(b"changed")
        with self.assertRaises(ValueError):
            finalize_run(run, self.base / "empty", self.save_record(self.record()))
        self.assertFalse((run / "result.json").exists())

    def test_missing_answer_files_are_not_repaired(self):
        run = self.prepare()
        result = finalize_run(run, self.base / "empty", self.save_record(self.record()))
        self.assertEqual(result["model_grade"]["status"], "invalid_submission")
        self.assertEqual(result["artifact_sha256"], {})

    def test_candidate_execution_record_is_not_trusted(self):
        run = self.prepare()
        source = self.base / "candidate"
        source.mkdir()
        record = source / "execution.json"
        record.write_text(json.dumps(self.record()))
        with self.assertRaises(ValueError):
            finalize_run(run, source, record)
        self.assertFalse((run / "submission").exists())

    def test_execution_metadata_validation(self):
        mutations = [dict(outcome="not_run"), dict(input_tokens=True), dict(output_tokens=-1),
                     dict(provider=""), dict(cost_basis="unknown"), dict(reported_cost_usd="NaN"),
                     dict(kind="model_run"), dict(tools_used="Python"), dict(failure_details="contradictory"),
                     dict(started_at_utc="2027-01-01T00:00:00Z"),
                     dict(started_at_utc="2027-01-01T00:00:00", finished_at_utc="2027-01-01T00:01:00"),
                     dict(started_at_utc="2027-01-01T00:02:00Z", finished_at_utc="2027-01-01T00:01:00Z")]
        for update in mutations:
            with self.subTest(update=update):
                record = self.record()
                record.update(update)
                with self.assertRaises(ValueError):
                    validate_execution(record)
        timed = self.record()
        timed.update(started_at_utc="2027-01-01T00:00:00Z", finished_at_utc="2027-01-01T00:01:30Z")
        self.assertEqual(validate_execution(timed), 90)


if __name__ == "__main__":
    unittest.main()
