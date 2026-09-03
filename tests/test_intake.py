from pathlib import Path

import pytest

from sovradar.intake import EvidencePackError, evidence_for_gate, load_evidence_pack

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
EXAMPLE = ROOT / "data" / "templates" / "evidence-pack-example"


def test_example_pack_loads():
    manifest, records = load_evidence_pack(EXAMPLE, SCHEMAS)
    assert manifest["schema_version"] == "1.0"
    assert len(records) >= 4
    assert any(r.effective_trust >= 2 for r in records)


def test_gate_filter():
    _, records = load_evidence_pack(EXAMPLE, SCHEMAS)
    assert evidence_for_gate(records, "HG-04")


def test_pack_rejects_path_traversal(tmp_path):
    (tmp_path / "manifest.json").write_text("""{
      "schema_version":"1.0","assessment_id":"x","created_at":"2026-09-03T10:00:00Z",
      "producer":{"organization":"x","role":"x"},"scope":{"workload_id":"w"},
      "evidence_files":["evidence/../../outside.json"],"redaction_statement":"none"
    }""", encoding="utf-8")
    with pytest.raises(EvidencePackError):
        load_evidence_pack(tmp_path, SCHEMAS)
