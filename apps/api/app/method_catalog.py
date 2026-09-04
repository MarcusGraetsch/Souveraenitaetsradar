from __future__ import annotations

import csv
from functools import lru_cache

from .answer_controls import answer_control_for
from .settings import settings


@lru_cache(maxsize=1)
def load_questions() -> list[dict[str, object]]:
    question_dir = settings.method_dir / "question_bank"
    questions: list[dict[str, object]] = []
    if not question_dir.exists():
        return questions

    for path in sorted(question_dir.glob("*.csv")):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            for row in reader:
                if not row.get("QID"):
                    continue
                answer_type = row.get("Antworttyp", "")
                questions.append({
                    "id": row.get("QID", ""),
                    "domain": row.get("Domäne", ""),
                    "target_object": row.get("Zielobjekt", ""),
                    "question": row.get("Frage", ""),
                    "answer_type": answer_type,
                    "answer_control": answer_control_for(answer_type),
                    "applicability": row.get("Anwendbarkeit", ""),
                    "requiredness": row.get("Pflichtgrad", ""),
                    "expected_evidence": row.get("Erwartete Evidenz", ""),
                    "min_trust": row.get("Min. Trust", ""),
                    "risk_ids": row.get("Risiko-IDs", ""),
                    "sov_reference": row.get("SOV-Bezug", ""),
                    "follow_up": row.get("Follow-up / Entscheidungslogik", ""),
                })
    return questions


def question_ids() -> set[str]:
    return {str(q["id"]) for q in load_questions()}
