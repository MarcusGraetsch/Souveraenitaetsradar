# 2026-09-07 – DecisionCase / Provider Intelligence

Issue: #65  
Branch: `method/decision-case-provider-intelligence`  
Rollen: `architect`, `methodologist`, `project-coordinator`  
Reviewklasse: B – Methode/Architektur  
Review: Self-Review; technisches/methodisches Review vor Schema-/Runtime-Implementierung erforderlich.

## Ziel

Den bestehenden single-assessment-orientierten Souveränitätsradar so erweitern, dass mehrere Zielarchitekturen desselben Workloads vergleichbar bewertet werden können und öffentliche Provider-Evidence zentral wiederverwendbar wird.

## Ausgangsbefund

Der bestehende Methodenkern besitzt bereits die wesentlichen Schutzplanken:

- cloud-agnostischer Core
- Provider Capability ≠ Applied Capability
- Human-reviewed Claims vor Gate-Wirkung
- Evidence Confidence getrennt von Risikohöhe
- Gate first, score second
- providerneutrale Adapter
- generisches Domain Model mit Provider, Service, LegalEntity, Contract, Location, Dependency, Evidence, Claim und RiskScenario

Der wesentliche Gap liegt nicht in der Risiko-/Gate-Methode, sondern eine Ebene darüber: Managemententscheidungen vergleichen mehrere Architekturvarianten; Runtime-Assessment und Public Evidence sind bisher primär assessmentbezogen.

## Änderungen

### `docs/architecture/DECISION_CASE_AND_PROVIDER_INTELLIGENCE.md`

Neu dokumentiert:

- `DecisionCase` als Aggregatebene über mehreren `ArchitectureOption`s
- Shared Organization/Workload Facts vs. option-spezifische Facts
- `OptionAssessment` als bestehende Assessment-Semantik je Variante
- Architecture Option Types inklusive On-Prem, Public/Sovereign Cloud, Hybrid, Multi-Cloud und hypothetischer Zielarchitektur
- Organisation Capability vs. Architecture Skill Demand
- zentrale versionierte Provider Intelligence Knowledge Base
- Provider -> LegalEntity -> Offering -> Region/Scope -> Service -> ProviderCapabilityClaim -> EvidenceSource
- nationale Herkunft nicht als pauschaler Score, sondern explizite Rechts-/Kontrollfakten
- Hypothetical Options als `project-assumption`, niemals Providerfakt
- Provider Intelligence belegt nur Capability; Applied Capability bleibt kundenspezifisch
- vergleichendes Ergebnis mit Hard Gates, Souveränität, Workload Risk, Security/Operational Risk, Evidence Confidence, Wirtschaftlichkeit und Remediation
- Recommendation getrennt von CustomerDecision
- stufenweiser Implementierungspfad Methode -> Schema -> Runtime -> UI

### `project/DECISIONS.yaml`

Version 12, neue akzeptierte interne Methodenentscheidungen:

- DEC-037: DecisionCase + ArchitectureOptions
- DEC-038: wiederverwendbare Provider-Intelligence-Schicht
- DEC-039: Empfehlung aus transparentem Variantenvergleich, kein einzelner Wahrheitsscore; finale Entscheidung bleibt beim Kunden

Quelle der neuen Entscheidungen: `INT-04` / interne Methodenentwicklung aus Issue #65.

## Nicht geändert

- keine Gate-Formel
- keine Capability-/Requirement-Schwellen
- keine Frage-/Risikotaxonomie
- keine Runtime-/DB-/API-/UI-Modelle
- keine Providerdaten
- kein Nationalitätsranking
- keine regulatorische Aussage

## Security / Daten

Keine Kundendaten, Credentials oder Raw Evidence verarbeitet. Für die spätere Provider-Intelligence-Schicht bleibt offen, welche Provider-Volltexte unter Lizenz-/Nutzungsbedingungen gespeichert werden dürfen. Architektur fordert deshalb mindestens Metadaten, Scope, Version/Periode, Source Locator und Review State; Lizenz-/Volltextentscheidung ist vor Ingestion separat zu treffen.

## Self-Review gegen Repo-Prinzipien

- Providerneutralität: erhalten.
- Provider Adapter als Translation-only: erhalten.
- Provider Capability ≠ Applied Capability: explizit verstärkt.
- Fehlende Evidence -> UNVERIFIED: unverändert.
- Human Review / Legal Boundary: unverändert.
- Gate first, score second: unverändert.
- Hypothetische Varianten werden als Annahmen gekennzeichnet.
- Keine neue externe Normbehauptung.

## Offene Reviewpunkte

Vor Schema-/Runtime-Implementierung klären:

1. ein Workload vs. optional Workload-Gruppe pro DecisionCase
2. technische Repräsentation `OptionAssessment` vs. `Assessment.architecture_option_id`
3. Versionierung und Invalidierung von ProviderCapabilityClaims
4. zulässiger Speicherumfang öffentlicher Providerdokumente (Metadaten/Exzerpte/Volltext)
5. Reassessment-Trigger bei Provider-/Service-/Ownership-/Contract-Drift
6. Pflichtfelder für wirtschaftlichen Vergleich

## Tests / Validierung

Dokumentations-/Entscheidungsänderung ohne Runtime-Code. Kein deterministischer Rule-/Schema-Test erforderlich. Vor Merge sind mindestens YAML-/Repository-Validation und CI auf dem PR zu prüfen. Die spätere Schemaänderung ist Reviewklasse B und benötigt Boundary-/Backward-Compatibility-Tests.
