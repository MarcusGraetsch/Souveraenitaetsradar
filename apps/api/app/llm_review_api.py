from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from sovradar.applicability import apply_to_questions, default_profile

from .database import get_db
from .method_catalog import load_questions
from .models import Answer, Assessment, AssessmentProfile, Evidence, LlmImport, LlmProposalReview

router = APIRouter()


class LlmProposalReviewCreate(BaseModel):
    decision: Literal["accepted", "edited", "rejected"]
    answer_value: str = ""
    evidence_ids: list[str] | None = None
    reviewer_note: str = ""


class LlmProposalReviewOut(BaseModel):
    id: str
    assessment_id: str
    llm_import_id: str
    proposal_index: int
    question_id: str
    decision: Literal["accepted", "edited", "rejected"]
    final_answer_value: str
    evidence_ids: list[str]
    answer_id: str | None
    reviewer_note: str
    created_at: datetime


def _assessment_payload(assessment: Assessment) -> dict[str, str]:
    return {
        "id": assessment.id,
        "name": assessment.name,
        "customer": assessment.customer,
        "description": assessment.description,
        "workload_type": assessment.workload_type,
        "criticality": assessment.criticality,
        "confidentiality": assessment.confidentiality,
        "integrity": assessment.integrity,
        "availability": assessment.availability,
        "control_region": assessment.control_region,
        "regulatory_context": assessment.regulatory_context,
    }


def _profile_dict(assessment: Assessment, db: Session) -> dict:
    base = default_profile(_assessment_payload(assessment))
    row = db.get(AssessmentProfile, assessment.id)
    if not row:
        return base
    try:
        saved = json.loads(row.profile_json or "{}")
    except json.JSONDecodeError:
        saved = {}
    return {**base, **saved}


def _question_state(assessment: Assessment, question_id: str, db: Session) -> str:
    evaluated = apply_to_questions(
        load_questions(),
        _assessment_payload(assessment),
        _profile_dict(assessment, db),
    )
    for question in evaluated:
        if question["id"] == question_id:
            return str(question["applicability_status"])
    raise HTTPException(422, f"unknown question_id: {question_id}")


def _as_review(row: LlmProposalReview) -> LlmProposalReviewOut:
    return LlmProposalReviewOut(
        id=row.id,
        assessment_id=row.assessment_id,
        llm_import_id=row.llm_import_id,
        proposal_index=row.proposal_index,
        question_id=row.question_id,
        decision=row.decision,
        final_answer_value=row.final_answer_value,
        evidence_ids=json.loads(row.evidence_ids_json or "[]"),
        answer_id=row.answer_id or None,
        reviewer_note=row.reviewer_note,
        created_at=row.created_at,
    )


def _proposal(import_row: LlmImport, proposal_index: int) -> dict:
    try:
        proposals = json.loads(import_row.proposals_json or "[]")
    except json.JSONDecodeError as exc:
        raise HTTPException(500, "stored LLM proposal payload is invalid") from exc
    if proposal_index < 0 or proposal_index >= len(proposals):
        raise HTTPException(404, "LLM proposal not found")
    proposal = proposals[proposal_index]
    if not isinstance(proposal, dict):
        raise HTTPException(500, "stored LLM proposal has invalid shape")
    return proposal


@router.get(
    "/api/assessments/{assessment_id}/llm-bridge/proposal-reviews",
    response_model=list[LlmProposalReviewOut],
)
def list_llm_proposal_reviews(assessment_id: str, db: Session = Depends(get_db)):
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    rows = db.scalars(
        select(LlmProposalReview)
        .where(LlmProposalReview.assessment_id == assessment_id)
        .order_by(LlmProposalReview.created_at.desc())
    ).all()
    return [_as_review(row) for row in rows]


@router.post(
    "/api/assessments/{assessment_id}/llm-bridge/imports/{llm_import_id}/proposals/{proposal_index}/review",
    response_model=LlmProposalReviewOut,
    status_code=201,
)
def review_llm_proposal(
    assessment_id: str,
    llm_import_id: str,
    proposal_index: int,
    payload: LlmProposalReviewCreate,
    db: Session = Depends(get_db),
):
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(404, "Assessment not found")

    import_row = db.get(LlmImport, llm_import_id)
    if not import_row or import_row.assessment_id != assessment_id:
        raise HTTPException(404, "LLM import not found")

    existing = db.scalar(
        select(LlmProposalReview).where(
            LlmProposalReview.llm_import_id == llm_import_id,
            LlmProposalReview.proposal_index == proposal_index,
        )
    )
    if existing:
        raise HTTPException(409, "LLM proposal has already been reviewed")

    proposal = _proposal(import_row, proposal_index)
    question_id = str(proposal.get("question_id", ""))
    proposed_answer = str(proposal.get("proposed_answer", ""))
    proposed_evidence = [str(item) for item in proposal.get("evidence_ids", [])]

    answer_id: str | None = None
    final_answer_value = ""
    selected_evidence: list[str] = []

    if payload.decision != "rejected":
        applicability = _question_state(assessment, question_id, db)
        if applicability != "applicable":
            raise HTTPException(
                409,
                f"question applicability must be resolved before accepting an LLM proposal (current: {applicability})",
            )

        if payload.decision == "accepted":
            final_answer_value = proposed_answer
        else:
            final_answer_value = payload.answer_value.strip()
            if not final_answer_value:
                raise HTTPException(422, "edited review requires a non-empty answer_value")

        selected_evidence = proposed_evidence if payload.evidence_ids is None else payload.evidence_ids
        if not set(selected_evidence).issubset(set(proposed_evidence)):
            raise HTTPException(422, "review evidence_ids must be a subset of the proposal evidence_ids")
        known_evidence = set(
            db.scalars(select(Evidence.id).where(Evidence.assessment_id == assessment_id)).all()
        )
        unknown_evidence = set(selected_evidence) - known_evidence
        if unknown_evidence:
            raise HTTPException(422, f"unknown evidence id(s): {sorted(unknown_evidence)}")

        answer = db.scalar(
            select(Answer).where(
                Answer.assessment_id == assessment_id,
                Answer.question_id == question_id,
            )
        )
        if answer is None:
            answer = Answer(
                id=str(uuid.uuid4()),
                assessment_id=assessment_id,
                question_id=question_id,
            )
            db.add(answer)
        answer.answer_value = final_answer_value
        answer.evidence_ids_json = json.dumps(selected_evidence)
        answer.review_state = "reviewed"
        db.flush()
        answer_id = answer.id

    review = LlmProposalReview(
        id=str(uuid.uuid4()),
        assessment_id=assessment_id,
        llm_import_id=llm_import_id,
        proposal_index=proposal_index,
        question_id=question_id,
        decision=payload.decision,
        final_answer_value=final_answer_value,
        evidence_ids_json=json.dumps(selected_evidence),
        answer_id=answer_id or "",
        reviewer_note=payload.reviewer_note,
    )
    db.add(review)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(409, "LLM proposal has already been reviewed") from exc
    db.refresh(review)
    return _as_review(review)
