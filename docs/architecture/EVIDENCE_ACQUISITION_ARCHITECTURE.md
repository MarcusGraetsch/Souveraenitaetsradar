# Evidence Acquisition Architecture

## Problem

A consulting method must work even when the customer will not grant external consultants cloud credentials. Requiring account access would also bind the product to specific provider APIs and increase operational/security liability.

## Standard acquisition modes

### 1. Customer-provided documents
Contracts, DPAs, SLAs, audit reports, policies, architecture diagrams, CMDB exports.

### 2. Customer-generated technical exports
The customer runs its own approved commands/tools and provides redacted outputs, e.g.:

- AWS Config / Resource Explorer / CLI JSON exports
- Azure Resource Graph / Azure Policy exports
- GCP Cloud Asset Inventory exports
- OpenStack resource exports
- Kubernetes manifests / Helm values / policy reports
- Terraform plan/state extracts with secrets removed
- SaaS admin/config exports

The Radar consumes files. It does not need provider credentials.

### 3. Screenshare / guided observation
A customer administrator opens the relevant configuration while the consultant records structured observations. Screenshots are optional and subject to customer policy.

### 4. Test evidence
Exit/restore/failover/key/identity/autonomy tests produce test reports. These are often stronger than static config evidence.

### 5. Public provider evidence
Provider docs, terms and trust-center material establish available service capability and conditional claims. They do not prove customer configuration.

## Evidence Pack

Each pack contains a manifest plus evidence records. Attachments may remain outside the repository; records can reference secure project storage.

Core fields:

- evidence_id
- evidence_type
- source / producer
- scope
- collected_or_valid_at
- framework/provider version
- applied_state
- claim_ids
- locator
- base_trust
- scope_fit
- freshness_fit
- sensitivity
- review_status

## Trust principle

`effective_trust = min(base_trust, scope_fit, freshness_fit)`

Trust does not raise/lower technical risk; it controls whether a finding is verified.

## What cannot be fully automated

- legal conclusions
- contractual interpretation
- business criticality and risk appetite
- effectiveness without test evidence
- exit/autonomy without actual exercise

Automation should expose gaps, not invent certainty.
