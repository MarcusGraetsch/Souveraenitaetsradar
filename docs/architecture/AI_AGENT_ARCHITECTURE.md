# AI Agent Architecture

## Ziele

Mehrere KI-Systeme sollen das Repository verstehen und ohne proprietären Chatkontext weiterarbeiten können.

## Kanonische Steuerung

`AGENTS.md` ist die einzige kanonische Agentenpolicy. Modell-/Tool-spezifische Einstiegsdateien dürfen nur darauf verweisen.

## Agentenaufgaben

Geeignet:

- Quellen suchen und Fundstellen extrahieren
- Dokumente strukturieren
- Claims/Evidence vorschlagen
- Widersprüche finden
- Folgefragen generieren
- Code/Tests implementieren
- PRs reviewen
- Handoffs/Status pflegen

Nicht autonom freigeben:

- Risikoakzeptanz
- rechtliche Schlussentscheidung
- produktive Security-Ausnahme
- Änderung harter Management-Mindestanforderungen

## Shared Context

Agenten sollen Zustand aus Dateien lesen, nicht aus „wer vorher welches Modell war“. Jede Session schreibt Handoff/Log, wenn sie substantiell ist.

## Parallelität

Parallel arbeitende Agenten sollen möglichst getrennte Branches/Issues nutzen. Änderungen an denselben Methodenkernen oder State-Dateien sind zu koordinieren.
