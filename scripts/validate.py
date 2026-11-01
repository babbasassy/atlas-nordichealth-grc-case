#!/usr/bin/env python3
"""Check fictional case artifacts for consistency, never control effectiveness.

Uses only the Python standard library. Run with --help for CLI options.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import sys


INPUT_NAMES = ("register.json", "treatments.json", "controls.json")
SCOPE = "artifact consistency not control effectiveness"


def score_band(score: int) -> str:
    """Return the exercise band; booleans are not numeric ratings."""
    if type(score) is not int or not 1 <= score <= 25:
        raise ValueError("score must be an integer from 1 through 25")
    for upper, band in ((4, "low"), (9, "moderate"), (16, "high"), (25, "critical")):
        if score <= upper:
            return band
    raise AssertionError("unreachable")


class Checker:
    def __init__(self) -> None:
        self.errors: list[dict[str, str]] = []

    def error(self, code: str, path: str, message: str) -> None:
        self.errors.append({"code": code, "path": path, "message": message})

    def exact(self, row: dict, key: str, expected: object, path: str) -> None:
        if key not in row or type(row[key]) is not type(expected) or row[key] != expected:
            self.error("REQUIRED_VALUE", f"{path}.{key}", f"Must be {expected!r} for this proposed fictional case.")

    def text(self, row: dict, key: str, path: str) -> None:
        value = row.get(key)
        if not isinstance(value, str) or not value.strip():
            self.error("REQUIRED_TEXT", f"{path}.{key}", "Must be a nonempty string.")

    def strings(self, row: dict, key: str, path: str, *, nonempty: bool = True) -> list[str]:
        value = row.get(key)
        location = f"{path}.{key}"
        if not isinstance(value, list):
            self.error("STRING_LIST", location, "Must be a list of nonempty strings.")
            return []
        if nonempty and not value:
            self.error("EMPTY_LIST", location, "At least one entry is required.")
        result = []
        for index, item in enumerate(value):
            if not isinstance(item, str) or not item.strip():
                self.error("STRING_LIST", f"{location}[{index}]", "Must be a nonempty string.")
            elif item in result:
                self.error("DUPLICATE_REFERENCE", f"{location}[{index}]", f"Duplicate value {item!r}.")
            else:
                result.append(item)
        return result

    def integer(self, row: dict, key: str, path: str, minimum: int, maximum: int | None = None) -> bool:
        value = row.get(key)
        if type(value) is not int or value < minimum or (maximum is not None and value > maximum):
            bound = f"{minimum} through {maximum}" if maximum is not None else f"at least {minimum}"
            self.error("INTEGER_RANGE", f"{path}.{key}", f"Must be an integer {bound}; booleans are invalid.")
            return False
        return True

    def document(self, value: object, filename: str, kind: str) -> dict:
        if not isinstance(value, dict):
            self.error("DOCUMENT_OBJECT", filename, "Top level must be a JSON object.")
            return {}
        self.exact(value, "kind", kind, filename)
        return value

    def records(self, document: dict, key: str, filename: str) -> dict[str, tuple[dict, str]]:
        rows = document.get(key)
        path = f"{filename}.{key}"
        if not isinstance(rows, list):
            self.error("RECORD_LIST", path, "Must be a list of objects.")
            return {}
        if not rows:
            self.error("EMPTY_LIST", path, "At least one record is required.")
        indexed = {}
        for index, row in enumerate(rows):
            location = f"{path}[{index}]"
            if not isinstance(row, dict):
                self.error("RECORD_OBJECT", location, "Record must be a JSON object.")
                continue
            self.text(row, "id", location)
            identifier = row.get("id")
            if not isinstance(identifier, str) or not identifier.strip():
                continue
            if identifier in indexed:
                self.error("DUPLICATE_ID", f"{location}.id", f"Duplicate identifier {identifier!r}.")
                continue
            indexed[identifier] = (row, location)
        return indexed


def validate_documents(register: object, treatments: object, controls: object) -> list[dict[str, str]]:
    """Validate parsed JSON values without changing them or accessing files."""
    check = Checker()
    register = check.document(register, "register.json", "fictional_risk_assessment")
    treatments = check.document(treatments, "treatments.json", "fictional_proposed_treatments")
    controls = check.document(controls, "controls.json", "fictional_proposed_controls")
    check.exact(controls, "coverage", "illustrative_subset_not_full_iso_annex_a", "controls.json")
    assessment_date = register.get("assessment_date")
    try:
        if not isinstance(assessment_date, str) or date.fromisoformat(assessment_date).isoformat() != assessment_date:
            raise ValueError("not an ISO calendar date")
    except ValueError:
        check.error("ASSESSMENT_DATE", "register.json.assessment_date", "Must be a valid YYYY-MM-DD calendar date.")

    assets = check.records(register, "assets", "register.json")
    risks = check.records(register, "risks", "register.json")
    plans = check.records(treatments, "treatments", "treatments.json")
    safeguards = check.records(controls, "controls", "controls.json")
    risk_links = {}
    plan_links = {}
    control_links = {}

    for asset, path in assets.values():
        for key in ("name", "owner_role"):
            check.text(asset, key, path)
        check.strings(asset, "data_categories", path)

    for identifier, (risk, path) in risks.items():
        for key in ("owner_role", "scenario", "rationale", "treatment_id"):
            check.text(risk, key, path)
        asset_ids = check.strings(risk, "asset_ids", path)
        control_ids = check.strings(risk, "control_ids", path)
        risk_links[identifier] = control_ids
        for asset_id in asset_ids:
            if asset_id not in assets:
                check.error("UNKNOWN_ASSET", f"{path}.asset_ids", f"Asset {asset_id!r} does not exist.")
        valid_likelihood = check.integer(risk, "likelihood", path, 1, 5)
        valid_impact = check.integer(risk, "impact", path, 1, 5)
        valid_score = check.integer(risk, "score", path, 1, 25)
        if valid_likelihood and valid_impact:
            expected_score = risk["likelihood"] * risk["impact"]
            if valid_score and risk["score"] != expected_score:
                check.error("SCORE_MISMATCH", f"{path}.score", f"Expected likelihood x impact = {expected_score}.")
            expected_band = score_band(expected_score)
            if risk.get("band") != expected_band:
                check.error("BAND_MISMATCH", f"{path}.band", f"Expected {expected_band!r} from the recalculated score.")
            escalation = risk["impact"] == 5 or expected_score >= 17
            if type(risk.get("escalation_required")) is not bool or risk["escalation_required"] != escalation:
                check.error("ESCALATION_MISMATCH", f"{path}.escalation_required", f"An explicit boolean {escalation!r} is required: impact 5 or a critical score requires escalation.")
        elif risk.get("band") not in ("low", "moderate", "high", "critical"):
            check.error("BAND_VALUE", f"{path}.band", "Must be low, moderate, high or critical.")
        check.exact(risk, "acceptance", "pending", path)
        check.exact(risk, "actual_residual", None, path)

    for identifier, (plan, path) in plans.items():
        for key in ("risk_id", "action"):
            check.text(plan, key, path)
        plan_links[identifier] = check.strings(plan, "control_ids", path)
        check.strings(plan, "required_evidence", path)
        check.integer(plan, "review_window_days", path, 1)
        check.exact(plan, "status", "proposed", path)
        check.exact(plan, "implementation_evidence", [], path)
        check.exact(plan, "approval", "pending", path)

    for identifier, (control, path) in safeguards.items():
        for key in ("name", "reason"):
            check.text(control, key, path)
        applicable = control.get("applicable")
        if type(applicable) is not bool:
            check.error("BOOLEAN_REQUIRED", f"{path}.applicable", "Must be true or false.")
        control_links[identifier] = check.strings(control, "risk_ids", path, nonempty=applicable is True)
        check.strings(control, "nsm_principles", path, nonempty=applicable is True)
        if applicable is True:
            check.exact(control, "status", "proposed", path)
            check.exact(control, "evidence_status", "not_implemented", path)
        elif applicable is False:
            check.exact(control, "risk_ids", [], path)
            check.exact(control, "status", "not_applicable", path)
            check.exact(control, "evidence_status", "not_applicable", path)

    # Check every direction independently so an orphan cannot hide behind a valid link.
    for identifier, (risk, path) in risks.items():
        treatment_id = risk.get("treatment_id")
        if not isinstance(treatment_id, str) or treatment_id not in plans:
            check.error("UNKNOWN_TREATMENT", f"{path}.treatment_id", "Referenced treatment does not exist.")
        else:
            plan = plans[treatment_id][0]
            if plan.get("risk_id") != identifier:
                check.error("TREATMENT_RECIPROCITY", f"{path}.treatment_id", "Treatment must point back to this risk.")
            if set(risk_links[identifier]) != set(plan_links[treatment_id]):
                check.error("TREATMENT_CONTROL_MISMATCH", f"{path}.control_ids", "Risk and its treatment must reference the same controls.")
        for control_id in risk_links[identifier]:
            if control_id not in safeguards:
                check.error("UNKNOWN_CONTROL", f"{path}.control_ids", f"Control {control_id!r} does not exist.")
            elif identifier not in control_links[control_id]:
                check.error("CONTROL_RECIPROCITY", f"{path}.control_ids", f"Control {control_id!r} must point back to this risk.")
            elif safeguards[control_id][0].get("applicable") is not True:
                check.error("EXCLUDED_CONTROL_REFERENCE", f"{path}.control_ids", f"Control {control_id!r} is not applicable.")

    for identifier, (plan, path) in plans.items():
        risk_id = plan.get("risk_id")
        if not isinstance(risk_id, str) or risk_id not in risks:
            check.error("UNKNOWN_RISK", f"{path}.risk_id", "Referenced risk does not exist.")
        elif risks[risk_id][0].get("treatment_id") != identifier:
            check.error("TREATMENT_RECIPROCITY", f"{path}.risk_id", "Risk must point back to this treatment.")
        for control_id in plan_links[identifier]:
            if control_id not in safeguards:
                check.error("UNKNOWN_CONTROL", f"{path}.control_ids", f"Control {control_id!r} does not exist.")
            elif not isinstance(risk_id, str) or risk_id not in control_links[control_id]:
                check.error("CONTROL_RECIPROCITY", f"{path}.control_ids", f"Control {control_id!r} must reference this treatment's risk.")

    for identifier, (_, path) in safeguards.items():
        for risk_id in control_links[identifier]:
            if risk_id not in risks:
                check.error("UNKNOWN_RISK", f"{path}.risk_ids", f"Risk {risk_id!r} does not exist.")
            elif identifier not in risk_links[risk_id]:
                check.error("CONTROL_RECIPROCITY", f"{path}.risk_ids", f"Risk {risk_id!r} must point back to this control.")
    return check.errors


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON property {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"Nonstandard JSON constant {value!r}")


def build_report(root: Path) -> dict:
    """Hash original bytes and report missing, unreadable or malformed inputs."""
    documents = {}
    inputs = []
    errors = []
    for name in INPUT_NAMES:
        record = {"file": name, "sha256": None}
        inputs.append(record)
        try:
            raw = (root / name).read_bytes()
            record["sha256"] = hashlib.sha256(raw).hexdigest()
            documents[name] = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=_unique_object, parse_constant=_reject_constant)
        except OSError as exc:
            errors.append({"code": "INPUT_READ_ERROR", "path": name, "message": exc.strerror or "Unable to read input file."})
        except (UnicodeError, ValueError, RecursionError) as exc:
            errors.append({"code": "INPUT_JSON_ERROR", "path": name, "message": str(exc)})
    if len(documents) == len(INPUT_NAMES):
        errors.extend(validate_documents(*(documents[name] for name in INPUT_NAMES)))
    counts = {}
    for filename, key in (("register.json", "assets"), ("register.json", "risks"), ("treatments.json", "treatments"), ("controls.json", "controls")):
        document = documents.get(filename)
        rows = document.get(key) if isinstance(document, dict) else None
        counts[key] = len(rows) if isinstance(rows, list) else None
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scope": SCOPE,
        "root": root.resolve().name,
        "inputs": inputs,
        "counts": counts,
        "valid": not errors,
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Folder containing register.json, treatments.json and controls.json.")
    parser.add_argument("--output", type=Path, help="Optional JSON report path (also printed to stdout).")
    args = parser.parse_args(argv)
    report = build_report(args.root)
    rendered = json.dumps(report, indent=2, ensure_ascii=True) + "\n"
    if args.output:
        if args.output.resolve() in {(args.root / name).resolve() for name in INPUT_NAMES}:
            print("OUTPUT_PATH_ERROR: report must not overwrite an input file.", file=sys.stderr)
            return 2
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        except OSError as exc:
            print(f"OUTPUT_WRITE_ERROR: {exc}", file=sys.stderr)
            return 2
    print(rendered, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
