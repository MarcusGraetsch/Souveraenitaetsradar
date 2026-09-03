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
    writer.writerow(["QID", "Domäne", "Zielobjekt", "Frage", "Antworttyp", "Anwendbarkeit", "Fragentyp", "Pflichtgrad", "Erwartete Evidenz", "Min. Trust", "Risiko-IDs", "SOV-Bezug", "Framework / Regulatorik", "Source IDs", "Follow-up / Entscheidungslogik", "Scoring-Rolle", "Provenienztyp", "Fundstelle / Herleitung", "Herleitungsnotiz"])
    writer.writerow(["DK-03", "Daten", "Key", "Wer kontrolliert Schlüssel?", "Text", "immer", "Fakt", "Basis", "KMS-Konzept", "3", "G z.S8", "SOV-3", "", "INT-01", "", "Exposure", "internal-method", "", ""])

os.environ["DATABASE_URL"] = f"sqlite:///{ROOT / 'test.db'}"
os.environ["SOVRADAR_RUNTIME_DIR"] = str(ROOT / "runtime")
os.environ["SOVRADAR_METHOD_DIR"] = str(ROOT / "method")

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import delete  # noqa: E402
from apps.api.app.database import Base, SessionLocal, engine  # noqa: E402
from apps.api.app.main import app  # noqa: E402
from apps.api.app.models import Answer, Assessment, Evidence, LlmImport  # noqa: E402

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def reset_db() -> None:
    with SessionLocal() as db:
        for model in (LlmImport, Answer, Evidence, Assessment):
            db.execute(delete(model))
        db.commit()


def test_end_to_end_assessment_and_llm_bridge():
    reset_db()
    with client:
        health = client.get("/api/health")
        assert health.status_code == 200
        assert health.json()["method_questions"] == 1
        created = client.post("/api/assessments", json={"name": "Pilot", "customer": "Kunde A"})
        assert created.status_code == 201
        assessment = created.json()
        answer = client.put(f"/api/assessments/{assessment['id']}/answers/DK-03", json={"question_id": "DK-03", "answer_value": "teilweise", "comment": "Review nötig"})
        assert answer.status_code == 200
        evidence = client.post(f"/api/assessments/{assessment['id']}/evidence", data={"title": "KMS-Konzept", "evidence_type": "architecture", "content_excerpt": "Kunde verwaltet einen Schlüssel."})
        assert evidence.status_code == 201
        ev = evidence.json()
        prompt = client.get(f"/api/assessments/{assessment['id']}/llm-bridge/prompt")
        assert prompt.status_code == 200
        assert assessment["id"] in prompt.json()["prompt"]
        imported = client.post(f"/api/assessments/{assessment['id']}/llm-bridge/import", json={"assessment_id": assessment["id"], "proposals": [{"question_id": "DK-03", "proposed_answer": "teilweise", "rationale": "Auszug stützt kundenseitige Beteiligung.", "evidence_ids": [ev["id"]], "confidence": 0.8}], "evidence_gaps": [], "warnings": ["Schlüssel-Custody nicht vollständig geklärt"]})
        assert imported.status_code == 200
        assert imported.json()["proposals"][0]["question_id"] == "DK-03"


def test_llm_import_rejects_unknown_ids():
    reset_db()
    with client:
        assessment = client.post("/api/assessments", json={"name": "Pilot"}).json()
        response = client.post(f"/api/assessments/{assessment['id']}/llm-bridge/import", json={"assessment_id": assessment["id"], "proposals": [{"question_id": "NOT-A-QUESTION", "proposed_answer": "x", "rationale": "x", "evidence_ids": [], "confidence": 0.5}]})
        assert response.status_code == 422
