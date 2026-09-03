#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from sovradar.intake import EvidencePackError, load_evidence_pack  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/evidence-pack/validate_evidence_pack.py <pack-dir>", file=sys.stderr)
        return 2
    try:
        manifest, records = load_evidence_pack(sys.argv[1], ROOT / "schemas")
    except EvidencePackError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    summary = {
        "assessment_id": manifest["assessment_id"], "evidence_count": len(records),
        "evidence_ids": [r.evidence_id for r in records], "gates": sorted({g for r in records for g in r.gate_ids}),
        "min_effective_trust": min((r.effective_trust for r in records), default=0),
        "max_effective_trust": max((r.effective_trust for r in records), default=0),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
