# NEXT-118 – zweiter realer LLM-Bridge-Lauf

Datum: 2026-09-04
Provenienz: `evidence-observation` für beobachtetes Modell-/UI-Verhalten, `internal-method` für abgeleitete Produktanforderungen.

## Ergebnis

Nach Merge von PR #48 wurde derselbe synthetische Fall erneut mit dem lokal/intern betriebenen Gemma-4:26b-Modell getestet.

- Assessment-ID wurde zeichenidentisch zurückgegeben.
- Import wurde erfolgreich validiert und gespeichert.
- SC-01 und SC-02 referenzieren die vorhandene Evidence-ID.
- geplanter Zustand wurde als geplant formuliert; keine Hochstufung zu beobachtet/getestet.
- Warning erkennt korrekt, dass die Evidence eine Anforderung/Absicht und keinen technischen Implementierungsnachweis darstellt.

## Rest-Findings

- `confidence: 1.0` bleibt für semantisch interpretierte Vorschläge zu hoch.
- SC-01 enthält `Agent` aus dem Assessment-Kontext; die Evidence selbst beschreibt Chatbot/Audio-Interview.
- SC-02 enthält leichte Kontextanreicherung (`Fachabteilung`, `automatisierte Datenerfassung`).
- DK-13 wurde als `evidence_gap` ausgegeben, obwohl die Frage `needs_review` ist; methodisch ist zunächst die Anwendbarkeit zu klären.
- `LLM confidence` muss in der UI klar von Evidence Trust / Radar Trust unterschieden werden.

## Workflow-Finding

Die importierten Answer-Proposals werden aktuell nur in der LLM-Bridge-Auditansicht gespeichert/angezeigt. Die Fragen-Seite lädt `answers`, aber keine `llmImports`; es existiert kein Human-Review-Pfad `Proposal -> prüfen/editieren -> als Antwort übernehmen`.

Dies ist getrennt von #40 (Claim Proposals) zu behandeln. Für Answer-Proposals ist ein eigener Review-/Übernahmepfad nötig.
