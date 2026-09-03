# AGENTS.md – verbindliche, modellneutrale Arbeitsanweisung

Diese Datei ist die **kanonische Arbeitsanweisung** für alle KI-Agenten, Coding-Agenten und automatisierten Reviewer in diesem Repository.

## 1. Startsequenz – immer zuerst

Vor Planung oder Änderung in dieser Reihenfolge lesen:

1. `AGENTS.md`
2. `project/PROJECT_STATE.yaml`
3. `project/HANDOFF.md`
4. `project/NEXT_ACTIONS.yaml`
5. `project/DECISIONS.yaml`
6. relevante Dateien unter `docs/`, `data/`, `config/`, `schemas/`
7. offene Issues und PRs, sofern GitHub-Zugriff vorhanden ist

Repo-State schlägt Chatgedächtnis. Nicht aus älteren Chats rekonstruieren, wenn das Repository eine aktuelle Aussage enthält.

## 2. Source of Truth

Priorität bei Konflikten:

1. tatsächlich geprüfte externe Primärquellen / regulatorische Originaldokumente
2. akzeptierte ADRs und `project/DECISIONS.yaml`
3. aktuelle maschinenlesbare Methodik unter `data/method/` und `config/`
4. `project/PROJECT_STATE.yaml`
5. Methodendokumentation
6. Agenten-Session-Logs

Widersprüche nicht still auflösen: Konflikt dokumentieren und Review auslösen.

## 3. Projektarchitektur – nicht verhandelbare Grundsätze

- **cloud-agnostischer Methodenkern**: keine AWS-/Azure-/GCP-spezifische Regel darf den Kern dominieren.
- **kein Credential-/Root-Zugang als Voraussetzung**: Standard ist Customer-mediated Evidence.
- **Provider Adapter sind Übersetzer**, nicht Risk Engines.
- **Security und Souveränität getrennt** bewerten.
- **Provider Capability ≠ Applied Capability**.
- **Evidence Confidence ≠ Risikohöhe**.
- **Gate first, score second**.
- fehlende Information = `UNVERIFIED`, nicht automatisch `FAIL`.
- Risikoakzeptanz und Legal-Schlussfolgerungen bleiben menschliche Entscheidungen.

## 4. Agentenrollen

Ein Agent nennt pro Task mindestens eine Rolle:

- `researcher` – Quellen, Fundstellen, Versionen
- `methodologist` – Risiko-/Souveränitätsmethodik
- `architect` – Domain-, Evidence-, Tool-/Integrationsarchitektur
- `developer` – Code, Schema, Tests
- `reviewer` – unabhängige Prüfung
- `evidence-analyst` – Evidence Intake, Claims, Scope/Trust
- `project-coordinator` – Issues, Handoffs, State/Roadmap

Implementierer und Reviewer desselben substantiellen Changes sollen nach Möglichkeit getrennt sein. Self-Review muss als solcher markiert werden.

## 5. Planungsprotokoll

Vor substantiellen Änderungen dokumentieren:

- Ziel / Problem
- Scope und Nicht-Scope
- Rolle
- betroffene Dateien
- Quellen-/Provenienzbedarf
- Daten-/Security-Risiko
- Akzeptanzkriterien
- Tests und Reviewklasse

Danach umsetzen. Große Umbauten ohne Issue/Plan vermeiden.

## 6. Provenienzpflicht

Jede neue fachliche Regel, Frage, Risikokategorie, Formel oder Schwelle erhält eine Provenienzklasse:

- `external-direct`
- `external-derived`
- `internal-method`
- `project-assumption`
- `evidence-observation`

Source-ID/Fundstelle referenzieren. Interne Schwellen tragen `INT-01`/`INT-02` oder eine spätere interne Decision-ID. Eigene Regeln niemals als Normtext ausgeben.

## 7. Evidence-Regeln

Evidence-Zustände:

`asserted -> documented -> observed/configured -> tested -> attested`

Provider-/Service-Fähigkeit kann zusätzlich `available` sein.

Pflichtprinzipien:

- Provider-Dokumentation belegt primär `available`/`documented` Service Capability.
- Applied Capability benötigt kundenspezifische Evidence.
- Customer Evidence wird bevorzugt als **Evidence Pack** übergeben.
- keine Cloud-Credentials, Tokens oder Root-/Owner-Zugänge als Standardanforderung.
- vom Kunden erzeugte Exporte sind erlaubt und bevorzugt, sofern redigiert/scope-klar.
- Evidence enthält mindestens Quelle, Scope, Zeit/Version, Trust, Scope Fit, Applied State.
- Raw Kundenevidence nicht in Git committen.

## 8. Provider-Agnostik

Der Methodenkern arbeitet mit generischen Objekten und Capabilities. Beispiele:

- `KeyControlCapability` statt nur AWS KMS / Azure Key Vault / GCP Cloud KMS
- `IdentityTrustAnchor` statt providergebundener IAM-Begriffe
- `DataLocationConstraint` statt einzelner Region-API
- `ExitPortabilityCapability`
- `OperationalAutonomyCapability`
- `ProviderDependency` / `CommonCauseGroup`

Provider Adapter dürfen:

- öffentliche Providerbegriffe auf generische Felder mappen
- vom Kunden bereitgestellte Exporte parsen
- Folgefragen erzeugen

Provider Adapter dürfen **nicht**:

- eigene Hard-Gate-Schwellen erfinden
- automatisch Kundenaccounts scannen
- Credentials verlangen
- Risikoakzeptanz treffen

## 9. Softwareentwicklung

- deterministische Regeln in Code/Config, nicht nur Prompts
- neue Regeln mit Unit-/Boundary-Tests
- Schemas rückwärtskompatibel oder mit Migration
- keine Secrets/Kundendaten
- Evidence-Pack-Parser arbeitet lokal und dateibasiert
- Parser dürfen keine externen Systeme kontaktieren, außer ausdrücklich als separater Research-/Adapter-Task

## 10. Git- und Review-Workflow

- `main` stabil und handoff-fähig halten
- Branches: `feature/`, `fix/`, `research/`, `method/`, `docs/`, `chore/`
- substantielle Änderungen per PR
- PR enthält: Ziel, Änderungen, Quellen/Provenienz, Tests, Risiken, Handoff-Auswirkung
- kein Merge mit `BLOCKER`

Reviewklassen stehen in `docs/project/REVIEW_PROCESS.md`.

## 11. Multi-Agent-Koordination

- ein Issue = eine primäre Outcome-Verantwortung
- Agent schreibt vor Start kurz in Issue/Branch, welchen Scope er übernimmt
- parallele Agenten vermeiden dieselben State-/Methoden-Dateien
- `PROJECT_STATE.yaml` ist kein Chatlog; nur Gesamtzustand
- Details in `project/agent-log/`
- Handoff muss explizit sagen: erledigt, offen, Entscheidungen, nächste Dateien/Tests

## 12. Abschluss eines Tasks

Vor Ende:

1. Tests/Validator ausführen.
2. Provenienz prüfen.
3. offene Punkte benennen.
4. Session-Log schreiben/aktualisieren.
5. Handoff/State/NEXT_ACTIONS nur bei echter Zustandsänderung aktualisieren.
6. PR-Review-ready machen.

## 13. Sicherheits-Stopps

Sofort stoppen/eskalieren bei:

- Secret-/Credential-Fund
- Anforderung nach Kunden-Root-/Owner-Zugang als Standardlösung
- unklarer Lizenzlage bei Volltextübernahme
- regulatorischer Behauptung ohne belastbare Quelle
- automatischer Risikoakzeptanz
- Kundendaten in GitHub/Issues/PRs

## 14. Kommunikationsstandard

Kennzeichne Aussagen als:

- **Fact** – belegt
- **Observation** – aus Evidence beobachtet
- **Assumption** – Annahme
- **Inference** – methodische Ableitung
- **Decision** – akzeptierte Projektentscheidung
- **Open** – offen

Der nächste Agent muss ohne Chatkontext verstehen können, warum der Stand so ist.
