# NEXT-118 – erster realer LLM-Bridge-Pilot

Datum: 2026-09-04
Rollen: evidence-analyst, methodologist, developer, reviewer (Self-Review)
Provenienz: `evidence-observation` für beobachtetes LLM-Verhalten; `internal-method` für daraus abgeleitete Schutzregeln.

## Setup

- synthetisches Assessment `Musterbehörde Berlin`
- lokal/intern betriebenes Gemma-Modell
- eine freigegebene `customer-statement` Evidence mit geplanter Audio-/Chatbot-Datenerhebung im Wohngeldkontext
- Copy/Paste LLM Bridge

Keine echten Kundendaten oder Secrets im Test.

## Beobachtung 1 – opaque Assessment-ID verändert

Prompt-ID:

`44a70bdf-7d68-40f6-8243-6b6abff2001a`

LLM-Antwort:

`44a_70bdf-7d68-40f6-8243-6b6abff2001a`

Der bestehende Server lehnte den Import korrekt mit `assessment_id mismatch` ab. Das ist eine gewünschte Sicherheitsbarriere; eine fuzzy/automatische ID-Korrektur bleibt verboten.

Folge: #46. Prompt und UI werden robuster, ohne Strict Equality aufzuweichen.

## Beobachtung 2 – Context als Evidence-Proposal verwendet

Das Modell erzeugte für `SC-05` und `SC-16` Vorschläge ohne Evidence-Referenz und begründete sie nur mit Assessment-Header-Werten. Das widerspricht dem aktuellen Bridge-Modus, der ausschließlich evidence-getragene Answer-Proposals erzeugen soll, und bestätigt die Bedeutung von DEC-034 `Context Fact != Evidence`.

Folge: #47. `LlmProposal.evidence_ids` ist für diesen Proposal-Typ nicht mehr leer zulässig. Spätere Context-Extraction-Proposals erhalten einen getrennten Typ/Workflow.

## Beobachtung 3 – Status-/Zeitachsenverschiebung

Die Evidence beschrieb einen geplanten Zustand (`soll ... Interview mit Audio geführt werden`). Das Modell formulierte daraus `Audiodaten aus den durchgeführten Interviews` und machte damit aus Planung faktisch Beobachtung/Realität.

Folge: Promptvertrag verlangt explizit, geplant/gewünscht/behauptet von implementiert/beobachtet/getestet zu unterscheiden.

## Beobachtung 4 – Proposal-Qualität

- `DK-01`: grundsätzlich von der Kundenaussage getragen, aber nur partiell; Bürgerdaten und geplante Audiodaten sind genannt, die Frage verlangt breitere Datenklassen.
- `SC-02`: grundsätzlich plausibel, aber die Formulierung sollte eher `Wohngeldprozess / Datenerhebung für Wohngeld` lauten und nicht suggerieren, die KI zahle selbst Wohngeld aus.
- `SC-05`, `SC-16`: im aktuellen Evidence-Proposal-Modus unzulässig, da keine Evidence-ID.
- `confidence=1.0` war für mehrere semantisch interpretierte Aussagen zu hoch.
- `evidence_gaps` und `warnings` waren als Mechanismus grundsätzlich brauchbar.

## Implementierter Sofortfix

Branch: `fix/next-118-llm-bridge-hardening`

- JSON-Beispiel im Prompt enthält die tatsächliche Assessment-ID statt `<must match>`.
- Assessment-/Question-/Evidence-IDs werden explizit als opaque/zeichenidentisch gekennzeichnet.
- Assessment/Relevanzprofil sind in diesem Bridge-Modus nur Kontext, kein alleiniger Proposal-Beleg.
- jedes Answer-Proposal benötigt mindestens eine Evidence-ID.
- Prompt bewahrt epistemischen/zeitlichen Status und fordert konservative Confidence.
- Webclient erkennt eine abweichende Assessment-ID vor dem POST und zeigt erwartet/erhalten; keine automatische Reparatur.
- Regressionstests für Promptvertrag und evidence-freie Proposals.

## Nicht gelöst / Follow-up

- separate Context-Extraction-Proposal-Schemas für #37/#41
- LLM Claim Proposal Review Queue aus #40
- prompt_version/schema_version/request nonce/checksum für spätere robuste Korrelation
- systematische Modellvergleichstests mit internen LLM-Endpunkten nach #43
