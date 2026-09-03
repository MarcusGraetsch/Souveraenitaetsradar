from __future__ import annotations

from collections.abc import Iterable

from .models import Claim, EvidenceRecord, GateEvaluation
from .rules import evidence_gate, final_gate, technical_gate


REVIEWED_EVIDENCE_STATES = {"reviewed", "approved"}


def _reviewed_evidence_by_id(records: Iterable[EvidenceRecord]) -> dict[str, EvidenceRecord]:
    return {
        record.evidence_id: record
        for record in records
        if record.review_status in REVIEWED_EVIDENCE_STATES
    }


def evaluate_gate(
    gate_id: str,
    requirement_level: int,
    claims: Iterable[Claim],
    evidence: Iterable[EvidenceRecord],
) -> GateEvaluation:
    """Evaluate one hard gate using only human-confirmed claims.

    Internal operationalization (INT-03):
    - only reviewed/approved claims affect the gate;
    - capability is the weakest confirmed capability claim for the gate;
    - each capability claim must have at least one reviewed/approved supporting
      EvidenceRecord to contribute evidence trust;
    - the best linked evidence may support a single claim, while the gate trust
      is limited by the weakest supported capability claim;
    - missing claims/evidence remains UNVERIFIED rather than being inferred.
    """

    if requirement_level not in range(0, 5):
        raise ValueError("requirement_level must be between 0 and 4")

    confirmed = [
        claim
        for claim in claims
        if claim.gate_id == gate_id and claim.is_human_confirmed
    ]
    capability_claims = [claim for claim in confirmed if claim.capability_level is not None]
    for claim in capability_claims:
        if claim.capability_level not in range(0, 5):
            raise ValueError(f"capability_level must be 0..4 for claim {claim.claim_id}")

    capability_level = min((claim.capability_level for claim in capability_claims), default=None)
    reviewed_evidence = _reviewed_evidence_by_id(evidence)

    claim_trust: list[int] = []
    linked_evidence_ids: set[str] = set()
    unsupported_claim_ids: list[str] = []
    for claim in capability_claims:
        supporting = [reviewed_evidence[eid] for eid in claim.evidence_ids if eid in reviewed_evidence]
        if not supporting:
            unsupported_claim_ids.append(claim.claim_id)
            continue
        linked_evidence_ids.update(record.evidence_id for record in supporting)
        claim_trust.append(max(record.effective_trust for record in supporting))

    effective_trust = None
    if capability_claims and not unsupported_claim_ids and len(claim_trust) == len(capability_claims):
        effective_trust = min(claim_trust)

    technical_state = technical_gate(requirement_level, capability_level)
    evidence_state = evidence_gate(requirement_level, effective_trust)
    final_state = final_gate(technical_state, evidence_state)

    reasons: list[str] = []
    if requirement_level == 0:
        reasons.append("Gate ist für dieses Assessment nicht erforderlich (Requirement 0).")
    elif not capability_claims:
        reasons.append("Keine human-bestätigte Applied-Capability-Aussage für dieses Gate vorhanden.")
    if unsupported_claim_ids:
        reasons.append(
            "Human-bestätigte Capability-Claims ohne reviewed/approved Evidence: "
            + ", ".join(sorted(unsupported_claim_ids))
        )
    if capability_level is not None:
        reasons.append(f"Applied Capability = {capability_level}, Requirement = {requirement_level}.")
    if effective_trust is not None:
        reasons.append(f"Effective Evidence Trust = {effective_trust}.")
    elif requirement_level > 0:
        reasons.append("Evidence Trust ist nicht ausreichend ableitbar; Gate bleibt evidenzseitig UNVERIFIED.")

    return GateEvaluation(
        gate_id=gate_id,
        requirement_level=requirement_level,
        capability_level=capability_level,
        effective_trust=effective_trust,
        technical_state=technical_state,
        evidence_state=evidence_state,
        final_state=final_state,
        claim_ids=tuple(claim.claim_id for claim in confirmed),
        evidence_ids=tuple(sorted(linked_evidence_ids)),
        reasons=tuple(reasons),
    )
