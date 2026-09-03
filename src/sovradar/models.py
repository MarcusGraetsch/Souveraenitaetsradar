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
