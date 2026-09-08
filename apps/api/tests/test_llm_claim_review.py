from __future__ import annotations

from sqlalchemy import delete

from apps.api.app.database import SessionLocal
from apps.api.app.models import LlmClaimImport, LlmClaimProposalReview
from apps.api.tests.test_api import client, reset_db


def _reset() -> None:
    with SessionLocal() as db:
        db.execute(delete(LlmClaimProposalReview))
        db.execute(delete(LlmClaimImport))
        db.commit()
    reset_db()


def _assessment(name: str = "Claim Proposal Pilot") -> dict:
    return client.post(
        "/api/assessments",
        json={"name": name, "criticality": "medium", "workload_type": "ai-agent"},
    ).json()


def _reviewed_evidence(assessment_id: str, *, reviewed: bool = True) -> dict:
    evidence = client.post(
        f"/api/assessments/{assessment_id}/evidence",
        data={
            "title": "Synthetischer Exit-Nachweis",
            "evidence_type": "test",
            "description": "INTERNAL-DESCRIPTION-MUST-NOT-BE-IN-PROMPT",
            "content_excerpt": "APPROVED-EXCERPT: Exit wurde Ende-zu-Ende getestet.",
        },
    ).json()
    if reviewed:
        response = client.put(
            f"/api/assessments/{assessment_id}/evidence/{evidence['id']}/review",
            json={
                "applied_state": "tested",
                "base_trust": 4,
                "scope_fit": 4,
                "freshness_fit": 4,
                "review_status": "reviewed",
            },
        )
        assert response.status_code == 200
    return evidence


def _claim_result(assessment_id: str, evidence_id: str, *, statement: str = "Exit wurde Ende-zu-Ende getestet.") -> dict:
    return {
        "assessment_id": assessment_id,
        "prompt_version": "claim-proposals-v1",
        "method_version": "1.0",
        "proposals": [
            {
                "gate_id": "HG-04",
                "statement": statement,
                "capability_level": 2,
                "evidence_ids": [evidence_id],
                "question_ids": ["DK-03"],
                "rationale": "Der freigegebene Testauszug trägt die Feststellung.",
                "confidence": 0.8,
            }
        ],
        "evidence_gaps": [],
        "warnings": [],
    }


def _gate_state(assessment_id: str, gate_id: str) -> str:
    return next(
        item["final_state"]
        for item in client.get(f"/api/assessments/{assessment_id}/gates").json()
        if item["gate_id"] == gate_id
    )


def test_claim_prompt_uses_opaque_id_method_levels_and_only_approved_excerpt():
    _reset()
    with client:
        assessment = _assessment()
        evidence = _reviewed_evidence(assessment["id"])
        answer = client.put(
            f"/api/assessments/{assessment['id']}/answers/DK-03",
            json={
                "question_id": "DK-03",
                "answer_value": "synthetischer Kontext",
                "comment": "human reviewed",
                "review_state": "reviewed",
            },
        )
        assert answer.status_code == 200

        response = client.get(f"/api/assessments/{assessment['id']}/llm-bridge/claim-prompt")
        assert response.status_code == 200
        payload = response.json()
        assert payload["prompt_version"] == "claim-proposals-v1"
        assert payload["method_version"] == "1.0"
        prompt = payload["prompt"]
        assert assessment["id"] in prompt
        assert evidence["id"] in prompt
        assert "OPAQUE IDENTIFIERS" in prompt
        assert "APPROVED-EXCERPT" in prompt
        assert "INTERNAL-DESCRIPTION-MUST-NOT-BE-IN-PROMPT" not in prompt
        assert "Gate-ID: HG-04" in prompt
        assert "Stufe 2: 2" in prompt
        assert "Setze niemals PASS, FAIL" in prompt


def test_import_alone_does_not_create_claim_or_change_gate():
    _reset()
    with client:
        assessment = _assessment()
        evidence = _reviewed_evidence(assessment["id"])
        before_claims = client.get(f"/api/assessments/{assessment['id']}/claims").json()
        before_gate = _gate_state(assessment["id"], "HG-04")

        imported = client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-import",
            json=_claim_result(assessment["id"], evidence["id"]),
        )
        assert imported.status_code == 200, imported.text
        assert imported.json()["proposals"][0]["gate_id"] == "HG-04"
        assert client.get(f"/api/assessments/{assessment['id']}/claims").json() == before_claims
        assert _gate_state(assessment["id"], "HG-04") == before_gate == "UNVERIFIED"


def test_accept_creates_reviewed_claim_and_only_then_changes_deterministic_gate():
    _reset()
    with client:
        assessment = _assessment()
        evidence = _reviewed_evidence(assessment["id"])
        imported = client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-import",
            json=_claim_result(assessment["id"], evidence["id"]),
        ).json()
        assert _gate_state(assessment["id"], "HG-04") == "UNVERIFIED"

        reviewed = client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-imports/{imported['id']}/proposals/0/review",
            json={"decision": "accepted", "reviewer_note": "synthetic human confirmation"},
        )
        assert reviewed.status_code == 201, reviewed.text
        review = reviewed.json()
        assert review["decision"] == "accepted"
        assert review["claim_id"]
        claims = client.get(f"/api/assessments/{assessment['id']}/claims").json()
        claim = next(item for item in claims if item["id"] == review["claim_id"])
        assert claim["review_status"] == "reviewed"
        assert claim["capability_level"] == 2
        assert claim["evidence_ids"] == [evidence["id"]]
        assert claim["question_ids"] == ["DK-03"]
        assert _gate_state(assessment["id"], "HG-04") == "PASS"

        duplicate = client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-imports/{imported['id']}/proposals/0/review",
            json={"decision": "accepted"},
        )
        assert duplicate.status_code == 409


def test_accept_is_blocked_until_supporting_evidence_is_human_reviewed():
    _reset()
    with client:
        assessment = _assessment()
        evidence = _reviewed_evidence(assessment["id"], reviewed=False)
        imported = client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-import",
            json=_claim_result(assessment["id"], evidence["id"]),
        ).json()

        response = client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-imports/{imported['id']}/proposals/0/review",
            json={"decision": "accepted"},
        )
        assert response.status_code == 409
        assert "reviewed/approved" in response.text
        assert client.get(f"/api/assessments/{assessment['id']}/claims").json() == []
        assert _gate_state(assessment["id"], "HG-04") == "UNVERIFIED"


def test_edit_can_change_mapping_but_requires_known_reviewed_evidence_and_questions():
    _reset()
    with client:
        assessment = _assessment()
        evidence = _reviewed_evidence(assessment["id"])
        imported = client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-import",
            json=_claim_result(assessment["id"], evidence["id"]),
        ).json()

        response = client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-imports/{imported['id']}/proposals/0/review",
            json={
                "decision": "edited",
                "gate_id": "HG-03",
                "statement": "Bearbeitete human-geprüfte Feststellung.",
                "capability_level": 1,
                "evidence_ids": [evidence["id"]],
                "question_ids": ["DK-03"],
                "reviewer_note": "Gate-Zuordnung fachlich korrigiert.",
            },
        )
        assert response.status_code == 201, response.text
        review = response.json()
        assert review["gate_id"] == "HG-03"
        assert review["final_capability_level"] == 1
        claim = next(
            item
            for item in client.get(f"/api/assessments/{assessment['id']}/claims").json()
            if item["id"] == review["claim_id"]
        )
        assert claim["gate_id"] == "HG-03"
        assert claim["statement"] == "Bearbeitete human-geprüfte Feststellung."


def test_reject_records_review_without_creating_claim():
    _reset()
    with client:
        assessment = _assessment()
        evidence = _reviewed_evidence(assessment["id"])
        imported = client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-import",
            json=_claim_result(assessment["id"], evidence["id"]),
        ).json()
        before_gate = _gate_state(assessment["id"], "HG-04")

        response = client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-imports/{imported['id']}/proposals/0/review",
            json={"decision": "rejected", "reviewer_note": "nicht ausreichend belastbar"},
        )
        assert response.status_code == 201
        assert response.json()["claim_id"] is None
        assert client.get(f"/api/assessments/{assessment['id']}/claims").json() == []
        assert _gate_state(assessment["id"], "HG-04") == before_gate


def test_claim_import_contract_rejects_mismatch_unknown_ids_and_wrong_versions():
    _reset()
    with client:
        assessment = _assessment()
        evidence = _reviewed_evidence(assessment["id"])
        payload = _claim_result(assessment["id"], evidence["id"])

        mismatch = dict(payload)
        mismatch["assessment_id"] = "wrong-assessment-id"
        assert client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-import", json=mismatch
        ).status_code == 400

        wrong_version = {**payload, "prompt_version": "claim-proposals-v0"}
        assert client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-import", json=wrong_version
        ).status_code == 422

        unknown_evidence = _claim_result(assessment["id"], "does-not-exist")
        assert client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-import", json=unknown_evidence
        ).status_code == 422

        unknown_question = _claim_result(assessment["id"], evidence["id"])
        unknown_question["proposals"][0]["question_ids"] = ["NOT-A-QUESTION"]
        assert client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/claim-import", json=unknown_question
        ).status_code == 422
