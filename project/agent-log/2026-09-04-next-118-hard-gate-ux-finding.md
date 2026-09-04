# NEXT-118 – Hard-Gate-UX-Finding

Datum: 2026-09-04
Provenienz: evidence-observation

## Beobachtung

Im ersten manuellen Consultant-Test erschlossen sich zentrale Begriffe der Hard-Gate-Seite nicht ohne Vorwissen:

- `Hard Gates`
- `nicht kompensierbare Mindestanforderungen`
- `Claim`
- `Evidence`
- `Req / Cap / Trust`
- `Jurisdiction & Effective Control`
- `Claims / Human Review`

Die Kacheln `Req 2 · Cap ? · Trust ?` transportieren interne Methoden-/Datenmodellbegriffe, aber keinen verständlichen Arbeitsstatus für einen Consultant.

## Produktbefund

Die Methodik selbst soll nicht vereinfacht oder aufgeweicht werden. Die Benutzeroberfläche soll jedoch normale deutsche Fachsprache verwenden und interne Begriffe nur sekundär zeigen.

Vorgeschlagene primäre UI-Begriffe:

- Hard Gates -> Zwingende Mindestanforderungen (K.O.-Kriterien)
- nicht kompensierbar -> nicht durch andere Stärken ausgleichbar
- Claim -> geprüfte Feststellung
- Evidence -> Nachweis / Beleg
- Requirement -> geforderte Mindeststufe
- Applied Capability -> nachgewiesener Erfüllungsgrad
- Evidence Trust -> Belegstärke / Nachweisvertrauen
- Human Review -> Prüfung durch Consultant
- UNVERIFIED -> nicht ausreichend belegt

Kacheln sollen statt `Req 2 · Cap ? · Trust ?` verständliche Statuszeilen zeigen.

## Referenz

Siehe `docs/product/CONSULTANT_TERMINOLOGY.md`.

## Methodische Grenze

Interne Codes und stabile Datenbegriffe können in API, Export, Auditspur und Detailansichten erhalten bleiben. Die deterministische Gate-Logik wird nicht verändert.
