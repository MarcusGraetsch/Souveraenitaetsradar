# Provider-neutral Control / Capability Model

Core capabilities should be named by function, not brand.

| Generic capability | Example provider manifestations |
|---|---|
| DataLocationControl | regions, geo-fencing, tenant location commitments |
| KeyControlCapability | customer-managed/external keys, HSM, client-side encryption |
| IdentityTrustAnchor | external IdP, local IdP, break-glass, PKI/DNS trust |
| AuditObservabilityCapability | audit logs, export, independent telemetry |
| ExitPortabilityCapability | export formats, APIs, config portability, tested migration |
| OperationalAutonomyCapability | degraded mode, disconnect/reconnect, self-operation |
| SupplyChainTransparency | subprocessors, model providers, software/hardware dependencies |
| SecurityControlCapability | IAM, network isolation, monitoring, secure SDLC, runtime controls |

Provider adapters map evidence to these capabilities. Core gates consume only generic capabilities.
