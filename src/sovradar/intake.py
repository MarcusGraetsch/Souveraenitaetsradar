from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator

from .models import AppliedState, EvidenceRecord


class EvidencePackError(ValueError):
    pass


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise EvidencePackError(f"invalid JSON {path}: {exc}") from exc


def _validate(instance: dict, schema_path: Path, label: str) -> None:
    schema = _load_json(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        details = "; ".join(f"{list(e.path)}: {e.message}" for e in errors[:10])
        raise EvidencePackError(f"{label} schema validation failed: {details}")


def load_evidence_pack(pack_dir: str | Path, schema_dir: str | Path) -> tuple[dict, list[EvidenceRecord]]:
    pack = Path(pack_dir).resolve()
    schemas = Path(schema_dir).resolve()
    if not pack.is_dir():
        raise EvidencePackError(f"pack directory not found: {pack}")

    manifest_path = pack / "manifest.json"
    manifest = _load_json(manifest_path)
    _validate(manifest, schemas / "evidence-pack.schema.json", "manifest")

    records: list[EvidenceRecord] = []
    seen: set[str] = set()
    for rel in manifest["evidence_files"]:
        candidate = (pack / rel).resolve()
        try:
            candidate.relative_to(pack)
        except ValueError as exc:
            raise EvidencePackError(f"evidence path escapes pack: {rel}") from exc
        raw = _load_json(candidate)
        _validate(raw, schemas / "evidence-record.schema.json", rel)
        if raw["evidence_id"] in seen:
            raise EvidencePackError(f"duplicate evidence_id: {raw['evidence_id']}")
        seen.add(raw["evidence_id"])
        records.append(EvidenceRecord(
            evidence_id=raw["evidence_id"], evidence_type=raw["evidence_type"], title=raw["title"], producer=raw["producer"],
            scope=raw["scope"], applied_state=AppliedState(raw["applied_state"]), base_trust=raw["base_trust"],
            scope_fit=raw["scope_fit"], freshness_fit=raw["freshness_fit"], sensitivity=raw["sensitivity"],
            review_status=raw["review_status"], claim_ids=tuple(raw.get("claim_ids", [])), gate_ids=tuple(raw.get("gate_ids", [])),
            request_ids=tuple(raw.get("request_ids", [])), source_ref=raw.get("source_ref"), attachment_ref=raw.get("attachment_ref"), locator=raw.get("locator"),
            valid_at=raw.get("valid_at"), version=raw.get("version"), notes=raw.get("notes")
        ))
    return manifest, records


def evidence_for_gate(records: Iterable[EvidenceRecord], gate_id: str) -> list[EvidenceRecord]:
    return [r for r in records if gate_id in r.gate_ids]


def evidence_for_request(records: Iterable[EvidenceRecord], request_id: str) -> list[EvidenceRecord]:
    return [r for r in records if request_id in r.request_ids]
