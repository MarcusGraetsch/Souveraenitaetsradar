# Task Protocol for Human and AI Contributors

## Task states

`backlog -> ready -> in_progress -> review -> blocked -> done`

## Before work

Record in issue/plan:

- outcome
- role
- files
- dependencies
- provenance needs
- acceptance criteria
- review class

## During work

- Keep one primary outcome per issue.
- If scope changes materially, update issue before expanding implementation.
- Do not silently alter method defaults while doing unrelated development.

## Handoff payload

Every substantive agent handoff contains:

```yaml
completed: []
changed_files: []
tests: []
decisions: []
open_questions: []
risks: []
recommended_next_action: "..."
```

Use `project/agent-log/` for durable detail. Use `PROJECT_STATE.yaml` only for current project truth.
