# Contributing

## Workflow

1. Issue oder klarer Task.
2. Branch von `main`.
3. Änderungen klein und nachvollziehbar halten.
4. Quellen-/Provenienzinformation ergänzen.
5. Tests/Validierung ausführen.
6. PR anhand des Templates erstellen.
7. Reviewpunkte abarbeiten.
8. Bevorzugt squash-merge nach Freigabe.

## Commit-Konvention

Empfohlen:

- `method:` Methodik/Regelwerk
- `research:` Quellen/Crosswalk
- `feat:` Softwarefunktion
- `fix:` Fehlerkorrektur
- `test:` Tests
- `docs:` Dokumentation
- `chore:` Repo/CI/PM

## Daten und Evidence

Keine Secrets, personenbezogenen Kundendaten oder unredigierten account-spezifischen Raw-Evidence-Dumps committen. Für technische Evidence nur synthetische Fixtures oder explizit freigegebene, redigierte Beispiele verwenden.

## Änderungen an Regeln/Schwellen

Jede Änderung an Scoring, Hard Gates, Trust-Leveln oder Default-Schwellen benötigt:

- Decision/Issue-Referenz
- Provenienzklasse
- Begründung
- Grenzwerttests
- Hinweis, ob externe Vorgabe oder internes Default
