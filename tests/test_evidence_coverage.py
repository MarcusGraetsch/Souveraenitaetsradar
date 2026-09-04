from __future__ import annotations

import json
from pathlib import Path

from sovradar.evidence_coverage import analyze_request_coverage, state_satisfies
from sovradar.gate_catalog import load_evidence_requests
from sovradar.intake import load_evidence_pack
from sovradar.models import AppliedState

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "data/templates/evidence-pack-example"
PLAN = ROOT / "data/pilots/next-101/requirement-plan.json"


def test_applied_state_sufficiency_is_explicit_not_numeric():
    assert state_satisfies(AppliedState.TESTED, AppliedState.CONFIGURED)
    assert state_satisfies(AppliedState.ATTESTED, AppliedState.TESTED)
    assert state_satisfies(AppliedState.OBSERVED, AppliedState.DOCUMENTED)
    assert not state_satisfies(AppliedState.OBSERVED, AppliedState.CONFIGURED)
    assert not state_satisfies(AppliedState.CONFIGURED, AppliedState.OBSERVED)
    assert not state_satisfies(AppliedState.AVAILABLE, AppliedState.DOCUMENTED)


def test_next_101_pack_has_explicit_request_mapping_and_four_plus_classes():
    manifest, records = load_evidence_pack(PACK, ROOT / "schemas")
    assert manifest["assessment_id"] == "SYNTH-R6A-001"
    assert len(records) == 5
    assert len({record.evidence_type for record in records}) == 5
    assert all(record.request_ids for record in records)
    assert {request_id for record in records for request_id in record.request_ids} >= {
        "ER-001",
        "ER-002",
        "ER-003",
        "ER-004",
        "ER-006",
        "ER-008",
        "ER-009",
        "ER-011",
    }


def test_next_101_coverage_baseline_exposes_verified_review_and_gaps():
    manifest, records = load_evidence_pack(PACK, ROOT / "schemas")
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    catalog = load_evidence_requests(ROOT / "data/method/evidence_request_catalog.csv")
    result = analyze_request_coverage(
        records,
        catalog,
        plan,
        workload_id=manifest["scope"]["workload_id"],
    )

    assert result["summary"] == {
        "evidence_count": 5,
        "evidence_classes": [
            "architecture",
            "contractual",
            "provider_export",
            "public_provider",
            "test_report",
        ],
        "evidence_class_count": 5,
        "required_request_count": 11,
        "verified": 3,
        "review_required": 4,
        "insufficient": 1,
        "missing": 3,
        "min_effective_trust": 2,
        "max_effective_trust": 4,
        "scope_mismatch_count": 0,
    }

    coverage = {item["request_id"]: item for item in result["request_coverage"]}
    assert coverage["ER-001"]["status"] == "VERIFIED"
    assert coverage["ER-002"]["status"] == "VERIFIED"
    assert coverage["ER-006"]["status"] == "VERIFIED"
    assert coverage["ER-003"]["status"] == "REVIEW_REQUIRED"
    assert coverage["ER-004"]["status"] == "REVIEW_REQUIRED"
    assert coverage["ER-009"]["status"] == "REVIEW_REQUIRED"
    assert coverage["ER-011"]["status"] == "REVIEW_REQUIRED"
    assert coverage["ER-008"]["status"] == "INSUFFICIENT"
    assert coverage["ER-005"]["status"] == "MISSING"
    assert coverage["ER-007"]["status"] == "MISSING"
    assert coverage["ER-012"]["status"] == "MISSING"

    assert len(result["gaps"]) == 8
    assert result["quality_findings"]["scope_mismatch_evidence_ids"] == []
    assert result["quality_findings"]["missing_locator_evidence_ids"] == []
    assert result["quality_findings"]["missing_source_ref_evidence_ids"] == []


def test_public_provider_evidence_does_not_satisfy_configured_requirement():
    manifest, records = load_evidence_pack(PACK, ROOT / "schemas")
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    catalog = load_evidence_requests(ROOT / "data/method/evidence_request_catalog.csv")
    result = analyze_request_coverage(records, catalog, plan, workload_id=manifest["scope"]["workload_id"])
    er003 = next(item for item in result["request_coverage"] if item["request_id"] == "ER-003")
    public = next(item for item in er003["candidates"] if item["evidence_id"] == "EV-005")
    assert public["applied_state"] == "available"
    assert public["sufficient"] is False
    assert any("does not satisfy required configured" in reason for reason in public["deficiencies"])
