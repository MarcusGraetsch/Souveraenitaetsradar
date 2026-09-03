# Method Overview

## 1. Prozesskern

Der Radar orientiert sich für Risikoanalyse/-behandlung an BSI-200-3-/ISO-27005-artiger Logik: Scope, relevante Gefährdungen, Risikoanalyse, Behandlung und Akzeptanz. Souveränitätsspezifische Gefährdungen werden als zusätzliche, explizit interne Risikotypen geführt.

## 2. Drei Ebenen

### Provider / Service Capability

Was bietet/garantiert der Dienst grundsätzlich?

### Applied Capability

Was nutzt der konkrete Kunde/Workload tatsächlich?

Zustände:

`available -> selected -> configured -> tested -> attested`

### Workload Risk

Welche Konsequenz hat die konkrete Abhängigkeit für den Geschäftsprozess?

## 3. Bewertungsachsen

- Sovereignty Capability
- Workload Sovereignty Risk
- Security/Operational Risk
- Evidence Confidence

Keine dieser Achsen darf eine andere still kompensieren.

## 4. Hard Gates

Siehe `data/method/r4_hard_gates.csv`.

1. Jurisdiktion & Effective Control
2. Datenresidenz & Verarbeitung
3. Schlüsselhoheit
4. Exit & Portabilität
5. Operational Autonomy
6. Identity & Trust Anchors
7. Supply Chain Critical Dependencies
8. Security Minimum

## 5. Gate first, score second

Wenn eine für den Workload nicht kompensierbare Mindestanforderung nicht erfüllt ist, darf ein hoher gewichteter Vergleichswert diesen Fail nicht wegmitteln.

## 6. Evidence

Evidence besitzt mindestens:

- Quelle
- Scope
- Zeit/Version
- Trust
- Scope Fit
- Applied State

Fehlende Evidence führt zu `UNVERIFIED`.

## 7. Strukturelle Risiken

Lock-in, Konzentration oder Jurisdiktionsabhängigkeit sind nicht sinnvoll nur als seltenes Ereignis zu modellieren. Der Radar trennt:

`strukturelle Exposition -> möglicher Trigger -> Auswirkung`.

## 8. KI

Für KI-/Agentensysteme werden mindestens getrennt betrachtet:

- Data Control
- Model Portability
- Agent/Tool/Policy Portability
- Tool Authorization und Side Effects
- Model-/Provider-/Terms-Drift

## 9. Provenienz

Alle Fragen, Regeln und Schwellen müssen externe Vorgabe, externe Ableitung, internes Methodendesign oder Projektannahme sichtbar machen.
