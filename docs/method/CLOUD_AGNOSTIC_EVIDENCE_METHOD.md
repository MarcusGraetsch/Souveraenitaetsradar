# Cloud-agnostic Evidence Method

## Evidence hierarchy by purpose

No single hierarchy is universally strongest. Evidence quality depends on the claim:

- **contractual/legal claim**: signed contract/DPA can outrank a technical screenshot
- **actual configuration claim**: exported configuration or observed setting can outrank provider marketing
- **control effectiveness claim**: repeatable test can outrank configuration
- **assurance claim**: independent report can outrank self-attestation, subject to scope/version

The Radar therefore stores `evidence_type`, `base_trust`, `scope_fit`, `freshness_fit`, and `applied_state` separately.

## Customer-friendly collection

For each gate, the assessor requests acceptable alternatives rather than one mandatory technology:

Example `HG-03 Key Control` may be evidenced by:

- key-management design + contract
- redacted KMS/Key Vault/Cloud KMS/OpenStack/K8s config export
- screenshots observed in session
- key revocation/restore test
- independent assurance

A customer can choose the evidence route allowed by policy.

## Provider independence test

A method question is acceptable for the core if it still makes sense after replacing provider brand names with another provider or SaaS product.
