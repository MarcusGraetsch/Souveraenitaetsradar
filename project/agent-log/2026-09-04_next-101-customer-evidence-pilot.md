# Agent Session – NEXT-101 Customer Evidence Pack Pilot

Datum: 2026-09-04
Rollen: evidence-analyst, methodologist, developer, reviewer
Issue: #2
PR: #27
Branch: `feature/next-101-customer-evidence-pilot`

## Ziel

Den cloud-agnostischen Souveränitäts-Radar erstmals mit einem providerneutralen Customer-mediated Evidence Pack reproduzierbar durchlaufen, ohne Cloud-Credentials und ohne direkte Provider-Account-Zugriffe.

## Implementiert

### Evidence Request Mapping

Evidence Records können explizit auf providerneutrale `ER-xxx` Evidence Requests aus `data/method/evidence_request_catalog.csv` verweisen. Dieses Mapping ist interne Methodenmetadaten und keine externe Norm- oder Rechtsfeststellung.

### Evidence-Coverage

`src/sovradar/evidence_coverage.py` unterscheidet vier Workflow-/Sufficiency-Zustände:

- `VERIFIED`
- `REVIEW_REQUIRED`
- `INSUFFICIENT`
- `MISSING`

Diese Zustände sind ausdrücklich **keine** Hard-Gate-PASS/FAIL-Entscheidungen. Evidence-Coverage erzeugt keine Human-reviewed Claims automatisch.

Applied-State-Sufficiency ist explizit modelliert. Insbesondere werden `observed` und `configured` nicht als austauschbar behandelt.

### Provider Capability vs. Applied Capability

Öffentliche Provider-Dokumentation bleibt mit `applied_state=available` ein Service-/Capability-Nachweis. Sie erfüllt eine assessment-spezifische Anforderung an `configured` Applied Capability nicht automatisch.

### Synthetisches Evidence Pack

Fünf Evidence-Klassen:

- contractual
- architecture
- provider_export
- test_report
- public_provider

Assessment-spezifische Baseline für elf erforderliche Evidence Requests:

- 3 VERIFIED
- 4 REVIEW_REQUIRED
- 1 INSUFFICIENT
- 3 MISSING
- keine Scope-Mismatches

Die Baseline enthält bewusst offene und unzureichende Nachweise, damit der Pilot keine künstlich vollständige Evidenzlage simuliert.

### Live-Webapp-Pilot

`tools/validation/customer_evidence_pack_webapp.py` verarbeitet das synthetische Pack gegen eine laufende Installation:

1. Assessment und Relevanzprofil anlegen.
2. Evidence Records in die Anwendung aufnehmen.
3. Applied State, Trust und Review Status übernehmen.
4. assessment-spezifische interne Gate Requirements setzen.
5. ausschließlich den im Pilotplan explizit vorgesehenen Human-reviewed Claim anlegen.
6. Hard Gates deterministisch berechnen.
7. Structured Export und Consultant Report prüfen.

Validierter Gate-Zustand:

- HG-01 PASS
- HG-02 UNVERIFIED
- HG-03 UNVERIFIED
- HG-04 UNVERIFIED
- HG-05 UNVERIFIED
- HG-06 UNVERIFIED
- HG-07 UNVERIFIED
- HG-08 UNVERIFIED

Damit wird bestätigt, dass fehlende reviewed Claims nicht aus vorhandener Evidence erfunden werden.

## Validierung

GitHub Actions Run `33837372041` vollständig grün:

- Python PASS
- Core Tests PASS
- API Tests PASS
- Offline NEXT-101 Evidence-Coverage-Pilot PASS
- Frontend PASS
- Compose Smoke PASS
- NEXT-114 Regression PASS
- NEXT-115 Regression PASS
- NEXT-113 Export/Restore Regression PASS
- NEXT-101 Live-Webapp-Pilot PASS
- Stop/Restart/Test PASS
- vollständiger Uninstall PASS

Artifact: `9923731562` (`consultant-validation-reports`).

## Governance / Grenzen

- Keine Cloud-Credentials benötigt oder angefordert.
- Keine Provider-spezifische Risikologik im Kern.
- Kein automatisches Erzeugen reviewed Claims aus Evidence oder Coverage.
- Fehlende Evidence bleibt Gap/UNVERIFIED.
- Provider Capability bleibt von Applied Capability getrennt.
- Assessment-spezifische Thresholds und Gate Requirements im Pilot sind interne Operationalisierung, keine externen Normvorgaben.
- Keine echten Kundendaten oder Secrets im Repository.

## Offene Security-Findings

- Issue #25 / NEXT-117: ZIP-Decompression-Bomb-Hardening vor untrusted Backup-Imports.
- Issue #26: vollständige serverseitige JSON-Schema-Validierung vor untrusted Structured Restore.

Beide Findings blockieren den lokalen synthetischen Ersttest nicht, müssen jedoch vor der Annahme nicht vertrauenswürdiger Importdateien geschlossen werden.

## Übergang zum manuellen Test

NEXT-118 / Issue #28 ist der nächste P0-Schritt. Das Runbook `docs/validation/FIRST_INSTALL_EVALUATION.md` führt durch die erste Installation und eine manuelle Consultant-Evaluation. Ziel ist jetzt ausdrücklich die menschliche Prüfung von Bedienbarkeit und fachlicher Plausibilität, nicht eine weitere rein automatisierte Validierung.
