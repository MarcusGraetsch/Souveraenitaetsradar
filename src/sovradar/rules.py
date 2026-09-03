from __future__ import annotations

from typing import Literal

TechnicalState = Literal["PASS", "FAIL", "UNVERIFIED", "N/A"]
EvidenceState = Literal["VERIFIED", "UNVERIFIED", "N/A"]
FinalState = Literal["PASS", "FAIL", "UNVERIFIED", "N/A"]


def effective_trust(base_trust: int, scope_fit: int, freshness_fit: int = 5) -> int:
    """Internal R5/R6 rule: evidence strength is limited by its weakest fit dimension."""
    vals = (base_trust, scope_fit, freshness_fit)
    if any(v < 0 or v > 5 for v in vals):
        raise ValueError("trust dimensions must be between 0 and 5")
    return min(vals)


def required_trust(requirement: int) -> int:
    """Internal configurable defaults from R4; not an external regulatory threshold."""
    mapping = {0: 0, 1: 2, 2: 3, 3: 4, 4: 4}
    try:
        return mapping[requirement]
    except KeyError as exc:
        raise ValueError("requirement must be between 0 and 4") from exc


def technical_gate(requirement: int, capability: int | None) -> TechnicalState:
    if requirement == 0:
        return "N/A"
    if capability is None:
        return "UNVERIFIED"
    if not 0 <= capability <= 4:
        raise ValueError("capability must be between 0 and 4")
    return "PASS" if capability >= requirement else "FAIL"


def evidence_gate(requirement: int, trust: int | None) -> EvidenceState:
    if requirement == 0:
        return "N/A"
    if trust is None:
        return "UNVERIFIED"
    return "VERIFIED" if trust >= required_trust(requirement) else "UNVERIFIED"


def final_gate(technical: TechnicalState, evidence: EvidenceState) -> FinalState:
    if technical == "N/A":
        return "N/A"
    if technical == "FAIL":
        return "FAIL"
    if technical == "UNVERIFIED" or evidence == "UNVERIFIED":
        return "UNVERIFIED"
    if technical == "PASS" and evidence == "VERIFIED":
        return "PASS"
    raise ValueError(f"invalid state combination: {technical=}, {evidence=}")


def structural_risk_class(exposure: int, impact: int) -> str:
    """Internal R4 matrix for persistent structural exposure; trigger is documented separately."""
    if exposure not in range(1, 5) or impact not in range(1, 5):
        raise ValueError("exposure and impact must be 1..4")
    score = exposure * impact
    if score <= 3:
        return "low"
    if score <= 6:
        return "medium"
    if score <= 11:
        return "high"
    return "very_high"
