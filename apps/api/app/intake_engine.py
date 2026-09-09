from __future__ import annotations

from .intake_schemas import AssessmentIntakeCreate, ComplianceCandidate, PreAssessmentContext

NIS2_SECTOR_HINTS = {
    "energy", "transport", "banking", "financial", "health", "water", "wastewater",
    "digital infrastructure", "ict", "managed service", "public administration", "space",
    "energie", "verkehr", "banken", "finanz", "gesundheit", "wasser", "digitale infrastruktur",
    "it-dienst", "öffentliche verwaltung", "oeffentliche verwaltung",
}
DORA_SECTOR_HINTS = {"bank", "banking", "insurance", "financial", "finance", "investment", "payment", "finanz", "versicherung", "zahlung"}


def _contains_hint(value: str, hints: set[str]) -> bool:
    lowered = value.strip().lower()
    return any(hint in lowered for hint in hints)


def build_compliance_candidates(payload: AssessmentIntakeCreate) -> list[ComplianceCandidate]:
    org = payload.organization
    workload = payload.workload
    candidates: list[ComplianceCandidate] = []

    if workload.personal_data == "yes":
        gdpr_status = "likely_applicable"
        gdpr_rationale = ["Der Workload verarbeitet nach Intake-Angabe personenbezogene Daten."]
        gdpr_missing: list[str] = ["Rolle(n) als Verantwortlicher/Auftragsverarbeiter und konkrete Verarbeitung prüfen."]
    elif workload.personal_data == "no":
        gdpr_status = "likely_not_applicable"
        gdpr_rationale = ["Für den betrachteten Workload wurde personenbezogene Datenverarbeitung verneint."]
        gdpr_missing = ["Prüfen, ob Betriebs-, Nutzer- oder Supportdaten dennoch personenbezogen sind."]
    else:
        gdpr_status = "needs_review"
        gdpr_rationale = ["Ob der Workload personenbezogene Daten verarbeitet, ist noch ungeklärt."]
        gdpr_missing = ["Personenbezug der verarbeiteten Daten klären."]
    candidates.append(ComplianceCandidate(
        framework="GDPR", candidate_status=gdpr_status, rationale=gdpr_rationale,
        missing_facts=gdpr_missing, source_refs=["SRC-11"],
    ))

    sector_nis2 = _contains_hint(org.sector, NIS2_SECTOR_HINTS)
    size_nis2 = org.employee_size in {"medium", "large"}
    if sector_nis2 and size_nis2:
        nis2_status = "likely_applicable"
        nis2_rationale = ["Sektor und Größenklasse sind als NIS2-relevante Routing-Signale erfasst."]
        nis2_missing = ["Konkrete Tätigkeit, nationale Umsetzung, Sonderfälle und Entity-Scope rechtlich prüfen."]
    else:
        nis2_status = "needs_review"
        nis2_rationale = ["Aus Sektor und Größenangaben ergibt sich noch keine belastbare NIS2-Anwendbarkeit."]
        nis2_missing = []
        if not sector_nis2:
            nis2_missing.append("Konkrete NIS2-Sektor-/Tätigkeitszuordnung prüfen.")
        if org.employee_size == "unknown":
            nis2_missing.append("Unternehmensgröße klären.")
        nis2_missing.append("Sonderfälle und nationale Umsetzung prüfen.")
    candidates.append(ComplianceCandidate(
        framework="NIS2", candidate_status=nis2_status, rationale=nis2_rationale,
        missing_facts=nis2_missing, source_refs=["SRC-06", "SRC-07"],
    ))

    if _contains_hint(org.sector, DORA_SECTOR_HINTS):
        dora_status = "likely_applicable"
        dora_rationale = ["Der angegebene Sektor deutet auf einen Finanz-/Versicherungs-/Zahlungsbezug hin."]
        dora_missing = ["Konkrete DORA-Unternehmenskategorie und ggf. ICT-Drittdienstleisterrolle prüfen."]
    else:
        dora_status = "needs_review"
        dora_rationale = ["Der Intake weist keinen eindeutigen Finanzsektorbezug aus; DORA wird nicht automatisch ausgeschlossen."]
        dora_missing = ["Prüfen, ob die Organisation unter eine DORA-Unternehmenskategorie oder relevante ICT-Drittdienstleisterrolle fällt."]
    candidates.append(ComplianceCandidate(
        framework="DORA", candidate_status=dora_status, rationale=dora_rationale,
        missing_facts=dora_missing, source_refs=["SRC-08", "SRC-09", "SRC-10"],
    ))

    if workload.ai_used == "yes" or workload.primary_archetype in {"ai-system", "ai-agent"}:
        ai_status = "needs_review"
        ai_rationale = ["Der Workload nutzt KI bzw. ist als KI-System/KI-Agent klassifiziert."]
        ai_missing = ["AI-Act-Rolle, Verwendungszweck, Risikokategorie und territoriale Anknüpfung prüfen."]
    elif workload.ai_used == "no":
        ai_status = "likely_not_applicable"
        ai_rationale = ["Für den betrachteten Workload wurde KI-Nutzung verneint."]
        ai_missing = ["Prüfen, ob eingebettete Drittservices dennoch KI-Funktionen enthalten."]
    else:
        ai_status = "needs_review"
        ai_rationale = ["KI-Nutzung ist noch ungeklärt."]
        ai_missing = ["KI-Nutzung und AI-Act-Rolle klären."]
    candidates.append(ComplianceCandidate(
        framework="AI_ACT", candidate_status=ai_status, rationale=ai_rationale,
        missing_facts=ai_missing, source_refs=["SRC-13", "SRC-18", "SRC-19"],
    ))
    return candidates


def build_pre_assessment(payload: AssessmentIntakeCreate) -> PreAssessmentContext:
    org = payload.organization
    workload = payload.workload
    missing: list[str] = []
    if workload.personal_data == "unknown":
        missing.append("Personenbezug der Workload-Daten klären")
    if workload.sensitive_business_data == "unknown":
        missing.append("Sensibilität von Fach-/Geschäftsdaten klären")
    if workload.external_provider_in_scope == "unknown":
        missing.append("Externen Provider-/Cloud-/SaaS-Scope klären")
    if org.group_structure == "unknown":
        missing.append("Konzern-/Gruppenstruktur klären")
    if org.employee_size == "unknown":
        missing.append("Organisationsgröße klären")

    deep_dives: list[str] = []
    if workload.primary_archetype in {"ai-system", "ai-agent"} or workload.ai_used == "yes":
        deep_dives += ["AI Act / KI-Governance", "Daten- & Modellabhängigkeit"]
    if workload.external_provider_in_scope == "yes" or workload.current_operating_model in {"public-cloud", "saas", "hybrid", "multi-cloud"}:
        deep_dives += ["C3A / Cloud-Autonomie", "Exit & Portabilität", "Provider Intelligence"]
    if org.organization_type in {"public_authority", "public_body"}:
        deep_dives.append("Öffentliche Verwaltung / BSI-Profil")

    countries = {org.headquarters_country, *org.activity_countries, *workload.user_countries}
    countries.discard("")
    complexity: list[str] = []
    if len(countries) > 1:
        complexity.append(f"Mehrere Länder im Scope: {', '.join(sorted(countries))}")
    if len(org.legal_entities) > 1:
        complexity.append(f"Mehrere juristische Einheiten im Scope: {len(org.legal_entities)}")

    tags = list(dict.fromkeys([*workload.tags, workload.primary_archetype]))
    focus = ["Entscheidungsziel und Scope bestätigen", "Datenarten und Datenflüsse klären", "Betriebs-/Providerabhängigkeiten erfassen"]
    if "ai-agent" in tags or "ai-system" in tags:
        focus.append("KI-Rolle, Modell-/Tool-Abhängigkeiten und Datenzugriffe klären")
    if workload.current_operating_model in {"public-cloud", "saas", "hybrid", "multi-cloud"}:
        focus.append("Jurisdiktion, Exit, Schlüssel-/IAM-Kontrolle und Lieferkette priorisieren")

    return PreAssessmentContext(
        workload_tags=tags,
        compliance_candidates=build_compliance_candidates(payload),
        missing_scope_facts=missing,
        suggested_deep_dive_profiles=list(dict.fromkeys(deep_dives)),
        suggested_screening_focus=focus,
        jurisdiction_complexity=complexity,
    )
