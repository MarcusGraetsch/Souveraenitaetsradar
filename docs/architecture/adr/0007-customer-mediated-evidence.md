# ADR-0007 – Customer-mediated Evidence as default

Status: accepted – 2026-09-03

## Decision

The default evidence acquisition mechanism is a customer-controlled Evidence Pack. Customers provide documents, exports, observations and test reports. The Radar does not require live cloud credentials.

## Consequences

Positive:
- realistic consulting workflow
- smaller attack/credential surface
- easier redaction and approval
- provider independence
- reproducible file-based evidence

Trade-off:
- some technical facts require customer cooperation
- evidence can be less fresh than direct API access
- follow-up questions remain important

These trade-offs are handled through Evidence Confidence, not hidden automation assumptions.
