# Souveränitätsradar

Der **Souveränitätsradar** ist ein Beratungs- und Softwareprojekt zur nachvollziehbaren **Entscheidungsunterstützung bei Fragen digitaler Souveränität**.

Im Mittelpunkt steht nicht die abstrakte Frage „Cloud oder On-Prem – was ist souveräner?“, sondern der vergleichende Entscheidungsfall:

> Welche Betriebs-/Architekturvariante ist für einen konkreten Workload unter den Zielen, Risiken, Fähigkeiten, Kosten und Mindestanforderungen der Organisation vorzuziehen – und wie belastbar ist diese Empfehlung belegt?

Der Radar soll eine begründete Empfehlung erzeugen können. Finale Entscheidung, Risikoakzeptanz und rechtliche Würdigung bleiben beim Kunden.

## Aktueller fachlicher Stand

Der aktuelle fachliche Zielstand ist **Methodenkern v0.4**:

- Decision Support statt Provider-/Länderranking
- Vergleich mehrerer `ArchitectureOption`s unter einem `DecisionCase`
- Status quo / Nichtstun als reale Option, soweit sinnvoll
- sieben verständliche Entscheidungsdimensionen plus separate Evidence Confidence
- adaptive Question Library statt 128-Fragen-Pflichtfragebogen
- Provider Intelligence für wiederverwendbare Provider-/Service-Nachweise
- Customer-mediated Evidence statt notwendiger Cloud-Credentials
- geopolitische Sorgen werden in prüfbare Szenarien übersetzt
- Frameworks werden nach ihrer Funktion genutzt, nicht als gestapelte Vollprüfungen

Primäre Referenz: [`docs/method/METHOD_CORE_V0_4_DE.md`](docs/method/METHOD_CORE_V0_4_DE.md).  
Terminologie: [`docs/method/GLOSSARY_DE.md`](docs/method/GLOSSARY_DE.md).

### Aktuelles Development Gate

Vor weiterer Methoden-, Schema-, Runtime- oder UI-Erweiterung wird der vollständige BSI-Kriterienkatalog **Criteria enabling Cloud Computing Autonomy (C3A)** gegen den v0.4-Kern geprüft: **Issue #68 / NEXT-120**.

Bis dieser Volltextreview abgeschlossen ist, gilt das vorhandene C3A-Mapping als Arbeitsstand und nicht als vollständige Ableitung.

## Framework-Rollen

Der Radar ist **anschlussfähig** an etablierte Methoden und Anforderungen, aber kein universelles Compliance-Audit.

- **Bitkom Cloud-Souveränität 2026:** Orientierung zu Handlungsfähigkeit, Chancen/Risiken, Skills, Interdependenzen und Exit
- **EU Cloud Sovereignty Framework + BSI C3A:** Provider-/Service-Souveränität und prüfbare Capabilities/Evidence
- **BSI 200-3 / IT-Grundschutz:** Scope, Zielobjekte, Gefährdungen, Risikobehandlung sowie Security-/Resilienz-Deep-Dive und Vollständigkeitscheck
- **Data Act:** Exit, Switching und Portabilität, soweit anwendbar
- **C5:** Security-/Assurance-Evidence
- **NIS2, DORA, DSGVO/EDPB, AI Act usw.:** aktivierbare Compliance-Overlays bzw. Methodenquellen bei tatsächlicher Anwendbarkeit

Details: [`docs/method/SOURCE_GUIDE.md`](docs/method/SOURCE_GUIDE.md).

## MVP-01: aktuelle Consultant-Webanwendung

Die operative Produktentwicklung läuft als lokal installierbare Webanwendung. Die Excel-Datei bleibt Methoden-/Entwicklungsreferenz; für den täglichen Beratungsworkflow ist sie nicht die primäre Oberfläche.

**Wichtig:** Die aktuelle Runtime implementiert noch wesentliche Teile des früheren Einzel-Assessment-/Guided-Question-Workflows. Sie ist technisch funktionsfähig und auditierbar, aber noch **nicht vollständig auf den Decision-Support-Kern v0.4 migriert**. Diese Abweichung ist als Implementation Gap dokumentiert und wird erst nach dem C3A-Volltextreview und der Methodenvalidierung aufgelöst.

Aktueller MVP-Stack:

- React + TypeScript + Vite
- Python + FastAPI
- PostgreSQL
- lokaler Dokument-Speicher unter `.runtime/`
- deterministischer Methodenkern unter `src/sovradar/`
- **LLM Bridge per Copy/Paste**, keine LLM-API-Calls
- Docker Compose

Noch **nicht** Teil des MVP: LiteLLM, n8n, LangGraph, Keycloak, S3, Kubernetes/GitOps.

### Schnellstart

```bash
git clone https://github.com/MarcusGraetsch/Souveraenitaetsradar.git
cd Souveraenitaetsradar
./install.sh
```

Danach:

```bash
./start.sh       # starten
./stop.sh        # stoppen, Daten behalten
./test.sh        # Health-/Runtime-Test
./uninstall.sh   # Anwendung + alle erzeugten Daten löschen
```

`./install.sh` kann für Reparatur oder Konfigurationsänderungen erneut ausgeführt werden und verwendet dabei das bestehende lokale Datenbankpasswort weiter. Existiert das Compose-Datenbank-Volume ohne die zugehörige `.env`, bricht die Installation zum Schutz vorhandener Daten mit einer konkreten Wiederherstellungs-/Löschanweisung ab, statt die API mit unpassenden Zugangsdaten in eine Neustartschleife zu schicken. `./test.sh` beendet sich bei einem abgestürzten oder neu startenden API-Container frühzeitig und gibt Status sowie die letzten API-Logzeilen aus.

Default: `http://localhost:8080`

> MVP-01 hat noch keine Authentisierung. Die Installation bindet deshalb standardmäßig nur an `127.0.0.1`. Netzwerkfreigabe nur in vertrauenswürdigen Testumgebungen verwenden.

### Unternehmensnetz / Enterprise CA

Der Installer prüft vor dem Docker-Build die TLS-Vertrauensketten für PyPI und die npm Registry und übernimmt den Host-CA-Bundle sicher als BuildKit-Secret. Wenn eine zusätzliche Unternehmens-CA nicht im System-Truststore liegt, kann sie als PEM explizit angegeben werden:

```bash
SOVRADAR_CA_CERT=/pfad/zur/enterprise-ca.pem ./install.sh
```

TLS-Verifikation wird nicht deaktiviert. Details: [`docs/operations/ENTERPRISE_CA.md`](docs/operations/ENTERPRISE_CA.md).

## Zielworkflow der Beratung

```text
Entscheidungsfrage / Workload
  -> gemeinsame Anforderungen, Ziele und K.O.-Kriterien
  -> realistische Varianten inkl. Status quo
  -> vorhandene Kundenartefakte vorbefüllen
  -> kompaktes Screening
  -> nur entscheidungsrelevante Deep Dives
  -> Provider Intelligence + Customer Evidence + Tests
  -> geprüfte Claims / Risikoszenarien / Maßnahmen
  -> Variantenvergleich
  -> Entscheidungsvorlage / Empfehlung
  -> Kundenentscheidung
```

Der Zielkorridor für das sichtbare Kernscreening liegt methodisch derzeit bei etwa **15–25 Fragen**. Das ist eine zu validierende interne Designhypothese, keine Normvorgabe.

## Aktueller Runtime-Workflow

Die bestehende Webapp arbeitet derzeit noch mit:

`Assessment -> Scope -> Relevanzprofil -> Guided Questions -> Evidence -> LLM Bridge -> Human Review -> Rule Engine / Ergebnis`

Applicability hat drei Zustände:

- `applicable`
- `not_applicable`
- `needs_review`

Unklare Bedingungen bleiben als `needs_review` sichtbar und werden niemals still ausgeblendet. Die vollständige Question Bank bleibt über Audit-/Alle-Fragen-Sichten inspizierbar.

Die **LLM Bridge** funktioniert bewusst ohne API:

1. Radar erzeugt einen strukturierten Prompt.
2. Berater kopiert ihn in einen freigegebenen LLM-Chat seiner Wahl.
3. LLM liefert strukturiertes JSON zurück.
4. JSON wird in den Radar eingefügt und validiert.
5. Ergebnisse bleiben **Vorschläge** und werden nicht automatisch als Beraterentscheidung übernommen.

LLM-Proposals entscheiden weder Applicability noch Hard Gates und werden ohne Human Review nicht zu wirksamen Claims.

Details: [`docs/product/MVP_01_CONSULTANT_WEBAPP.md`](docs/product/MVP_01_CONSULTANT_WEBAPP.md).

## Evidence- und Cloud-Prinzip

Der Standardprozess arbeitet mit **Customer-mediated Evidence**: Verträge, Architektur-/CMDB-/Dependency-Dokumentation, IaC/redigierte Konfigurationen, kundenseitige Provider-Exporte, Assurance-Nachweise, Screenshare-/Workshop-Beobachtungen und Testprotokolle.

Öffentliche Provider-Dokumentation belegt primär **Provider-/Service Capability**, nicht automatisch die konkrete Kundenkonfiguration oder Wirksamkeit im Workload.

AWS, Azure, GCP, OpenStack, Kubernetes, europäische Sovereign-Cloud-Angebote, chinesische Provider, SaaS und On-Prem-Varianten werden über dasselbe generische Modell betrachtet. Provider-Adapter sind reine Übersetzer und enthalten keine eigene Risikomethode.

## Was getrennt sichtbar bleiben muss

- Provider / Service Capability
- Applied Capability
- Workload Sovereignty Risk
- Security / Operational Risk
- Business-/Strategic Value
- Evidence Confidence
- Hard-Gate-/K.O.-Status
- Kosten, Maßnahmen und Restrisiken

Die Methode arbeitet nach **Gate first, score second**. Fehlende Evidence führt zu `UNVERIFIED`, nicht automatisch zu `FAIL`.

## Repository-Struktur

```text
.
├── apps/api/                        # FastAPI Backend
├── apps/web/                        # React/Vite Consultant UI
├── docker-compose.yml
├── install.sh / start.sh / stop.sh / test.sh / uninstall.sh
├── AGENTS.md
├── project/                         # State, Roadmap, Handoff, Decisions, Agent Logs
├── docs/product/                    # Produkt-/UX-Dokumentation
├── docs/method/                     # fachliche Methodik
├── docs/architecture/               # Architektur + ADRs
├── docs/history/                    # historischer Projektverlauf, nicht aktuelle Source of Truth
├── data/method/                     # aktuell implementierte maschinenlesbare Methodik
├── config/                          # aktuell implementierte Regeln und Evidence-Typen
├── schemas/                         # JSON Schemas
├── src/sovradar/                    # deterministischer Runtime-Methodenkern
├── tests/                           # Core Tests
└── .github/                         # CI, Templates, CODEOWNERS
```

## Laufzeitdaten

Laufzeitdaten gehören **nicht** ins Git-Repository. Sie liegen lokal im PostgreSQL-Docker-Volume `sovradar_db_data`, unter `.runtime/` und in `.env`. Lokales Build-Trust-Material liegt ausschließlich unter `.build/`. `./uninstall.sh` entfernt diese Daten nach expliziter `DELETE`-Bestätigung vollständig.

## Einstieg für Menschen und Agenten

1. `AGENTS.md`
2. `project/PROJECT_STATE.yaml`
3. `project/HANDOFF.md`
4. `project/NEXT_ACTIONS.yaml`
5. `project/DECISIONS.yaml`
6. `docs/method/METHOD_CORE_V0_4_DE.md`
7. `docs/method/GLOSSARY_DE.md`
8. offene Issues/PRs

Raw Kundenevidence, Cloud-Credentials und Secrets gehören niemals in GitHub Issues, PRs oder dieses Repository.
