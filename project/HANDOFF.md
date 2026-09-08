# Project Handoff

## Kurzfassung – Stand 08.09.2026

Der Souveränitäts-Radar ist fachlich auf **Decision Support für digitale Souveränität** ausgerichtet. Der aktuelle Zielstand steht in `docs/method/METHOD_CORE_V0_4_DE.md`.

Die technische Webapp ist vorhanden und validiert, bildet aber noch wesentliche Teile des früheren Einzel-Assessment-/Guided-Questions-Workflows ab. Diese Abweichung ist bewusst dokumentiert: **Zielmethode und Runtime sind noch nicht vollständig migriert.**

Der bisherige C3A-Review-Gate **NEXT-120 / Issue #68 ist fachlich abgeschlossen**. Der vollständige BSI-C3A-v1.0-Text wurde gegen Methodenkern v0.4, Provider Intelligence, Hard Gates, Risikotaxonomie und Question Library geprüft.

Kanonische C3A-Artefakte:

- `docs/method/C3A_V1_0_REVIEW.md`
- `data/method/c3a_v1_0_crosswalk.csv`
- `SRC-04` in `data/method/source_register.csv`

## Wichtigste C3A-Konsequenzen

- C3A ist ein nicht bindender Provider-/Service-Autonomie- und Evidence-Rahmen und ersetzt nicht den kunden-/workloadspezifischen Variantenvergleich.
- C3A deckt SOV-1 bis SOV-6 ab; SOV-7 Security & Compliance wird insbesondere über C5/IT-Grundschutz adressiert, SOV-8 liegt außerhalb des BSI-Scope.
- C3A setzt die Erfüllung der C5-Kriterien voraus. Eine formale C3A-Erfüllung darf daher nicht ohne belastbare C5-Scope-Evidence behauptet werden.
- `Criterion` und `Additional Criterion` sind keine Reifegradstufen. EU-/Deutschlandvarianten sind alternative Anforderungen. Der Kunde wählt abhängig von Use Case und Souveränitätsbedarf ein Requirement Profile.
- C3A-Datenklassen `Account Data`, `Cloud Service Customer Data`, `Cloud Service Derived Data` und `Cloud Service Provider Data` werden im C3A-/Provider-Intelligence-Scope getrennt betrachtet.
- C3A SOV-6 beschreibt primär providerseitige Source-Code-, Build-, Entwicklungs- und Fortführungsautonomie. Kundenseitiger Exit/Portabilität bleibt primär bei Data Act, DORA, Bitkom und interner Radar-Methodik.
- Mehrere frühere C3A-Fragenzuordnungen wurden quellengetreu korrigiert; Details im Crosswalk.

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
- BSI C3A: konkretisierender Provider-/Service-Autonomie- und Evidence-Layer für SOV-1 bis SOV-6
- BSI 200-3 / IT-Grundschutz: Anschlussfähigkeit, Security-/Resilienz-Deep-Dive, Gefährdungs- und Vollständigkeitsreferenz
- Data Act: Exit/Switching/Portabilität, soweit anwendbar
- C5: Security-/Assurance-Evidence und C3A-Voraussetzung
- NIS2, DORA, DSGVO/EDPB, AI Act usw.: nur bei tatsächlicher Anwendbarkeit als Compliance-Overlay; sonst ggf. Methoden-/Fragenquelle

### Fragenlogik

Die Question Bank bleibt eine **adaptive Question Library**, kein Pflichtfragebogen.

Zielbild:

```text
vorhandene Artefakte / Provider Intelligence
  -> Vorbefüllung
  -> ca. 15–25 Screening-Fragen
  -> nur entscheidungsrelevante Deep Dives / ausgewählte Requirement Profiles
  -> Evidence / Claims / Risiken / Gates
  -> Variantenvergleich
  -> Entscheidungsvorlage / Empfehlung
```

Der Zielkorridor 15–25 ist eine interne Designhypothese und muss in NEXT-119 an Referenzfällen kalibriert werden.

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
- aktuelle 0–4-Level und acht Gate-Domänen sind interne MVP-Operationalisierung, keine C3A-/EU-Skala

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

Die Runtime ist aktuell **pre-v0.4** hinsichtlich DecisionCase/ArchitectureOptions, Status-quo-/Business-Value-Vergleich, Requirement Profiles, sieben sichtbaren Decision Dimensions und stark verkleinertem Screeningkern.

## Aktuelle Reihenfolge

### 1. NEXT-118 / Issue #28 – erster operativer Schritt

Manuelle Consultant-Installation und Evaluation der vorhandenen Runtime auf einem frischen Zielsystem. Dabei explizit die Differenz zwischen pre-v0.4-UI und Zielmethodik dokumentieren.

### 2. NEXT-119 / Issue #67 – Methodenvalidierung

Methodenkern v0.4 an mehreren Referenzvarianten validieren; Screeningkern, Requirement-Profile-/Overlay-Aktivierung und Empfehlungsvorlage kalibrieren.

### 3. Erst danach größere Runtime-Migration

Schrittweise gemäß `docs/architecture/DECISION_SUPPORT_V0_4_ALIGNMENT.md`. Insbesondere keine voreilige Übernahme der heutigen C3A-Crosswalk-Einträge als globale Hard Gates.

## Parallel zulässig

- Security-Hardening, insbesondere Issue #25 / NEXT-117 und Issue #26
- Bugfixes
- Repository-/CI-Hygiene
- Provider-/Framework-Recherche ohne Vorwegnahme noch nicht validierter Scoringregeln

## Primäre Dokumente für den nächsten Agenten

1. `AGENTS.md`
2. `project/PROJECT_STATE.yaml`
3. dieses Handoff
4. `project/NEXT_ACTIONS.yaml`
5. `project/DECISIONS.yaml`
6. `docs/method/METHOD_CORE_V0_4_DE.md`
7. `docs/method/GLOSSARY_DE.md`
8. `docs/method/C3A_V1_0_REVIEW.md`
9. `data/method/c3a_v1_0_crosswalk.csv`
10. `docs/architecture/DECISION_CASE_AND_PROVIDER_INTELLIGENCE.md`
11. `docs/architecture/DECISION_SUPPORT_V0_4_ALIGNMENT.md`
12. `docs/architecture/INTAKE_AND_CONTEXT_SOURCES.md`
13. `docs/method/SOURCE_GUIDE.md`

`docs/history/` und Agent-Logs sind historische Nachweise, nicht die aktuelle Fachquelle. Repo-State schlägt Chatgedächtnis.
