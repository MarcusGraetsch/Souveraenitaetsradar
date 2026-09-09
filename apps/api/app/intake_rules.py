from __future__ import annotations

from .intake_schemas import AssessmentIntakeCreate, ComplianceCandidate, PreAssessmentContext

EU_COUNTRIES = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DE", "DK", "EE", "ES", "FI", "FR", "GR",
    "HU", "IE", "IT", "LT", "LU", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK",
}
EEA_COUNTRIES = EU_COUNTRIES | {"IS", "LI", "NO"}

NIS2_SECTORS = {
    "energy",
    "transport",
    "banking",
    "financial-market-infrastructure",
    "health",
    "drinking-water",
    "waste-water",
    "digital-infrastructure",
    "ict-managed-services",
    "public-administration",
    "space",
    "postal-courier",
    "waste-management",
    "chemicals",
    "food",
    "manufacturing-critical-products",
    "digital-providers",
    "research",
}

DORA_FINANCIAL_SECTORS = {
    "banking",
    "payments",
    "investment-services",
    "insurance",
    "pensions",
    "crypto-assets",
    "financial-market-infrastructure",
    "credit-rating",
    "crowdfunding",
}


def _code(value: str) -> str:
    return value.strip().upper()


def _codes(values: list[str]) -> set[str]:
    return {_code(value) for value in values if value.strip()}


def _eu_nexus(payload: AssessmentIntakeCreate) -> bool:
    org = payload.organization
    workload = payload.workload
    countries = {_code(org.country_code)} | _codes(org.activity_countries) | _codes(workload.usage_countries)
    countries |= {_code(org.primary_legal_entity.country_code)}
    countries |= {_code(item.country_code) for item in org.additional_legal_entities}
    return bool(countries & EU_COUNTRIES)


def _eea_nexus(payload: AssessmentIntakeCreate) -> bool:
    org = payload.organization
    workload = payload.workload
    countries = {_code(org.country_code)} | _codes(org.activity_countries) | _codes(workload.usage_countries)
    countries |= {_code(org.primary_legal_entity.country_code)}
    countries |= {_code(item.country_code) for item in org.additional_legal_entities}
    return bool(countries & EEA_COUNTRIES)


def _gdpr(payload: AssessmentIntakeCreate) -> ComplianceCandidate:
    personal = payload.workload.personal_data
    if personal == "yes" and _eea_nexus(payload):
        return ComplianceCandidate(
            framework="DSGVO",
            candidate_status="likely_applicable",
            rationale=[
                "Der Workload verarbeitet laut Intake personenbezogene Daten.",
                "Mindestens ein Organisations-, Tätigkeits-, Nutzungs- oder Legal-Entity-Bezug liegt im EWR.",
            ],
            missing_facts=["Rolle(n) als Verantwortlicher/Auftragsverarbeiter und konkrete Verarbeitung prüfen."],
            source_refs=["SRC-11"],
        )
    if personal == "yes":
        return ComplianceCandidate(
            framework="DSGVO",
            candidate_status="needs_review",
            rationale=["Personenbezogene Daten sind im Scope, aber der territoriale Bezug ist aus dem Intake nicht abschließend geklärt."],
            missing_facts=["Niederlassungs-, Markt-/Betroffenenbezug und Rollen der beteiligten Einheiten prüfen."],
            source_refs=["SRC-11"],
        )
    if personal == "no":
        return ComplianceCandidate(
            framework="DSGVO",
            candidate_status="likely_not_applicable",
            rationale=["Für den betrachteten Workload wurde personenbezogene Datenverarbeitung verneint."],
            missing_facts=["Prüfen, ob Account-, Support-, Beschäftigten- oder Telemetriedaten dennoch personenbezogen sind."],
            source_refs=["SRC-11"],
        )
    return ComplianceCandidate(
        framework="DSGVO",
        candidate_status="needs_review",
        rationale=["Ob der Workload personenbezogene Daten verarbeitet, ist noch ungeklärt."],
        missing_facts=["Datenarten und betroffene Personengruppen klären."],
        source_refs=["SRC-11"],
    )


def _nis2(payload: AssessmentIntakeCreate) -> ComplianceCandidate:
    org = payload.organization
    sector_in_scope = org.sector in NIS2_SECTORS
    size_supports = org.size_class in {"medium", "large", "public-sector"}
    if _eu_nexus(payload) and sector_in_scope and size_supports:
        return ComplianceCandidate(
            framework="NIS2",
            candidate_status="likely_applicable",
            rationale=[
                f"Der gewählte Sektor `{org.sector}` liegt in der Radar-NIS2-Sektorliste.",
                f"Die angegebene Größenklasse `{org.size_class}` spricht für eine vertiefte NIS2-Prüfung.",
                "Ein EU-Bezug ist im Intake vorhanden.",
            ],
            missing_facts=["Konkrete Einrichtung/Tätigkeit und nationales Umsetzungsgesetz durch Fachreview bestätigen."],
            source_refs=["SRC-06", "SRC-07"],
        )
    if sector_in_scope:
        missing = []
        if org.size_class in {"micro", "small", "unknown"}:
            missing.append("Größen-/Sondertatbestand prüfen; bestimmte Einrichtungen können unabhängig von Standardschwellen erfasst sein.")
        if not _eu_nexus(payload):
            missing.append("EU-Tätigkeits-/Niederlassungsbezug und nationales Recht prüfen.")
        return ComplianceCandidate(
            framework="NIS2",
            candidate_status="needs_review",
            rationale=[f"Der gewählte Sektor `{org.sector}` kann NIS2-relevant sein, die Intake-Fakten reichen aber nicht für eine belastbare Einordnung."],
            missing_facts=missing or ["Konkrete Einrichtung/Tätigkeit prüfen."],
            source_refs=["SRC-06", "SRC-07"],
        )
    return ComplianceCandidate(
        framework="NIS2",
        candidate_status="likely_not_applicable",
        rationale=[f"Der gewählte Primärsektor `{org.sector}` ist in der aktuellen Radar-NIS2-Sektorliste nicht enthalten."],
        missing_facts=["Weitere Tätigkeiten, Sondertatbestände oder nationale Erweiterungen bei Bedarf prüfen."],
        source_refs=["SRC-06", "SRC-07"],
    )


def _dora(payload: AssessmentIntakeCreate) -> ComplianceCandidate:
    org = payload.organization
    if org.sector in DORA_FINANCIAL_SECTORS and _eu_nexus(payload):
        return ComplianceCandidate(
            framework="DORA",
            candidate_status="likely_applicable",
            rationale=[f"Der gewählte Sektor `{org.sector}` gehört zu den im Radar als DORA-finanznah geführten Sektoren und ein EU-Bezug liegt vor."],
            missing_facts=["Konkreten Finanzunternehmenstyp und Rolle gemäß DORA durch Fachreview bestätigen."],
            source_refs=["SRC-08", "SRC-09", "SRC-10"],
        )
    if org.sector in DORA_FINANCIAL_SECTORS or org.sector in {"ict-managed-services", "digital-infrastructure"}:
        return ComplianceCandidate(
            framework="DORA",
            candidate_status="needs_review",
            rationale=["Finanz- bzw. ICT-Drittdienstleisterbezug ist möglich; die genaue DORA-Rolle ist noch nicht geklärt."],
            missing_facts=["Entitätstyp, Finanzmarktrolle sowie ggf. ICT-Drittdienstleister-/CTPP-Kontext prüfen."],
            source_refs=["SRC-08", "SRC-09", "SRC-10"],
        )
    return ComplianceCandidate(
        framework="DORA",
        candidate_status="likely_not_applicable",
        rationale=["Aus Organisationstyp/Sektor ergibt sich im Intake kein unmittelbarer Finanzsektorbezug."],
        missing_facts=["Nur bei abweichender Finanzmarktrolle oder relevanter Gruppenzugehörigkeit erneut prüfen."],
        source_refs=["SRC-08", "SRC-09", "SRC-10"],
    )


def _ai_act(payload: AssessmentIntakeCreate) -> ComplianceCandidate:
    workload = payload.workload
    ai_signal = (
        workload.ai_used == "yes"
        or workload.primary_archetype in {"ai-system", "ai-agent"}
        or bool({"ai", "agentic"} & {tag.strip().lower() for tag in workload.tags})
    )
    if ai_signal:
        missing = []
        if workload.ai_role in {"unknown", "none"}:
            missing.append("Rolle im KI-Lebenszyklus (z. B. Provider/Deployer/Integrator) klären.")
        missing.append("Use Case, Risikoklasse, betroffene Personen und territoriale Anknüpfung prüfen.")
        return ComplianceCandidate(
            framework="AI Act",
            candidate_status="needs_review",
            rationale=["Der Intake enthält ein KI-Signal; die Anwendbarkeit hängt zusätzlich von Rolle, Use Case und territorialem Bezug ab."],
            missing_facts=missing,
            source_refs=["SRC-13", "SRC-18", "SRC-19"],
        )
    if workload.ai_used == "no":
        return ComplianceCandidate(
            framework="AI Act",
            candidate_status="likely_not_applicable",
            rationale=["Der Workload ist nicht als KI-System/-Agent klassifiziert und KI-Nutzung wurde verneint."],
            source_refs=["SRC-13", "SRC-18", "SRC-19"],
        )
    return ComplianceCandidate(
        framework="AI Act",
        candidate_status="needs_review",
        rationale=["KI-Nutzung ist noch ungeklärt."],
        missing_facts=["Prüfen, ob KI-Modelle, generative Funktionen oder agentische Komponenten genutzt werden."],
        source_refs=["SRC-13", "SRC-18", "SRC-19"],
    )


def derive_pre_assessment(payload: AssessmentIntakeCreate) -> PreAssessmentContext:
    workload = payload.workload
    org = payload.organization
    tags = {tag.strip().lower() for tag in workload.tags if tag.strip()}

    classification = [f"Primärarchetyp: {workload.primary_archetype}"]
    classification.extend(f"Tag: {tag}" for tag in sorted(tags))

    missing: list[str] = []
    if org.size_class == "unknown":
        missing.append("Organisationsgröße ist noch ungeklärt; sie beeinflusst u. a. regulatorisches Routing.")
    if workload.personal_data == "unknown":
        missing.append("Personenbezogene Datenverarbeitung klären.")
    if workload.ai_used == "unknown":
        missing.append("KI-Nutzung klären.")
    if workload.external_cloud_or_saas == "unknown":
        missing.append("Externen Cloud-/SaaS-Bezug klären.")
    if org.group_structure == "yes" and not org.additional_legal_entities:
        missing.append("Konzernstruktur wurde bejaht, aber weitere beteiligte juristische Einheiten fehlen noch.")

    deep_dives: list[str] = []
    if workload.ai_used == "yes" or workload.primary_archetype in {"ai-system", "ai-agent"}:
        deep_dives.append("KI / AI-Act-Rollen- und Use-Case-Prüfung")
    if workload.external_cloud_or_saas == "yes" or workload.current_operating_model in {"public-cloud", "saas", "hybrid", "multi-cloud"}:
        deep_dives.append("Provider-/Service-Souveränität (EU-CSF/C3A/C5 je Requirement Profile)")
    if workload.personal_data == "yes":
        deep_dives.append("Datenschutz / Drittland- und Rollenprüfung")
    if org.organization_type in {"public-authority", "public-body"}:
        deep_dives.append("Öffentliche Verwaltung / einschlägige BSI-Profile")
    if org.group_structure == "yes" or org.additional_legal_entities:
        deep_dives.append("Legal-Entity-/Jurisdiktions- und Vertragskettenprüfung")

    return PreAssessmentContext(
        classification_suggestions=classification,
        compliance_candidates=[_gdpr(payload), _nis2(payload), _dora(payload), _ai_act(payload)],
        missing_facts=missing,
        suggested_deep_dives=deep_dives,
        warnings=[
            "Compliance-Kandidaten sind Routing-Vorschläge, keine Rechtsfeststellung; relevante Schlussfolgerungen benötigen HITL-04.",
            "Kritikalität und C/I/A sind beim Intake bewusst noch nicht festgelegt; sie folgen in einem späteren Business-Impact-/Schutzbedarfsreview.",
        ],
    )
