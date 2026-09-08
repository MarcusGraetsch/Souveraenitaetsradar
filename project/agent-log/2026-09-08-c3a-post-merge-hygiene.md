# Agent Log – C3A Post-Merge Hygiene / NEXT-121

Datum: 08.09.2026  
Issue: #69  
Rollen: project-coordinator, methodologist, developer, reviewer (Self-Review)  
Branch: `chore/post-merge-c3a-hygiene-ci`

## Ziel

Nach dem Merge von PR #66 die verbliebenen Repository-Hygiene- und CI-Probleme beseitigen, ohne die fachliche v0.4-/C3A-Methodik erneut umzubauen.

## Ausgangsbefunde

1. Merge-Commit `a0b26d66c3c62da6ea6304a1f84c39ecb01656e1` hatte einen roten `validate`-Workflow.
2. Python-Job scheiterte in `tools/validate_repo.py`.
3. Consultant-Walkthrough scheiterte in `progressive_workflow_validation.py`.
4. `data/method/source_register_addendum_v1.csv` enthielt im INT-05-Hinweis ein unquotiertes Semikolon und damit eine zusätzliche CSV-Spalte; zugleich war die Aussage „C3A-Volltextabgleich steht ... noch aus“ veraltet.
5. Der progressive Workflow-Test enthielt starre Frage-/Applicability-Zählwerte aus NEXT-114/115. Diese Werte sind als Regressionstest ungeeignet, sobald die Question Library fachlich erweitert oder präzisiert wird.
6. Issue #31 verwendete ebenfalls `NEXT-120`, obwohl diese Kennung kanonisch dem C3A-Volltextreview gehört.
7. Issue #68 war nach abgeschlossenem Volltextreview noch offen.

## Änderungen

- INT-05 im internen Quellenregister fachlich aktualisiert und CSV-Spaltenbreite repariert.
- Progressive-Workflow-Validierung auf robuste Invarianten umgestellt:
  - Total = All-View,
  - Applicability partitioniert den Bestand vollständig,
  - Relevant = Applicable + Needs Review,
  - Needs Review bleibt vollständig in Clarification sichtbar,
  - Work-/Relevant-/Stage-Sichten bleiben intern konsistent,
  - komplexer Workload behält Screening und Deep Dive,
  - unmittelbare Work Queue ist kleiner als der relevante Pfad,
  - beantwortete Screening-Frage wandert reproduzierbar nach Completed,
  - einfacher öffentlicher Workload bleibt kürzer als komplexer KI-Workload.
- Keine feste 128/124/83/41/4-Zählwertannahme mehr. Die vollständige Question Library bleibt weiterhin auditierbar; `compose-smoke` schützt zusätzlich gegen einen katastrophalen Bankverlust mit `method_questions >= 100`.
- Issue #68 als abgeschlossen dokumentiert und geschlossen.
- Issue #31 von der kollidierenden `NEXT-120`-Kennung bereinigt.
- Historischen PR #66 in Titel/Beschreibung auf den tatsächlich gemergten Scope (Decision Support v0.4 + Provider Intelligence + C3A) aktualisiert.

## Nicht geändert

- keine neue Scoring-/Gate-Formel,
- keine Requirement-Profile-Runtime,
- keine DB-/API-/UI-Migration,
- keine Providerbewertung,
- keine neue regulatorische Aussage.

## Provenienz

Die C3A-Fachgrundlage bleibt `SRC-04`, `docs/method/C3A_V1_0_REVIEW.md` und `data/method/c3a_v1_0_crosswalk.csv`. Die in diesem Task geänderte Test-/Repositorylogik ist interne Engineering-/Hygiene-Operationalisierung (`INT-03`/`INT-05`).

## Review

Self-Review. Vor Merge erforderlich:

- `validate` vollständig grün,
- insbesondere `python` und `consultant-walkthrough`,
- kein neuer fachlicher Scope,
- PR #69/Follow-up-PR referenziert diesen Log.
