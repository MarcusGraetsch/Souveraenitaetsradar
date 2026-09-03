# Review Process

## Review classes

### A – documentation / low impact
Self-review acceptable.

### B – method / schema / deterministic rule
Requires method or technical review:
- provenance/source
- scenario/regression impact
- unit/boundary tests
- no hidden threshold changes
- provider neutrality

### C – evidence ingestion / parser / sensitive data path
Requires technical + security review:
- no credentials required
- no network access by default
- redaction/sensitivity handling
- malformed/untrusted files
- path traversal / oversized file concerns
- provenance preservation

### D – legal/compliance claim
Requires primary source and, for legal conclusions, appropriate human review. Provider self-statements are marked as such.

### E – provider adapter
Requires architecture review:
- translation only
- no provider-specific rules in core
- missing fields -> unknown, not fail
- fixtures and mapping tests

## Merge readiness

- scope clear
- validator/tests green
- provenance complete
- no `BLOCKER`
- handoff/state updated if needed

Comment classes: `BLOCKER`, `MAJOR`, `MINOR`, `QUESTION`, `NIT`.
