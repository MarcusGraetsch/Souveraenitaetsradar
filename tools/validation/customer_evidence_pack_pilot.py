#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from sovradar.evidence_coverage import analyze_request_coverage  # noqa: E402
from sovradar.gate_catalog import load_evidence_requests  # noqa: E402
from sovradar.intake import load_evidence_pack  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the NEXT-101 provider-neutral Customer Evidence Pack pilot")
    parser.add_argument(
        "--pack",
        default=str(ROOT / "data/templates/evidence-pack-example"),
        help="Evidence Pack directory",
    )
    parser.add_argument(
        "--plan",
        default=str(ROOT / "data/pilots/next-101/requirement-plan.json"),
        help="Assessment-specific evidence requirement plan",
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / ".runtime/exports/next-101-evidence-pack-pilot.json"),
        help="JSON output path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pack_path = Path(args.pack).resolve()
    plan_path = Path(args.plan).resolve()
    output_path = Path(args.output).resolve()

    manifest, records = load_evidence_pack(pack_path, ROOT / "schemas")
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    requests = load_evidence_requests(ROOT / "data/method/evidence_request_catalog.csv")
    workload_id = str(plan.get("workload", {}).get("workload_id") or manifest["scope"]["workload_id"])

    result = analyze_request_coverage(
        records,
        requests,
        plan,
        workload_id=workload_id,
    )
    result["manifest"] = {
        "schema_version": manifest["schema_version"],
        "assessment_id": manifest["assessment_id"],
        "producer": manifest["producer"],
        "scope": manifest["scope"],
        "redaction_statement": manifest["redaction_statement"],
        "attachment_policy": manifest.get("attachment_policy", ""),
    }
    result["checks"] = {
        "assessment_id_matches_plan": manifest["assessment_id"] == plan.get("assessment_id"),
        "workload_scope_matches_plan": manifest["scope"]["workload_id"] == workload_id,
        "at_least_four_evidence_classes": result["summary"]["evidence_class_count"] >= 4,
        "no_scope_mismatch": result["summary"]["scope_mismatch_count"] == 0,
        "provenance_locators_complete": not result["quality_findings"]["missing_locator_evidence_ids"],
        "source_refs_complete": not result["quality_findings"]["missing_source_ref_evidence_ids"],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    checks_ok = all(result["checks"].values())
    expected_counts = {
        "verified": 3,
        "review_required": 4,
        "insufficient": 1,
        "missing": 3,
    }
    counts_ok = all(result["summary"][key] == value for key, value in expected_counts.items())

    print("NEXT-101 provider-neutral Evidence Pack pilot", "PASS" if checks_ok and counts_ok else "FAIL")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    print("Checks:", json.dumps(result["checks"], ensure_ascii=False))
    print("Expected coverage baseline:", json.dumps(expected_counts, ensure_ascii=False))
    print(f"Report: {output_path}")
    return 0 if checks_ok and counts_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
