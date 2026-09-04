# NEXT-118 – Multichannel Intake / ADOIT Reference Finding

Datum: 2026-09-04
Rollen: architect, methodologist, project-coordinator
Reviewklasse: B/C

## Anlass

Im ersten realen Consultant-Test wurde das bisherige Formular-/Relevanzprofil-Konzept weiter hinterfragt. Zusätzlich zu natürlicher Sprache sollen bestehende Kundenartefakte wiederverwendet werden. Gleichzeitig ist für den Projektkontext ein ADOIT-/BOC-Showcase relevant: Souveränitätsbewertung soll demonstrierbar aus natürlicher Beschreibung **und** vorhandenen ADOIT-/Architekturinformationen entstehen.

## Entscheidung / Produktbild

- Natürliche Sprache und Artefakte sind komplementäre First-Class-Intake-Kanäle.
- Beide Kanäle schreiben in dasselbe kanonische Context Model.
- Natürliche Sprache ist besonders wichtig für Nutzungskontext, Zielbild, organisatorische Realität und noch nicht modellierte Informationen.
- Strukturierte Artefakte sind besonders wichtig für explizite technische/architektonische Facts und nachvollziehbare Beziehungen.
- Context Facts sind nicht automatisch Evidence.
- Jede AI-gestützte Strukturierung benötigt ein explizites Processing Profile.
- ADOIT ist priorisierter Referenz-/Showcase-Adapter, der Methodenkern bleibt vendorneutral.

## ADOIT-Verifikation

Offizielle BOC-Dokumentation wurde für den Entwurf geprüft. Bestätigt sind aktuell u. a.:

- ArchiMate Model Exchange Import/Export in ADOIT,
- Repository-Export im AXR-Format,
- Excel-Schnittstellen für Objekt-/Attributdaten.

Daraus folgt: `ArchiMate YAML` wird nicht als natives ADOIT-Exportformat in die Methode aufgenommen, solange die konkrete Quelle/Transformation nicht geklärt ist. Generische YAML-Artefakte bleiben unabhängig davon unterstützungswürdig.

## Neue/aktualisierte Arbeitspakete

- #44 neuer Referenzfall: ADOIT + natürliche Sprache als Showcase.
- #37 Conversational Intake um Gleichwertigkeit mit Artefakt-Intake ergänzt.
- #41 Artifact-Ingestion um First-Class Natural Language ergänzt.
- #42 ADOIT priorisiert und Exportformat-Verifikation präzisiert.
- #43 Processing Profiles für natürliche Sprache + Artefakte präzisiert.
- #28 NEXT-118 mit dem Finding aktualisiert.

## Repository-Artefakte

- `docs/product/MULTICHANNEL_CONTEXT_INTAKE.md`
- `project/DECISIONS.yaml` DEC-032 bis DEC-035

## Datenschutz-/Security-Risiko

Besonders sensibel sind Architektur-, Vertrags-, IAM-, Host-/System-, Personen- und Security-Daten. `Radar strukturiert Kontext` darf niemals implizit bedeuten, dass ein vollständiges Artefakt an ein externes LLM gesendet wird. Raw Evidence bleibt standardmäßig lokal; externe Verarbeitung ist minimiert/redigiert oder explizit freigegeben.

## Nächster Validierungsschritt

NEXT-118 wird fortgeführt. Unmittelbar als Nächstes wird die bestehende Copy/Paste LLM Bridge manuell getestet. Danach sollen die realen Findings priorisiert und ein kleiner Referenzpilot `natürliche Sprache + ADOIT/EA + ergänzendes technisches/tabellarisches Artefakt` spezifiziert werden.
