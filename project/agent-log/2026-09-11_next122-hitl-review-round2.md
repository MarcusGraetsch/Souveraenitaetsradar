# NEXT-122 – HITL Review Runde 2

Datum: 2026-09-11
Rollen: Product Owner, Method Owner, Test-Consultant
PR: #78
Issue: #77

## Anlass

Der Product Owner hat den neuen Assessment Intake v0.5 auf einer realen Test-VM manuell geprüft.

## Findings

1. `Branche / Sektor` als Freitext ist zu offen.
2. `Konzern-/Gruppenstruktur = ja/nein/unklar` ist für den frühen Intake unklar und nicht hinreichend entscheidungsrelevant.
3. Technische Tag-Codes sind für Menschen ungeeignet.
4. Schritt 4 vermittelte nicht klar genug, ob bereits gespeichert wurde; der Speichern-Button war nicht ausreichend sichtbar.
5. Compliance-Codes und Statuswerte waren zu maschinennah dargestellt.

## Umgesetzte Korrekturen

- Primärer Sektor als kuratiertes Dropdown; `Tätigkeit / Zusatzinfo` als separates Freitextfeld.
- `Sonstiges` verlangt Zusatzinfo.
- Sektor ist ausdrücklich Routing-Hilfe, keine finale rechtliche Klassifikation.
- Sichtbare Konzern-/Gruppenstruktur-Frage entfernt.
- Mehrgesellschaftsbezug wird über konkrete Legal Entities erfasst; mehrere Entities erzeugen Scope-Komplexität.
- Technische Workload-Tags werden mit deutschen fachlichen Labels dargestellt.
- Schritt 4 heißt `Prüfen & Speichern`.
- Vor Speicherung steht explizit `Noch nicht gespeichert`.
- Eindeutiger CTA: `Assessment speichern & Voranalyse erstellen`.
- Voranalyse erscheint erst nach erfolgreichem POST und mit `Assessment gespeichert ✓`.
- GDPR/AI_ACT und machine statuses werden als DSGVO / EU AI Act bzw. verständliche deutsche Statusbegriffe dargestellt.

## Quellen-/Methodenhinweis

Die Sektor-Auswahlliste ist eine interne Routing-Taxonomie. Sie deckt zentrale NIS2-Sektoren und weitere allgemeine Wirtschaftssektoren ab. Sie ist weder NACE noch eine verbindliche NIS2-/DORA-Klassifikation. Eine formale Wirtschaftszweigklassifikation kann später separat an NACE Rev. 2.1 angebunden werden.

## Governance

- HITL-08: erfüllt.
- HITL-04: bleibt für rechtlich relevante Compliance-Aussagen zwingend.
- HITL-09: bleibt offen; erneuter manueller Test durch Product Owner + Method Owner vor Merge.
