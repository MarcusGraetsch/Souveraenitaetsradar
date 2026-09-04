from __future__ import annotations

import json
import uuid
from datetime import datetime
from functools import lru_cache
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from sovradar.applicability import apply_to_questions, default_profile
from sovradar.gate_catalog import load_hard_gates

from .database import get_db
from .llm_claim_bridge import CLAIM_PROMPT_VERSION, METHOD_VERSION, build_claim_prompt
from .method_catalog import load_questions, question_ids
from .models import (
    Answer,
    Assessment,
    AssessmentClaim,
    AssessmentProfile,
    Evidence,
    EvidenceReview,
    GateRequirement,
    LlmClaimImport,
    LlmClaimProposalReview,
)
from .settings import settings

router = APIRouter()

CRITICALITY_TEMPLATE = {
    "low": "basis",
    "medium": "standard",
    "high": "elevated",
    "critical": "critical",
}


class LlmClaimProposal(BaseModel):
    gate_id: str = Field(pattern=r"^HG-0[1-8]$")
    statement: str = Field(min_length=1)
    capability_level: int | None = Field(default=None, ge=0, le=4)
    evidence_ids: list[str] = Field(min_length=1)
    question_ids: list[str] = Field(min_length=1)
    rationale: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)


class LlmClaimGap(BaseModel):
    gate_id: str = Field(pattern=r"^HG-0[1-8]$")
    question_ids: list[str] = Field(default_factory=list)
    missing: str = Field(min_length=1)


class LlmClaimBridgeResult(BaseModel):
    assessment_id: str
    prompt_version: str
    method_version: str
    proposals: list[LlmClaimProposal] = Field(default_factory=list)
    evidence_gaps: list[LlmClaimGap] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class LlmClaimImportOut(BaseModel):
    id: str
    assessment_id: str
    prompt_version: str
    method_version: str
    validation_status: str
    proposals: list[LlmClaimProposal]
    evidence_gaps: list[LlmClaimGap]
    warnings: list[str]
    created_at: datetime


class LlmClaimProposalReviewCreate(BaseModel):
    decision: Literal["accepted", "edited", "rejected"]
    gate_id: str | None = Field(default=None, pattern=r"^HG-0[1-8]$")
    statement: str = ""
    capability_level: int | None = Field(default=None, ge=0, le=4)
    evidence_ids: list[str] | None = None
    question_ids: list[str] | None = None
    reviewer_note: str = ""


class LlmClaimProposalReviewOut(BaseModel):
    id: str
    assessment_id: str
    llm_claim_import_id: str
    proposal_index: int
    gate_id: str
    decision: Literal["accepted", "edited", "rejected"]
    final_statement: str
    final_capability_level: int | None
    evidence_ids: list[str]
    question_ids: list[str]
    claim_id: str | None
    reviewer_note: str
    created_at: datetime


@lru_cache(maxsize=1)
def _gate_map():
    return {
        gate.gate_id: gate
        for gate in load_hard_gates(settings.method_dir / "r4_hard_gates.csv")
    }


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


def _questions(assessment: Assessment, db: Session) -> list[dict]:
    answered_ids = set(
        db.scalars(
            select(Answer.question_id).where(
                Answer.assessment_id == assessment.id,
                Answer.answer_value != "",
            )
        ).all()
    )
    return apply_to_questions(
        load_questions(),
        _assessment_payload(assessment),
        _profile_dict(assessment, db),
        answered_question_ids=answered_ids,
    )


def _default_requirement(assessment: Assessment, gate_id: str) -> tuple[int, str]:
    gate = _gate_map().get(gate_id)
    if gate is None:
        raise HTTPException(422, f"unknown gate_id: {gate_id}")
    template = CRITICALITY_TEMPLATE.get(assessment.criticality, "standard")
    return gate.requirements[template], f"criticality-template:{template}"


def _requirement(assessment: Assessment, gate_id: str, db: Session) -> tuple[int, str]:
    row = db.get(GateRequirement, (assessment.id, gate_id))
    if row is not None:
        return row.requirement_level, row.source
    return _default_requirement(assessment, gate_id)


def _evidence_payload(assessment_id: str, db: Session) -> tuple[list[dict], dict[str, dict]]:
    reviews = {
        row.evidence_id: row
        for row in db.scalars(
            select(EvidenceReview).where(EvidenceReview.assessment_id == assessment_id)
        ).all()
    }
    evidence_payload: list[dict] = []
    review_payload: dict[str, dict] = {}
    for item in db.scalars(
        select(Evidence).where(Evidence.assessment_id == assessment_id)
    ).all():
        review = reviews.get(item.id)
        evidence_payload.append(
            {
                "id": item.id,
                "title": item.title,
                "evidence_type": item.evidence_type,
                "source": item.source,
                "source_date": item.source_date,
                "content_excerpt": item.content_excerpt,
            }
        )
        review_payload[item.id] = {
            "review_status": review.review_status if review else "raw",
            "applied_state": review.applied_state if review else "asserted",
            "effective_trust": min(review.base_trust, review.scope_fit, review.freshness_fit)
            if review
            else 0,
        }
    return evidence_payload, review_payload


def _answers_payload(assessment_id: str, db: Session) -> list[dict]:
    rows = db.scalars(select(Answer).where(Answer.assessment_id == assessment_id)).all()
    return [
        {
            "question_id": row.question_id,
            "answer_value": row.answer_value,
            "comment": row.comment,
            "evidence_ids": json.loads(row.evidence_ids_json or "[]"),
            "review_state": row.review_state,
        }
        for row in rows
    ]


def _claims_payload(assessment_id: str, db: Session) -> list[dict]:
    rows = db.scalars(
        select(AssessmentClaim).where(AssessmentClaim.assessment_id == assessment_id)
    ).all()
    return [
        {
            "id": row.id,
            "gate_id": row.gate_id,
            "statement": row.statement,
            "review_status": row.review_status,
            "capability_level": row.capability_level,
            "evidence_ids": json.loads(row.evidence_ids_json or "[]"),
            "question_ids": json.loads(row.question_ids_json or "[]"),
        }
        for row in rows
    ]


def _gates_payload(assessment: Assessment, db: Session) -> list[dict]:
    payload: list[dict] = []
    for gate in _gate_map().values():
        level, source = _requirement(assessment, gate.gate_id, db)
        payload.append(
            {
                "gate_id": gate.gate_id,
                "name": gate.name,
                "subject": gate.subject,
                "requirement_level": level,
                "requirement_source": source,
                "capability_levels": gate.capability_levels,
            }
        )
    return payload


def _as_import(row: LlmClaimImport) -> LlmClaimImportOut:
    return LlmClaimImportOut(
        id=row.id,
        assessment_id=row.assessment_id,
        prompt_version=row.prompt_version,
        method_version=row.method_version,
        validation_status=row.validation_status,
        proposals=json.loads(row.proposals_json or "[]"),
        evidence_gaps=json.loads(row.gaps_json or "[]"),
        warnings=json.loads(row.warnings_json or "[]"),
        created_at=row.created_at,
    )


def _as_review(row: LlmClaimProposalReview) -> LlmClaimProposalReviewOut:
    return LlmClaimProposalReviewOut(
        id=row.id,
        assessment_id=row.assessment_id,
        llm_claim_import_id=row.llm_claim_import_id,
        proposal_index=row.proposal_index,
        gate_id=row.gate_id,
        decision=row.decision,
        final_statement=row.final_statement,
        final_capability_level=row.final_capability_level,
        evidence_ids=json.loads(row.evidence_ids_json or "[]"),
        question_ids=json.loads(row.question_ids_json or "[]"),
        claim_id=row.claim_id or None,
        reviewer_note=row.reviewer_note,
        created_at=row.created_at,
    )


def _proposal(import_row: LlmClaimImport, proposal_index: int) -> dict:
    try:
        proposals = json.loads(import_row.proposals_json or "[]")
    except json.JSONDecodeError as exc:
        raise HTTPException(500, "stored LLM claim proposal payload is invalid") from exc
    if proposal_index < 0 or proposal_index >= len(proposals):
        raise HTTPException(404, "LLM claim proposal not found")
    proposal = proposals[proposal_index]
    if not isinstance(proposal, dict):
        raise HTTPException(500, "stored LLM claim proposal has invalid shape")
    return proposal


def _validate_evidence_ids(
    assessment_id: str,
    evidence_ids: list[str],
    db: Session,
    *,
    require_reviewed: bool,
) -> None:
    if not evidence_ids:
        raise HTTPException(422, "a reviewed finding requires at least one evidence id")
    known = set(
        db.scalars(select(Evidence.id).where(Evidence.assessment_id == assessment_id)).all()
    )
    unknown = set(evidence_ids) - known
    if unknown:
        raise HTTPException(422, f"unknown evidence id(s): {sorted(unknown)}")
    if require_reviewed:
        reviewed = set(
            db.scalars(
                select(EvidenceReview.evidence_id).where(
                    EvidenceReview.assessment_id == assessment_id,
                    EvidenceReview.review_status.in_(["reviewed", "approved"]),
                )
            ).all()
        )
        not_reviewed = set(evidence_ids) - reviewed
        if not_reviewed:
            raise HTTPException(
                409,
                "supporting evidence must be reviewed/approved before accepting a finding: "
                f"{sorted(not_reviewed)}",
            )


def _validate_question_ids(values: list[str]) -> None:
    if not values:
        raise HTTPException(422, "a finding proposal requires at least one question id")
    unknown = set(values) - question_ids()
    if unknown:
        raise HTTPException(422, f"unknown question id(s): {sorted(unknown)}")


@router.get("/api/assessments/{assessment_id}/llm-bridge/claim-prompt")
def claim_prompt(assessment_id: str, db: Session = Depends(get_db)):
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(404, "Assessment not found")
    evidence, reviews = _evidence_payload(assessment_id, db)
    return {
        "prompt_version": CLAIM_PROMPT_VERSION,
        "method_version": METHOD_VERSION,
        "prompt": build_claim_prompt(
            _assessment_payload(assessment),
            _profile_dict(assessment, db),
            _answers_payload(assessment_id, db),
            evidence,
            reviews,
            _questions(assessment, db),
            _gates_payload(assessment, db),
            _claims_payload(assessment_id, db),
        ),
    }


@router.post(
    "/api/assessments/{assessment_id}/llm-bridge/claim-import",
    response_model=LlmClaimImportOut,
)
def import_claim_proposals(
    assessment_id: str,
    payload: LlmClaimBridgeResult,
    db: Session = Depends(get_db),
):
    if payload.assessment_id != assessment_id:
        raise HTTPException(400, "assessment_id mismatch")
    if payload.prompt_version != CLAIM_PROMPT_VERSION:
        raise HTTPException(422, f"unsupported prompt_version: {payload.prompt_version}")
    if payload.method_version != METHOD_VERSION:
        raise HTTPException(422, f"unsupported method_version: {payload.method_version}")
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")

    gates = _gate_map()
    for proposal in payload.proposals:
        if proposal.gate_id not in gates:
            raise HTTPException(422, f"unknown gate_id: {proposal.gate_id}")
        _validate_evidence_ids(assessment_id, proposal.evidence_ids, db, require_reviewed=False)
        _validate_question_ids(proposal.question_ids)
    for gap in payload.evidence_gaps:
        if gap.gate_id not in gates:
            raise HTTPException(422, f"unknown gate_id: {gap.gate_id}")
        if gap.question_ids:
            _validate_question_ids(gap.question_ids)

    row = LlmClaimImport(
        id=str(uuid.uuid4()),
        assessment_id=assessment_id,
        prompt_version=payload.prompt_version,
        method_version=payload.method_version,
        raw_json=payload.model_dump_json(),
        proposals_json=json.dumps(
            [item.model_dump() for item in payload.proposals], ensure_ascii=False
        ),
        gaps_json=json.dumps(
            [item.model_dump() for item in payload.evidence_gaps], ensure_ascii=False
        ),
        warnings_json=json.dumps(payload.warnings, ensure_ascii=False),
        validation_status="valid",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _as_import(row)


@router.get(
    "/api/assessments/{assessment_id}/llm-bridge/claim-imports",
    response_model=list[LlmClaimImportOut],
)
def list_claim_imports(assessment_id: str, db: Session = Depends(get_db)):
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    rows = db.scalars(
        select(LlmClaimImport)
        .where(LlmClaimImport.assessment_id == assessment_id)
        .order_by(LlmClaimImport.created_at.desc())
    ).all()
    return [_as_import(row) for row in rows]


@router.get(
    "/api/assessments/{assessment_id}/llm-bridge/claim-proposal-reviews",
    response_model=list[LlmClaimProposalReviewOut],
)
def list_claim_proposal_reviews(assessment_id: str, db: Session = Depends(get_db)):
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    rows = db.scalars(
        select(LlmClaimProposalReview)
        .where(LlmClaimProposalReview.assessment_id == assessment_id)
        .order_by(LlmClaimProposalReview.created_at.desc())
    ).all()
    return [_as_review(row) for row in rows]


@router.post(
    "/api/assessments/{assessment_id}/llm-bridge/claim-imports/{claim_import_id}/proposals/{proposal_index}/review",
    response_model=LlmClaimProposalReviewOut,
    status_code=201,
)
def review_claim_proposal(
    assessment_id: str,
    claim_import_id: str,
    proposal_index: int,
    payload: LlmClaimProposalReviewCreate,
    db: Session = Depends(get_db),
):
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    import_row = db.get(LlmClaimImport, claim_import_id)
    if not import_row or import_row.assessment_id != assessment_id:
        raise HTTPException(404, "LLM claim import not found")

    existing = db.scalar(
        select(LlmClaimProposalReview).where(
            LlmClaimProposalReview.llm_claim_import_id == claim_import_id,
            LlmClaimProposalReview.proposal_index == proposal_index,
        )
    )
    if existing:
        raise HTTPException(409, "LLM claim proposal has already been reviewed")

    proposal = _proposal(import_row, proposal_index)
    proposed_gate = str(proposal.get("gate_id", ""))
    proposed_statement = str(proposal.get("statement", ""))
    proposed_capability = proposal.get("capability_level")
    proposed_evidence = [str(item) for item in proposal.get("evidence_ids", [])]
    proposed_questions = [str(item) for item in proposal.get("question_ids", [])]

    final_gate = proposed_gate
    final_statement = ""
    final_capability: int | None = None
    final_evidence: list[str] = []
    final_questions: list[str] = []
    claim_id: str | None = None
    review_id = str(uuid.uuid4())

    if payload.decision != "rejected":
        if payload.decision == "accepted":
            final_gate = proposed_gate
            final_statement = proposed_statement.strip()
            final_capability = proposed_capability
            final_evidence = proposed_evidence
            final_questions = proposed_questions
        else:
            final_gate = payload.gate_id or proposed_gate
            final_statement = payload.statement.strip()
            if not final_statement:
                raise HTTPException(422, "edited review requires a non-empty statement")
            final_capability = payload.capability_level
            final_evidence = payload.evidence_ids if payload.evidence_ids is not None else proposed_evidence
            final_questions = payload.question_ids if payload.question_ids is not None else proposed_questions

        if final_gate not in _gate_map():
            raise HTTPException(422, f"unknown gate_id: {final_gate}")
        if not final_statement:
            raise HTTPException(422, "reviewed finding must not be empty")
        if final_capability is not None and final_capability not in range(0, 5):
            raise HTTPException(422, "capability_level must be between 0 and 4")
        _validate_evidence_ids(
            assessment_id, final_evidence, db, require_reviewed=True
        )
        _validate_question_ids(final_questions)

        claim_id = str(uuid.uuid4())
        db.add(
            AssessmentClaim(
                id=claim_id,
                assessment_id=assessment_id,
                gate_id=final_gate,
                statement=final_statement,
                review_status="reviewed",
                capability_level=final_capability,
                evidence_ids_json=json.dumps(final_evidence),
                question_ids_json=json.dumps(final_questions),
                notes=(
                    f"Human-reviewed aus LLM-Feststellungsvorschlag {claim_import_id}"
                    f"#{proposal_index}; Review-ID {review_id}."
                ),
            )
        )
        db.flush()

    review = LlmClaimProposalReview(
        id=review_id,
        assessment_id=assessment_id,
        llm_claim_import_id=claim_import_id,
        proposal_index=proposal_index,
        gate_id=final_gate,
        decision=payload.decision,
        final_statement=final_statement,
        final_capability_level=final_capability,
        evidence_ids_json=json.dumps(final_evidence),
        question_ids_json=json.dumps(final_questions),
        claim_id=claim_id or "",
        reviewer_note=payload.reviewer_note,
    )
    db.add(review)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(409, "LLM claim proposal has already been reviewed") from exc
    db.refresh(review)
    return _as_review(review)
