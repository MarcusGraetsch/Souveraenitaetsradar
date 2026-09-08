# Question Library

Der Fragenbestand ist zur besseren agentischen Verarbeitung nach Domänen aufgeteilt. Die CSV-Spalten stammen historisch aus dem Methodenmodell v0.9; fachlich ist die Bank seit Methodenkern v0.4 ausdrücklich eine **Question Library und kein Pflichtfragebogen**.

## Aktueller Status

- Alle 128 Fragen bleiben als Deep-Dive-/Audit-Wissensbestand erhalten.
- Der spätere sichtbare Screeningkern soll nur etwa 15–25 entscheidungsrelevante Kernfragen nutzen; Kalibrierung in NEXT-119.
- Applicability und Workflow-Priorisierung bleiben getrennt.
- Source IDs, Provenienztyp und Herleitung sind für jede Frage verpflichtend.

## C3A v1.0

Der vollständige C3A-Volltext wurde am 08.09.2026 geprüft. Maßgebliche Referenzen:

- `docs/method/C3A_V1_0_REVIEW.md`
- `data/method/c3a_v1_0_crosswalk.csv`
- `SRC-04`

Ein Teil der bestehenden Fragen enthält bereits C3A-Bezüge aus einem früheren Provenienzreview. Der Volltextreview hat mehrere Stellen als `partial`, `misaligned` oder `gap` identifiziert, insbesondere in SOV-3 bis SOV-6.

**Bis zur kriterienscharfen Question-Library-Migration in NEXT-119 gilt der neue C3A-Crosswalk als fachlich höherrangige Mappingreferenz.** Eine ältere pauschale C3A-Nennung in einer Frage darf nicht als Beleg für vollständige oder wortgetreue C3A-Abdeckung verwendet werden.

Insbesondere:

- C3A `Criterion` und `Additional Criterion` sind keine Radar-Level.
- EU-/Deutschlandvarianten sind alternative Kundenanforderungen, keine Reifegradleiter.
- C3A deckt SOV-1 bis SOV-6 ab und setzt C5-Erfüllung voraus.
- C3A SOV-6 ist primär Provider-Fortführungs-/Entwicklungsfähigkeit und nicht automatisch kundenseitige Exit-Portabilität.

Änderungen an Fragen müssen Source IDs, Provenienz, Fundstelle und die C3A-Crosswalk-Auswirkungen mitpflegen.
