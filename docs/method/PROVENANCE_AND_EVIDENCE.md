# Provenance and Evidence

## Provenienztypen

- externe direkte Quelle
- quellennaher abgeleiteter Prüfgegenstand
- internes Methodendesign
- Projektannahme
- konkrete Evidence-Beobachtung

## Evidence Trust

Das aktuelle Modell nutzt Trust-Level 0–5. Die Zahlen sind internes Design.

R5 ergänzt:

`effective_trust = min(base_trust, scope_fit)`

R6 sieht zusätzlich `freshness_fit` vor:

`effective_trust = min(base_trust, scope_fit, freshness_fit)`

## Wichtige Regel

Eine starke allgemeine Quelle kann trotzdem geringe Passung auf einen konkreten Account, Vertrag, Service, Region oder Modellstand haben.

## Chain of Custody

Technische R6-Evidence trägt:

- Collector ID
- Command
- UTC Timestamp
- Account/Region/Resource Scope
- Raw File
- SHA-256
- Exit Code
- Review State

## Umgang mit fehlender Evidence

Kein „negative evidence by absence“ ohne explizite Regel. Standardzustand ist `UNVERIFIED`.
