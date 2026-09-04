#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from sovradar.evidence_coverage import analyze_request_coverage  # noqa: E402
from sovradar.gate_catalog import load_evidence_requests  # noqa: E402
from sovradar.intake import load_evidence_pack  # noqa: E402

PACK = ROOT / "data/templates/evidence-pack-example"
PLAN = ROOT / "data/pilots/next-101/requirement-plan.json"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _json_request(base_url: str, method: str, path: str, payload: Any | None = None) -> Any:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(base_url + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
            return json.loads(body.decode("utf-8")) if body else None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} -> HTTP {exc.code}: {detail}") from exc


def _text_request(base_url: str, path: str) -> str:
    request = urllib.request.Request(base_url + path, headers={"Accept": "text/plain"}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GET {path} -> HTTP {exc.code}: {detail}") from exc


def _multipart_request(base_url: str, path: str, fields: dict[str, str]) -> Any:
    boundary = "----sovradar-next101-" + uuid.uuid4().hex
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )
    chunks.append(f"--{boundary}--\r\n".encode())
    request = urllib.request.Request(
        base_url + path,
        data=b"".join(chunks),
        headers={
            "Accept": "application/json",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"POST {path} -> HTTP {exc.code}: {detail}") from exc


def run(base_url: str, output: Path) -> dict[str, Any]:
    health = _json_request(base_url, "GET", "/api/health")
    _assert(health.get("status") == "ok", f"API health failed: {health}")

    manifest, records = load_evidence_pack(PACK, ROOT / "schemas")
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    catalog = load_evidence_requests(ROOT / "data/method/evidence_request_catalog.csv")
    workload_id = manifest["scope"]["workload_id"]
    coverage = analyze_request_coverage(records, catalog, plan, workload_id=workload_id)

    _assert(coverage["summary"]["verified"] == 3, "unexpected VERIFIED baseline")
    _assert(coverage["summary"]["review_required"] == 4, "unexpected REVIEW_REQUIRED baseline")
    _assert(coverage["summary"]["insufficient"] == 1, "unexpected INSUFFICIENT baseline")
    _assert(coverage["summary"]["missing"] == 3, "unexpected MISSING baseline")

    assessment = _json_request(
        base_url,
        "POST",
        "/api/assessments",
        {
            "name": "NEXT-101 – Customer Evidence Pack Pilot",
            "customer": "Synthetischer Kunde",
            "description": (
                "Providerneutraler Evidence-Pack-Pilot. Alle Daten, Providerbezeichnungen, "
                "Claims und Capability-Level sind synthetische Testannahmen."
            ),
            "workload_type": plan["workload"]["type"],
            "criticality": plan["workload"]["criticality"],
            "confidentiality": "high",
            "integrity": "high",
            "availability": "medium",
            "control_region": plan["workload"]["control_region"],
            "regulatory_context": "Synthetischer Methodenpilot; keine Rechtsfeststellung",
        },
    )
    assessment_id = assessment["id"]

    profile = _json_request(
        base_url,
        "PUT",
        f"/api/assessments/{assessment_id}/profile",
        {
            "service_model": "managed-service",
            "cloud_service": True,
            "contract_in_scope": True,
            "data_processing": True,
            "persistent_data": True,
            "encryption_used": True,
            "key_model": "mixed",
            "ai_used": False,
            "agentic_ai": False,
            "exit_relevant": True,
            "backup_relevant": True,
            "multi_provider": True,
            "subcontractors_used": True,
            "c5_relevant": True,
            "c3a_relevant": False,
            "iam_relevant": True,
            "logging_relevant": True,
            "internet_exposed": False,
        },
    )
    _assert(profile["cloud_service"] is True and profile["ai_used"] is False, "profile not persisted")

    api_evidence_ids: dict[str, str] = {}
    review_results: dict[str, dict[str, Any]] = {}
    for record in records:
        created = _multipart_request(
            base_url,
            f"/api/assessments/{assessment_id}/evidence",
            {
                "title": record.title,
                "evidence_type": record.evidence_type,
                "description": record.notes or "NEXT-101 synthetic Evidence Pack record.",
                "source": f"{record.producer} | {record.source_ref or 'no-source-ref'}",
                "source_date": (record.valid_at or "")[:10],
                "content_excerpt": "",
            },
        )
        api_evidence_ids[record.evidence_id] = created["id"]
        reviewed = _json_request(
            base_url,
            "PUT",
            f"/api/assessments/{assessment_id}/evidence/{created['id']}/review",
            {
                "applied_state": record.applied_state.value,
                "base_trust": record.base_trust,
                "scope_fit": record.scope_fit,
                "freshness_fit": record.freshness_fit,
                "review_status": record.review_status,
            },
        )
        _assert(reviewed["effective_trust"] == record.effective_trust, f"trust drift for {record.evidence_id}")
        review_results[record.evidence_id] = reviewed

    gate_requirements = plan["gate_requirements"]
    current_requirements = {
        item["gate_id"]: item
        for item in _json_request(base_url, "GET", f"/api/assessments/{assessment_id}/gate-requirements")
    }
    governed_change_count = 0
    for gate_id, level in gate_requirements.items():
        current = current_requirements[gate_id]
        if current["requirement_level"] == level:
            continue
        updated = _json_request(
            base_url,
            "PUT",
            f"/api/assessments/{assessment_id}/gate-requirements/{gate_id}",
            {
                "requirement_level": level,
                "reason": "Synthetischer NEXT-101-Pilotplan zur reproduzierbaren Methodenvalidierung.",
            },
        )
        _assert(updated["requirement_level"] == level, f"requirement override failed for {gate_id}")
        _assert(updated["is_override"] is True, f"requirement was not marked as override for {gate_id}")
        governed_change_count += 1
    requirement_audit = _json_request(base_url, "GET", f"/api/assessments/{assessment_id}/gate-requirement-changes")
    _assert(len(requirement_audit) == governed_change_count, "gate requirement changes were not audited")

    created_claims: list[dict[str, Any]] = []
    for claim in plan["human_reviewed_claims"]:
        created_claims.append(
            _json_request(
                base_url,
                "POST",
                f"/api/assessments/{assessment_id}/claims",
                {
                    "gate_id": claim["gate_id"],
                    "statement": claim["statement"],
                    "review_status": claim["review_status"],
                    "capability_level": claim["capability_level"],
                    "evidence_ids": [api_evidence_ids[item] for item in claim["evidence_ids"]],
                    "question_ids": [],
                    "notes": claim["notes"],
                },
            )
        )

    gates = _json_request(base_url, "GET", f"/api/assessments/{assessment_id}/gates")
    gate_states = {item["gate_id"]: item["final_state"] for item in gates}
    expected_gate_states = plan["expected_gate_states"]
    _assert(gate_states == expected_gate_states, f"unexpected gate states: {gate_states}")

    structured_export = _json_request(base_url, "GET", f"/api/assessments/{assessment_id}/export")
    consultant_report = _text_request(base_url, f"/api/assessments/{assessment_id}/report")

    _assert(len(structured_export["evidence"]) == len(records), "export lost evidence metadata")
    _assert(structured_export["export_meta"]["includes_raw_evidence_files"] is False, "default export contains raw evidence")
    _assert(structured_export["export_meta"]["includes_sensitive_evidence_fields"] is False, "default export contains sensitive fields")
    _assert(all("content_excerpt" not in item for item in structured_export["evidence"]), "default export leaked excerpts")
    _assert(len(structured_export["gate_requirement_changes"]) == governed_change_count, "default export lost requirement audit")
    _assert("secure://" not in consultant_report, "consultant report leaked Evidence source locators")
    _assert("HG-01" in consultant_report and "UNVERIFIED" in consultant_report, "report misses gate outcomes")

    er003 = next(item for item in coverage["request_coverage"] if item["request_id"] == "ER-003")
    provider_public = next(item for item in er003["candidates"] if item["evidence_id"] == "EV-005")
    _assert(provider_public["applied_state"] == "available", "public provider state changed")
    _assert(provider_public["sufficient"] is False, "provider capability was promoted to applied capability")

    acceptance_checks = {
        "customer_pack_loaded_without_cloud_credentials": True,
        "five_evidence_classes_preserved": coverage["summary"]["evidence_class_count"] == 5,
        "coverage_exposes_verified_review_insufficient_missing": (
            coverage["summary"]["verified"],
            coverage["summary"]["review_required"],
            coverage["summary"]["insufficient"],
            coverage["summary"]["missing"],
        ) == (3, 4, 1, 3),
        "public_provider_capability_not_promoted": provider_public["sufficient"] is False,
        "only_explicit_human_claims_created": len(created_claims) == len(plan["human_reviewed_claims"]) == 1,
        "gate_requirement_changes_audited": len(requirement_audit) == governed_change_count,
        "gate_states_match_conservative_baseline": gate_states == expected_gate_states,
        "default_export_minimizes_evidence": structured_export["export_meta"]["includes_sensitive_evidence_fields"] is False,
        "consultant_report_omits_source_locators": "secure://" not in consultant_report,
    }
    _assert(all(acceptance_checks.values()), f"acceptance checks failed: {acceptance_checks}")

    report = {
        "validation_id": "NEXT-101-WEBAPP-01",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pilot_id": plan["pilot_id"],
        "assessment_id": assessment_id,
        "source_pack_assessment_id": manifest["assessment_id"],
        "workload_id": workload_id,
        "coverage_summary": coverage["summary"],
        "coverage_gaps": coverage["gaps"],
        "api_evidence_id_map": api_evidence_ids,
        "review_statuses": {key: value["review_status"] for key, value in review_results.items()},
        "explicit_human_claim_count": len(created_claims),
        "gate_requirements": gate_requirements,
        "gate_requirement_change_count": governed_change_count,
        "gate_states": gate_states,
        "export_schema": structured_export["export_meta"]["schema_name"],
        "acceptance_checks": acceptance_checks,
        "interpretation": [
            "Evidence-request coverage is a workflow/sufficiency view and is not itself a Hard-Gate decision.",
            "Only the explicit synthetic human-reviewed claim was allowed to affect a Hard Gate.",
            "Unresolved Evidence Requests remain visible as gaps instead of being converted into invented FAIL/PASS claims.",
            "Provider/service capability evidence remains distinct from applied customer configuration.",
            "Any synthetic deviation from the criticality-based gate requirement default is explicitly reasoned and audited.",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run NEXT-101 Customer Evidence Pack through the live Consultant Webapp API")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080")
    parser.add_argument("--output", default=str(ROOT / ".runtime/exports/next-101-webapp-pilot.json"))
    args = parser.parse_args()
    report = run(args.base_url.rstrip("/"), Path(args.output).resolve())
    print("NEXT-101 Customer Evidence Pack Webapp Pilot PASS")
    print(json.dumps({"coverage": report["coverage_summary"], "gate_states": report["gate_states"]}, ensure_ascii=False, indent=2))
    print(f"Report: {Path(args.output).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
