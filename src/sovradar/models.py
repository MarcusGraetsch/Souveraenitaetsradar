from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AppliedState(str, Enum):
    ASSERTED = "asserted"
    AVAILABLE = "available"
    DOCUMENTED = "documented"
    OBSERVED = "observed"
    CONFIGURED = "configured"
    TESTED = "tested"
    ATTESTED = "attested"


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    evidence_type: str
    title: str
    producer: str
    scope: dict[str, Any]
    applied_state: AppliedState
    base_trust: int
    scope_fit: int
    freshness_fit: int
    sensitivity: str
    review_status: str
    claim_ids: tuple[str, ...] = field(default_factory=tuple)
    gate_ids: tuple[str, ...] = field(default_factory=tuple)
    source_ref: str | None = None
    attachment_ref: str | None = None
    locator: str | None = None
    valid_at: str | None = None
    version: str | None = None
    notes: str | None = None

    @property
    def effective_trust(self) -> int:
        return min(self.base_trust, self.scope_fit, self.freshness_fit)


@dataclass(frozen=True)
class GenericFact:
    fact_type: str
    subject_id: str
    value: Any
    evidence_id: str
    confidence: int
    provider: str | None = None
    source_locator: str | None = None


@dataclass(frozen=True)
class Claim:
    """Human-reviewed statement used by deterministic gate evaluation.

    `capability_level` is the Radar's internal 0..4 applied-capability level for
    the claim scope. A claim without a capability level can still document a
    fact, but it cannot by itself turn a gate PASS or FAIL.
    """

    claim_id: str
    gate_id: str
    statement: str
    review_status: str
    capability_level: int | None = None
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    question_ids: tuple[str, ...] = field(default_factory=tuple)
    notes: str | None = None

    @property
    def is_human_confirmed(self) -> bool:
        return self.review_status in {"reviewed", "approved"}


@dataclass(frozen=True)
class GateDefinition:
    gate_id: str
    name: str
    subject: str
    requirements: dict[str, int]
    source_ids: tuple[str, ...] = field(default_factory=tuple)
    provenance: str = ""


@dataclass(frozen=True)
class EvidenceRequest:
    request_id: str
    gate_id: str
    claim_area: str
    acceptable_evidence: str
    required_for: str
    follow_up: str
    preferred_applied_state: str
    typical_min_trust: str
    provenance: str


@dataclass(frozen=True)
class GateEvaluation:
    gate_id: str
    requirement_level: int
    capability_level: int | None
    effective_trust: int | None
    technical_state: str
    evidence_state: str
    final_state: str
    claim_ids: tuple[str, ...] = field(default_factory=tuple)
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    reasons: tuple[str, ...] = field(default_factory=tuple)
