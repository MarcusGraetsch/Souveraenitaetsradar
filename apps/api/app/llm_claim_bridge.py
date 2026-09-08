from __future__ import annotations

import json
from typing import Any

CLAIM_PROMPT_VERSION = "claim-proposals-v1"
METHOD_VERSION = "1.0"


def response_schema(assessment_id: str) -> dict[str, Any]:
    return {
        "assessment_id": assessment_id,
        "prompt_version": CLAIM_PROMPT_VERSION,
        "method_version": METHOD_VERSION,
        "proposals": [
            {
                "gate_id": "HG-01",
                "statement": "<evidence-backed factual finding>",
                "capability_level": 2,
                "evidence_ids": ["<existing Evidence-ID>"],
                "question_ids": ["<existing Question-ID>"],
                "rationale": "<short reasoning based only on supplied Evidence>",
                "confidence": 0.0,
            }
        ],
        "evidence_gaps": [
            {
                "gate_id": "HG-03",
                "question_ids": ["<existing Question-ID>"],
                "missing": "<what is still required before a finding can be supported>",
            }
        ],
        "warnings": ["<contradiction, ambiguity or caveat>"],
    }


def build_claim_prompt(
    assessment: dict[str, Any],
    profile: dict[str, Any],
    answers: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    evidence_reviews: dict[str, dict[str, Any]],
    questions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> str:
    reviewed_answers = [item for item in answers if item.get("review_state") == "reviewed" and item.get("answer_value")]

    answer_lines = [
        " | ".join(
            [
                str(item.get("question_id", "")),
                f"Antwort: {item.get('answer_value', '')}",
                f"Kommentar: {item.get('comment', '')}",
                f"Nachweis-IDs: {', '.join(item.get('evidence_ids') or []) or '[keine]'}",
            ]
        )
        for item in reviewed_answers
    ]

    evidence_lines: list[str] = []
    for item in evidence:
        review = evidence_reviews.get(str(item.get("id")), {})
        evidence_lines.append(
            "\n".join(
                [
                    f"Evidence-ID: {item.get('id', '')}",
                    f"Titel: {item.get('title', '')}",
                    f"Typ: {item.get('evidence_type', '')}",
                    f"Quelle: {item.get('source', '')}",
                    f"Stand: {item.get('source_date', '')}",
                    f"Prüfstatus: {review.get('review_status', 'raw')}",
                    f"Applied State: {review.get('applied_state', 'asserted')}",
                    f"Wirksame Belegstärke: {review.get('effective_trust', 0)}",
                    "Interne Evidence-Beschreibung: [nicht an LLM freigegeben]",
                    f"Freigegebener Auszug: {item.get('content_excerpt', '') or '[kein Textauszug für LLM freigegeben]'}",
                ]
            )
        )

    question_lines = [
        " | ".join(
            [
                str(item.get("id", "")),
                str(item.get("domain", "")),
                str(item.get("question", "")),
                f"Applicability: {item.get('applicability_status', 'unknown')}",
                f"Workflow: {item.get('workflow_stage', '')}",
                f"Erwarteter Nachweis: {item.get('expected_evidence', '')}",
            ]
        )
        for item in questions
        if item.get("applicability_status") != "not_applicable"
    ]

    gate_lines: list[str] = []
    for gate in gates:
        capability_levels = gate.get("capability_levels") or {}
        level_text = "; ".join(
            f"Stufe {level}: {capability_levels.get(str(level), capability_levels.get(level, ''))}"
            for level in range(5)
        )
        gate_lines.append(
            "\n".join(
                [
                    f"Gate-ID: {gate.get('gate_id', '')}",
                    f"Name: {gate.get('name', '')}",
                    f"Prüfgegenstand: {gate.get('subject', '')}",
                    f"Aktuelle geforderte Mindeststufe: {gate.get('requirement_level', '')}",
                    f"Quelle der Mindeststufe: {gate.get('requirement_source', '')}",
                    f"Interne Capability-Stufen: {level_text}",
                ]
            )
        )

    claim_lines = [
        " | ".join(
            [
                str(item.get("gate_id", "")),
                f"Status: {item.get('review_status', '')}",
                f"Stufe: {item.get('capability_level', '')}",
                f"Aussage: {item.get('statement', '')}",
                f"Evidence: {', '.join(item.get('evidence_ids') or []) or '[keine]'}",
            ]
        )
        for item in claims
    ]

    return f"""SOUVERÄNITÄTS-RADAR – LLM-FESTSTELLUNGSVORSCHLÄGE

PROMPT-VERSION
{CLAIM_PROMPT_VERSION}

METHODENVERSION
{METHOD_VERSION}

ROLLE
Du unterstützt einen Consultant dabei, aus bereits erfassten Antworten und freigegebenen Nachweisen prüfbare fachliche Feststellungen für die zwingenden Mindestanforderungen vorzubereiten. Du entscheidest keine Gate-Ergebnisse und keine Risiken.

HARTE REGELN
1. Erzeuge ausschließlich **Vorschläge für fachliche Feststellungen**. Setze niemals PASS, FAIL, UNVERIFIED, Risikoakzeptanz oder Rechtsfolgen.
2. Jedes Proposal MUSS mindestens eine unten aufgeführte Evidence-ID und mindestens eine unten aufgeführte Question-ID referenzieren.
3. Assessment, Relevanzprofil und bereits erfasste Antworten sind Kontext. Sie ersetzen keinen Nachweis.
4. Nutze für Aussagen ausschließlich den als `Freigegebener Auszug` markierten Evidence-Inhalt. Interne Beschreibungen oder Raw-Dateien sind nicht freigegeben und werden nicht übertragen.
5. Behandle Assessment-ID, Gate-IDs, Question-IDs und Evidence-IDs als **OPAQUE IDENTIFIERS**. Kopiere sie zeichenidentisch und korrigiere oder normalisiere sie nicht.
6. Bewahre den epistemischen und zeitlichen Status: geplant/gewünscht/behauptet ist nicht implementiert/beobachtet/getestet.
7. Capability-Level 0–4 sind eine interne Radar-Operationalisierung. Verwende einen Level nur, wenn die bereitgestellte Evidence die für dieses Gate unten angegebene Beschreibung trägt. Erfinde keine eigene Stufenbedeutung.
8. Wenn die Evidence eine Feststellung, ihren Scope oder einen Capability-Level nicht ausreichend trägt, erzeuge **kein Proposal**, sondern einen Eintrag unter `evidence_gaps`.
9. Öffentliche Provider-Dokumentation über eine verfügbare Funktion belegt nicht automatisch deren kundenspezifische Konfiguration oder Wirksamkeit.
10. Berücksichtige bestehende Feststellungen und vermeide inhaltsgleiche Duplikate.
11. Verwende confidence konservativ. `1.0` nur bei expliziter und vollständiger Evidenzdeckung. Confidence ist nur Modell-Selbsteinschätzung und kein Radar-Trust.
12. Gib ausschließlich valides JSON im unten beschriebenen Format zurück. Keine Markdown-Codeblöcke, keine Einleitung.

ASSESSMENT
Assessment-ID: {assessment.get('id', '')}
Name: {assessment.get('name', '')}
Kunde: {assessment.get('customer', '')}
Workload-Typ: {assessment.get('workload_type', '')}
Beschreibung: {assessment.get('description', '')}
Kritikalität: {assessment.get('criticality', '')}
Schutzbedarf C/I/A: {assessment.get('confidentiality', '')} / {assessment.get('integrity', '')} / {assessment.get('availability', '')}
Ziel-Kontrollraum: {assessment.get('control_region', '')}
Regulatorischer Kontext: {assessment.get('regulatory_context', '')}

RELEVANZPROFIL – NUR KONTEXT
{json.dumps(profile, ensure_ascii=False, indent=2)}

HUMAN-GEPRÜFTE ANTWORTEN – KONTEXT
{chr(10).join(answer_lines) if answer_lines else '[noch keine human-geprüften Antworten]'}

NACHWEISE / FREIGEGEBENE AUSZÜGE
{chr(10).join(evidence_lines) if evidence_lines else '[noch keine Nachweise erfasst]'}

RELEVANTE FRAGEN
{chr(10).join(question_lines) if question_lines else '[keine relevanten Fragen]'}

K.O.-KRITERIEN UND INTERNE STUFENBESCHREIBUNGEN
{chr(10).join(gate_lines) if gate_lines else '[keine Gate-Definitionen]'}

BEREITS ERFASSTE FESTSTELLUNGEN
{chr(10).join(claim_lines) if claim_lines else '[noch keine Feststellungen]'}

AUFGABE
- Schlage nur Feststellungen vor, die durch die bereitgestellten Nachweise getragen werden.
- Verknüpfe jede Feststellung mit den relevanten Gate-, Question- und Evidence-IDs.
- Nutze Capability-Level nur entsprechend der angegebenen gate-spezifischen Stufenbeschreibung.
- Nutze `evidence_gaps`, wenn eine belastbare Feststellung oder Stufenzuordnung noch nicht möglich ist.
- Nutze `warnings` für Widersprüche, Scope-Probleme oder sonstige Unsicherheiten.
- Setze niemals selbst ein Gate-Ergebnis.

JSON-FORMAT
{json.dumps(response_schema(str(assessment.get('id', ''))), ensure_ascii=False, indent=2)}
"""
