# R6 AWS Collector Approach – retired as standard

## Why it existed

R5 showed that public provider documentation cannot prove customer-specific Applied Capability. R6 v0.9 therefore experimented with a read-only AWS Bedrock collector.

## Why it was retired

- customers may not grant external consultants cloud credentials
- even read-only access introduces credential, liability and security concerns
- a provider API collector biases the product toward one cloud
- exit, autonomy, contracts and organizational controls cannot be proven by API collection alone

## What remains useful

- Provider Capability != Applied Capability
- evidence needs scope/time/provenance
- technical facts can be exported and normalized
- missing technical evidence should remain UNVERIFIED
- chain-of-custody concepts are useful for customer-generated exports

The current architecture implements these lessons through file-based Customer Evidence Packs and optional provider adapters.
