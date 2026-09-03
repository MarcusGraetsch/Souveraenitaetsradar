# Project Handoff

## Kurzfassung

Der Souveränitätsradar hat zwei klar getrennte Ebenen: **Methodenkern** (cloud-agnostische Assessment-Methode) und **Produkt** (ab MVP-01 lokal installierbare Consultant-Webanwendung). Die Excel-Arbeitsmappe v1.0 bleibt Methoden-/Entwicklungsreferenz, ist aber nicht mehr die primäre Benutzeroberfläche.

## Aktuelle Produktentscheidung

MVP-01 verwendet React/TypeScript/Vite, FastAPI, PostgreSQL, lokalen Dokument-Speicher `.runtime/`, Docker Compose und eine Copy/Paste **LLM Bridge** ohne API-Keys. Nicht im MVP: LiteLLM, n8n, LangGraph, Keycloak, S3, Kubernetes/GitOps.

Consultant-Workflow:

```text
Assessment -> Scope/Kritikalität/CIA -> Fragen -> Evidence -> LLM Bridge -> Human Review -> Rule Engine/Hard Gates/Risks -> Management Ergebnis
```

## Fachlicher Kern

Bewertet wird ein Workload in einer konkreten Provider-/Service-/Architektur-/Vertragskonstellation, nicht ein Provider pauschal. Security Capability, Sovereignty Capability, Workload Sovereignty Risk, klassisches Informationssicherheits-/Betriebsrisiko und Evidence Confidence bleiben getrennt.

Hard Gates: Jurisdiktion & Effective Control; Datenresidenz & Verarbeitung; Schlüsselhoheit; Exit & Portabilität; Operational Autonomy; Identity & Trust Anchors; Supply Chain Critical Dependencies; Security Minimum.

Fehlende Evidence bleibt `UNVERIFIED`; LLM-Vorschläge sind keine Entscheidungen.

## Verworfene Ansätze

- Ein durch uns betriebener Cloud-Account-Collector ist nicht Zielarchitektur.
- LLM-API-Integration ist für MVP-01 bewusst verschoben.
- Excel ist nicht mehr die geplante operative Consultant-UI.

## Aktueller Development-Fokus

GitHub Issue #11 / `NEXT-110`: installierbarer End-to-End-Webapp-Skeleton.

Danach: `NEXT-111` dynamische Question Applicability; `NEXT-112` Evidence -> Claim -> Hard Gate; `NEXT-113` Backup/Export/Consultant Report; `NEXT-114` vollständiger synthetischer Consultant-Durchlauf auf sauberer VM.

Die Methodentasks `NEXT-101` bis `NEXT-108` bleiben relevant. `NEXT-109` (CLI als primäre MVP-Oberfläche) ist zurückgestellt; CLI kann später als Test-/Automationsinterface bestehen.

## Regeln für den nächsten Agenten

- `AGENTS.md` zuerst lesen.
- Keine Cloud-Credentials anfordern.
- Keine LLM API im MVP-01 ohne neue Decision einführen.
- Keine Provider-spezifische Logik in den Rule-Core einbauen.
- Raw Kundenevidence nie committen.
- Keine LLM-Proposals automatisch als Answers übernehmen.
- `./uninstall.sh` muss alle erzeugten Runtime-Daten löschen können.
- substantielle Änderungen über Issue/Branch/PR/CI/Agent-Log führen.
