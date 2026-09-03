#!/usr/bin/env python3
from pathlib import Path
import csv, json, sys
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
errors = []

for path in ROOT.rglob('*.json'):
    if '.git' in path.parts: continue
    try: json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc: errors.append(f'JSON {path.relative_to(ROOT)}: {exc}')

for path in ROOT.rglob('*.yaml'):
    try: yaml.safe_load(path.read_text(encoding='utf-8'))
    except Exception as exc: errors.append(f'YAML {path.relative_to(ROOT)}: {exc}')

for path in (ROOT/'data').rglob('*.csv'):
    try:
        with path.open(encoding='utf-8-sig', newline='') as f: rows=list(csv.reader(f, delimiter=';'))
        if not rows or not any(rows[0]): errors.append(f'CSV {path.relative_to(ROOT)}: empty header')
        else:
            width=len(rows[0])
            for i,row in enumerate(rows[1:], start=2):
                if len(row) != width: errors.append(f'CSV {path.relative_to(ROOT)} row {i}: {len(row)} != {width}')
    except Exception as exc: errors.append(f'CSV {path.relative_to(ROOT)}: {exc}')

try:
    schema=json.loads((ROOT/'schemas/project-state.schema.json').read_text(encoding='utf-8'))
    state=yaml.safe_load((ROOT/'project/PROJECT_STATE.yaml').read_text(encoding='utf-8'))
    for err in Draft202012Validator(schema).iter_errors(state): errors.append('PROJECT_STATE schema: ' + err.message)
except Exception as exc: errors.append(f'PROJECT_STATE validation setup: {exc}')

if (ROOT/'tools/aws-bedrock-evidence').exists(): errors.append('retired direct AWS collector must not exist in active tools/')
rules_text=(ROOT/'src/sovradar/rules.py').read_text(encoding='utf-8').lower()
for brand in ('aws','azure','google cloud','gcp','bedrock'):
    if brand in rules_text: errors.append(f'provider brand found in core rules.py: {brand}')

required=[ROOT/'AGENTS.md',ROOT/'project/PROJECT_STATE.yaml',ROOT/'project/HANDOFF.md',ROOT/'schemas/evidence-pack.schema.json',ROOT/'data/method/evidence_request_catalog.csv',ROOT/'docs/architecture/EVIDENCE_ACQUISITION_ARCHITECTURE.md']
for p in required:
    if not p.exists(): errors.append(f'missing required file: {p.relative_to(ROOT)}')

if errors:
    print('\n'.join(errors), file=sys.stderr); raise SystemExit(1)
print('repository validation OK')
