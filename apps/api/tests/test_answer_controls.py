from __future__ import annotations

import csv
from pathlib import Path

from apps.api.app.answer_controls import answer_control_for


REPO_ROOT = Path(__file__).resolve().parents[3]
QUESTION_BANK = REPO_ROOT / "data" / "method" / "question_bank"


def test_all_method_answer_types_have_explicit_control_mapping() -> None:
    unresolved: list[str] = []
    total = 0
    for path in sorted(QUESTION_BANK.glob("*.csv")):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle, delimiter=";"):
                if not row.get("QID"):
                    continue
                total += 1
                control = answer_control_for(row.get("Antworttyp", ""))
                if control["mapping_status"] != "mapped":
                    unresolved.append(
                        f"{row['QID']}={row.get('Antworttyp', '')!r} ({path.name})"
                    )

    assert total == 128
    assert not unresolved, "Unmapped method answer types:\n" + "\n".join(unresolved)


def test_scope_fact_questions_use_fact_controls_not_compliance_status() -> None:
    rows: dict[str, dict[str, str]] = {}
    path = QUESTION_BANK / "scope-kritikalitaet.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter=";"):
            rows[row["QID"]] = row

    sc01 = answer_control_for(rows["SC-01"]["Antworttyp"])
    sc02 = answer_control_for(rows["SC-02"]["Antworttyp"])
    assert sc01["kind"] == "text"
    assert sc02["kind"] == "list"
    assert not sc01["options"]
    assert not sc02["options"]


def test_common_control_types_are_deterministic() -> None:
    assert answer_control_for("Boolean")["kind"] == "single_select"
    assert [item["value"] for item in answer_control_for("Boolean")["options"]] == [
        "yes",
        "no",
        "unknown",
    ]
    assert [item["value"] for item in answer_control_for("Enum 1-5")["options"]] == [
        "1",
        "2",
        "3",
        "4",
        "5",
        "unknown",
    ]
    assert [item["value"] for item in answer_control_for("Enum Kunde/Provider/Dritter")["options"]][:-1] == [
        "Kunde",
        "Provider",
        "Dritter",
    ]
