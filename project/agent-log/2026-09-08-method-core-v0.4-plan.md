# Plan – Methodenkern v0.4 als Decision-Support-Methode

Datum: 2026-09-08  
Rolle: `methodologist`, `architect`, `project-coordinator`  
Branch: `method/decision-case-provider-intelligence`

## Ziel / Problem

Der bestehende Radar ist methodisch belastbar, droht aber in Beratung und Management-Kommunikation zu viel Framework-, Fragen- und Objektmodell-Overhead sichtbar zu machen. Der Methodenkern soll deshalb als verständliche, adaptive Entscheidungsmethode neu geordnet werden, ohne die vorhandene Evidence-/Gate-/Provider-Logik zu verlieren.

## Scope

- neuen deutschsprachigen Methodenkern v0.4 dokumentieren
- Rolle von BSI 200-3, Bitkom 2026, EU Cloud Sovereignty Framework, BSI C3A, Data Act, NIS2, DORA, C5 und kundenspezifischer Compliance klar trennen
- Status quo / Nichtstun und Business-/Innovationsnutzen als explizite Entscheidungsdimension aufnehmen
- 128 Fragen als adaptive Question Library, nicht als Standardfragebogen festschreiben
- vorhandene Kundenartefakte und Interviews als kombinierte Intake-Kanäle strukturieren
- ArchiMate/CMDB/IaC/BIA/ISMS/Verträge/Tests als optionale Datenquellen definieren, nie als Voraussetzung
- politische/geopolitische Sorgen in prüfbare Szenarien übersetzen statt Länder-/Provider-Pauschalurteile zu verwenden
- Glossar, Source Guide und Projektentscheidungen entsprechend aktualisieren

## Nicht-Scope

- keine Runtime-/DB-/API-/UI-Änderung
- keine neue Scoring-Formel
- keine Provider-Rangliste
- keine konkreten Providerbewertungen
- keine neuen regulatorischen Schwellen

## Quellen / Provenienz

Primär: `SRC-01`, `SRC-03`, `SRC-04`, `SRC-05`, `SRC-06`, `SRC-08`, `SRC-12`, `SRC-17`, `SRC-21`, `INT-04` sowie neue interne Herleitung `INT-05`.

Externe Aussagen werden als `external-direct` oder `external-derived`, neue Strukturierungsregeln als `internal-method` gekennzeichnet.

## Daten-/Security-Risiko

Keine Kundendaten. Keine Raw Evidence. Keine Credentials. Nur Methodendokumentation und Projektmetadaten.

## Akzeptanzkriterien

1. Methodenkern ist in 5 Minuten erklärbar und trennt Beratungsoberfläche von interner Wissens-/Frameworktiefe.
2. BSI 200-3 bleibt Anschluss-/Deep-Dive-/Vollständigkeitsreferenz, aber nicht zwingende Primärmethode für jeden Fall.
3. Bitkom/EU-CSF/C3A/Data-Act-Rollen sind klar beschrieben.
4. DORA/NIS2/DSGVO/AI-Act etc. werden als aktivierbare Overlays statt universeller Basis behandelt.
5. Status quo, Chancen/Innovation, Kosten und geopolitische Szenarien sind explizit im Entscheidungsbild enthalten.
6. Question Library und adaptive Vertiefung sind dokumentiert.
7. Optionaler Artefakt-Import + Interviewworkflow ist dokumentiert.
8. Glossar und Decisions sind konsistent.

## Tests / Reviewklasse

Reviewklasse B – Methode/Architektur.

Prüfen:
- YAML-Syntax von `project/DECISIONS.yaml`
- keine neuen unmarkierten Normbehauptungen
- Glossar-/Methodenlinks auflösbar
- keine Runtime-Regressions zu erwarten, da Dokumentations-/Metadatenänderung
- Self-Review auf Providerneutralität, Verständlichkeit und Overhead
