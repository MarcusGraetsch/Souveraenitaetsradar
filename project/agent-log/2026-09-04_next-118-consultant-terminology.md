# Agent Log – Consultant-freundliche Terminologie

Datum: 2026-09-04
Issue: #50
PR: #61
Branch: `feature/next-118-consultant-terminology`
Rollen: developer, methodologist, reviewer
Reviewklasse: B

## Anlass

Die reale NEXT-118-Evaluation zeigte, dass die bisherige UI ohne Methoden-Vorwissen schwer verständlich war. Insbesondere `Hard Gates`, `Claim`, `Evidence`, `Req`, `Cap`, `Trust`, `UNVERIFIED` sowie mehrere englische Gate-/Evidence-Request-Titel waren als primäre Consultant-Sprache ungeeignet.

## Quellen / Herleitung

Die sichtbaren Begriffe und Übersetzungen wurden aus folgenden bestehenden Projektquellen abgeleitet:

- `docs/product/CONSULTANT_TERMINOLOGY.md`
- `docs/product/HARD_GATE_PLAIN_LANGUAGE_EXAMPLE.md`
- `data/method/r4_hard_gates.csv`
- `data/method/evidence_request_catalog.csv`
- Finding aus NEXT-118 / Issue #50

Es wurden keine Gate-Regeln, Stufenbedeutungen oder externen Normanforderungen neu erfunden.

## Umsetzung

Neuer Frontend-Layer:

`apps/web/src/consultantTerminology.ts`

Er trennt stabile interne Datenbegriffe von sichtbarer Consultant-Sprache.

### Primäre UI

- `Evidence` -> `Nachweise`
- `Hard Gates` -> `Zwingende Mindestanforderungen (K.O.-Kriterien)`
- `Claim` -> `geprüfte Feststellung`
- `Requirement` -> `geforderte Mindeststufe`
- `Applied Capability` -> `nachgewiesener Erfüllungsgrad`
- `Evidence Trust` -> `Belegstärke`
- `Review Status` -> `Prüfstatus`
- PASS -> `Mindestanforderung erfüllt`
- FAIL -> `Mindestanforderung nicht erfüllt`
- UNVERIFIED -> `nicht ausreichend belegt`
- N/A -> `nicht anwendbar`

### Gate-Darstellung

Alle HG-01 bis HG-08 haben einen deutschen Primärnamen und einen kurzen erklärenden Prüfgegenstand. Die interne Gate-ID bleibt sichtbar; der interne Methodenname wird in der Detailansicht sekundär angezeigt.

Die Kacheln zeigen nun:

- `Gefordert: Stufe X`
- `Erfüllungsgrad: ...`
- `Belegstärke: ...`
- verständlichen Status-Badge

### Evidence Requests

ER-001 bis ER-012 werden mit deutschem Titel, deutscher Prüffrage und deutschen Beispiel-Nachweisen dargestellt. Request-IDs bleiben unverändert sichtbar und auditierbar.

### Nachweisprüfung

Sichtbare Begriffe wurden lokalisiert:

- Nachweiszustand
- Prüfstatus
- Ausgangs-Belegstärke
- Passung zum Assessment
- Aktualität
- wirksame Belegstärke

Interne Werte wie `configured`, `reviewed`, `PASS` etc. werden nicht verändert.

### Geprüfte Feststellungen

Der bisherige technische `Claims / Human Review`-Editor verwendet jetzt Consultant-Sprache. Die Persistenz/API bleibt unverändert.

## 0–4-Skala

Die Oberfläche bezeichnet 0–4 ausdrücklich als **interne Operationalisierung des Radars und nicht als offizielle Normskala**. Dieser PR verändert weder Stufenlogik noch Requirement Defaults oder Override-Wirkung. Die weitergehende Override-Governance bleibt #51.

## Layout

Da deutsche Statuslabels länger als PASS/FAIL sind, dürfen `.state-badge`-Elemente jetzt umbrechen. Das verhindert Überlauf in Gate-Kacheln, ohne andere Badge-Typen zu verändern.

## Regression

`tests/test_consultant_terminology.py` prüft:

- Mapping für alle 8 HG-Gates;
- Mapping für alle 12 gate-bezogenen Evidence Requests ER-001 bis ER-012;
- interne Zustandswerte bleiben im Mapping vorhanden;
- zentrale Consultant-Bezeichnungen sind implementiert.

## Abgrenzung

Unverändert:

- API-Enums und IDs
- Export-/Backup-Schema
- Gate-Berechnung
- Trust-Berechnung
- Claim-Wirksamkeit
- Requirement Defaults
- Provenienz

## Offene Punkte

- #51: Mindeststufen/Override-Governance, Begründung und Audit der manuellen Änderung.
- Reale NEXT-118-UI-Prüfung nach Deployment bleibt erforderlich; automatisierte Tests ersetzen nicht die Consultant-Betrachtung.
