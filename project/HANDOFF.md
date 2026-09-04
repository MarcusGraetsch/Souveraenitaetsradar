# Project Handoff

## Kurzfassung

Der Souveränitäts-Radar besteht aus einem cloud-agnostischen Methodenkern und einer lokal installierbaren Consultant-Webanwendung. Excel v1.0 bleibt Methodenreferenz, nicht operative UI. Die produktive Arbeitskette lautet aktuell:

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
  -> optional LLM Bridge
  -> Human-reviewed Claims
  -> Gate Requirements prüfen/überschreiben
  -> Hard Gates PASS / FAIL / UNVERIFIED / N/A
  -> Ergebnis
  -> Structured Export / Consultant Report / Backup / Restore
```

NEXT-112, NEXT-114 und NEXT-115 sind auf `main`. NEXT-113 / Issue #23 befindet sich in PR #24 im finalen Review.

## Verbindliche Methodenregeln

- Security Capability, Sovereignty Capability, Workload Sovereignty Risk und Evidence Confidence bleiben getrennte Achsen.
- Gate first, score second.
- Provider/Service Capability ist nicht Applied Capability.
- Fehlende Evidence ist `UNVERIFIED`, kein erfundenes PASS oder FAIL.
- Human-reviewed/approved Claims sind die einzige Brücke von Evidence zur deterministischen Gate-Bewertung.
- Raw Evidence oder LLM-Proposals wirken niemals direkt auf Gates.
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

NEXT-115 Baseline komplexer KI-Agent:

- 128 total
- 124 relevant
- 83 applicable
- 41 needs_review
- 4 not_applicable
- 44 screening
- 41 clarification
- 39 deep_dive
- 4 excluded

Der Public-Content-Fall ist mit 84 relevanten Fragen kürzer, besitzt aber aufgrund der aktuellen Definition von `work = screening + clarification` fast dieselbe unmittelbare Queue. NEXT-116 / Issue #22 bleibt dafür als P1-UX-Follow-up offen.

## NEXT-113 – implementierter Stand

PR #24 enthält jetzt:

### Structured Export

- versioniertes Schema `sovradar.assessment-export` v1.0
- JSON-Schema `schemas/assessment-export.schema.json`
- Scope und Assessment-Metadaten
- Relevanzprofil
- Answers inkl. Review State und Evidence-Links
- Evidence-Metadaten und Evidence Reviews
- Applied State sowie Base/Scope/Freshness Trust
- Claims inkl. Review Status und Referenzen
- Gate-Requirement-Overrides
- deterministisch neu berechnete Gate Results
- LLM-Bridge-Importe als Auditspur
- Exportwarnungen

Standardexport enthält keine Raw-Evidence-Dateien und keine `content_excerpt`-Inhalte.

### Consultant Report

Der Markdown-Bericht enthält Scope, Evidenzlage, Hard-Gate-Ergebnisse, UNVERIFIED/Evidence Gaps, technische Mindestabweichungen, Governance-Hinweise und Provenienz. Raw Evidence und freigegebene Evidence-Auszüge werden nicht automatisch eingebettet. Der Bericht ist keine Rechtsfeststellung und keine automatische Risikoakzeptanz.

### Backup / Restore

- Structured Backup ist Default und enthält keine Raw Evidence.
- Full Backup mit Raw Evidence ist explizites Opt-in.
- Restore überschreibt kein bestehendes Assessment, sondern erzeugt ein neues.
- Evidence-IDs und Referenzen werden remapped.
- Hard Gates werden nach Restore neu berechnet.
- Source- und Restored-Gate-Zustand werden semantisch verglichen.
- Structured Restore meldet fehlende Raw Evidence transparent.
- Full Restore kann ausdrücklich eingebettete Raw Evidence wiederherstellen.
- LLM-Proposals bleiben nach Restore reine Vorschläge/Auditspur.

### UI

Im Ergebnis-Tab stehen Structured JSON, Consultant Report, Structured Backup, Full Backup mit Warnung sowie JSON-/ZIP-Restore zur Verfügung.

## NEXT-113 – validierte Fachchecks

Der installierte E2E-Runner `tools/validation/export_restore_validation.py` hat wiederholt erfolgreich geprüft:

- Default Export omits sensitive Evidence
- Consultant Report omits sensitive Evidence
- Default Backup has no Raw Evidence
- Full Backup requires explicit opt-in
- Structured Restore creates a new Assessment
- Structured Restore preserves Gate Semantics
- Structured Restore reports missing Raw Evidence
- Full Restore restores Raw Evidence
- Full Restore preserves Gate Semantics
- Source Gate States remain unchanged

Synthetischer Testzustand:

- HG-01 = PASS
- HG-03 = FAIL
- HG-04 = UNVERIFIED
- übrige Gates = N/A

## Lifecycle-Finding und Fix

Die Full-Restore-Validierung deckte unter Linux ein reales Berechtigungsproblem auf: Evidence-Dateien im Bind-Mount konnten dem Container-Root gehören und hostseitig eine vollständige Deinstallation verhindern.

`uninstall.sh` wurde deshalb gehärtet:

1. Runtime-Inhalte werden vor `docker compose down` innerhalb des API-Containers entfernt.
2. Der Mountpoint wird für die Host-Löschung wieder beschreibbar gemacht.
3. Nach der Löschung prüft das Script explizit, dass `.runtime` und `.env` nicht mehr existieren.
4. Ein erfolgreicher Nicht-Repository-Löschpfad endet explizit mit `exit 0`.

Der finale vollständige CI-Lauf nach dieser Korrektur ist das letzte technische Merge-Gate von NEXT-113.

## Security-Hardening-Finding – NEXT-117 / Issue #25

Der Backup-Import extrahiert keine fremden ZIP-Pfade auf das Dateisystem und begrenzt die komprimierte Uploadgröße. Einzelne ZIP-Member werden aktuell jedoch mit `archive.read(...)` gelesen, bevor für alle Member die unkomprimierte Größe geprüft ist.

Vor Nutzung nicht vertrauenswürdiger Backup-Dateien müssen daher ergänzt werden:

- Vorabprüfung von `ZipInfo.file_size`
- kleine Limits für `assessment.json` und `manifest.json`
- per-Evidence-Limit vor Dekompression
- Limit der gesamten unkomprimierten Archivgröße
- Limit der ZIP-Eintragsanzahl
- negative Tests für Oversize-/Decompression-Bomb-Fälle

Das ist als Issue #25 dokumentiert. Es ist kein bereits gelöster Schutz und keine Methodenanforderung.

## Agent-Regeln

- `AGENTS.md` zuerst lesen.
- Danach `project/PROJECT_STATE.yaml`, dieses Handoff und `project/NEXT_ACTIONS.yaml` lesen.
- Keine Kunden-Cloud-Credentials anfordern.
- Keine LLM API im MVP ohne neue Decision.
- Keine Provider-spezifische Logik in Gate-/Rule-Core.
- Raw Kundenevidence nie committen.
- LLM-Proposals niemals automatisch als reviewed Claim/Answer übernehmen.
- Fehlende Evidence niemals automatisch als FAIL interpretieren.
- `needs_review` niemals still ausblenden.
- Workflow Stage niemals als Ersatz für Applicability verwenden.
- substantielle Änderungen über Issue/Branch/PR/CI/Agent-Log dokumentieren.

## Unmittelbar nächste Schritte

1. Vollständigen CI-Lauf von PR #24 nach dem letzten Uninstall-Fix abwarten und prüfen.
2. PR #24 aktualisieren, Self-Review durchführen und aus Draft nehmen.
3. Bei grüner CI NEXT-113 mergen und Issue #23 schließen.
4. Danach Projektstatus/NEXT_ACTIONS auf `completed` aktualisieren.
5. Nächste Produktentscheidung zwischen NEXT-101 (realer Customer-Evidence-Pack-Pilot), NEXT-116 (UX-Reduktion) und NEXT-117 (Backup-Import-Hardening) anhand P0/P1 und Pilotbedarf treffen.
