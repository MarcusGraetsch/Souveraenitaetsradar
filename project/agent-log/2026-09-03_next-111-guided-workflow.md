# Agent Session – NEXT-111 Guided Workflow

Datum: 2026-09-03
Rollen: methodologist, developer, reviewer (Self-Review)
Issue: #13
PR: #14
Branch: `feature/next-111-guided-workflow`

## Ziel

Den statischen 128-Fragen-Katalog in einen nachvollziehbaren Consultant-Fragenpfad überführen, ohne die Anwendbarkeit durch ein LLM entscheiden zu lassen und ohne unklare Fragen still auszublenden.

## Umgesetzt

- neues deterministisches Modul `src/sovradar/applicability.py`
- drei Zustände: `applicable`, `not_applicable`, `needs_review`
- konservative Behandlung unbekannter/nicht operationalisierter Bedingungen als `needs_review`
- separates persistiertes Assessment-Relevanzprofil
- API für Relevanzprofil und assessment-spezifischen Fragenpfad
- Web-UI für Relevanzprofil
- Standardansicht `Relevante Fragen` plus transparente Ansicht `Alle Fragen`
- sichtbare Applicability-Begründung je Frage
- LLM Bridge erhält nur relevante bzw. zu prüfende offene Fragen
- Ergebnisübersicht zählt nur aktive Fragen
- Core- und API-Tests für unterschiedliche Fragenpfade

## Methodische Entscheidung

Die natürliche Spalte `Anwendbarkeit` der bestehenden Question Bank bleibt fachliche Source-of-Truth. Der neue Code operationalisiert zunächst nur Bedingungen, die aus expliziten generischen Scope-Fakten sicher ableitbar sind. Eine unbekannte Formulierung wird nicht heuristisch weggedeutet, sondern als `needs_review` sichtbar gehalten.

Das Relevanzprofil ist Scope-Kontext und wird bewusst nicht als normale Fragenantwort gespeichert. Beispiele: KI-Nutzung, Datenverarbeitung, Verschlüsselung, Schlüsselmodell, Exit-Relevanz, Unterauftragnehmer, IAM und Logging.

## Tests / Acceptance

PR-CI Run `33762878013` war vor dem finalen Status-/Handoff-Commit vollständig grün:

- Repository Validator: PASS
- bestehende Core Tests: PASS
- `tests/test_applicability.py`: PASS
- FastAPI Tests inkl. Profil-/Fragenpfad: PASS
- TypeScript/Vite Build: PASS
- Docker Compose Build/Runtime Smoke: PASS

Expliziter Boundary-Test: fehlender Kontext bei `wenn Verschlüsselung` ergibt `needs_review` und entfernt die Frage nicht aus dem relevanten Pfad.

Nach den finalen Projektstatus-Updates muss die PR-CI nochmals vollständig grün sein, bevor gemerged wird.

## Bekannte Grenzen

- Die Question Bank enthält viele natürliche Anwendbarkeitsformulierungen. Noch nicht modellierte Ausdrücke bleiben korrekt als `needs_review` sichtbar.
- Das Relevanzprofil ist MVP-Scope und noch kein vollständiges Discovery-/BIA-Datenmodell.
- Eine echte Hard-Gate-Auswertung gehört in NEXT-112 / Issue #15.
- LLM-Vorschläge können weiterhin noch nicht einzeln per Human-Review in Antworten übernommen werden.

## Handoff

NEXT-111 ist funktional implementiert. Nächster P0-Produkt-/Methodenschritt ist `NEXT-112` / Issue #15: `Evidence -> Claim -> Hard Gate`.

Dabei zwingend beibehalten:

1. alle acht Hard Gates.
2. fehlende/unzureichende Evidence = `UNVERIFIED`.
3. technische Mindestunterschreitung kann `FAIL` ergeben.
4. `PASS` nur mit ausreichender technischer und Evidence-Grundlage.
5. Provider Capability und Applied Capability getrennt.
6. LLM-Vorschläge ohne Human Review haben keine Gate-Auswirkung.

Guided-Workflow-UX zusätzlich im ersten synthetischen End-to-End-Durchlauf (NEXT-114) prüfen.

Provenienz: `INT-03` / interne Produkt- und Methodenoperationalisierung. Keine externe Norm wird durch die Applicability-Regeln neu behauptet.
