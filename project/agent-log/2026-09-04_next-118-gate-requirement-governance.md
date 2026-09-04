# NEXT-118 / Issue #51 – Gate-Requirement-Governance

Datum: 2026-09-04
Branch: `feature/next-118-gate-requirement-governance`
PR: #62
Rollen: developer, methodologist, reviewer/project-coordinator
Provenienz: evidence-observation + internal-method

## Anlass

Der reale Consultant-Test zeigte auf der bisherigen Gate-Seite ein direkt editierbares `Requirement 0–4` ohne ausreichende Erklärung der Stufen, ihrer internen Herkunft oder der Folgen eines Overrides. Eine Änderung konnte die deterministische PASS-/FAIL-Grenze beeinflussen, ohne dass eine fachliche Begründung oder Auditspur erzwungen wurde.

## Methodische Grenze

Die vorhandene Methodenbank `data/method/r4_hard_gates.csv` enthält bereits pro Gate die fachlichen Beschreibungen der Capability-Stufen 0–4 sowie die internen Basis-/Standard-/Elevated-/Critical-Defaults. Diese Implementierung erfindet keine neuen Stufenbedeutungen und verändert keine Gate-Formel.

Die Skala bleibt eine interne Radar-Operationalisierung und keine offizielle BSI-, EU- oder Gesetzesskala.

## Umsetzung

- `GateDefinition` stellt die bereits vorhandenen Capability-0..4-Beschreibungen maschinenlesbar bereit.
- Assessment-Gate-Requirements unterscheiden jetzt explizit Standardwert und Override.
- Ein manueller Override benötigt eine nicht-leere fachliche Begründung.
- Ein Wert identisch zum Kritikalitäts-Standard wird nicht als Override gespeichert.
- Rückkehr zum Standard erfolgt über einen eigenen Reset mit Begründung.
- Neue additive Tabelle `gate_requirement_changes` dokumentiert:
  - Gate-ID
  - Override/Reset
  - vorherige und neue Stufe
  - vorherige und neue Quelle
  - Begründung
  - Zeitpunkt
- Consultant-UI zeigt:
  - Standardwert und Herleitung
  - aktuellen Wert
  - alle fünf vorhandenen per-Gate-Stufenbeschreibungen
  - begründeten Override-Workflow
  - expliziten Reset
  - Änderungshistorie
- Structured Export, Backup und Consultant Report enthalten die Governance-Auditspur.
- Restore stellt die Auditspur mit neuen IDs wieder her. Die Historie selbst beeinflusst keine Gates; aktuelle Overrides und die deterministische Rule Engine bleiben maßgeblich.
- Export-Schema v1.0 bleibt rückwärtskompatibel, da `gate_requirement_changes` optional ist.

## Tests / Validierung

Gezielte Regressionen decken ab:

- fehlende Override-Begründung wird abgelehnt;
- Standardwert kann nicht als künstlicher Override gespeichert werden;
- begründeter Override erzeugt Audit und kann PASS→FAIL verändern;
- begründeter Reset erzeugt Audit und stellt den Standardwert wieder her;
- Methodenkatalog liefert die vorhandenen 0–4-Beschreibungen;
- Structured Export / Backup / Restore bewahren Auditspur und Gate-Semantik;
- Legacy-v1.0-Export ohne neue Auditfelder bleibt restorebar;
- Synthetic Consultant Walkthrough, NEXT-101 und NEXT-113 setzen nur tatsächliche Abweichungen und dokumentieren synthetische Gründe.

## Entscheidung

DEC-036 präzisiert DEC-024: Gate-Requirements bleiben fachlich anpassbar, aber nicht mehr als beiläufiger Schwellenwert-Edit. Jede Abweichung und jede Rückkehr zum Standard ist ein begründeter, auditierbarer Governance-Vorgang.

## Offen bis Merge

- vollständige CI auf dem finalen PR-Head;
- Self-Review des gesamten Diffs;
- bei grünem Head: PR ready, Merge, Main-Verifikation, Issue #51 schließen;
- danach erneuter manueller Blick auf die K.O.-Kriterien-Seite im NEXT-118-Test.