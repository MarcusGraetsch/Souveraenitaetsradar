# MVP-01 – Consultant Web Application

## Ziel

Der Souveränitäts-Radar wird ab MVP-01 als lokal installierbare Webanwendung entwickelt. Die bestehende Excel-Datei bleibt Methoden-/Entwicklungsreferenz, ist aber nicht mehr die primäre Bedienoberfläche für Assessments.

Der Beratungsworkflow lautet:

`Assessment anlegen -> Scope -> Relevanzprofil -> Guided Questions -> Evidence -> LLM Bridge -> Human Review -> Rule Engine / Ergebnis`

## MVP-Technologien

| Schicht | MVP-01 |
|---|---|
| Frontend | React + TypeScript + Vite |
| Backend | Python + FastAPI |
| Datenbank | PostgreSQL |
| Dokumente | lokales Filesystem `.runtime/` |
| Methodenkern | `src/sovradar/` + `data/method/` |
| KI | Copy/Paste **LLM Bridge**, keine API-Calls |
| Deployment | Docker Compose |
| Auth | noch keine; MVP lokal/Single-User |

Nicht Teil von MVP-01: LiteLLM, n8n, LangGraph, Keycloak, S3, Kubernetes/GitOps.

## Guided Workflow / Question Applicability

Die 128 Fragen der Methodenbank sind **kein statischer Fragebogen**. Die Webanwendung erzeugt einen nachvollziehbaren Fragenpfad aus Assessment-Scope und einem separaten Relevanzprofil.

Das Relevanzprofil enthält Scope-Fakten wie:

- Service-Modell und Cloud-Bezug
- Datenverarbeitung und Persistenz
- Verschlüsselung und Schlüsselmodell
- KI- bzw. agentische KI-Nutzung
- Exit-/Portabilitätsrelevanz
- Backup/Restore
- Multi-Provider und Unterauftragnehmer
- IAM, Logging/Monitoring, C5/C3A

Applicability wird im Methodenkern deterministisch bewertet. Es gibt genau drei Zustände:

- `applicable` – die bekannten Bedingungen sind erfüllt
- `not_applicable` – die Bedingung ist nach dem aktuellen Scope sicher ausgeschlossen
- `needs_review` – Kontext fehlt oder die natürliche Anwendbarkeitsregel ist noch nicht ausreichend operationalisiert

`needs_review` bleibt im Standardfragenpfad sichtbar. **Unklarheit darf nie dazu führen, dass eine Frage still verschwindet.** Im UI kann der Berater zusätzlich jederzeit auf `Alle Fragen` umschalten und auch sicher nicht anwendbare Fragen samt Begründung sehen.

Die heutige Engine operationalisiert bewusst nur sichere, generische Bedingungen. Noch nicht modellierte Anwendbarkeitsausdrücke werden konservativ als `needs_review` behandelt statt durch heuristische KI oder Providerlogik entschieden.

## LLM Bridge

Die erste Produktversion validiert den Nutzen von KI-Unterstützung, ohne gleichzeitig API-Key-Management, Kosten, Provider-Routing oder zusätzliche Datenübertragungen einzuführen.

Die Anwendung erzeugt ein Prompt Package. Der Berater kopiert es in einen freigegebenen LLM-Chat und fügt das zurückgegebene JSON in den Radar ein. Das Backend validiert `assessment_id`, bekannte Question IDs, bekannte Evidence IDs und die JSON-Struktur. Der Import erzeugt **Vorschläge**, keine automatisch übernommenen Assessment-Antworten.

Ab Guided Workflow enthält der LLM-Prompt nur offene `applicable`- und `needs_review`-Fragen. Die Applicability-Entscheidung selbst wird **nicht** an das LLM delegiert.

## Lokale Persistenz

Laufzeitdaten befinden sich ausschließlich im PostgreSQL-Docker-Volume `sovradar_db_data`, in `.runtime/` und in `.env`. Diese Pfade dürfen nicht committed werden.

## Lifecycle

```bash
git clone https://github.com/MarcusGraetsch/Souveraenitaetsradar.git
cd Souveraenitaetsradar
./install.sh
./test.sh
```

Betrieb: `./start.sh`, `./stop.sh`.

Vollständige Datenlöschung: `./uninstall.sh`. Der Uninstaller verlangt explizit `DELETE` und entfernt anschließend Container, lokal gebaute Images, DB-Volume, `.runtime/` und `.env`. Das Git-Repository wird nur nach einer zweiten Bestätigung entfernt.

## Security Boundary MVP-01

- keine Kunden-Cloud-Credentials
- keine LLM-API-Keys
- keine automatischen Cloud-Scans
- keine Ausführung hochgeladener Dateien
- maximale Uploadgröße standardmäßig 50 MiB
- Dateien werden unter UUID-Namen abgelegt
- Dateiinhalte werden noch nicht automatisch geparst
- Netzwerk-Bind `127.0.0.1` ist Default
- `0.0.0.0` nur für vertrauenswürdige Testnetze, da Auth später kommt

## Nächste Produktstufe

Nach dem Guided Workflow sind die wichtigsten offenen Schritte:

- Evidence -> Claim -> Hard Gate Integration
- echte Gate-/Risikoansicht aus der Rule Engine
- Human-Review-Übernahme einzelner LLM-Vorschläge in Answers
- Assessment-/Evidence-Export und Backup
- vollständiger synthetischer Consultant-Durchlauf auf sauberer VM
- Dokumenttext-Extraktion
- produktive Authentisierung

Die Excel-Arbeitsmappe bleibt fachliche Referenz. Neue operative Funktionen werden primär im Repository und in der Webanwendung entwickelt.
