from __future__ import annotations

import json
import uuid
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from sovradar.gate_catalog import evidence_requests_by_gate, load_evidence_requests, load_hard_gates, validate_gate_evidence_mapping
from sovradar.gate_evaluation import evaluate_gate
from sovradar.models import AppliedState, Claim as CoreClaim, EvidenceRecord

from .database import get_db
from .llm_review_api import router as llm_review_router
from .method_catalog import question_ids
from .models import Assessment, AssessmentClaim, Evidence, EvidenceReview, GateRequirement
from .schemas import (
    ClaimCreate,
    ClaimOut,
    EvidenceRequestOut,
    EvidenceReviewOut,
    EvidenceReviewUpsert,
    GateDefinitionOut,
    GateEvaluationOut,
    GateRequirementOut,
    GateRequirementUpsert,
)
from .settings import settings

router = APIRouter()
# API composition: main.py already mounts this router. Keep the LLM answer-review
# router separate in implementation while exposing it through the existing API mount.
router.include_router(llm_review_router)

CRITICALITY_TEMPLATE = {
    "low": "basis",
    "medium": "standard",
    "high": "elevated",
    "critical": "critical",
}


@lru_cache(maxsize=1)
def _catalog():
    gates = load_hard_gates(settings.method_dir / "r4_hard_gates.csv")
    requests = load_evidence_requests(settings.method_dir / "evidence_request_catalog.csv")
    validate_gate_evidence_mapping(gates, requests)
    return gates, evidence_requests_by_gate(requests)


def _gate_map():
    gates, _ = _catalog()
    return {gate.gate_id: gate for gate in gates}


def _evidence_request_out(item) -> EvidenceRequestOut:
    return EvidenceRequestOut(
        request_id=item.request_id,
        gate_id=item.gate_id,
        claim_area=item.claim_area,
        acceptable_evidence=item.acceptable_evidence,
        required_for=item.required_for,
        follow_up=item.follow_up,
        preferred_applied_state=item.preferred_applied_state,
        typical_min_trust=item.typical_min_trust,
        provenance=item.provenance,
    )


def _default_requirement(assessment: Assessment, gate_id: str) -> tuple[int, str]:
    gate = _gate_map().get(gate_id)
    if gate is None:
        raise HTTPException(400, f"unknown gate_id: {gate_id}")
    template = CRITICALITY_TEMPLATE.get(assessment.criticality, "standard")
    return gate.requirements[template], f"criticality-template:{template}"


def _requirement(assessment: Assessment, gate_id: str, db: Session) -> tuple[int, str, object | None]:
    row = db.get(GateRequirement, (assessment.id, gate_id))
    if row is not None:
        return row.requirement_level, row.source, row.updated_at
    level, source = _default_requirement(assessment, gate_id)
    return level, source, None


def _as_claim(row: AssessmentClaim) -> ClaimOut:
    return ClaimOut(
        id=row.id,
        assessment_id=row.assessment_id,
        gate_id=row.gate_id,
        statement=row.statement,
        review_status=row.review_status,
        capability_level=row.capability_level,
        evidence_ids=json.loads(row.evidence_ids_json or "[]"),
        question_ids=json.loads(row.question_ids_json or "[]"),
        notes=row.notes,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _validate_claim_links(assessment_id: str, payload: ClaimCreate, db: Session) -> None:
    if payload.gate_id not in _gate_map():
        raise HTTPException(422, f"unknown gate_id: {payload.gate_id}")
    known_evidence = set(db.scalars(select(Evidence.id).where(Evidence.assessment_id == assessment_id)).all())
    unknown_evidence = set(payload.evidence_ids) - known_evidence
    if unknown_evidence:
        raise HTTPException(422, f"unknown evidence id(s): {sorted(unknown_evidence)}")
    unknown_questions = set(payload.question_ids) - question_ids()
    if unknown_questions:
        raise HTTPException(422, f"unknown question id(s): {sorted(unknown_questions)}")


def _review_out(row: EvidenceReview) -> EvidenceReviewOut:
    return EvidenceReviewOut(
        evidence_id=row.evidence_id,
        assessment_id=row.assessment_id,
        applied_state=row.applied_state,
        base_trust=row.base_trust,
        scope_fit=row.scope_fit,
        freshness_fit=row.freshness_fit,
        review_status=row.review_status,
        effective_trust=min(row.base_trust, row.scope_fit, row.freshness_fit),
        updated_at=row.updated_at,
    )


def _core_evidence(assessment_id: str, db: Session) -> list[EvidenceRecord]:
    evidence_rows = db.scalars(select(Evidence).where(Evidence.assessment_id == assessment_id)).all()
    reviews = {
        row.evidence_id: row
        for row in db.scalars(select(EvidenceReview).where(EvidenceReview.assessment_id == assessment_id)).all()
    }
    records: list[EvidenceRecord] = []
    for item in evidence_rows:
        review = reviews.get(item.id)
        records.append(
            EvidenceRecord(
                evidence_id=item.id,
                evidence_type=item.evidence_type,
                title=item.title,
                producer=item.source or "consultant-intake",
                scope={"workload_id": assessment_id},
                applied_state=AppliedState(review.applied_state if review else "asserted"),
                base_trust=review.base_trust if review else 0,
                scope_fit=review.scope_fit if review else 0,
                freshness_fit=review.freshness_fit if review else 0,
                sensitivity="internal",
                review_status=review.review_status if review else "raw",
                source_ref=item.source or None,
                locator=item.source_date or None,
                notes=item.description or None,
            )
        )
    return records


def _core_claims(assessment_id: str, db: Session) -> list[CoreClaim]:
    rows = db.scalars(select(AssessmentClaim).where(AssessmentClaim.assessment_id == assessment_id)).all()
    return [
        CoreClaim(
            claim_id=row.id,
            gate_id=row.gate_id,
            statement=row.statement,
            review_status=row.review_status,
            capability_level=row.capability_level,
            evidence_ids=tuple(json.loads(row.evidence_ids_json or "[]")),
            question_ids=tuple(json.loads(row.question_ids_json or "[]")),
            notes=row.notes or None,
        )
        for row in rows
    ]


@router.get("/api/method/hard-gates", response_model=list[GateDefinitionOut])
def hard_gates():
    gates, grouped = _catalog()
    return [
        GateDefinitionOut(
            gate_id=gate.gate_id,
            name=gate.name,
            subject=gate.subject,
            requirement_templates=gate.requirements,
            source_ids=list(gate.source_ids),
            provenance=gate.provenance,
            evidence_requests=[_evidence_request_out(item) for item in grouped.get(gate.gate_id, [])],
        )
        for gate in gates
    ]


@router.get("/api/assessments/{assessment_id}/gate-requirements", response_model=list[GateRequirementOut])
def gate_requirements(assessment_id: str, db: Session = Depends(get_db)):
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(404, "Assessment not found")
    gates, _ = _catalog()
    result = []
    for gate in gates:
        level, source, updated_at = _requirement(assessment, gate.gate_id, db)
        result.append(GateRequirementOut(assessment_id=assessment_id, gate_id=gate.gate_id, requirement_level=level, source=source, updated_at=updated_at))
    return result


@router.put("/api/assessments/{assessment_id}/gate-requirements/{gate_id}", response_model=GateRequirementOut)
def put_gate_requirement(assessment_id: str, gate_id: str, payload: GateRequirementUpsert, db: Session = Depends(get_db)):
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(404, "Assessment not found")
    if gate_id not in _gate_map():
        raise HTTPException(400, "unknown gate_id")
    row = db.get(GateRequirement, (assessment_id, gate_id))
    if row is None:
        row = GateRequirement(assessment_id=assessment_id, gate_id=gate_id, requirement_level=payload.requirement_level, source="consultant-override")
        db.add(row)
    else:
        row.requirement_level = payload.requirement_level
        row.source = "consultant-override"
    db.commit()
    db.refresh(row)
    return GateRequirementOut(assessment_id=row.assessment_id, gate_id=row.gate_id, requirement_level=row.requirement_level, source=row.source, updated_at=row.updated_at)


@router.get("/api/assessments/{assessment_id}/evidence-reviews", response_model=list[EvidenceReviewOut])
def evidence_reviews(assessment_id: str, db: Session = Depends(get_db)):
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    rows = db.scalars(select(EvidenceReview).where(EvidenceReview.assessment_id == assessment_id)).all()
    return [_review_out(row) for row in rows]


@router.put("/api/assessments/{assessment_id}/evidence/{evidence_id}/review", response_model=EvidenceReviewOut)
def put_evidence_review(assessment_id: str, evidence_id: str, payload: EvidenceReviewUpsert, db: Session = Depends(get_db)):
    evidence = db.get(Evidence, evidence_id)
    if evidence is None or evidence.assessment_id != assessment_id:
        raise HTTPException(404, "Evidence not found")
    row = db.get(EvidenceReview, evidence_id)
    if row is None:
        row = EvidenceReview(evidence_id=evidence_id, assessment_id=assessment_id)
        db.add(row)
    row.applied_state = payload.applied_state
    row.base_trust = payload.base_trust
    row.scope_fit = payload.scope_fit
    row.freshness_fit = payload.freshness_fit
    row.review_status = payload.review_status
    db.commit()
    db.refresh(row)
    return _review_out(row)


@router.get("/api/assessments/{assessment_id}/claims", response_model=list[ClaimOut])
def claims(assessment_id: str, db: Session = Depends(get_db)):
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    rows = db.scalars(select(AssessmentClaim).where(AssessmentClaim.assessment_id == assessment_id).order_by(AssessmentClaim.created_at)).all()
    return [_as_claim(row) for row in rows]


@router.post("/api/assessments/{assessment_id}/claims", response_model=ClaimOut, status_code=201)
def create_claim(assessment_id: str, payload: ClaimCreate, db: Session = Depends(get_db)):
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    _validate_claim_links(assessment_id, payload, db)
    row = AssessmentClaim(
        id=str(uuid.uuid4()),
        assessment_id=assessment_id,
        gate_id=payload.gate_id,
        statement=payload.statement,
        review_status=payload.review_status,
        capability_level=payload.capability_level,
        evidence_ids_json=json.dumps(payload.evidence_ids),
        question_ids_json=json.dumps(payload.question_ids),
        notes=payload.notes,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _as_claim(row)


@router.put("/api/assessments/{assessment_id}/claims/{claim_id}", response_model=ClaimOut)
def put_claim(assessment_id: str, claim_id: str, payload: ClaimCreate, db: Session = Depends(get_db)):
    row = db.get(AssessmentClaim, claim_id)
    if row is None or row.assessment_id != assessment_id:
        raise HTTPException(404, "Claim not found")
    _validate_claim_links(assessment_id, payload, db)
    row.gate_id = payload.gate_id
    row.statement = payload.statement
    row.review_status = payload.review_status
    row.capability_level = payload.capability_level
    row.evidence_ids_json = json.dumps(payload.evidence_ids)
    row.question_ids_json = json.dumps(payload.question_ids)
    row.notes = payload.notes
    db.commit()
    db.refresh(row)
    return _as_claim(row)


@router.delete("/api/assessments/{assessment_id}/claims/{claim_id}", status_code=204)
def delete_claim(assessment_id: str, claim_id: str, db: Session = Depends(get_db)):
    row = db.get(AssessmentClaim, claim_id)
    if row is None or row.assessment_id != assessment_id:
        raise HTTPException(404, "Claim not found")
    db.delete(row)
    db.commit()


@router.get("/api/assessments/{assessment_id}/gates", response_model=list[GateEvaluationOut])
def evaluate_gates(assessment_id: str, db: Session = Depends(get_db)):
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(404, "Assessment not found")
    gates, grouped = _catalog()
    core_claims = _core_claims(assessment_id, db)
    core_evidence = _core_evidence(assessment_id, db)
    result: list[GateEvaluationOut] = []
    for gate in gates:
        requirement_level, requirement_source, _ = _requirement(assessment, gate.gate_id, db)
        evaluated = evaluate_gate(gate.gate_id, requirement_level, core_claims, core_evidence)
        result.append(
            GateEvaluationOut(
                gate_id=gate.gate_id,
                name=gate.name,
                subject=gate.subject,
                requirement_level=requirement_level,
                requirement_source=requirement_source,
                capability_level=evaluated.capability_level,
                effective_trust=evaluated.effective_trust,
                technical_state=evaluated.technical_state,
                evidence_state=evaluated.evidence_state,
                final_state=evaluated.final_state,
                claim_ids=list(evaluated.claim_ids),
                evidence_ids=list(evaluated.evidence_ids),
                reasons=list(evaluated.reasons),
                evidence_requests=[_evidence_request_out(item) for item in grouped.get(gate.gate_id, [])],
            )
        )
    return result
