from __future__ import annotations

import csv
import os
import tempfile
from pathlib import Path

ROOT = Path(tempfile.mkdtemp(prefix="sovradar-api-test-"))
METHOD_DIR = ROOT / "method" / "question_bank"
METHOD_DIR.mkdir(parents=True)
with (METHOD_DIR / "test.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle, delimiter=";")
    writer.writerow([
        "QID", "Domäne", "Zielobjekt", "Frage", "Antworttyp", "Anwendbarkeit",
        "Fragentyp", "Pflichtgrad", "Erwartete Evidenz", "Min. Trust",
        "Risiko-IDs", "SOV-Bezug", "Framework / Regulatorik", "Source IDs",
        "Follow-up / Entscheidungslogik", "Scoring-Rolle", "Provenienztyp",
        "Fundstelle / Herleitung", "Herleitungsnotiz",
    ])
    writer.writerow([
        "DK-03", "Daten", "Key", "Wer kontrolliert Schlüssel?", "Text", "immer",
        "Fakt", "Basis", "KMS-Konzept", "3", "G z.S8", "SOV-3", "", "INT-01",
        "", "Exposure", "internal-method", "", "",
    ])
    writer.writerow([
        "KI-01", "Daten", "AI", "Welche Agenten-Tools werden verwendet?", "Text",
        "wenn generative KI/Agenten", "Fakt", "Bedingt", "Agentenarchitektur", "3",
        "G z.S9", "SOV-3", "", "INT-01", "", "Exposure", "internal-method", "", "",
    ])

os.environ["DATABASE_URL"] = f"sqlite:///{ROOT / 'test.db'}"
os.environ["SOVRADAR_RUNTIME_DIR"] = str(ROOT / "runtime")
os.environ["SOVRADAR_METHOD_DIR"] = str(ROOT / "method")

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import delete  # noqa: E402
from apps.api.app.database import Base, SessionLocal, engine  # noqa: E402
from apps.api.app.main import app  # noqa: E402
from apps.api.app.models import (  # noqa: E402
    Answer,
    Assessment,
    AssessmentProfile,
    Evidence,
    LlmImport,
)

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def reset_db() -> None:
    with SessionLocal() as db:
        for model in (LlmImport, Answer, Evidence, AssessmentProfile, Assessment):
            db.execute(delete(model))
        db.commit()


def test_end_to_end_assessment_and_llm_bridge():
    reset_db()
    with client:
        health = client.get("/api/health")
        assert health.status_code == 200
        assert health.json()["method_questions"] == 2
        created = client.post(
            "/api/assessments",
            json={"name": "Pilot", "customer": "Kunde A", "workload_type": "ai-agent"},
        )
        assert created.status_code == 201
        assessment = created.json()

        profile = client.get(f"/api/assessments/{assessment['id']}/profile")
        assert profile.status_code == 200
        assert profile.json()["ai_used"] is True
        assert profile.json()["agentic_ai"] is True

        questions = client.get(f"/api/assessments/{assessment['id']}/questions")
        assert questions.status_code == 200
        assert {q["id"] for q in questions.json()} == {"DK-03", "KI-01"}

        answer = client.put(
            f"/api/assessments/{assessment['id']}/answers/DK-03",
            json={
                "question_id": "DK-03",
                "answer_value": "teilweise",
                "comment": "Review nötig",
            },
        )
        assert answer.status_code == 200
        evidence = client.post(
            f"/api/assessments/{assessment['id']}/evidence",
            data={
                "title": "KMS-Konzept",
                "evidence_type": "architecture",
                "content_excerpt": "Kunde verwaltet einen Schlüssel.",
            },
        )
        assert evidence.status_code == 201
        ev = evidence.json()
        prompt = client.get(f"/api/assessments/{assessment['id']}/llm-bridge/prompt")
        assert prompt.status_code == 200
        assert assessment["id"] in prompt.json()["prompt"]
        assert "KI-01" in prompt.json()["prompt"]
        imported = client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/import",
            json={
                "assessment_id": assessment["id"],
                "proposals": [{
                    "question_id": "DK-03",
                    "proposed_answer": "teilweise",
                    "rationale": "Auszug stützt kundenseitige Beteiligung.",
                    "evidence_ids": [ev["id"]],
                    "confidence": 0.8,
                }],
                "evidence_gaps": [],
                "warnings": ["Schlüssel-Custody nicht vollständig geklärt"],
            },
        )
        assert imported.status_code == 200
        assert imported.json()["proposals"][0]["question_id"] == "DK-03"


def test_profile_changes_question_path_conservatively():
    reset_db()
    with client:
        assessment = client.post(
            "/api/assessments",
            json={"name": "Public Website", "workload_type": "application", "confidentiality": "low"},
        ).json()

        relevant = client.get(f"/api/assessments/{assessment['id']}/questions?view=relevant")
        assert {q["id"] for q in relevant.json()} == {"DK-03"}

        all_questions = client.get(f"/api/assessments/{assessment['id']}/questions?view=all")
        ai_question = next(q for q in all_questions.json() if q["id"] == "KI-01")
        assert ai_question["applicability_status"] == "not_applicable"

        update = client.put(
            f"/api/assessments/{assessment['id']}/profile",
            json={
                "service_model": "unknown",
                "cloud_service": None,
                "contract_in_scope": None,
                "data_processing": None,
                "persistent_data": None,
                "encryption_used": None,
                "key_model": "unknown",
                "ai_used": True,
                "agentic_ai": True,
                "exit_relevant": None,
                "backup_relevant": None,
                "multi_provider": None,
                "subcontractors_used": None,
                "c5_relevant": None,
                "c3a_relevant": None,
                "iam_relevant": None,
                "logging_relevant": None,
                "internet_exposed": True,
            },
        )
        assert update.status_code == 200

        relevant_after = client.get(
            f"/api/assessments/{assessment['id']}/questions?view=relevant"
        )
        assert {q["id"] for q in relevant_after.json()} == {"DK-03", "KI-01"}


def test_llm_import_rejects_unknown_ids():
    reset_db()
    with client:
        assessment = client.post("/api/assessments", json={"name": "Pilot"}).json()
        response = client.post(
            f"/api/assessments/{assessment['id']}/llm-bridge/import",
            json={
                "assessment_id": assessment["id"],
                "proposals": [{
                    "question_id": "NOT-A-QUESTION",
                    "proposed_answer": "x",
                    "rationale": "x",
                    "evidence_ids": [],
                    "confidence": 0.5,
                }],
            },
        )
        assert response.status_code == 422
