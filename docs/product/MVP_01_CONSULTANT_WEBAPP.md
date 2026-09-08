# MVP-01 – Consultant Web Application

Status: **aktuell implementierte Runtime / pre-v0.4-Zielmethodik**  
Fachliches Zielmodell: `docs/method/METHOD_CORE_V0_4_DE.md`  
Aktuelles Development Gate: Issue #68 / NEXT-120

## Einordnung

Die Webanwendung ist die vorhandene, technisch validierte Consultant-Runtime. Sie implementiert wesentliche Ergebnisse der früheren MVP-/Evidence-/Gate-Operationalisierung (`INT-03`).

Sie ist **nicht identisch mit dem aktuellen fachlichen Decision-Support-Zielmodell v0.4**. Insbesondere fehlen in der Runtime noch der vollständige Variantenvergleich über `DecisionCase`/`ArchitectureOption`, Status-quo-/Business-Value-Sicht, die sieben sichtbaren Decision Dimensions und der stark verkleinerte adaptive Screening-Einstieg.

Diese Abweichung ist ein dokumentierter Implementation Gap und kein Methodenwiderspruch. Vor weiterer fachlicher Runtime-/Schema-/UI-Migration wird der vollständige BSI-C3A-Kriterienkatalog in NEXT-120 geprüft.

## Ziel der vorhandenen Runtime

Der Souveränitäts-Radar ist als lokal installierbare Webanwendung verfügbar. Die Excel-Datei bleibt Methoden-/Entwicklungsreferenz, ist aber nicht die primäre Bedienoberfläche.

Der **aktuell implementierte** Workflow lautet:

`Assessment -> Scope -> Relevanzprofil -> Guided Questions -> Evidence -> optional LLM Bridge -> Human-reviewed Claims -> Hard Gates -> Ergebnis`

Der fachliche Zielworkflow v0.4 ist im README und in `METHOD_CORE_V0_4_DE.md` beschrieben.

## MVP-Technologien

| Schicht | MVP-01 |
|---|---|
| Frontend | React + TypeScript + Vite |
| Backend | Python + FastAPI |
| Datenbank | PostgreSQL |
| Dokumente | lokales Filesystem `.runtime/` |
| Runtime-Methodik | `src/sovradar/` + `data/method/` + `config/` |
| KI | Copy/Paste **LLM Bridge**, keine API-Calls |
| Deployment | Docker Compose |
| Auth | noch keine; MVP lokal/Single-User |

Nicht Teil von MVP-01: LiteLLM, n8n, LangGraph, Keycloak, S3, Kubernetes/GitOps.

## Guided Workflow

Die 128 Fragen sind bereits in der Runtime als Methodenbank und nicht als statische Pflichtliste gedacht. Aus Assessment-Scope und Relevanzprofil entstehen drei Zustände: `applicable`, `not_applicable`, `needs_review`. Unklarheit darf eine Frage nie still ausblenden. Der Berater kann jederzeit zwischen relevanten und allen Fragen wechseln.

Die aktuelle Runtime priorisiert aber noch deutlich mehr Fragen als der v0.4-Zielkorridor von etwa 15–25 sichtbaren Kernfragen. Die spätere Reduktion wird erst nach NEXT-120 und der Methodenvalidierung umgesetzt.

## Evidence Review

Evidence wird zunächst lokal erfasst und ist noch kein automatisch vertrauenswürdiger Nachweis. Der Berater bewertet je Evidence:

- Applied State: `asserted`, `available`, `documented`, `observed`, `configured`, `tested`, `attested`
- Base Trust 0–5
- Scope Fit 0–5
- Freshness Fit 0–5
- Review Status: `raw`, `normalized`, `reviewed`, `approved`, `rejected`

Der effektive Trust ist intern definiert als Minimum aus Base Trust, Scope Fit und Freshness Fit. Evidence ohne Review bleibt `raw` mit Trust 0 und kann kein Hard Gate verifizieren.

Diese Trust-/Applied-State-Logik ist interne Runtime-Operationalisierung und keine externe BSI-/EU-/C3A-Skala.

## Human-reviewed Claims

Ein Claim ist eine vom Berater verantwortete Aussage, die Evidence mit einem Hard Gate verbindet. Claims können einen reinen Fakt dokumentieren oder zusätzlich ein Applied-Capability-Level 0–4 tragen.

Nur `reviewed` oder `approved` Claims beeinflussen Hard Gates. LLM-Vorschläge werden **nicht automatisch** in Claims umgewandelt und erhalten keinen Gate-Einfluss ohne Human Review.

Die aktuelle interne Aggregation ist konservativ:

- schwächste bestätigte Capability begrenzt das Gate
- jeder Capability-Claim benötigt reviewed/approved Evidence
- stärkster passender Nachweis kann einen einzelnen Claim stützen
- schwächster belegter Capability-Claim begrenzt den Gate-Trust
- fehlende Claims/Evidence bleiben `UNVERIFIED`

Diese Logik ist interne Operationalisierung (`INT-03`), keine externe Normformel. Ob C3A spätere Anpassungen an Capability-/Evidence-Modellen nahelegt, wird in NEXT-120 geprüft.

## Hard Gates

Die Webanwendung zeigt derzeit acht nicht kompensierbare Mindestanforderungen:

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

Die acht Gates sind interne Methodik. NEXT-120 prüft ausdrücklich, ob C3A eine fachliche Anpassung, Ergänzung oder bessere Abgrenzung nahelegt.

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

## Nächste fachliche Nutzung der Runtime

Die manuelle Consultant-Evaluation `NEXT-118` bleibt vorgesehen, ist aber derzeit **durch NEXT-120 / C3A-Volltextreview blockiert**. Nach dem C3A-Review soll die bestehende Runtime gezielt darauf geprüft werden, welche UI-/Workflow-Teile gegenüber v0.4 erhalten, vereinfacht oder ersetzt werden müssen.
