# NEXT-114 – Synthetischer Consultant-Durchlauf

## Zweck

Dieser Lauf validiert den Souveränitäts-Radar als **Beratungsworkflow** und nicht nur als Sammlung einzelner Unit Tests. Er beantwortet die Frage, ob ein Consultant aus einem sauberen Checkout eine Installation starten und ein Assessment von Scope/Relevanzprofil über Fragen und Evidence bis zu Human-reviewed Claims und Hard-Gate-Ergebnissen durchführen kann.

Der Testfall ist vollständig synthetisch. **Keine Aussage in diesem Szenario beschreibt einen realen Provider, ein reales Cloud-Angebot oder eine reale Kundenarchitektur.** Alle technischen, vertraglichen und organisatorischen Merkmale sind Testannahmen (`PRJ-01` / Validation Fixture).

## Szenario

Ein agentisches KI-System verarbeitet sensible Fachdaten in einem Managed-Service-/Cloud-Kontext. Der Fall ist absichtlich breit genug, um Datenverarbeitung, Schlüsselkontrolle, Exit, IAM/Trust Anchors, Supply Chain, C5/C3A-Relevanz und die Trennung von Evidence Confidence und technischer Capability sichtbar zu machen.

Das Assessment erhält `high` als Kritikalität. Für den deterministischen Validierungskern werden die Gate Requirements anschließend explizit als **Consultant Override** gesetzt, damit PASS/FAIL/UNVERIFIED reproduzierbar erzeugt werden. Diese Werte sind Testkonfiguration und keine regulatorischen Mindestwerte.

## Erwartete Gate-Zustände

| Gate | Requirement | Synthetische Capability / Evidence | Erwartung |
|---|---:|---|---|
| HG-01 Jurisdiktion & Effective Control | 2 | reviewed Claim Level 3 + reviewed Evidence Trust 4 | PASS |
| HG-02 Datenresidenz & Verarbeitung | 0 | nicht Teil dieses isolierten Gate-Tests | N/A |
| HG-03 Schlüsselhoheit | 3 | reviewed Claim Level 1 + reviewed Evidence Trust 4 | FAIL |
| HG-04 Exit & Portabilität | 3 | reviewed Claim Level 3, aber **ohne reviewed Evidence** | UNVERIFIED |
| HG-05 Operational Autonomy | 0 | nicht Teil dieses isolierten Gate-Tests | N/A |
| HG-06 Identity & Trust Anchors | 0 | nicht Teil dieses isolierten Gate-Tests | N/A |
| HG-07 Supply Chain Critical Dependencies | 0 | nicht Teil dieses isolierten Gate-Tests | N/A |
| HG-08 Security Minimum | 0 | nicht Teil dieses isolierten Gate-Tests | N/A |

Zusätzlich wird für HG-03 ein **draft Claim mit Capability 4** angelegt. Dieser darf den reviewed Claim Level 1 nicht überstimmen. Damit wird die Human-Review-Grenze im laufenden System geprüft.

## LLM-Bridge-Negativtest

Der Lauf erzeugt das LLM Prompt Package, importiert anschließend ein synthetisches Proposal-JSON und prüft danach zwei Bedingungen:

1. Die Anzahl der Claims ist unverändert.
2. Die Hard-Gate-Ergebnisse sind unverändert.

Damit wird im End-to-End-Pfad abgesichert, dass die Copy/Paste LLM Bridge Vorschläge liefern kann, aber ohne Human Review keine Gate-Entscheidung verändert.

## Automatisierter Ablauf

`tools/validation/synthetic_consultant_walkthrough.py` arbeitet ausschließlich gegen die HTTP-API einer laufenden lokalen Installation und verwendet nur Python-Standardbibliothek. Der Runner:

1. prüft `/api/health`,
2. legt das synthetische Assessment an,
3. setzt das Relevanzprofil,
4. liest den Guided Question Path und `Alle Fragen`,
5. speichert eine reviewed Beispielantwort,
6. erfasst zwei synthetische Evidence-Objekte,
7. reviewt Evidence mit Applied State und Trust,
8. setzt die Gate Requirements als Consultant Overrides,
9. erzeugt reviewed/draft Claims,
10. prüft PASS/FAIL/UNVERIFIED/N/A,
11. testet die LLM Bridge ohne automatische Claim-/Gate-Wirkung,
12. schreibt einen JSON-Validierungsbericht.

Lokaler Aufruf bei bereits laufender Installation:

```bash
python3 tools/validation/synthetic_consultant_walkthrough.py \
  --base-url http://127.0.0.1:8080 \
  --output .runtime/exports/synthetic-consultant-walkthrough.json
```

## CI-Lifecycle

Der Job `consultant-walkthrough` in `.github/workflows/validate.yml` geht weiter als der normale Compose-Smoke-Test:

```text
Clean Checkout
  -> ./install.sh (Default: localhost:8080)
  -> synthetischer Consultant-Durchlauf
  -> Report nach /tmp sichern
  -> ./stop.sh
  -> ./start.sh
  -> ./test.sh
  -> ./uninstall.sh mit explizitem DELETE
  -> .runtime/.env und Container-Reste prüfen
  -> JSON-Bericht als GitHub-Actions-Artifact hochladen
```

Damit validiert CI sowohl den Assessment-Pfad als auch den Produkt-Lifecycle.

## Was dieser Test nicht beweist

Der Lauf ist kein produktiver Kundenpilot und keine Providerbewertung. Er beweist insbesondere **nicht**:

- dass die internen Requirement-Templates bereits optimal kalibriert sind,
- dass Capability Level 0–4 inter-rater-stabil vergeben werden,
- dass alle 128 Fragen bereits perfekt operationalisierte Applicability-Regeln besitzen,
- dass reale Vertrags-/Assurance-Dokumente ausreichend automatisch verarbeitet werden,
- dass ein bestimmter Cloud-/KI-Provider die hier verwendeten synthetischen Eigenschaften besitzt.

Diese Punkte bleiben Gegenstand späterer Kalibrierungs- und Evidence-Piloten.

## Umgang mit Findings

Fehlschläge werden nicht durch Anpassung der erwarteten Gate-Zustände „grün gerechnet“. Bei einem echten UX-, Lifecycle- oder Methodikproblem wird ein separates GitHub Issue angelegt. Nur klar erkennbare Test-/Implementierungsfehler des Walkthrough-Runners werden direkt im NEXT-114-Branch behoben.
