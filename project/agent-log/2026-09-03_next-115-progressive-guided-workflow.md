# Agent Session – NEXT-115 Progressive Guided Workflow

Datum: 2026-09-03
Rollen: methodologist, developer, reviewer
Issue: #20
Branch: `feature/next-115-progressive-guided-workflow`

## Ausgangslage

NEXT-114 wurde erfolgreich auf `main` integriert. Der vollständige synthetische Consultant-Durchlauf bestätigte die technische Funktionsfähigkeit des operativen Workflows, zeigte aber ein klares UX-/Methodik-Finding:

- 128 Methodenfragen gesamt
- 124 Fragen im bisherigen relevanten Pfad
- 83 `applicable`
- 41 `needs_review`
- 4 `not_applicable`

Die konservative Applicability war korrekt, aber die Arbeitsorganisation war unzureichend: ein komplexer KI-Agent präsentierte dem Consultant fast die gesamte Fragenbank gleichzeitig.

## Ziel

Den Fragenpfad progressiv priorisieren, ohne die bestehende Applicability zu verändern oder Unsicherheit zu verstecken.

## Methodische Entscheidung

Applicability und Workflow Stage sind getrennte Achsen.

Applicability bleibt:

- `applicable`
- `needs_review`
- `not_applicable`

Workflow Stage wird ergänzt:

- `screening`
- `clarification`
- `deep_dive`
- `completed`
- `excluded`

Interne MVP-Regel `INT-03`:

1. deterministisch `not_applicable` → `excluded`
2. beantwortet → `completed`
3. `needs_review` → `clarification`
4. `applicable` + Basis-Pflichtgrad oder Scope-Domäne → `screening`
5. übrige `applicable` → `deep_dive`

Workflow Stage ist reine Priorisierung und keine Risiko-/Normlogik.

## Implementiert

### Core

`src/sovradar/applicability.py`

- `WorkflowStage`
- `WorkflowStageResult`
- `evaluate_workflow_stage(...)`
- `apply_to_questions(...)` akzeptiert `answered_question_ids`
- stabile Sortierung nach Workflow Order, Domäne und Question ID

### API

`apps/api/app/main.py`

- bestehende Questions-API um Views erweitert:
  - `work`
  - `screening`
  - `clarification`
  - `deep_dive`
  - `completed`
  - `relevant`
  - `all`
- Antworten werden bei der Stage-Berechnung berücksichtigt
- neuer Endpoint `/api/assessments/{assessment_id}/question-workflow`
- Summary enthält Total, Relevant, Work Queue, Applicability Counts, Stage Counts und Domänenfortschritt

### Consultant UI

- Stage-spezifische Navigation
- unmittelbare Arbeitsqueue getrennt von Clarification und Deep Dive
- sichtbare `needs_review`-Queue
- Completed-Ansicht
- Audit-/All-Questions-Ansicht bleibt vollständig
- Stage-/Progress-Metriken werden sichtbar gemacht

### Tests

- Applicability-Regressionsfälle bleiben erhalten
- Workflow-Stage-Unit-Tests ergänzt
- Tests gegen die reale 128-Fragen-Methodenbank ergänzt
- API-Tests für neue Views/Summary ergänzt

### End-to-End-Validierung

`tools/validation/progressive_workflow_validation.py`

Der Runner arbeitet gegen die laufende installierte Anwendung und prüft:

- NEXT-114-Baseline bleibt exakt erhalten
- alle 41 `needs_review` erscheinen in Clarification
- Screening und Deep Dive existieren
- unmittelbare Work Queue ist kleiner als der bisherige relevante Pfad
- beantwortete Screening-Frage wechselt nach Completed
- alle 128 Fragen bleiben in All/Audit sichtbar
- einfacher Public-Content-Workload ist kürzer als der komplexe KI-Agent

CI wurde so erweitert, dass sowohl NEXT-114 als Regression als auch NEXT-115 ausgeführt und als JSON-Artefakte gespeichert werden.

## Governance

- keine LLM-Entscheidung über Applicability
- keine LLM-Entscheidung über Workflow Stage
- `needs_review` darf nicht versteckt werden
- Stage darf Applicability nicht überschreiben
- All-Questions/Audit View muss vollständige Methodenbank erhalten
- synthetische Testprofile sind keine Providerfakten

## Review-/Validierungsplan

1. PR gegen `main` öffnen.
2. vollständige CI abwarten.
3. NEXT-115 Artifact auswerten und exakte Stage Counts übernehmen.
4. bei echten Problemen separate Issues erstellen.
5. Self-Review durchführen.
6. nach grüner CI squash-mergen und Issue #20 schließen.

## Noch offen

Die MVP-Screeningregel `Basis/Scope → Screening`, sonstige applicable → Deep Dive ist bewusst einfach. Sie ist eine erste operative Priorisierung und muss später anhand realer Consultant-Fälle und Inter-Rater-Erfahrung kalibriert werden. Sie darf nicht als fachliche oder regulatorische Prioritätsvorgabe interpretiert werden.
