# Souveränitätsradar

Der **Souveränitätsradar** ist ein Beratungs- und Softwareprojekt zur nachvollziehbaren Bewertung digitaler Souveränitätsrisiken von Cloud-, Plattform-, SaaS- und KI-Lösungen.

Das Projekt verbindet Informationssicherheits-Risikoanalyse, digitale Souveränität, Compliance/Governance und Evidence-Bewertung. Der Methodenkern ist **cloud-agnostisch** und benötigt **keinen direkten Zugang zu Kunden-Cloud-Accounts**.

## MVP-01: Consultant Web Application

Die operative Produktentwicklung läuft als lokal installierbare Webanwendung. Die Excel-Datei bleibt Methoden-/Entwicklungsreferenz; für den täglichen Beratungsworkflow ist sie nicht mehr die primäre Oberfläche.

Aktueller MVP-Stack:

- React + TypeScript + Vite
- Python + FastAPI
- PostgreSQL
- lokaler Dokument-Speicher unter `.runtime/`
- vorhandener deterministischer Methodenkern unter `src/sovradar/`
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

Default: `http://localhost:8080`

> MVP-01 hat noch keine Authentisierung. Die Installation bindet deshalb standardmäßig nur an `127.0.0.1`. Netzwerkfreigabe nur in vertrauenswürdigen Testumgebungen verwenden.

### Unternehmensnetz / Enterprise CA

Der Installer prüft vor dem Docker-Build die TLS-Vertrauensketten für PyPI und die npm Registry und übernimmt den Host-CA-Bundle sicher als BuildKit-Secret. Wenn eine zusätzliche Unternehmens-CA nicht im System-Truststore liegt, kann sie als PEM explizit angegeben werden:

```bash
SOVRADAR_CA_CERT=/pfad/zur/enterprise-ca.pem ./install.sh
```

TLS-Verifikation wird nicht deaktiviert. Details: [`docs/operations/ENTERPRISE_CA.md`](docs/operations/ENTERPRISE_CA.md).

## Consultant Workflow

`Assessment anlegen -> Scope -> Relevanzprofil -> Guided Questions -> Evidence -> LLM Bridge -> Human Review -> Rule Engine / Ergebnis`

Ein Assessment startet mit Workload, Kritikalität, Schutzbedarf, Kontrollraum und regulatorischem Kontext. Danach pflegt der Berater ein kompaktes **Relevanzprofil** mit Scope-Fakten wie Datenverarbeitung, Verschlüsselung, KI-Nutzung, Exit-Relevanz, IAM oder Unterauftragnehmern.

Aus Assessment + Relevanzprofil erzeugt der Radar einen deterministischen Fragenpfad aus der kanonischen Question Bank. Applicability hat drei Zustände:

- `applicable`
- `not_applicable`
- `needs_review`

Unklare Bedingungen bleiben als `needs_review` sichtbar und werden niemals still ausgeblendet. Die Oberfläche bietet zusätzlich `Alle Fragen`, damit die Filterentscheidung jederzeit geprüft werden kann.

Im aktuellen MVP können Assessments angelegt, Relevanzprofile gepflegt, relevante Fragen beantwortet, Evidence-Metadaten/Dateien lokal erfasst und LLM-Analysepakete erzeugt werden.

Die **LLM Bridge** funktioniert bewusst ohne API:

1. Radar erzeugt einen strukturierten Prompt mit offenen relevanten/zu prüfenden Fragen.
2. Berater kopiert ihn in einen freigegebenen LLM-Chat seiner Wahl.
3. LLM liefert strukturiertes JSON zurück.
4. JSON wird in den Radar eingefügt.
5. Das Backend validiert Assessment-ID, Question IDs, Evidence IDs und Schema.
6. Ergebnisse bleiben **Vorschläge** und werden nicht automatisch als Beraterentscheidung übernommen.

Die Applicability-Entscheidung selbst wird nicht an das LLM delegiert.

Details: [`docs/product/MVP_01_CONSULTANT_WEBAPP.md`](docs/product/MVP_01_CONSULTANT_WEBAPP.md)

## Evidence- und Cloud-Prinzip

Der Standardprozess arbeitet mit **Customer-mediated Evidence**: Verträge, Architektur-/CMDB-/Dependency-Dokumentation, IaC/redigierte Konfigurationen, kundenseitige Provider-Exporte, Assurance-Nachweise, Screenshare-/Workshop-Beobachtungen und Testprotokolle. Öffentliche Provider-Dokumentation belegt primär Service Capability, nicht Kundenkonfiguration.

AWS, Azure, GCP, OpenStack, Kubernetes, europäische Sovereign-Cloud-Angebote und SaaS werden über dasselbe generische Domänen- und Regelmodell bewertet. Provider-Adapter sind reine Übersetzer und enthalten keine eigene Risikomethode.

## Was der Radar getrennt ausweist

1. Provider / Service Capability
2. Applied Capability
3. Workload Sovereignty Risk
4. klassisches Informationssicherheits- und Betriebsrisiko
5. Evidence Confidence

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
├── data/method/                     # kanonische maschinenlesbare Methodik
├── config/                          # Regeln und Evidence-Typen
├── schemas/                         # JSON Schemas
├── src/sovradar/                    # deterministischer Methodenkern
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
6. offene Issues/PRs

Raw Kundenevidence, Cloud-Credentials und Secrets gehören niemals in GitHub Issues, PRs oder dieses Repository.
