# Provenance and Evidence

## Provenienztypen

- `external-direct` – direkte externe Quelle/Vorgabe
- `external-derived` – quellennah abgeleiteter Prüfgegenstand
- `internal-method` – internes Methodendesign
- `project-assumption` – Projekt-/Testszenario
- `evidence-observation` – konkrete Beobachtung aus bereitgestellter Evidence

## Evidence Trust

Das Radar nutzt ein internes Trust-Modell 0–5. Es ist **keine externe regulatorische Skala**.

Aktuelle Regel:

`effective_trust = min(base_trust, scope_fit, freshness_fit)`

Eine starke Quelle kann daher für einen konkreten Workload trotzdem wenig beweiskräftig sein, wenn Scope oder Aktualität nicht passen.

## Evidence Provenance / Chain of Custody

Für kundenvermittelte Evidence sollen mindestens gespeichert werden:

- Evidence ID
- Producer / Source
- Assessment-/Workload-Scope
- Datum / Version / Gültigkeit
- Attachment-/Source-Referenz
- Locator (Seite, Abschnitt, Feld, Resource-Alias)
- optional Hash der bereitgestellten Datei
- Redaktions-/Sensitivity-Klasse
- Applied State
- Base Trust / Scope Fit / Freshness Fit
- Review State

Das System benötigt **keine** Cloud-Account-ID oder ausgeführten Cloud-Command als Pflichtfeld. Solche Metadaten können in einem kundenseitig erzeugten Export vorkommen, sind aber nicht methodischer Standard.

## Fehlende Evidence

Kein „negative evidence by absence“ ohne explizite Regel. Standardzustand ist `UNVERIFIED` bzw. Evidence Gap.
