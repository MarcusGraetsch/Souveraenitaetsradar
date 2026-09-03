#!/usr/bin/env python3
from pathlib import Path
import csv,json,sys,yaml
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]; errors=[]
for p in ROOT.rglob('*.json'):
    try: json.loads(p.read_text(encoding='utf-8'))
    except Exception as exc: errors.append(f'JSON {p.relative_to(ROOT)}: {exc}')
for p in ROOT.rglob('*.yaml'):
    try: yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception as exc: errors.append(f'YAML {p.relative_to(ROOT)}: {exc}')
for p in (ROOT/'data').rglob('*.csv'):
    try:
        with p.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.reader(f,delimiter=';'))
        if not rows or not any(rows[0]): errors.append(f'CSV {p.relative_to(ROOT)}: empty header')
        else:
            w=len(rows[0])
            for i,row in enumerate(rows[1:],2):
                if len(row)!=w: errors.append(f'CSV {p.relative_to(ROOT)} row {i}: {len(row)} != {w}')
    except Exception as exc: errors.append(f'CSV {p.relative_to(ROOT)}: {exc}')
try:
    schema=json.loads((ROOT/'schemas/project-state.schema.json').read_text()); state=yaml.safe_load((ROOT/'project/PROJECT_STATE.yaml').read_text())
    for err in Draft202012Validator(schema).iter_errors(state): errors.append('PROJECT_STATE schema: '+err.message)
except Exception as exc: errors.append(f'PROJECT_STATE validation setup: {exc}')
if errors: print('\n'.join(errors),file=sys.stderr); raise SystemExit(1)
print('repository validation OK')
