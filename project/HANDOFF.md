# Project Handoff

## Kurzfassung

Der Souveränitätsradar ist kein AWS-Collector-Projekt. Der aktuelle Kern ist eine **cloud-agnostische Assessment-Methode mit kundenvermittelter Evidence**.

Am 03.09.2026 wurde die R6-Richtung korrigiert: Ein durch uns gesteuerter Read-only-Collector in Kundenaccounts wäre im Beratungsalltag häufig unrealistisch und erzeugt Credential-, Haftungs- und Security-Probleme. Dieser Ansatz ist als Standard verworfen.

## Fachlicher Kern

Bewertet wird ein **Workload in einer konkreten Provider-/Service-/Architektur-/Vertragskonstellation**, nicht ein Provider pauschal.

Getrennte Ausgaben:

- Security Capability
- Sovereignty Capability
- Workload Sovereignty Risk
- klassisches Informationssicherheits-/Betriebsrisiko
- Evidence Confidence

Hard Gates:

1. Jurisdiktion & Effective Control
2. Datenresidenz & Verarbeitung
3. Schlüsselhoheit
4. Exit & Portabilität
5. Operational Autonomy
6. Identity & Trust Anchors
7. Supply Chain Critical Dependencies
8. Security Minimum

## Aktueller Evidence-Prozess

```text
Customer / Provider / Auditor
   │
   ├─ Vertrag / DPA / SLA
   ├─ Architektur / CMDB / Dependency Export
   ├─ IaC / redigierter Konfig-Export
   ├─ kundenseitiger Provider-Export
   ├─ Assurance Report / Zertifikat
   ├─ Screenshot / Screenshare Observation
   └─ Testprotokoll
          │
          ▼
Customer Evidence Pack
          │
          ▼
Validation + Normalization + Claim/Evidence Mapping
          │
          ▼
Generic Domain Graph / Rule Engine
          │
          ▼
PASS / FAIL / UNVERIFIED + Risks + Confidence
          │
          ▼
AI-assisted Explanation + Human Review
```

## Bereits vorhanden

- Methodenmodell v1.0 als Workbook
- 128 Fragen in acht Domänen
- Risiko-Taxonomie inkl. G z.S1–G z.S12
- R4 Hard Gates/Factor Rules
- Source-/Provenienzregister
- erste deterministische Python-Regeln
- Evidence-Pack-Schema und lokaler Validator
- Multi-Agent-/Review-/PM-Struktur
- historische R5-Bedrock-Evidence als Provider-Beispiel

## Verworfener Ansatz

Der v0.9 AWS-Bedrock-Collector ist **nicht** der nächste Schritt und **nicht** die Zielarchitektur. Historie siehe `docs/history/R6_AWS_COLLECTOR_APPROACH_RETIRED.md`.

## Nächste Arbeit

Beginne mit `NEXT-101`, `NEXT-102` oder `NEXT-103`. Ein guter erster Development-Task ist der lokale Evidence-Pack-Loader und die Verbindung `Evidence -> Claim -> Gate`.

## Regeln für den nächsten Agenten

- Keine Cloud-Credentials anfordern.
- Keine Provider-spezifische Logik in `src/sovradar/rules.py` einbauen.
- Provider Adapter nur als Übersetzungsschicht.
- Kein Evidence Gap als FAIL ausgeben.
- Alle neuen Methodenregeln mit Provenienz versehen.
- Issue/PR/Handoff/Agent-Log pflegen.
