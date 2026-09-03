# Project Handoff

## Kurzfassung

Der Souveränitätsradar hat zwei klar getrennte Ebenen: **Methodenkern** (cloud-agnostische Assessment-Methode) und **Produkt** (lokal installierbare Consultant-Webanwendung). Die Excel-Arbeitsmappe v1.0 bleibt Methoden-/Entwicklungsreferenz, ist aber nicht mehr die primäre Benutzeroberfläche.

MVP-01A ist auf `main` implementiert und per CI inklusive Docker-Compose-Smoke-Test validiert. Der aktuelle Development-Fokus ist **NEXT-111 / Guided Workflow**.

## Aktuelle Produktarchitektur

MVP-01 verwendet:

- React + TypeScript + Vite
- FastAPI
- PostgreSQL
- lokalen Dokument-Speicher `.runtime/`
- Docker Compose
- Copy/Paste **LLM Bridge** ohne API-Keys

Nicht im MVP: LiteLLM, n8n, LangGraph, Keycloak, S3, Kubernetes/GitOps.

Consultant-Workflow:

```text
Assessment
  -> Scope / Kritikalität / CIA
  -> Relevanzprofil
  -> Guided Questions
  -> Evidence
  -> LLM Bridge
  -> Human Review
  -> Rule Engine / Hard Gates / Risks
  -> Management Ergebnis
```

## Guided Workflow / NEXT-111

Die 128 Methodenfragen sind **kein statischer Fragebogen**. Der Radar erzeugt einen Fragenpfad aus Assessment-Scope und einem separaten Relevanzprofil.

Das Relevanzprofil enthält generische Scope-Fakten, zum Beispiel:

- Service-Modell / Cloud-Bezug
- Datenverarbeitung und Persistenz
- Verschlüsselung und Schlüsselmodell
- KI / agentische KI
- Exit-/Portabilitätsrelevanz
- Backup/Restore
- Multi-Provider / Unterauftragnehmer
- IAM und Logging/Monitoring
- C5/C3A-Relevanz

Applicability wird deterministisch im Core ausgewertet:

- `applicable`
- `not_applicable`
- `needs_review`

**Wichtig:** Fehlender Kontext oder eine noch nicht operationalisierte natürliche Anwendbarkeitsregel führt zu `needs_review`. Die Frage bleibt sichtbar. Die Anwendung darf eine Frage nur aus dem Standardpfad entfernen, wenn sie sicher `not_applicable` ist.

Die UI bietet deshalb `Relevante Fragen` und `Alle Fragen`. Jede Frage zeigt den Applicability-Zustand und die Begründung.

Die LLM Bridge erhält nur offene `applicable`- und `needs_review`-Fragen. Das LLM entscheidet nicht über Applicability.

## Fachlicher Kern

Bewertet wird ein Workload in einer konkreten Provider-/Service-/Architektur-/Vertragskonstellation, nicht ein Provider pauschal.

Getrennte Bewertungsachsen:

- Provider / Service Capability
- Applied Capability
- Workload Sovereignty Risk
- klassisches Informationssicherheits-/Betriebsrisiko
- Evidence Confidence

Hard Gates:

1. Jurisdiktion & Effective Control
2. Datenresidenz & Verarbeitung
3. Schlüsselhoheit
4. Exit & Portabilität
5. Operational Autonomy
6. Identity & Trust Anchors
7. Supply Chain Critical Dependencies
8. Security Minimum

Fehlende Evidence bleibt `UNVERIFIED`; LLM-Vorschläge sind keine Entscheidungen.

## Verworfene / verschobene Ansätze

- Ein durch uns betriebener Cloud-Account-Collector ist nicht Zielarchitektur.
- Kunden-Root-/Owner-/Cloud-Credentials sind keine Voraussetzung.
- LLM-API-Integration ist für MVP-01 bewusst verschoben.
- Excel ist nicht mehr die operative Consultant-UI.
- Provider-spezifische Risikoregeln gehören nicht in den Core.

## Development-Status

- `NEXT-110` / Issue #11: MVP-01A Webapp-Skeleton – abgeschlossen auf `main`.
- `NEXT-111` / Issue #13: Guided Workflow und Question Applicability – aktueller Change.
- `NEXT-112`: Evidence -> Claim -> Hard Gate – nächster P0-Produkt-/Methodenschritt.
- `NEXT-113`: Backup/Export/Consultant Report.
- `NEXT-114`: vollständiger synthetischer Consultant-Durchlauf auf sauberer VM.

Die Methodentasks `NEXT-101` bis `NEXT-108` bleiben relevant. `NEXT-109` (CLI als primäre MVP-Oberfläche) ist zurückgestellt; CLI kann später als Test-/Automationsinterface bestehen.

## Regeln für den nächsten Agenten

- `AGENTS.md` zuerst lesen.
- Keine Cloud-Credentials anfordern.
- Keine LLM API im MVP-01 ohne neue Decision einführen.
- Keine Provider-spezifische Logik in den Rule-Core einbauen.
- Raw Kundenevidence nie committen.
- Keine LLM-Proposals automatisch als Answers übernehmen.
- Unklare Applicability nie still ausblenden.
- `./uninstall.sh` muss alle erzeugten Runtime-Daten löschen können.
- substantielle Änderungen über Issue/Branch/PR/CI/Agent-Log führen.

## Nächster Handoff nach NEXT-111

Nach grünem Merge von NEXT-111:

1. `NEXT-112` starten.
2. Evidence-Objekte und Human-reviewed Claims mit den acht Hard Gates verbinden.
3. `UNVERIFIED` bei fehlender Evidence beibehalten.
4. Service Capability und Applied Capability nicht vermischen.
5. Danach den ersten vollständigen synthetischen Beraterdurchlauf durchführen.
