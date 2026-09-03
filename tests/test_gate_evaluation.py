from sovradar.gate_evaluation import evaluate_gate
from sovradar.models import AppliedState, Claim, EvidenceRecord


def ev(evidence_id: str, trust: int, review_status: str = "reviewed") -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id=evidence_id,
        evidence_type="test_report",
        title=evidence_id,
        producer="test",
        scope={"workload_id": "w"},
        applied_state=AppliedState.TESTED,
        base_trust=trust,
        scope_fit=trust,
        freshness_fit=trust,
        sensitivity="internal",
        review_status=review_status,
    )


def claim(claim_id: str, level: int | None, evidence_ids=(), review_status="reviewed") -> Claim:
    return Claim(
        claim_id=claim_id,
        gate_id="HG-04",
        statement="Exit capability",
        review_status=review_status,
        capability_level=level,
        evidence_ids=tuple(evidence_ids),
    )


def test_gate_pass_requires_capability_and_sufficient_reviewed_evidence():
    result = evaluate_gate("HG-04", 2, [claim("C1", 2, ["EV1"])], [ev("EV1", 4)])
    assert result.technical_state == "PASS"
    assert result.evidence_state == "VERIFIED"
    assert result.final_state == "PASS"


def test_technical_shortfall_is_fail_even_with_strong_evidence():
    result = evaluate_gate("HG-04", 3, [claim("C1", 2, ["EV1"])], [ev("EV1", 5)])
    assert result.technical_state == "FAIL"
    assert result.final_state == "FAIL"


def test_missing_evidence_keeps_gate_unverified():
    result = evaluate_gate("HG-04", 2, [claim("C1", 3, [])], [])
    assert result.technical_state == "PASS"
    assert result.evidence_state == "UNVERIFIED"
    assert result.final_state == "UNVERIFIED"


def test_unreviewed_claim_never_changes_gate():
    result = evaluate_gate("HG-04", 2, [claim("C1", 4, ["EV1"], review_status="draft")], [ev("EV1", 5)])
    assert result.capability_level is None
    assert result.final_state == "UNVERIFIED"


def test_unreviewed_evidence_does_not_verify_claim():
    result = evaluate_gate("HG-04", 2, [claim("C1", 4, ["EV1"])], [ev("EV1", 5, review_status="raw")])
    assert result.technical_state == "PASS"
    assert result.evidence_state == "UNVERIFIED"
    assert result.final_state == "UNVERIFIED"


def test_weakest_confirmed_capability_and_claim_trust_limit_gate():
    claims = [claim("C1", 4, ["EV1"]), claim("C2", 2, ["EV2"])]
    evidence = [ev("EV1", 5), ev("EV2", 3)]
    result = evaluate_gate("HG-04", 2, claims, evidence)
    assert result.capability_level == 2
    assert result.effective_trust == 3
    assert result.final_state == "PASS"


def test_requirement_zero_is_not_applicable():
    result = evaluate_gate("HG-04", 0, [], [])
    assert result.final_state == "N/A"
