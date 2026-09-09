from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

TriState = Literal["yes", "no", "unknown"]
ComplianceStatus = Literal["likely_applicable", "likely_not_applicable", "needs_review"]
ReviewStatus = Literal["not_reviewed", "human_confirmed", "human_rejected"]

OrganizationType = Literal[
    "private-company",
    "public-authority",
    "public-body",
    "nonprofit",
    "education-research",
    "other",
]

OrganizationSize = Literal["micro", "small", "medium", "large", "public-sector", "unknown"]

WorkloadArchetype = Literal[
    "business-application",
    "saas",
    "data-platform",
    "api-integration",
    "cloud-platform",
    "ai-system",
    "ai-agent",
    "devops-platform",
    "iam-service",
    "database-storage",
    "infrastructure",
    "collaboration",
    "ot-iot-edge",
    "other",
]

OperatingModel = Literal[
    "on-prem",
    "private-cloud",
    "public-cloud",
    "saas",
    "hybrid",
    "multi-cloud",
    "open",
    "unknown",
]

AiRole = Literal["provider", "deployer", "integrator", "third-party-service", "unknown", "none"]


class DecisionCaseIntake(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    goal: str = Field(min_length=5, max_length=4000)
    project_reference: str = Field(default="", max_length=255)
    consultant_owner: str = Field(default="", max_length=255)
    target_decision_date: str = Field(default="", max_length=32)


class LegalEntityIntake(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    country_code: str = Field(min_length=2, max_length=2)
    city: str = Field(default="", max_length=255)
    role: Literal[
        "workload-owner",
        "operator",
        "contracting-party",
        "data-controller",
        "data-processor",
        "user-entity",
        "other",
    ] = "workload-owner"


class OrganizationIntake(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    organization_type: OrganizationType
    country_code: str = Field(min_length=2, max_length=2)
    postal_code: str = Field(default="", max_length=32)
    city: str = Field(min_length=1, max_length=255)
    sector: str = Field(min_length=2, max_length=128)
    size_class: OrganizationSize
    employee_count: int | None = Field(default=None, ge=0)
    annual_turnover_eur_million: float | None = Field(default=None, ge=0)
    balance_sheet_eur_million: float | None = Field(default=None, ge=0)
    group_structure: TriState = "unknown"
    activity_countries: list[str] = Field(default_factory=list, max_length=100)
    primary_legal_entity: LegalEntityIntake
    additional_legal_entities: list[LegalEntityIntake] = Field(default_factory=list, max_length=50)


class WorkloadIntake(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    description: str = Field(min_length=10, max_length=12000)
    primary_archetype: WorkloadArchetype
    tags: list[str] = Field(default_factory=list, max_length=50)
    usage_countries: list[str] = Field(default_factory=list, max_length=100)
    personal_data: TriState = "unknown"
    sensitive_business_or_domain_data: TriState = "unknown"
    ai_used: TriState = "unknown"
    ai_role: AiRole = "unknown"
    external_cloud_or_saas: TriState = "unknown"
    current_operating_model: OperatingModel = "unknown"


class AssessmentIntakeCreate(BaseModel):
    decision_case: DecisionCaseIntake
    organization: OrganizationIntake
    workload: WorkloadIntake


class ComplianceCandidate(BaseModel):
    framework: Literal["DSGVO", "NIS2", "DORA", "AI Act"]
    candidate_status: ComplianceStatus
    rationale: list[str] = Field(default_factory=list)
    missing_facts: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    review_status: ReviewStatus = "not_reviewed"


class PreAssessmentContext(BaseModel):
    classification_suggestions: list[str] = Field(default_factory=list)
    compliance_candidates: list[ComplianceCandidate] = Field(default_factory=list)
    missing_facts: list[str] = Field(default_factory=list)
    suggested_deep_dives: list[str] = Field(default_factory=list)
    screening_target: str = "15-25 Kernfragen"
    warnings: list[str] = Field(default_factory=list)


class AssessmentIntakeStored(BaseModel):
    assessment_id: str
    schema_version: str
    decision_case: DecisionCaseIntake
    organization: OrganizationIntake
    workload: WorkloadIntake
    pre_assessment: PreAssessmentContext
    created_at: datetime
    updated_at: datetime


class AssessmentIntakeCreateResult(BaseModel):
    assessment: dict
    intake: AssessmentIntakeStored
