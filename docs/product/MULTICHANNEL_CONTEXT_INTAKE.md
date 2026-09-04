# Multichannel Context Intake – natürliche Sprache + bestehende Artefakte

Stand: 2026-09-04
Status: Produkt-/Architekturentwurf aus NEXT-118
Provenienz: `internal-method` / `project-assumption`; konkrete Tool-/Exportdetails sind vor Implementierung gegen Primärdokumentation zu verifizieren.

## 1. Zielbild

Der Souveränitäts-Radar soll nicht als formularzentrierter Fragebogen funktionieren. Der Consultant bzw. Kunde beschreibt den Bewertungsgegenstand in natürlicher Sprache **und/oder** stellt bereits vorhandene Artefakte bereit. Beide Kanäle sind First-Class-Inputs und werden in dasselbe kanonische Kontextmodell überführt.

```text
Natürliche Sprache / Interview / Transkript
                    +
EA-/Architektur-/CMDB-/Cloud-/IaC-/ISMS-/Office-Artefakte
                    ↓
          Safe Local Intake Layer
                    ↓
Parser / Adapter / AI-gestützte Extraktion
                    ↓
normalisierte Facts / Entities / Relations + Provenienz
                    ↓
         Vorschläge / Unsicherheiten
                    ↓
              Human Review
                    ↓
bestätigter Assessment-Kontext
                    ↓
Applicability / Questions / Evidence Plan
                    ↓
Claims / Hard Gates / Ergebnis
```

## 2. Warum natürliche Sprache gleichwertig wichtig ist

Strukturierte Architekturmodelle bilden nicht automatisch den tatsächlichen Nutzungskontext ab. Natürliche Sprache kann Informationen enthalten, die in EA-/CMDB-Modellen fehlen, zum Beispiel:

- Zweck und fachliche Nutzung eines Systems,
- geplante Änderungen oder noch nicht modellierte Zielarchitektur,
- tatsächliche Verantwortlichkeiten,
- implizite Abhängigkeiten und operative Workarounds,
- geplante KI-/Agentenfunktionen,
- Umgang mit Daten und Nutzergruppen,
- bekannte Unsicherheiten oder offene Entscheidungen,
- Erwartungen an Exit, Autonomie, Kontrollraum oder regulatorische Rahmenbedingungen.

Deshalb gilt nicht `Artefakt statt Sprache`, sondern `Artefakt + Sprache + Human Review`.

Ein natürlichsprachlicher Input ist jedoch nicht automatisch technische Evidence. Für konkrete technische oder vertragliche Aussagen bleibt ein maschinenlesbarer Export, Vertrag, Testprotokoll oder anderer Nachweis stärker. Der Radar muss daher **Kontext-Fact**, **Evidence** und **Trust** getrennt halten.

## 3. Quellenklassen

### 3.1 Natürliche Sprache

- Freitextbeschreibung des Bewertungsgegenstands,
- Interviewnotizen,
- Workshop-Protokolle,
- später optional Spracheingabe/Transkript,
- natürliche Ergänzungen zu importierten Modellen: „Dieses Interface ist im Modell noch nicht enthalten“ oder „Der Service wird nur für Tochtergesellschaft X eingesetzt“.

### 3.2 Strukturierte und halbstrukturierte Artefakte

- CSV/XLSX/Tabellen,
- JSON/YAML/XML,
- ArchiMate-/EA-Austauschformate,
- CMDB-/Inventarexporte,
- Cloud-/Kubernetes-/IaC-Exporte,
- Grundschutz-/ISMS-/SAM-/Infrastrukturanalysen,
- Verträge und Assurance-Dokumente,
- PDF/SVG/PNG/Screenshots,
- bestehende Beratungsworkbooks.

## 4. Prioritätsregel ohne Abwertung natürlicher Sprache

Quellen werden nicht global in eine einzige Rangfolge gebracht. Stattdessen gilt:

- **für Nutzungskontext, Zielbild und organisatorische Realität** kann natürliche Sprache die primäre Quelle sein;
- **für explizit modellierte Architekturbeziehungen** ist eine strukturierte EA-/CMDB-Quelle vorzuziehen;
- **für technische Konfiguration** ist ein kundenseitig erzeugter Export einer Bildinterpretation vorzuziehen;
- **für vertragliche Aussagen** ist der Vertrag/DPA/SLA die primäre Evidence;
- **für getestete Fähigkeiten** ist ein Testprotokoll stärker als eine bloße Dokumentationsaussage.

Wenn eine strukturierte Quelle existiert, soll ein Screenshot nicht die primäre Wahrheit für exakt dieselbe technische Aussage werden. Natürlichsprachliche Ergänzungen bleiben dennoch zulässig und werden als eigene Quelle mit Review-State geführt.

## 5. Kanonisches Kontextmodell

Alle Intake-Kanäle schreiben in dasselbe provider- und toolneutrale Zwischenmodell. Importer/LLM-Adapter enthalten keine Risiko- oder Gate-Logik.

Beispielobjekte:

- Organisation / Legal Entity / Standort,
- Assessment Subject / Komponente / Service,
- Application / Platform / Infrastructure Resource,
- Business Process / Critical Function,
- Data Store / Data Flow / Interface / Dependency,
- Provider / Contract / Subprocessor,
- Identity / Trust Anchor / Key / Region,
- Source Artifact / Evidence Record,
- extracted Fact / Relation / Uncertainty.

Jeder extrahierte oder vorgeschlagene Fact benötigt mindestens:

- `source_type`,
- `source_artifact` oder `conversation/input reference`,
- Locator/Abschnitt/Objekt-ID soweit verfügbar,
- Parser-/Adapter-/Prompt-Version,
- Confidence,
- Review-State `suggested | confirmed | overridden | unknown`,
- optional Konfliktbezug zu anderen Facts.

## 6. ADOIT als priorisierter Referenz-/Showcase-Fall

ADOIT ist für das Projekt ein besonders wichtiger Referenzfall, auch im Kontext eines geplanten Vortrags gegenüber bzw. mit BOC. Der Showcase soll demonstrieren, wie **bestehende Enterprise-Architecture-Informationen und natürliche Sprache gemeinsam** zu einer nachvollziehbaren Souveränitätsbewertung führen.

Wichtig: Der Radar bleibt vendorneutral. ADOIT ist ein priorisierter Adapter und Demonstrator, nicht Voraussetzung der Methode.

### 6.1 Relevante ADOIT-Quellen

Vor Implementierung je eingesetzter ADOIT-Version zu verifizieren:

- ArchiMate Model Exchange Format,
- Excel-Schnittstellen/-Exporte,
- Repository-/Objekt-/Relations-Exporte,
- Diagramm-/View-Informationen,
- ggf. weitere freigegebene Export-/API-Möglichkeiten.

ADOIT dokumentiert aktuell u. a. ArchiMate Model Exchange und Repository-/Excel-Import-/Exportmöglichkeiten. Konkrete Begriffe wie „ArchiMate YAML“ dürfen nicht als unterstütztes ADOIT-Nativformat angenommen werden, bevor die tatsächliche Quelle/Transformation geklärt ist. Generische YAML-Dateien bleiben selbstverständlich ein möglicher Radar-Input.

### 6.2 Referenzdemo

```text
1. Consultant/Kunde beschreibt einen geplanten Cloud-/KI-Service in eigenen Worten.
2. ADOIT-Modell/Export wird zusätzlich bereitgestellt.
3. Radar extrahiert Elemente, Beziehungen, Views und Attribute aus der strukturierten Quelle.
4. AI/LLM strukturiert die natürliche Beschreibung und ordnet sie dem Modell zu.
5. Radar zeigt:
   - bestätigte Übereinstimmungen,
   - neue vorgeschlagene Facts,
   - Widersprüche,
   - fehlende Informationen,
   - Confidence und Quelle.
6. Consultant bestätigt oder korrigiert.
7. Erst der bestätigte Kontext steuert Relevanzprofil, Fragen und Evidence Plan.
8. Evidence/Antworten können später LLM-Claim-Proposals erzeugen.
9. Nur human-reviewed Claims wirken auf die deterministische Gate Engine.
```

### 6.3 Kernbotschaften für den BOC-/ADOIT-Kontext

- Vorhandene EA-Investitionen werden weiterverwendet statt durch einen neuen Fragebogen ersetzt.
- Natürliche Sprache liefert den tatsächlichen Nutzungskontext und ergänzt Modelllücken.
- LLMs sind Extraktions-/Zuordnungs-/Analyseassistenz, nicht die Risiko- oder Legal-Engine.
- Jede Ableitung bleibt quellenbezogen, nachvollziehbar und human-reviewbar.
- Dasselbe Konzept funktioniert auch mit anderen EA-, CMDB-, Cloud-, IaC- und Office-Quellen.

## 7. AI- und Datenschutzgrenze

Die Aktion „Radar strukturiert Kontext“ darf nicht gleichbedeutend mit „Datei ungeprüft an ein LLM senden“ sein.

Vor AI-Verarbeitung ist ein Processing Profile anzuwenden:

1. `NO_AI / LOCAL_PARSER_ONLY`
2. `INTERNAL_LLM_ALLOWED`
3. `EXTERNAL_REDACTED_ONLY`
4. `EXTERNAL_APPROVED`

Grundregeln:

- Raw Artefakte bleiben standardmäßig lokal.
- Secrets/Credentials/API-Keys niemals an LLMs.
- externe LLMs erhalten standardmäßig nur minimierte/redigierte oder explizit freigegebene Inhalte.
- interne LLM-Endpunkte können bevorzugt werden, wenn der konkrete Endpoint für die Datenklasse freigegeben ist.
- Modellname allein entscheidet nicht über Zulässigkeit; Endpoint-/Deployment-/Retention-/Training-/Logging-Eigenschaften sind maßgeblich.
- AI-Ausgabe bleibt Proposal/Extraction bis Human Review.

## 8. Beziehung zu bestehenden Epics

- #32/#35: Organisations-, Rechtsraum- und Regulatorik-Kontext
- #37: Conversational Intake
- #39: Guided Evidence Plan
- #40: LLM Claim Proposals
- #41: Artifact-Ingestion-Layer
- #42: Adapter-Priorisierung
- #43: AI-Execution/Data-Routing
- #44: ADOIT + natürliche Sprache Reference Showcase

## 9. Nächste fachliche Validierung

Nach Abschluss von NEXT-118 sollte ein kleiner Referenzpilot definiert werden, der mindestens drei Inputs kombiniert:

1. natürliche Beschreibung/Interview,
2. ADOIT-/ArchiMate- oder vergleichbares EA-Artefakt,
3. ein ergänzendes technisches oder tabellarisches Artefakt (z. B. Kubernetes YAML, Cloud-Export oder Excel-Inventar).

Erfolg ist nicht maximale Automatisierung, sondern nachvollziehbare **Informationswiederverwendung** mit klarer Provenienz, Datenschutzgrenze und Human Review.
