# Project Handoff

## Kurzfassung

Der Souveränitätsradar hat einen cloud-agnostischen Methodenkern und eine lokal installierbare Consultant-Webanwendung. Excel v1.0 bleibt Methodenreferenz, nicht operative UI.

MVP-01A, Guided Workflow, Evidence Intake und das providerneutrale Hard-Gate-Mapping sind auf `main`. NEXT-112 ist implementiert und nach grüner CI bereit zum Merge: Evidence Review → Human-reviewed Claim → deterministische Hard-Gate-Bewertung ist jetzt durchgängig in Backend und UI vorhanden.

## Consultant-Workflow

```text
Assessment
  -> Scope / Kritikalität / CIA
  -> Relevanzprofil
  -> Guided Questions
  -> Evidence erfassen
  -> Evidence Review / Trust
  -> optional LLM Bridge
  -> Human-reviewed Claims
  -> Gate Requirements prüfen/überschreiben
  -> Hard Gates PASS / FAIL / UNVERIFIED / N/A
  -> Ergebnis
```

## NEXT-112 – verbindliche Regeln

- Roh-Evidence oder LLM-Proposals wirken niemals direkt auf Gates.
- Nur `reviewed`/`approved` Claims wirken.
- Capability-Claims nutzen das interne Radar-Level 0–4.
- Jeder Capability-Claim benötigt reviewed/approved Evidence für eine verifizierte Aussage.
- Mehrere Claims werden konservativ aggregiert: schwächste bestätigte Capability begrenzt das Gate.
- Pro Claim kann der stärkste passende Nachweis tragen; Gate-Trust wird durch den schwächsten belegten Capability-Claim begrenzt.
- Fehlende/unzureichende Evidence bleibt `UNVERIFIED`.
- Requirement 0 ergibt `N/A`.
- Technische Unterschreitung ergibt `FAIL`, auch bei starker Evidence.
- Die Aggregation ist interne Operationalisierung `INT-03`, keine externe Normformel.

## Gate Requirements

MVP-Default nach Kritikalität:

- low → Basis
- medium → Standard
- high → Elevated
- critical → Critical

Das ist eine interne Startkonfiguration. Jeder Gate-Wert ist 0–4 editierbar und wird als `consultant-override` gespeichert. Niemals als gesetzliche oder normative Vorgabe darstellen.

## Acht Hard Gates

HG-01 Jurisdiktion & Effective Control; HG-02 Datenresidenz & Verarbeitung; HG-03 Schlüsselhoheit; HG-04 Exit & Portabilität; HG-05 Operational Autonomy; HG-06 Identity & Trust Anchors; HG-07 Supply Chain Critical Dependencies; HG-08 Security Minimum.

Fachliche Source-of-Truth: `data/method/r4_hard_gates.csv` und `data/method/evidence_request_catalog.csv`.

## Produktstatus

Implementiert:

- React/Vite Consultant UI
- FastAPI + PostgreSQL
- lokaler Dokument-Speicher
- Install/Start/Stop/Test/Uninstall-Lifecycle
- Relevanzprofil + Guided Questions
- lokale Evidence-Erfassung
- Copy/Paste LLM Bridge
- Evidence Review mit Applied State und Trust-Dimensionen
- Claim CRUD mit Evidence-/Question-Links und Human Review
- Gate Requirement Defaults + Consultant Override
- acht Hard-Gate-Karten mit Reasons und Evidence Requests
- Ergebnisübersicht

PR #17 enthält die NEXT-112-Produktintegration. Eine vollständige CI auf dem Feature-Stand war grün für Core/API Tests, Frontend Build und Docker Compose Smoke. Nach finalem State-Commit CI nochmals prüfen und dann squash-mergen.

## Regeln für andere Agenten

- `AGENTS.md` zuerst lesen.
- Keine Kunden-Cloud-Credentials anfordern.
- Keine LLM API im MVP ohne neue Decision.
- Keine Provider-spezifische Logik in Gate-/Rule-Core.
- Raw Kundenevidence nie committen.
- LLM-Proposals niemals automatisch als reviewed Claim/Answer übernehmen.
- Fehlende Evidence niemals automatisch als FAIL interpretieren.
- Requirement-Defaults niemals als regulatorische Vorgabe darstellen.
- Unklare Applicability nie still ausblenden.
- `./uninstall.sh` muss alle erzeugten Runtime-Daten löschen können.
- substantielle Änderungen via Issue/Branch/PR/CI/Agent-Log.

## Nächster Schritt – NEXT-114 / Issue #18

**Kein weiterer Feature-Ausbau zuerst.** Einen vollständigen synthetischen Consultant-Durchlauf auf sauberer Installation durchführen:

1. Clone / Install / Test
2. synthetisches Assessment + Relevanzprofil
3. Guided Questions
4. synthetische Customer-mediated Evidence
5. Evidence Review
6. optional LLM Bridge
7. Human-reviewed Claims
8. Gate Requirements prüfen
9. alle acht Hard Gates bewerten
10. gezielt mindestens PASS, FAIL und UNVERIFIED zeigen
11. UX-/Methodikprobleme als Issues erfassen
12. Stop/Start und destruktive Deinstallation testen

Erst danach NEXT-113 (Backup/Export/Consultant Report) priorisieren.
