#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _json_request(base_url: str, method: str, path: str, payload: Any | None = None) -> Any:
    data = None
    headers: dict[str, str] = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(base_url + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
            if not body:
                return None
            return json.loads(body.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} -> HTTP {exc.code}: {detail}") from exc


def _multipart_request(base_url: str, path: str, fields: dict[str, str]) -> Any:
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


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run(base_url: str, output: Path) -> dict[str, Any]:
    health = _json_request(base_url, "GET", "/api/health")
    _assert(health.get("status") == "ok", f"API health failed: {health}")

    assessment = _json_request(
        base_url,
        "POST",
        "/api/assessments",
        {
            "name": "SYN-NEXT-114 – KI-Agent mit sensiblen Fachdaten",
            "customer": "Synthetischer Kunde",
            "description": (
                "Providerneutraler Validierungsfall: ein agentisches KI-System verarbeitet sensible "
                "Fachdaten. Technische, vertragliche und betriebliche Merkmale sind ausschließlich "
                "synthetische Testannahmen."
            ),
            "workload_type": "ai-agent",
            "criticality": "high",
            "confidentiality": "high",
            "integrity": "high",
            "availability": "medium",
            "control_region": "EU/EWR",
            "regulatory_context": "Synthetischer Testkontext; keine Rechtsfeststellung",
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
        },
    )
    _assert(profile["ai_used"] is True and profile["agentic_ai"] is True, "AI profile not persisted")

    relevant_questions = _json_request(base_url, "GET", f"/api/assessments/{assessment_id}/questions?view=relevant")
    all_questions = _json_request(base_url, "GET", f"/api/assessments/{assessment_id}/questions?view=all")
    _assert(len(relevant_questions) > 0, "guided question path is empty")
    _assert(len(all_questions) >= len(relevant_questions), "all-question view is smaller than guided path")

    first_question_id = relevant_questions[0]["id"]
    saved_answer = _json_request(
        base_url,
        "PUT",
        f"/api/assessments/{assessment_id}/answers/{first_question_id}",
        {
            "question_id": first_question_id,
            "answer_value": "synthetisch geprüft",
            "comment": "NEXT-114 Validierungsantwort; keine Provider-Tatsache.",
            "evidence_ids": [],
            "review_state": "reviewed",
        },
    )
    _assert(saved_answer["review_state"] == "reviewed", "reviewed answer not persisted")

    evidence_control = _multipart_request(
        base_url,
        f"/api/assessments/{assessment_id}/evidence",
        {
            "title": "Synthetische Jurisdiktions- und Kontrollunterlage",
            "evidence_type": "contract",
            "description": "Test-Evidence für HG-01; ausschließlich synthetische Annahme.",
            "source": "NEXT-114 synthetic fixture",
            "source_date": "2026-09-03",
            "content_excerpt": "Testannahme: Kontrollstruktur und Jurisdiktionsmerkmale sind dokumentiert.",
        },
    )
    evidence_key = _multipart_request(
        base_url,
        f"/api/assessments/{assessment_id}/evidence",
        {
            "title": "Synthetische KMS-Konfiguration",
            "evidence_type": "configuration",
            "description": "Test-Evidence für HG-03; ausschließlich synthetische Annahme.",
            "source": "NEXT-114 synthetic fixture",
            "source_date": "2026-09-03",
            "content_excerpt": "Testannahme: Schlüsselkontrolle ist nur eingeschränkt kundenseitig wirksam.",
        },
    )

    for evidence, applied_state in ((evidence_control, "documented"), (evidence_key, "configured")):
        review = _json_request(
            base_url,
            "PUT",
            f"/api/assessments/{assessment_id}/evidence/{evidence['id']}/review",
            {
                "applied_state": applied_state,
                "base_trust": 4,
                "scope_fit": 4,
                "freshness_fit": 4,
                "review_status": "reviewed",
            },
        )
        _assert(review["effective_trust"] == 4, f"unexpected effective trust: {review}")

    requirement_plan = {
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
        for item in _json_request(base_url, "GET", f"/api/assessments/{assessment_id}/gate-requirements")
    }
    requirement_changes = 0
    for gate_id, level in requirement_plan.items():
        current = current_requirements[gate_id]
        if current["requirement_level"] == level:
            continue
        result = _json_request(
            base_url,
            "PUT",
            f"/api/assessments/{assessment_id}/gate-requirements/{gate_id}",
            {
                "requirement_level": level,
                "reason": "Synthetischer Validierungsplan zur reproduzierbaren Gate-Semantik.",
            },
        )
        _assert(result["requirement_level"] == level, f"requirement override failed for {gate_id}")
        _assert(result["source"] == "consultant-override", f"override provenance missing for {gate_id}")
        requirement_changes += 1
    audit = _json_request(base_url, "GET", f"/api/assessments/{assessment_id}/gate-requirement-changes")
    _assert(len(audit) == requirement_changes, "governed requirement changes were not audited")

    claims_payload = [
        {
            "gate_id": "HG-01",
            "statement": "Synthetisch: Applied Capability für Jurisdiktion/Effective Control erreicht Level 3.",
            "review_status": "reviewed",
            "capability_level": 3,
            "evidence_ids": [evidence_control["id"]],
            "question_ids": [],
            "notes": "Erzeugt bewusst einen PASS im Validierungslauf.",
        },
        {
            "gate_id": "HG-03",
            "statement": "Synthetisch: Applied Capability für Schlüsselhoheit erreicht nur Level 1.",
            "review_status": "reviewed",
            "capability_level": 1,
            "evidence_ids": [evidence_key["id"]],
            "question_ids": [],
            "notes": "Erzeugt bewusst einen technischen FAIL im Validierungslauf.",
        },
        {
            "gate_id": "HG-04",
            "statement": "Synthetisch: Exit Capability wird mit Level 3 behauptet, aber ohne reviewed Evidence.",
            "review_status": "reviewed",
            "capability_level": 3,
            "evidence_ids": [],
            "question_ids": [],
            "notes": "Erzeugt bewusst UNVERIFIED wegen fehlender Evidence.",
        },
        {
            "gate_id": "HG-03",
            "statement": "Entwurf: stärkere Key-Control-Annahme darf den reviewed FAIL nicht überstimmen.",
            "review_status": "draft",
            "capability_level": 4,
            "evidence_ids": [evidence_key["id"]],
            "question_ids": [],
            "notes": "Negativtest der Human-Review-Grenze.",
        },
    ]
    created_claims = [
        _json_request(base_url, "POST", f"/api/assessments/{assessment_id}/claims", payload)
        for payload in claims_payload
    ]

    gates_before_llm = _json_request(base_url, "GET", f"/api/assessments/{assessment_id}/gates")
    state_before = {gate["gate_id"]: gate["final_state"] for gate in gates_before_llm}
    expected_states = {
        "HG-01": "PASS",
        "HG-02": "N/A",
        "HG-03": "FAIL",
        "HG-04": "UNVERIFIED",
        "HG-05": "N/A",
        "HG-06": "N/A",
        "HG-07": "N/A",
        "HG-08": "N/A",
    }
    _assert(state_before == expected_states, f"unexpected gate states before LLM bridge: {state_before}")

    claims_before_llm = _json_request(base_url, "GET", f"/api/assessments/{assessment_id}/claims")
    prompt = _json_request(base_url, "GET", f"/api/assessments/{assessment_id}/llm-bridge/prompt")
    _assert(assessment_id in prompt["prompt"], "LLM bridge prompt missing assessment id")
    llm_import = _json_request(
        base_url,
        "POST",
        f"/api/assessments/{assessment_id}/llm-bridge/import",
        {
            "assessment_id": assessment_id,
            "proposals": [
                {
                    "question_id": first_question_id,
                    "proposed_answer": "synthetischer Vorschlag",
                    "rationale": "Nur Validierung der Copy/Paste Bridge; keine automatische Entscheidungswirkung.",
                    "evidence_ids": [evidence_control["id"]],
                    "confidence": 0.75,
                }
            ],
            "evidence_gaps": [],
            "warnings": ["Synthetischer Validierungslauf"],
        },
    )
    _assert(llm_import["validation_status"] == "valid", "LLM bridge import failed validation")

    claims_after_llm = _json_request(base_url, "GET", f"/api/assessments/{assessment_id}/claims")
    gates_after_llm = _json_request(base_url, "GET", f"/api/assessments/{assessment_id}/gates")
    state_after = {gate["gate_id"]: gate["final_state"] for gate in gates_after_llm}
    _assert(len(claims_after_llm) == len(claims_before_llm), "LLM import changed claim count")
    _assert(state_after == state_before, "LLM import changed deterministic gate result")

    applicability_counts: dict[str, int] = {}
    for question in relevant_questions:
        status = question.get("applicability_status", "unknown")
        applicability_counts[status] = applicability_counts.get(status, 0) + 1

    report = {
        "validation_id": "NEXT-114-SYN-01",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scenario": "Providerneutraler KI-Agent mit sensiblen Fachdaten",
        "scope_statement": "Alle Provider-/Architekturmerkmale sind synthetische Testannahmen.",
        "assessment_id": assessment_id,
        "health": health,
        "guided_workflow": {
            "relevant_question_count": len(relevant_questions),
            "all_question_count": len(all_questions),
            "applicability_counts": applicability_counts,
            "reviewed_answer_question_id": first_question_id,
        },
        "evidence": {
            "count": 2,
            "reviewed_ids": [evidence_control["id"], evidence_key["id"]],
            "effective_trust": 4,
        },
        "claims": {
            "count": len(created_claims),
            "human_reviewed_capability_claims": 3,
            "draft_negative_control_claims": 1,
        },
        "gate_requirements": requirement_plan,
        "gate_requirement_audit_count": len(audit),
        "gate_states": state_after,
        "expected_gate_states": expected_states,
        "llm_bridge": {
            "import_status": llm_import["validation_status"],
            "proposal_count": len(llm_import["proposals"]),
            "claim_count_before": len(claims_before_llm),
            "claim_count_after": len(claims_after_llm),
            "gate_states_unchanged": state_before == state_after,
        },
        "acceptance_checks": {
            "guided_questions_available": len(relevant_questions) > 0,
            "evidence_reviewed": True,
            "governed_requirement_changes_audited": len(audit) == requirement_changes,
            "pass_demonstrated": "PASS" in state_after.values(),
            "fail_demonstrated": "FAIL" in state_after.values(),
            "unverified_demonstrated": "UNVERIFIED" in state_after.values(),
            "llm_did_not_create_claim": len(claims_after_llm) == len(claims_before_llm),
            "llm_did_not_change_gate": state_before == state_after,
        },
    }
    _assert(all(report["acceptance_checks"].values()), f"acceptance checks failed: {report['acceptance_checks']}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run NEXT-114 synthetic consultant walkthrough against a live Souveraenitaets-Radar instance.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080")
    parser.add_argument("--output", default=".runtime/exports/synthetic-consultant-walkthrough.json")
    args = parser.parse_args()
    try:
        report = run(args.base_url.rstrip("/"), Path(args.output))
    except Exception as exc:  # noqa: BLE001 - validation CLI must surface the complete failure
        print(f"NEXT-114 synthetic walkthrough FAILED: {exc}", file=sys.stderr)
        return 1
    print("NEXT-114 synthetic walkthrough PASS")
    print(json.dumps(report["acceptance_checks"], indent=2, ensure_ascii=False))
    print("Gate states:", json.dumps(report["gate_states"], sort_keys=True))
    print("Report:", args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
