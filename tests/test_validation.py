"""Independent examples of valid and misleading fictional case artifacts."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate.py"
TEMP_PARENT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("case_validation", SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def baseline():
    """Small synthetic fixture deliberately independent of the portfolio data."""
    register = {
        "kind": "fictional_risk_assessment", "assessment_date": "2026-10-31",
        "assets": [{"id": "A01", "name": "Synthetic service", "owner_role": "Service owner", "data_categories": ["synthetic events"]}],
        "risks": [{
            "id": "R01", "asset_ids": ["A01"], "owner_role": "Service owner",
            "scenario": "A hypothetical administrative error interrupts the service.",
            "likelihood": 2, "impact": 3, "score": 6, "band": "moderate",
            "rationale": "Several conditions are needed; interruption could affect scheduling.",
            "control_ids": ["C01"], "treatment_id": "T01", "acceptance": "pending",
            "actual_residual": None, "escalation_required": False,
        }],
    }
    treatments = {"kind": "fictional_proposed_treatments", "treatments": [{
        "id": "T01", "risk_id": "R01", "control_ids": ["C01"], "status": "proposed",
        "review_window_days": 7, "action": "Propose a scoped recovery exercise.",
        "required_evidence": ["Recorded recovery results for synthetic events"],
        "implementation_evidence": [], "approval": "pending",
    }]}
    controls = {
        "kind": "fictional_proposed_controls", "coverage": "illustrative_subset_not_full_iso_annex_a",
        "controls": [
            {"id": "C01", "name": "Recovery exercise", "applicable": True,
             "reason": "The service depends on recoverable records.", "risk_ids": ["R01"],
             "nsm_principles": ["2.9"], "status": "proposed", "evidence_status": "not_implemented"},
            {"id": "C02", "name": "Medical device management", "applicable": False,
             "reason": "Medical devices are outside this administrative service exercise.", "risk_ids": [],
             "nsm_principles": [], "status": "not_applicable", "evidence_status": "not_applicable"},
        ],
    }
    return register, treatments, controls


class ValidationTests(unittest.TestCase):
    def assert_code(self, documents, code):
        errors = validator.validate_documents(*documents)
        self.assertIn(code, {error["code"] for error in errors}, errors)
        self.assertTrue(all(error["path"] and error["message"] for error in errors))

    def test_valid_baseline_and_no_mutation(self):
        documents = baseline()
        original = copy.deepcopy(documents)
        self.assertEqual([], validator.validate_documents(*documents))
        self.assertEqual(original, documents)

    def test_band_boundaries(self):
        expected = {1: "low", 4: "low", 5: "moderate", 9: "moderate", 10: "high", 16: "high", 17: "critical", 25: "critical"}
        for score, band in expected.items():
            with self.subTest(score=score):
                self.assertEqual(band, validator.score_band(score))
        for invalid in (0, 26, True, False, 1.0, "5", None):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                validator.score_band(invalid)

    def test_impact_five_escalates_even_with_moderate_product(self):
        documents = baseline()
        risk = documents[0]["risks"][0]
        risk.update(likelihood=1, impact=5, score=5, band="moderate", escalation_required=True)
        self.assertEqual([], validator.validate_documents(*documents))
        risk["escalation_required"] = False
        self.assert_code(documents, "ESCALATION_MISMATCH")

    def test_critical_score_escalates_with_impact_below_five(self):
        documents = baseline()
        documents[0]["risks"][0].update(likelihood=5, impact=4, score=20, band="critical", escalation_required=True)
        self.assertEqual([], validator.validate_documents(*documents))
        documents[0]["risks"][0]["escalation_required"] = 1
        self.assert_code(documents, "ESCALATION_MISMATCH")

    def test_missing_escalation_flag_is_rejected(self):
        documents = baseline()
        del documents[0]["risks"][0]["escalation_required"]
        self.assert_code(documents, "ESCALATION_MISMATCH")

    def test_score_and_band_are_recalculated(self):
        documents = baseline()
        documents[0]["risks"][0].update(score=4, band="low")
        self.assert_code(documents, "SCORE_MISMATCH")
        self.assert_code(documents, "BAND_MISMATCH")

    def test_duplicate_identifiers_in_every_register(self):
        for document_index, key in ((0, "assets"), (0, "risks"), (1, "treatments"), (2, "controls")):
            with self.subTest(key=key):
                documents = baseline()
                documents[document_index][key].append(copy.deepcopy(documents[document_index][key][0]))
                self.assert_code(documents, "DUPLICATE_ID")

    def test_duplicate_reference(self):
        documents = baseline()
        documents[0]["risks"][0]["asset_ids"].append("A01")
        self.assert_code(documents, "DUPLICATE_REFERENCE")

    def test_unknown_references(self):
        examples = ((0, "risks", "asset_ids", ["A99"], "UNKNOWN_ASSET"),
                    (0, "risks", "control_ids", ["C99"], "UNKNOWN_CONTROL"),
                    (0, "risks", "treatment_id", "T99", "UNKNOWN_TREATMENT"),
                    (1, "treatments", "risk_id", "R99", "UNKNOWN_RISK"),
                    (1, "treatments", "control_ids", ["C99"], "UNKNOWN_CONTROL"),
                    (2, "controls", "risk_ids", ["R99"], "UNKNOWN_RISK"))
        for index, key, field, value, code in examples:
            with self.subTest(field=field, index=index):
                documents = baseline()
                documents[index][key][0][field] = value
                self.assert_code(documents, code)

    def test_orphan_treatment_is_rejected(self):
        documents = baseline()
        orphan = copy.deepcopy(documents[1]["treatments"][0])
        orphan["id"] = "T02"
        documents[1]["treatments"].append(orphan)
        self.assert_code(documents, "TREATMENT_RECIPROCITY")

    def test_control_reciprocity_in_both_directions(self):
        documents = baseline()
        documents[2]["controls"][0]["risk_ids"] = []
        self.assert_code(documents, "CONTROL_RECIPROCITY")
        documents = baseline()
        extra = copy.deepcopy(documents[2]["controls"][0])
        extra["id"] = "C03"
        documents[2]["controls"].append(extra)
        self.assert_code(documents, "CONTROL_RECIPROCITY")

    def test_risk_and_treatment_control_sets_must_match(self):
        documents = baseline()
        documents[1]["treatments"][0]["control_ids"] = ["C02"]
        self.assert_code(documents, "TREATMENT_CONTROL_MISMATCH")

    def test_numeric_types_and_ranges(self):
        for field, values in (("likelihood", (0, 6, True, 2.0, "2", None)),
                              ("impact", (0, 6, False, 3.0, "3", [])),
                              ("score", (0, 26, True, 6.0, "6", {}))):
            for value in values:
                with self.subTest(field=field, value=value):
                    documents = baseline()
                    documents[0]["risks"][0][field] = value
                    self.assert_code(documents, "INTEGER_RANGE")
        for value in (0, -1, True, 7.0, "7"):
            with self.subTest(review_window_days=value):
                documents = baseline()
                documents[1]["treatments"][0]["review_window_days"] = value
                self.assert_code(documents, "INTEGER_RANGE")

    def test_false_completion_acceptance_and_residual_claims(self):
        examples = ((0, "risks", "acceptance", "accepted"),
                    (0, "risks", "actual_residual", {"score": 2}),
                    (1, "treatments", "status", "completed"),
                    (1, "treatments", "approval", "approved"),
                    (1, "treatments", "implementation_evidence", ["unverified screenshot"]),
                    (2, "controls", "status", "implemented"),
                    (2, "controls", "evidence_status", "verified"))
        for index, key, field, value in examples:
            with self.subTest(field=field, index=index):
                documents = baseline()
                documents[index][key][0][field] = value
                self.assert_code(documents, "REQUIRED_VALUE")

    def test_exclusion_requires_reason_and_no_risk_links(self):
        documents = baseline()
        documents[2]["controls"][1]["reason"] = "  "
        self.assert_code(documents, "REQUIRED_TEXT")
        documents = baseline()
        documents[2]["controls"][1]["risk_ids"] = ["R01"]
        self.assert_code(documents, "REQUIRED_VALUE")
        documents[0]["risks"][0]["control_ids"].append("C02")
        self.assert_code(documents, "EXCLUDED_CONTROL_REFERENCE")

    def test_missing_nullable_field_and_wrong_applicability_type(self):
        documents = baseline()
        del documents[0]["risks"][0]["actual_residual"]
        self.assert_code(documents, "REQUIRED_VALUE")
        documents = baseline()
        documents[2]["controls"][0]["applicable"] = 1
        self.assert_code(documents, "BOOLEAN_REQUIRED")

    def test_structurally_malformed_input_returns_errors(self):
        for value in (None, [], "text", 12, True):
            with self.subTest(value=value):
                self.assert_code((value, value, value), "DOCUMENT_OBJECT")
        documents = baseline()
        documents[0]["risks"][0].update(treatment_id=[], asset_ids={}, control_ids=[None, {}])
        documents[1]["treatments"][0]["risk_id"] = {}
        self.assert_code(documents, "STRING_LIST")


class FileAndCliTests(unittest.TestCase):
    def write_fixture(self, directory):
        for filename, document in zip(validator.INPUT_NAMES, baseline()):
            (directory / filename).write_text(json.dumps(document), encoding="utf-8")

    def test_report_hashes_match_input_bytes(self):
        with tempfile.TemporaryDirectory(dir=TEMP_PARENT) as temporary:
            directory = Path(temporary)
            self.write_fixture(directory)
            report = validator.build_report(directory)
            self.assertTrue(report["valid"])
            self.assertEqual(directory.name, report["root"])
            self.assertNotIn(json.dumps(str(directory.parent))[1:-1], json.dumps(report))
            self.assertEqual("artifact consistency not control effectiveness", report["scope"])
            self.assertEqual({"assets": 1, "risks": 1, "treatments": 1, "controls": 2}, report["counts"])
            self.assertTrue(report["timestamp_utc"].endswith("+00:00"))
            for item in report["inputs"]:
                self.assertEqual(hashlib.sha256((directory / item["file"]).read_bytes()).hexdigest(), item["sha256"])

    def test_missing_input_is_named(self):
        with tempfile.TemporaryDirectory(dir=TEMP_PARENT) as temporary:
            report = validator.build_report(Path(temporary))
            self.assertFalse(report["valid"])
            self.assertEqual(3, len(report["errors"]))
            self.assertEqual({"INPUT_READ_ERROR"}, {error["code"] for error in report["errors"]})
            self.assertTrue(all(item["sha256"] is None for item in report["inputs"]))
            self.assertNotIn(json.dumps(str(Path(temporary).parent))[1:-1], json.dumps(report))

    def test_malformed_duplicate_and_nonstandard_json(self):
        for content in ('{"broken":', '{"kind":"one","kind":"two"}', '{"score":NaN}', '{"score":Infinity}'):
            with self.subTest(content=content), tempfile.TemporaryDirectory(dir=TEMP_PARENT) as temporary:
                directory = Path(temporary)
                self.write_fixture(directory)
                (directory / "register.json").write_text(content, encoding="utf-8")
                report = validator.build_report(directory)
                self.assertFalse(report["valid"])
                self.assertEqual("INPUT_JSON_ERROR", report["errors"][0]["code"])
                self.assertEqual("register.json", report["errors"][0]["path"])
                self.assertIsNotNone(report["inputs"][0]["sha256"])

    def test_cli_valid_and_invalid_exit_with_saved_report(self):
        with tempfile.TemporaryDirectory(dir=TEMP_PARENT) as temporary:
            directory = Path(temporary)
            self.write_fixture(directory)
            output = directory / "evidence" / "validation.json"
            command = [sys.executable, str(SCRIPT), "--root", str(directory), "--output", str(output)]
            valid = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(0, valid.returncode, valid.stderr)
            self.assertTrue(json.loads(output.read_text(encoding="utf-8"))["valid"])
            (directory / "register.json").write_text("broken", encoding="utf-8")
            invalid = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(1, invalid.returncode)
            self.assertNotIn("Traceback", invalid.stderr)
            self.assertFalse(json.loads(output.read_text(encoding="utf-8"))["valid"])

    def test_cli_will_not_overwrite_an_input(self):
        with tempfile.TemporaryDirectory(dir=TEMP_PARENT) as temporary:
            directory = Path(temporary)
            self.write_fixture(directory)
            original = (directory / "register.json").read_bytes()
            result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(directory), "--output", str(directory / "register.json")], capture_output=True, text=True, check=False)
            self.assertEqual(2, result.returncode)
            self.assertEqual(original, (directory / "register.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
