# Project Handoff

## Kurzfassung

Der Souveränitätsradar hat einen cloud-agnostischen Methodenkern und eine lokal installierbare Consultant-Webanwendung. Excel v1.0 bleibt Methodenreferenz, nicht operative UI.

NEXT-112 und NEXT-114 sind auf `main`. NEXT-115 / Issue #20 ist jetzt implementiert und durch GitHub Actions Run `33794873133` vollständig grün validiert. PR #21 enthält die progressive Fragenpriorisierung.

Die bisherige Fachbaseline bleibt unverändert: beim komplexen KI-Agenten 128 Fragen gesamt, 124 relevant, 83 `applicable`, 41 `needs_review`, 4 `not_applicable`. Neu ist, dass diese Fragen nicht mehr als eine einzige Arbeitsliste behandelt werden, sondern in getrennte Workflow-Stufen fallen.

## Consultant-Workflow

```text
Assessment
  -> Scope / Kritikalität / CIA
  -> Relevanzprofil
  -> Progressive Questions
       -> Screening
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
  -> Export / Consultant Report  [NEXT-113]
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

## NEXT-115 – validierte Zahlen

CI Run: `33794873133`
Artifact: `consultant-validation-reports`, ID `9908787146`

### Komplexer KI-Agent

Vor einer Testantwort:

- total: 128
- relevant: 124
- applicable: 83
- needs_review: 41
- not_applicable: 4
- screening: 44
- clarification: 41
- deep_dive: 39
- completed: 0
- excluded: 4
- aktuelle work_queue: 85

Nach Beantwortung einer Screening-Frage:

- screening: 43
- completed: 1
- clarification: 41
- deep_dive: 39
- excluded: 4

Die beantwortete Frage `OA-01` wechselte deterministisch nach `completed`; die Audit-Ansicht blieb bei 128 Fragen.

### Öffentliche Inhaltswebsite

- total: 128
- relevant: 84
- applicable: 43
- needs_review: 41
- not_applicable: 44
- screening: 43
- clarification: 41
- deep_dive: 0
- completed: 0
- excluded: 44
- aktuelle work_queue: 84

Der relevante Gesamtpfad ist damit deutlich kürzer als beim komplexen KI-Agenten (84 vs. 124). Die unmittelbare Arbeitsqueue ist allerdings noch fast gleich groß (84 vs. 85), weil `work` aktuell Screening und Clarification zusammenfasst. Dieses Finding wurde **nicht verdeckt**, sondern als NEXT-116 / Issue #22 dokumentiert.

## NEXT-115 – technische Ergebnisse

Implementiert:

- `WorkflowStage` und `WorkflowStageResult` im Applicability-Core
- getrennte `evaluate_workflow_stage(...)`-Logik
- Questions-API mit `work`, `screening`, `clarification`, `deep_dive`, `completed`, `relevant`, `all`
- `/api/assessments/{id}/question-workflow` mit Stage-, Applicability- und Domänenzahlen
- Consultant-UI mit progressiver Navigation und sichtbarer Klärungsqueue
- Completed- und vollständige Audit-Ansicht
- Unit-/API-/Real-Method-Bank-Regressionschecks
- End-to-End-Runner `tools/validation/progressive_workflow_validation.py`
- CI führt NEXT-114 weiter als Regressionstest und NEXT-115 zusätzlich aus

Alle Jobs des Validierungslaufs waren grün:

- Python/Core/API
- Frontend Build
- Docker Compose Smoke
- NEXT-114 Consultant Walkthrough
- NEXT-115 Progressive Workflow
- Stop/Restart/Test/Uninstall

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

## Offenes UX-Finding – NEXT-116 / Issue #22

NEXT-115 löst die fehlende Stufung. Es löst noch nicht vollständig die Größe der unmittelbaren ersten Arbeitsqueue. Der Public-Content-Fall hat zwar deutlich weniger relevante Fragen, aber fast dieselbe `work_queue`, weil 41 `needs_review`-Fragen und viele Basisfragen sofort sichtbar bleiben.

NEXT-116 soll deshalb insbesondere prüfen:

- `work` nur aus einer kleineren Screening-Queue bilden
- Clarification separat sichtbar halten
- weitere Basis-/Domänenfragen erst durch Scope, Answers, Evidence Gaps oder Gate State aktivieren
- einfache und komplexe Workloads bereits in der ersten Consultant-Arbeitsstufe deutlicher unterscheiden

Das ist eine Produkt-/Methodenverbesserung, keine externe Normanforderung.

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
- alle 128 Fragen müssen über die Audit-/All-Questions-View inspizierbar bleiben.
- substantielle Änderungen via Issue/Branch/PR/CI/Agent-Log.

## Nächster P0-Schritt – NEXT-113

Nach Merge von PR #21 ist der nächste P0-Produktbaustein **Assessment Backup, Export und Consultant Report**.

Ziel:

1. Assessment vollständig und reproduzierbar sichern/exportieren.
2. Scope, Relevanzprofil, Antworten, Evidence-Metadaten/Reviews, Claims, Gate Requirements und Gate Results exportieren.
3. Raw Evidence nicht unbeabsichtigt in Reports einbetten.
4. Consultant Report strukturiert trennen in Fakten/Evidence, Capability/Gates, Risiken, Unsicherheit und Management-Entscheidungen.
5. Provenienz sichtbar halten.
6. Backup/Restore gegen synthetische Daten testen.
7. Export/Report darf keine Gate States verändern.

NEXT-116 / Issue #22 bleibt als P1-UX-Verbesserung parallel im Backlog.
