# HITL-Entscheidungsvorlage – Assessment Intake v0.5

Stand: 2026-09-09

Diese Vorlage dient der menschlichen Freigabe des neuen Assessment-Einstiegs. Sie ersetzt keine Runtime-Implementierung.

## Entscheidung A – UI-Muster
- A1: 3–4-stufiger Wizard
- A2: ein Formular mit progressiv aufklappbaren Bereichen

Empfehlung: A1 Wizard, weil Organisations-, Workload- und Compliance-Fakten semantisch getrennt bleiben und die erste Seite nicht überladen wird.

## Entscheidung B – Workload-Klassifikation
- B1: ein Primärtyp + mehrere Tags
- B2: reine Mehrfachauswahl ohne Primärtyp
- B3: nur freie Beschreibung

Empfehlung: B1. Der Primärtyp hält Routing/Reporting stabil, Tags modellieren Überschneidungen, Freitext bleibt zusätzlich erhalten.

## Entscheidung C – Compliance
- C1: bereits in v0.5 regelbasierte Compliance-Kandidaten erzeugen
- C2: in v0.5 zunächst nur die nötigen Fakten erfassen; Ableitung später

Empfehlung: C1 in kleinem, transparentem Umfang für DSGVO/NIS2/DORA/AI Act mit `likely_applicable / likely_not_applicable / needs_review`, Begründung, fehlenden Fakten und Human Review. Keine finale Rechtsfeststellung.

## Entscheidung D – C/I/A und Kritikalität
- D1: aus dem Erstellformular entfernen und später als Business-Impact-/Schutzbedarfsreview behandeln
- D2: optional im Erstellformular lassen
- D3: verpflichtend beibehalten

Empfehlung: D1. Ungeprüfte Defaultwerte `medium` erzeugen Scheingenauigkeit.

## Entscheidung E – Konzern / juristische Einheiten
- E1: primäre juristische Einheit + optional mehrere weitere Einheiten im Scope
- E2: zunächst nur eine juristische Einheit
- E3: vollständiges Konzernmodell als Pflicht

Empfehlung: E1. Damit werden Tochter-/Mutterkonstellationen unterstützt, ohne einfache Fälle zu überfrachten.

## Entscheidung F – Pflichtfelder im Minimalpfad
Empfohlene Pflichtfelder:
- Titel des Entscheidungsfalls
- Entscheidungsfrage/Ziel
- Organisationsname
- Organisationstyp
- Sitzland + Ort
- Branche/Sektor
- Unternehmensgröße mindestens als Größenklasse bzw. Beschäftigtenzahl
- Workload-Name
- natürliche Workload-Beschreibung
- primärer Workload-Archetyp
- primäre juristische Einheit/Workload-Zuordnung

Alle weiteren Angaben progressiv/optional bzw. nur bei Routingbedarf.

HUMAN GATE: HITL-08 | Rolle: Product Owner + Method Owner | Freigabe dieser Entscheidungen erlaubt die konkrete Runtime-Implementierung.