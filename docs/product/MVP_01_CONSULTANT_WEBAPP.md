# MVP-01 – Consultant Web Application

## Ziel

Der Souveränitäts-Radar wird als lokal installierbare Webanwendung entwickelt. Die Excel-Datei bleibt Methoden-/Entwicklungsreferenz, ist aber nicht die primäre Bedienoberfläche.

Der Beratungsworkflow lautet:

`Assessment -> Scope -> Relevanzprofil -> Guided Questions -> Evidence -> optional LLM Bridge -> Human-reviewed Claims -> Hard Gates -> Ergebnis`

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

## Guided Workflow

Die 128 Fragen sind eine Methodenbank, kein statischer Fragebogen. Aus Assessment-Scope und Relevanzprofil entstehen drei Zustände: `applicable`, `not_applicable`, `needs_review`. Unklarheit darf eine Frage nie still ausblenden. Der Berater kann jederzeit zwischen `Relevante Fragen` und `Alle Fragen` wechseln.

## Evidence Review

Evidence wird zunächst lokal erfasst und ist noch kein automatisch vertrauenswürdiger Nachweis. Der Berater bewertet je Evidence:

- Applied State: `asserted`, `available`, `documented`, `observed`, `configured`, `tested`, `attested`
- Base Trust 0–5
- Scope Fit 0–5
- Freshness Fit 0–5
- Review Status: `raw`, `normalized`, `reviewed`, `approved`, `rejected`

Der effektive Trust ist intern definiert als Minimum aus Base Trust, Scope Fit und Freshness Fit. Evidence ohne Review bleibt `raw` mit Trust 0 und kann kein Hard Gate verifizieren.

## Human-reviewed Claims

Ein Claim ist eine vom Berater verantwortete Aussage, die Evidence mit einem Hard Gate verbindet. Claims können einen reinen Fakt dokumentieren oder zusätzlich ein Applied-Capability-Level 0–4 tragen.

Nur `reviewed` oder `approved` Claims beeinflussen Hard Gates. LLM-Vorschläge werden **nicht automatisch** in Claims umgewandelt und erhalten keinen Gate-Einfluss ohne Human Review.

Die interne Aggregation ist konservativ:

- schwächste bestätigte Capability begrenzt das Gate
- jeder Capability-Claim benötigt reviewed/approved Evidence
- stärkster passender Nachweis kann einen einzelnen Claim stützen
- schwächster belegter Capability-Claim begrenzt den Gate-Trust
- fehlende Claims/Evidence bleiben `UNVERIFIED`

Diese Logik ist interne Operationalisierung (`INT-03`), keine externe Normformel.

## Hard Gates

Die Webanwendung zeigt acht nicht kompensierbare Mindestanforderungen:

1. HG-01 Jurisdiktion & Effective Control
2. HG-02 Datenresidenz & Verarbeitung
3. HG-03 Schlüsselhoheit
4. HG-04 Exit & Portabilität
5. HG-05 Operational Autonomy
6. HG-06 Identity & Trust Anchors
7. HG-07 Supply Chain Critical Dependencies
8. HG-08 Security Minimum

Zustände: `PASS`, `FAIL`, `UNVERIFIED`, `N/A`.

Die technische Gate-Logik und Evidence-Logik bleiben getrennt. Ein technisches Requirement kann trotz starker Evidence `FAIL` sein. Umgekehrt bleibt eine technisch plausibel erfüllte Anforderung ohne ausreichende Evidence `UNVERIFIED`.

## Gate Requirements

Für den MVP werden die vorhandenen R4-Templates über Kritikalität vorbelegt:

- low → Basis
- medium → Standard
- high → Elevated
- critical → Critical

Das ist **keine regulatorische Vorgabe**, sondern eine interne Startkonfiguration. Der Berater kann jedes Gate 0–4 überschreiben. Das System speichert dies als `consultant-override`.

## LLM Bridge

Die Anwendung erzeugt ein Prompt Package für einen freigegebenen LLM-Chat. Das zurückgegebene JSON wird validiert und als Vorschlag gespeichert. Die LLM Bridge entscheidet weder Applicability noch Claims, Gate Requirements oder Risikoakzeptanz.

## Lokale Persistenz

Laufzeitdaten befinden sich im PostgreSQL-Docker-Volume `sovradar_db_data`, in `.runtime/` und in `.env`. Diese Pfade werden nicht committed.

## Lifecycle

```bash
git clone https://github.com/MarcusGraetsch/Souveraenitaetsradar.git
cd Souveraenitaetsradar
./install.sh
./test.sh
```

Betrieb: `./start.sh`, `./stop.sh`.

Vollständige Datenlöschung: `./uninstall.sh`. Der Uninstaller verlangt explizit `DELETE` und entfernt Container, lokal gebaute Images, DB-Volume, `.runtime/` und `.env`. Das Git-Repository wird nur nach einer zweiten Bestätigung entfernt.

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

## Danach

Nach Abschluss von NEXT-112 soll zunächst ein vollständiger synthetischer Consultant-Durchlauf auf einer sauberen Installation erfolgen. Erst danach sollten Export/Report, Dokumentextraktion oder weitere Automatisierung ausgebaut werden. Ziel ist zu prüfen, ob ein Berater den Workflow ohne Kenntnis der internen Methoden-/Maschinenebene tatsächlich bedienen kann.
