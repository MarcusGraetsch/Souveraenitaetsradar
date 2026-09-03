# AGENTS.md – verbindliche Arbeitsanweisung

Diese Datei ist die **kanonische, modellneutrale Arbeitsanweisung** für alle KI-Agenten und automatisierten Entwickler, die an diesem Repository arbeiten.

## 1. Startsequenz – immer zuerst

Vor Planung oder Änderung in dieser Reihenfolge lesen:

1. `AGENTS.md`
2. `project/PROJECT_STATE.yaml`
3. `project/HANDOFF.md`
4. `project/NEXT_ACTIONS.yaml`
5. `project/DECISIONS.yaml`
6. die für die Aufgabe relevanten Dateien unter `docs/`, `data/`, `config/` und `schemas/`
7. offene Issues/PRs, sofern Zugriff auf GitHub besteht

Nicht aus älteren Chatverläufen oder Modellgedächtnis rekonstruieren, wenn das Repository eine aktuelle Aussage enthält.

## 2. Source of Truth

Priorität bei Konflikten:

1. Primärquellen / regulatorische Originaldokumente, soweit im Source Register referenziert und tatsächlich geprüft
2. akzeptierte ADRs und `project/DECISIONS.yaml`
3. aktuelles Methodenmodell / maschinenlesbare Exporte unter `data/method/`
4. `project/PROJECT_STATE.yaml`
5. sonstige Dokumentation
6. Agenten-Session-Logs

Bei einem Widerspruch **nicht still korrigieren**. Konflikt dokumentieren und Review verlangen.

## 3. Rollen für Agenten

Ein Agent soll pro Task mindestens eine Rolle explizit einnehmen:

- `researcher` – Quellenrecherche, Fundstellen, Crosswalks
- `methodologist` – Risiko-/Souveränitätsmethodik
- `architect` – Daten-, Tool- und Integrationsarchitektur
- `developer` – Implementierung und Tests
- `reviewer` – unabhängige Prüfung; verändert den zu prüfenden Kern möglichst nicht gleichzeitig
- `evidence-analyst` – Evidence Extraction/Normalization
- `project-coordinator` – Issues, Handoffs, Status, Roadmap

Wenn ein Agent Implementierer **und** Reviewer desselben Changes wäre, ist das als Self-Review zu kennzeichnen. Für risikoreiche Änderungen ist ein zweiter unabhängiger Review vorzusehen.

## 4. Planen vs. Umsetzen

Vor substantiellen Änderungen:

- Ziel und Scope nennen.
- Betroffene Dateien nennen.
- Quellen-/Provenienzbedarf bestimmen.
- Risiken und offene Entscheidungen nennen.
- Tests/Review festlegen.

Danach darf umgesetzt werden, sofern die Aufgabe dies erlaubt.

Keine großflächigen Umbauten ohne nachvollziehbaren Plan oder Issue.

## 5. Provenienzpflicht

Jede neue fachliche Regel, Frage, Risikokategorie, Formel oder Schwelle muss einer Klasse zugeordnet werden:

- `external-direct` – direkte externe Vorgabe/Begriff
- `external-derived` – quellennah abgeleitet
- `internal-method` – eigenes Methodendesign
- `project-assumption` – Projekt-/Testszenario
- `evidence-observation` – Beobachtung aus konkreter Evidence

Dabei Source-ID/Fundstelle referenzieren. Interne Schwellen müssen `INT-01` oder eine spätere interne Decision-ID tragen.

**Verboten:** eigene Regeln so formulieren, als stünden sie in einer Norm.

## 6. Evidence-Regeln

- `available` ist nicht `configured`.
- `configured` ist nicht `tested`.
- `tested` ist nicht `attested`.
- fehlende Information = `UNVERIFIED`, nicht automatisch `FAIL`.
- Provider-Dokumentation belegt primär Provider-/Service-Capability.
- Applied Capability benötigt kunden-/ressourcenspezifische Evidence.
- Evidence muss mindestens Source, Scope, Zeit/Version und Trust/Confidence tragen.

R6-Technik-Evidence ist read-only zu erheben. Keine Fachdaten, Prompts, Log-Events oder S3-Objekte ohne expliziten Scope und Freigabe.

## 7. Entwicklung

- Deterministische Regeln gehören in Code/Config, nicht nur in Prompts.
- Jede neue Regel erhält Unit Tests, einschließlich Grenzwerte.
- Öffentliche Schnittstellen typisieren und dokumentieren.
- Keine Secrets, Tokens, Kundendaten oder Account-spezifischen sensitiven Evidence-Dumps committen.
- Raw Evidence grundsätzlich nicht ins Repo, sofern sie kunden-/accountbezogene Interna enthält.
- Keine produktiven Write-/Invoke-Operationen in Evidence Collectors ohne gesonderte Architekturentscheidung.

## 8. Git-Workflow

Standard:

- `main` soll reviewbar und stabil bleiben.
- Branches: `feature/...`, `fix/...`, `research/...`, `method/...`, `docs/...`, `bootstrap/...`.
- Substantielle Änderungen über PR.
- PR muss Ziel, Änderungen, Quellen/Provenienz, Tests, offene Risiken und Handoff enthalten.
- Kein Merge mit offenen `BLOCKER`-Reviewpunkten.

## 9. Review-Schwerpunkte

Reviewer prüfen mindestens:

1. Fachliche Richtigkeit und Quellenbezug
2. Keine unzulässige Verallgemeinerung
3. Provenienz korrekt gekennzeichnet
4. Security vs. Souveränität nicht vermischt
5. Evidence Confidence separat behandelt
6. Hard Gates nicht durch Score kompensiert
7. Code-/Formeltests vorhanden
8. Datenschutz/Secrets/Evidence-Sensitivität
9. Rückwärtskompatibilität von Datenmodellen
10. Dokumentation/Handoff aktualisiert

## 10. Abschluss eines Agenten-Tasks

Vor Ende:

- Tests/Validierung ausführen.
- Änderungen zusammenfassen.
- Offene Punkte nennen.
- `project/agent-log/YYYY-MM-DD_<kurzthema>.md` anlegen oder aktualisieren.
- Falls nötig `project/HANDOFF.md`, `PROJECT_STATE.yaml` und `NEXT_ACTIONS.yaml` aktualisieren.
- Keine erledigten Punkte als offen stehen lassen und keine offenen Punkte still als erledigt markieren.

## 11. Sicherheits-Stopps

Sofort stoppen/eskalieren bei:

- Secret-/Credential-Fund
- produktivem Write-/Delete-/Invoke-Risiko ohne Freigabe
- unklarer Lizenzlage bei Volltextübernahme
- regulatorischer Behauptung ohne belastbare Quelle
- automatischer Risikoakzeptanz ohne menschliche Entscheidung
- Kundendaten in Repo/Issue/PR

## 12. Kommunikationsstandard

Berichte knapp, prüfbar und differenziert:

- **Fact** – belegt
- **Observation** – aus Evidence beobachtet
- **Assumption** – Annahme
- **Inference** – methodische Ableitung
- **Decision** – akzeptierte Projektentscheidung
- **Open** – noch zu klären

Der nächste Agent soll ohne vorherigen Chat verstehen können, warum der aktuelle Stand so ist.
