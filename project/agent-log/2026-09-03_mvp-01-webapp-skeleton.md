# Agent Log – MVP-01 Consultant Web Application Skeleton

Date: 2026-09-03
Issue: #11
Roles: architect, developer, project-coordinator
Review class: B/C self-review; CI required before merge

## Goal

Turn the method repository into the first installable consultant-facing product skeleton, following the operational pattern: clone, install, test, run, stop and clean uninstall.

## Decisions implemented

- React/TypeScript/Vite frontend.
- FastAPI backend.
- PostgreSQL persistence.
- Local `.runtime/` document storage for MVP.
- Docker Compose deployment.
- No direct LLM/API integration in MVP-01.
- Copy/Paste LLM Bridge with deterministic JSON validation.
- Uninstall removes all generated application data after explicit confirmation.

## Scope implemented

- Docker Compose three-service skeleton (`web`, `api`, `db`).
- Assessment creation/listing/deletion.
- Question-bank loading from canonical CSV files.
- Assessment answer persistence.
- Evidence metadata + optional local file upload.
- Prompt Package generation.
- Structured LLM JSON validation/import as proposals.
- Runtime lifecycle scripts.
- API integration tests and frontend build in CI.

## Explicit non-scope

LLM API calls, provider account scanning, S3, n8n/LangGraph/LiteLLM, Keycloak/OIDC, Kubernetes, automatic acceptance of LLM proposals and full Hard-Gate evaluation in the UI.

## Handoff

After merge, first operational task is to clone `main` on a clean development VM and run `./install.sh` followed by one complete synthetic assessment flow. Findings should drive the next UI/rule-engine integration iteration.
