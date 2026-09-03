# Souveränitätsradar

Der **Souveränitätsradar** ist ein Beratungs- und Softwareprojekt zur nachvollziehbaren Bewertung digitaler Souveränitätsrisiken von Cloud-, Plattform-, SaaS- und KI-Lösungen.

Das Projekt verbindet klassische Informationssicherheits-Risikoanalyse mit digitalen Souveränitätsdimensionen, Compliance-/Governance-Anforderungen, Evidenzbewertung und einer später KI-gestützten Assessment-Engine.

## Aktuelle Leitentscheidung

Der Radar ist **cloud-agnostisch** und benötigt **keinen direkten Zugang zu Kunden-Cloud-Accounts**. Der Standardprozess arbeitet mit einem **Customer Evidence Pack**:

- Verträge, DPA, SLA, Exit-Regelungen
- Architektur- und Dependency-Dokumentation
- CMDB-/DataGerry-/DORA-RoI-artige Exporte
- IaC und redigierte Konfigurationsauszüge
- vom Kunden erzeugte Provider-Exporte
- Audit-/Assurance-Nachweise
- Screenshare-/Workshop-Beobachtungen
- Testprotokolle für Exit, Restore, Failover, Key Control und Autonomie
- öffentliche Provider-Dokumentation als Nachweis der **Service Capability**, nicht der Kundenkonfiguration

AWS, Azure, GCP, OpenStack, Kubernetes, europäische Sovereign-Cloud-Angebote oder SaaS werden über dasselbe generische Domänen- und Regelmodell bewertet. Provider-spezifische Adapter übersetzen nur Begriffe und Evidence in das generische Modell; sie enthalten **keine eigene Risikomethode**.

## Was der Radar getrennt ausweist

1. **Provider / Service Capability** – was ein Dienst grundsätzlich anbietet oder zusichert.
2. **Applied Capability** – was der Kunde tatsächlich ausgewählt, konfiguriert, dokumentiert, getestet oder auditiert hat.
3. **Workload Sovereignty Risk** – verbleibende souveränitätsbezogene Risiken des konkreten Geschäftsprozesses.
4. **klassisches Informationssicherheits- und Betriebsrisiko** – damit mehr Souveränität nicht automatisch als mehr Sicherheit gilt.
5. **Evidence Confidence** – Belastbarkeit und Scope der verwendeten Nachweise.

Die Methode arbeitet nach **Gate first, score second**: nicht kompensierbare Mindestanforderungen werden vor gewichteten Vergleichswerten geprüft.

## Aktueller Stand

- **Projektphase:** R6 – Customer-mediated Evidence Pilot
- **Methodenmodell:** v1.0
- **R1–R5:** konsolidiert
- **R6:** AWS-Collector-Idee als Standardpfad verworfen; cloud-agnostische Evidence-Architektur implementiert
- **nächster Meilenstein:** ein providerneutraler Evidence-Pack-Pilot mit synthetischen oder vom Kunden exportierten Nachweisen

### Einstieg

- [`AGENTS.md`](AGENTS.md) – kanonische Arbeitsregeln für alle KI-Agenten
- [`project/PROJECT_STATE.yaml`](project/PROJECT_STATE.yaml) – aktueller Zustand
- [`project/HANDOFF.md`](project/HANDOFF.md) – Übergabe an neuen Menschen/Agenten
- [`project/NEXT_ACTIONS.yaml`](project/NEXT_ACTIONS.yaml) – priorisiertes Backlog
- [`project/DECISIONS.yaml`](project/DECISIONS.yaml) – akzeptierte Entscheidungen
- [`docs/architecture/EVIDENCE_ACQUISITION_ARCHITECTURE.md`](docs/architecture/EVIDENCE_ACQUISITION_ARCHITECTURE.md)
- [`docs/project/MULTI_AGENT_PROJECT_MANAGEMENT.md`](docs/project/MULTI_AGENT_PROJECT_MANAGEMENT.md)
- [`data/method/`](data/method/) – maschinenlesbare Methodik
- [`artifacts/method/METHOD_WORKBOOK_MANIFEST.md`](artifacts/method/METHOD_WORKBOOK_MANIFEST.md) – Manifest des erzeugten Methoden-Workbooks; kanonische Daten liegen unter `data/method/`

## Repository-Struktur

```text
.
├── AGENTS.md
├── OPENAI.md / CLAUDE.md / GEMINI.md / CODEX.md
├── project/                         # State, Roadmap, Handoff, Decisions, Agent Logs
├── docs/
│   ├── method/                      # fachliche Methodik
│   ├── architecture/                # Architektur + ADRs
│   ├── project/                     # Projektmanagement, Review, DoD, Releases
│   └── history/                     # R1–R6 Historie inkl. verworfener Ansätze
├── data/
│   ├── method/                      # aktuelle maschinenlesbare Methodik
│   ├── templates/                   # providerneutrale Evidence-Pack-Templates
│   └── history/                     # historische Pilotdaten
├── config/                          # versionierte Regeln und Evidence-Typen
├── schemas/                         # JSON Schemas
├── src/sovradar/                    # deterministischer Methodenkern
├── tests/                           # Unit-/Schema-/Intake-Tests
├── tools/evidence-pack/             # lokaler, credential-freier Evidence-Pack-Workflow
├── artifacts/method/                # aktuelles Methoden-Workbook
└── .github/                         # CI, Templates, CODEOWNERS
```

## Sicherheits- und Beratungsprinzip

Das Projekt soll **nicht** voraussetzen, dass Kunden uns Root-, Owner- oder sonstige Cloud-Credentials geben. Falls ein Kunde freiwillig technische Exporte erzeugt, geschieht dies unter seiner Kontrolle. Unsere Software verarbeitet bereitgestellte Evidence lokal oder in einer explizit freigegebenen Projektumgebung.

Raw Kundenevidence gehört standardmäßig **nicht** in dieses Repository.

## Schnellstart für Agenten

1. `AGENTS.md` vollständig lesen.
2. `project/PROJECT_STATE.yaml`, `project/HANDOFF.md`, `project/NEXT_ACTIONS.yaml`, `project/DECISIONS.yaml` lesen.
3. Offene Issues/PRs prüfen.
4. Für substanzielle Arbeit einen Plan und eine Rolle nennen.
5. Änderungen auf Branch + PR durchführen, Tests/Provenienz aktualisieren.
6. Session-Log und Handoff/State nur bei tatsächlicher Zustandsänderung aktualisieren.

## Externe Quellen

Normen, regulatorische Dokumente und Provider-Inhalte werden nicht ungeprüft oder lizenzwidrig kopiert. Das Repository speichert Referenzen, Fundstellen, Ableitungen und eigene Arbeitsartefakte. Die Herkunft fachlicher Regeln ist über `data/method/source_register.csv` und die Provenienzfelder nachvollziehbar.
