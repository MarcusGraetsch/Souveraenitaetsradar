# Project Handoff

## Kurzfassung

Der Souveränitäts-Radar besteht aus einem cloud-agnostischen Methodenkern und einer lokal installierbaren Consultant-Webanwendung. Excel v1.0 bleibt Methodenreferenz, nicht operative UI. Die aktuelle Arbeitskette lautet:

```text
Assessment
  -> Scope / Kritikalität / CIA
  -> Relevanzprofil
  -> Progressive Questions
       -> Screening
       -> Klärung nötig
       -> Deep Dive
       -> Erledigt
       -> Alle Fragen / Audit
  -> Evidence erfassen
  -> Evidence Review / Trust
  -> Evidence-Request-Coverage prüfen
  -> optional LLM Bridge
  -> Human-reviewed Claims
  -> Gate Requirements prüfen/überschreiben
  -> Hard Gates PASS / FAIL / UNVERIFIED / N/A
  -> Ergebnis
  -> Structured Export / Consultant Report / Backup / Restore
```

NEXT-101, NEXT-112, NEXT-113, NEXT-114 und NEXT-115 sind technisch abgeschlossen bzw. für den Merge von PR #27 validiert. Der nächste P0-Schritt ist **NEXT-118 / Issue #28: erste manuelle Consultant-Installation und Evaluation**.

## Verbindliche Methodenregeln

- Security Capability, Sovereignty Capability, Workload Sovereignty Risk und Evidence Confidence bleiben getrennte Achsen.
- Gate first, score second.
- Provider/Service Capability ist nicht Applied Capability.
- Fehlende Evidence ist `UNVERIFIED`, kein erfundenes PASS oder FAIL.
- Human-reviewed/approved Claims sind die einzige Brücke von Evidence zur deterministischen Gate-Bewertung.
- Raw Evidence oder LLM-Proposals wirken niemals direkt auf Gates.
- Evidence-Request-Coverage ist ein Workflow-/Sufficiency-Zustand und **kein Hard-Gate-Ergebnis**.
- Gate-Requirement-Defaults sind interne Startkonfigurationen und keine Normvorgaben.
- Radar Capability Level 0–4 ist interne Operationalisierung und kein offizieller EU-SEAL.
- Customer-mediated Evidence ist Standard; Kunden-Cloud-Credentials sind keine Voraussetzung.

## Guided Workflow

Applicability und Workflow Stage bleiben getrennt.

Applicability:

- `applicable`
- `needs_review`
- `not_applicable`

Workflow Stage:

- `screening`
- `clarification`
- `deep_dive`
- `completed`
- `excluded`

`needs_review` darf niemals still verschwinden. Alle 128 Methodenfragen bleiben über die All-Questions-/Audit-Ansicht inspizierbar. Ein LLM entscheidet weder Applicability noch Workflow Stage.

NEXT-115 Baseline komplexer KI-Agent: 128 total, 124 relevant, 83 applicable, 41 needs_review, 4 not_applicable; Workflow 44 screening, 41 clarification, 39 deep_dive, 4 excluded. Der Public-Content-Fall ist mit 84 relevanten Fragen kürzer, besitzt aber wegen `work = screening + clarification` fast dieselbe unmittelbare Queue. NEXT-116 / Issue #22 bleibt dafür als P1-UX-Follow-up offen.

## NEXT-101 – Customer Evidence Pack Pilot

PR #27 implementiert den ersten providerneutralen Customer-mediated-Evidence-Pilot ohne Cloud-Credentials.

### Evidence Pack

Das synthetische Pack enthält fünf Evidence-Klassen:

- contractual
- architecture
- provider_export
- test_report
- public_provider

Evidence Records besitzen jetzt explizite `request_ids`, die auf `data/method/evidence_request_catalog.csv` verweisen. Das Mapping ist interne Methodenmetadaten und keine Normfeststellung.

### Evidence-Coverage

`src/sovradar/evidence_coverage.py` bewertet assessment-spezifische Evidence Requests konservativ mit vier Zuständen:

- `VERIFIED`: Scope, Trust und Applied State passen und Evidence ist reviewed/approved.
- `REVIEW_REQUIRED`: Evidence passt technisch, Human Review fehlt noch.
- `INSUFFICIENT`: gemappte Evidence verfehlt Scope, Trust oder Applied-State-Anforderung.
- `MISSING`: keine Evidence ist dem Request zugeordnet.

Die Applied-State-Beziehung ist bewusst nicht als simple numerische Rangfolge implementiert. `observed` und `configured` sind beispielsweise nicht austauschbar.

Baseline des synthetischen High-Criticality-Falls:

- 11 erforderliche Evidence Requests
- 3 VERIFIED
- 4 REVIEW_REQUIRED
- 1 INSUFFICIENT
- 3 MISSING
- 5 Evidence-Klassen
- keine Scope-Mismatches

Öffentliche Provider-Dokumentation mit `applied_state=available` erfüllt eine Anforderung an `configured` Applied Capability ausdrücklich nicht.

### Live-Webapp-Pilot

`tools/validation/customer_evidence_pack_webapp.py` führt das Pack durch die laufende Webanwendung:

1. Assessment und Relevanzprofil anlegen.
2. fünf Evidence Records aufnehmen.
3. Applied State, Trust und Review Status übernehmen.
4. explizite interne Gate Requirements setzen.
5. ausschließlich den im Pilotplan ausdrücklich vorgegebenen Human-Reviewed Claim anlegen.
6. Hard Gates berechnen.
7. Structured Export und Consultant Report prüfen.

Erwarteter und validierter Zustand:

- HG-01 = PASS
- HG-02 bis HG-08 = UNVERIFIED

Das ist absichtlich konservativ. Der Runner erzeugt **keine Claims automatisch aus Evidence-Coverage**. Nur der explizite synthetische Consultant-Claim darf Gate-Wirkung entfalten.

### CI

GitHub Actions Run `33837372041`, Artifact `9923731562`:

- Python PASS
- Core Tests PASS
- API Tests PASS
- Offline NEXT-101 Coverage Pilot PASS
- Frontend PASS
- Compose Smoke PASS
- NEXT-114 Regression PASS
- NEXT-115 Regression PASS
- NEXT-113 Export/Restore Regression PASS
- NEXT-101 Live-Webapp-Pilot PASS
- Stop/Restart/Test PASS
- vollständiger Uninstall PASS

## NEXT-113 – Export / Report / Backup / Restore

- Structured Export ist versioniert und enthält standardmäßig keine Raw Evidence.
- Consultant Report minimiert Evidence-Inhalte.
- Full Backup mit Raw Evidence ist explizites Opt-in.
- Restore erzeugt ein neues Assessment, remappt Referenzen und berechnet Gates neu.
- semantischer Gate-Vergleich nach Restore ist vorhanden.

Merge-Gate Run: `33834276156`, Artifact `9922749183`.

## Offene Security-Hardening-Punkte

### Issue #25 / NEXT-117

Vor Nutzung nicht vertrauenswürdiger ZIP-Backups fehlen noch Vorablimits für:

- `ZipInfo.file_size`
- unkomprimierte Gesamtgröße
- per-Evidence-Größe
- Anzahl ZIP-Einträge

### Issue #26

Structured JSON und `assessment.json` aus Backup-ZIPs sollen vor untrusted Nutzung vollständig serverseitig gegen das versionierte Export-Schema validiert werden.

Diese Findings blockieren den lokalen Ersttest mit eigenen synthetischen Daten nicht, sind aber vor fremden/untrusted Importen zu schließen.

## NEXT-118 – erste manuelle Consultant-Evaluation

Runbook:

`docs/validation/FIRST_INSTALL_EVALUATION.md`

Ziel: Nicht erneut nur technische Automation testen, sondern die Anwendung als Berater selbst bedienen und bewerten.

Prüfschwerpunkte:

- Installation und lokaler Zugriff
- Scope-/Assessment-Verständlichkeit
- Guided Workflow und Fragenmenge
- Evidence Intake, Applied State und Trust
- Human-reviewed Claims
- Requirement/Capability/Evidence-Logik der Hard Gates
- Export, Consultant Report, Backup und Restore
- Trennung fachlicher Methodikprobleme von reinen UX-Problemen

Für Findings mindestens Stelle, Beobachtung, Erwartung, Schweregrad und Einordnung `Methodik` vs. `Produkt/UX` notieren.

## Agent-Regeln

- `AGENTS.md` zuerst lesen.
- Danach `project/PROJECT_STATE.yaml`, dieses Handoff und `project/NEXT_ACTIONS.yaml` lesen.
- Keine Kunden-Cloud-Credentials anfordern.
- Keine LLM API im MVP ohne neue Decision.
- Keine Provider-spezifische Logik in Gate-/Rule-Core.
- Raw Kundenevidence nie committen.
- LLM-Proposals niemals automatisch als reviewed Claim/Answer übernehmen.
- Evidence-Coverage niemals automatisch in reviewed Claims umwandeln.
- Fehlende Evidence niemals automatisch als FAIL interpretieren.
- `needs_review` niemals still ausblenden.
- Workflow Stage niemals als Ersatz für Applicability verwenden.
- substantielle Änderungen über Issue/Branch/PR/CI/Agent-Log dokumentieren.

## Unmittelbar nächste Schritte

1. PR #27 nach finalem Self-Review mergen; Issue #2 schließen.
2. Main-CI prüfen.
3. NEXT-118 / Issue #28 auf einem frischen Zielsystem durchführen.
4. Findings aus dem manuellen Test als konkrete Issues/Decisions erfassen.
5. Danach Priorität zwischen NEXT-116, Security-Hardening (#25/#26) und erstem realen Customer-mediated Pilot festlegen.
