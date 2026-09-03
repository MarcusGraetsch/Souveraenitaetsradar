# Tool Architecture – Zielbild

```text
Sources / Evidence
  ├─ Standards & regulation
  ├─ Provider docs / contracts
  ├─ Technical collectors
  ├─ CMDB / DataGerry / DORA-RoI-like inventory
  └─ Human interviews / tests
          │
          ▼
Evidence Ingestion & Normalization
          │
          ├─ provenance / version / hash
          ├─ claim extraction
          └─ scope / trust / freshness
          │
          ▼
Domain Graph
  Workload ─ Provider ─ Service ─ Contract ─ Legal Entity
     │          │         │          │
   Data       Region     Key       Subprovider
     │          │         │          │
  Model ─ Agent/Tool ─ Identity ─ Dependency
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
  ├─ evidence matching
  ├─ conflict detection
  ├─ follow-up questions
  └─ explanation/draft reporting
          │
          ▼
Human Review / Risk Acceptance
          │
          ▼
Radar / Management Report / Measures
```

KI sitzt **nicht** an der Stelle der deterministischen Gate-Entscheidung oder Risikoakzeptanz.
