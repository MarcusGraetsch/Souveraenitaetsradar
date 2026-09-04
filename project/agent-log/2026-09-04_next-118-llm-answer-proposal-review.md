# Agent Session – NEXT-118 LLM Answer Proposal Human Review

Datum: 2026-09-04
Branch: `feature/next-118-llm-answer-review`
PR: #58
Rollen: `developer`, `methodologist`, anschließend `reviewer/security`
Reviewklasse: C – LLM-gestützter Daten-/Entscheidungspfad mit menschlicher Bestätigung; keine automatische Gate-Wirkung

## Anlass

Der zweite reale Gemma-4:26b-Lauf im NEXT-118 Consultant-Test konnte valide, evidence-referenzierte Antwortvorschläge importieren. Diese Vorschläge waren anschließend jedoch nur in der LLM-Bridge sichtbar. Es existierte kein vollständiger fachlicher Review-Pfad vom unveränderten LLM-Proposal zur vom Consultant verantworteten Radar-Antwort.

Issue #49 definiert deshalb:

`LLM Proposal -> Consultant Review -> Accept / Edit / Reject -> Radar Answer`

## Ziel

- LLM-Proposal bleibt unverändert auditierbar.
- Consultant kann Vorschläge übernehmen, bearbeiten und übernehmen oder ablehnen.
- Die Anwendbarkeit einer Frage bleibt ein eigener Zustand.
- Nachweise werden nicht automatisch erweitert.
- LLM Confidence wird nicht mit Evidence Trust / Radar Trust vermischt.
- Eine übernommene Antwort verändert keine Claims oder Hard Gates automatisch.

## Backend

### Neue persistente Auditspur

Neue Tabelle `llm_proposal_reviews`:

- `id`
- `assessment_id`
- `llm_import_id`
- `proposal_index`
- `question_id`
- `decision` (`accepted`, `edited`, `rejected`)
- `final_answer_value`
- `evidence_ids_json`
- `answer_id`
- `reviewer_note`
- `created_at`

Unique Constraint auf `(llm_import_id, proposal_index)` verhindert doppelte Reviews.

Die neue Tabelle ist bewusst gewählt, weil das Projekt derzeit keine Alembic-Migrationen besitzt. `create_all()` kann eine neue Tabelle auf bestehenden Installationen ergänzen, ohne bestehende `answers` um neue Spalten migrieren zu müssen.

### Review API

- `GET /api/assessments/{assessment_id}/llm-bridge/proposal-reviews`
- `POST /api/assessments/{assessment_id}/llm-bridge/imports/{llm_import_id}/proposals/{proposal_index}/review`

Review-Entscheidungen:

- `accepted`: ursprünglichen Proposal-Wert übernehmen;
- `edited`: Consultant-Wert übernehmen;
- `rejected`: Auditspur speichern, keine Radar-Antwort erzeugen.

### Governance Guards

Vor `accepted` oder `edited` wird serverseitig geprüft:

1. Assessment und LLM-Import gehören zusammen.
2. Proposal existiert und wurde noch nicht reviewed.
3. aktuelle Question Applicability ist `applicable`; `needs_review` und `not_applicable` blockieren Übernahme.
4. gewählte Evidence-IDs sind Teil der ursprünglichen Proposal-Evidence-IDs.
5. gewählte Evidence-IDs existieren im Assessment.
6. finaler Answer-Wert entspricht dem methodischen `answer_control`:
   - `single_select`: nur erlaubte maschinenlesbare Werte;
   - `date`: ISO `YYYY-MM-DD`;
   - Text/List/Structured Text: nicht leer.
7. Answer und Proposal-Review werden in einer Transaktion gespeichert.

Akzeptierte/bearbeitete Antworten erhalten `review_state=reviewed`.

## Frontend

Neue Komponente `apps/web/src/LlmReviewWorkspace.tsx` in der LLM Bridge.

Pro Proposal sichtbar:

- Frage-ID, Domäne und Fragetext;
- aktuelle Anwendbarkeit;
- unveränderter KI-Vorschlag;
- Modellbegründung;
- `Modell-Selbsteinschätzung` statt `Confidence`;
- ausdrücklicher Hinweis, dass dies weder Belegstärke noch Radar Trust ist;
- referenzierte Nachweise mit Titel und ID;
- optionale Prüfnotiz.

Aktionen:

- `Übernehmen`
- `Bearbeiten`
- `Bearbeitet übernehmen`
- `Ablehnen`

Bei noch ungeklärter/nicht anwendbarer Frage sind Übernahme und Bearbeitung gesperrt; Ablehnung bleibt möglich.

Wenn der LLM-Wert nicht zum methodischen Antwortformat passt, ist direkte Übernahme ebenfalls gesperrt. Beim Bearbeiten rendert die Review-UI das passende Methoden-Control (z. B. Select oder Datum).

Unterhalb des Arbeitsbereichs bleibt ein separater `Import-Audit`, der die ursprüngliche LLM-Ausgabe unverändert zeigt.

## Gate-Isolation

Tests vergleichen Hard-Gate-Zustände vor und nach der Übernahme einer LLM-Antwort. Die Zustände bleiben identisch.

Eine Answer-Übernahme erzeugt keine Claims und keine Applied Capability. Gate-Wirkung entsteht weiterhin ausschließlich über den separaten human-bestätigten Claim-/Evidence-Pfad.

## Tests

Neue Tests decken ab:

- accepted -> reviewed Answer + Audit Record;
- edited -> Consultant-Wert statt Proposal-Wert;
- rejected -> Audit Record ohne Answer;
- doppelte Review -> HTTP 409;
- `needs_review` / `not_applicable` -> keine Übernahme;
- keine zusätzlichen Evidence-IDs gegenüber Proposal;
- Gate-Zustände unverändert;
- Single-Select-Answer muss maschinenlesbaren Methodenwert verwenden;
- Datum muss ISO-Format haben.

## Bewusste Grenze / Folgeissue

Die lokale Datenbank-Auditspur ist persistent, aber der bestehende Assessment Export/Backup/Restore v1.0 kennt `llm_proposal_reviews` noch nicht. Bei Export + Restore würde die explizite Zuordnung Proposal -> Human Review -> Answer derzeit verloren gehen, obwohl LLM-Import und Answer selbst erhalten bleiben.

Dafür wurde #59 eröffnet:
`[MVP-AUDIT] LLM-Proposal-Reviews in Export/Backup/Restore erhalten`.

Das wird nicht als gelöst dargestellt und ist eine separate Export-/Schema-Hardening-Aufgabe.

## Nicht-Scope

- LLM Claim Proposals / #40
- semantische Qualität/Confidence-Kalibrierung des Modells / #47
- vollständige AI Processing Profiles / #43
- Hard-Gate-Terminologie / #50
- Requirement-Override-Governance / #51
- dedizierte strukturierte Schemas für zusammengesetzte Answer Types / #38

## Re-Test

Nach Merge soll NEXT-118 auf der Fresh-VM mit dem bestehenden Gemma-Import erneut geprüft werden:

1. SC-01/SC-02 Proposal sichtbar;
2. Modell-Selbsteinschätzung klar getrennt;
3. Evidence-Refs sichtbar;
4. Übernehmen/Bearbeiten/Ablehnen funktionieren;
5. akzeptierte Antwort erscheint in Radar;
6. Proposal bleibt Audit-seitig unverändert;
7. Hard Gates bleiben unverändert.
