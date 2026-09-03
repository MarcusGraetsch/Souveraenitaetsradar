# Agent Session – NEXT-114 Synthetic Consultant Walkthrough

Datum: 2026-09-03
Rollen: evidence-analyst, developer, methodologist, reviewer
Issue: #18
Branch: `feature/next-114-synthetic-walkthrough`
PR: #19

## Ausgangslage

NEXT-112 wurde nach grüner CI als PR #17 nach `main` gemerged (`85caf27f091ed728585c1db969eb325695f7e1db`). Damit sind Evidence Review, Human-reviewed Claims, Gate Requirements und alle acht Hard Gates operativ in der Webanwendung vorhanden.

Der nächste Schritt war bewusst **Validation vor Feature-Ausbau**.

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

- `docs/validation/NEXT_114_RESULT_2026-09-03.md`
  - tatsächliches Validierungsergebnis einschließlich CI, Gate States, LLM Governance, Lifecycle und UX-Finding dokumentiert.

## Tatsächlicher Validierungslauf

GitHub Actions Run: `33789278423`
Artifact: `synthetic-consultant-walkthrough`, ID `9906680972`
Digest: `sha256:400c4ca2334a7ece036e10561c67f418ff02e5fdb2e25a3d561a4a63e0a97a91`

Alle vier Jobs waren grün:

- `python`
- `frontend`
- `compose-smoke`
- `consultant-walkthrough`

Der `consultant-walkthrough` bestätigte nacheinander:

1. Clean Checkout + `install.sh`
2. API/Web Health
3. synthetisches Assessment + Relevanzprofil
4. Guided Question Path
5. reviewed Beispielantwort
6. synthetische Evidence
7. Evidence Review / Trust
8. Human-reviewed Claims
9. Gate Requirement Overrides
10. Hard-Gate Evaluation
11. LLM Bridge Negative Control
12. JSON Report
13. `stop.sh`
14. `start.sh`
15. `test.sh`
16. `uninstall.sh` mit `DELETE`
17. Prüfung auf entfernte `.runtime`, `.env` und Container-Reste

## Laufzeitresultate

Methodenfragen insgesamt: **128**

Guided Workflow im komplexen KI-Agent-Fall:

- 124 im relevanten Standardpfad
- 83 `applicable`
- 41 `needs_review`
- 4 `not_applicable`

Gate States:

- HG-01 PASS
- HG-02 N/A
- HG-03 FAIL
- HG-04 UNVERIFIED
- HG-05 N/A
- HG-06 N/A
- HG-07 N/A
- HG-08 N/A

Evidence:

- 2 synthetische Evidence-Objekte
- beide reviewed
- Effective Trust 4

Claims:

- 3 human-reviewed Capability Claims
- 1 draft Negativkontroll-Claim
- draft Capability 4 für HG-03 änderte den reviewed Capability-1-Befund nicht

LLM Bridge:

- Importstatus `valid`
- 1 synthetisches Proposal
- Claim Count vorher 4, nachher 4
- Gate States unverändert

Damit wurden alle NEXT-114-Acceptance Checks erfüllt.

## Neues Finding → NEXT-115 / Issue #20

Der konservative Applicability-Mechanismus hat korrekt verhindert, dass unklare Fragen verschwinden. Produktseitig ist der Fragenpfad bei komplexen Workloads aber noch nicht ausreichend priorisiert: **124/128** ist operativ fast wieder ein Vollfragebogen.

Dafür wurde Issue #20 als **NEXT-115 / P0** angelegt:

`Guided Workflow progressiv priorisieren (KI-Agent: 124/128 aktiv)`

Ziel ist nicht aggressiveres Wegfiltern, sondern deterministisches Staging:

- Screening / Jetzt beantworten
- sichtbare `needs_review`-Klärungsqueue
- deterministisch aktivierter Deep Dive
- All-Questions/Audit View bleibt vollständig

LLM darf nicht über Applicability oder Stage entscheiden.

## Wichtige methodische Grenzen

1. Der Fall enthält **keine realen Providerfakten**. Alle technischen/vertraglichen Aussagen sind synthetische Validierungsannahmen.
2. Gate Requirement Overrides in diesem Test sind reine Testkonfiguration, keine regulatorischen Schwellen.
3. PASS/FAIL/UNVERIFIED wurden gezielt isoliert, um die Regelkette zu prüfen; der Test ist keine vollständige reale Risikobewertung eines KI-Systems.
4. `N/A` bei den übrigen Gates bedeutet nur Requirement 0 im isolierten Gate-Test, nicht generelle Irrelevanz für reale KI-Agenten.
5. Das 124/128-Finding darf nicht durch Verstecken von `needs_review` „gelöst“ werden.

## Leitplanken für andere Agents

- Keine echten Providermerkmale in den synthetischen Fixture-Text hineininterpretieren.
- Keine LLM-Proposals automatisch in Claims/Answers/Gates übernehmen.
- Fehlende Evidence weiterhin als UNVERIFIED behandeln.
- Requirement-Defaults und Test-Overrides immer als interne Operationalisierung kennzeichnen.
- `needs_review` sichtbar halten; Priorisierung/Staging statt stilles Wegfiltern.
- LLM nicht zum deterministischen Applicability-/Stage-Entscheider machen.
- Echte Findings als eigene Issues dokumentieren; Tests nicht durch Abschwächen der Akzeptanzkriterien grün machen.
- Raw Kundenevidence nie committen.

## Nächster Schritt

Nach finaler CI auf dem dokumentierten Branch-Stand PR #19 mergen und NEXT-114 schließen. Danach NEXT-115 auf eigenem Branch implementieren. NEXT-113 Backup/Export/Report bleibt dahinter P1.
