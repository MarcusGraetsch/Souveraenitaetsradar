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
    evidence_ids: list[str] = Field(default_factory=list)
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


class EvidenceReviewUpsert(BaseModel):
    applied_state: Literal["asserted", "available", "documented", "observed", "configured", "tested", "attested"] = "asserted"
    base_trust: int = Field(default=0, ge=0, le=5)
    scope_fit: int = Field(default=0, ge=0, le=5)
    freshness_fit: int = Field(default=0, ge=0, le=5)
    review_status: Literal["raw", "normalized", "reviewed", "approved", "rejected"] = "raw"


class EvidenceReviewOut(EvidenceReviewUpsert):
    evidence_id: str
    assessment_id: str
    effective_trust: int
    updated_at: datetime


class ClaimCreate(BaseModel):
    gate_id: str = Field(pattern=r"^HG-0[1-8]$")
    statement: str = Field(min_length=1)
    review_status: Literal["draft", "reviewed", "approved", "rejected"] = "draft"
    capability_level: int | None = Field(default=None, ge=0, le=4)
    evidence_ids: list[str] = Field(default_factory=list)
    question_ids: list[str] = Field(default_factory=list)
    notes: str = ""


class ClaimOut(ClaimCreate):
    id: str
    assessment_id: str
    created_at: datetime
    updated_at: datetime


class GateRequirementUpsert(BaseModel):
    requirement_level: int = Field(ge=0, le=4)


class GateRequirementOut(BaseModel):
    assessment_id: str
    gate_id: str
    requirement_level: int
    source: str
    updated_at: datetime | None = None


class EvidenceRequestOut(BaseModel):
    request_id: str
    gate_id: str
    claim_area: str
    acceptable_evidence: str
    required_for: str
    follow_up: str
    preferred_applied_state: str
    typical_min_trust: str
    provenance: str


class GateDefinitionOut(BaseModel):
    gate_id: str
    name: str
    subject: str
    requirement_templates: dict[str, int]
    source_ids: list[str]
    provenance: str
    evidence_requests: list[EvidenceRequestOut] = Field(default_factory=list)


class GateEvaluationOut(BaseModel):
    gate_id: str
    name: str
    subject: str
    requirement_level: int
    requirement_source: str
    capability_level: int | None
    effective_trust: int | None
    technical_state: Literal["PASS", "FAIL", "UNVERIFIED", "N/A"]
    evidence_state: Literal["VERIFIED", "UNVERIFIED", "N/A"]
    final_state: Literal["PASS", "FAIL", "UNVERIFIED", "N/A"]
    claim_ids: list[str]
    evidence_ids: list[str]
    reasons: list[str]
    evidence_requests: list[EvidenceRequestOut] = Field(default_factory=list)


class LlmProposal(BaseModel):
    question_id: str
    proposed_answer: str
    rationale: str
    evidence_ids: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


class LlmGap(BaseModel):
    question_id: str
    missing: str


class LlmBridgeResult(BaseModel):
    assessment_id: str
    proposals: list[LlmProposal] = Field(default_factory=list)
    evidence_gaps: list[LlmGap] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class LlmImportOut(BaseModel):
    id: str
    assessment_id: str
    validation_status: str
    proposals: list[LlmProposal]
    evidence_gaps: list[LlmGap]
    warnings: list[str]
    created_at: datetime
