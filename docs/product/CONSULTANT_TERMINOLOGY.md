# Consultant-freundliche Terminologie

Status: Entwurf aus NEXT-118 Manual Evaluation
Datum: 2026-09-04
Provenienz: evidence-observation + internal-method

## Ziel

Die Weboberfläche soll Fachlichkeit erhalten, aber keine unnötigen englischen oder manager-/entwicklerzentrierten Begriffe voraussetzen. Interne Modellbegriffe und stabile Codes dürfen in API, Export und Auditspur bestehen bleiben; die Consultant-UI verwendet verständliche deutsche Bezeichnungen und kurze Erklärungen.

## Leitprinzip

**Interner Methoden-/Datenbegriff != zwingend sichtbarer UI-Begriff.**

Die UI erklärt zuerst die Sache in normaler Sprache; der interne Begriff kann sekundär in Klammern, Tooltip, Detailansicht oder Export erscheinen.

## Vorschlag für die Gate-Oberfläche

| Interner Begriff | Consultant-UI | Erklärung |
|---|---|---|
| Hard Gates | Zwingende Mindestanforderungen (K.O.-Kriterien) | Anforderungen, die nicht durch Stärken an anderer Stelle ausgeglichen werden können. |
| non-compensable | nicht durch andere Stärken ausgleichbar | Beispiel: Eine zwingende Vorgabe zum Rechts-/Kontrollraum bleibt verletzt, auch wenn Security oder Exit sehr gut sind. |
| Claim | geprüfte Feststellung | Vom Consultant verantwortete Aussage, die sich auf Nachweise stützt. |
| Evidence | Nachweis / Beleg | Dokument, Export, Konfiguration, Test, Beobachtung oder sonstige Quelle, die eine Aussage stützt. |
| Evidence Request | benötigter Nachweis | Welcher Beleg für die Prüfung noch benötigt wird. |
| Requirement | geforderte Mindeststufe | Internes Anforderungsniveau des konkreten Gates. |
| Applied Capability | nachgewiesener Erfüllungsgrad | Wie weit die Anforderung im konkreten Assessment nach bestätigten Feststellungen tatsächlich erfüllt ist. |
| Evidence Trust | Belegstärke / Nachweisvertrauen | Wie belastbar, passend und aktuell die verwendeten Nachweise sind. |
| Human Review | Prüfung durch Consultant | Menschliche fachliche Prüfung vor Wirksamkeit in der Bewertung. |
| Review Status | Prüfstatus | Entwurf, geprüft, freigegeben, verworfen. |
| UNVERIFIED | nicht ausreichend belegt | Es fehlen bestätigte Aussagen oder ausreichend belastbare Nachweise. |
| PASS | Mindestanforderung erfüllt | Deterministisches Ergebnis nach bestätigten Aussagen/Nachweisen. |
| FAIL | Mindestanforderung nicht erfüllt | Geforderte Mindeststufe wird nach bestätigten Aussagen/Nachweisen nicht erreicht. |
| N/A | nicht anwendbar | Gate ist für den konkreten Scope nicht anzuwenden. |

## Karten-/Kacheltext

Statt:

`Req 2 · Cap ? · Trust ?`

soll die Consultant-UI z. B. zeigen:

- `Gefordert: Stufe 2`
- `Erfüllungsgrad: noch offen`
- `Belegstärke: noch offen`
- `Status: nicht ausreichend belegt`

Die internen Kurzformen `Req`, `Cap`, `Trust` bleiben optional für Debug-/Methodendetails.

## Beispiel HG-01

Statt:

`Jurisdiction & Effective Control`

primär:

**Rechtsraum und tatsächliche Kontrolle**

Sekundär kann der interne/englische Methodenname angezeigt werden.

## Claim-Formular

Statt `Claims / Human Review`:

**Geprüfte Feststellungen**

Hilfetext:

> Hier hält der Consultant fachliche Aussagen fest, die auf Nachweisen beruhen. Erst geprüfte oder freigegebene Feststellungen dürfen die Bewertung einer zwingenden Mindestanforderung beeinflussen. KI-Vorschläge werden niemals automatisch übernommen.

Felder:

- `Aussage` -> `Feststellung / Aussage`
- `Capability Level` -> `Erfüllungsgrad`
- `Review Status` -> `Prüfstatus`
- `Question IDs` -> `Verknüpfte Fragen`
- `Supporting Evidence` -> `Stützende Nachweise`
- `Claim speichern` -> `Feststellung speichern`

## Evidence-Requests

Evidence-Request-Titel und Beschreibungen sollen deutsch angezeigt werden. Interne IDs wie `ER-001` bleiben sichtbar/auditierbar, aber nicht erklärungsbedürftige englische Labels als Primärtext.

## Methodengrenze

Diese Terminologieänderung verändert keine Gate-Logik, Schwellenwerte, Claim-Wirksamkeit oder Provenienz. Sie betrifft ausschließlich Verständlichkeit und UX.
