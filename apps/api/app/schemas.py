from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class AssessmentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    customer: str = ""
    description: str = ""
    workload_type: str = "other"
    criticality: str = "medium"
    confidentiality: str = "medium"
    integrity: str = "medium"
    availability: str = "medium"
    control_region: str = "EU/EWR"
    regulatory_context: str = ""


class AssessmentOut(AssessmentCreate):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RelevanceProfile(BaseModel):
    service_model: Literal["unknown", "saas", "paas", "iaas", "managed-service", "on-prem", "other"] = "unknown"
    cloud_service: bool | None = None
    contract_in_scope: bool | None = None
    data_processing: bool | None = None
    persistent_data: bool | None = None
    encryption_used: bool | None = None
    key_model: Literal["unknown", "customer", "provider", "external", "mixed", "none"] = "unknown"
    ai_used: bool | None = None
    agentic_ai: bool | None = None
    exit_relevant: bool | None = None
    backup_relevant: bool | None = None
    multi_provider: bool | None = None
    subcontractors_used: bool | None = None
    c5_relevant: bool | None = None
    c3a_relevant: bool | None = None
    iam_relevant: bool | None = None
    logging_relevant: bool | None = None
    internet_exposed: bool | None = None


class RelevanceProfileOut(RelevanceProfile):
    assessment_id: str
    updated_at: datetime | None = None


class AnswerUpsert(BaseModel):
    question_id: str
    answer_value: str = ""
    comment: str = ""
    evidence_ids: list[str] = []
    review_state: Literal["draft", "reviewed"] = "draft"


class AnswerOut(AnswerUpsert):
    id: str
    assessment_id: str
    updated_at: datetime


class EvidenceCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    evidence_type: str = "other"
    description: str = ""
    source: str = ""
    source_date: str = ""
    content_excerpt: str = ""


class EvidenceOut(EvidenceCreate):
    id: str
    assessment_id: str
    file_name: str
    created_at: datetime


class LlmProposal(BaseModel):
    question_id: str
    proposed_answer: str
    rationale: str
    evidence_ids: list[str] = []
    confidence: float = Field(ge=0, le=1)


class LlmGap(BaseModel):
    question_id: str
    missing: str


class LlmBridgeResult(BaseModel):
    assessment_id: str
    proposals: list[LlmProposal] = []
    evidence_gaps: list[LlmGap] = []
    warnings: list[str] = []


class LlmImportOut(BaseModel):
    id: str
    assessment_id: str
    validation_status: str
    proposals: list[LlmProposal]
    evidence_gaps: list[LlmGap]
    warnings: list[str]
    created_at: datetime
