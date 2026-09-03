# Tool Architecture – Cloud-agnostic Target

```text
External / Customer-controlled sources
  ├─ Contracts / DPA / SLA / Exit clauses
  ├─ Architecture / CMDB / DataGerry / dependency exports
  ├─ IaC / configuration exports / screenshots
  ├─ Customer-generated provider inventory exports
  ├─ Assurance reports / certificates
  ├─ Public provider documentation
  ├─ Interviews / workshops
  └─ Exit / restore / failover / autonomy test reports
             │
             ▼
      Customer Evidence Pack
      ├─ manifest.json
      ├─ evidence records
      ├─ redacted attachments (outside Git)
      └─ scope / provenance / timestamps
             │
             ▼
Evidence Intake & Normalization
  ├─ schema validation
  ├─ evidence type / trust / scope / freshness
  ├─ claim extraction / page or field locators
  ├─ conflict detection
  └─ provider adapter (optional translation only)
             │
             ▼
Generic Domain Graph
  Workload ─ Provider ─ Service ─ Contract ─ Legal Entity
     │          │         │          │
   Data      Location   KeyControl  Subprovider
     │          │         │          │
  Model ─ Agent/Tool ─ Identity ─ Dependency/CommonCause
             │
             ▼
Deterministic Rule Engine
  ├─ applicability
  ├─ hard gates
  ├─ applied capability
  ├─ structural risk
  ├─ evidence confidence
  └─ decision state
             │
             ▼
AI-assisted Analyst Layer
  ├─ document extraction
  ├─ claim/evidence suggestions
  ├─ conflict/gap detection
  ├─ follow-up questions
  └─ explanation/report drafting
             │
             ▼
Human Review / Risk Acceptance
             │
             ▼
Radar / Management Report / Measures
```

## Key boundary

The Radar does **not** need credentials to AWS, Azure, GCP or another provider. A customer may generate exports using their own approved tooling and submit them as evidence.

## Provider adapters

Adapters only translate evidence such as:

- AWS KMS / Azure Key Vault / GCP Cloud KMS -> generic `KeyControlCapability`
- AWS Config / Azure Resource Graph / GCP Asset Inventory -> generic Resource/Location/Dependency facts
- provider-specific region names -> generic `Location` objects

Hard gates and risk thresholds stay outside adapters.
