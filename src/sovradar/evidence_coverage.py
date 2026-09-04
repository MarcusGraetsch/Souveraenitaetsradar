from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .models import AppliedState, EvidenceRecord, EvidenceRequest


class EvidenceCoverageError(ValueError):
    pass


@dataclass(frozen=True)
class RequestRequirement:
    request_id: str
    min_trust: int
    min_applied_state: AppliedState
    reason: str = ""


_ACCEPTABLE_STATES: dict[AppliedState, frozenset[AppliedState]] = {
    AppliedState.ASSERTED: frozenset(AppliedState),
    AppliedState.AVAILABLE: frozenset({
        AppliedState.AVAILABLE,
        AppliedState.DOCUMENTED,
        AppliedState.OBSERVED,
        AppliedState.CONFIGURED,
        AppliedState.TESTED,
        AppliedState.ATTESTED,
    }),
    AppliedState.DOCUMENTED: frozenset({
        AppliedState.DOCUMENTED,
        AppliedState.OBSERVED,
        AppliedState.CONFIGURED,
        AppliedState.TESTED,
        AppliedState.ATTESTED,
    }),
    AppliedState.OBSERVED: frozenset({
        AppliedState.OBSERVED,
        AppliedState.TESTED,
        AppliedState.ATTESTED,
    }),
    AppliedState.CONFIGURED: frozenset({
        AppliedState.CONFIGURED,
        AppliedState.TESTED,
        AppliedState.ATTESTED,
    }),
    AppliedState.TESTED: frozenset({AppliedState.TESTED, AppliedState.ATTESTED}),
    AppliedState.ATTESTED: frozenset({AppliedState.ATTESTED}),
}


def state_satisfies(actual: AppliedState, required: AppliedState) -> bool:
    """Return whether an evidence state is sufficient for a required state.

    The relation is intentionally explicit rather than a simple numeric ranking:
    `observed` and `configured` are not treated as interchangeable. This is an
    internal evidence-sufficiency rule, not an external normative scale.
    """

    return actual in _ACCEPTABLE_STATES[required]


def requirements_from_plan(plan: dict[str, Any]) -> list[RequestRequirement]:
    raw = plan.get("required_requests")
    if not isinstance(raw, list) or not raw:
        raise EvidenceCoverageError("pilot plan requires a non-empty required_requests list")
    result: list[RequestRequirement] = []
    seen: set[str] = set()
    for item in raw:
        if not isinstance(item, dict):
            raise EvidenceCoverageError("required_requests entries must be objects")
        request_id = str(item.get("request_id") or "").strip()
        if not request_id:
            raise EvidenceCoverageError("required request without request_id")
        if request_id in seen:
            raise EvidenceCoverageError(f"duplicate required request: {request_id}")
        seen.add(request_id)
        try:
            min_trust = int(item.get("min_trust"))
        except (TypeError, ValueError) as exc:
            raise EvidenceCoverageError(f"invalid min_trust for {request_id}") from exc
        if min_trust not in range(0, 6):
            raise EvidenceCoverageError(f"min_trust outside 0..5 for {request_id}")
        try:
            min_state = AppliedState(str(item.get("min_applied_state") or ""))
        except ValueError as exc:
            raise EvidenceCoverageError(f"invalid min_applied_state for {request_id}") from exc
        result.append(
            RequestRequirement(
                request_id=request_id,
                min_trust=min_trust,
                min_applied_state=min_state,
                reason=str(item.get("reason") or "").strip(),
            )
        )
    return result


def _candidate_diagnostics(
    record: EvidenceRecord,
    requirement: RequestRequirement,
    workload_id: str,
) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if record.scope.get("workload_id") != workload_id:
        reasons.append(
            f"scope mismatch: {record.scope.get('workload_id')!r} != {workload_id!r}"
        )
    if record.effective_trust < requirement.min_trust:
        reasons.append(
            f"effective trust {record.effective_trust} < required {requirement.min_trust}"
        )
    if not state_satisfies(record.applied_state, requirement.min_applied_state):
        reasons.append(
            f"applied state {record.applied_state.value} does not satisfy required {requirement.min_applied_state.value}"
        )
    return not reasons, reasons


def analyze_request_coverage(
    records: Iterable[EvidenceRecord],
    catalog: Iterable[EvidenceRequest],
    plan: dict[str, Any],
    *,
    workload_id: str,
) -> dict[str, Any]:
    """Assess whether a customer evidence pack covers assessment-specific requests.

    Statuses are evidence-workflow statuses, not risk/gate decisions:
    - VERIFIED: sufficient evidence and human review/approval exist.
    - REVIEW_REQUIRED: evidence is technically sufficient but not yet human reviewed.
    - INSUFFICIENT: mapped evidence exists but misses scope/trust/applied-state requirements.
    - MISSING: no evidence maps to the request.
    """

    records = list(records)
    catalog_map = {item.request_id: item for item in catalog}
    requirements = requirements_from_plan(plan)
    unknown_required = {item.request_id for item in requirements} - set(catalog_map)
    if unknown_required:
        raise EvidenceCoverageError(f"unknown required request ids: {sorted(unknown_required)}")

    mapped_request_ids = {request_id for record in records for request_id in record.request_ids}
    unknown_mapped = mapped_request_ids - set(catalog_map)
    if unknown_mapped:
        raise EvidenceCoverageError(f"evidence maps to unknown request ids: {sorted(unknown_mapped)}")

    coverage: list[dict[str, Any]] = []
    gaps: list[dict[str, Any]] = []
    counts = {"VERIFIED": 0, "REVIEW_REQUIRED": 0, "INSUFFICIENT": 0, "MISSING": 0}

    for requirement in requirements:
        request = catalog_map[requirement.request_id]
        candidates = [record for record in records if requirement.request_id in record.request_ids]
        candidate_details: list[dict[str, Any]] = []
        sufficient_reviewed: list[EvidenceRecord] = []
        sufficient_unreviewed: list[EvidenceRecord] = []

        for record in candidates:
            sufficient, reasons = _candidate_diagnostics(record, requirement, workload_id)
            human_reviewed = record.review_status in {"reviewed", "approved"}
            candidate_details.append(
                {
                    "evidence_id": record.evidence_id,
                    "evidence_type": record.evidence_type,
                    "applied_state": record.applied_state.value,
                    "effective_trust": record.effective_trust,
                    "review_status": record.review_status,
                    "scope_workload_id": record.scope.get("workload_id"),
                    "sufficient": sufficient,
                    "human_reviewed": human_reviewed,
                    "deficiencies": reasons,
                }
            )
            if sufficient and human_reviewed:
                sufficient_reviewed.append(record)
            elif sufficient:
                sufficient_unreviewed.append(record)

        if sufficient_reviewed:
            status = "VERIFIED"
            reason = "Mindestens ein scope-, trust- und state-passender Nachweis ist human-reviewed/approved."
        elif sufficient_unreviewed:
            status = "REVIEW_REQUIRED"
            reason = "Passende Evidence liegt vor, ist aber noch nicht human-reviewed/approved."
        elif candidates:
            status = "INSUFFICIENT"
            reason = "Gemappte Evidence liegt vor, erfüllt aber Scope, Trust oder Applied-State-Mindestanforderung nicht."
        else:
            status = "MISSING"
            reason = "Keine Evidence ist diesem Evidence Request zugeordnet."

        counts[status] += 1
        entry = {
            "request_id": request.request_id,
            "gate_id": request.gate_id,
            "claim_area": request.claim_area,
            "status": status,
            "status_reason": reason,
            "required_min_trust": requirement.min_trust,
            "required_min_applied_state": requirement.min_applied_state.value,
            "requirement_reason": requirement.reason,
            "catalog_typical_min_trust": request.typical_min_trust,
            "catalog_preferred_applied_state": request.preferred_applied_state,
            "acceptable_evidence": request.acceptable_evidence,
            "follow_up": request.follow_up,
            "provenance": request.provenance,
            "evidence_ids": [item.evidence_id for item in candidates],
            "candidates": candidate_details,
        }
        coverage.append(entry)
        if status != "VERIFIED":
            gaps.append(
                {
                    "request_id": request.request_id,
                    "gate_id": request.gate_id,
                    "status": status,
                    "missing_or_action": request.follow_up,
                    "reason": reason,
                    "candidate_evidence_ids": [item.evidence_id for item in candidates],
                }
            )

    evidence_types = sorted({record.evidence_type for record in records})
    effective_trusts = [record.effective_trust for record in records]
    scope_mismatch_ids = sorted(
        record.evidence_id for record in records if record.scope.get("workload_id") != workload_id
    )
    without_locator = sorted(record.evidence_id for record in records if not record.locator)
    without_source_ref = sorted(record.evidence_id for record in records if not record.source_ref)

    return {
        "pilot_id": plan.get("pilot_id"),
        "assessment_id": plan.get("assessment_id"),
        "workload_id": workload_id,
        "summary": {
            "evidence_count": len(records),
            "evidence_classes": evidence_types,
            "evidence_class_count": len(evidence_types),
            "required_request_count": len(requirements),
            "verified": counts["VERIFIED"],
            "review_required": counts["REVIEW_REQUIRED"],
            "insufficient": counts["INSUFFICIENT"],
            "missing": counts["MISSING"],
            "min_effective_trust": min(effective_trusts, default=0),
            "max_effective_trust": max(effective_trusts, default=0),
            "scope_mismatch_count": len(scope_mismatch_ids),
        },
        "request_coverage": coverage,
        "gaps": gaps,
        "quality_findings": {
            "scope_mismatch_evidence_ids": scope_mismatch_ids,
            "missing_locator_evidence_ids": without_locator,
            "missing_source_ref_evidence_ids": without_source_ref,
        },
        "interpretation": [
            "Coverage status is evidence sufficiency/workflow state, not a Hard-Gate PASS/FAIL decision.",
            "Public provider capability evidence remains provider/service capability unless applied configuration is evidenced.",
            "REVIEW_REQUIRED never upgrades Evidence to a human-reviewed Claim automatically.",
        ],
    }
