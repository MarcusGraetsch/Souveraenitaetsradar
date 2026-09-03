from __future__ import annotations

import csv
import os
import tempfile
from pathlib import Path

ROOT = Path(tempfile.mkdtemp(prefix="sovradar-api-test-"))
METHOD_ROOT = ROOT / "method"
METHOD_DIR = METHOD_ROOT / "question_bank"
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

with (METHOD_ROOT / "r4_hard_gates.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle, delimiter=";")
    writer.writerow([
        "Gate-ID", "Gate", "Prüfgegenstand", "Capability 0", "Capability 1",
        "Capability 2", "Capability 3", "Capability 4", "Basis Req", "Standard Req",
        "Elevated Req", "Critical Req", "Source IDs", "Provenienz / Herleitung",
    ])
    for index in range(1, 9):
        gate_id = f"HG-{index:02d}"
        writer.writerow([
            gate_id, f"Gate {index}", f"Prüfgegenstand {index}", "0", "1", "2", "3", "4",
            1, 2, 3, 3, "INT-01", "Interne Testdefinition",
        ])

with (METHOD_ROOT / "evidence_request_catalog.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle, delimiter=";")
    writer.writerow([
        "Request-ID", "Gate-ID", "Claim area", "Acceptable evidence examples",
        "Required for", "Provider-neutral follow-up", "Preferred applied state",
        "Typical min trust", "Provenance",
    ])
    for index in range(1, 9):
        writer.writerow([
            f"ER-{index:03d}", f"HG-{index:02d}", f"Claim {index}", "document; test",
            "all", f"Follow-up {index}?", "tested", "3", "INT-02",
        ])

os.environ["DATABASE_URL"] = f"sqlite:///{ROOT / 'test.db'}"
os.environ["SOVRADAR_RUNTIME_DIR"] = str(ROOT / "runtime")
os.environ["SOVRADAR_METHOD_DIR"] = str(METHOD_ROOT)

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import delete  # noqa: E402
from apps.api.app.database import Base, SessionLocal, engine  # noqa: E402
from apps.api.app.main import app  # noqa: E402
from apps.api.app.models import (  # noqa: E402
    Answer,
    Assessment,
    AssessmentClaim,
    AssessmentProfile,
    Evidence,
    EvidenceReview,
    GateRequirement,
    LlmImport,
)

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def reset_db() -> None:
    with SessionLocal() as db:
        for model in (
            LlmImport,
            AssessmentClaim,
            GateRequirement,
            EvidenceReview,
            Answer,
            Evidence,
            AssessmentProfile,
            Assessment,
        ):
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


def test_hard_gate_api_pass_fail_and_unverified_flow():
    reset_db()
    with client:
        assessment = client.post(
            "/api/assessments",
            json={"name": "Gate Pilot", "criticality": "medium"},
        ).json()
        assessment_id = assessment["id"]

        catalog = client.get("/api/method/hard-gates")
        assert catalog.status_code == 200
        assert len(catalog.json()) == 8

        initial = client.get(f"/api/assessments/{assessment_id}/gates")
        assert initial.status_code == 200
        assert len(initial.json()) == 8
        hg04 = next(item for item in initial.json() if item["gate_id"] == "HG-04")
        assert hg04["requirement_level"] == 2
        assert hg04["requirement_source"] == "criticality-template:standard"
        assert hg04["final_state"] == "UNVERIFIED"

        evidence = client.post(
            f"/api/assessments/{assessment_id}/evidence",
            data={"title": "Exit-Test", "evidence_type": "test", "description": "Testnachweis"},
        ).json()
        evidence_id = evidence["id"]

        review = client.put(
            f"/api/assessments/{assessment_id}/evidence/{evidence_id}/review",
            json={
                "applied_state": "tested",
                "base_trust": 4,
                "scope_fit": 4,
                "freshness_fit": 4,
                "review_status": "reviewed",
            },
        )
        assert review.status_code == 200
        assert review.json()["effective_trust"] == 4

        claim = client.post(
            f"/api/assessments/{assessment_id}/claims",
            json={
                "gate_id": "HG-04",
                "statement": "Exit wurde end-to-end getestet.",
                "review_status": "reviewed",
                "capability_level": 2,
                "evidence_ids": [evidence_id],
                "question_ids": ["DK-03"],
            },
        )
        assert claim.status_code == 201

        passed = client.get(f"/api/assessments/{assessment_id}/gates").json()
        hg04 = next(item for item in passed if item["gate_id"] == "HG-04")
        assert hg04["technical_state"] == "PASS"
        assert hg04["evidence_state"] == "VERIFIED"
        assert hg04["final_state"] == "PASS"
        assert evidence_id in hg04["evidence_ids"]

        override = client.put(
            f"/api/assessments/{assessment_id}/gate-requirements/HG-04",
            json={"requirement_level": 3},
        )
        assert override.status_code == 200
        assert override.json()["source"] == "consultant-override"

        failed = client.get(f"/api/assessments/{assessment_id}/gates").json()
        hg04 = next(item for item in failed if item["gate_id"] == "HG-04")
        assert hg04["technical_state"] == "FAIL"
        assert hg04["final_state"] == "FAIL"


def test_unreviewed_claim_and_evidence_cannot_change_gate():
    reset_db()
    with client:
        assessment = client.post("/api/assessments", json={"name": "Review Boundary"}).json()
        assessment_id = assessment["id"]
        evidence = client.post(
            f"/api/assessments/{assessment_id}/evidence",
            data={"title": "Draft Evidence", "evidence_type": "document"},
        ).json()

        client.put(
            f"/api/assessments/{assessment_id}/evidence/{evidence['id']}/review",
            json={
                "applied_state": "documented",
                "base_trust": 5,
                "scope_fit": 5,
                "freshness_fit": 5,
                "review_status": "raw",
            },
        )
        draft_claim = client.post(
            f"/api/assessments/{assessment_id}/claims",
            json={
                "gate_id": "HG-03",
                "statement": "Nur ein Vorschlag, noch nicht bestätigt.",
                "review_status": "draft",
                "capability_level": 4,
                "evidence_ids": [evidence["id"]],
            },
        )
        assert draft_claim.status_code == 201
        gate = next(
            item for item in client.get(f"/api/assessments/{assessment_id}/gates").json()
            if item["gate_id"] == "HG-03"
        )
        assert gate["capability_level"] is None
        assert gate["final_state"] == "UNVERIFIED"


def test_claim_rejects_unknown_evidence_and_question_ids():
    reset_db()
    with client:
        assessment = client.post("/api/assessments", json={"name": "Invalid Links"}).json()
        bad_evidence = client.post(
            f"/api/assessments/{assessment['id']}/claims",
            json={
                "gate_id": "HG-01",
                "statement": "x",
                "evidence_ids": ["does-not-exist"],
            },
        )
        assert bad_evidence.status_code == 422

        bad_question = client.post(
            f"/api/assessments/{assessment['id']}/claims",
            json={
                "gate_id": "HG-01",
                "statement": "x",
                "question_ids": ["NOT-A-QUESTION"],
            },
        )
        assert bad_question.status_code == 422
