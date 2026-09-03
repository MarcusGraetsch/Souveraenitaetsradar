# Project Handoff

## Kurzfassung

Der Souveränitätsradar hat einen cloud-agnostischen Methodenkern und eine lokal installierbare Consultant-Webanwendung. Excel v1.0 bleibt Methodenreferenz, nicht operative UI.

MVP-01A, Guided Workflow, Evidence Intake, providerneutrales Hard-Gate-Mapping und NEXT-112 sind auf `main`. PR #17 wurde nach grüner CI als Squash-Merge `85caf27f091ed728585c1db969eb325695f7e1db` integriert.

Aktueller Fokus ist **NEXT-114 / Issue #18: vollständiger synthetischer Consultant-Durchlauf**. Vor weiteren Produktfeatures wird der gesamte Workflow inklusive Installation, Evidence Review, Claims, Hard Gates, LLM-Negativkontrolle sowie Stop/Start/Uninstall reproduzierbar validiert.

## Consultant-Workflow

```text
Assessment
  -> Scope / Kritikalität / CIA
  -> Relevanzprofil
  -> Guided Questions
  -> Evidence erfassen
  -> Evidence Review / Trust
  -> optional LLM Bridge
  -> Human-reviewed Claims
  -> Gate Requirements prüfen/überschreiben
  -> Hard Gates PASS / FAIL / UNVERIFIED / N/A
  -> Ergebnis
```

## Verbindliche Gate-Regeln

- Roh-Evidence oder LLM-Proposals wirken niemals direkt auf Gates.
- Nur `reviewed`/`approved` Claims wirken.
- Capability-Claims nutzen das interne Radar-Level 0–4.
- Jeder Capability-Claim benötigt reviewed/approved Evidence für eine verifizierte Aussage.
- Mehrere Claims werden konservativ aggregiert: schwächste bestätigte Capability begrenzt das Gate.
- Pro Claim kann der stärkste passende Nachweis tragen; Gate-Trust wird durch den schwächsten belegten Capability-Claim begrenzt.
- Fehlende/unzureichende Evidence bleibt `UNVERIFIED`.
- Requirement 0 ergibt `N/A`.
- Technische Unterschreitung ergibt `FAIL`, auch bei starker Evidence.
- Die Aggregation ist interne Operationalisierung `INT-03`, keine externe Normformel.

## Gate Requirements

MVP-Default nach Kritikalität:

- low → Basis
- medium → Standard
- high → Elevated
- critical → Critical

Das ist eine interne Startkonfiguration. Jeder Gate-Wert ist 0–4 editierbar und wird als `consultant-override` gespeichert. Niemals als gesetzliche oder normative Vorgabe darstellen.

## Acht Hard Gates

HG-01 Jurisdiktion & Effective Control; HG-02 Datenresidenz & Verarbeitung; HG-03 Schlüsselhoheit; HG-04 Exit & Portabilität; HG-05 Operational Autonomy; HG-06 Identity & Trust Anchors; HG-07 Supply Chain Critical Dependencies; HG-08 Security Minimum.

Fachliche Source-of-Truth: `data/method/r4_hard_gates.csv` und `data/method/evidence_request_catalog.csv`.

## Produktstatus

Implementiert auf `main`:

- React/Vite Consultant UI
- FastAPI + PostgreSQL
- lokaler Dokument-Speicher
- Install/Start/Stop/Test/Uninstall-Lifecycle
- Relevanzprofil + Guided Questions
- lokale Evidence-Erfassung
- Copy/Paste LLM Bridge
- Evidence Review mit Applied State und Trust-Dimensionen
- Claim CRUD mit Evidence-/Question-Links und Human Review
- Gate Requirement Defaults + Consultant Override
- acht Hard-Gate-Karten mit Reasons und Evidence Requests
- Ergebnisübersicht

## NEXT-114 – laufende Validierung

Branch: `feature/next-114-synthetic-walkthrough`
Issue: #18

Neue Validierungsartefakte:

- `tools/validation/synthetic_consultant_walkthrough.py`
- `docs/validation/NEXT_114_SYNTHETIC_WALKTHROUGH.md`
- `project/agent-log/2026-09-03_next-114-synthetic-walkthrough.md`
- CI-Job `consultant-walkthrough`

Der synthetische Fall ist ein providerneutraler KI-Agent mit sensiblen Fachdaten. **Alle Merkmale sind Testannahmen, keine Providerfakten.** Die Gate Requirements werden im Test bewusst überschrieben, damit die deterministische Regelkette isoliert geprüft werden kann:

- HG-01 → PASS
- HG-03 → FAIL
- HG-04 → UNVERIFIED
- übrige Gates → N/A im isolierten Test

Zusätzlich wird ein draft Capability-4-Claim für HG-03 als Negativkontrolle erzeugt. Er darf den reviewed Capability-1-Claim nicht überstimmen.

Die LLM Bridge wird ebenfalls als Negativkontrolle getestet: nach Import eines synthetischen Vorschlags müssen Claim-Anzahl und Gate-Ergebnisse unverändert sein.

CI validiert:

```text
Clean Checkout
  -> install.sh
  -> synthetischer Consultant-Durchlauf
  -> JSON Report
  -> stop.sh
  -> start.sh
  -> test.sh
  -> uninstall.sh mit DELETE
  -> Prüfung .runtime/.env/Container-Reste
  -> Report als Actions Artifact
```

## Regeln für andere Agenten

- `AGENTS.md` zuerst lesen.
- Keine Kunden-Cloud-Credentials anfordern.
- Keine LLM API im MVP ohne neue Decision.
- Keine Provider-spezifische Logik in Gate-/Rule-Core.
- Raw Kundenevidence nie committen.
- LLM-Proposals niemals automatisch als reviewed Claim/Answer übernehmen.
- Fehlende Evidence niemals automatisch als FAIL interpretieren.
- Requirement-Defaults und synthetische Overrides niemals als regulatorische Vorgabe darstellen.
- Synthetische Providermerkmale niemals zu realen Providerfakten umdeuten.
- Unklare Applicability nie still ausblenden.
- `./uninstall.sh` muss alle erzeugten Runtime-Daten löschen können.
- substantielle Änderungen via Issue/Branch/PR/CI/Agent-Log.
- NEXT-114 nicht durch Abschwächen der Expected States grün rechnen. Echte Findings als separate Issues dokumentieren.

## Nächster Schritt nach NEXT-114

Wenn der vollständige Walkthrough grün ist und keine Blocker offen bleiben, NEXT-114 schließen und mergen. Danach voraussichtlich NEXT-113 (Backup/Export/Consultant Report) priorisieren. Ein realer Provider-/Kundenpilot folgt erst auf einer validierten operativen Basis.
