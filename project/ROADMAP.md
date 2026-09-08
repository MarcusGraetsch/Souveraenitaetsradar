# Roadmap

Status: **aktuelle Projektroadmap**  
Stand: 2026-09-08

Historische Detailentwicklung R1–R6 liegt in `docs/history/R1_R6_HISTORY.md` und den Agent-Logs. Diese Roadmap beschreibt den **aktuellen** Ziel- und Arbeitsstand.

## Bereits erreicht

### Methoden- und Evidence-Basis

- BSI-200-3-Crosswalk und elementare Gefährdungen als Referenz/Deep-Dive-Bestand
- zusätzliche Souveränitätsrisiken `G z.S1–G z.S12`
- Question Bank mit 128 atomaren Fragen als interne Wissens-/Deep-Dive-Bibliothek
- Provenienz- und Evidence-Modell
- Security, Souveränität und Evidence Confidence getrennt
- Hard Gates / `PASS` / `FAIL` / `UNVERIFIED`
- Provider Capability ≠ Applied Capability
- Customer-mediated Evidence als Standard
- providerneutraler Evidence Request Catalog und Customer Evidence Pack
- erster Public-Provider-Evidence-Pilot mit Amazon Bedrock als Beispiel, nicht Providerfokus

### Produkt-MVP

Die Webanwendung ist **bereits implementiert** und lokal installierbar:

- React/Vite Consultant UI
- FastAPI Backend
- PostgreSQL
- Docker Compose + Install/Start/Stop/Test/Uninstall
- Guided Questions / Applicability / Progressive Workflow
- Evidence Intake und Human Review
- Evidence -> Claim -> Hard Gate
- Copy/Paste LLM Bridge ohne LLM-API-Pflicht
- Structured Export / Consultant Report / Backup / Restore

Die aktuelle Runtime ist technisch validiert, bildet aber noch nicht vollständig den neueren Decision-Support-Zielstand v0.4 ab.

## Aktueller fachlicher Zielstand: Methodenkern v0.4

Primäre Referenz: `docs/method/METHOD_CORE_V0_4_DE.md`.

Zielbild:

- Radar als **Decision-Support-System** für mehrere Betriebs-/Architekturvarianten eines Workloads
- `DecisionCase` + `ArchitectureOption`
- Status quo / Nichtstun als explizite Option, soweit sinnvoll
- Business-/Innovationsnutzen zusätzlich zu Risiken
- sieben sichtbare Entscheidungsdimensionen + separate Evidence Confidence
- adaptive Question Library statt 128-Fragen-Pflichtworkflow
- vorhandene Kundenartefakte + Interview als kombinierter Intake
- Provider Intelligence als wiederverwendbare, versionierte Provider-/Service-Evidence
- geopolitische Sorgen als prüfbare Szenarien, nicht als Länder-/Provider-Score
- BSI 200-3 als Anschluss-/Deep-Dive-/Vollständigkeitsreferenz
- EU-CSF/C3A als Provider-/Service-Souveränitätslayer
- Data Act für Exit/Switching
- NIS2/DORA/DSGVO/AI Act usw. nur bei tatsächlicher Anwendbarkeit als Compliance-Overlay

## Aktuelles Gate – NEXT-120 / Issue #68

**Vor weiterer fachlicher Methoden-, Schema-, Runtime- oder UI-Entwicklung:** vollständigen BSI-C3A-Kriterienkatalog gegen v0.4 prüfen.

Erwartete Outputs:

- C3A ↔ Methodenkern-v0.4-Gap-/Crosswalk
- Prüfung der Provider-Intelligence-Struktur
- Prüfung der sieben Entscheidungsdimensionen
- Prüfung von Hard Gates und `G z.S`-Risiken
- Kennzeichnung: direkt aus C3A / abgeleitet / interne Methode
- notwendige Änderungen an Methode, Glossar, Source Register und Decisions

Bis Abschluss ist das bisherige C3A-Mapping **vorläufig**.

## Danach – Methodenvalidierung

### NEXT-118 – manuelle Consultant-Evaluation

Die vorhandene Runtime aus Beratersicht bedienen und dokumentieren, wo die aktuelle UI den v0.4-Zielworkflow noch nicht abbildet.

Status nach dieser Hygiene: **wartet auf NEXT-120**.

### NEXT-119 – v0.4 Referenzfallvalidierung

Denselben Workload mindestens über folgende Varianten vergleichen:

- bestehendes On-Prem
- US-Hyperscaler in EU-Region
- deutscher/europäischer Provider
- optional hypothetische Sollarchitektur

Ziele:

- Screeningkern auf ca. 15–25 Fragen kalibrieren
- adaptive Deep-Dive-Trigger validieren
- Status-quo-/Business-Value-Betrachtung prüfen
- geopolitische Sorge in prüfbare Szenarien übersetzen
- Framework-/Compliance-Overlay-Aktivierung testen
- Empfehlungsvorlage aus Consultant-Sicht validieren

Status: **wartet auf NEXT-120**.

## Danach – schrittweise Runtime-Migration

Nur nach C3A-Review und Methodenvalidierung:

1. Question-Library-Metadaten / kleiner Screeningkern
2. `DecisionCase` / `ArchitectureOption` inkl. Status quo
3. Business-/Opportunity-Profil
4. sieben Managementdimensionen
5. Deep-Dive-/Compliance-Profile
6. `ContextSource` / Artefaktadapter
7. geopolitische `RiskScenario`-Klassifikation
8. Decision Template / Empfehlungsausgabe
9. Provider-Intelligence-Runtime

Jeder Schritt benötigt Backward-Compatibility-, Boundary- und Provenienztests.

## Parallel zulässige Arbeiten

Arbeiten, die das fachliche Gate nicht vorwegnehmen:

- Security-Hardening (`NEXT-117`, Issue #25; Restore-Schema Issue #26)
- reine Bugfixes
- Repository-/CI-Hygiene
- Dokumentationsfehler
- unabhängige Quellensicherung ohne neue Methodenbehauptung

## Spätere Ausbaustufen

- Provider Adapter Library
- Vertrags-/Assurance-Dokument-Pipeline
- Provider Intelligence mit Freshness-/Drift-Monitoring
- CMDB-/ArchiMate-/ADOIT-/DataGerry-Adapter
- DORA-RoI-/andere Governance-Imports
- Portfolio-/Dependency-Graph für Konzentrationsrisiken
- Inter-Rater-Kalibrierung
- reale Kundenpiloten mit redigierter Evidence
- Continuous Reassessment aus versionierten Provider- und Kunden-Snapshots
- optional kontrollierte LLM-API-Integration nach eigener Entscheidung und Security-/Processing-Profil
