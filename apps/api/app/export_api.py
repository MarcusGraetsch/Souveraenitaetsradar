from __future__ import annotations

import io
import json
import uuid
import zipfile
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Body, Depends, File, HTTPException, Query, Response, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from sovradar.gate_catalog import load_hard_gates
from sovradar.gate_evaluation import evaluate_gate
from sovradar.models import AppliedState, Claim as CoreClaim, EvidenceRecord

from .database import get_db
from .models import (
    Answer,
    Assessment,
    AssessmentClaim,
    AssessmentProfile,
    Evidence,
    EvidenceReview,
    GateRequirement,
    LlmImport,
)
from .settings import settings

router = APIRouter()

EXPORT_SCHEMA_NAME = "sovradar.assessment-export"
EXPORT_SCHEMA_VERSION = "1.0"
BACKUP_SCHEMA_NAME = "sovradar.assessment-backup"
BACKUP_SCHEMA_VERSION = "1.0"
PRODUCT_VERSION = "0.4.0"
METHOD_VERSION = "1.0"

CRITICALITY_TEMPLATE = {
    "low": "basis",
    "medium": "standard",
    "high": "elevated",
    "critical": "critical",
}


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _iso(value: Any) -> str | None:
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _json_loads(raw: str | None, fallback: Any) -> Any:
    try:
        return json.loads(raw or "")
    except (json.JSONDecodeError, TypeError):
        return fallback


@lru_cache(maxsize=1)
def _gate_catalog():
    return load_hard_gates(settings.method_dir / "r4_hard_gates.csv")


def _gate_map():
    return {gate.gate_id: gate for gate in _gate_catalog()}


def _default_requirement(assessment: Assessment, gate_id: str) -> tuple[int, str]:
    gate = _gate_map().get(gate_id)
    if gate is None:
        raise HTTPException(400, f"unknown gate_id: {gate_id}")
    template = CRITICALITY_TEMPLATE.get(assessment.criticality, "standard")
    return gate.requirements[template], f"criticality-template:{template}"


def _requirement(assessment: Assessment, gate_id: str, db: Session) -> tuple[int, str]:
    row = db.get(GateRequirement, (assessment.id, gate_id))
    if row is not None:
        return row.requirement_level, row.source
    return _default_requirement(assessment, gate_id)


def _core_evidence(assessment_id: str, db: Session) -> list[EvidenceRecord]:
    evidence_rows = db.scalars(select(Evidence).where(Evidence.assessment_id == assessment_id)).all()
    reviews = {
        row.evidence_id: row
        for row in db.scalars(select(EvidenceReview).where(EvidenceReview.assessment_id == assessment_id)).all()
    }
    records: list[EvidenceRecord] = []
    for item in evidence_rows:
        review = reviews.get(item.id)
        records.append(
            EvidenceRecord(
                evidence_id=item.id,
                evidence_type=item.evidence_type,
                title=item.title,
                producer=item.source or "consultant-intake",
                scope={"workload_id": assessment_id},
                applied_state=AppliedState(review.applied_state if review else "asserted"),
                base_trust=review.base_trust if review else 0,
                scope_fit=review.scope_fit if review else 0,
                freshness_fit=review.freshness_fit if review else 0,
                sensitivity="internal",
                review_status=review.review_status if review else "raw",
                source_ref=item.source or None,
                locator=item.source_date or None,
                notes=item.description or None,
            )
        )
    return records


def _core_claims(assessment_id: str, db: Session) -> list[CoreClaim]:
    rows = db.scalars(select(AssessmentClaim).where(AssessmentClaim.assessment_id == assessment_id)).all()
    return [
        CoreClaim(
            claim_id=row.id,
            gate_id=row.gate_id,
            statement=row.statement,
            review_status=row.review_status,
            capability_level=row.capability_level,
            evidence_ids=tuple(_json_loads(row.evidence_ids_json, [])),
            question_ids=tuple(_json_loads(row.question_ids_json, [])),
            notes=row.notes or None,
        )
        for row in rows
    ]


def _gate_snapshot(assessment: Assessment, db: Session) -> list[dict[str, Any]]:
    claims = _core_claims(assessment.id, db)
    evidence = _core_evidence(assessment.id, db)
    result: list[dict[str, Any]] = []
    for gate in _gate_catalog():
        requirement_level, requirement_source = _requirement(assessment, gate.gate_id, db)
        evaluated = evaluate_gate(gate.gate_id, requirement_level, claims, evidence)
        result.append(
            {
                "gate_id": gate.gate_id,
                "name": gate.name,
                "subject": gate.subject,
                "requirement_level": requirement_level,
                "requirement_source": requirement_source,
                "capability_level": evaluated.capability_level,
                "effective_trust": evaluated.effective_trust,
                "technical_state": evaluated.technical_state,
                "evidence_state": evaluated.evidence_state,
                "final_state": evaluated.final_state,
                "claim_ids": list(evaluated.claim_ids),
                "evidence_ids": list(evaluated.evidence_ids),
                "reasons": list(evaluated.reasons),
                "source_ids": list(gate.source_ids),
                "provenance": gate.provenance,
            }
        )
    return result


def _assessment_snapshot(row: Assessment) -> dict[str, Any]:
    return {
        "id": row.id,
        "name": row.name,
        "customer": row.customer,
        "description": row.description,
        "workload_type": row.workload_type,
        "criticality": row.criticality,
        "confidentiality": row.confidentiality,
        "integrity": row.integrity,
        "availability": row.availability,
        "control_region": row.control_region,
        "regulatory_context": row.regulatory_context,
        "status": row.status,
        "created_at": _iso(row.created_at),
        "updated_at": _iso(row.updated_at),
    }


def build_structured_export(
    assessment_id: str,
    db: Session,
    *,
    include_sensitive_evidence_fields: bool = False,
) -> dict[str, Any]:
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(404, "Assessment not found")

    profile_row = db.get(AssessmentProfile, assessment_id)
    answers = db.scalars(select(Answer).where(Answer.assessment_id == assessment_id).order_by(Answer.question_id)).all()
    evidence_rows = db.scalars(select(Evidence).where(Evidence.assessment_id == assessment_id).order_by(Evidence.created_at)).all()
    reviews = db.scalars(select(EvidenceReview).where(EvidenceReview.assessment_id == assessment_id)).all()
    claims = db.scalars(select(AssessmentClaim).where(AssessmentClaim.assessment_id == assessment_id).order_by(AssessmentClaim.created_at)).all()
    overrides = db.scalars(select(GateRequirement).where(GateRequirement.assessment_id == assessment_id).order_by(GateRequirement.gate_id)).all()
    llm_imports = db.scalars(select(LlmImport).where(LlmImport.assessment_id == assessment_id).order_by(LlmImport.created_at)).all()

    warnings: list[str] = []
    evidence_payload: list[dict[str, Any]] = []
    for item in evidence_rows:
        source_path = settings.documents_dir / assessment_id / item.stored_name if item.stored_name else None
        has_file = bool(source_path and source_path.is_file())
        if item.file_name and not has_file:
            warnings.append(f"Evidence {item.id} references file '{item.file_name}', but no local file is present.")
        payload = {
            "id": item.id,
            "title": item.title,
            "evidence_type": item.evidence_type,
            "description": item.description,
            "source": item.source,
            "source_date": item.source_date,
            "file_name": item.file_name,
            "has_file": has_file,
            "has_content_excerpt": bool(item.content_excerpt),
            "created_at": _iso(item.created_at),
        }
        if include_sensitive_evidence_fields:
            payload["content_excerpt"] = item.content_excerpt
        evidence_payload.append(payload)

    return {
        "export_meta": {
            "schema_name": EXPORT_SCHEMA_NAME,
            "schema_version": EXPORT_SCHEMA_VERSION,
            "product_version": PRODUCT_VERSION,
            "method_version": METHOD_VERSION,
            "exported_at": _utcnow_iso(),
            "source_assessment_id": assessment_id,
            "includes_raw_evidence_files": False,
            "includes_sensitive_evidence_fields": include_sensitive_evidence_fields,
        },
        "assessment": _assessment_snapshot(assessment),
        "relevance_profile": _json_loads(profile_row.profile_json, {}) if profile_row else {},
        "answers": [
            {
                "id": row.id,
                "question_id": row.question_id,
                "answer_value": row.answer_value,
                "comment": row.comment,
                "evidence_ids": _json_loads(row.evidence_ids_json, []),
                "review_state": row.review_state,
                "updated_at": _iso(row.updated_at),
            }
            for row in answers
        ],
        "evidence": evidence_payload,
        "evidence_reviews": [
            {
                "evidence_id": row.evidence_id,
                "applied_state": row.applied_state,
                "base_trust": row.base_trust,
                "scope_fit": row.scope_fit,
                "freshness_fit": row.freshness_fit,
                "effective_trust": min(row.base_trust, row.scope_fit, row.freshness_fit),
                "review_status": row.review_status,
                "updated_at": _iso(row.updated_at),
            }
            for row in reviews
        ],
        "claims": [
            {
                "id": row.id,
                "gate_id": row.gate_id,
                "statement": row.statement,
                "review_status": row.review_status,
                "capability_level": row.capability_level,
                "evidence_ids": _json_loads(row.evidence_ids_json, []),
                "question_ids": _json_loads(row.question_ids_json, []),
                "notes": row.notes,
                "created_at": _iso(row.created_at),
                "updated_at": _iso(row.updated_at),
            }
            for row in claims
        ],
        "gate_requirement_overrides": [
            {
                "gate_id": row.gate_id,
                "requirement_level": row.requirement_level,
                "source": row.source,
                "updated_at": _iso(row.updated_at),
            }
            for row in overrides
        ],
        "gate_results": _gate_snapshot(assessment, db),
        "llm_imports": [
            {
                "id": row.id,
                "validation_status": row.validation_status,
                "proposals": _json_loads(row.proposals_json, []),
                "evidence_gaps": _json_loads(row.gaps_json, []),
                "warnings": _json_loads(row.warnings_json, []),
                "created_at": _iso(row.created_at),
            }
            for row in llm_imports
        ],
        "warnings": warnings,
    }


def validate_export_payload(payload: dict[str, Any]) -> None:
    if not isinstance(payload, dict):
        raise HTTPException(422, "assessment export must be a JSON object")
    meta = payload.get("export_meta")
    if not isinstance(meta, dict):
        raise HTTPException(422, "missing export_meta")
    if meta.get("schema_name") != EXPORT_SCHEMA_NAME:
        raise HTTPException(422, f"unsupported schema_name: {meta.get('schema_name')!r}")
    if meta.get("schema_version") != EXPORT_SCHEMA_VERSION:
        raise HTTPException(422, f"unsupported schema_version: {meta.get('schema_version')!r}")
    if not isinstance(payload.get("assessment"), dict):
        raise HTTPException(422, "missing assessment object")
    for field in (
        "relevance_profile",
        "answers",
        "evidence",
        "evidence_reviews",
        "claims",
        "gate_requirement_overrides",
        "gate_results",
        "llm_imports",
    ):
        expected = dict if field == "relevance_profile" else list
        if not isinstance(payload.get(field), expected):
            raise HTTPException(422, f"invalid or missing field: {field}")


def _decision_label(gates: list[dict[str, Any]]) -> str:
    if any(item.get("final_state") == "FAIL" for item in gates):
        return "BLOCK / Management-Entscheidung erforderlich"
    if any(item.get("final_state") == "UNVERIFIED" for item in gates):
        return "EVIDENCE HOLD / Nachweise vervollständigen"
    if any(item.get("final_state") == "PASS" for item in gates):
        return "GATES PASS / keine automatische Risikoakzeptanz"
    return "Keine anwendbaren Gate-Ergebnisse"


def render_consultant_report(export: dict[str, Any]) -> str:
    validate_export_payload(export)
    assessment = export["assessment"]
    gates = export["gate_results"]
    evidence = export["evidence"]
    reviews = {item["evidence_id"]: item for item in export["evidence_reviews"]}
    claims = export["claims"]
    llm_imports = export["llm_imports"]

    reviewed_evidence = sum(
        1 for item in reviews.values() if item.get("review_status") in {"reviewed", "approved"}
    )
    unverified = [item for item in gates if item.get("final_state") == "UNVERIFIED"]
    failed = [item for item in gates if item.get("final_state") == "FAIL"]
    passed = [item for item in gates if item.get("final_state") == "PASS"]
    applicable = [item for item in gates if item.get("final_state") != "N/A"]
    reviewed_claims = [item for item in claims if item.get("review_status") in {"reviewed", "approved"}]

    lines = [
        "# Souveränitäts-Radar – Consultant Report",
        "",
        f"**Assessment:** {assessment.get('name', '—')}",
        f"**Kunde:** {assessment.get('customer') or '—'}",
        f"**Workload:** {assessment.get('workload_type', '—')}",
        f"**Kritikalität:** {assessment.get('criticality', '—')}",
        f"**Kontrollraum:** {assessment.get('control_region', '—')}",
        f"**Exportzeit:** {export['export_meta'].get('exported_at', '—')}",
        "",
        "> Dieser Bericht ist eine Beratungs-/Arbeitsunterlage. Er enthält keine automatische Risikoakzeptanz und keine Rechtsfeststellung.",
        "",
        "## 1. Scope und Management-Kontext",
        "",
        f"- Vertraulichkeit: **{assessment.get('confidentiality', '—')}**",
        f"- Integrität: **{assessment.get('integrity', '—')}**",
        f"- Verfügbarkeit: **{assessment.get('availability', '—')}**",
        f"- Regulatorischer Kontext: {assessment.get('regulatory_context') or 'nicht erfasst'}",
        f"- Beschreibung: {assessment.get('description') or 'nicht erfasst'}",
        "",
        "## 2. Evidenzlage",
        "",
        f"- Evidence-Objekte: **{len(evidence)}**",
        f"- reviewed/approved Evidence Reviews: **{reviewed_evidence}**",
        f"- human-reviewed/approved Claims: **{len(reviewed_claims)}**",
        f"- Export-Warnungen: **{len(export.get('warnings', []))}**",
        "",
        "Raw Evidence-Dateien und freigegebene Content-Excerpts werden in diesem Consultant Report nicht eingebettet.",
        "",
        "## 3. Hard-Gate-Ergebnisse",
        "",
        f"**Arbeitsstatus:** {_decision_label(gates)}",
        "",
        "| Gate | Requirement | Capability | Trust | Status |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for item in gates:
        lines.append(
            f"| {item['gate_id']} {item['name']} | {item['requirement_level']} | "
            f"{item['capability_level'] if item['capability_level'] is not None else '—'} | "
            f"{item['effective_trust'] if item['effective_trust'] is not None else '—'} | {item['final_state']} |"
        )

    lines.extend([
        "",
        f"PASS: **{len(passed)}** · FAIL: **{len(failed)}** · UNVERIFIED: **{len(unverified)}** · anwendbare Gates: **{len(applicable)}**",
        "",
        "## 4. Offene Evidence Gaps / UNVERIFIED",
        "",
    ])
    if not unverified:
        lines.append("Keine UNVERIFIED Hard Gates im aktuellen Stand.")
    else:
        for item in unverified:
            lines.append(f"### {item['gate_id']} – {item['name']}")
            for reason in item.get("reasons", []):
                lines.append(f"- {reason}")
            lines.append("")

    lines.extend([
        "## 5. Technische Mindestabweichungen / FAIL",
        "",
    ])
    if not failed:
        lines.append("Keine technischen Hard-Gate-Fails im aktuellen Stand.")
    else:
        for item in failed:
            lines.append(
                f"- **{item['gate_id']} {item['name']}**: Requirement {item['requirement_level']}, "
                f"Capability {item['capability_level'] if item['capability_level'] is not None else '—'}."
            )

    lines.extend([
        "",
        "## 6. Management- und Governance-Hinweise",
        "",
        "- Hard-Gate-Ergebnisse ersetzen keine vollständige Risikoanalyse und keine Management-Risikoakzeptanz.",
        "- Radar Capability Level 0–4 und interne Schwellen sind interne Operationalisierung und kein offizieller EU-SEAL.",
        "- Fehlende Evidence wird als UNVERIFIED behandelt und nicht automatisch als technisches FAIL interpretiert.",
        "- Legal-Schlussfolgerungen, Ausnahmen und finale Freigaben bleiben menschliche Entscheidungen.",
        "",
        "## 7. Provenienz",
        "",
    ])
    for item in gates:
        source_ids = ", ".join(item.get("source_ids") or []) or "INT-03"
        lines.append(f"- {item['gate_id']}: {source_ids} · {item.get('provenance') or 'interne Operationalisierung'}")

    lines.extend([
        "",
        "## 8. LLM-Bridge-Auditspur",
        "",
        f"Importierte LLM-Ergebnisobjekte: **{len(llm_imports)}**. Diese bleiben Vorschläge und ändern ohne Human Review weder Claims noch Hard Gates.",
        "",
        "---",
        f"Schema: `{export['export_meta']['schema_name']}` v{export['export_meta']['schema_version']} · Produkt {export['export_meta']['product_version']} · Methode {export['export_meta']['method_version']}",
        "",
    ])
    return "\n".join(lines)


def _remap_evidence_ids(ids: list[str], evidence_map: dict[str, str]) -> list[str]:
    return [evidence_map[item] for item in ids if item in evidence_map]


def restore_structured_export(payload: dict[str, Any], db: Session) -> dict[str, Any]:
    validate_export_payload(payload)
    source = payload["assessment"]
    new_assessment_id = str(uuid.uuid4())
    assessment = Assessment(
        id=new_assessment_id,
        name=f"{source.get('name') or 'Assessment'} (Restore)",
        customer=source.get("customer", ""),
        description=source.get("description", ""),
        workload_type=source.get("workload_type", "other"),
        criticality=source.get("criticality", "medium"),
        confidentiality=source.get("confidentiality", "medium"),
        integrity=source.get("integrity", "medium"),
        availability=source.get("availability", "medium"),
        control_region=source.get("control_region", "EU/EWR"),
        regulatory_context=source.get("regulatory_context", ""),
        status=source.get("status", "draft"),
    )
    db.add(assessment)
    db.add(
        AssessmentProfile(
            assessment_id=new_assessment_id,
            profile_json=json.dumps(payload.get("relevance_profile", {}), ensure_ascii=False),
        )
    )

    evidence_map: dict[str, str] = {}
    missing_raw_files: list[str] = []
    for item in payload["evidence"]:
        old_id = str(item.get("id"))
        new_id = str(uuid.uuid4())
        evidence_map[old_id] = new_id
        file_name = Path(str(item.get("file_name") or "")).name[:255]
        if file_name and item.get("has_file"):
            missing_raw_files.append(old_id)
        db.add(
            Evidence(
                id=new_id,
                assessment_id=new_assessment_id,
                title=str(item.get("title") or "Restored Evidence")[:255],
                evidence_type=str(item.get("evidence_type") or "other")[:64],
                description=str(item.get("description") or ""),
                source=str(item.get("source") or ""),
                source_date=str(item.get("source_date") or "")[:64],
                content_excerpt=str(item.get("content_excerpt") or ""),
                file_name=file_name,
                stored_name="",
            )
        )

    for item in payload["evidence_reviews"]:
        old_evidence_id = str(item.get("evidence_id"))
        new_evidence_id = evidence_map.get(old_evidence_id)
        if not new_evidence_id:
            continue
        db.add(
            EvidenceReview(
                evidence_id=new_evidence_id,
                assessment_id=new_assessment_id,
                applied_state=str(item.get("applied_state") or "asserted"),
                base_trust=int(item.get("base_trust") or 0),
                scope_fit=int(item.get("scope_fit") or 0),
                freshness_fit=int(item.get("freshness_fit") or 0),
                review_status=str(item.get("review_status") or "raw"),
            )
        )

    for item in payload["answers"]:
        db.add(
            Answer(
                id=str(uuid.uuid4()),
                assessment_id=new_assessment_id,
                question_id=str(item.get("question_id") or "")[:64],
                answer_value=str(item.get("answer_value") or ""),
                comment=str(item.get("comment") or ""),
                evidence_ids_json=json.dumps(
                    _remap_evidence_ids(list(item.get("evidence_ids") or []), evidence_map)
                ),
                review_state=str(item.get("review_state") or "draft"),
            )
        )

    for item in payload["claims"]:
        db.add(
            AssessmentClaim(
                id=str(uuid.uuid4()),
                assessment_id=new_assessment_id,
                gate_id=str(item.get("gate_id") or "")[:16],
                statement=str(item.get("statement") or ""),
                review_status=str(item.get("review_status") or "draft"),
                capability_level=item.get("capability_level"),
                evidence_ids_json=json.dumps(
                    _remap_evidence_ids(list(item.get("evidence_ids") or []), evidence_map)
                ),
                question_ids_json=json.dumps(list(item.get("question_ids") or [])),
                notes=str(item.get("notes") or ""),
            )
        )

    for item in payload["gate_requirement_overrides"]:
        gate_id = str(item.get("gate_id") or "")[:16]
        if gate_id not in _gate_map():
            continue
        db.add(
            GateRequirement(
                assessment_id=new_assessment_id,
                gate_id=gate_id,
                requirement_level=int(item.get("requirement_level") or 0),
                source=str(item.get("source") or "restored-override")[:64],
            )
        )

    for item in payload["llm_imports"]:
        proposals = []
        for proposal in list(item.get("proposals") or []):
            normalized = dict(proposal)
            normalized["evidence_ids"] = _remap_evidence_ids(
                list(normalized.get("evidence_ids") or []), evidence_map
            )
            proposals.append(normalized)
        gaps = list(item.get("evidence_gaps") or [])
        warnings = list(item.get("warnings") or [])
        raw = {
            "assessment_id": new_assessment_id,
            "proposals": proposals,
            "evidence_gaps": gaps,
            "warnings": warnings,
        }
        db.add(
            LlmImport(
                id=str(uuid.uuid4()),
                assessment_id=new_assessment_id,
                raw_json=json.dumps(raw, ensure_ascii=False),
                proposals_json=json.dumps(proposals, ensure_ascii=False),
                gaps_json=json.dumps(gaps, ensure_ascii=False),
                warnings_json=json.dumps(warnings, ensure_ascii=False),
                validation_status=str(item.get("validation_status") or "valid")[:32],
            )
        )

    db.commit()
    db.refresh(assessment)
    restored_gates = _gate_snapshot(assessment, db)
    source_gates = {item["gate_id"]: item for item in payload["gate_results"]}
    comparisons: list[dict[str, Any]] = []
    drift = False
    for restored in restored_gates:
        source_gate = source_gates.get(restored["gate_id"])
        fields = [
            "requirement_level",
            "capability_level",
            "effective_trust",
            "technical_state",
            "evidence_state",
            "final_state",
        ]
        differences = {
            field: {"source": source_gate.get(field) if source_gate else None, "restored": restored.get(field)}
            for field in fields
            if source_gate is None or source_gate.get(field) != restored.get(field)
        }
        if differences:
            drift = True
        comparisons.append(
            {
                "gate_id": restored["gate_id"],
                "matches": not differences,
                "differences": differences,
            }
        )

    return {
        "assessment_id": new_assessment_id,
        "restored_from_assessment_id": payload["export_meta"].get("source_assessment_id"),
        "evidence_id_map": evidence_map,
        "missing_raw_file_source_evidence_ids": missing_raw_files,
        "gate_semantic_drift": drift,
        "gate_comparison": comparisons,
        "warnings": [
            "Structured restore recreates metadata and decision state. Raw Evidence files are absent unless restored from an explicit full backup."
        ] if missing_raw_files else [],
    }


def _safe_filename(name: str, fallback: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "-" for ch in name).strip("-.")
    return cleaned[:120] or fallback


def build_backup(assessment_id: str, db: Session, *, include_evidence: bool) -> tuple[bytes, dict[str, Any]]:
    export = build_structured_export(
        assessment_id,
        db,
        include_sensitive_evidence_fields=include_evidence,
    )
    assessment = db.get(Assessment, assessment_id)
    assert assessment is not None
    report = render_consultant_report(
        build_structured_export(assessment_id, db, include_sensitive_evidence_fields=False)
    )
    missing_files: list[str] = []
    included_files: list[dict[str, Any]] = []
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("assessment.json", json.dumps(export, indent=2, ensure_ascii=False) + "\n")
        archive.writestr("consultant-report.md", report)
        if include_evidence:
            for item in db.scalars(select(Evidence).where(Evidence.assessment_id == assessment_id)).all():
                if not item.stored_name or not item.file_name:
                    continue
                source = settings.documents_dir / assessment_id / item.stored_name
                if not source.is_file():
                    missing_files.append(item.id)
                    continue
                safe_name = _safe_filename(Path(item.file_name).name, f"evidence-{item.id}")
                arcname = f"evidence/{item.id}/{safe_name}"
                archive.write(source, arcname)
                included_files.append({"evidence_id": item.id, "path": arcname, "size": source.stat().st_size})
        manifest = {
            "schema_name": BACKUP_SCHEMA_NAME,
            "schema_version": BACKUP_SCHEMA_VERSION,
            "created_at": _utcnow_iso(),
            "assessment_id": assessment_id,
            "assessment_name": assessment.name,
            "includes_raw_evidence": include_evidence,
            "included_files": included_files,
            "missing_file_evidence_ids": missing_files,
        }
        archive.writestr("manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    return buffer.getvalue(), manifest


def restore_backup(data: bytes, db: Session) -> dict[str, Any]:
    try:
        archive = zipfile.ZipFile(io.BytesIO(data), "r")
    except zipfile.BadZipFile as exc:
        raise HTTPException(422, "invalid backup ZIP") from exc
    with archive:
        names = set(archive.namelist())
        if "assessment.json" not in names:
            raise HTTPException(422, "backup ZIP is missing assessment.json")
        try:
            payload = json.loads(archive.read("assessment.json").decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise HTTPException(422, "assessment.json is invalid") from exc
        manifest = {}
        if "manifest.json" in names:
            try:
                manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                manifest = {}
        result = restore_structured_export(payload, db)
        assessment_id = result["assessment_id"]
        evidence_map = result["evidence_id_map"]
        restored_files: list[str] = []
        file_warnings: list[str] = []
        if manifest.get("includes_raw_evidence"):
            target_dir = settings.documents_dir / assessment_id
            target_dir.mkdir(parents=True, exist_ok=True)
            for item in list(manifest.get("included_files") or []):
                old_evidence_id = str(item.get("evidence_id") or "")
                new_evidence_id = evidence_map.get(old_evidence_id)
                arcname = str(item.get("path") or "")
                if not new_evidence_id or arcname not in names or not arcname.startswith(f"evidence/{old_evidence_id}/"):
                    continue
                raw = archive.read(arcname)
                if len(raw) > settings.max_upload_bytes:
                    file_warnings.append(f"Evidence {old_evidence_id}: file exceeds configured per-file limit and was not restored.")
                    continue
                original_name = Path(arcname).name[:255]
                suffix = Path(original_name).suffix[:20]
                stored_name = f"{new_evidence_id}{suffix}"
                target = target_dir / stored_name
                target.write_bytes(raw)
                row = db.get(Evidence, new_evidence_id)
                if row:
                    row.file_name = original_name
                    row.stored_name = stored_name
                restored_files.append(new_evidence_id)
            db.commit()
        result["restored_raw_evidence_ids"] = restored_files
        result["warnings"] = list(result.get("warnings") or []) + file_warnings
        if restored_files:
            result["missing_raw_file_source_evidence_ids"] = [
                old_id
                for old_id in result["missing_raw_file_source_evidence_ids"]
                if evidence_map.get(old_id) not in restored_files
            ]
        return result


@router.get("/api/assessments/{assessment_id}/export")
def assessment_export(
    assessment_id: str,
    include_sensitive_evidence_fields: bool = Query(False),
    db: Session = Depends(get_db),
):
    return build_structured_export(
        assessment_id,
        db,
        include_sensitive_evidence_fields=include_sensitive_evidence_fields,
    )


@router.get("/api/assessments/{assessment_id}/report")
def consultant_report(assessment_id: str, db: Session = Depends(get_db)):
    export = build_structured_export(assessment_id, db, include_sensitive_evidence_fields=False)
    report = render_consultant_report(export)
    filename = _safe_filename(export["assessment"].get("name") or assessment_id, "assessment") + "-report.md"
    return Response(
        report,
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/api/assessments/{assessment_id}/backup")
def assessment_backup(
    assessment_id: str,
    include_evidence: bool = Query(False),
    db: Session = Depends(get_db),
):
    payload, manifest = build_backup(assessment_id, db, include_evidence=include_evidence)
    filename = f"sovradar-{assessment_id}{'-full' if include_evidence else '-structured'}.zip"
    return Response(
        payload,
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Sovradar-Includes-Evidence": "true" if manifest["includes_raw_evidence"] else "false",
        },
    )


@router.post("/api/assessments/import", status_code=201)
def import_assessment(payload: dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    return restore_structured_export(payload, db)


@router.post("/api/assessments/import-backup", status_code=201)
async def import_backup(file: UploadFile = File(...), db: Session = Depends(get_db)):
    data = await file.read(settings.max_upload_bytes * 5 + 1)
    if len(data) > settings.max_upload_bytes * 5:
        raise HTTPException(413, "backup exceeds configured upload limit")
    return restore_backup(data, db)
