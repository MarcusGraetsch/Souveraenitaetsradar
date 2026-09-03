# Customer Evidence Pack

## Goal

A portable handoff from customer to assessment without giving the assessor live cloud access.

## Minimal pack

```text
evidence-pack/
├── manifest.json
├── evidence/
│   ├── EV-001.json
│   └── EV-002.json
└── attachments/          # optional; normally secure project storage, not Git
```

## Manifest

Identifies assessment, customer-controlled scope, producer, date, evidence IDs and redaction statement.

## Evidence record

Each evidence record states:

- what it claims
- evidence type
- producer/source
- scope (workload/service/location/resource/contract)
- locator into attachment/source
- time/version
- applied state
- trust dimensions
- sensitivity
- review status

## Redaction

Never require secrets. Resource identifiers may be pseudonymised as long as relationships remain stable.

## Evidence gaps

Missing evidence is explicit. The tool should generate a request/follow-up rather than infer a negative technical state.
