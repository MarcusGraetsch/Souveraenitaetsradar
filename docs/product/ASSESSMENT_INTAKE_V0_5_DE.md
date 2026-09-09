# Assessment Intake / Decision Context v0.5 – Entwurf

Status: **Product-/Methodenentwurf, nicht Runtime-verbindlich**
Datum: 2026-09-09

## Ziel

Der Einstieg in ein neues Assessment soll genügend belastbare Rahmeninformationen erfassen, damit der Souveränitäts-Radar spätere Fragen, Compliance-Overlays, Schutzbedarfs-/Business-Impact-Vorschläge und Variantenvergleiche gezielt vorbereiten kann – ohne den Consultant beim ersten Bildschirm mit einem Vollassessment zu überladen.

Der heutige Runtime-Stand (`Name`, `Kunde`, Beschreibung, Workload-Typ, Kritikalität, C/I/A, Kontrollraum, freier regulatorischer Kontext) ist dafür zu flach und teilweise semantisch falsch platziert.

## Leitprinzipien

1. **Fakten vor Bewertungen.** Beim Anlegen werden möglichst beobachtbare Organisations-, Standort- und Workload-Fakten erhoben. Kritikalität, Schutzbedarf oder Rechtsanwendbarkeit werden daraus später vorgeschlagen und bestätigt.
2. **Natürliche Sprache + strukturierte Felder.** Ein Consultant soll den Workload frei beschreiben können; strukturierte Felder ermöglichen deterministic routing und nachvollziehbare Compliance-Kandidaten.
3. **Automatisierung schlägt vor, Mensch bestätigt.** LLMs und Regeln dürfen klassifizieren und Kandidaten ableiten, aber keine endgültige Rechtsanwendbarkeit, Schutzbedarfsfeststellung oder Risikoakzeptanz erzeugen.
4. **Organisation ist nicht nur ein Kundenname.** Konzern, juristische Einheit, Standort und Workload-Zuordnung werden getrennt modelliert.
5. **Adresse ist ein Signal, keine Compliance-Entscheidung.** Rechts-/Regelungsanwendbarkeit hängt zusätzlich von Tätigkeit/Sektor, Unternehmensgröße, Rolle, Datenverarbeitung, Nutzungsort und weiteren Kriterien ab.
6. **Progressive Erfassung.** Nur die Informationen, die für Routing oder spätere Entscheidungen voraussichtlich relevant sind, werden früh erhoben; Spezialfragen bleiben Deep Dive.

## Vorgeschlagener Einstieg als Wizard

### Schritt 1 – Entscheidungsfall

Pflichtfelder:
- **Titel des Entscheidungsfalls** – klare Beschriftung statt unspezifisch `Name`.
  - Beispiel: `Betriebsmodell KI-Assistent Bürgerdienste`.
- **Entscheidungsfrage / Ziel** – natürliche Sprache.
  - Beispiel: `Welche Betriebsvariante bietet ausreichende Souveränität bei vertretbarem Aufwand?`

Optional:
- internes Projekt-/Aktenzeichen
- Consultant/Owner
- gewünschter Entscheidungstermin

Hinweis: Der Entscheidungsfall ist nicht dasselbe wie Kunde oder Workload.

### Schritt 2 – Organisation / Kunde

Mindestens:
- Organisationsname
- Organisationstyp: Unternehmen / Behörde / sonstige öffentliche Stelle / Non-Profit / Sonstiges
- primäre juristische Einheit
- Sitz/registrierte Adresse: Land, Postleitzahl, Ort; Straße optional für Compliance-Routing normalerweise nicht nötig
- weitere Länder, in denen relevante Tätigkeiten/Dienste erbracht werden
- Branche/Sektor
- Beschäftigtenzahl oder Größenklasse
- optional Umsatz und Bilanzsumme, wenn für Größenklassifizierung/Regelungsprüfung relevant
- Konzern-/Gruppenstruktur vorhanden? ja/nein/unklar

Bei Gruppenstruktur optional wiederholbar:
- Muttergesellschaft
- Tochter-/Schwestergesellschaften im Scope
- Land/Sitz der jeweiligen juristischen Einheit
- Rolle im Decision Case: Workload Owner / Betreiber / Datenverantwortlicher / Vertragspartner / Nutzergruppe

### Schritt 3 – Workload

Pflicht:
- **Workload-Name**
- **kurze natürliche Beschreibung** (mehrzeilig)
- **primärer Workload-Archetyp**

Vorgeschlagene primäre Archetypen:
- Fachanwendung / Business Application
- SaaS-Anwendung
- Daten-/Analyseplattform
- Integrations-/API-Service
- Cloud-/Plattformdienst
- KI-System
- KI-Agent / agentisches System
- Entwicklungs-/CI-CD-/DevOps-Plattform
- Identitäts-/IAM-/Trust-Service
- Datenbank-/Storage-Service
- Infrastruktur-/Compute-Plattform
- End-User-/Collaboration-Service
- OT/IoT/Edge-System
- Sonstiges

Zusätzlich **Mehrfach-Tags** statt Mehrfachauswahl beim Primärtyp, z. B.:
- `ai`
- `agentic`
- `internet_exposed`
- `customer_facing`
- `internal`
- `data_intensive`
- `identity_critical`
- `real_time`
- `regulated_process`
- `multi_provider`

Begründung: Ein einzelner primärer Typ hält Routing und Reports eindeutig; Tags erlauben überlappende Eigenschaften.

Weitere frühe Workload-Fakten:
- welche juristische Einheit(en) besitzt/betreibt/nutzt den Workload?
- hauptsächliche Nutzergruppen und Nutzungsländer
- verarbeitet der Workload personenbezogene Daten? ja/nein/unklar
- verarbeitet er besonders schützenswerte/sensible Fach- oder Geschäftsdata? ja/nein/unklar
- KI eingesetzt? ja/nein/unklar; falls ja Rolle grob: provider/deployer/integrierter Drittservice/unklar
- externer Anbieter/Cloud/SaaS bereits im Scope? ja/nein/unklar
- aktueller Betriebszustand: On-Prem / Private Cloud / Public Cloud / SaaS / Hybrid / Multi-Cloud / noch offen

### Schritt 4 – Vorläufiger Organisations-/Regelungskontext

Nicht als freies Feld `Regulatorischer Kontext`, sondern als **automatisch erzeugte Kandidatenliste**.

Die Engine erhält strukturierte Fakten und erzeugt pro Regelwerk:
- `candidate_status`: likely_applicable / likely_not_applicable / needs_review
- `rationale`: welche Fakten/Regeln führten zum Vorschlag
- `missing_facts`: welche Angaben für eine belastbarere Einordnung fehlen
- `source_refs`: normative Quellen
- `review_status`: not_reviewed / human_confirmed / human_rejected

Beispiele:
- DSGVO
- NIS2 / nationales Umsetzungsgesetz
- DORA
- AI Act
- sektorspezifische Regeln
- BSI-/öffentliche-Verwaltungsprofile
- kundeneigene Policies

Wichtig: `candidate_status` ist **keine Rechtsberatung und keine finale Anwendbarkeitsentscheidung**. Relevante rechtliche Schlussfolgerungen benötigen HITL-04.

## Warum Adresse allein nicht reicht

### NIS2
Anwendbarkeit hängt u. a. von Sektor/Tätigkeit, Unternehmensgröße und Tätigkeit/Dienstleistung in der EU ab; zusätzliche Sonderfälle können unabhängig von der normalen Größenschwelle erfasst sein. Daher benötigt das Tool mindestens Sektor, Größenfakten und Tätigkeitsländer.

### DORA
DORA gilt für definierte Arten von Finanzunternehmen und bestimmte ICT-Drittdienstleister. Standort allein klassifiziert die Organisation nicht.

### DSGVO
Entscheidend sind Verarbeitung personenbezogener Daten, Niederlassung/Marktbezug bzw. Verhalten betroffener Personen, nicht lediglich die Postanschrift des Kunden.

### AI Act
Anwendbarkeit hängt neben territorialem Bezug auch von der Rolle im KI-Lebenszyklus (z. B. Provider/Deployer) und der konkreten Verwendung ab.

Daraus folgt: Adresse ist ein nützlicher Input für Jurisdiktion und Routing, aber nur ein Baustein einer Compliance-Kandidatenlogik.

## Kritikalität und C/I/A nicht mehr als Pflichtfelder beim Anlegen

Der aktuelle Einstieg erzwingt `criticality` und C/I/A mit Default `medium`. Das erzeugt Scheingenauigkeit: Ein nicht geprüfter Default fließt bereits als scheinbarer Fakt in spätere Logik ein.

### Zielmodell

Beim Intake zunächst keine finale Bewertung verlangen.

Stattdessen später eigener Schritt `Business Impact & Schutzbedarf`:
- betroffene Geschäftsprozesse/Funktionen
- Ausfallfolgen und tolerierbare Unterbrechung
- Daten-/Informationsarten
- Folgen von Offenlegung, Manipulation und Nichtverfügbarkeit
- finanzielle, rechtliche, operative, gesellschaftliche/reputative Schäden
- vorhandene BIA-/BCM-/ISMS-Werte importierbar

Regeln/LLM dürfen daraus **Vorschläge** generieren:
- suggested criticality
- suggested confidentiality/integrity/availability
- Begründung
- Confidence
- zugrunde liegende Fakten

Finale Werte benötigen Consultant/Customer Review. Ein Workload-Archetyp darf höchstens Routing-Hinweise oder typische Fragen aktivieren, aber nicht allein einen finalen Schutzbedarf festlegen.

## Automatische Vorbewertung nach dem Intake

Nach Abschluss der ersten 3 Schritte sollte das Tool sofort einen transparenten `Pre-Assessment Context` erzeugen:

1. erkannte Workload-Tags / Klassifikationsvorschläge
2. Compliance-/Regelwerkskandidaten mit Status und Begründung
3. fehlende Organisations-/Scope-Fakten
4. vorgeschlagene Deep-Dive-Profile
5. Vorschlag, welche 15–25 Screeningfragen besonders relevant sind
6. optional Schutzbedarfs-/Kritikalitätshinweise, ausdrücklich `unreviewed`
7. erkannte Konzern-/Jurisdiktionskomplexität

Keine dieser Vorbewertungen darf bereits eine finale Souveränitätsbewertung erzeugen.

## Datenmodell – minimale neue Konzepte

Der bestehende flache `Assessment`-Datensatz sollte langfristig nicht weiter mit immer mehr Strings angereichert werden.

Vorgeschlagene Trennung:

- `DecisionCase`
- `Organization`
- `LegalEntity`
- `Location`
- `OrganizationActivityProfile`
- `OrganizationSizeFacts`
- `Workload`
- `WorkloadEntityRole` (Zuordnung Workload ↔ LegalEntity)
- `WorkloadClassification` (primär + Tags + Herkunft + Reviewstatus)
- `ComplianceApplicabilityCandidate`
- `BusinessImpactProfile`

Diese Begriffe sind Software-/Methodenmodellierung; keine externen Normbegriffe, soweit nicht im Glossar anders ausgewiesen.

## Import-/Automatisierungsoptionen

Später können Intake-Fakten optional aus vorhandenen Quellen vorbelegt werden:
- CRM/Kundenstammdaten
- CMDB/Servicekatalog
- ArchiMate Model Exchange
- Architekturdiagramme
- BIA/BCM
- ISMS/Risikoregister
- Verträge
- IaC/GitOps

Import erzeugt zunächst Vorschläge/Fakten mit Provenienz; er ersetzt nicht automatisch Human Review.

## Nicht tun

- keine globale Regel `Adresse Deutschland -> NIS2/DSGVO gilt`
- keine automatische Rechtsfeststellung allein aus Firmennamen oder Geocoding
- keine finale C/I/A-Klassifizierung allein aus Workload-Kategorie oder LLM-Text
- keine 30+ Pflichtfelder auf einem einzigen Bildschirm
- kein vollständiges Konzernmodell als Voraussetzung für einen einfachen Fall
- keine Vermischung von `Assessment-Name`, `Kunde` und `Workload-Name`

## Offene Product-/Methodenentscheidungen

Vor Runtime-Implementierung müssen Product Owner / Method Owner mindestens entscheiden:

1. Wizard mit 3–4 Schritten oder ein progressiv aufklappbares Formular?
2. Welche Organisationsfelder sind im Minimalpfad Pflicht?
3. Welche Workload-Archetypen werden als v0.5-Startliste akzeptiert?
4. Primärtyp + Mehrfach-Tags als Klassifikationsmodell akzeptieren?
5. Soll die erste Runtime-Version bereits Compliance-Kandidaten regelbasiert ableiten oder zunächst nur die dafür nötigen Fakten erfassen?
6. C/I/A/Kritikalität vollständig aus `Assessment anlegen` entfernen und in einen späteren Review-Schritt verschieben?
7. Wie viele juristische Einheiten sollen im ersten UI-Release unterstützt werden: eine primäre + optionale weitere oder beliebig viele?

## Human Gates

- **HITL-08:** Freigabe des Intake-Zielbilds zur Runtime-Migration.
- **HITL-09:** Review vor Merge der substantiellen Produkt-/Methodenänderung.
- **HITL-04:** Jede später automatisch vorgeschlagene rechtliche Anwendbarkeit bleibt reviewpflichtig.
- **HITL-01:** Workload-/Decision-Case-Scope bleibt menschlich zu bestätigen.

