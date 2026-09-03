# AI Agent Architecture

## Objective

Multiple AI systems must be able to plan, implement, research and review without access to private prior chat history.

## Canonical context

`AGENTS.md` + `project/*` are the shared state. Model-specific files only redirect there.

## AI roles in the product

Appropriate:

- extract clauses/claims from supplied documents
- map claims to questions/gates
- identify contradictions and missing evidence
- normalize provider terminology through adapters
- propose follow-up questions
- draft explanations and reports
- assist with code/tests/reviews

Not autonomous:

- risk acceptance
- legal conclusion
- security exception
- hard-management-requirement changes

## Evidence safety

AI receives only evidence the customer has approved for the assessment environment. The product architecture must not assume AI has direct access to cloud tenants/accounts.

## Multi-agent repository work

- planner: decomposes issue and acceptance criteria
- implementer: changes code/docs/data
- reviewer: independently checks source/provenance/tests
- project-coordinator: updates state/handoff only when warranted

Agent identity is less important than durable files, issue state and review evidence.
