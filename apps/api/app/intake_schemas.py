from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


TriState = Literal["yes", "no", "unknown"]
CandidateStatus = Literal["likely_applicable", "likely_not_applicable", "needs_review"]
ReviewStatus = Literal["not_reviewed", "human_confirmed", "human_rejected"]


class DecisionCaseInput(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    objective: str = Field(min_length=1)
    project_reference: str = ""
    consultant_owner: str = ""
    target_decision_date: str = ""


class LegalEntityInput(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    country: str = Field(min_length=2, max_length=128)
    city: str = ""
    postal_code: str = ""
    role: Literal[
        "primary",
        "workload_owner",
        "operator",
        "contracting_party",
        "data_controller",
        "user_group",
        "other",
    ] = "other"


class OrganizationInput(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    organization_type: Literal[
        "company", "public_authority", "public_body", "non_profit", "other"
    ]
    sector: str = Field(min_length=1, max_length=255)
    employee_size: Literal["micro", "small", "medium", "large", "unknown"]
    headquarters_country: str = Field(min_length=2, max_length=128)
    headquarters_city: str = ""
    headquarters_postal_code: str = ""
    headquarters_street: str = ""
    activity_countries: list[str] = Field(default_factory=list)
    group_structure: TriState = "unknown"
    annual_revenue_eur: str = ""
    balance_sheet_eur: str = ""
    legal_entities: list[LegalEntityInput] = Field(min_length=1)


class WorkloadInput(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    primary_archetype: Literal[
        "business-application",
        "saas",
        "data-analytics",
        "integration-api",
        "cloud-platform",
        "ai-system",
        "ai-agent",
        "devops-platform",
        "iam-trust",
        "database-storage",
        "infrastructure-compute",
        "collaboration",
        "ot-iot-edge",
        "other",
    ]
    tags: list[str] = Field(default_factory=list)
    personal_data: TriState = "unknown"
    sensitive_business_data: TriState = "unknown"
    ai_used: TriState = "unknown"
    ai_role: Literal["provider", "deployer", "third_party_service", "unknown", "not_applicable"] = "unknown"
    external_provider_in_scope: TriState = "unknown"
    current_operating_model: Literal[
        "on-prem",
        "private-cloud",
        "public-cloud",
        "saas",
        "hybrid",
        "multi-cloud",
        "open",
        "unknown",
    ] = "unknown"
    user_countries: list[str] = Field(default_factory=list)
    legal_entity_names: list[str] = Field(default_factory=list)


class AssessmentIntakeCreate(BaseModel):
    decision_case: DecisionCaseInput
    organization: OrganizationInput
    workload: WorkloadInput


class ComplianceCandidate(BaseModel):
    framework: Literal["GDPR", "NIS2", "DORA", "AI_ACT"]
    candidate_status: CandidateStatus
    rationale: list[str]
    missing_facts: list[str] = Field(default_factory=list)
    source_refs: list[str]
    review_status: ReviewStatus = "not_reviewed"
    disclaimer: str = "Vorläufige Routing-Hilfe; keine Rechtsfeststellung. Relevante Schlussfolgerungen benötigen HITL-04."


class PreAssessmentContext(BaseModel):
    workload_tags: list[str]
    compliance_candidates: list[ComplianceCandidate]
    missing_scope_facts: list[str]
    suggested_deep_dive_profiles: list[str]
    suggested_screening_focus: list[str]
    jurisdiction_complexity: list[str]
    criticality_status: Literal["unassessed"] = "unassessed"
    cia_status: Literal["unassessed"] = "unassessed"


class AssessmentIntakeOut(BaseModel):
    assessment_id: str
    decision_case: DecisionCaseInput
    organization: OrganizationInput
    workload: WorkloadInput
    pre_assessment: PreAssessmentContext
