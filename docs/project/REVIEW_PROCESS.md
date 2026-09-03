# Review Process

## Klassen

### A – Dokumentation / geringe Auswirkung

Beispiele: Tippfehler, Linkfix. Self-review möglich.

### B – Methodik / Datenmodell / Rule Change

Erfordert fachlichen Review. Prüfpunkte:

- Quelle/Fundstelle
- Provenienzklasse
- Auswirkungen auf bestehende Szenarien
- Unit-/Boundary-Tests
- keine stillen Schwellenänderungen

### C – Security-/Evidence-Collector

Erfordert technischen + Security Review. Insbesondere:

- read-only Garantie
- keine Payload-/Secret-Erhebung
- Permission Scope
- Fehlerbehandlung
- Chain of Custody

### D – Legal-/Compliance-Behauptung

Erfordert Primärquelle und bei rechtlicher Bewertung ggf. qualifizierten Human Review. Provider-Selbstauskunft ist als solche zu kennzeichnen.

## PR Review

Ein PR ist mergefähig, wenn:

- Scope klar ist
- Tests grün sind
- Quellen/Provenienz vollständig sind
- keine offenen Blocker vorhanden sind
- Handoff/State bei Bedarf aktualisiert wurde

## Review-Kommentar-Klassen

- `BLOCKER` – Merge nicht zulässig
- `MAJOR` – vor Merge beheben oder explizit entscheiden
- `MINOR` – sollte behoben werden
- `QUESTION` – Klärung
- `NIT` – optional

## Unabhängigkeit

Für grundlegende Methodik oder Security-sensitive Collector-Änderungen soll Reviewer nicht identisch mit dem primären Implementierer sein. Agenten-Self-Review muss explizit als Self-Review markiert werden.
