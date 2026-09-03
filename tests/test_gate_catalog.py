from pathlib import Path

from sovradar.gate_catalog import (
    evidence_requests_by_gate,
    load_evidence_requests,
    load_hard_gates,
    validate_gate_evidence_mapping,
)

ROOT = Path(__file__).resolve().parents[1]


def test_all_eight_hard_gates_have_provider_neutral_evidence_requests():
    gates = load_hard_gates(ROOT / "data" / "method" / "r4_hard_gates.csv")
    requests = load_evidence_requests(ROOT / "data" / "method" / "evidence_request_catalog.csv")
    validate_gate_evidence_mapping(gates, requests)

    assert [gate.gate_id for gate in gates] == [f"HG-{i:02d}" for i in range(1, 9)]
    grouped = evidence_requests_by_gate(requests)
    for gate in gates:
        assert grouped[gate.gate_id]
        assert gate.name
        assert all(0 <= level <= 4 for level in gate.requirements.values())


def test_gate_catalog_exposes_requirement_templates_and_provenance():
    gates = load_hard_gates(ROOT / "data" / "method" / "r4_hard_gates.csv")
    exit_gate = next(gate for gate in gates if gate.gate_id == "HG-04")
    assert exit_gate.requirements["basis"] == 1
    assert exit_gate.requirements["critical"] == 3
    assert "INT-01" in exit_gate.source_ids
    assert exit_gate.provenance
