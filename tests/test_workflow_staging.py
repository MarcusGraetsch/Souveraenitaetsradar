from __future__ import annotations

import csv
from pathlib import Path

from sovradar.applicability import apply_to_questions

ROOT = Path(__file__).resolve().parents[1]
QUESTION_BANK = ROOT / "data" / "method" / "question_bank"


def load_questions() -> list[dict[str, str]]:
    questions: list[dict[str, str]] = []
    for path in sorted(QUESTION_BANK.glob("*.csv")):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle, delimiter=";"):
                if not row.get("QID"):
                    continue
                questions.append(
                    {
                        "id": row.get("QID", ""),
                        "domain": row.get("Domäne", ""),
                        "applicability": row.get("Anwendbarkeit", ""),
                        "requiredness": row.get("Pflichtgrad", ""),
                    }
                )
    return questions


def complex_ai_agent() -> tuple[dict, dict]:
    assessment = {
        "workload_type": "ai-agent",
        "criticality": "high",
        "confidentiality": "high",
        "integrity": "high",
        "availability": "medium",
    }
    profile = {
        "service_model": "managed-service",
        "cloud_service": True,
        "contract_in_scope": True,
        "data_processing": True,
        "persistent_data": True,
        "encryption_used": True,
        "key_model": "mixed",
        "ai_used": True,
        "agentic_ai": True,
        "exit_relevant": True,
        "backup_relevant": True,
        "multi_provider": False,
        "subcontractors_used": True,
        "c5_relevant": True,
        "c3a_relevant": True,
        "iam_relevant": True,
        "logging_relevant": True,
        "internet_exposed": True,
    }
    return assessment, profile


def simple_public_content() -> tuple[dict, dict]:
    assessment = {
        "workload_type": "application",
        "criticality": "medium",
        "confidentiality": "low",
        "integrity": "medium",
        "availability": "medium",
    }
    profile = {
        "service_model": "other",
        "cloud_service": False,
        "contract_in_scope": False,
        "data_processing": False,
        "persistent_data": False,
        "encryption_used": False,
        "key_model": "none",
        "ai_used": False,
        "agentic_ai": False,
        "exit_relevant": False,
        "backup_relevant": False,
        "multi_provider": False,
        "subcontractors_used": False,
        "c5_relevant": False,
        "c3a_relevant": False,
        "iam_relevant": False,
        "logging_relevant": False,
        "internet_exposed": True,
    }
    return assessment, profile


def count_stage(rows: list[dict], stage: str) -> int:
    return sum(row["workflow_stage"] == stage for row in rows)


def test_next_114_baseline_is_preserved_but_progressively_staged():
    questions = load_questions()
    assessment, profile = complex_ai_agent()
    rows = apply_to_questions(questions, assessment, profile)

    assert len(rows) == 128
    assert sum(row["applicability_status"] == "applicable" for row in rows) == 83
    assert sum(row["applicability_status"] == "needs_review" for row in rows) == 41
    assert sum(row["applicability_status"] == "not_applicable" for row in rows) == 4

    assert count_stage(rows, "clarification") == 41
    assert count_stage(rows, "screening") > 0
    assert count_stage(rows, "deep_dive") > 0
    assert count_stage(rows, "excluded") == 4

    relevant = 128 - count_stage(rows, "excluded")
    immediate_work = count_stage(rows, "screening") + count_stage(rows, "clarification")
    assert relevant == 124
    assert immediate_work < relevant


def test_needs_review_is_never_hidden_by_staging():
    assessment, profile = complex_ai_agent()
    rows = apply_to_questions(load_questions(), assessment, profile)
    unresolved = [row for row in rows if row["applicability_status"] == "needs_review"]
    assert unresolved
    assert all(row["workflow_stage"] == "clarification" for row in unresolved)


def test_simple_public_content_workload_is_materially_shorter_than_complex_ai_agent():
    questions = load_questions()
    complex_assessment, complex_profile = complex_ai_agent()
    public_assessment, public_profile = simple_public_content()

    complex_rows = apply_to_questions(questions, complex_assessment, complex_profile)
    public_rows = apply_to_questions(questions, public_assessment, public_profile)

    complex_relevant = sum(row["workflow_stage"] != "excluded" for row in complex_rows)
    public_relevant = sum(row["workflow_stage"] != "excluded" for row in public_rows)
    complex_work = sum(row["workflow_stage"] in {"screening", "clarification"} for row in complex_rows)
    public_work = sum(row["workflow_stage"] in {"screening", "clarification"} for row in public_rows)

    assert public_relevant < complex_relevant
    assert public_work < complex_work
