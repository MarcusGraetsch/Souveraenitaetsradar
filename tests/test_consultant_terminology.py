from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "data" / "method" / "r4_hard_gates.csv"
REQUESTS = ROOT / "data" / "method" / "evidence_request_catalog.csv"
UI = ROOT / "apps" / "web" / "src" / "consultantTerminology.ts"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def test_all_hard_gates_have_consultant_facing_labels() -> None:
    source = UI.read_text(encoding="utf-8")
    gate_ids = {row["Gate-ID"] for row in _rows(GATES)}
    assert gate_ids == {f"HG-{index:02d}" for index in range(1, 9)}
    missing = sorted(gate_id for gate_id in gate_ids if f"'{gate_id}'" not in source)
    assert not missing, f"missing consultant terminology for gates: {missing}"


def test_all_gate_evidence_requests_have_consultant_facing_labels() -> None:
    source = UI.read_text(encoding="utf-8")
    request_ids = {
        row["Request-ID"]
        for row in _rows(REQUESTS)
        if row["Gate-ID"].startswith("HG-")
    }
    assert request_ids == {f"ER-{index:03d}" for index in range(1, 13)}
    missing = sorted(request_id for request_id in request_ids if f"'{request_id}'" not in source)
    assert not missing, f"missing consultant terminology for evidence requests: {missing}"


def test_internal_gate_and_review_values_remain_visible_only_as_mapping_keys() -> None:
    source = UI.read_text(encoding="utf-8")
    for internal_value in ("PASS", "FAIL", "UNVERIFIED", "N/A", "draft", "reviewed", "approved", "rejected"):
        assert internal_value in source
    for consultant_label in (
        "Mindestanforderung erfüllt",
        "Mindestanforderung nicht erfüllt",
        "nicht ausreichend belegt",
        "Geprüfte Feststellungen",
        "Belegstärke",
    ):
        assert consultant_label in source or consultant_label in (ROOT / "apps" / "web" / "src" / "App.tsx").read_text(encoding="utf-8")
