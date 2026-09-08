# Method Overview

> Primäre verständliche Fachreferenz: `docs/method/METHOD_CORE_V0_4_DE.md`.  
> Terminologie: `docs/method/GLOSSARY_DE.md`.  
> C3A-Review: `docs/method/C3A_V1_0_REVIEW.md` + `data/method/c3a_v1_0_crosswalk.csv`.

## 1. Purpose

Der Souveränitäts-Radar ist primär ein **Decision-Support-Instrument** für die vergleichende Bewertung von Betriebs-/Architekturvarianten eines konkreten Workloads. Er ist kein universelles Compliance-Audit und kein politisches Provider-Ranking.

Die Methode soll eine nachvollziehbare Empfehlung erzeugen dürfen; finale Entscheidung, Risikoakzeptanz und rechtliche Würdigung bleiben beim Kunden.

## 2. Method position

Der Radar ist **anschlussfähig** an etablierte Risiko- und Compliance-Verfahren, aber nicht auf ein einziges Framework reduziert.

- Bitkom Cloud-Souveränität 2026: konzeptionelle Orientierung zu Handlungsfähigkeit, Chancen/Risiken, Skills, Interdependenzen und Exit.
- EU Cloud Sovereignty Framework: breiter Provider-/Service-Souveränitätsrahmen und Evidence-Fragen.
- BSI C3A v1.0: kriterienspezifischer Provider-/Service-Autonomie-Layer für SOV-1 bis SOV-6; `Criterion`/`Additional Criterion`; use-case-abhängige Kundenauswahl; C5-Prerequisite für formale C3A-Erfüllung.
- BSI 200-3: Scope-/Zielobjekt-, Gefährdungs-, Risikobehandlungs- und Risikoappetit-Referenz; zusätzlich Deep Dive und Vollständigkeitscheck.
- Data Act: allgemeine Exit-/Switching-/Portabilitätsreferenz, soweit anwendbar.
- C5: Security-/Assurance-Layer und C3A-Voraussetzung.
- NIS2, DORA, DSGVO/EDPB, AI Act und weitere Vorgaben: aktivierbare Compliance-Overlays bzw. Methodenquellen, sofern für Kunde/Workload einschlägig.

## 3. Assessment target

The target is a **workload in a concrete provider/service/architecture/contract context**, independent of cloud brand.

For comparative decisions, multiple ArchitectureOptions of the same workload are evaluated under one DecisionCase. A realistic status-quo / do-nothing option should be included where relevant.

C3A itself evaluates a concrete **set of cloud services** in the selected criterion scope. A provider brand is never sufficient scope for a C3A claim.

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

Die sieben Dimensionen sind interne Radar-Methodik, keine unveränderte C3A-/EU-CSF-Taxonomie.

## 5. Capability layers

### Provider / Service Capability
What a service offers, documents, contractually promises or has independently attested.

### Applied Capability
What the customer actually uses or proves through supplied evidence.

Recommended state model in the current runtime:

`asserted -> documented -> observed/configured -> tested -> attested`

`available` is a provider-side state and does not alone satisfy Applied Capability.

These states are internal operationalization, not an official C3A/EU maturity scale.

### C3A Criterion Evidence

C3A Criterion-/Additional-Criterion-Erfüllung wird kriterienspezifisch, scope- und evidencebezogen betrachtet. `C`, `AC`, EU- und Deutschlandvarianten werden nicht in die interne 0–4-Skala als offizielle Levels umgedeutet.

## 6. Adaptive assessment instead of full questionnaire

The existing question bank is a **Question Library**, not a mandatory questionnaire.

Target flow:

`existing artifacts -> prefill -> 15–25 core screening questions -> decision gaps -> targeted deep dives -> evidence -> comparison/recommendation`

A question is deepened when it can materially change the recommendation, affects a non-compensable minimum requirement, clarifies a significant risk/benefit, differentiates options or closes an important evidence gap.

The 15–25 range is an internal design hypothesis and must be calibrated in NEXT-119.

For C3A, the customer/use case determines which Criteria and Additional Criteria are relevant. The Radar should therefore later instantiate a `C3ARequirementProfile` instead of forcing all C3A criteria into every assessment.

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

No single artifact type is a prerequisite. Context Fact and Evidence remain distinct.

For C3A residence checks, the target model should distinguish Account Data, Cloud Service Customer Data, Cloud Service Derived Data and Cloud Service Provider Data.

## 8. Hard Gates

The current runtime uses eight internal Hard Gates; see `data/method/r4_hard_gates.csv`.

Their current structure is **internal method design**, not a BSI/EU/C3A gate catalog. The C3A review confirms that future non-compensable requirements should increasingly be instantiated from explicit customer requirements/profiles. The eight gate domains may remain a management grouping, but C3A C1/C2/AC choices are not fixed gate levels.

## 9. Gate first, score second

A non-compensable minimum requirement cannot be averaged away by other strengths. Scores are optional management aids, not truth values.

## 10. Structural and geopolitical risk

Persistent dependencies such as lock-in or concentration are modelled as:

`condition/exposure -> optional trigger -> consequence -> controls -> impact`.

Political or geopolitical concerns are translated into testable scenarios (e.g. compelled access, sanctions/export controls, service withdrawal, support loss, ownership/control change, contractual/price shock) and applied consistently to all relevant options, including On-Prem supply-chain dependencies.

C3A contributes concrete provider-side test points for some of these scenarios, especially extraterritorial exposure, disconnect/reconnect, supply-chain substitution and provider development continuity.

## 11. AI/Agent systems

At least:

- Data Control
- Model Portability
- Agent/Tool/Policy Portability
- Tool Authorization / Side Effects
- Model/Provider/Terms Drift

## 12. Provenance

Every question/rule/threshold identifies whether it is external, externally derived, internal method design, project assumption or evidence observation.

For C3A, the completed full-text review and `c3a_v1_0_crosswalk.csv` are the authoritative project mapping. Older broad C3A references in the Question Library must not be treated as complete C3A coverage until they are migrated in NEXT-119.
