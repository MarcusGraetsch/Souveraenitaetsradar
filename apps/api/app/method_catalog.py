from __future__ import annotations

import csv
from functools import lru_cache

from .settings import settings


@lru_cache(maxsize=1)
def load_questions() -> list[dict[str, str]]:
    question_dir = settings.method_dir / "question_bank"
    questions: list[dict[str, str]] = []
    if not question_dir.exists():
        return questions

    for path in sorted(question_dir.glob("*.csv")):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            for row in reader:
                if not row.get("QID"):
                    continue
                questions.append({
                    "id": row.get("QID", ""),
                    "domain": row.get("Domäne", ""),
                    "target_object": row.get("Zielobjekt", ""),
                    "question": row.get("Frage", ""),
                    "answer_type": row.get("Antworttyp", ""),
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
    return {q["id"] for q in load_questions()}
