import pytest

from sovradar.rules import effective_trust, evidence_gate, final_gate, structural_risk_class, technical_gate


def test_effective_trust_uses_floor():
    assert effective_trust(4, 2, 5) == 2


def test_gate_equal_requirement_passes():
    assert technical_gate(3, 3) == "PASS"


def test_gate_missing_capability_is_unverified():
    assert technical_gate(3, None) == "UNVERIFIED"


def test_evidence_requirement_three_needs_trust_four():
    assert evidence_gate(3, 3) == "UNVERIFIED"
    assert evidence_gate(3, 4) == "VERIFIED"


def test_fail_beats_missing_evidence():
    assert final_gate("FAIL", "UNVERIFIED") == "FAIL"


def test_unverified_is_preserved():
    assert final_gate("PASS", "UNVERIFIED") == "UNVERIFIED"

@pytest.mark.parametrize(("exposure", "impact", "expected"),[(1,1,"low"),(2,2,"medium"),(3,3,"high"),(4,4,"very_high")])
def test_structural_risk_class(exposure, impact, expected):
    assert structural_risk_class(exposure, impact) == expected
