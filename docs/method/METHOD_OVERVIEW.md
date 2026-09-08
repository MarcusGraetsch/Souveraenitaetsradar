# Method Overview

> Für die verständliche deutschsprachige Methodendarstellung gilt `docs/method/METHOD_CORE_V0_4_DE.md` als primäre Arbeitsreferenz. Terminologie: `docs/method/GLOSSARY_DE.md`.

## 1. Purpose

Der Souveränitäts-Radar ist primär ein **Decision-Support-Instrument** für die vergleichende Bewertung von Betriebs-/Architekturvarianten eines konkreten Workloads. Er ist kein universelles Compliance-Audit und kein politisches Provider-Ranking.

Die Methode soll eine nachvollziehbare Empfehlung erzeugen dürfen; finale Entscheidung, Risikoakzeptanz und rechtliche Würdigung bleiben beim Kunden.

## 2. Method position

Der Radar ist **anschlussfähig** an etablierte Risiko- und Compliance-Verfahren, aber nicht auf ein einziges Framework reduziert.

- Bitkom Cloud-Souveränität 2026: konzeptionelle Orientierung zu Handlungsfähigkeit, Chancen/Risiken, Skills, Interdependenzen und Exit.
- EU Cloud Sovereignty Framework + BSI C3A: Provider-/Service-Souveränität und prüfbare Capability-/Evidence-Fragen.
- BSI 200-3: Scope-/Zielobjekt-, Gefährdungs-, Risikobehandlungs- und Risikoappetit-Referenz; zusätzlich Deep Dive und Vollständigkeitscheck.
- Data Act: allgemeine Exit-/Switching-/Portabilitätsreferenz, soweit anwendbar.
- C5: Assurance-/Control-Evidence.
- NIS2, DORA, DSGVO/EDPB, AI Act und weitere Vorgaben: aktivierbare Compliance-Overlays bzw. Methodenquellen, sofern für Kunde/Workload einschlägig.

## 3. Assessment target

The target is a **workload in a concrete provider/service/architecture/contract context**, independent of cloud brand.

For comparative decisions, multiple ArchitectureOptions of the same workload are evaluated under one DecisionCase. A realistic status-quo / do-nothing option should be included where relevant.

## 4. Visible decision dimensions

Die Managementsicht arbeitet mit sieben verständlichen Dimensionen:

1. Geschäft & Innovation
2. Security & Resilienz
3. Recht, Daten & Kontrolle
4. Technologie & Exit
5. Organisation & Skills
6. Lieferkette & Geopolitik
7. Wirtschaft & Vertrag

Separat: **Evidence Confidence / Belastbarkeit der Erkenntnisse**.

The detailed internal outputs remain:

- Sovereignty Capability
- Workload Sovereignty Risk
- Security/Operational Risk
- Evidence Confidence

No axis silently compensates another.

## 5. Capability layers

### Provider / Service Capability
What a service offers or contractually promises.

### Applied Capability
What the customer actually uses or proves through supplied evidence.

Recommended state model:

`asserted -> documented -> observed -> configured -> tested -> attested`

`available` is a provider-side state and does not alone satisfy Applied Capability.

## 6. Adaptive assessment instead of full questionnaire

The existing question bank is a **Question Library**, not a mandatory questionnaire.

Standard flow:

`existing artifacts -> prefill -> 15–25 core screening questions -> decision gaps -> targeted deep dives -> evidence -> comparison/recommendation`

A question is deepened when it can materially change the recommendation, affects a non-compensable minimum requirement, clarifies a significant risk/benefit, differentiates options or closes an important evidence gap.

## 7. Input channels

Customer-mediated Evidence remains standard. Optional intake sources include:

- interviews / workshops
- service catalog / CMDB
- ArchiMate / enterprise-architecture exports
- architecture diagrams
- BIA / BCM
- ISMS / risk register
- contracts / SLA / DPA / exit clauses
- IaC and declarative platform artifacts
- IAM / PKI / KMS documentation
- FinOps / cost data
- backup / restore / DR / exit tests

No single artifact type is a prerequisite.

## 8. Hard Gates

See `data/method/r4_hard_gates.csv`.

1. Jurisdiction & Effective Control
2. Data Residence & Processing
3. Key Control
4. Exit & Portability
5. Operational Autonomy
6. Identity & Trust Anchors
7. Supply Chain Critical Dependencies
8. Security Minimum

## 9. Gate first, score second

A non-compensable minimum requirement cannot be averaged away by other strengths. Scores are optional management aids, not truth values.

## 10. Structural and geopolitical risk

Persistent dependencies such as lock-in or concentration are modelled as:

`condition/exposure -> optional trigger -> consequence -> controls -> impact`.

Political or geopolitical concerns are translated into testable scenarios (e.g. compelled access, sanctions/export controls, service withdrawal, support loss, ownership/control change, contractual/price shock) and applied consistently to all relevant options, including On-Prem supply-chain dependencies.

## 11. AI/Agent systems

At least:

- Data Control
- Model Portability
- Agent/Tool/Policy Portability
- Tool Authorization / Side Effects
- Model/Provider/Terms Drift

## 12. Provenance

Every question/rule/threshold identifies whether it is external, externally derived, internal method design, project assumption or evidence observation.
