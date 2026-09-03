# Domain Model

## Core entities

- `Assessment`
- `Organization`
- `BusinessFunction`
- `Workload`
- `Provider`
- `Service`
- `LegalEntity`
- `Contract`
- `Location`
- `DataClass`
- `IdentityTrustAnchor`
- `KeyControlCapability`
- `ModelOrAIService`
- `Dependency`
- `CommonCauseGroup`
- `Evidence`
- `Claim`
- `ControlCapability`
- `RiskScenario`
- `GateRequirement`
- `GateResult`

## Provider-neutral evidence relationship

```text
Evidence --supports/contradicts--> Claim
Claim --describes--> GenericFact / Capability
GenericFact --scoped-to--> Workload / Service / Contract / Dependency
GateRequirement --evaluates--> Applied Capability
```

## Applied state

Recommended ordered states:

`asserted -> documented -> observed -> configured -> tested -> attested`

Provider service documentation may additionally establish `available`, but `available` alone is not customer-specific Applied Capability.
