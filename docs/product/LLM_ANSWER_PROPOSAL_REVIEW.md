# LLM Answer Proposal Review

## Problem

Importierte LLM-Antwortvorschläge sind heute nur Auditobjekte in der LLM Bridge. Sie werden nicht als Review-Queue mit den zugehörigen Fragen verbunden.

## Zielbild

`LLM Proposal -> Consultant Review -> Accept / Edit / Reject -> Answer draft/reviewed`

Dabei gelten:
- Proposal bleibt unverändert auditierbar.
- Übernommene Antwort speichert Referenz auf Proposal/Import und Evidence-IDs.
- Consultant kann Text und Evidence-Verknüpfung vor Übernahme ändern.
- Ablehnung bleibt nachvollziehbar.
- LLM Confidence wird als Modell-Selbsteinschätzung bezeichnet und nicht mit Evidence Trust verwechselt.
- `needs_review`-Fragen dürfen nicht durch einen Evidence-Gap implizit als anwendbar behandelt werden; Applicability-Clarification ist eigener Zustand.
- Übernahme in eine Antwort ändert keine Claims oder Hard Gates automatisch.

## UX

Auf der Fragen-Seite bzw. in einer Review-Queue soll pro Proposal sichtbar sein:
- Frage und Domäne
- vorgeschlagene Antwort
- Begründung
- referenzierte Evidence
- LLM Confidence
- Applicability-Status
- Aktionen: `Übernehmen`, `Bearbeiten und übernehmen`, `Ablehnen`

## Provenienz

Finding aus NEXT-118, zweiter realer LLM-Bridge-Lauf mit lokal/intern betriebenem Gemma-4:26b.
