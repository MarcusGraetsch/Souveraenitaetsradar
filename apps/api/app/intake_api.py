from __future__ import annotations

import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sovradar.applicability import default_profile

from .database import get_db
from .intake_models import AssessmentIntake
from .intake_rules import derive_pre_assessment
from .intake_schemas import (
    AssessmentIntakeCreate,
    AssessmentIntakeCreateResult,
    AssessmentIntakeStored,
)
from .models import Assessment, AssessmentProfile
from .schemas import AssessmentOut, RelevanceProfile

router = APIRouter()
INTAKE_SCHEMA_VERSION = "0.5"


def _normalize(payload: AssessmentIntakeCreate) -> AssessmentIntakeCreate:
    normalized = payload.model_copy(deep=True)
    org = normalized.organization
    org.country_code = org.country_code.strip().upper()
    org.activity_countries = [item.strip().upper() for item in org.activity_countries if item.strip()]
    org.primary_legal_entity.country_code = org.primary_legal_entity.country_code.strip().upper()
    for entity in org.additional_legal_entities:
        entity.country_code = entity.country_code.strip().upper()
    normalized.workload.usage_countries = [
        item.strip().upper() for item in normalized.workload.usage_countries if item.strip()
    ]
    normalized.workload.tags = sorted(
        {item.strip().lower() for item in normalized.workload.tags if item.strip()}
    )
    return normalized


def _assessment_out(row: Assessment) -> AssessmentOut:
    return AssessmentOut.model_validate(row)


def _profile_from_intake(assessment: Assessment, payload: AssessmentIntakeCreate) -> RelevanceProfile:
    values = default_profile(_assessment_out(assessment).model_dump())
    workload = payload.workload

    def tri(value: str) -> bool | None:
        if value == "yes":
            return True
        if value == "no":
            return False
        return None

    values["ai_used"] = tri(workload.ai_used)
    if workload.primary_archetype == "ai-agent" or "agentic" in workload.tags:
        values["agentic_ai"] = True
    elif workload.ai_used == "no":
        values["agentic_ai"] = False
    else:
        values["agentic_ai"] = None
    values["cloud_service"] = tri(workload.external_cloud_or_saas)
    if workload.personal_data == "yes" or workload.sensitive_business_or_domain_data == "yes":
        values["data_processing"] = True
    elif workload.personal_data == "no" and workload.sensitive_business_or_domain_data == "no":
        values["data_processing"] = False
    else:
        values["data_processing"] = None
    values["multi_provider"] = (
        True if workload.current_operating_model == "multi-cloud" or "multi_provider" in workload.tags else None
    )
    values["contract_in_scope"] = True if workload.external_cloud_or_saas == "yes" else None
    if workload.current_operating_model == "saas":
        values["service_model"] = "saas"
    elif workload.current_operating_model == "on-prem":
        values["service_model"] = "on-prem"
    else:
        values["service_model"] = "unknown"
    return RelevanceProfile(**values)


def _stored(row: AssessmentIntake) -> AssessmentIntakeStored:
    intake = json.loads(row.intake_json)
    pre = json.loads(row.pre_assessment_json)
    return AssessmentIntakeStored(
        assessment_id=row.assessment_id,
        schema_version=row.schema_version,
        decision_case=intake["decision_case"],
        organization=intake["organization"],
        workload=intake["workload"],
        pre_assessment=pre,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


@router.post("/api/intake/assessments", response_model=AssessmentIntakeCreateResult, status_code=201)
def create_assessment_from_intake(
    payload: AssessmentIntakeCreate,
    db: Session = Depends(get_db),
):
    payload = _normalize(payload)
    pre_assessment = derive_pre_assessment(payload)

    assessment = Assessment(
        id=str(uuid.uuid4()),
        name=payload.decision_case.title,
        customer=payload.organization.name,
        description=payload.workload.description,
        workload_type=payload.workload.primary_archetype,
        criticality="unreviewed",
        confidentiality="unreviewed",
        integrity="unreviewed",
        availability="unreviewed",
        control_region="unreviewed",
        regulatory_context="",
        status="draft",
    )
    db.add(assessment)
    db.flush()

    profile = _profile_from_intake(assessment, payload)
    db.add(
        AssessmentProfile(
            assessment_id=assessment.id,
            profile_json=profile.model_dump_json(),
        )
    )
    intake_row = AssessmentIntake(
        assessment_id=assessment.id,
        schema_version=INTAKE_SCHEMA_VERSION,
        intake_json=payload.model_dump_json(),
        pre_assessment_json=pre_assessment.model_dump_json(),
    )
    db.add(intake_row)
    db.commit()
    db.refresh(assessment)
    db.refresh(intake_row)

    return AssessmentIntakeCreateResult(
        assessment=_assessment_out(assessment).model_dump(mode="json"),
        intake=_stored(intake_row),
    )


@router.get("/api/assessments/{assessment_id}/intake", response_model=AssessmentIntakeStored)
def get_assessment_intake(assessment_id: str, db: Session = Depends(get_db)):
    if not db.get(Assessment, assessment_id):
        raise HTTPException(404, "Assessment not found")
    row = db.get(AssessmentIntake, assessment_id)
    if row is None:
        raise HTTPException(404, "Structured intake not available for this legacy assessment")
    return _stored(row)
