# Project Handoff

## Kurzfassung

Der Souveränitätsradar besteht aus zwei getrennten Ebenen: **Methodenkern** (cloud-agnostische Assessment-Methode) und **Produkt** (lokal installierbare Consultant-Webanwendung). Die Excel-Arbeitsmappe v1.0 ist Methoden-/Entwicklungsreferenz, nicht operative Benutzeroberfläche.

MVP-01A und NEXT-111 Guided Workflow sind auf `main`. Die NEXT-112-Core-Foundation **Evidence → Claim → Hard Gate** ist ebenfalls auf `main`. Aktueller Development-Fokus ist die Persistenz/API/UI der acht Hard Gates.

## Produktarchitektur

MVP-01 verwendet React/TypeScript/Vite, FastAPI, PostgreSQL, lokalen Dokument-Speicher `.runtime/`, Docker Compose und eine Copy/Paste **LLM Bridge** ohne API-Keys. Nicht im MVP: LiteLLM, n8n, LangGraph, Keycloak, S3, Kubernetes/GitOps.

Consultant-Workflow:

```text
Assessment
  -> Scope / Kritikalität / CIA
  -> Relevanzprofil
  -> Guided Questions
  -> Evidence erfassen und reviewen
  -> optional LLM Bridge
  -> Human-reviewed Claims
  -> Hard Gates PASS / FAIL / UNVERIFIED / N/A
  -> Risks / Management Ergebnis
```

## Evidence → Claim → Hard Gate

Roh-Evidence oder LLM-Proposals wirken **nie direkt** auf einen Gate-Zustand.

Ein Gate wird ausschließlich aus human-bestätigten Claims und geprüfter Evidence deterministisch ausgewertet:

- `Claim.review_status` muss `reviewed` oder `approved` sein.
- Capability-Claims nutzen das interne Radar-Level 0–4.
- Jeder Capability-Claim benötigt reviewed/approved Evidence, damit Evidence Trust ableitbar ist.
- Mehrere bestätigte Capability-Claims werden konservativ aggregiert: die schwächste Capability begrenzt das Gate.
- Pro Claim kann der stärkste passende Nachweis tragen; der Gate-Trust wird durch den schwächsten belegten Capability-Claim begrenzt.
- Fehlende oder nicht ausreichend geprüfte Evidence bleibt `UNVERIFIED`.
- Requirement 0 ergibt `N/A`.
- Technisches Requirement unterschritten ergibt `FAIL`, auch bei starker Evidence.

Diese Aggregation ist interne Operationalisierung (`INT-03`), keine externe Normformel.

## Gate Requirements

Die R4-Templates werden im MVP nach Kritikalität vorbelegt:

- low → Basis
- medium → Standard
- high → Elevated
- critical → Critical

Das ist **nur eine interne Startkonfiguration**. Der Berater kann jedes Gate auf Basis von Rechtslage, Schutzbedarf, Policy und Risikoappetit auf 0–4 überschreiben. Overrides werden als `consultant-override` gespeichert.

## Acht Hard Gates

1. HG-01 Jurisdiktion & Effective Control
2. HG-02 Datenresidenz & Verarbeitung
3. HG-03 Schlüsselhoheit
4. HG-04 Exit & Portabilität
5. HG-05 Operational Autonomy
6. HG-06 Identity & Trust Anchors
7. HG-07 Supply Chain Critical Dependencies
8. HG-08 Security Minimum

Die fachliche Source-of-Truth bleibt `data/method/r4_hard_gates.csv`; akzeptable Evidence/Follow-ups stehen in `data/method/evidence_request_catalog.csv`.

## Aktueller Branch

`feature/next-112-gate-api-ui`

Bereits umgesetzt:

- PostgreSQL-Persistenz für `EvidenceReview`, `AssessmentClaim`, `GateRequirement`
- Evidence Review mit Applied State, Base Trust, Scope Fit, Freshness Fit und Review Status
- Claim CRUD mit Gate-/Evidence-/Question-Links und Human Review State
- Gate-Requirement Defaults + Consultant Override
- API für alle acht Gate-Auswertungen inklusive Reasons und Evidence Requests
- Consultant-UI: Evidence Review, Hard-Gate-Karten, Requirement-Override, Claim-Erfassung und Ergebnisübersicht
- API-Tests für PASS/FAIL/UNVERIFIED, Human-Review-Grenzen und ungültige Links

Noch vor Merge zu erledigen: CI prüfen, etwaige Fehler korrigieren, Projektstate/Agent-Log finalisieren, Self-Review und Merge.

## Regeln für andere Agenten

- `AGENTS.md` zuerst lesen.
- Keine Cloud-Credentials anfordern.
- Keine LLM API im MVP-01 ohne neue Decision einführen.
- Keine Provider-spezifische Logik in Gate-/Rule-Core einbauen.
- Raw Kundenevidence nie committen.
- LLM-Proposals niemals automatisch als reviewed Claim oder Answer übernehmen.
- Fehlende Evidence niemals automatisch als FAIL interpretieren.
- Requirement-Defaults niemals als regulatorische Vorgabe darstellen.
- Unklare Applicability nie still ausblenden.
- `./uninstall.sh` muss alle erzeugten Runtime-Daten löschen können.
- substantielle Änderungen über Issue/Branch/PR/CI/Agent-Log führen.

## Danach

Nach NEXT-112 sollte zuerst ein vollständiger synthetischer Consultant-Durchlauf auf einer sauberen Installation erfolgen, bevor weitere methodische oder technische Komplexität ergänzt wird. Damit prüfen wir, ob der reale Beratungsworkflow verständlich und vollständig ist.
