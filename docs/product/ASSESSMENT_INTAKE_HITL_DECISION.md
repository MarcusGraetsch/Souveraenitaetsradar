# HITL-Entscheidung – Assessment Intake v0.5

Stand: 2026-09-09
Status: **HITL-08 freigegeben**

Diese Entscheidung dokumentiert die menschliche Product-/Method-Owner-Freigabe des neuen Assessment-Einstiegs.

## Freigegebene Entscheidungen

### A1 – UI-Muster
**Freigegeben:** 3–4-stufiger Wizard.

Begründung: Organisations-, Workload- und Compliance-Fakten bleiben semantisch getrennt und die erste Seite wird nicht überladen.

### B1 – Workload-Klassifikation
**Freigegeben:** ein Primärtyp + mehrere Tags + natürliche Freitextbeschreibung.

Der Primärtyp hält Routing/Reporting stabil, Tags modellieren Überschneidungen, Freitext bewahrt fachlichen Kontext.

### C1 – Compliance
**Freigegeben:** bereits in v0.5 kleine, transparente regelbasierte Compliance-Kandidaten für DSGVO/NIS2/DORA/AI Act erzeugen.

Erlaubte Kandidatenzustände:
- `likely_applicable`
- `likely_not_applicable`
- `needs_review`

Jeder Kandidat muss Begründung, fehlende Fakten, Quellenreferenzen und Reviewstatus tragen. Die Kandidatenlogik ist Routing-Hilfe und **keine finale Rechtsfeststellung**. Relevante rechtliche Schlussfolgerungen benötigen HITL-04.

### D1 – C/I/A und Kritikalität
**Freigegeben:** aus dem Erstellformular entfernen und später als Business-Impact-/Schutzbedarfsreview behandeln.

Ungeprüfte Defaultwerte wie `medium` dürfen im neuen Intake nicht als scheinbar bestätigte Fakten entstehen. Regeln/LLM dürfen später Vorschläge erzeugen; finale Werte benötigen Human Review.

### E1 – Konzern / juristische Einheiten
**Freigegeben:** primäre juristische Einheit + optional mehrere weitere Einheiten im Scope.

Damit werden Tochter-/Mutter-/Schwestergesellschaften unterstützt, ohne einfache Fälle zu überfrachten.

### F – Pflichtfelder im Minimalpfad
**Freigegeben:**
- Titel des Entscheidungsfalls
- Entscheidungsfrage/Ziel
- Organisationsname
- Organisationstyp
- Sitzland + Ort
- Branche/Sektor
- Unternehmensgröße mindestens als Größenklasse
- Workload-Name
- natürliche Workload-Beschreibung
- primärer Workload-Archetyp
- primäre juristische Einheit/Workload-Zuordnung

Alle weiteren Angaben progressiv/optional bzw. nur bei Routingbedarf.

## Umsetzungsfolgen

NEXT-122 darf auf dieser Grundlage Runtime-Änderungen an Datenmodell/API/UI durchführen. Abwärtskompatibilität zur bestehenden Assessment-Runtime bleibt erhalten, bis die v0.5-Funktionalität ausreichend validiert ist.

Die bestehende pre-v0.4/v0.4-Runtime darf weiterhin alte Assessments lesen; neue v0.5-Intakes markieren Kritikalität und C/I/A initial als `unknown` statt Scheingenauigkeit zu erzeugen.

## Noch offene Human Gates

- **HITL-09:** substantieller Implementierungs-PR muss vor Merge menschlich reviewed werden.
- **HITL-04:** Compliance-Kandidaten dürfen nicht automatisch zu rechtlichen Feststellungen werden.
- **HITL-01:** der konkrete Decision-Case-/Workload-Scope bleibt im Kundenprojekt menschlich zu bestätigen.

HUMAN GATE: HITL-08 | Rolle: Product Owner + Method Owner | Ergebnis: **GO – A1, B1, C1, D1, E1 und F freigegeben am 2026-09-09.**
