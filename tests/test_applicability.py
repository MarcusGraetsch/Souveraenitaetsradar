from sovradar.applicability import (
    ApplicabilityStatus,
    WorkflowStage,
    apply_to_questions,
    default_profile,
    evaluate_applicability,
    evaluate_workflow_stage,
)


def assessment(**overrides):
    base = {
        "workload_type": "saas",
        "criticality": "medium",
        "confidentiality": "medium",
        "integrity": "medium",
        "availability": "medium",
    }
    base.update(overrides)
    return base


def test_unknown_context_never_silently_filters_question():
    result = evaluate_applicability(
        "wenn Verschlüsselung",
        assessment(),
        {"encryption_used": None},
    )
    assert result.status is ApplicabilityStatus.NEEDS_REVIEW


def test_explicit_false_condition_can_filter_question():
    result = evaluate_applicability(
        "wenn Verschlüsselung",
        assessment(),
        {"encryption_used": False},
    )
    assert result.status is ApplicabilityStatus.NOT_APPLICABLE


def test_ai_agent_activates_agentic_question():
    current = assessment(workload_type="ai-agent")
    result = evaluate_applicability(
        "wenn generative KI/Agenten",
        current,
        default_profile(current),
    )
    assert result.status is ApplicabilityStatus.APPLICABLE


def test_non_ai_workload_filters_agentic_question():
    current = assessment(workload_type="saas")
    result = evaluate_applicability(
        "wenn generative KI/Agenten",
        current,
        default_profile(current),
    )
    assert result.status is ApplicabilityStatus.NOT_APPLICABLE


def test_high_confidentiality_rule_is_deterministic():
    high = evaluate_applicability(
        "wenn Vertraulichkeit hoch/sehr hoch",
        assessment(confidentiality="high"),
        {},
    )
    low = evaluate_applicability(
        "wenn Vertraulichkeit hoch/sehr hoch",
        assessment(confidentiality="low"),
        {},
    )
    assert high.status is ApplicabilityStatus.APPLICABLE
    assert low.status is ApplicabilityStatus.NOT_APPLICABLE


def test_public_site_and_sensitive_ai_agent_have_different_paths():
    questions = [
        {"id": "Q1", "applicability": "immer", "requiredness": "Basis", "domain": "Scope"},
        {"id": "Q2", "applicability": "wenn generative KI/Agenten", "requiredness": "Bedingt", "domain": "KI"},
        {"id": "Q3", "applicability": "wenn Vertraulichkeit hoch/sehr hoch", "requiredness": "Bedingt", "domain": "Daten"},
        {"id": "Q4", "applicability": "wenn Exit relevant", "requiredness": "Bedingt", "domain": "Exit"},
    ]
    public = assessment(
        workload_type="application",
        confidentiality="low",
        criticality="medium",
    )
    public_profile = {
        **default_profile(public),
        "exit_relevant": False,
    }
    ai = assessment(
        workload_type="ai-agent",
        confidentiality="high",
        criticality="high",
    )
    ai_profile = {
        **default_profile(ai),
        "exit_relevant": True,
    }

    public_path = apply_to_questions(questions, public, public_profile)
    ai_path = apply_to_questions(questions, ai, ai_profile)

    public_active = {
        q["id"] for q in public_path if q["applicability_status"] != "not_applicable"
    }
    ai_active = {
        q["id"] for q in ai_path if q["applicability_status"] != "not_applicable"
    }

    assert public_active == {"Q1"}
    assert ai_active == {"Q1", "Q2", "Q3", "Q4"}


def test_needs_review_is_explicit_clarification_not_excluded():
    question = {"id": "Q1", "domain": "Daten", "requiredness": "Bedingt"}
    applicability = evaluate_applicability(
        "wenn Verschlüsselung",
        assessment(),
        {"encryption_used": None},
    )
    stage = evaluate_workflow_stage(question, applicability)
    assert stage.stage is WorkflowStage.CLARIFICATION


def test_basis_applicable_question_is_screening():
    question = {"id": "Q1", "domain": "Governance", "requiredness": "Basis"}
    applicability = evaluate_applicability("immer", assessment(), {})
    stage = evaluate_workflow_stage(question, applicability)
    assert stage.stage is WorkflowStage.SCREENING


def test_conditional_applicable_question_is_deep_dive():
    question = {"id": "Q1", "domain": "Exit", "requiredness": "Bedingt"}
    applicability = evaluate_applicability(
        "wenn Exit relevant",
        assessment(),
        {"exit_relevant": True},
    )
    stage = evaluate_workflow_stage(question, applicability)
    assert stage.stage is WorkflowStage.DEEP_DIVE


def test_answered_question_moves_to_completed_without_changing_applicability():
    questions = [
        {"id": "Q1", "applicability": "immer", "requiredness": "Basis", "domain": "Scope"},
    ]
    result = apply_to_questions(
        questions,
        assessment(),
        {},
        answered_question_ids={"Q1"},
    )[0]
    assert result["applicability_status"] == "applicable"
    assert result["workflow_stage"] == "completed"


def test_not_applicable_question_is_excluded_but_remains_in_result():
    questions = [
        {"id": "Q1", "applicability": "wenn generative KI/Agenten", "requiredness": "Bedingt", "domain": "KI"},
    ]
    result = apply_to_questions(
        questions,
        assessment(workload_type="application"),
        default_profile(assessment(workload_type="application")),
    )[0]
    assert result["applicability_status"] == "not_applicable"
    assert result["workflow_stage"] == "excluded"
