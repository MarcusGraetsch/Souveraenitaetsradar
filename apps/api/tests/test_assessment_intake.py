from __future__ import annotations

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from apps.api.app.database import Base
from apps.api.app.intake_api import create_assessment_intake
from apps.api.app.intake_models import AssessmentIntakeContext
from apps.api.app.intake_schemas import AssessmentIntakeCreate
from apps.api.app.models import Assessment


def _payload() -> AssessmentIntakeCreate:
    return AssessmentIntakeCreate.model_validate({
        "decision_case": {
            "title": "Betriebsmodell KI-Assistent Bürgerdienste",
            "objective": "Welche Betriebsvariante bietet ausreichende Souveränität?",
        },
        "organization": {
            "name": "Beispielstadt",
            "organization_type": "public_authority",
            "sector": "Öffentliche Verwaltung",
            "employee_size": "large",
            "headquarters_country": "Deutschland",
            "headquarters_city": "Berlin",
            "activity_countries": ["Deutschland", "Frankreich"],
            "group_structure": "yes",
            "legal_entities": [
                {"name": "Beispielstadt", "country": "Deutschland", "city": "Berlin", "role": "primary"},
                {"name": "Service-Tochter", "country": "Frankreich", "city": "Paris", "role": "operator"},
            ],
        },
        "workload": {
            "name": "KI-Assistent",
            "description": "Agentischer Assistent mit Zugriff auf interne Fachdaten und Fachsysteme.",
            "primary_archetype": "ai-agent",
            "tags": ["agentic", "identity_critical"],
            "personal_data": "yes",
            "sensitive_business_data": "yes",
            "ai_used": "yes",
            "ai_role": "deployer",
            "external_provider_in_scope": "yes",
            "current_operating_model": "public-cloud",
            "user_countries": ["Deutschland", "Frankreich"],
        },
    })


def test_preassessment_is_suggestive_not_final() -> None:
    from apps.api.app.intake_engine import build_pre_assessment

    pre = build_pre_assessment(_payload())
    candidates = {candidate.framework: candidate for candidate in pre.compliance_candidates}

    assert candidates["GDPR"].candidate_status == "likely_applicable"
    assert candidates["NIS2"].candidate_status == "likely_applicable"
    assert candidates["AI_ACT"].candidate_status == "needs_review"
    assert all(candidate.review_status == "not_reviewed" for candidate in candidates.values())
    assert all("keine Rechtsfeststellung" in candidate.disclaimer for candidate in candidates.values())
    assert pre.cia_status == "unassessed"
    assert pre.criticality_status == "unassessed"
    assert "C3A / Cloud-Autonomie" in pre.suggested_deep_dive_profiles
    assert pre.jurisdiction_complexity


def test_create_intake_persists_structured_context_without_fake_cia_defaults() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db:
        result = create_assessment_intake(_payload(), db)
        assessment = db.get(Assessment, result.assessment_id)
        intake = db.get(AssessmentIntakeContext, result.assessment_id)

        assert assessment is not None
        assert assessment.name == "Betriebsmodell KI-Assistent Bürgerdienste"
        assert assessment.customer == "Beispielstadt"
        assert assessment.criticality == "unknown"
        assert assessment.confidentiality == "unknown"
        assert assessment.integrity == "unknown"
        assert assessment.availability == "unknown"
        assert intake is not None
        assert intake.schema_version == "0.5"
        assert len(result.organization.legal_entities) == 2
        assert result.workload.primary_archetype == "ai-agent"
        assert db.scalar(select(Assessment).where(Assessment.id == result.assessment_id)) is not None
