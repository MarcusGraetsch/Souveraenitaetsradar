from __future__ import annotations

import csv
from pathlib import Path

from .models import EvidenceRequest, GateDefinition


class GateCatalogError(ValueError):
    pass


def _split_sources(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.replace(",", ";").split(";") if part.strip())


def load_hard_gates(path: str | Path) -> list[GateDefinition]:
    source = Path(path)
    gates: list[GateDefinition] = []
    seen: set[str] = set()
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        for row in reader:
            gate_id = (row.get("Gate-ID") or "").strip()
            if not gate_id:
                continue
            if gate_id in seen:
                raise GateCatalogError(f"duplicate gate id: {gate_id}")
            seen.add(gate_id)
            try:
                requirements = {
                    "basis": int(row.get("Basis Req") or 0),
                    "standard": int(row.get("Standard Req") or 0),
                    "elevated": int(row.get("Elevated Req") or 0),
                    "critical": int(row.get("Critical Req") or 0),
                }
            except ValueError as exc:
                raise GateCatalogError(f"invalid requirement level for {gate_id}") from exc
            if any(level not in range(0, 5) for level in requirements.values()):
                raise GateCatalogError(f"requirement level outside 0..4 for {gate_id}")
            capability_levels = {
                level: (row.get(f"Capability {level}") or "").strip()
                for level in range(0, 5)
            }
            missing_descriptions = [level for level, text in capability_levels.items() if not text]
            if missing_descriptions:
                raise GateCatalogError(
                    f"missing capability descriptions for {gate_id}: {missing_descriptions}"
                )
            gates.append(
                GateDefinition(
                    gate_id=gate_id,
                    name=(row.get("Gate") or "").strip(),
                    subject=(row.get("Prüfgegenstand") or "").strip(),
                    requirements=requirements,
                    capability_levels=capability_levels,
                    source_ids=_split_sources(row.get("Source IDs") or ""),
                    provenance=(row.get("Provenienz / Herleitung") or "").strip(),
                )
            )
    return gates


def load_evidence_requests(path: str | Path) -> list[EvidenceRequest]:
    source = Path(path)
    requests: list[EvidenceRequest] = []
    seen: set[str] = set()
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        for row in reader:
            request_id = (row.get("Request-ID") or "").strip()
            if not request_id:
                continue
            if request_id in seen:
                raise GateCatalogError(f"duplicate request id: {request_id}")
            seen.add(request_id)
            requests.append(
                EvidenceRequest(
                    request_id=request_id,
                    gate_id=(row.get("Gate-ID") or "").strip(),
                    claim_area=(row.get("Claim area") or "").strip(),
                    acceptable_evidence=(row.get("Acceptable evidence examples") or "").strip(),
                    required_for=(row.get("Required for") or "").strip(),
                    follow_up=(row.get("Provider-neutral follow-up") or "").strip(),
                    preferred_applied_state=(row.get("Preferred applied state") or "").strip(),
                    typical_min_trust=(row.get("Typical min trust") or "").strip(),
                    provenance=(row.get("Provenance") or "").strip(),
                )
            )
    return requests


def evidence_requests_by_gate(requests: list[EvidenceRequest]) -> dict[str, list[EvidenceRequest]]:
    grouped: dict[str, list[EvidenceRequest]] = {}
    for request in requests:
        grouped.setdefault(request.gate_id, []).append(request)
    return grouped


def validate_gate_evidence_mapping(gates: list[GateDefinition], requests: list[EvidenceRequest]) -> None:
    gate_ids = {gate.gate_id for gate in gates}
    mapped_ids = {request.gate_id for request in requests if request.gate_id.startswith("HG-")}
    unknown = mapped_ids - gate_ids
    if unknown:
        raise GateCatalogError(f"evidence requests reference unknown gates: {sorted(unknown)}")
    missing = gate_ids - mapped_ids
    if missing:
        raise GateCatalogError(f"hard gates without evidence requests: {sorted(missing)}")
