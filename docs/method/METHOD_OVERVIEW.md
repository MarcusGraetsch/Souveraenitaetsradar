# Method Overview

## 1. Process core

The Radar uses BSI-200-3-/ISO-27005-like risk-process logic for scope, hazards, risk analysis, treatment and acceptance, supplemented by explicit sovereignty-specific risk types.

## 2. Assessment target

The target is a **workload in a concrete provider/service/architecture/contract context**, independent of cloud brand.

## 3. Capability layers

### Provider / Service Capability
What a service offers or contractually promises.

### Applied Capability
What the customer actually uses or proves through supplied evidence.

Recommended state model:

`asserted -> documented -> observed -> configured -> tested -> attested`

`available` is a provider-side state and does not alone satisfy Applied Capability.

## 4. Output axes

- Sovereignty Capability
- Workload Sovereignty Risk
- Security/Operational Risk
- Evidence Confidence

No axis silently compensates another.

## 5. Hard Gates

See `data/method/r4_hard_gates.csv`.

1. Jurisdiction & Effective Control
2. Data Residence & Processing
3. Key Control
4. Exit & Portability
5. Operational Autonomy
6. Identity & Trust Anchors
7. Supply Chain Critical Dependencies
8. Security Minimum

## 6. Evidence acquisition

Default: Customer Evidence Pack. Evidence may be contractual, assurance, architecture, IaC/config export, customer-generated provider export, test evidence, interview, public-provider evidence or manual observation.

## 7. Gate first, score second

A non-compensable minimum requirement cannot be averaged away by other strengths.

## 8. Structural risk

Persistent dependencies such as lock-in or concentration are modelled as:

`condition/exposure -> optional trigger -> consequence -> controls -> impact`.

## 9. AI/Agent systems

At least:

- Data Control
- Model Portability
- Agent/Tool/Policy Portability
- Tool Authorization / Side Effects
- Model/Provider/Terms Drift

## 10. Provenance

Every question/rule/threshold identifies whether it is external, externally derived, internal method design, project assumption or evidence observation.
