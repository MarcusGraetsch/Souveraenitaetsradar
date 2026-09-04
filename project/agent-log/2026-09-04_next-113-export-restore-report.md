# Agent Session – NEXT-113 Assessment Export, Backup/Restore und Consultant Report

Datum: 2026-09-04
Rollen: developer, reviewer, evidence-analyst
Issue: #23
PR: #24
Branch: `feature/next-113-backup-export-report`

## Ausgangslage

Nach NEXT-112, NEXT-114 und NEXT-115 konnte der Souveränitäts-Radar Assessments lokal durchführen und Hard Gates deterministisch bewerten. Es fehlte jedoch ein reproduzierbarer Weg, einen Assessment-Zustand zu sichern, weiterzugeben, wiederherzustellen und als Consultant Report auszugeben.

## Ziel

Drei unterschiedliche Artefakte mit unterschiedlichen Schutzbedarfen werden getrennt behandelt:

1. Structured Assessment Export für Nachvollziehbarkeit, Audit und Restore.
2. Consultant Report für Beratung/Management ohne automatische Einbettung von Raw Evidence.
3. Full Backup mit Raw Evidence ausschließlich nach explizitem Opt-in.

## Implementiert

### Structured Export

- Schema `sovradar.assessment-export` v1.0.
- JSON-Schema unter `schemas/assessment-export.schema.json`.
- Enthält Scope, Relevanzprofil, Answers, Evidence-Metadaten und Reviews, Claims, Gate-Requirement-Overrides, deterministisch berechnete Gate Results sowie LLM-Bridge-Auditspur.
- Standardexport enthält weder Raw-Evidence-Dateien noch Evidence-Textauszüge.

### Consultant Report

- Markdown-Bericht für Berater-/Managementnutzung.
- Trennt Scope, Evidence-Lage, Hard Gates, UNVERIFIED/Evidence Gaps, FAIL-Abweichungen, Governance-Hinweise und Provenienz.
- Keine Raw Evidence und keine freigegebenen Evidence-Textauszüge.
- Keine automatische Risikoakzeptanz oder Rechtsfeststellung.

### Backup und Restore

- Structured ZIP Backup ohne Raw Evidence als Default.
- Full Backup mit Raw Evidence nur über explizites `include_evidence=true`.
- Restore erzeugt immer ein neues Assessment.
- Evidence-IDs und verknüpfte Referenzen werden neu gemappt.
- Gate-Requirement-Overrides werden wiederhergestellt.
- LLM-Importe bleiben Auditspur/Vorschläge.
- Hard Gates werden nach Restore neu berechnet und semantisch gegen den Exportzustand verglichen.
- Fehlende Raw Evidence wird bei Structured Restore ausdrücklich ausgewiesen.

### Consultant UI

Im Ergebnisbereich stehen zur Verfügung:

- Structured JSON Download
- Consultant Report Download
- strukturiertes Backup
- Vollbackup inkl. Evidence mit expliziter Warnung/Bestätigung
- Restore von JSON oder ZIP als neues Assessment
- sichtbarer Hinweis bei Gate-Semantik-Drift

### API-Struktur

Der Export-Router wird explizit in `main.py` registriert. Die frühere indirekte Registrierung über Import-Side-Effects im LLM-Bridge-Modul wurde entfernt.

## Validierung

Finaler Merge-Gate-Lauf:

- GitHub Actions Run: `33834276156`
- Artifact: `9922749183` (`consultant-validation-reports`)
- Python: PASS
- Frontend: PASS
- Compose Smoke: PASS
- Consultant Walkthrough: PASS
- Install / Stop / Restart / Test / vollständiger Uninstall: PASS

Der installierte NEXT-113-End-to-End-Runner bestätigte:

- Standardexport enthält keine sensitiven Evidence-Inhalte.
- Consultant Report enthält keine sensitiven Evidence-Inhalte.
- Standardbackup enthält keine Raw Evidence.
- Full Backup erfordert explizites Opt-in.
- Structured Restore erzeugt ein neues Assessment.
- Structured Restore erhält Gate-Semantik.
- fehlende Raw Evidence wird sichtbar gemeldet.
- Full Restore stellt Raw Evidence wieder her.
- Full Restore erhält Gate-Semantik.
- Export/Report/Backup verändern den Source-Gate-Zustand nicht.

Validierter synthetischer Gate-Zustand:

- HG-01 PASS
- HG-03 FAIL
- HG-04 UNVERIFIED
- übrige Gates N/A

NEXT-114 und NEXT-115 liefen im selben Merge-Gate als Regression ebenfalls erfolgreich.

## Lifecycle-Finding und Abschluss

Die Full-Restore-Validierung deckte unter Linux ein reales Berechtigungsproblem auf: Evidence-Dateien im Bind-Mount konnten dem Container-Root gehören und hostseitig eine vollständige Deinstallation verhindern. Nach der containerseitigen Runtime-Bereinigung blieb zunächst ein zweites Problem sichtbar: `docker compose run` konsumierte die restliche stdin des interaktiven Uninstall-Dialogs, wodurch der abschließende `read` mit EOF und Exit 1 endete.

Der finale Fix:

- Runtime-Inhalte werden containerseitig gelöscht.
- `docker compose run -T ... </dev/null` ist von der Dialog-stdin isoliert.
- `.runtime` und `.env` werden nach der Deinstallation explizit auf Abwesenheit geprüft.
- der optionale Repository-Dialog toleriert EOF.
- erfolgreicher Uninstall endet explizit mit Exit 0.

Run `33834276156` bestätigt den vollständigen Lifecycle.

## Governance-Entscheidungen

- DEC-027: Structured Export, Consultant Report und Raw-Evidence-Backup bleiben getrennt.
- DEC-028: Restore erzeugt ein neues Assessment und Gates werden neu berechnet.
- DEC-029: Consultant Reports minimieren Evidence-Inhalte.
- DEC-030: LLM-Bridge-Importe bleiben beim Export/Restore Auditspur.

## Security Review / offener Hardening-Punkt

Der Backup-Import nutzt `zipfile` ohne Dateisystem-Extraktion und vermeidet damit klassische Zip-Slip-Extraktion. Die aktuelle Uploadgröße ist begrenzt. Vor einem Einsatz außerhalb des lokalen MVP muss zusätzlich die **unkomprimierte Größe jedes ZIP-Members vor `archive.read()`** geprüft werden, um komprimierte Decompression-Bombs frühzeitig abzulehnen. Das ist als NEXT-117 / Issue #25 erfasst und wird nicht als bereits gelöst dargestellt.

## Reviewstatus

Alle definierten NEXT-113-Merge-Gates sind technisch erfüllt. PR #24 kann nach Self-Review aus Draft genommen und gemerged werden. Das Security-Hardening aus Issue #25 bleibt ein eigenständiges P1-Follow-up und blockiert den lokalen MVP-Nachweis nicht.
