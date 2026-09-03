# Agent Session – NEXT-114 Synthetic Consultant Walkthrough

Datum: 2026-09-03
Rollen: evidence-analyst, developer, methodologist, reviewer
Issue: #18
Branch: `feature/next-114-synthetic-walkthrough`

## Ausgangslage

NEXT-112 wurde nach grüner CI als PR #17 nach `main` gemerged (`85caf27f091ed728585c1db969eb325695f7e1db`). Damit sind Evidence Review, Human-reviewed Claims, Gate Requirements und alle acht Hard Gates operativ in der Webanwendung vorhanden.

Der nächste Schritt ist bewusst **Validation vor Feature-Ausbau**.

## Ziel dieser Session

Einen reproduzierbaren End-to-End-Pfad schaffen, der nicht nur Unit Tests, sondern die installierte Anwendung als Consultant benutzt:

`Clean Checkout -> install -> Scope/Profile -> Questions -> Evidence -> Evidence Review -> Claims -> Hard Gates -> LLM Bridge Negative Control -> Result -> stop/start -> uninstall`

## Implementiert

- `tools/validation/synthetic_consultant_walkthrough.py`
  - HTTP-basierter End-to-End-Runner nur mit Python-Standardbibliothek.
  - legt einen providerneutralen synthetischen KI-Agent-Fall an.
  - verwendet keine Cloud-Credentials und keine LLM API.
  - erzeugt bewusst:
    - HG-01 = PASS,
    - HG-03 = FAIL,
    - HG-04 = UNVERIFIED,
    - restliche Gates in diesem isolierten Test = N/A.
  - testet einen draft Capability-4-Claim als Negativkontrolle gegen einen reviewed Capability-1-Claim.
  - importiert ein synthetisches LLM Proposal und prüft, dass weder Claim-Anzahl noch Gate-Ergebnisse verändert werden.
  - schreibt einen JSON-Validierungsbericht.

- `.github/workflows/validate.yml`
  - zusätzlicher Job `consultant-walkthrough`.
  - startet aus sauberem GitHub-Actions-Checkout.
  - führt `./install.sh` mit lokalen Defaults aus.
  - führt den synthetischen Assessment-Runner aus.
  - prüft `./stop.sh`, `./start.sh`, `./test.sh`.
  - führt `./uninstall.sh` mit explizitem `DELETE` aus.
  - prüft, dass `.runtime` und `.env` entfernt wurden und keine Radar-Container verbleiben.
  - lädt den JSON-Bericht als CI-Artifact hoch.

- `docs/validation/NEXT_114_SYNTHETIC_WALKTHROUGH.md`
  - Szenario, erwartete Gate-Zustände, LLM-Negativtest, Lifecycle und Grenzen des Tests dokumentiert.

## Wichtige methodische Grenzen

1. Der Fall enthält **keine realen Providerfakten**. Alle technischen/vertraglichen Aussagen sind synthetische Validierungsannahmen.
2. Gate Requirement Overrides in diesem Test sind reine Testkonfiguration, keine regulatorischen Schwellen.
3. Der Test darf nicht zur „Kalibrierung durch Erwartungsanpassung“ missbraucht werden. Wenn echte Methodik-/UX-Probleme auftreten, separate Issues anlegen.
4. PASS/FAIL/UNVERIFIED werden gezielt isoliert, um die Regelkette zu prüfen; der Test ist keine vollständige reale Risikobewertung eines KI-Systems.
5. `N/A` bei den übrigen Gates bedeutet nur, dass diese im isolierten Gate-Test auf Requirement 0 gesetzt wurden, nicht dass sie für reale KI-Agenten irrelevant wären.

## Leitplanken für andere Agents

- Keine echten Providermerkmale in den synthetischen Fixture-Text hineininterpretieren.
- Keine LLM-Proposals automatisch in Claims/Answers/Gates übernehmen.
- Fehlende Evidence weiterhin als UNVERIFIED behandeln.
- Requirement-Defaults und Test-Overrides immer als interne Operationalisierung kennzeichnen.
- Bei CI-Fehlern zuerst unterscheiden zwischen Runner-/Lifecycle-Bug und echtem Produkt-/Methodik-Finding.
- Echte Findings als eigene Issues dokumentieren; NEXT-114 nicht durch Abschwächen der Akzeptanzkriterien grün machen.
- Raw Kundenevidence nie committen.

## Nächster Schritt nach grünem CI-Lauf

1. CI-Artifact und Logs prüfen.
2. Falls der Walkthrough methodische oder UX-Probleme zeigt: separate Issues anlegen und priorisieren.
3. Wenn die Akzeptanzkriterien erfüllt sind, NEXT-114 schließen und auf `main` mergen.
4. Danach voraussichtlich NEXT-113 (Backup/Export/Consultant Report) starten, bevor ein realer Provider-/Kundenpilot folgt.
