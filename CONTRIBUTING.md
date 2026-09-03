# Contributing

## Workflow

1. Select/create an issue with acceptance criteria.
2. Read `AGENTS.md` and project state.
3. Create branch from `main`.
4. Implement scoped change.
5. Update provenance/tests/docs.
6. Open PR using template.
7. Resolve review findings.
8. Prefer squash merge after approval.

## Commit prefixes

`method:`, `research:`, `feat:`, `fix:`, `test:`, `docs:`, `chore:`.

## Provider neutrality

New provider-specific parsing belongs under an adapter namespace. Core rules must not depend on provider brand/API names.

## Customer data

No secrets, customer evidence packs, contracts or unredacted exports in Git. Use synthetic fixtures.

## Rule changes

Scoring/Hard-Gate/Trust/default threshold changes require decision reference, provenance, regression/boundary tests and explicit statement whether external or internal.
