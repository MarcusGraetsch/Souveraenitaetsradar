# Souveränitätsradar

Der **Souveränitätsradar** ist ein Beratungs- und Softwareprojekt zur nachvollziehbaren Bewertung digitaler Souveränitätsrisiken von Cloud-, Plattform- und KI-Lösungen.

Das Projekt verbindet klassische Informationssicherheits-Risikoanalyse mit digitalen Souveränitätsdimensionen, regulatorischen Anforderungen, Evidenzbewertung und einer später KI-gestützten Assessment-Engine.

## Zielbild

Das Ergebnis soll nicht nur ein Fragebogen oder ein einzelner Score sein. Der Radar trennt bewusst:

1. **Provider / Service Capability** – welche souveränitäts- und sicherheitsrelevanten Fähigkeiten ein Dienst grundsätzlich anbietet.
2. **Applied Capability** – welche Fähigkeiten im konkreten Kunden- und Architekturkontext tatsächlich ausgewählt, konfiguriert, getestet oder auditiert sind.
3. **Workload Sovereignty Risk** – welches Souveränitätsrisiko für den konkreten Geschäftsprozess verbleibt.
4. **klassisches Informationssicherheits- und Betriebsrisiko** – damit „mehr Souveränität“ nicht automatisch als „mehr Sicherheit“ ausgegeben wird.
5. **Evidence Confidence** – wie belastbar die Aussagen sind.

Die Methode arbeitet nach dem Grundsatz **Gate first, score second**: nicht kompensierbare Mindestanforderungen werden vor einem gewichteten Vergleich geprüft.

## Aktueller Stand

**Projektphase:** R6 – technischer Evidence-Pilot  
**Methodenmodell:** v0.9  
**Status:** Methodik R1–R5 konsolidiert; read-only AWS-Bedrock-Evidence-Collector und Normalizer vorbereitet; echter autorisierter Account-Lauf steht aus.

Siehe:

- [`project/PROJECT_STATE.yaml`](project/PROJECT_STATE.yaml) – maschinenlesbarer aktueller Zustand
- [`project/HANDOFF.md`](project/HANDOFF.md) – Einstieg für neue Menschen und Agenten
- [`project/NEXT_ACTIONS.yaml`](project/NEXT_ACTIONS.yaml) – priorisierte nächsten Schritte
- [`AGENTS.md`](AGENTS.md) – verbindliche Arbeitsregeln für KI-Agenten
- [`docs/method/METHOD_OVERVIEW.md`](docs/method/METHOD_OVERVIEW.md) – fachliche Methodik
- [`docs/project/REVIEW_PROCESS.md`](docs/project/REVIEW_PROCESS.md) – Review- und Merge-Prozess
- [`data/method/`](data/method/) – maschinenlesbare Exporte des aktuellen Arbeitsmodells
- [`artifacts/method/README.md`](artifacts/method/README.md) – Hinweis zum binären Methoden-Workbook

## Repository-Struktur

```text
.
├── AGENTS.md                    # kanonische Agentenregeln
├── project/                     # Zustand, Roadmap, Handoffs, Entscheidungen
├── docs/
│   ├── method/                  # fachliche Methode
│   ├── architecture/            # Zielarchitektur und ADRs
│   ├── project/                 # Review, DoD, Release, PM-Regeln
│   └── history/                 # Entwicklung R1–R6
├── data/method/                 # maschinenlesbare Exporte aus dem Methodenmodell
├── config/rules/                # versionierte interne Default-Regeln
├── schemas/                     # JSON-Schemas für Tool-/API-Entwicklung
├── src/sovradar/                # erster deterministischer Methodenkern
├── tests/                       # Unit Tests für Regelengine
├── tools/aws-bedrock-evidence/  # R6 read-only Evidence Collector
├── artifacts/method/            # versioniertes Workbook
└── .github/                     # PR/Issue Templates, CODEOWNERS, CI
```

## Arbeitsprinzipien

- **Provenienzpflicht:** externe Quellen, interne Ableitungen und Projektannahmen werden getrennt ausgewiesen.
- **Keine Quellenwäsche:** eine interne Formel wird nicht als Normvorgabe dargestellt.
- **Deterministische Entscheidung vor generativer Erklärung:** Regeln, Gates und Evidence States sollen maschinenlesbar und testbar sein.
- **KI mit Human Review:** Agenten dürfen recherchieren, extrahieren, planen, entwickeln und Reviews vorbereiten; fachliche Risikoakzeptanz und produktive Freigabe bleiben menschliche Entscheidungen.
- **Keine stillen Annahmen:** fehlende Evidenz wird `UNVERIFIED`, nicht automatisch `PASS` oder `FAIL`.
- **Review vor Merge:** substanzielle Änderungen laufen über Branch + Pull Request.

## Schnellstart für Agenten

1. `AGENTS.md` vollständig lesen.
2. `project/PROJECT_STATE.yaml` lesen.
3. `project/HANDOFF.md` lesen.
4. `project/NEXT_ACTIONS.yaml` prüfen.
5. Relevante ADRs und Methodendokumente lesen.
6. Vor Änderungen bestehende Issues/PRs prüfen.
7. Nach Arbeit einen Session-Log unter `project/agent-log/` anlegen/aktualisieren und `project/PROJECT_STATE.yaml` nur ändern, wenn sich der Gesamtzustand tatsächlich geändert hat.

## Lizenz / externe Quellen

Externe Standards, regulatorische Dokumente und Provider-Inhalte werden nicht ungeprüft in das Repository kopiert. Das Repository speichert soweit möglich **Referenzen, Fundstellen, Ableitungen und eigene Arbeitsartefakte**. Bei lizenz- oder urheberrechtlich eingeschränkten Quellen ist der Originaltext außerhalb des Repositories zu beziehen.
