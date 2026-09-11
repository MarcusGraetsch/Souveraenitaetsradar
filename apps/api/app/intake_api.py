from __future__ import annotations

import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sovradar.applicability import default_profile

from .database import get_db
from .intake_engine import build_pre_assessment
from .intake_models import AssessmentIntakeContext
from .intake_schemas import AssessmentIntakeCreate, AssessmentIntakeOut
from .models import Assessment, AssessmentProfile
from .schemas import AssessmentOut, RelevanceProfile

router = APIRouter(prefix="/api", tags=["assessment-intake"])


def _as_assessment(model: Assessment) -> AssessmentOut:
    return AssessmentOut.model_validate(model)


def _workload_type_for_legacy(primary_archetype: str) -> str:
    mapping = {
        "business-application": "application",
        "saas": "saas",
        "cloud-platform": "cloud-platform",
        "ai-system": "ai-system",
        "ai-agent": "ai-agent",
        "infrastructure-compute": "infrastructure",
    }
    return mapping.get(primary_archetype, "other")


@router.post("/assessment-intakes", response_model=AssessmentIntakeOut, status_code=201)
def create_assessment_intake(payload: AssessmentIntakeCreate, db: Session = Depends(get_db)):
    pre = build_pre_assessment(payload)
    row = Assessment(
        id=str(uuid.uuid4()),
        name=payload.decision_case.title,
        customer=payload.organization.name,
        description=payload.workload.description,
        workload_type=_workload_type_for_legacy(payload.workload.primary_archetype),
        criticality="unknown",
        confidentiality="unknown",
        integrity="unknown",
        availability="unknown",
        control_region="unknown",
        regulatory_context="",
    )
    db.add(row)
    db.flush()

    assessment_payload = _as_assessment(row).model_dump()
    profile_values = default_profile(assessment_payload)
    profile_values["ai_used"] = payload.workload.ai_used == "yes" or payload.workload.primary_archetype in {"ai-system", "ai-agent"}
    profile_values["agentic_ai"] = payload.workload.primary_archetype == "ai-agent" or "agentic" in payload.workload.tags
    profile_values["multi_provider"] = payload.workload.current_operating_model == "multi-cloud" or "multi_provider" in payload.workload.tags
    profile_values["internet_exposed"] = "internet_exposed" in payload.workload.tags
    profile_values["cloud_service"] = payload.workload.current_operating_model in {"public-cloud", "saas", "hybrid", "multi-cloud"}
    profile = RelevanceProfile(**profile_values)
    db.add(AssessmentProfile(assessment_id=row.id, profile_json=profile.model_dump_json()))

    db.add(AssessmentIntakeContext(
        assessment_id=row.id,
        context_json=payload.model_dump_json(),
        pre_assessment_json=pre.model_dump_json(),
    ))
    db.commit()
    return AssessmentIntakeOut(
        assessment_id=row.id,
        decision_case=payload.decision_case,
        organization=payload.organization,
        workload=payload.workload,
        pre_assessment=pre,
    )


@router.get("/assessments/{assessment_id}/intake", response_model=AssessmentIntakeOut)
def get_assessment_intake(assessment_id: str, db: Session = Depends(get_db)):
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    row = db.get(AssessmentIntakeContext, assessment_id)
    if not row:
        raise HTTPException(404, "Assessment intake not found")
    context = json.loads(row.context_json)
    pre = json.loads(row.pre_assessment_json)
    return AssessmentIntakeOut(assessment_id=assessment_id, **context, pre_assessment=pre)
