# Agent Log – LLM Proposal Review Export / Restore

Datum: 2026-09-04
Issue: #59
PR: #60
Branch: `feature/mvp-audit-llm-review-export`
Rollen: developer, reviewer (Self-Review), project-coordinator
Reviewklasse: B

## Ziel

Die mit #49 eingeführte Human-Review-Auditspur für importierte LLM-Antwortvorschläge darf beim Export, Backup oder Restore eines Assessments nicht verloren gehen.

Zielkette:

`LLM Import -> Proposal -> Consultant Review -> accepted/edited/rejected -> Answer reference`

## Umsetzung

- `build_structured_export()` exportiert `llm_proposal_reviews` mit:
  - Review-ID
  - LLM-Import-ID
  - Proposal-Index
  - Question-ID
  - Entscheidung `accepted|edited|rejected`
  - finalem Review-Wert
  - Evidence-IDs
  - Answer-ID
  - Prüfnotiz
  - Zeitstempel
- Restore erzeugt neue IDs und remappt:
  - Evidence-IDs
  - Answer-IDs
  - LLM-Import-IDs
- Review-Datensätze werden auf die remappten Referenzen geschrieben.
- Structured Backup und Full Backup übernehmen die Auditspur automatisch über `assessment.json`.
- Consultant Report nennt zusätzlich die Anzahl human-geprüfter LLM-Antwortvorschläge.

## Rückwärtskompatibilität

`schemas/assessment-export.schema.json` bleibt Version `1.0`.

`llm_proposal_reviews` ist absichtlich **optional**. Dadurch bleiben ältere v1.0-Exporte ohne dieses Feld weiterhin importierbar. Neue Exporte enthalten das Feld immer, auch wenn die Liste leer ist.

## Governance

- Restore erzeugt weiterhin ein neues Assessment.
- LLM Proposal Reviews werden nicht in Claims umgewandelt.
- Restore erzeugt keine neue Gate-Wirkung aus LLM-Reviews.
- Gate Results werden weiterhin deterministisch neu berechnet und gegen die Quelle verglichen.
- Standardexport enthält weiterhin keine Raw-Evidence-Dateien oder freigegebenen Evidence-Textauszüge.
- Full Backup bleibt explizites Opt-in für Raw Evidence.

## Tests

`apps/api/tests/test_export_api.py` deckt jetzt zusätzlich ab:

1. neuer Structured Export validiert gegen das JSON Schema;
2. Review-Auditspur ist im Structured Export vorhanden;
3. Structured Backup enthält die Review-Auditspur;
4. Structured Restore remappt Evidence-, Import- und Answer-IDs korrekt;
5. Entscheidung, Question-ID, finaler Wert und Prüfnotiz bleiben erhalten;
6. Legacy-v1.0-Export ohne `llm_proposal_reviews` bleibt importierbar;
7. Full Backup Restore erhält Review-Auditspur und Raw Evidence;
8. Gate-Semantik bleibt unverändert.

CI Run `33890363159` auf Code-Head `4c42372c5b8575d8164baa66846773586a6ac887` war vollständig grün: Python/API, Frontend, Compose-Smoke und Consultant-Walkthrough.

## Produktversion

Der Structured Export trägt mit diesem Feature `product_version=0.5.0`, da der Human-Review-Pfad plus portable Auditspur gegenüber dem bisherigen 0.4.x-MVP einen neuen funktionalen Stand bildet. Das Export-Schema selbst bleibt aus Kompatibilitätsgründen v1.0.

## Self-Review

Geprüft:

- keine Änderung an Gate-Berechnung;
- keine automatische Claim-Erzeugung;
- kein Raw-Evidence-Leak im Standardexport/Report;
- Legacy-Restore bleibt möglich;
- Restore remappt statt IDs aus fremden Assessments blind wiederzuverwenden;
- neue Review-Tabelle bleibt additive Persistenz.

Keine BLOCKER gefunden.

## Offen

- Issue #26 bleibt zuständig für vollständige serverseitige JSON-Schema-Validierung untrusted Structured Imports.
- Issue #25 bleibt zuständig für ZIP-Decompression-Bomb-Hardening.
- Die reale manuelle NEXT-118-Evaluation soll den exportierten/restaurierten Review-Workflow noch aus Consultant-Sicht prüfen.
