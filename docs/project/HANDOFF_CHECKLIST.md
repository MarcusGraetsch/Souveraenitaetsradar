# Handoff checklist

Before handing the repository to another human or agent:

- `main` contains the accepted state and CI is green.
- `AGENTS.md` reflects current non-negotiable rules.
- `project/PROJECT_STATE.yaml` reflects the current phase.
- `project/HANDOFF.md` explains the current method and discarded approaches.
- `project/NEXT_ACTIONS.yaml` contains executable next steps and dependencies.
- substantive decisions are in `project/DECISIONS.yaml` and/or ADRs.
- source-derived method content has provenance.
- raw customer evidence, credentials and secrets are absent from Git.
- active GitHub issues preserve their `NEXT-*` identifiers.

A receiving agent should be able to work from the repository without chat history.
