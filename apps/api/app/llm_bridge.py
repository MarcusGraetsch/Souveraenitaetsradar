from __future__ import annotations

import json

from .method_catalog import load_questions


RESPONSE_SCHEMA = {
    "assessment_id": "<must match>",
    "proposals": [{
        "question_id": "DK-03",
        "proposed_answer": "<answer proposal>",
        "rationale": "<short reasoning based only on supplied material>",
        "evidence_ids": ["<existing evidence id>"],
        "confidence": 0.0,
    }],
    "evidence_gaps": [{"question_id": "TE-04", "missing": "<what is missing>"}],
    "warnings": ["<contradiction, ambiguity or caveat>"],
}


def build_prompt(
    assessment: dict,
    answers: list[dict],
    evidence: list[dict],
    *,
    questions: list[dict] | None = None,
    profile: dict | None = None,
) -> str:
    questions = questions if questions is not None else load_questions()
    answered = {item["question_id"] for item in answers if item.get("answer_value")}
    unresolved = [q for q in questions if q["id"] not in answered]

    evidence_lines = []
    for item in evidence:
        evidence_lines.append("\n".join([
            f"Evidence-ID: {item['id']}",
            f"Titel: {item['title']}",
            f"Typ: {item['evidence_type']}",
            f"Quelle: {item.get('source', '')}",
            f"Stand: {item.get('source_date', '')}",
            f"Beschreibung: {item.get('description', '')}",
            f"Freigegebener Auszug: {item.get('content_excerpt', '') or '[kein Textauszug im Radar]'}",
        ]))

    question_lines = [
        " | ".join([
            q["id"],
            q["domain"],
            q["question"],
            f"Applicability: {q.get('applicability_status', 'unknown')}",
            f"Grund: {q.get('applicability_reason', '')}",
            f"erwartete Evidenz: {q['expected_evidence']}",
        ])
        for q in unresolved
    ]
    current_answers = [
        f"{a['question_id']}: {a.get('answer_value', '')} | Kommentar: {a.get('comment', '')}"
        for a in answers if a.get("answer_value")
    ]

    return f"""SOUVERÄNITÄTS-RADAR – EXTERNE LLM-ANALYSE

ROLLE
Du unterstützt einen Berater bei der strukturierten Analyse digitaler Souveränität. Du entscheidest keine Risiken und akzeptierst keine Risiken. Du erzeugst ausschließlich prüfbare Vorschläge.

HARTE REGELN
1. Nutze ausschließlich die nachfolgend bereitgestellten Informationen und vom Benutzer im Chat zusätzlich bereitgestellte Dokumente.
2. Erfinde keine Fakten, Anbietermerkmale, Vertragsbedingungen oder technischen Einstellungen.
3. Fehlende Information ist fehlende Information – nicht PASS und nicht FAIL.
4. Trenne Beobachtung, Annahme und Ableitung.
5. Verweise in jedem Vorschlag auf vorhandene Evidence-IDs, sofern Evidence die Aussage stützt.
6. Fragen mit Applicability `needs_review` sind bewusst sichtbar: behandle sie nicht automatisch als anwendbar oder nicht anwendbar.
7. Gib ausschließlich valides JSON im unten beschriebenen Format zurück. Keine Markdown-Codeblöcke und keine Einleitung.

ASSESSMENT
Assessment-ID: {assessment['id']}
Name: {assessment['name']}
Kunde: {assessment.get('customer', '')}
Workload-Typ: {assessment.get('workload_type', '')}
Beschreibung: {assessment.get('description', '')}
Kritikalität: {assessment.get('criticality', '')}
Schutzbedarf C/I/A: {assessment.get('confidentiality', '')} / {assessment.get('integrity', '')} / {assessment.get('availability', '')}
Ziel-Kontrollraum: {assessment.get('control_region', '')}
Regulatorischer Kontext: {assessment.get('regulatory_context', '')}

RELEVANZPROFIL
{json.dumps(profile or {}, ensure_ascii=False, indent=2)}

BEREITS ERFASSTE ANTWORTEN
{chr(10).join(current_answers) if current_answers else '[noch keine Antworten]'}

EVIDENCE-METADATEN / FREIGEGEBENE AUSZÜGE
{chr(10).join(evidence_lines) if evidence_lines else '[noch keine Evidence erfasst]'}

OFFENE RELEVANTE / ZU PRÜFENDE FRAGEN
{chr(10).join(question_lines) if question_lines else '[keine offenen relevanten Fragen]'}

AUFGABE
- Schlage Antworten nur dort vor, wo die bereitgestellte Evidence dies trägt.
- Nenne die Evidence-IDs und eine knappe Begründung.
- Führe fehlende Informationen als evidence_gaps auf.
- Führe Widersprüche/Unsicherheiten als warnings auf.
- confidence ist eine Hilfsgröße 0..1 und ersetzt keinen Radar-Trust-Level.

JSON-FORMAT
{json.dumps(RESPONSE_SCHEMA, ensure_ascii=False, indent=2)}
"""
