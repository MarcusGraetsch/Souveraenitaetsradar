# Project Handoff

## Kurzfassung

Der Souveränitätsradar hat einen cloud-agnostischen Methodenkern und eine lokal installierbare Consultant-Webanwendung. Excel v1.0 bleibt Methodenreferenz, nicht operative UI.

MVP-01A, Guided Workflow, Evidence Intake, providerneutrales Hard-Gate-Mapping und NEXT-112 sind auf `main`. PR #17 wurde nach grüner CI als Squash-Merge `85caf27f091ed728585c1db969eb325695f7e1db` integriert.

**NEXT-114 ist erfolgreich durchlaufen.** GitHub Actions Run `33789278423` war in allen vier Jobs grün, einschließlich des vollständigen Clean-Checkout-Consultant-Lifecycle-Tests. Das wichtigste Finding ist jetzt NEXT-115 / Issue #20: bei einem komplexen KI-Agenten lagen 124 von 128 Fragen im Standardpfad. Der nächste P0-Schritt ist deshalb ein progressiv priorisierter Guided Workflow – ohne Unsicherheit zu verstecken.

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

## NEXT-114 – Ergebnis

Branch/PR: `feature/next-114-synthetic-walkthrough` / #19
Issue: #18
CI Run: `33789278423`
Artifact: `synthetic-consultant-walkthrough`, ID `9906680972`

Resultate des synthetischen providerneutralen KI-Agent-Falls:

- Methodenfragen gesamt: 128
- Standardpfad: 124
- davon `applicable`: 83
- davon `needs_review`: 41
- HG-01 → **PASS**
- HG-03 → **FAIL**
- HG-04 → **UNVERIFIED**
- übrige Gates → N/A im isolierten Gate-Test
- zwei Evidence-Objekte mit Effective Trust 4
- drei human-reviewed Capability Claims plus ein draft Negativkontroll-Claim
- LLM Proposal erfolgreich importiert; Claim Count blieb 4 → 4
- Gate States blieben nach LLM Import unverändert
- Installation, Stop, Restart, Health-Test und vollständige Deinstallation erfolgreich
- `.runtime` und `.env` nach Uninstall entfernt; keine Radar-Container verblieben

Vollständige Dokumentation:
- `docs/validation/NEXT_114_SYNTHETIC_WALKTHROUGH.md`
- `docs/validation/NEXT_114_RESULT_2026-09-03.md`
- `project/agent-log/2026-09-03_next-114-synthetic-walkthrough.md`

**Wichtig:** Alle Merkmale und Gate Overrides des NEXT-114-Falls sind Testannahmen. Keine Providerbewertung und keine regulatorischen Mindestwerte daraus ableiten.

## NEXT-115 – nächster P0

Issue #20: `Guided Workflow progressiv priorisieren (KI-Agent: 124/128 aktiv)`.

Das Finding ist kein Fehler der konservativen Applicability-Regel: unklare Fragen wurden korrekt nicht versteckt. Das Produktproblem ist die Arbeitsorganisation. Bei komplexen Workloads sieht der Consultant fast die gesamte Fragenbank gleichzeitig.

Zielbild für NEXT-115:

```text
Stage 0  Scope / Relevanzprofil
Stage 1  Screening / Jetzt beantworten
Stage 2  Klärung nötig (needs_review sichtbar)
Stage 3  Deep Dive – deterministisch aktiviert
Stage 4  Alle Fragen / Audit View
```

Deep-Dive-Aktivierung darf nur nachvollziehbar aus Scope, bestehenden Answers, Evidence Gaps oder Gate State entstehen. Ein LLM darf Textvorschläge/Folgefragen unterstützen, aber nicht Applicability oder Workflow Stage deterministisch entscheiden.

Die Baseline für Regressionstests ist der NEXT-114-Fall: **124/128 im bisherigen Standardpfad, 83 applicable + 41 needs_review.** Zusätzlich muss ein einfacher Public-Content-Workload deutlich kürzer bleiben.

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
- `needs_review` niemals still ausblenden, nur sichtbar priorisieren/stufen.
- LLM niemals zum deterministischen Applicability-/Stage-Entscheider machen.
- Alle 128 Fragen müssen über die Audit-/All-Questions-View inspizierbar bleiben.
- `./uninstall.sh` muss alle erzeugten Runtime-Daten löschen können.
- substantielle Änderungen via Issue/Branch/PR/CI/Agent-Log.

## Nächster Schritt

PR #19 nach finalem grünen CI-Lauf mergen und NEXT-114 schließen. Danach auf einem eigenen NEXT-115-Branch die progressive Workflow-Staging-Logik implementieren. NEXT-113 (Backup/Export/Consultant Report) bleibt P1 dahinter.
