# Agent Session – NEXT-112 Evidence → Claim → Hard Gate

Datum: 2026-09-03
Rollen: developer, methodologist, reviewer (Self-Review)
Issues: #3, #4, #15
Branches: `feature/evidence-gate-foundation`, `feature/next-112-gate-api-ui`

## Ziel

Die providerneutrale Evidence-Foundation mit dem R4-Hard-Gate-Modell und der Consultant-Webanwendung verbinden. Ein Gate darf nur aus human-bestätigten Claims und überprüfter Evidence deterministisch bewertet werden. LLM-Vorschläge dürfen niemals direkt ein Gate verändern.

## Vorhandene Basis / NEXT-102

NEXT-102 wurde verifiziert und abgeschlossen:

- typisierte `EvidenceRecord`s
- Evidence-Pack-/Record-Schemas
- lokaler, cloud-unabhängiger Pack Loader
- deterministische Schemafehler
- Path-Traversal-Schutz
- Unit Tests

Issue #3 ist geschlossen.

## Kernentscheidungen

1. `Claim` ist die verbindende Schicht zwischen Evidence und Gate-Bewertung.
2. Nur `reviewed`/`approved` Claims beeinflussen Gates.
3. Claims ohne Capability-Level dokumentieren Fakten, erzeugen aber keinen technischen PASS/FAIL.
4. Pro Gate gilt konservativ die schwächste human-bestätigte Capability-Aussage.
5. Ein Capability-Claim benötigt reviewed/approved Evidence, damit Evidence Trust ableitbar ist.
6. Pro Claim darf der stärkste passende Nachweis tragen; Gate-Trust wird durch den schwächsten belegten Capability-Claim begrenzt.
7. Fehlende Claims oder Evidence bleiben `UNVERIFIED`.
8. Requirement 0 ergibt `N/A`.
9. Gate-Requirement-Templates werden nach Kritikalität vorbelegt (`low→Basis`, `medium→Standard`, `high→Elevated`, `critical→Critical`) und sind ausdrücklich als Consultant-Override editierbar.
10. Diese Aggregations- und Defaultlogik ist interne Operationalisierung (`INT-03`), keine externe Normformel.

## Foundation – auf main

PR #16 wurde nach grüner CI squash-gemerged.

Enthalten:

- `Claim`, `GateDefinition`, `EvidenceRequest`, `GateEvaluation`
- typisierter Loader für `r4_hard_gates.csv` und `evidence_request_catalog.csv`
- Vollständigkeitsprüfung HG-01…HG-08
- `evaluate_gate()` mit PASS / FAIL / UNVERIFIED / N/A
- Unit Tests für Gate-Katalog und Gate-Auswertung
- DEC-022/DEC-023

## API/UI – aktueller Branch

Auf `feature/next-112-gate-api-ui` umgesetzt:

### Persistenz

Neue Tabellen statt Spaltenänderungen an bestehenden MVP-Tabellen, damit vorhandene Installationen mit `Base.metadata.create_all()` weiterlaufen können:

- `evidence_reviews`
- `assessment_claims`
- `gate_requirements`

### Evidence Review

Berater bewertet je Evidence:

- Applied State (`asserted` bis `attested`)
- Base Trust 0–5
- Scope Fit 0–5
- Freshness Fit 0–5
- Review Status
- Effective Trust = Minimum der drei Trust-Dimensionen

Evidence ohne Review bleibt `raw` / Trust 0 und kann kein Gate verifizieren.

### Claims

Claim CRUD mit:

- Gate-ID
- Aussage
- Capability Level 0–4 oder reiner Fakt
- Evidence-Links
- optionale Question-Links
- Review State
- Notiz

Evidence-/Question-IDs werden serverseitig validiert.

### Gate Requirements

Default wird aus Kritikalität + `r4_hard_gates.csv` gelesen. Jede manuelle Anpassung wird als `consultant-override` gespeichert. Die UI weist ausdrücklich darauf hin, dass dies keine Normvorgabe ist.

### Hard-Gate API

- Methodenkatalog inkl. Evidence Requests
- Requirements lesen/überschreiben
- Evidence Review lesen/speichern
- Claim CRUD
- alle acht Gates auswerten

Gate-Response enthält Requirement, Applied Capability, Evidence Trust, Technical/Evidence/Final State, Claim-/Evidence-IDs, deterministische Reasons und Evidence Requests.

### Consultant UI

- Evidence-Review-Felder direkt an Evidence-Karten
- neuer Tab `Hard Gates`
- acht Gate-Karten mit PASS/FAIL/UNVERIFIED/N/A
- Requirement-Override 0–4
- Drill-down auf Begründungen und benötigte Evidence
- Claim-Erfassung und Human Review
- Ergebnisübersicht mit Gate-Zählung und Arbeitsstatus

LLM Bridge bleibt separat; kein Button erzeugt automatisch einen reviewed Claim aus einem LLM-Proposal.

## Tests auf dem aktuellen Branch

API-Tests wurden erweitert für:

- acht Gates vorhanden
- Kritikalitäts-Default
- Evidence Review + Trust
- reviewed Claim + ausreichende Evidence → PASS
- Consultant-Override über Capability → FAIL
- draft Claim / raw Evidence → UNVERIFIED
- unbekannte Evidence-/Question-Links → 422

Noch auszuführen/zu prüfen: vollständige CI (Core/API, Frontend Build, Compose Smoke). Erst bei Grün wird gemerged.

## Leitplanken für andere Agenten

- Keine Provider-Sonderlogik in Gate-/Rule-Core.
- Keine automatische Übernahme von LLM-Proposals in Claims.
- Keine Ableitung `fehlende Evidence = FAIL`.
- Keine Risikoakzeptanz automatisieren.
- Requirement-Defaults nicht als regulatorische Pflicht darstellen.
- Bei neuen Schwellen/Heuristiken Provenienz als interne Regel kenntlich machen.
- Raw Kundenevidence nicht committen.
