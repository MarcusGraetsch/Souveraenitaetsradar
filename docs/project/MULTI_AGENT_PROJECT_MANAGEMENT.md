# Multi-Agent Project Management

## Goal

Different AI systems and humans can continue the project without shared conversation memory.

## Durable coordination surfaces

- GitHub Issues – task intent, acceptance criteria, owner/agent role
- Branch – implementation scope
- Pull Request – review, provenance, tests, decision record
- `project/PROJECT_STATE.yaml` – current project truth
- `project/NEXT_ACTIONS.yaml` – prioritized work
- `project/DECISIONS.yaml` / ADR – accepted decisions
- `project/agent-log/` – session detail and handoff

## Agent lifecycle

1. **Orient**: read canonical files and issue.
2. **Plan**: write scope, role, acceptance criteria.
3. **Execute**: work on branch, keep changes scoped.
4. **Self-check**: tests, provenance, security.
5. **Review**: another agent/human if class B/C/D.
6. **Integrate**: merge only with no blockers.
7. **Handoff**: update logs/state as needed.

## Review separation

For method/security/legal-sensitive changes use a reviewer who did not author the main change. If only one agent is available, label review as `self-review` and keep an explicit follow-up review item.

## State hygiene

Do not turn `PROJECT_STATE.yaml` into a chronological log. Historical rationale belongs in ADRs and agent logs.

## Conflict handling

If parallel agents change the same method/state file:

- stop automatic merge
- reconcile against accepted decisions and source register
- preserve both rationales in review
- resolve before updating global state
