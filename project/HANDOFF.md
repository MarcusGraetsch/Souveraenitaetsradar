# Project Handoff

## Kurzfassung

Der Souveränitätsradar hat einen cloud-agnostischen Methodenkern und eine lokal installierbare Consultant-Webanwendung. Excel v1.0 bleibt Methodenreferenz, nicht operative UI.

NEXT-112 und NEXT-114 sind auf `main`. NEXT-114 hat den vollständigen installierten Consultant-Durchlauf erfolgreich validiert und dabei als wichtigstes UX-Finding gezeigt, dass beim komplexen KI-Agenten **124 von 128 Fragen** im bisherigen Standardpfad lagen: 83 `applicable`, 41 `needs_review`, 4 `not_applicable`.

**NEXT-115 / Issue #20 ist jetzt implementiert und bereit für PR-/CI-Review.** Die Lösung verändert die Applicability nicht, sondern ergänzt eine separate, deterministische Arbeitspriorisierung.

## Consultant-Workflow

```text
Assessment
  -> Scope / Kritikalität / CIA
  -> Relevanzprofil
  -> Progressive Questions
       -> Screening / jetzt beantworten
       -> Klärung nötig
       -> Deep Dive
       -> Erledigt
       -> Alle Fragen / Audit
  -> Evidence erfassen
  -> Evidence Review / Trust
  -> optional LLM Bridge
  -> Human-reviewed Claims
  -> Gate Requirements prüfen/überschreiben
  -> Hard Gates PASS / FAIL / UNVERIFIED / N/A
  -> Ergebnis
```

## NEXT-115 – verbindliche Workflow-Regeln

Applicability und Workflow Stage sind **zwei getrennte Zustände**.

Applicability:

- `applicable`
- `needs_review`
- `not_applicable`

Workflow Stage:

- `screening`
- `clarification`
- `deep_dive`
- `completed`
- `excluded`

Interne MVP-Operationalisierung `INT-03`:

1. `not_applicable` → `excluded`; bleibt in der Audit-Ansicht sichtbar.
2. Bereits beantwortete Frage → `completed`; bleibt in der Audit-Ansicht sichtbar.
3. `needs_review` → immer `clarification`; keine stille Filterung.
4. `applicable` + Pflichtgrad Basis bzw. Scope-Domäne → `screening`.
5. übrige `applicable` Fragen → `deep_dive`.

Die Stage ist Arbeitsreihenfolge/UX, keine Risikologik und keine normative Vorgabe. Ein LLM darf weder Applicability noch Stage deterministisch entscheiden.

## Neue Produktbausteine

Branch: `feature/next-115-progressive-guided-workflow`
Issue: #20

Implementiert:

- `WorkflowStage` und `WorkflowStageResult` im Applicability-Core
- getrennte `evaluate_workflow_stage(...)`-Logik
- `apply_to_questions(...)` berücksichtigt bereits beantwortete Fragen
- API-Views für `work`, `screening`, `clarification`, `deep_dive`, `completed`, `relevant`, `all`
- `/api/assessments/{id}/question-workflow` mit Stage-, Applicability- und Domänenzahlen
- Consultant-UI mit Stage-Navigation statt einer einzigen fast vollständigen Fragenliste
- sichtbare Klärungsqueue für `needs_review`
- vollständige Audit-/All-Questions-Ansicht
- Unit- und API-Regressionstests
- Real-Method-Bank-Test gegen alle 128 Fragen
- `tools/validation/progressive_workflow_validation.py` als installierter End-to-End-Test
- CI erweitert, damit NEXT-114 weiterhin als Regressionstest läuft und NEXT-115 einen eigenen maschinenlesbaren Report erzeugt

## Baseline und Akzeptanz

Die NEXT-114-Fachbaseline darf sich nicht verändern:

- Gesamt: 128
- relevant: 124
- `applicable`: 83
- `needs_review`: 41
- `not_applicable`: 4

NEXT-115 muss zusätzlich zeigen:

- alle 41 `needs_review` liegen sichtbar in `clarification`
- `screening` ist nicht leer
- `deep_dive` ist nicht leer
- unmittelbare Arbeitsqueue ist kleiner als der alte relevante 124er-Pfad
- eine beantwortete Screening-Frage wechselt in `completed`
- alle 128 Fragen bleiben in `all` erhalten
- ein einfacher Public-Content-Workload hat einen deutlich kleineren relevanten und unmittelbaren Arbeitsumfang als der komplexe KI-Agent

Die exakten Stage-Zahlen werden aus dem CI-Artifact des NEXT-115-Validierungslaufs übernommen und danach in PROJECT_STATE/NEXT_ACTIONS dokumentiert.

## Verbindliche Gate-Regeln bleiben unverändert

- Roh-Evidence oder LLM-Proposals wirken niemals direkt auf Gates.
- Nur `reviewed`/`approved` Claims wirken.
- Capability-Claims nutzen das interne Radar-Level 0–4.
- Jeder Capability-Claim benötigt reviewed/approved Evidence für eine verifizierte Aussage.
- Mehrere Claims werden konservativ aggregiert: schwächste bestätigte Capability begrenzt das Gate.
- Fehlende/unzureichende Evidence bleibt `UNVERIFIED`.
- Requirement 0 ergibt `N/A`.
- Technische Unterschreitung ergibt `FAIL`, auch bei starker Evidence.
- Gate-Requirement-Defaults bleiben interne Startkonfigurationen und keine Normvorgaben.

## Regeln für andere Agents

- `AGENTS.md` zuerst lesen.
- Keine Kunden-Cloud-Credentials anfordern.
- Keine LLM API im MVP ohne neue Decision.
- Keine Provider-spezifische Logik in Gate-/Rule-Core.
- Raw Kundenevidence nie committen.
- LLM-Proposals niemals automatisch als reviewed Claim/Answer übernehmen.
- Fehlende Evidence niemals automatisch als FAIL interpretieren.
- `needs_review` niemals still ausblenden.
- Workflow Stage niemals als Ersatz für Applicability verwenden.
- beantwortete oder ausgeschlossene Fragen aus der Audit-Ansicht nicht entfernen.
- LLM niemals zum deterministischen Applicability-/Stage-Entscheider machen.
- Alle 128 Fragen müssen über die Audit-/All-Questions-View inspizierbar bleiben.
- substantielle Änderungen via Issue/Branch/PR/CI/Agent-Log.

## Nächster Schritt

1. NEXT-115 PR gegen `main` öffnen.
2. vollständige CI prüfen: Python/Core/API, Frontend, Compose, NEXT-114 Regression und NEXT-115 Progressive Workflow.
3. NEXT-115 Artifact auswerten und exakte Stage-Zahlen dokumentieren.
4. echte Findings als separate Issues erfassen; Testkriterien nicht zur Grünfärbung abschwächen.
5. nach Self-Review und grüner CI squash-mergen und Issue #20 schließen.
6. danach NEXT-113 (Backup/Export/Consultant Report) als nächsten Produktbaustein starten.
