# Agent Session – NEXT-115 Progressive Guided Workflow

Datum: 2026-09-03
Rollen: methodologist, developer, reviewer
Issue: #20
PR: #21
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

- Questions-API mit Views `work`, `screening`, `clarification`, `deep_dive`, `completed`, `relevant`, `all`
- Antworten werden bei der Stage-Berechnung berücksichtigt
- neuer Endpoint `/api/assessments/{assessment_id}/question-workflow`
- Summary enthält Total, Relevant, Work Queue, Applicability Counts, Stage Counts und Domänenfortschritt

### Consultant UI

- Stage-spezifische Navigation
- sichtbare Screening-, Clarification-, Deep-Dive- und Completed-Queues
- `needs_review` bleibt sichtbar
- Audit-/All-Questions-Ansicht bleibt vollständig
- Stage-/Progress-Metriken werden angezeigt

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
- Work Queue ist kleiner als der bisherige relevante Pfad
- beantwortete Screening-Frage wechselt nach Completed
- alle 128 Fragen bleiben in All/Audit sichtbar
- einfacher Public-Content-Workload ist im relevanten Gesamtpfad kürzer als der komplexe KI-Agent

CI führt NEXT-114 weiterhin als Regression aus und erzeugt zusätzlich den NEXT-115-Report.

## CI-Ergebnis

PR #21 löste GitHub Actions Run `33794873133` aus.

Alle Jobs erfolgreich:

- `python` → success
- `frontend` → success
- `compose-smoke` → success
- `consultant-walkthrough` → success
  - Clean Install → success
  - NEXT-114 Walkthrough → success
  - NEXT-115 Progressive Workflow → success
  - Stop/Restart/Test → success
  - vollständiger Uninstall → success
  - Report Upload → success

Artifact: `consultant-validation-reports`, ID `9908787146`.

## Validierte NEXT-115-Zahlen

### Komplexer KI-Agent – vor Antwort

- total 128
- relevant 124
- applicable 83
- needs_review 41
- not_applicable 4
- screening 44
- clarification 41
- deep_dive 39
- completed 0
- excluded 4
- work_queue 85

### Nach einer beantworteten Screening-Frage

- screening 43
- clarification 41
- deep_dive 39
- completed 1
- excluded 4
- work_queue 84

Question `OA-01` wechselte nach `completed`; `all` blieb bei 128.

### Public-Content-Fall

- total 128
- relevant 84
- applicable 43
- needs_review 41
- not_applicable 44
- screening 43
- clarification 41
- deep_dive 0
- completed 0
- excluded 44
- work_queue 84

Alle im Runner definierten Akzeptanzchecks sind `true`.

## Wichtiges Review-Finding

Die progressive Stufung funktioniert, aber die aktuelle `work_queue` kombiniert Screening und Clarification. Dadurch ist die unmittelbare Queue beim komplexen KI-Agenten 85 und beim Public-Content-Fall 84 – also nahezu gleich groß.

Das wurde **nicht als Erfolg umgedeutet**. Der relevante Gesamtpfad ist zwar bereits deutlich differenziert (124 vs. 84), aber die erste operative Queue braucht eine weitere Iteration.

Dafür wurde **NEXT-116 / Issue #22** angelegt:

`Screening und Klärungsqueue für einfache Workloads weiter reduzieren`.

Vorgesehene Richtung:

- `work` künftig stärker auf Screening begrenzen
- Clarification separat sichtbar halten
- Basis-/Domänenfragen deterministisch erst aus Scope, Answers, Evidence Gaps oder Gate State hochstufen
- einfache vs. komplexe Workloads schon in der ersten Arbeitsstufe deutlicher differenzieren

## Governance

- keine LLM-Entscheidung über Applicability
- keine LLM-Entscheidung über Workflow Stage
- `needs_review` darf nicht versteckt werden
- Stage darf Applicability nicht überschreiben
- All-Questions/Audit View muss vollständige Methodenbank erhalten
- synthetische Testprofile sind keine Providerfakten
- verbleibende UX-Schwächen werden als Findings dokumentiert statt Akzeptanzkriterien nachträglich weichzurechnen

## Abschluss / Nächster Schritt

NEXT-115 ist fachlich und technisch validiert. Vor Merge von PR #21 erfolgt noch der finale Self-Review und ein letzter CI-Lauf nach den State-/Handoff-Updates.

Danach:

1. PR #21 squash-mergen und Issue #20 schließen.
2. NEXT-113 als nächsten P0 starten: Backup, Export und Consultant Report.
3. NEXT-116 / Issue #22 als P1-UX-Verbesserung im Backlog behalten.
