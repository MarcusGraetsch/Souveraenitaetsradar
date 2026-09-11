# HITL-Entscheidungsvorlage – Assessment Intake v0.5

Stand: 2026-09-11

Diese Vorlage dokumentiert die menschlichen Freigaben und Folgekorrekturen für den neuen Assessment-Einstieg.

## Entscheidung A – UI-Muster
- A1: 3–4-stufiger Wizard
- A2: ein Formular mit progressiv aufklappbaren Bereichen

**Entscheidung: A1 freigegeben.**

Der Wizard besteht aus vier Schritten:
1. Entscheidungsfall
2. Organisation
3. Workload & Beteiligte
4. Prüfen & Speichern

Die automatische Voranalyse wird **erst nach** dem expliziten Speichern erzeugt und angezeigt.

## Entscheidung B – Workload-Klassifikation
- B1: ein Primärtyp + mehrere Tags
- B2: reine Mehrfachauswahl ohne Primärtyp
- B3: nur freie Beschreibung

**Entscheidung: B1 freigegeben.**

Folgekorrektur aus HITL-Review Runde 2: technische Tag-Codes bleiben intern stabil, werden in der UI aber ausschließlich als verständliche fachliche Labels angezeigt.

## Entscheidung C – Compliance
- C1: bereits in v0.5 regelbasierte Compliance-Kandidaten erzeugen
- C2: in v0.5 zunächst nur die nötigen Fakten erfassen; Ableitung später

**Entscheidung: C1 freigegeben.**

Umfang: DSGVO, NIS2, DORA, EU AI Act mit `likely_applicable / likely_not_applicable / needs_review`, Begründung, fehlenden Fakten und Human Review. Keine finale Rechtsfeststellung.

Folgekorrektur aus HITL-Review Runde 2: maschinennahe Status-/Framework-Codes werden für Menschen übersetzt. Vor dem Speichern wird keine Voranalyse angezeigt.

## Entscheidung D – C/I/A und Kritikalität
- D1: aus dem Erstellformular entfernen und später als Business-Impact-/Schutzbedarfsreview behandeln
- D2: optional im Erstellformular lassen
- D3: verpflichtend beibehalten

**Entscheidung: D1 freigegeben.**

Ungeprüfte Defaultwerte wie `medium` erzeugen Scheingenauigkeit. Neue v0.5-Intakes setzen diese Felder intern auf `unknown`.

## Entscheidung E – Konzern / juristische Einheiten
- E1: primäre juristische Einheit + optional mehrere weitere Einheiten im Scope
- E2: zunächst nur eine juristische Einheit
- E3: vollständiges Konzernmodell als Pflicht

**Entscheidung: E1 freigegeben.**

Folgekorrektur aus HITL-Review Runde 2: `Konzern-/Gruppenstruktur = ja/nein/unklar` wird nicht mehr als frühe sichtbare Intake-Frage gestellt. Mehrgesellschafts-/Tochterkonstellationen werden konkret über die Legal Entities modelliert. Mehrere Entities im Scope erzeugen einen Hinweis auf Scope-Komplexität; die vollständige Konzernstruktur ist kein Intake-Pflichtobjekt.

## Entscheidung F – Pflichtfelder im Minimalpfad
Freigegebene Pflichtfelder:
- Titel des Entscheidungsfalls
- Entscheidungsfrage/Ziel
- Organisationsname
- Organisationstyp
- Sitzland + Ort
- Branche/Sektor
- Workload-Name
- natürliche Workload-Beschreibung
- primärer Workload-Archetyp
- primäre juristische Einheit/Workload-Zuordnung

Die Organisationsgröße darf zunächst `noch unklar` bleiben und wird dann als offener Scope-Fakt ausgewiesen.

## Folgeentscheidung G – Branche / Sektor
HITL-Review Runde 2 hat den reinen Freitext verworfen.

**Zielbild:**
- kuratiertes Dropdown `Primärer Sektor` als Routing-Hilfe,
- separates Freitextfeld `Tätigkeit / Zusatzinfo`,
- bei `Sonstiges` ist Zusatzinfo verpflichtend,
- keine Behauptung, dass die Produktauswahl bereits eine rechtlich verbindliche NIS2-/DORA-Klassifikation darstellt.

Die Auswahl deckt zentrale NIS2-Sektoren sowie allgemeine Wirtschaftssektoren ab. Eine spätere formale Wirtschaftszweigklassifikation kann separat an NACE Rev. 2.1 angebunden werden.

## Governance

HITL-08 ist abgeschlossen. Die Runtime-Implementierung ist zulässig.

HITL-04 bleibt für rechtlich relevante Compliance-Schlussfolgerungen zwingend.

HITL-09 bleibt vor Merge offen: Product Owner + Method Owner müssen den aktualisierten Einstieg manuell prüfen und ausdrücklich freigeben.
