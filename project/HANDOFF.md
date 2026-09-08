# Project Handoff

## Kurzfassung – Stand 08.09.2026

Der Souveränitäts-Radar ist fachlich auf **Decision Support für digitale Souveränität** ausgerichtet. Der aktuelle Zielstand steht in `docs/method/METHOD_CORE_V0_4_DE.md`.

Die technische Webapp ist vorhanden und validiert, bildet aber noch wesentliche Teile des früheren Einzel-Assessment-/Guided-Questions-Workflows ab. Diese Abweichung ist bewusst dokumentiert: **Zielmethode und Runtime sind noch nicht vollständig migriert.**

Vor weiterer fachlicher Methoden-, Schema-, Runtime- oder UI-Entwicklung gilt ein explizites Gate:

> **NEXT-120 / Issue #68 – vollständigen BSI-C3A-Kriterienkatalog gegen Methodenkern v0.4 und die bestehende Architektur prüfen.**

Der C3A-Volltext wird vom Projektinhaber bereitgestellt. Bis dahin ist NEXT-120 `waiting_input`.

## Aktueller fachlicher Zielstand

### Beratungsziel

Für einen konkreten Workload werden mehrere realistische Betriebs-/Architekturvarianten verglichen. Der Radar darf eine Empfehlung formulieren; finale Entscheidung, Risikoakzeptanz und rechtliche Würdigung bleiben beim Kunden.

Typische Optionen:

- Status quo / heutiges On-Prem
- modernisiertes On-Prem / Private Cloud
- US-Hyperscaler in EU-Region
- deutscher/europäischer Cloud-Provider
- chinesischer Provider
- Sovereign Cloud
- Hybrid-/Multi-Cloud
- hypothetische Sollarchitektur

### Sichtbare Entscheidungsdimensionen

1. Geschäft & Innovation
2. Security & Resilienz
3. Recht, Daten & Kontrolle
4. Technologie & Exit
5. Organisation & Skills
6. Lieferkette & Geopolitik
7. Wirtschaft & Vertrag

Separat: **Evidence Confidence / Belastbarkeit der Erkenntnisse**.

### Framework-Rollen

Frameworks werden nicht als mehrere Vollprüfungen gestapelt:

- Bitkom Cloud-Souveränität 2026: Handlungsfähigkeit, Risiko/Chance, Skills, Interdependenzen, Exit
- EU Cloud Sovereignty Framework: Provider-/Service-Souveränität und Evidence
- BSI C3A: wichtiger Provider-/Service-Souveränitätslayer; **Detailmapping noch nicht vollständig geprüft, siehe #68**
- BSI 200-3 / IT-Grundschutz: Anschlussfähigkeit, Security-/Resilienz-Deep-Dive, Gefährdungs- und Vollständigkeitsreferenz
- Data Act: Exit/Switching/Portabilität, soweit anwendbar
- C5: Security-/Assurance-Evidence
- NIS2, DORA, DSGVO/EDPB, AI Act usw.: nur bei tatsächlicher Anwendbarkeit als Compliance-Overlay; sonst ggf. Methoden-/Fragenquelle

### Fragenlogik

Die 128 Fragen bleiben als **Question Library** erhalten. Sie sind kein Pflichtfragebogen.

Zielbild:

```text
vorhandene Artefakte / Provider Intelligence
  -> Vorbefüllung
  -> ca. 15–25 Screening-Fragen
  -> nur entscheidungsrelevante Deep Dives
  -> Evidence / Claims / Risiken / Gates
  -> Variantenvergleich
  -> Entscheidungsvorlage / Empfehlung
```

Der Zielkorridor 15–25 ist eine interne Designhypothese und muss nach NEXT-120 in Referenzfällen kalibriert werden.

### Intake

Optionale Quellen:

- Interview / Workshop
- Servicekatalog / CMDB
- ArchiMate / EA-Modelle
- Architekturdiagramme
- BIA / BCM
- ISMS / Risikoregister
- Verträge / SLA / AVV / Exit-Klauseln
- IaC / Terraform / OpenTofu / Bicep / CloudFormation
- Kubernetes / Helm / Argo CD / GitOps
- IAM / PKI / KMS
- FinOps / Kosteninformationen
- Backup-/Restore-/DR-/Exit-Tests

Keiner dieser Artefakttypen ist Voraussetzung. Kontextquelle ≠ automatisch ausreichende Evidence.

### Geopolitik

Providerherkunft ist kein Score. Politische oder geopolitische Sorgen werden in prüfbare Szenarien zerlegt, z. B.:

- staatlich erzwungener Zugriff
- Sanktionen / Exportkontrollen
- Serviceentzug / Servicebeschränkung
- Support-/Updateverlust
- Change of Control
- Preis-/Vertragsschock

Die Szenarien werden auf alle relevanten Varianten angewandt, auch auf On-Prem-Lieferketten.

## Bestehende verbindliche Evidence-/Gate-Regeln

- cloud-agnostischer Core
- Customer-mediated Evidence; keine Cloud-Credentials als Voraussetzung
- Provider Adapter = Translation only
- Provider/Service Capability ≠ Applied Capability
- Evidence Confidence ≠ Risikohöhe
- Gate first, score second
- fehlende Evidence = `UNVERIFIED`, nicht automatisch FAIL
- Human-reviewed Claims sind die einzige Brücke von Evidence zu deterministischen Hard Gates
- LLM-Proposals wirken ohne Human Review nicht auf Gates
- Legal Conclusions, Risikoakzeptanz und Kundenentscheidung bleiben menschlich
- Raw Kundenevidence wird nicht committed

## Runtime-Stand

Vorhanden und technisch validiert:

- React/Vite Consultant UI
- FastAPI / PostgreSQL / Docker Compose
- Assessment + Relevanzprofil
- Applicability `applicable | needs_review | not_applicable`
- Workflow `screening | clarification | deep_dive | completed | excluded`
- Evidence Intake / Evidence Review
- Evidence -> Claim -> Hard Gate
- Copy/Paste LLM Bridge
- Structured Export / Consultant Report / Backup / Restore

Die Runtime ist aktuell **pre-v0.4** hinsichtlich DecisionCase/ArchitectureOptions, Status-quo-/Business-Value-Vergleich, sieben sichtbaren Decision Dimensions und stark verkleinertem Screeningkern.

## Aktuelle Reihenfolge

### 1. NEXT-120 / Issue #68 – jetzt

C3A-Volltextreview. Keine neue fachliche Runtime-/Schema-/UI-Entwicklung bis Abschluss.

### 2. NEXT-118 / Issue #28 – danach

Manuelle Consultant-Evaluation der vorhandenen Runtime. Status: `blocked_by NEXT-120`.

### 3. NEXT-119 / Issue #67 – danach bzw. parallel nach Freigabe

Methodenkern v0.4 an mehreren Referenzvarianten validieren; Screeningkern, Overlay-Aktivierung und Empfehlungsvorlage kalibrieren. Status: `blocked_by NEXT-120`.

### 4. Erst danach Runtime-Migration

Schrittweise gemäß `docs/architecture/DECISION_SUPPORT_V0_4_ALIGNMENT.md`.

## Parallel zulässig

- Security-Hardening, insbesondere Issue #25 / NEXT-117 und Issue #26
- Bugfixes
- Repository-/CI-Hygiene
- Quellensicherung ohne neue fachliche Vorwegnahme

## Primäre Dokumente für den nächsten Agenten

1. `AGENTS.md`
2. `project/PROJECT_STATE.yaml`
3. dieses Handoff
4. `project/NEXT_ACTIONS.yaml`
5. `project/DECISIONS.yaml`
6. `docs/method/METHOD_CORE_V0_4_DE.md`
7. `docs/method/GLOSSARY_DE.md`
8. `docs/method/GLOSSARY_DE_V0_4_ADDENDUM.md`
9. `docs/architecture/DECISION_CASE_AND_PROVIDER_INTELLIGENCE.md`
10. `docs/architecture/DECISION_SUPPORT_V0_4_ALIGNMENT.md`
11. `docs/architecture/INTAKE_AND_CONTEXT_SOURCES.md`
12. `docs/method/SOURCE_GUIDE.md`
13. Issue #68

`docs/history/` und Agent-Logs sind historische Nachweise, nicht die aktuelle Fachquelle. Repo-State schlägt Chatgedächtnis.
