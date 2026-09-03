# Evidence Pack Tools

`validate_evidence_pack.py` validates a local customer/synthetic pack against repository schemas. It performs **no network access** and requires **no cloud credentials**.

```bash
python tools/evidence-pack/validate_evidence_pack.py data/templates/evidence-pack-example
```

Real customer packs should normally remain outside Git and be referenced from the assessment workspace.
