# MVP-01 – Consultant Web Application

## Ziel

Der Souveränitäts-Radar wird ab MVP-01 als lokal installierbare Webanwendung entwickelt. Die bestehende Excel-Datei bleibt Methoden-/Entwicklungsreferenz, ist aber nicht mehr die primäre Bedienoberfläche für Assessments.

Der Beratungsworkflow lautet:

`Assessment anlegen -> Scope -> Fragen -> Evidence -> LLM Bridge -> Human Review -> Rule Engine / Ergebnis`

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

## LLM Bridge

Die erste Produktversion validiert den Nutzen von KI-Unterstützung, ohne gleichzeitig API-Key-Management, Kosten, Provider-Routing oder zusätzliche Datenübertragungen einzuführen.

Die Anwendung erzeugt ein Prompt Package. Der Berater kopiert es in einen freigegebenen LLM-Chat und fügt das zurückgegebene JSON in den Radar ein. Das Backend validiert `assessment_id`, bekannte Question IDs, bekannte Evidence IDs und die JSON-Struktur. Der Import erzeugt **Vorschläge**, keine automatisch übernommenen Assessment-Antworten.

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

## Noch nicht implementiert

- dynamische Question Applicability statt reinem Domänenfilter
- Evidence -> Claim -> Hard Gate Integration
- echte Gate-/Risikoansicht aus der Rule Engine
- Human-Review-Übernahme einzelner LLM-Vorschläge in Answers
- Assessment-/Evidence-Export und Backup
- Dokumenttext-Extraktion
- produktive Authentisierung

Diese Punkte werden nach einem installierbaren End-to-End-Smoke-Test priorisiert.
