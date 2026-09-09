# NEXT-122 – Assessment Intake / Decision Context v0.5 Implementierung

Datum: 2026-09-09
Status: in Umsetzung

## Human Gate

HITL-08 wurde durch Product Owner + Method Owner explizit freigegeben:

- A1: 3–4-stufiger Wizard
- B1: Primär-Archetyp + Mehrfach-Tags + Freitext
- C1: transparente Compliance-Kandidaten für DSGVO/NIS2/DORA/AI Act
- D1: C/I/A und Kritikalität aus dem Intake entfernen
- E1: primäre + optionale weitere juristische Einheiten
- F: definierter Minimalpflichtsatz

Quelle der Freigabe: `docs/product/ASSESSMENT_INTAKE_HITL_DECISION.md`.

## Implementierter Stand

### API / Datenmodell

- neue strukturierte Pydantic-Schemas für Decision Case, Organisation, Legal Entities und Workload
- neue separate Persistenz `assessment_intake_contexts` statt weiterer flacher Strings im Legacy-Assessment
- neuer Endpoint `POST /api/assessment-intakes`
- neuer Endpoint `GET /api/assessments/{assessment_id}/intake`
- bestehende `/api/assessments`-API bleibt erhalten
- neue v0.5-Intakes legen Legacy-Felder `criticality`, `confidentiality`, `integrity`, `availability` bewusst als `unknown` an

### Pre-Assessment

Deterministische Routing-Hilfe erzeugt:
- Workload-Tags
- Compliance-Kandidaten mit `likely_applicable / likely_not_applicable / needs_review`
- Begründung und Missing Facts
- Source Refs aus dem bestehenden Source Guide
- `review_status=not_reviewed`
- vorgeschlagene Deep-Dive-Profile
- Screening-Fokus
- Jurisdiktions-/Entity-Komplexität

Compliance-Kandidaten sind ausdrücklich keine Rechtsfeststellung; HITL-04 bleibt erforderlich.

### UI

- neues Intake-Wizard-Overlay vor dem bisherigen `Neues Assessment`-Formular
- Schritt 1: Entscheidungsfall
- Schritt 2: Organisation
- Schritt 3: Workload + primäre/weitere Legal Entities
- Schritt 4: Zusammenfassung und anschließend Pre-Assessment-Ausgabe
- C/I/A/Kritikalität werden im Wizard nicht abgefragt

Die Integration ist absichtlich additiv, damit die bestehende Assessment-Runtime und alte Assessments zunächst abwärtskompatibel bleiben.

## Tests

Neue Tests prüfen insbesondere:
- Compliance-Ausgaben bleiben unreviewed und ausdrücklich nicht final
- C/I/A und Kritikalität bleiben unassessed/unknown
- strukturierter Intake wird separat persistiert
- mehrere Legal Entities werden unterstützt
- C3A-/Cloud-Deep-Dive wird bei passenden Cloud-/Provider-Fakten vorgeschlagen

## Offene Punkte vor Merge

1. CI vollständig grün.
2. UI-Wizard auf echter Runtime gegen NEXT-118 manuell testen.
3. Product-/Method-Owner prüft insbesondere Pflichtfelder, Begriffe, Workload-Archetypen und Compliance-Kandidaten.
4. HITL-09 vor Merge dokumentieren.
5. Nach Merge NEXT-118 am neuen Intake fortsetzen.

HUMAN GATE: HITL-09 | Rolle: Product Owner + Method Owner | Status: noch offen bis CI und manueller UI-Test vorliegen.
