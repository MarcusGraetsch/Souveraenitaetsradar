# Agent Session – NEXT-118 Typed Answer Controls

Datum: 2026-09-04
Branch: `feature/next-118-typed-answer-controls`
Rollen: `methodologist`, `developer`, anschließend `reviewer`
Reviewklasse: B – Methodenmetadaten werden in UI-Controls umgesetzt; keine Gate-/Risk-Logik verändert

## Anlass

Der reale NEXT-118 Consultant-Test zeigte an SC-01 und SC-02, dass die Fragen-Seite für alle Fragen dasselbe Status-Dropdown `erfüllt / teilweise / nicht erfüllt / unbekannt / nicht anwendbar` verwendete. Das ist für Fakten-, Listen-, Zeit-, Rollen- und andere Erhebungsfragen semantisch falsch.

## Befund

Die bestehende Question Bank enthält bereits für alle 128 Fragen das Feld `Antworttyp`. Beispiele:

- SC-01: `Text/ID`
- SC-02: `Referenzliste`
- SC-03: `Enum 1-5`
- weitere Fragen: `Boolean`, `Boolean/Teilweise`, `Dauer`, `Größe`, `Liste`, `Länderliste`, explizite Enums und zusammengesetzte Antworttypen.

Damit lag der Hauptfehler nicht in der Methodenbank, sondern in der Weboberfläche, die diese Metadaten bislang ignorierte.

## Umsetzung

### Server

- neues Modul `apps/api/app/answer_controls.py`;
- deterministische Normalisierung von Methoden-`Antworttyp` zu einer kleinen UI-Control-Sprache;
- `method_catalog.load_questions()` liefert zusätzlich `answer_control`;
- unbekannte Typen erhalten keinen stillen Compliance-Status-Fallback, sondern `mapping_status=needs_review`.

### UI

`QuestionCard` rendert jetzt methodengesteuert:

- Text/ID, Text, Rolle/Person, Land -> Textfeld;
- Liste/Referenzliste/Länderliste -> mehrzeilige Listen-/Textantwort;
- Boolean -> Ja / Nein / Noch unklar;
- Boolean/Teilweise -> Ja / Teilweise / Nein / Noch unklar;
- Enum 1-5 -> Stufe 1 bis 5 plus Noch unklar;
- explizit kodierte Enums -> konkrete Optionen aus dem Methodentyp;
- Datum/Zeitpunkt -> Datumseingabe;
- Dauer/Größe/Prozent -> Wert mit Einheit bzw. Prozentangabe;
- zusammengesetzte Typen -> vorerst strukturierte Textantwort statt erfundener Dropdown-Semantik.

Systemische Applicability bleibt getrennt von der fachlichen Antwort. Bei `not_applicable` wird keine fachliche Antwort verlangt.

### Kompatibilität

- keine DB-Migration;
- `Answer.answer_value` bleibt String;
- Export/Restore und bestehende API-Verträge bleiben kompatibel;
- vorhandene Legacy-Werte werden nicht automatisch gelöscht oder umgeschrieben.

## Inventar-/Regressionstest

`apps/api/tests/test_answer_controls.py` scannt die vollständige Methodenbank und verlangt für alle 128 Fragen ein explizites Mapping.

Der erste CI-Lauf identifizierte genau vier noch ungemappte Typen:

- GV-02 `SOV1-8 + Schwelle`
- SP-04 `Graph/Ja-Nein`
- SE-01 `Dokument+Scope`
- TE-12 `Prozent/Enum`

Diese vier sind zusammengesetzte Antwortmodelle und werden bis zu einem eigenen Feldschema bewusst als `structured_text` behandelt.

## Grenzen / Folgearbeit

Issue #38 bleibt offen. Die aktuelle Änderung behebt den falschen universellen Dropdown und schafft eine maschinenlesbare UI-Abbildung für alle 128 Fragen. Zusammengesetzte Typen können später zu echten strukturierten Feldschemas weiterentwickelt werden.

Der nächste Produktblock ist #49: LLM Answer Proposals müssen auf der Fragen-Seite mit Human Review (`Übernehmen / Bearbeiten und übernehmen / Ablehnen`) verarbeitet werden. Dieses Review muss die hier eingeführten fachlich passenden Antwortfelder verwenden.

## Teststatus

CI Run `33876848031` auf Commit `f8d41ed0910d6a544b6ad6c32bbfee07ca5bf1a3` vollständig grün:

- Python / Repository Validator: PASS
- API Tests inkl. 128-Fragen-Answer-Control-Inventar: PASS
- Frontend TypeScript Build: PASS
- Compose Smoke: PASS
- Consultant Walkthrough: PASS
- Export/Restore: PASS
- Stop/Restart: PASS
- kompletter Uninstall: PASS

## Review

Kein Eingriff in Gate-Berechnung, Requirement-Level, Trust-Berechnung oder LLM-Gate-Isolation. Die Änderung reduziert vielmehr semantische Fehleingaben, indem sie vorhandene Methodenmetadaten sichtbar und nutzbar macht.
