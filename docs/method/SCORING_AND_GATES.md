# Scoring and Gates

Status: **aktuell implementierte interne Operationalisierung / unter v0.4-Review**

## Kein einzelner „Wahrheitsscore“

Der Radar soll mehrere Dimensionen zeigen. Ein Score darf Hard-Gate-Fails nicht kompensieren.

Im Methodenkern v0.4 sind Scores nur optionale Managementhilfen. Die Empfehlung muss auch ohne einen einzigen Gesamtscore über Anforderungen, Risiken, Nutzen, Maßnahmen, Trade-offs und Evidence nachvollziehbar sein.

## Hard Gates

Hard Gates sind **interne Operationalisierung nicht kompensierbarer Mindestanforderungen**. Sie sind keine unverändert aus BSI, EU-CSF oder C3A übernommene Normstruktur.

Die aktuelle Runtime verwendet acht Gates. Ob diese Struktur fachlich angepasst oder ergänzt werden sollte, wird im C3A-Volltextreview **NEXT-120 / Issue #68** ausdrücklich geprüft.

## Capability / Requirement 0–4

Die Skala ist **interne Operationalisierung**, kein offizieller EU-SEAL und keine C3A-Skala.

## Evidence Gate

Die aktuelle Runtime trennt technisches Erfüllen und Evidenz:

- Technical Gate: Capability >= Requirement
- Evidence Gate: Effective Trust >= Required Trust
- Final: `FAIL`, `UNVERIFIED`, `PASS`

Diese Formel beschreibt die **implementierte INT-03-Runtime-Semantik**. Sie darf nicht als externe Normformel ausgegeben werden.

## Interne Default-Schwellen

Siehe `config/rules/r4-defaults.yaml` und `data/method/r4_factor_rules.csv`.

Alle numerischen Schwellen sind konfigurierbare interne Defaults, sofern nicht ausdrücklich anders nachgewiesen. Sie müssen später durch Referenzfälle und Inter-Rater-Kalibrierung überprüft werden.

## Exit

Aktuell getrennt:

- Exit Transition Ratio
- Cutover Downtime Ratio
- Exit Test Maturity

Diese Trennung bleibt methodisch sinnvoll; Data Act, DORA und nach NEXT-120 ggf. C3A liefern zusätzliche fachliche Quellen, ohne dass deren Begriffe automatisch identisch mit den internen Faktoren sind.

## Konzentration

Portfolio-/Common-Cause-Ebene. Ein Einzelworkload kann einen Flag erzeugen, aber keine vollständige Portfoliokonzentration berechnen.

## KI Portability

Aktuell drei Teillevel plus Floor:

- Data Control
- Model Portability
- Agent/Tool/Policy Portability

Der Floor `MIN(...)` hat Vorrang vor Durchschnittswerten.

Auch diese Logik ist interne Methodik und muss bei späterer Weiterentwicklung weiterhin mit Provenienz, Boundary-Tests und klarer Trennung von externen Frameworks geführt werden.
