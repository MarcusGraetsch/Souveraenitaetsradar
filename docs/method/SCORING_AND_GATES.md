# Scoring and Gates

## Kein einzelner „Wahrheitsscore“

Der Radar soll mehrere Dimensionen zeigen. Ein Score darf Hard-Gate-Fails nicht kompensieren.

## Capability / Requirement 0–4

Die Skala ist **interne Operationalisierung**, nicht offizieller EU-SEAL.

## Evidence Gate

Technisches Erfüllen und Evidenz werden getrennt geprüft:

- Technical Gate: Capability >= Requirement
- Evidence Gate: Effective Trust >= Required Trust
- Final: `FAIL`, `UNVERIFIED`, `PASS`

## Interne Default-Schwellen

Siehe `config/rules/r4-defaults.yaml` und `data/method/r4_factor_rules.csv`.

Alle numerischen Schwellen sind konfigurierbare interne Defaults, sofern nicht ausdrücklich anders nachgewiesen.

## Exit

Getrennt:

- Exit Transition Ratio
- Cutover Downtime Ratio
- Exit Test Maturity

## Konzentration

Portfolio-/Common-Cause-Ebene. Ein Einzelworkload kann einen Flag erzeugen, aber keine vollständige Portfoliokonzentration berechnen.

## KI Portability

Drei Teillevel plus Floor:

- Data Control
- Model Portability
- Agent/Tool/Policy Portability

Der Floor `MIN(...)` hat Vorrang vor Durchschnittswerten.
