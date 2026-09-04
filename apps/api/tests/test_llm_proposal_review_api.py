from __future__ import annotations

import pytest
from fastapi import HTTPException
from sqlalchemy import delete

from apps.api.app.database import SessionLocal
from apps.api.app.llm_review_api import _validate_answer_value
from apps.api.app.models import LlmProposalReview
from apps.api.tests.test_api import client, reset_db


def _reset() -> None:
    with SessionLocal() as db:
        db.execute(delete(LlmProposalReview))
        db.commit()
    reset_db()


def _fixture(question_id: str = "DK-03", workload_type: str = "saas") -> tuple[str, str, str]:
    assessment = client.post(
        "/api/assessments",
        json={
            "name": "LLM proposal review test",
            "customer": "Synthetic Customer",
            "workload_type": workload_type,
            "criticality": "medium",
            "confidentiality": "medium",
            "integrity": "medium",
            "availability": "medium",
        },
    ).json()
    assessment_id = assessment["id"]

    evidence = client.post(
        f"/api/assessments/{assessment_id}/evidence",
        data={
            "title": "Reviewed source excerpt",
            "evidence_type": "customer-statement",
            "description": "Internal description",
            "source": "Synthetic workshop",
            "content_excerpt": "Synthetic approved excerpt",
        },
    ).json()
    evidence_id = evidence["id"]

    imported = client.post(
        f"/api/assessments/{assessment_id}/llm-bridge/import",
        json={
            "assessment_id": assessment_id,
            "proposals": [
                {
                    "question_id": question_id,
                    "proposed_answer": "Provider",
                    "rationale": "Synthetic rationale",
                    "evidence_ids": [evidence_id],
                    "confidence": 0.72,
                }
            ],
            "evidence_gaps": [],
            "warnings": [],
        },
    )
    assert imported.status_code == 200, imported.text
    return assessment_id, evidence_id, imported.json()["id"]


def _gate_states(assessment_id: str) -> dict[str, str]:
    return {
        item["gate_id"]: item["final_state"]
        for item in client.get(f"/api/assessments/{assessment_id}/gates").json()
    }


def test_accept_proposal_creates_reviewed_answer_and_audit_record_without_gate_change() -> None:
    _reset()
    with client:
        assessment_id, evidence_id, import_id = _fixture()
        before = _gate_states(assessment_id)

        response = client.post(
            f"/api/assessments/{assessment_id}/llm-bridge/imports/{import_id}/proposals/0/review",
            json={"decision": "accepted"},
        )
        assert response.status_code == 201, response.text
        review = response.json()
        assert review["decision"] == "accepted"
        assert review["question_id"] == "DK-03"
        assert review["final_answer_value"] == "Provider"
        assert review["evidence_ids"] == [evidence_id]
        assert review["answer_id"]

        answers = client.get(f"/api/assessments/{assessment_id}/answers").json()
        assert len(answers) == 1
        assert answers[0]["question_id"] == "DK-03"
        assert answers[0]["answer_value"] == "Provider"
        assert answers[0]["evidence_ids"] == [evidence_id]
        assert answers[0]["review_state"] == "reviewed"

        reviews = client.get(
            f"/api/assessments/{assessment_id}/llm-bridge/proposal-reviews"
        ).json()
        assert [item["id"] for item in reviews] == [review["id"]]
        assert _gate_states(assessment_id) == before


def test_edit_and_accept_uses_consultant_answer_not_original_proposal() -> None:
    _reset()
    with client:
        assessment_id, evidence_id, import_id = _fixture()
        response = client.post(
            f"/api/assessments/{assessment_id}/llm-bridge/imports/{import_id}/proposals/0/review",
            json={
                "decision": "edited",
                "answer_value": "Kunde und Provider gemeinsam",
                "evidence_ids": [evidence_id],
                "reviewer_note": "Proposal fachlich präzisiert.",
            },
        )
        assert response.status_code == 201, response.text
        review = response.json()
        assert review["decision"] == "edited"
        assert review["final_answer_value"] == "Kunde und Provider gemeinsam"
        assert review["reviewer_note"] == "Proposal fachlich präzisiert."

        answer = client.get(f"/api/assessments/{assessment_id}/answers").json()[0]
        assert answer["answer_value"] == "Kunde und Provider gemeinsam"
        assert answer["review_state"] == "reviewed"


def test_reject_is_auditable_and_does_not_create_answer() -> None:
    _reset()
    with client:
        assessment_id, _, import_id = _fixture()
        response = client.post(
            f"/api/assessments/{assessment_id}/llm-bridge/imports/{import_id}/proposals/0/review",
            json={"decision": "rejected", "reviewer_note": "Nicht ausreichend getragen."},
        )
        assert response.status_code == 201, response.text
        assert response.json()["decision"] == "rejected"
        assert response.json()["answer_id"] is None
        assert client.get(f"/api/assessments/{assessment_id}/answers").json() == []


def test_same_proposal_cannot_be_reviewed_twice() -> None:
    _reset()
    with client:
        assessment_id, _, import_id = _fixture()
        path = (
            f"/api/assessments/{assessment_id}/llm-bridge/imports/{import_id}/proposals/0/review"
        )
        assert client.post(path, json={"decision": "accepted"}).status_code == 201
        second = client.post(path, json={"decision": "rejected"})
        assert second.status_code == 409


def test_non_applicable_or_unresolved_question_must_be_clarified_before_acceptance() -> None:
    _reset()
    with client:
        assessment_id, _, import_id = _fixture(question_id="KI-01", workload_type="other")
        response = client.post(
            f"/api/assessments/{assessment_id}/llm-bridge/imports/{import_id}/proposals/0/review",
            json={"decision": "accepted"},
        )
        assert response.status_code == 409
        assert "applicability" in response.text
        assert client.get(f"/api/assessments/{assessment_id}/answers").json() == []


def test_review_cannot_add_evidence_not_present_in_proposal() -> None:
    _reset()
    with client:
        assessment_id, _, import_id = _fixture()
        other = client.post(
            f"/api/assessments/{assessment_id}/evidence",
            data={"title": "Other evidence", "evidence_type": "other"},
        ).json()
        response = client.post(
            f"/api/assessments/{assessment_id}/llm-bridge/imports/{import_id}/proposals/0/review",
            json={"decision": "accepted", "evidence_ids": [other["id"]]},
        )
        assert response.status_code == 422


def test_single_select_review_requires_machine_readable_method_value() -> None:
    question = {
        "answer_type": "Boolean",
        "answer_control": {
            "kind": "single_select",
            "options": [
                {"value": "yes", "label": "Ja"},
                {"value": "no", "label": "Nein"},
            ],
        },
    }
    _validate_answer_value(question, "yes")
    with pytest.raises(HTTPException) as exc:
        _validate_answer_value(question, "Ja")
    assert exc.value.status_code == 422


def test_date_review_requires_iso_date() -> None:
    question = {
        "answer_type": "Datum",
        "answer_control": {"kind": "date", "options": []},
    }
    _validate_answer_value(question, "2026-09-04")
    with pytest.raises(HTTPException) as exc:
        _validate_answer_value(question, "04.09.2026")
    assert exc.value.status_code == 422
