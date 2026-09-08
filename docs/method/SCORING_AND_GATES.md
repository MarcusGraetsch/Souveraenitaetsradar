# Scoring and Gates

Status: **aktuell implementierte interne Operationalisierung / fachliches Zielbild nach C3A-Review dokumentiert**

## Kein einzelner „Wahrheitsscore“

Der Radar soll mehrere Dimensionen zeigen. Ein Score darf Hard-Gate-Fails nicht kompensieren.

Im Methodenkern v0.4 sind Scores nur optionale Managementhilfen. Die Empfehlung muss auch ohne einen einzigen Gesamtscore über Anforderungen, Risiken, Nutzen, Maßnahmen, Trade-offs und Evidence nachvollziehbar sein.

## Hard Gates

Hard Gates sind **interne Operationalisierung nicht kompensierbarer Mindestanforderungen**. Sie sind keine unverändert aus BSI, EU-CSF oder C3A übernommene Normstruktur.

Die aktuelle Runtime verwendet acht Gates. Der C3A-Volltextreview bestätigt deren Nutzen als **Gruppierung**, zeigt aber, dass konkrete nicht kompensierbare Anforderungen künftig stärker aus expliziten Kundenanforderungen bzw. Framework-Profilen instanziiert werden sollten.

Beispiel:

- Kunde fordert C3A `SOV-1-01-C1` → EU-Jurisdiktion wird konkretes Requirement.
- Kunde fordert C3A `SOV-1-01-C2` → deutsche Jurisdiktion wird konkretes Requirement.
- Diese beiden Kriterien sind **alternative Profile**, keine Level 3 und 4 derselben Skala.

## Capability / Requirement 0–4

Die aktuelle Skala ist **interne Operationalisierung**, kein offizieller EU-SEAL und keine C3A-Skala.

C3A `Criterion`, `Additional Criterion` und EU-/Deutschlandvarianten dürfen niemals automatisch in die 0–4-Skala als externe Reifegradstufen übersetzt werden.

## Zielbild: Requirement Profile

Nach NEXT-119 soll die Runtime perspektivisch explizite Requirement-Profile unterstützen:

```text
RequirementProfile
  -> requirement source / criterion ID
  -> scope
  -> mandatory / non-compensable
  -> required evidence
  -> ArchitectureOption applicability
  -> PASS / FAIL / UNVERIFIED / N/A
```

Die acht heutigen Gate-Domänen können dabei als verständliche Management-/UI-Gruppierung erhalten bleiben.

## C3A-spezifische Gate-Regeln

- C3A Kriterien werden use-case-abhängig ausgewählt.
- `Additional Criterion` ist nur aktiv, wenn der Kunde es fordert.
- Deutschlandvarianten sind nicht automatisch „höher“ als EU-Varianten.
- Für eine formale C3A-Erfüllungsbehauptung muss die von C3A vorausgesetzte C5-Erfüllung im passenden Scope belastbar vorliegen.
- Ein einzelnes erfülltes C3A-Kriterium darf nicht als C3A-Gesamtkonformität ausgegeben werden.
- C3A SOV-6 darf nicht pauschal als Kundenausstiegs-/Portabilitäts-Level verwendet werden.

## Evidence Gate

Die aktuelle Runtime trennt technisches Erfüllen und Evidenz:

- Technical Gate: Capability >= Requirement
- Evidence Gate: Effective Trust >= Required Trust
- Final: `FAIL`, `UNVERIFIED`, `PASS`

Diese Formel beschreibt die **implementierte INT-03-Runtime-Semantik**. Sie darf nicht als externe Normformel ausgegeben werden.

Für C3A muss Evidence zusätzlich kriterienspezifisch auf Service Set, Offering, Region/Legal Entity, Audit Scope und Framework-Version passen.

## Interne Default-Schwellen

Siehe `config/rules/r4-defaults.yaml` und `data/method/r4_factor_rules.csv`.

Alle numerischen Schwellen sind konfigurierbare interne Defaults, sofern nicht ausdrücklich anders nachgewiesen. Sie müssen durch Referenzfälle und Inter-Rater-Kalibrierung überprüft werden.

## Exit

Aktuell getrennt:

- Exit Transition Ratio
- Cutover Downtime Ratio
- Exit Test Maturity

Diese Trennung bleibt methodisch sinnvoll. Data Act, DORA und Bitkom sind hierfür die wichtigeren Quellen. C3A SOV-6 adressiert primär Provider-Fortführungs-/Entwicklungsfähigkeit und ist nicht mit kundenseitigem Switching gleichzusetzen.

## Konzentration

Portfolio-/Common-Cause-Ebene. Ein Einzelworkload kann einen Flag erzeugen, aber keine vollständige Portfoliokonzentration berechnen.

## KI Portability

Aktuell drei Teillevel plus Floor:

- Data Control
- Model Portability
- Agent/Tool/Policy Portability

Der Floor `MIN(...)` hat Vorrang vor Durchschnittswerten.

Auch diese Logik ist interne Methodik und muss bei späterer Weiterentwicklung weiterhin mit Provenienz, Boundary-Tests und klarer Trennung von externen Frameworks geführt werden.
