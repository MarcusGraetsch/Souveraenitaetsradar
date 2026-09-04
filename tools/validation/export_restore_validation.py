#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import sys
import urllib.error
import urllib.request
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RAW_SENTINEL = "RAW-EVIDENCE-SECRET-SENTINEL"
EXCERPT_SENTINEL = "EXCERPT-SECRET-SENTINEL"


def request_bytes(
    base_url: str,
    method: str,
    path: str,
    payload: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[bytes, dict[str, str]]:
    request = urllib.request.Request(
        base_url + path,
        data=payload,
        headers={"Accept": "*/*", **(headers or {})},
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read(), {k.lower(): v for k, v in response.headers.items()}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} -> HTTP {exc.code}: {detail}") from exc


def request_json(base_url: str, method: str, path: str, payload: Any | None = None) -> Any:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    body, _ = request_bytes(base_url, method, path, data, headers)
    return None if not body else json.loads(body.decode("utf-8"))


def multipart_body(
    fields: dict[str, str],
    *,
    file_field: str | None = None,
    file_name: str = "",
    file_bytes: bytes = b"",
    file_type: str = "application/octet-stream",
) -> tuple[bytes, str]:
    boundary = "----sovradar-" + uuid.uuid4().hex
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
    if file_field:
        safe_name = Path(file_name).name
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                (
                    f'Content-Disposition: form-data; name="{file_field}"; '
                    f'filename="{safe_name}"\r\n'
                ).encode(),
                f"Content-Type: {file_type}\r\n\r\n".encode(),
                file_bytes,
                b"\r\n",
            ]
        )
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def request_multipart_json(
    base_url: str,
    path: str,
    fields: dict[str, str],
    *,
    file_field: str | None = None,
    file_name: str = "",
    file_bytes: bytes = b"",
    file_type: str = "application/octet-stream",
) -> Any:
    body, content_type = multipart_body(
        fields,
        file_field=file_field,
        file_name=file_name,
        file_bytes=file_bytes,
        file_type=file_type,
    )
    raw, _ = request_bytes(
        base_url,
        "POST",
        path,
        body,
        {"Content-Type": content_type, "Accept": "application/json"},
    )
    return json.loads(raw.decode("utf-8"))


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def zip_content(data: bytes) -> dict[str, bytes]:
    with zipfile.ZipFile(io.BytesIO(data), "r") as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def gate_states(base_url: str, assessment_id: str) -> dict[str, str]:
    return {
        item["gate_id"]: item["final_state"]
        for item in request_json(base_url, "GET", f"/api/assessments/{assessment_id}/gates")
    }


def create_fixture(base_url: str) -> dict[str, Any]:
    assessment = request_json(
        base_url,
        "POST",
        "/api/assessments",
        {
            "name": "SYN-NEXT-113 – Export Restore Pilot",
            "customer": "Synthetischer Kunde",
            "description": "Providerneutraler Export-/Restore-Test; keine Providerfakten.",
            "workload_type": "ai-agent",
            "criticality": "high",
            "confidentiality": "high",
            "integrity": "high",
            "availability": "medium",
            "control_region": "EU/EWR",
            "regulatory_context": "Synthetischer Test; keine Rechtsfeststellung",
        },
    )
    assessment_id = assessment["id"]

    evidence = request_multipart_json(
        base_url,
        f"/api/assessments/{assessment_id}/evidence",
        {
            "title": "Synthetische Evidence mit Datei",
            "evidence_type": "contract",
            "description": "NEXT-113 Testnachweis",
            "source": "NEXT-113 fixture",
            "source_date": "2026-09-03",
            "content_excerpt": EXCERPT_SENTINEL,
        },
        file_field="file",
        file_name="sensitive-evidence.txt",
        file_bytes=RAW_SENTINEL.encode("utf-8"),
        file_type="text/plain",
    )
    evidence_id = evidence["id"]
    review = request_json(
        base_url,
        "PUT",
        f"/api/assessments/{assessment_id}/evidence/{evidence_id}/review",
        {
            "applied_state": "documented",
            "base_trust": 4,
            "scope_fit": 4,
            "freshness_fit": 4,
            "review_status": "reviewed",
        },
    )
    check(review["effective_trust"] == 4, "Evidence review did not persist")

    requirements = {
        "HG-01": 2,
        "HG-02": 0,
        "HG-03": 3,
        "HG-04": 3,
        "HG-05": 0,
        "HG-06": 0,
        "HG-07": 0,
        "HG-08": 0,
    }
    current_requirements = {
        item["gate_id"]: item
        for item in request_json(base_url, "GET", f"/api/assessments/{assessment_id}/gate-requirements")
    }
    requirement_change_count = 0
    for gate_id, level in requirements.items():
        current = current_requirements[gate_id]
        if current["requirement_level"] == level:
            continue
        stored = request_json(
            base_url,
            "PUT",
            f"/api/assessments/{assessment_id}/gate-requirements/{gate_id}",
            {
                "requirement_level": level,
                "reason": "Synthetischer Export-/Restore-Validierungsplan für reproduzierbare Gate-Zustände.",
            },
        )
        check(stored["source"] == "consultant-override", f"Override provenance missing for {gate_id}")
        requirement_change_count += 1
    requirement_audit = request_json(base_url, "GET", f"/api/assessments/{assessment_id}/gate-requirement-changes")
    check(len(requirement_audit) == requirement_change_count, "Requirement audit count mismatch")

    claims = [
        {
            "gate_id": "HG-01",
            "statement": "Synthetisch: Jurisdiktion/Control erreicht Capability 3.",
            "review_status": "reviewed",
            "capability_level": 3,
            "evidence_ids": [evidence_id],
            "question_ids": [],
            "notes": "Expected PASS",
        },
        {
            "gate_id": "HG-03",
            "statement": "Synthetisch: Key Control erreicht nur Capability 1.",
            "review_status": "reviewed",
            "capability_level": 1,
            "evidence_ids": [evidence_id],
            "question_ids": [],
            "notes": "Expected FAIL",
        },
        {
            "gate_id": "HG-04",
            "statement": "Synthetisch: Exit Capability 3, aber ohne reviewed Evidence.",
            "review_status": "reviewed",
            "capability_level": 3,
            "evidence_ids": [],
            "question_ids": [],
            "notes": "Expected UNVERIFIED",
        },
    ]
    for claim in claims:
        request_json(base_url, "POST", f"/api/assessments/{assessment_id}/claims", claim)

    states = gate_states(base_url, assessment_id)
    check(states["HG-01"] == "PASS", f"HG-01 expected PASS: {states}")
    check(states["HG-03"] == "FAIL", f"HG-03 expected FAIL: {states}")
    check(states["HG-04"] == "UNVERIFIED", f"HG-04 expected UNVERIFIED: {states}")
    return {
        "assessment_id": assessment_id,
        "evidence_id": evidence_id,
        "gate_states": states,
        "gate_requirement_change_count": requirement_change_count,
    }


def run(base_url: str, output: Path) -> dict[str, Any]:
    health = request_json(base_url, "GET", "/api/health")
    check(health["status"] == "ok", f"API unhealthy: {health}")
    fixture = create_fixture(base_url)
    assessment_id = fixture["assessment_id"]
    evidence_id = fixture["evidence_id"]
    states_before = fixture["gate_states"]
    requirement_change_count = fixture["gate_requirement_change_count"]

    structured = request_json(base_url, "GET", f"/api/assessments/{assessment_id}/export")
    serialized = json.dumps(structured, ensure_ascii=False)
    check(structured["export_meta"]["schema_name"] == "sovradar.assessment-export", "wrong export schema")
    check(structured["export_meta"]["schema_version"] == "1.0", "wrong export schema version")
    check(structured["export_meta"]["includes_raw_evidence_files"] is False, "structured export claims raw evidence")
    check(structured["export_meta"]["includes_sensitive_evidence_fields"] is False, "default export exposed sensitive fields")
    check(EXCERPT_SENTINEL not in serialized, "default export leaked Evidence excerpt")
    check(RAW_SENTINEL not in serialized, "default export leaked raw file content")
    check(structured["evidence"][0]["has_file"] is True, "export lost file-presence metadata")
    check(len(structured["gate_requirement_changes"]) == requirement_change_count, "export lost gate requirement audit history")

    report_bytes, report_headers = request_bytes(base_url, "GET", f"/api/assessments/{assessment_id}/report")
    report = report_bytes.decode("utf-8")
    check("text/markdown" in report_headers.get("content-type", ""), "report has wrong media type")
    check("HG-01" in report and "HG-03" in report and "HG-04" in report, "report misses gates")
    check("Mindeststufen-Audit" in report, "report misses gate requirement governance audit")
    check(EXCERPT_SENTINEL not in report, "report leaked Evidence excerpt")
    check(RAW_SENTINEL not in report, "report leaked raw file content")

    structured_zip, structured_headers = request_bytes(
        base_url,
        "GET",
        f"/api/assessments/{assessment_id}/backup",
    )
    check(structured_headers.get("x-sovradar-includes-evidence") == "false", "default backup did not declare evidence=false")
    structured_files = zip_content(structured_zip)
    check(not any(name.startswith("evidence/") for name in structured_files), "default backup contains raw Evidence")
    check(EXCERPT_SENTINEL not in structured_files["assessment.json"].decode("utf-8"), "default backup leaked excerpt")
    check(RAW_SENTINEL.encode("utf-8") not in b"".join(structured_files.values()), "default backup leaked raw content")

    full_zip, full_headers = request_bytes(
        base_url,
        "GET",
        f"/api/assessments/{assessment_id}/backup?include_evidence=true",
    )
    check(full_headers.get("x-sovradar-includes-evidence") == "true", "full backup did not declare evidence=true")
    full_files = zip_content(full_zip)
    raw_paths = [name for name in full_files if name.startswith(f"evidence/{evidence_id}/")]
    check(len(raw_paths) == 1, f"full backup missing expected raw Evidence: {list(full_files)}")
    check(full_files[raw_paths[0]] == RAW_SENTINEL.encode("utf-8"), "full backup changed raw Evidence content")
    check(EXCERPT_SENTINEL in full_files["assessment.json"].decode("utf-8"), "explicit full backup omitted approved excerpt")
    check(EXCERPT_SENTINEL not in full_files["consultant-report.md"].decode("utf-8"), "report inside full backup leaked excerpt")

    structured_restore = request_json(base_url, "POST", "/api/assessments/import", structured)
    structured_restored_id = structured_restore["assessment_id"]
    check(structured_restored_id != assessment_id, "structured restore overwrote source Assessment")
    check(structured_restore["gate_semantic_drift"] is False, f"structured restore gate drift: {structured_restore}")
    check(structured_restore["restored_gate_requirement_change_count"] == requirement_change_count, "structured restore lost requirement audit")
    check(evidence_id in structured_restore["missing_raw_file_source_evidence_ids"], "missing raw file was not reported")
    check(gate_states(base_url, structured_restored_id) == states_before, "structured restore changed gate states")
    structured_restored_export = request_json(base_url, "GET", f"/api/assessments/{structured_restored_id}/export")
    check(structured_restored_export["evidence"][0]["has_file"] is False, "structured restore invented raw file")
    check(len(structured_restored_export["gate_requirement_changes"]) == requirement_change_count, "structured restore export lost requirement audit")
    check(bool(structured_restored_export["warnings"]), "structured restore did not expose missing file warning")

    full_restore = request_multipart_json(
        base_url,
        "/api/assessments/import-backup",
        {},
        file_field="file",
        file_name="sovradar-full-backup.zip",
        file_bytes=full_zip,
        file_type="application/zip",
    )
    full_restored_id = full_restore["assessment_id"]
    check(full_restored_id not in {assessment_id, structured_restored_id}, "full restore reused an existing Assessment ID")
    check(full_restore["gate_semantic_drift"] is False, f"full restore gate drift: {full_restore}")
    check(full_restore["restored_gate_requirement_change_count"] == requirement_change_count, "full restore lost requirement audit")
    check(len(full_restore["restored_raw_evidence_ids"]) == 1, "full restore did not restore raw Evidence")
    check(full_restore["missing_raw_file_source_evidence_ids"] == [], "full restore still reports raw Evidence missing")
    check(gate_states(base_url, full_restored_id) == states_before, "full restore changed gate states")
    full_restored_export = request_json(base_url, "GET", f"/api/assessments/{full_restored_id}/export")
    check(full_restored_export["evidence"][0]["has_file"] is True, "full restore lost raw file presence")
    check(len(full_restored_export["gate_requirement_changes"]) == requirement_change_count, "full restore export lost requirement audit")

    states_after = gate_states(base_url, assessment_id)
    check(states_after == states_before, "export/report/restore operations mutated source gate states")

    checks = {
        "default_export_omits_sensitive_evidence": EXCERPT_SENTINEL not in serialized and RAW_SENTINEL not in serialized,
        "consultant_report_omits_sensitive_evidence": EXCERPT_SENTINEL not in report and RAW_SENTINEL not in report,
        "gate_requirement_audit_exported": len(structured["gate_requirement_changes"]) == requirement_change_count,
        "default_backup_has_no_raw_evidence": not any(name.startswith("evidence/") for name in structured_files),
        "full_backup_requires_explicit_opt_in": full_headers.get("x-sovradar-includes-evidence") == "true" and len(raw_paths) == 1,
        "structured_restore_uses_new_assessment": structured_restored_id != assessment_id,
        "structured_restore_preserves_gate_semantics": structured_restore["gate_semantic_drift"] is False,
        "structured_restore_preserves_requirement_audit": structured_restore["restored_gate_requirement_change_count"] == requirement_change_count,
        "structured_restore_reports_missing_raw_file": evidence_id in structured_restore["missing_raw_file_source_evidence_ids"],
        "full_restore_restores_raw_file": len(full_restore["restored_raw_evidence_ids"]) == 1,
        "full_restore_preserves_gate_semantics": full_restore["gate_semantic_drift"] is False,
        "full_restore_preserves_requirement_audit": full_restore["restored_gate_requirement_change_count"] == requirement_change_count,
        "source_gate_states_unchanged": states_after == states_before,
    }
    check(all(checks.values()), f"acceptance failure: {checks}")

    result = {
        "validation_id": "NEXT-113-EXPORT-RESTORE-01",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_assessment_id": assessment_id,
        "structured_restored_assessment_id": structured_restored_id,
        "full_restored_assessment_id": full_restored_id,
        "source_gate_states": states_before,
        "gate_requirement_change_count": requirement_change_count,
        "schema": {
            "name": structured["export_meta"]["schema_name"],
            "version": structured["export_meta"]["schema_version"],
        },
        "backup": {
            "structured_entries": sorted(structured_files),
            "full_entries": sorted(full_files),
            "raw_evidence_count": len(raw_paths),
        },
        "structured_restore": {
            "gate_semantic_drift": structured_restore["gate_semantic_drift"],
            "restored_gate_requirement_change_count": structured_restore["restored_gate_requirement_change_count"],
            "missing_raw_file_source_evidence_ids": structured_restore["missing_raw_file_source_evidence_ids"],
        },
        "full_restore": {
            "gate_semantic_drift": full_restore["gate_semantic_drift"],
            "restored_gate_requirement_change_count": full_restore["restored_gate_requirement_change_count"],
            "restored_raw_evidence_count": len(full_restore["restored_raw_evidence_ids"]),
        },
        "acceptance_checks": checks,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate NEXT-113 export, backup, restore and Consultant Report against a running Radar instance.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080")
    parser.add_argument("--output", default=".runtime/exports/export-restore-validation.json")
    args = parser.parse_args()
    try:
        result = run(args.base_url.rstrip("/"), Path(args.output))
    except Exception as exc:  # noqa: BLE001 - validation runner must expose complete failure
        print(f"NEXT-113 export/restore validation FAILED: {exc}", file=sys.stderr)
        return 1
    print("NEXT-113 export/restore validation PASS")
    print(json.dumps(result["acceptance_checks"], indent=2, ensure_ascii=False))
    print("Gate states:", json.dumps(result["source_gate_states"], sort_keys=True))
    print("Report:", args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
