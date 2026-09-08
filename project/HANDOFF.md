# Project Handoff

## Kurzfassung – Stand 08.09.2026

Der Souveränitäts-Radar besteht aus einem cloud-agnostischen Methodenkern und einer lokal installierbaren Consultant-Webanwendung. Die technische MVP-Basis bleibt unverändert; auf Branch `method/decision-case-provider-intelligence` / PR #66 wird derzeit die **nächste Methodenebene** vorbereitet.

Der neue Entwurf `docs/method/METHOD_CORE_V0_4_DE.md` positioniert den Radar ausdrücklich als **Decision-Support-Instrument für vergleichende Souveränitätsentscheidungen**, nicht als universelles Compliance-Audit.

Issue #67 dokumentiert diese Neufokussierung.

## Methodenkern v0.4 – verbindliche Richtung für weitere Planung

### Beratungsziel

Ein konkreter Workload wird über mehrere realistische Betriebs-/Architekturvarianten verglichen. Eine Empfehlung ist zulässig; finale Kundenentscheidung, Risikoakzeptanz und Legal Conclusions bleiben beim Kunden.

Bei Migrations-/Modernisierungsentscheidungen soll die realistische **Status-quo-/Nichtstun-Variante** mitbetrachtet werden, damit auch Modernisierungs-, Skill-, Security- und Innovationsrisiken des Verbleibs sichtbar werden.

### Sichtbare Entscheidungsdimensionen

1. Geschäft & Innovation
2. Security & Resilienz
3. Recht, Daten & Kontrolle
4. Technologie & Exit
5. Organisation & Skills
6. Lieferkette & Geopolitik
7. Wirtschaft & Vertrag

Separat: **Evidence Confidence / Belastbarkeit der Erkenntnisse**.

Die internen Achsen Security Capability, Sovereignty Capability, Workload Sovereignty Risk und Evidence Confidence bleiben bestehen und dürfen sich nicht still kompensieren.

### Framework-Rollen

Frameworks werden nicht als mehrere vollständige Pflichtaudits gestapelt:

- Bitkom Cloud-Souveränität 2026: Orientierungs-/Handlungsfähigkeitsrahmen, Risiko/Chance, Skills, Interdependenzen und Exit.
- EU Cloud Sovereignty Framework + BSI C3A: Provider-/Service-Souveränitäts- und Evidence-Layer.
- BSI 200-3 / IT-Grundschutz: Anschlussfähigkeit, Security-/Resilienz-Deep-Dive, Gefährdungs- und Vollständigkeitsreferenz; die 47 elementaren Gefährdungen sind kein sichtbarer Pflichtfragebogen.
- Data Act: allgemeine Exit-/Switching-/Portabilitätsreferenz, soweit anwendbar.
- C5: Assurance-/Control-Evidence.
- NIS2, DORA, DSGVO/EDPB, AI Act, BSI-Mindeststandard usw.: aktivierbare Compliance-Overlays bzw. Methodenquellen nur bei tatsächlicher Anwendbarkeit.

Siehe `docs/method/SOURCE_GUIDE.md`.

### Adaptive Fragenlogik

Die 128 Methodenfragen bleiben als **Question Library** erhalten. Ziel der sichtbaren Beratung ist ein Screening von ca. 15–25 Kernfragen und danach nur gezielte Vertiefung, wenn:

- die Antwort die Empfehlung materiell verändern kann;
- ein Hard Gate / Mindestkriterium betroffen ist;
- ein wesentliches Risiko oder ein wesentlicher Vorteil ungeklärt ist;
- sich die Varianten gerade in diesem Punkt unterscheiden;
- ein entscheidungsrelevantes Evidence Gap geschlossen werden muss.

NEXT-116 wird daher erst nach methodischer Referenzfallvalidierung weitergeführt.

### Intake

Der bevorzugte Ablauf lautet:

```text
vorhandene Artefakte / Provider Intelligence
        -> Vorbefüllung
        -> kurzes Interview
        -> Entscheidungslücken
        -> gezielte Evidence Requests
        -> Claims / Risiken / Gates
        -> Vergleich / Empfehlung
```

Optionale Inputs sind Servicekatalog/CMDB, ArchiMate/EA, Architekturdiagramme, BIA/BCM, ISMS/Risikoregister, Verträge/SLA/AVV, IaC, Kubernetes/Helm/Argo CD, IAM/PKI/KMS, FinOps sowie Backup-/Restore-/DR-/Exit-Tests. Kein Artefakttyp ist Voraussetzung.

ArchiMate kann über das standardisierte Model Exchange File Format bzw. dokumentierte Tool-Adapter genutzt werden. Ein generisches ArchiMate-YAML wird nicht vorausgesetzt. Siehe `docs/architecture/INTAKE_AND_CONTEXT_SOURCES.md`.

### Politische / geopolitische Sorgen

Aussagen wie „US-Cloud ist unsouverän“ oder „deutscher Provider ist souverän“ sind keine Methodenregeln. Sorgen werden in prüfbare Szenarien übersetzt, z. B.:

- compelled access / staatlich erzwungener Zugriff
- Sanktionen / Exportkontrollen
- Serviceentzug oder -beschränkung
- Support-/Updateverlust
- Change of Control
- Preis-/Vertragsänderung

Diese Szenarien werden konsistent auf alle relevanten Varianten angewandt, einschließlich On-Prem-Abhängigkeiten von ausländischer Hardware, Software, Lizenzen, Support oder Trust Anchors.

## Bestehende Evidence-/Gate-Regeln bleiben unverändert

- cloud-agnostischer Core
- Customer-mediated Evidence; keine Cloud-Credentials als Voraussetzung
- Provider Adapter = Translation only
- Provider/Service Capability ≠ Applied Capability
- Evidence Confidence ≠ Risikohöhe
- Gate first, score second
- fehlende Evidence = `UNVERIFIED`, nicht automatisch FAIL
- Human-reviewed Claims sind die einzige Brücke von Evidence zu deterministischen Hard Gates
- Raw Evidence / LLM-Proposals wirken niemals direkt auf Gates
- Legal Conclusions und Risk Acceptance bleiben menschlich
- Raw Kundenevidence wird nicht committed

## Technischer MVP-Stand

NEXT-101, NEXT-112, NEXT-113, NEXT-114 und NEXT-115 sind technisch umgesetzt/validiert. Die aktuelle Webapp besitzt weiterhin den bisherigen Assessment-/Questions-/Evidence-/Claims-/Gates-Workflow. Die v0.4-Methodik ist **noch nicht in Runtime, Schema oder UI implementiert**.

Wichtige vorhandene technische Regeln:

- Applicability: `applicable`, `needs_review`, `not_applicable`
- Workflow Stage: `screening`, `clarification`, `deep_dive`, `completed`, `excluded`
- Evidence Coverage: `VERIFIED`, `REVIEW_REQUIRED`, `INSUFFICIENT`, `MISSING`
- öffentliche Provider-Dokumentation mit `available` belegt keine `configured` Applied Capability
- Standardexport/Consultant Report enthalten keine Raw Evidence
- Restore erzeugt neues Assessment und berechnet Gates neu

## Nächste Schritte

### NEXT-118 / Issue #28 – weiterhin erster P0-Schritt

Erste manuelle Consultant-Installation und Evaluation auf einem frischen Zielsystem. Zusätzlich zu den bisherigen UX-/Evidence-Fragen soll explizit dokumentiert werden, wo die aktuelle UI den neuen v0.4-Decision-Support-Kern überlädt oder falsch priorisiert.

### NEXT-119 / Issue #67 – danach Methodenkern validieren

Mindestens denselben Workload über folgende Referenzvarianten vergleichen:

- bestehendes On-Prem
- US-Hyperscaler in EU-Region
- deutscher/europäischer Provider
- optional hypothetische Soll-/Sovereign-Architektur

Ziele:

- Screeningkern auf ca. 15–25 Fragen kalibrieren
- adaptive Deep-Dive-Trigger definieren
- Framework-/Compliance-Overlay-Aktivierung prüfen
- Status quo / Business Value sichtbar machen
- geopolitische Sorgen in prüfbare Szenarien übersetzen
- Recommendation Template testen

Erst danach sollten größere Runtime-/Schema-/UI-Umbauten für DecisionCase/ArchitectureOptions und die neue sichtbare Methodik umgesetzt werden.

## Offene Security-Hardening-Punkte

- Issue #25 / NEXT-117: ZIP-Decompression-Bomb-Limits vor untrusted Backup-Import
- Issue #26: vollständige serverseitige Schema-Validierung für untrusted Structured Restore

## Primäre Dokumente für den nächsten Agenten

1. `AGENTS.md`
2. `project/PROJECT_STATE.yaml`
3. dieses Handoff
4. `project/NEXT_ACTIONS.yaml`
5. `project/DECISIONS.yaml`
6. `docs/method/METHOD_CORE_V0_4_DE.md`
7. `docs/method/GLOSSARY_DE.md`
8. `docs/architecture/DECISION_CASE_AND_PROVIDER_INTELLIGENCE.md`
9. `docs/architecture/INTAKE_AND_CONTEXT_SOURCES.md`
10. `docs/method/SOURCE_GUIDE.md`

Repo-State schlägt Chatgedächtnis.
