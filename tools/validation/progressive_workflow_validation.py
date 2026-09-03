#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def request(base_url: str, method: str, path: str, payload: Any | None = None) -> Any:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(base_url + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read()
            return None if not body else json.loads(body.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} -> HTTP {exc.code}: {detail}") from exc


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def create_assessment(base_url: str, *, name: str, workload_type: str, criticality: str, confidentiality: str, integrity: str = "medium", availability: str = "medium") -> dict[str, Any]:
    return request(
        base_url,
        "POST",
        "/api/assessments",
        {
            "name": name,
            "customer": "Synthetischer NEXT-115-Test",
            "description": "Providerneutraler Workflow-Test; sämtliche Merkmale sind synthetische Annahmen.",
            "workload_type": workload_type,
            "criticality": criticality,
            "confidentiality": confidentiality,
            "integrity": integrity,
            "availability": availability,
            "control_region": "EU/EWR",
            "regulatory_context": "Synthetischer Workflow-Test; keine Rechtsfeststellung",
        },
    )


def set_profile(base_url: str, assessment_id: str, profile: dict[str, Any]) -> None:
    response = request(base_url, "PUT", f"/api/assessments/{assessment_id}/profile", profile)
    check(response["assessment_id"] == assessment_id, "profile did not persist")


def complex_profile() -> dict[str, Any]:
    return {
        "service_model": "managed-service",
        "cloud_service": True,
        "contract_in_scope": True,
        "data_processing": True,
        "persistent_data": True,
        "encryption_used": True,
        "key_model": "mixed",
        "ai_used": True,
        "agentic_ai": True,
        "exit_relevant": True,
        "backup_relevant": True,
        "multi_provider": False,
        "subcontractors_used": True,
        "c5_relevant": True,
        "c3a_relevant": True,
        "iam_relevant": True,
        "logging_relevant": True,
        "internet_exposed": True,
    }


def public_profile() -> dict[str, Any]:
    return {
        "service_model": "other",
        "cloud_service": False,
        "contract_in_scope": False,
        "data_processing": False,
        "persistent_data": False,
        "encryption_used": False,
        "key_model": "none",
        "ai_used": False,
        "agentic_ai": False,
        "exit_relevant": False,
        "backup_relevant": False,
        "multi_provider": False,
        "subcontractors_used": False,
        "c5_relevant": False,
        "c3a_relevant": False,
        "iam_relevant": False,
        "logging_relevant": False,
        "internet_exposed": True,
    }


def snapshot(base_url: str, assessment_id: str) -> dict[str, Any]:
    summary = request(base_url, "GET", f"/api/assessments/{assessment_id}/question-workflow")
    all_questions = request(base_url, "GET", f"/api/assessments/{assessment_id}/questions?view=all")
    relevant = request(base_url, "GET", f"/api/assessments/{assessment_id}/questions?view=relevant")
    work = request(base_url, "GET", f"/api/assessments/{assessment_id}/questions?view=work")
    screening = request(base_url, "GET", f"/api/assessments/{assessment_id}/questions?view=screening")
    clarification = request(base_url, "GET", f"/api/assessments/{assessment_id}/questions?view=clarification")
    deep_dive = request(base_url, "GET", f"/api/assessments/{assessment_id}/questions?view=deep_dive")
    completed = request(base_url, "GET", f"/api/assessments/{assessment_id}/questions?view=completed")
    return {
        "summary": summary,
        "all": all_questions,
        "relevant": relevant,
        "work": work,
        "screening": screening,
        "clarification": clarification,
        "deep_dive": deep_dive,
        "completed": completed,
    }


def validate_complex(base_url: str) -> dict[str, Any]:
    assessment = create_assessment(
        base_url,
        name="SYN-NEXT-115 – komplexer KI-Agent",
        workload_type="ai-agent",
        criticality="high",
        confidentiality="high",
        integrity="high",
    )
    assessment_id = assessment["id"]
    set_profile(base_url, assessment_id, complex_profile())
    before = snapshot(base_url, assessment_id)
    summary = before["summary"]

    check(summary["total"] == 128, f"unexpected question total: {summary}")
    check(summary["relevant"] == 124, f"NEXT-114 relevant baseline changed: {summary}")
    check(summary["applicability"]["applicable"] == 83, f"applicable baseline changed: {summary}")
    check(summary["applicability"]["needs_review"] == 41, f"needs_review baseline changed: {summary}")
    check(summary["applicability"]["not_applicable"] == 4, f"not_applicable baseline changed: {summary}")
    check(summary["stages"]["clarification"] == 41, "needs_review is not fully represented in clarification queue")
    check(summary["stages"]["screening"] > 0, "screening queue is empty")
    check(summary["stages"]["deep_dive"] > 0, "deep-dive queue is empty")
    check(summary["work_queue"] < summary["relevant"], "progressive work queue does not reduce immediate workload")
    check(len(before["work"]) == summary["work_queue"], "work view and summary disagree")
    check(len(before["clarification"]) == 41, "clarification view lost unresolved questions")
    check(all(q["applicability_status"] == "needs_review" for q in before["clarification"]), "clarification view contains non-needs_review questions")
    check(len(before["all"]) == 128, "all-questions audit view is incomplete")

    first_screening = before["screening"][0]
    saved = request(
        base_url,
        "PUT",
        f"/api/assessments/{assessment_id}/answers/{first_screening['id']}",
        {
            "question_id": first_screening["id"],
            "answer_value": "fulfilled",
            "comment": "NEXT-115 Workflow-Regressionscheck",
            "evidence_ids": [],
            "review_state": "reviewed",
        },
    )
    check(saved["question_id"] == first_screening["id"], "screening answer did not persist")
    after = snapshot(base_url, assessment_id)
    after_summary = after["summary"]
    check(after_summary["stages"]["completed"] == summary["stages"]["completed"] + 1, "answered question did not move to completed")
    check(after_summary["stages"]["screening"] == summary["stages"]["screening"] - 1, "answered screening question did not leave screening queue")
    check(any(q["id"] == first_screening["id"] for q in after["completed"]), "completed view does not expose answered question")
    check(len(after["all"]) == 128, "answering a question removed it from audit view")

    return {
        "assessment_id": assessment_id,
        "before": summary,
        "after": after_summary,
        "answered_screening_question": first_screening["id"],
    }


def validate_public(base_url: str) -> dict[str, Any]:
    assessment = create_assessment(
        base_url,
        name="SYN-NEXT-115 – öffentliche Inhaltswebsite",
        workload_type="application",
        criticality="medium",
        confidentiality="low",
    )
    assessment_id = assessment["id"]
    set_profile(base_url, assessment_id, public_profile())
    current = snapshot(base_url, assessment_id)
    summary = current["summary"]
    check(summary["total"] == 128, "public audit view does not contain complete method bank")
    check(len(current["all"]) == 128, "public all-question view incomplete")
    return {"assessment_id": assessment_id, "summary": summary}


def run(base_url: str, output: Path) -> dict[str, Any]:
    health = request(base_url, "GET", "/api/health")
    check(health["status"] == "ok", f"API not healthy: {health}")

    complex_result = validate_complex(base_url)
    public_result = validate_public(base_url)
    complex_summary = complex_result["before"]
    public_summary = public_result["summary"]

    check(public_summary["relevant"] < complex_summary["relevant"], "simple public workload is not shorter than complex AI workload")
    check(public_summary["work_queue"] < complex_summary["work_queue"], "public immediate work queue is not shorter than complex AI queue")

    report = {
        "validation_id": "NEXT-115-PROGRESSIVE-01",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy": complex_summary["policy"],
        "complex_ai_agent": complex_result,
        "public_content": public_result,
        "acceptance_checks": {
            "all_questions_remain_inspectable": complex_summary["total"] == 128 and public_summary["total"] == 128,
            "next_114_applicability_baseline_preserved": complex_summary["relevant"] == 124 and complex_summary["applicability"]["needs_review"] == 41,
            "needs_review_visible_in_clarification": complex_summary["stages"]["clarification"] == 41,
            "immediate_queue_smaller_than_relevant_path": complex_summary["work_queue"] < complex_summary["relevant"],
            "screening_and_deep_dive_exist": complex_summary["stages"]["screening"] > 0 and complex_summary["stages"]["deep_dive"] > 0,
            "answered_question_moves_to_completed": complex_result["after"]["stages"]["completed"] == complex_summary["stages"]["completed"] + 1,
            "public_workload_is_shorter": public_summary["work_queue"] < complex_summary["work_queue"],
        },
    }
    check(all(report["acceptance_checks"].values()), f"acceptance failure: {report['acceptance_checks']}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate NEXT-115 progressive question workflow against a running Radar instance.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080")
    parser.add_argument("--output", default=".runtime/exports/progressive-workflow-validation.json")
    args = parser.parse_args()
    try:
        report = run(args.base_url.rstrip("/"), Path(args.output))
    except Exception as exc:  # noqa: BLE001 - validation runner must expose complete failures
        print(f"NEXT-115 progressive workflow FAILED: {exc}", file=sys.stderr)
        return 1
    print("NEXT-115 progressive workflow PASS")
    print(json.dumps(report["acceptance_checks"], indent=2, ensure_ascii=False))
    print("Complex stage counts:", json.dumps(report["complex_ai_agent"]["before"]["stages"], sort_keys=True))
    print("Public stage counts:", json.dumps(report["public_content"]["summary"]["stages"], sort_keys=True))
    print("Report:", args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
