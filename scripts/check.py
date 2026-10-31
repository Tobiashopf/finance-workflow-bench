"""Run reference tests and the separate integer-cent verification."""
import runpy
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
result = unittest.TextTestRunner(verbosity=2).run(suite)
if not result.wasSuccessful():
    raise SystemExit(1)
runpy.run_path(str(ROOT / "scripts/verify_reference.py"), run_name="__main__")
runpy.run_path(str(ROOT / "scripts/verify_borrowing_base.py"), run_name="__main__")
fingerprints = {str(path.relative_to(ROOT)).replace("\\", "/"): hashlib.sha256(path.read_bytes()).hexdigest()
                for folder in ("src", "tests", "scripts") for path in sorted((ROOT / folder).rglob("*.py"))}
record = dict(status="passed", tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
              skipped=len(result.skipped), python_version=sys.version.split()[0], source_sha256=fingerprints,
              note="Automated reference and grader checks; not model evaluation or independent code audit")
(ROOT / "reports/test-results.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
