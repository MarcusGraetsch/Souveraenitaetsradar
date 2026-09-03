# Agent Session – NEXT-112 Evidence → Claim → Hard Gate

Datum: 2026-09-03
Rollen: developer, methodologist, reviewer (Self-Review)
Issues: #3, #4, #15
Branch: `feature/evidence-gate-foundation`

## Ziel

Die vorhandene providerneutrale Evidence-Foundation mit dem R4-Hard-Gate-Modell verbinden. Ein Gate darf nur aus human-bestätigten Claims und überprüfter Evidence deterministisch bewertet werden. LLM-Vorschläge dürfen niemals direkt ein Gate verändern.

## Vorhandene Basis bestätigt

NEXT-102 ist im Repository bereits materiell erfüllt:

- `src/sovradar/models.py` enthält typisierte Evidence Records.
- `schemas/evidence-pack.schema.json` und `schemas/evidence-record.schema.json` validieren Customer Evidence Packs.
- `src/sovradar/intake.py` lädt Packs lokal, ohne Netz-/Cloudzugriff.
- Path-Traversal wird abgewehrt.
- `tests/test_intake.py` deckt gültiges Pack, Gate-Filter und invaliden Pfad ab.

Deshalb wird NEXT-102 als abgeschlossen behandelt und nicht neu implementiert.

## Neue Kernentscheidungen für NEXT-112

1. `Claim` ist die verbindende Schicht zwischen Roh-/Reviewed Evidence und Gate-Bewertung.
2. Nur `reviewed`/`approved` Claims beeinflussen Gates.
3. Claims ohne Capability-Level dürfen Fakten dokumentieren, aber keinen technischen PASS/FAIL erzeugen.
4. Pro Gate gilt konservativ die schwächste human-bestätigte Capability-Aussage.
5. Ein Capability-Claim benötigt reviewed/approved Evidence, damit Evidence Trust ableitbar ist.
6. Pro Claim darf der stärkste passende Nachweis tragen; Gate-Trust wird durch den schwächsten belegten Capability-Claim begrenzt.
7. Fehlende Claims oder Evidence bleiben `UNVERIFIED`.
8. Requirement 0 ergibt `N/A`.
9. Diese Aggregationslogik ist interne Operationalisierung (`INT-03`), keine externe Normformel.

## Bereits umgesetzt auf diesem Branch

- `Claim`, `GateDefinition`, `EvidenceRequest`, `GateEvaluation` im Core-Datenmodell.
- typisierter Loader für `r4_hard_gates.csv` und `evidence_request_catalog.csv`.
- deterministische Validierung, dass alle acht Hard Gates Evidence Requests besitzen.
- `evaluate_gate()` mit PASS / FAIL / UNVERIFIED / N/A.
- Unit Tests für Gate-Katalog und Gate-Auswertung.

## Nächste Umsetzung

- Persistenz für Claims, Evidence-Review-Metadaten und Gate Requirements in FastAPI/PostgreSQL.
- API-Endpunkte für Claim Review und Gate-Auswertung.
- acht Gate-Karten im Consultant-UI mit Drill-down auf Claims/Evidence/Reasoning.
- API-/Frontend-/Compose-Tests.

## Leitplanken für andere Agenten

- Keine Provider-Sonderlogik in `gate_evaluation.py` oder Gate-Katalog.
- Keine automatische Übernahme von LLM-Proposals in Claims.
- Keine Ableitung `fehlende Evidence = FAIL`.
- Keine Risikoakzeptanz automatisieren.
- Bei neuen Schwellen/Heuristiken immer Provenienz als interne Regel kenntlich machen.
- Raw Kundenevidence nicht committen.
