# Provider Adapter Architecture

## Purpose

Provider adapters isolate terminology and file formats from the method core.

```python
ProviderAdapter.parse(input_files) -> list[GenericFact]
```

A `GenericFact` might describe:

- resource location
- key-control mode
- identity dependency
- logging capability
- provider/subprovider dependency
- data export capability
- model/AI dependency

## Adapter rules

Adapters MAY:

- recognize provider-specific fields
- normalize resource identifiers and locations
- emit generic facts with source locators
- mark unknown/conditional fields
- propose follow-up questions

Adapters MUST NOT:

- assign final risk acceptance
- embed provider-specific hard-gate thresholds
- require live provider credentials
- silently convert missing fields to FAIL
- make legal conclusions

## Agnostik test

The core architecture is considered provider-agnostic only if:

1. the same assessment schema can represent at least two hyperscalers and one non-hyperscaler/SaaS scenario;
2. core `rules.py` contains no provider brand names;
3. deleting one adapter does not change rule semantics;
4. manual/documentary evidence can satisfy a claim when provider export is unavailable.
