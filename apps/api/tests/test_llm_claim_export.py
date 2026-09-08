from __future__ import annotations

from apps.api.tests.test_llm_claim_review import (
    _assessment,
    _claim_result,
    _gate_state,
    _reset,
    _reviewed_evidence,
    client,
)


def _accepted_finding_fixture() -> tuple[str, str, dict, dict]:
    assessment = _assessment("Claim Export Pilot")
    assessment_id = assessment["id"]
    evidence = _reviewed_evidence(assessment_id)
    imported = client.post(
        f"/api/assessments/{assessment_id}/llm-bridge/claim-import",
        json=_claim_result(assessment_id, evidence["id"]),
    ).json()
    review_response = client.post(
        f"/api/assessments/{assessment_id}/llm-bridge/claim-imports/{imported['id']}/proposals/0/review",
        json={"decision": "accepted", "reviewer_note": "export roundtrip"},
    )
    assert review_response.status_code == 201, review_response.text
    return assessment_id, evidence["id"], imported, review_response.json()


def test_export_restore_preserves_finding_import_review_claim_links_and_gate_semantics():
    _reset()
    with client:
        assessment_id, evidence_id, imported, review = _accepted_finding_fixture()
        assert _gate_state(assessment_id, "HG-04") == "PASS"

        payload = client.get(f"/api/assessments/{assessment_id}/export").json()
        assert len(payload["llm_claim_imports"]) == 1
        assert len(payload["llm_claim_proposal_reviews"]) == 1
        source_import = payload["llm_claim_imports"][0]
        source_review = payload["llm_claim_proposal_reviews"][0]
        assert source_import["id"] == imported["id"]
        assert source_import["prompt_version"] == "claim-proposals-v1"
        assert source_import["proposals"][0]["evidence_ids"] == [evidence_id]
        assert source_review["claim_id"] == review["claim_id"]
        assert source_review["decision"] == "accepted"

        restored = client.post("/api/assessments/import", json=payload)
        assert restored.status_code == 201, restored.text
        result = restored.json()
        restored_id = result["assessment_id"]
        assert result["gate_semantic_drift"] is False
        assert result["restored_llm_claim_proposal_review_count"] == 1
        assert result["llm_claim_import_id_map"][imported["id"]] != imported["id"]
        assert result["claim_id_map"][review["claim_id"]] != review["claim_id"]
        assert _gate_state(restored_id, "HG-04") == "PASS"

        restored_imports = client.get(
            f"/api/assessments/{restored_id}/llm-bridge/claim-imports"
        ).json()
        restored_reviews = client.get(
            f"/api/assessments/{restored_id}/llm-bridge/claim-proposal-reviews"
        ).json()
        assert len(restored_imports) == 1
        assert len(restored_reviews) == 1
        restored_import = restored_imports[0]
        restored_review = restored_reviews[0]
        assert restored_import["id"] == result["llm_claim_import_id_map"][imported["id"]]
        assert restored_import["assessment_id"] == restored_id
        assert restored_import["proposals"][0]["evidence_ids"] == [result["evidence_id_map"][evidence_id]]
        assert restored_review["llm_claim_import_id"] == restored_import["id"]
        assert restored_review["claim_id"] == result["claim_id_map"][review["claim_id"]]
        assert restored_review["evidence_ids"] == [result["evidence_id_map"][evidence_id]]

        restored_export = client.get(f"/api/assessments/{restored_id}/export").json()
        assert len(restored_export["llm_claim_imports"]) == 1
        assert len(restored_export["llm_claim_proposal_reviews"]) == 1


def test_legacy_v1_export_without_finding_audit_fields_still_restores():
    _reset()
    with client:
        assessment_id, _, _, _ = _accepted_finding_fixture()
        payload = client.get(f"/api/assessments/{assessment_id}/export").json()
        payload.pop("llm_claim_imports")
        payload.pop("llm_claim_proposal_reviews")

        restored = client.post("/api/assessments/import", json=payload)
        assert restored.status_code == 201, restored.text
        result = restored.json()
        assert result["restored_llm_claim_proposal_review_count"] == 0
        restored_id = result["assessment_id"]
        assert client.get(
            f"/api/assessments/{restored_id}/llm-bridge/claim-imports"
        ).json() == []
        assert client.get(
            f"/api/assessments/{restored_id}/llm-bridge/claim-proposal-reviews"
        ).json() == []
