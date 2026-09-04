from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

from jsonschema import Draft202012Validator
from sqlalchemy import delete

from apps.api.app.database import SessionLocal
from apps.api.app.models import LlmProposalReview
from apps.api.tests.test_api import client, reset_db

REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = REPO_ROOT / "schemas" / "assessment-export.schema.json"
RAW_SENTINEL = "RAW-EVIDENCE-SECRET-SENTINEL"
EXCERPT_SENTINEL = "EXCERPT-SECRET-SENTINEL"


def _reset() -> None:
    with SessionLocal() as db:
        db.execute(delete(LlmProposalReview))
        db.commit()
    reset_db()


def _create_export_fixture() -> tuple[str, str, dict[str, str]]:
    assessment = client.post(
        "/api/assessments",
        json={
            "name": "NEXT-113 Export Pilot",
            "customer": "Synthetic Customer",
            "workload_type": "ai-agent",
            "criticality": "high",
            "confidentiality": "high",
            "integrity": "high",
            "availability": "medium",
            "regulatory_context": "synthetic test",
        },
    ).json()
    assessment_id = assessment["id"]

    evidence_response = client.post(
        f"/api/assessments/{assessment_id}/evidence",
        data={
            "title": "Synthetic contract evidence",
            "evidence_type": "contract",
            "description": "Synthetic evidence for export/restore tests.",
            "source": "NEXT-113 fixture",
            "source_date": "2026-09-03",
            "content_excerpt": EXCERPT_SENTINEL,
        },
        files={"file": ("sensitive.txt", RAW_SENTINEL.encode("utf-8"), "text/plain")},
    )
    assert evidence_response.status_code == 201
    evidence = evidence_response.json()
    evidence_id = evidence["id"]

    reviewed = client.put(
        f"/api/assessments/{assessment_id}/evidence/{evidence_id}/review",
        json={
            "applied_state": "documented",
            "base_trust": 4,
            "scope_fit": 4,
            "freshness_fit": 4,
            "review_status": "reviewed",
        },
    )
    assert reviewed.status_code == 200

    llm_import = client.post(
        f"/api/assessments/{assessment_id}/llm-bridge/import",
        json={
            "assessment_id": assessment_id,
            "proposals": [
                {
                    "question_id": "DK-03",
                    "proposed_answer": "Provider",
                    "rationale": "Synthetic proposal for export/restore audit.",
                    "evidence_ids": [evidence_id],
                    "confidence": 0.72,
                }
            ],
            "evidence_gaps": [],
            "warnings": [],
        },
    )
    assert llm_import.status_code == 200, llm_import.text
    llm_import_id = llm_import.json()["id"]
    llm_review = client.post(
        f"/api/assessments/{assessment_id}/llm-bridge/imports/{llm_import_id}/proposals/0/review",
        json={
            "decision": "accepted",
            "reviewer_note": "Synthetic consultant accepted the answer proposal.",
        },
    )
    assert llm_review.status_code == 201, llm_review.text

    requirement_plan = {
        "HG-01": 2,
        "HG-02": 0,
        "HG-03": 3,
        "HG-04": 3,
        "HG-05": 0,
        "HG-06": 0,
        "HG-07": 0,
        "HG-08": 0,
    }
    current_requirements = {
        item["gate_id"]: item
        for item in client.get(f"/api/assessments/{assessment_id}/gate-requirements").json()
    }
    for gate_id, level in requirement_plan.items():
        if current_requirements[gate_id]["requirement_level"] == level:
            continue
        response = client.put(
            f"/api/assessments/{assessment_id}/gate-requirements/{gate_id}",
            json={
                "requirement_level": level,
                "reason": "Synthetic export/restore fixture requirement plan.",
            },
        )
        assert response.status_code == 200, response.text
        assert response.json()["is_override"] is True

    claims = [
        {
            "gate_id": "HG-01",
            "statement": "Synthetic reviewed capability 3 for jurisdiction/control.",
            "review_status": "reviewed",
            "capability_level": 3,
            "evidence_ids": [evidence_id],
            "question_ids": [],
            "notes": "Expected PASS",
        },
        {
            "gate_id": "HG-03",
            "statement": "Synthetic reviewed capability 1 for key control.",
            "review_status": "reviewed",
            "capability_level": 1,
            "evidence_ids": [evidence_id],
            "question_ids": [],
            "notes": "Expected FAIL",
        },
        {
            "gate_id": "HG-04",
            "statement": "Synthetic capability 3 for exit without reviewed evidence.",
            "review_status": "reviewed",
            "capability_level": 3,
            "evidence_ids": [],
            "question_ids": [],
            "notes": "Expected UNVERIFIED",
        },
    ]
    for payload in claims:
        response = client.post(f"/api/assessments/{assessment_id}/claims", json=payload)
        assert response.status_code == 201

    state_map = {
        item["gate_id"]: item["final_state"]
        for item in client.get(f"/api/assessments/{assessment_id}/gates").json()
    }
    assert state_map["HG-01"] == "PASS"
    assert state_map["HG-03"] == "FAIL"
    assert state_map["HG-04"] == "UNVERIFIED"
    return assessment_id, evidence_id, state_map


def _zip_files(data: bytes) -> dict[str, bytes]:
    with zipfile.ZipFile(io.BytesIO(data), "r") as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def test_structured_export_validates_and_omits_sensitive_evidence_by_default():
    _reset()
    with client:
        assessment_id, _, before = _create_export_fixture()
        response = client.get(f"/api/assessments/{assessment_id}/export")
        assert response.status_code == 200
        payload = response.json()

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(payload)
        assert payload["export_meta"]["schema_name"] == "sovradar.assessment-export"
        assert payload["export_meta"]["schema_version"] == "1.0"
        assert payload["export_meta"]["includes_raw_evidence_files"] is False
        assert payload["export_meta"]["includes_sensitive_evidence_fields"] is False
        assert payload["evidence"][0]["has_file"] is True
        assert payload["evidence"][0]["has_content_excerpt"] is True
        assert "content_excerpt" not in payload["evidence"][0]
        assert len(payload["llm_proposal_reviews"]) == 1
        assert payload["gate_requirement_changes"]
        assert all(item["reason"] for item in payload["gate_requirement_changes"])
        review = payload["llm_proposal_reviews"][0]
        assert review["decision"] == "accepted"
        assert review["question_id"] == "DK-03"
        assert review["evidence_ids"] == [payload["evidence"][0]["id"]]
        assert review["answer_id"] in {item["id"] for item in payload["answers"]}
        serialized = json.dumps(payload, ensure_ascii=False)
        assert EXCERPT_SENTINEL not in serialized
        assert RAW_SENTINEL not in serialized

        after = {
            item["gate_id"]: item["final_state"]
            for item in client.get(f"/api/assessments/{assessment_id}/gates").json()
        }
        assert after == before


def test_consultant_report_does_not_embed_sensitive_evidence_content():
    _reset()
    with client:
        assessment_id, _, before = _create_export_fixture()
        response = client.get(f"/api/assessments/{assessment_id}/report")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/markdown")
        report = response.text
        assert "# Souveränitäts-Radar – Consultant Report" in report
        assert "HG-01" in report and "HG-03" in report and "HG-04" in report
        assert "keine automatische Risikoakzeptanz" in report
        assert "Human-geprüfte LLM-Antwortvorschläge: **1**" in report
        assert "Mindeststufen-Audit" in report
        assert "Begründung:" in report
        assert EXCERPT_SENTINEL not in report
        assert RAW_SENTINEL not in report
        after = {
            item["gate_id"]: item["final_state"]
            for item in client.get(f"/api/assessments/{assessment_id}/gates").json()
        }
        assert after == before


def test_structured_backup_excludes_raw_files_and_full_backup_requires_opt_in():
    _reset()
    with client:
        assessment_id, evidence_id, _ = _create_export_fixture()

        structured = client.get(f"/api/assessments/{assessment_id}/backup")
        assert structured.status_code == 200
        assert structured.headers["x-sovradar-includes-evidence"] == "false"
        structured_files = _zip_files(structured.content)
        assert {"assessment.json", "consultant-report.md", "manifest.json"}.issubset(structured_files)
        assert not any(name.startswith("evidence/") for name in structured_files)
        structured_payload = json.loads(structured_files["assessment.json"].decode("utf-8"))
        assert len(structured_payload["llm_proposal_reviews"]) == 1
        assert structured_payload["gate_requirement_changes"]
        assert EXCERPT_SENTINEL not in structured_files["assessment.json"].decode("utf-8")
        assert RAW_SENTINEL.encode("utf-8") not in b"".join(structured_files.values())

        full = client.get(f"/api/assessments/{assessment_id}/backup?include_evidence=true")
        assert full.status_code == 200
        assert full.headers["x-sovradar-includes-evidence"] == "true"
        full_files = _zip_files(full.content)
        evidence_paths = [name for name in full_files if name.startswith(f"evidence/{evidence_id}/")]
        assert len(evidence_paths) == 1
        assert full_files[evidence_paths[0]] == RAW_SENTINEL.encode("utf-8")
        assert EXCERPT_SENTINEL in full_files["assessment.json"].decode("utf-8")
        assert EXCERPT_SENTINEL not in full_files["consultant-report.md"].decode("utf-8")


def test_structured_restore_remaps_ids_and_preserves_gate_semantics_without_raw_files():
    _reset()
    with client:
        assessment_id, evidence_id, before = _create_export_fixture()
        payload = client.get(f"/api/assessments/{assessment_id}/export").json()
        source_review = payload["llm_proposal_reviews"][0]
        source_requirement_changes = payload["gate_requirement_changes"]

        restored = client.post("/api/assessments/import", json=payload)
        assert restored.status_code == 201, restored.text
        result = restored.json()
        assert result["assessment_id"] != assessment_id
        assert result["evidence_id_map"][evidence_id] != evidence_id
        assert result["restored_llm_proposal_review_count"] == 1
        assert result["restored_gate_requirement_change_count"] == len(source_requirement_changes)
        assert result["gate_semantic_drift"] is False
        assert evidence_id in result["missing_raw_file_source_evidence_ids"]
        assert all(item["matches"] for item in result["gate_comparison"])

        restored_id = result["assessment_id"]
        assessments = client.get("/api/assessments").json()
        assessment_ids = {item["id"] for item in assessments}
        assert assessment_id in assessment_ids
        assert restored_id in assessment_ids
        assert len(assessment_ids) == 2

        restored_reviews = client.get(
            f"/api/assessments/{restored_id}/llm-bridge/proposal-reviews"
        ).json()
        assert len(restored_reviews) == 1
        restored_review = restored_reviews[0]
        assert restored_review["decision"] == source_review["decision"]
        assert restored_review["question_id"] == source_review["question_id"]
        assert restored_review["final_answer_value"] == source_review["final_answer_value"]
        assert restored_review["reviewer_note"] == source_review["reviewer_note"]
        assert restored_review["evidence_ids"] == [result["evidence_id_map"][evidence_id]]
        assert restored_review["llm_import_id"] == result["llm_import_id_map"][source_review["llm_import_id"]]
        assert restored_review["answer_id"] == result["answer_id_map"][source_review["answer_id"]]

        restored_requirement_changes = client.get(
            f"/api/assessments/{restored_id}/gate-requirement-changes"
        ).json()
        assert len(restored_requirement_changes) == len(source_requirement_changes)
        assert [item["change_type"] for item in restored_requirement_changes] == [item["change_type"] for item in source_requirement_changes]
        assert [item["reason"] for item in restored_requirement_changes] == [item["reason"] for item in source_requirement_changes]
        assert [(item["previous_level"], item["new_level"]) for item in restored_requirement_changes] == [
            (item["previous_level"], item["new_level"]) for item in source_requirement_changes
        ]

        restored_states = {
            item["gate_id"]: item["final_state"]
            for item in client.get(f"/api/assessments/{restored_id}/gates").json()
        }
        assert restored_states == before
        restored_export = client.get(f"/api/assessments/{restored_id}/export").json()
        assert restored_export["evidence"][0]["has_file"] is False
        assert len(restored_export["llm_proposal_reviews"]) == 1
        assert len(restored_export["gate_requirement_changes"]) == len(source_requirement_changes)
        assert restored_export["warnings"]


def test_restore_accepts_legacy_v1_export_without_optional_audit_fields():
    _reset()
    with client:
        assessment_id, _, _ = _create_export_fixture()
        payload = client.get(f"/api/assessments/{assessment_id}/export").json()
        payload.pop("llm_proposal_reviews")
        payload.pop("gate_requirement_changes")

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(payload)
        restored = client.post("/api/assessments/import", json=payload)
        assert restored.status_code == 201, restored.text
        result = restored.json()
        assert result["restored_llm_proposal_review_count"] == 0
        assert result["restored_gate_requirement_change_count"] == 0
        reviews = client.get(
            f"/api/assessments/{result['assessment_id']}/llm-bridge/proposal-reviews"
        ).json()
        assert reviews == []
        requirement_changes = client.get(
            f"/api/assessments/{result['assessment_id']}/gate-requirement-changes"
        ).json()
        assert requirement_changes == []


def test_full_backup_restore_recovers_raw_evidence_and_preserves_gate_semantics():
    _reset()
    with client:
        assessment_id, _, before = _create_export_fixture()
        source_export = client.get(f"/api/assessments/{assessment_id}/export").json()
        source_requirement_change_count = len(source_export["gate_requirement_changes"])
        backup = client.get(f"/api/assessments/{assessment_id}/backup?include_evidence=true")
        assert backup.status_code == 200

        restored = client.post(
            "/api/assessments/import-backup",
            files={"file": ("backup.zip", backup.content, "application/zip")},
        )
        assert restored.status_code == 201
        result = restored.json()
        assert result["gate_semantic_drift"] is False
        assert result["restored_llm_proposal_review_count"] == 1
        assert result["restored_gate_requirement_change_count"] == source_requirement_change_count
        assert len(result["restored_raw_evidence_ids"]) == 1
        assert result["missing_raw_file_source_evidence_ids"] == []

        restored_id = result["assessment_id"]
        restored_states = {
            item["gate_id"]: item["final_state"]
            for item in client.get(f"/api/assessments/{restored_id}/gates").json()
        }
        assert restored_states == before
        restored_reviews = client.get(
            f"/api/assessments/{restored_id}/llm-bridge/proposal-reviews"
        ).json()
        assert len(restored_reviews) == 1
        restored_requirement_changes = client.get(
            f"/api/assessments/{restored_id}/gate-requirement-changes"
        ).json()
        assert len(restored_requirement_changes) == source_requirement_change_count
        restored_export = client.get(f"/api/assessments/{restored_id}/export").json()
        assert restored_export["evidence"][0]["has_file"] is True
        assert len(restored_export["llm_proposal_reviews"]) == 1
        assert len(restored_export["gate_requirement_changes"]) == source_requirement_change_count
        assert restored_export["warnings"] == []
