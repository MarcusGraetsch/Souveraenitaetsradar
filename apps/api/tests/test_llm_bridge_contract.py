from __future__ import annotations

import pytest
from pydantic import ValidationError

from apps.api.app.llm_bridge import build_prompt
from apps.api.app.schemas import LlmBridgeResult


def test_prompt_embeds_exact_assessment_id_and_evidence_contract() -> None:
    assessment_id = "44a70bdf-7d68-40f6-8243-6b6abff2001a"
    prompt = build_prompt(
        {
            "id": assessment_id,
            "name": "Pilot",
            "customer": "Musterbehörde",
            "workload_type": "ai-agent",
            "description": "Geplanter KI-Agent",
            "criticality": "high",
            "confidentiality": "high",
            "integrity": "high",
            "availability": "medium",
            "control_region": "Deutschland/EU",
            "regulatory_context": "DSGVO",
        },
        answers=[],
        evidence=[
            {
                "id": "ev-123",
                "title": "Kundenaussage",
                "evidence_type": "customer-statement",
                "source": "Workshop",
                "source_date": "2026-09-04",
                "description": "INTERNAL-DESCRIPTION-MUST-NOT-LEAK",
                "content_excerpt": "Es sollen Audio-Interviews geführt werden.",
            }
        ],
        questions=[
            {
                "id": "DK-01",
                "domain": "Daten",
                "question": "Welche Datenklassen werden verarbeitet?",
                "applicability_status": "applicable",
                "applicability_reason": "immer",
                "expected_evidence": "Dateninventar",
            }
        ],
        profile={"ai_used": True},
    )

    assert f'Assessment-ID: {assessment_id}' in prompt
    assert f'"assessment_id": "{assessment_id}"' in prompt
    assert "OPAQUE IDENTIFIERS" in prompt
    assert "Jedes Proposal MUSS mindestens eine" in prompt
    assert "geplant/gewünscht/behauptet ist nicht implementiert/beobachtet/getestet" in prompt
    assert "Es sollen Audio-Interviews geführt werden." in prompt
    assert "INTERNAL-DESCRIPTION-MUST-NOT-LEAK" not in prompt
    assert "Interne Evidence-Beschreibung: [nicht an LLM freigegeben]" in prompt


def test_prompt_with_no_approved_excerpt_does_not_leak_internal_description() -> None:
    prompt = build_prompt(
        {
            "id": "assessment-1",
            "name": "Pilot",
            "customer": "Musterbehörde",
            "workload_type": "ai-agent",
            "description": "Geplanter KI-Agent",
            "criticality": "high",
            "confidentiality": "high",
            "integrity": "high",
            "availability": "medium",
            "control_region": "Deutschland/EU",
            "regulatory_context": "DSGVO",
        },
        answers=[],
        evidence=[
            {
                "id": "ev-456",
                "title": "Interne Notiz",
                "evidence_type": "customer-statement",
                "source": "Workshop",
                "source_date": "2026-09-04",
                "description": "SENSITIVE-INTERNAL-NOTE",
                "content_excerpt": "",
            }
        ],
        questions=[],
        profile={},
    )

    assert "SENSITIVE-INTERNAL-NOTE" not in prompt
    assert "Freigegebener Auszug: [kein Textauszug für LLM freigegeben]" in prompt


def test_llm_answer_proposal_requires_evidence_reference() -> None:
    with pytest.raises(ValidationError):
        LlmBridgeResult.model_validate(
            {
                "assessment_id": "assessment-1",
                "proposals": [
                    {
                        "question_id": "SC-05",
                        "proposed_answer": "high/high/medium",
                        "rationale": "Nur aus dem Assessment-Header abgeleitet.",
                        "evidence_ids": [],
                        "confidence": 1.0,
                    }
                ],
                "evidence_gaps": [],
                "warnings": [],
            }
        )
