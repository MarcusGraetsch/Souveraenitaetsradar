# AGENTS.md – verbindliche, modellneutrale Arbeitsanweisung

Diese Datei ist die **kanonische Arbeitsanweisung** für alle KI-Agenten, Coding-Agenten und automatisierten Reviewer in diesem Repository.

## 1. Startsequenz – immer zuerst

Vor Planung oder Änderung in dieser Reihenfolge lesen:

1. `AGENTS.md`
2. `project/PROJECT_STATE.yaml`
3. `project/HANDOFF.md`
4. `project/NEXT_ACTIONS.yaml`
5. `project/DECISIONS.yaml`
6. `docs/method/METHOD_CORE_V0_4_DE.md` und `docs/method/GLOSSARY_DE.md`, sofern der Task die aktuelle Fachmethode betrifft
7. bei C3A-Bezug zusätzlich `docs/method/C3A_V1_0_REVIEW.md` und `data/method/c3a_v1_0_crosswalk.csv`
8. relevante Dateien unter `docs/`, `data/`, `config/`, `schemas/`
9. offene Issues und PRs, sofern GitHub-Zugriff vorhanden ist

Repo-State schlägt Chatgedächtnis. Nicht aus älteren Chats rekonstruieren, wenn das Repository eine aktuelle Aussage enthält.

## 2. Source of Truth

Das Repository unterscheidet bewusst zwischen **externer Fachquelle**, **fachlichem Zielmodell** und **aktuell implementierter Runtime**.

Priorität bei fachlichen Konflikten:

1. tatsächlich geprüfte externe Primärquellen / regulatorische Originaldokumente – aber nur für Aussagen, die diese Quelle tatsächlich trägt
2. akzeptierte ADRs und `project/DECISIONS.yaml`
3. aktueller fachlicher Zielstand: `docs/method/METHOD_CORE_V0_4_DE.md` plus `docs/method/GLOSSARY_DE.md`
4. `project/PROJECT_STATE.yaml` und `project/HANDOFF.md` für den aktuellen Projekt- und Migrationsstand
5. maschinenlesbare Methodik unter `data/method/` und `config/` für die **aktuell implementierte Runtime-Semantik**
6. weitere Methodendokumentation
7. Agenten-Session-Logs und History-Dokumente

Wichtig:

- Ein neuerer akzeptierter Methodenentscheid kann älteren maschinenlesbaren Runtime-Regeln fachlich voraus sein. Das ist ein **Implementation Gap**, kein Anlass, die Abweichung still aufzulösen.
- Umgekehrt darf ein Zieldokument nicht als bereits implementierte Runtime-Funktion beschrieben werden, solange Schema/Code/UI noch nicht migriert sind.
- `docs/history/` und ältere Agenten-Logs sind historische Evidenz des Projektverlaufs, keine aktuelle Methodenquelle.
- Widersprüche nicht still auflösen: Konflikt dokumentieren und Review auslösen.

## 3. Aktueller Methoden- und Entwicklungsstand

Der aktuelle fachliche Zielstand ist der **Decision-Support-Methodenkern v0.4**. Er versteht den Radar primär als vergleichende Entscheidungshilfe für Betriebs-/Architekturvarianten eines Workloads; nicht als universelles BSI-/NIS2-/DORA-Audit und nicht als Provider-Länderranking.

Die vorhandene Webanwendung implementiert noch wesentliche Teile des früheren Einzel-Assessment-/Guided-Questions-Workflows. Diese Runtime bleibt bis zur validierten Migration funktionsfähig und nachvollziehbar, ist aber nicht automatisch identisch mit dem fachlichen Zielbild v0.4.

### C3A-Review abgeschlossen

**NEXT-120 / Issue #68** ist fachlich abgeschlossen. C3A v1.0 wurde vollständig gegen Methodenkern v0.4, Provider Intelligence, Hard Gates, Risikotaxonomie und Question Library geprüft.

Kanonische C3A-Referenzen im Repository:

- `docs/method/C3A_V1_0_REVIEW.md`
- `data/method/c3a_v1_0_crosswalk.csv`
- `SRC-04`

Leitplanken daraus:

- C3A Criterion / Additional Criterion sind keine Reifegradstufen.
- formale C3A-Erfüllung nicht ohne C5-Scope-Evidence behaupten.
- C3A SOV-6 ist primär providerseitige Fortführungs-/Entwicklungsautonomie, nicht Kundenausstieg.
- C3A-Anforderungen werden über ein kundenspezifisches Requirement Profile aktiviert, nicht pauschal als globale Gates.

### Aktuelles Validierungs-Gate

Vor **größerer v0.4-Schema-/DB-/API-/UI-Migration** muss NEXT-119 die Methode an Referenzvarianten validieren und insbesondere Screeningkern, Requirement Profiles, Decision Dimensions und Recommendation-Logik kalibrieren. NEXT-118 kann die bestehende Runtime bereits operativ aus Consultant-Sicht evaluieren.

Erlaubt sind außerdem Repository-Hygiene, Bugfixes, Security-Hardening und quellengetreue Methoden-/Provider-Recherche.

## 4. Projektarchitektur – nicht verhandelbare Grundsätze

- **cloud-agnostischer Methodenkern**: keine AWS-/Azure-/GCP-spezifische Regel darf den Kern dominieren.
- **Decision Support statt Provider-Ranking**: Varianten werden anhand konkreter Anforderungen, Szenarien, Capabilities, Risiken, Nutzen und Evidence verglichen.
- **kein Credential-/Root-Zugang als Voraussetzung**: Standard ist Customer-mediated Evidence.
- **Provider Adapter sind Übersetzer**, nicht Risk Engines.
- **Security und Souveränität getrennt** bewerten.
- **Provider Capability ≠ Applied Capability**.
- **Evidence Confidence ≠ Risikohöhe**.
- **Gate first, score second**.
- fehlende Information = `UNVERIFIED`, nicht automatisch `FAIL`.
- Risikoakzeptanz, rechtliche Würdigung und finale Entscheidung bleiben menschliche Entscheidungen des Kunden.
- Providerherkunft/Jurisdiktion ist ein Fakt und kein pauschaler Souveränitätsscore.
- die Question Bank ist Wissens-/Deep-Dive-Bibliothek, kein verpflichtender 128-Fragen-Standardablauf.

## 5. Agentenrollen

Ein Agent nennt pro Task mindestens eine Rolle:

- `researcher` – Quellen, Fundstellen, Versionen
- `methodologist` – Risiko-/Souveränitätsmethodik
- `architect` – Domain-, Evidence-, Tool-/Integrationsarchitektur
- `developer` – Code, Schema, Tests
- `reviewer` – unabhängige Prüfung
- `evidence-analyst` – Evidence Intake, Claims, Scope/Trust
- `project-coordinator` – Issues, Handoffs, State/Roadmap

Implementierer und Reviewer desselben substantiellen Changes sollen nach Möglichkeit getrennt sein. Self-Review muss als solcher markiert werden.

## 6. Planungsprotokoll

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

## 7. Provenienzpflicht

Jede neue fachliche Regel, Frage, Risikokategorie, Formel oder Schwelle erhält eine Provenienzklasse:

- `external-direct`
- `external-derived`
- `internal-method`
- `project-assumption`
- `evidence-observation`

Source-ID/Fundstelle referenzieren. Interne Regeln und Schwellen referenzieren die passende `INT-*`-/`DEC-*`-Quelle. Eigene Regeln niemals als Normtext ausgeben.

## 8. Evidence-Regeln

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
- Kontextquellen wie Interview, CMDB, ArchiMate oder Diagramme dürfen Fragen vorbefüllen, werden aber nicht automatisch zu ausreichender Gate-/Risiko-Evidence.

## 9. Provider-Agnostik

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
- aus Herkunft/Nationalität einen pauschalen Score erzeugen

## 10. Softwareentwicklung

- deterministische Regeln in Code/Config, nicht nur Prompts
- neue Regeln mit Unit-/Boundary-Tests
- Schemas rückwärtskompatibel oder mit Migration
- keine Secrets/Kundendaten
- Evidence-Pack-Parser arbeitet lokal und dateibasiert
- Parser dürfen keine externen Systeme kontaktieren, außer ausdrücklich als separater Research-/Adapter-Task
- Zielmethodik und Runtime-Implementierung in PRs explizit unterscheiden
- vor größerer v0.4-Runtime-Migration NEXT-119 und den aktuellen Projektstand in `PROJECT_STATE.yaml` beachten
- C3A-Mappings immer gegen `C3A_V1_0_REVIEW.md`/Crosswalk prüfen und nicht aus Erinnerung ableiten

## 11. Git- und Review-Workflow

- `main` stabil und handoff-fähig halten
- Branches: `feature/`, `fix/`, `research/`, `method/`, `docs/`, `chore/`
- substantielle Änderungen per PR
- PR enthält: Ziel, Änderungen, Quellen/Provenienz, Tests, Risiken, Handoff-Auswirkung
- kein Merge mit `BLOCKER`

Reviewklassen stehen in `docs/project/REVIEW_PROCESS.md`.

## 12. Multi-Agent-Koordination

- ein Issue = eine primäre Outcome-Verantwortung
- Agent schreibt vor Start kurz in Issue/Branch, welchen Scope er übernimmt
- parallele Agenten vermeiden dieselben State-/Methoden-Dateien
- `PROJECT_STATE.yaml` ist kein Chatlog; nur Gesamtzustand
- Details in `project/agent-log/`
- Handoff muss explizit sagen: erledigt, offen, Entscheidungen, nächste Dateien/Tests

## 13. Abschluss eines Tasks

Vor Ende:

1. Tests/Validator ausführen.
2. Provenienz prüfen.
3. offene Punkte benennen.
4. Session-Log schreiben/aktualisieren.
5. Handoff/State/NEXT_ACTIONS nur bei echter Zustandsänderung aktualisieren.
6. PR-Review-ready machen.

## 14. Sicherheits-Stopps

Sofort stoppen/eskalieren bei:

- Secret-/Credential-Fund
- Anforderung nach Kunden-Root-/Owner-Zugang als Standardlösung
- unklarer Lizenzlage bei Volltextübernahme
- regulatorischer Behauptung ohne belastbare Quelle
- automatischer Risikoakzeptanz
- Kundendaten in GitHub/Issues/PRs

## 15. Kommunikationsstandard

Kennzeichne Aussagen als:

- **Fact** – belegt
- **Observation** – aus Evidence beobachtet
- **Assumption** – Annahme
- **Inference** – methodische Ableitung
- **Decision** – akzeptierte Projektentscheidung
- **Open** – offen

Der nächste Agent muss ohne Chatkontext verstehen können, warum der Stand so ist.
