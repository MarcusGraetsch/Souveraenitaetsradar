# Source Guide

Externe und projektbezogene Quellen liegen in `data/method/source_register.csv`. Interne Herleitungen und Runtime-/Methoden-Operationalisierungen liegen in `data/method/source_register_addendum_v1.csv`.

Beide Dateien bilden gemeinsam die aktuelle Provenienzreferenz. History-/Agent-Log-Dateien ersetzen das Source Register nicht.

Für C3A v1.0 gilt zusätzlich der abgeschlossene Volltextreview `docs/method/C3A_V1_0_REVIEW.md` und der maschinenlesbare Crosswalk `data/method/c3a_v1_0_crosswalk.csv`.

## Aktueller Quellenstatus: C3A

`SRC-04` (BSI C3A – Criteria enabling Cloud Computing Autonomy) wurde am 08.09.2026 **als vollständiger Volltext** gegen Methodenkern v0.4, Provider Intelligence, Hard Gates, Question Library und Risikotaxonomie geprüft.

Der Review bestätigt die Grundarchitektur, führt aber zu wichtigen Präzisierungen: C3A deckt SOV-1 bis SOV-6 ab, setzt C5-Erfüllung voraus, unterscheidet `Criterion` und `Additional Criterion`, lässt den Kunden use-case-abhängig Kriterien auswählen und verwendet EU-/Deutschlandvarianten als Anforderungsalternativen, nicht als Reifegradleiter.

## Grundsatz: Frameworks nicht stapeln

Der Radar führt **nicht automatisch mehrere vollständige Framework-Assessments parallel** durch. Quellen werden nach ihrer Funktion eingesetzt. Ein Framework kann eine Methoden-/Fragenquelle sein, ohne dass seine regulatorische oder formale Anwendbarkeit für den Kunden behauptet wird.

## Quellenrollen im Souveränitäts-Radar

| Rolle | Wichtige Quellen | Verwendung |
|---|---|---|
| **Orientierung / Entscheidungslogik** | `SRC-17` Bitkom Cloud-Souveränität 2026 | Handlungsfähigkeit, Risiko/Chance, Skills, Interdependenzen, Exit, organisatorische und politisch-regulatorische Risiken |
| **Provider-/Service-Souveränität** | `SRC-03`, `SRC-24` EU Cloud Sovereignty Framework | Souveränitätsdimensionen, Provider-/Service-Fragen, Evidence- und Bewertungslogik |
| **Provider-/Service-Autonomie** | `SRC-04` BSI C3A v1.0 | objektive/verifizierbare Kriterien für selbstbestimmte Cloud-Nutzung; SOV-1 bis SOV-6; Criterion/Additional Criterion; kundenabhängige Auswahl |
| **Security-/Risiko-Deep-Dive** | `SRC-01` BSI 200-3; `SRC-02` IT-Grundschutz; `SRC-22` ISO/IEC 27005; `SRC-15` NIST SP 800-30 | Zielobjekte, Gefährdungen, Risikoanalyse/-behandlung, Vollständigkeitscheck |
| **Security Assurance** | `SRC-05` BSI C5 | Provider-Control-/Assurance-Evidence; C3A setzt C5-Erfüllung voraus; kein automatischer Workload-Eignungsnachweis |
| **Exit / Switching / Portabilität** | `SRC-12` Data Act; ergänzend `SRC-08`, `SRC-17` | Wechsel zu anderem Provider oder On-Prem, Vertrags-/Portierungs-/Interoperabilitätsfragen; C3A SOV-6 ist hierfür nicht die Primärquelle |
| **Drittparteien / Konzentration / Exit** | `SRC-08` DORA, `SRC-09`, `SRC-10` | für Finanzunternehmen Compliance-Overlay; sonst methodische Quelle für Substituierbarkeit, Konzentration, Register-/Abhängigkeitsmodell |
| **Cyber-Risikomanagement** | `SRC-06` NIS2-DVO, `SRC-07` ENISA | Compliance-Overlay, wenn anwendbar; sonst Bestätigung für dokumentierte Risiko-/Behandlungsprozesse |
| **Legal / Drittland** | `SRC-11` EDPB | Transfer-/Jurisdiktionsprüfung, soweit einschlägig |
| **Öffentliche Verwaltung** | `SRC-21` BSI Mindeststandard externe Cloud-Dienste | spezifisches Overlay für einschlägige öffentliche Stellen |
| **KI** | `SRC-13`, `SRC-18`, `SRC-19` | KI-spezifische regulatorische/technische Overlays |
| **Enterprise-Architecture-Import** | `SRC-56` ArchiMate Model Exchange File Format | optionaler strukturierter Intake von Elementen/Beziehungen; kein Pflichtformat |
| **Provider Intelligence** | Provider-Primärdokumentation, C3A-/C5-Evidence und unabhängige Assurance | wiederverwendbare Provider-/Service-Capability-Evidence mit Scope, Version und Review |

## C3A v1.0 – verbindliche Interpretationsregeln

1. **C3A ist ein Guiding Framework und selbst nicht bindend.** Der Kunde bestimmt abhängig vom Use Case, welche Kriterien für seinen Souveränitätsbedarf relevant sind.
2. **C3A deckt SOV-1 bis SOV-6 ab.** SOV-7 Security & Compliance wird bewusst durch C5:2026/IT-Grundschutz/weitere BSI-Publikationen adressiert; SOV-8 liegt außerhalb des BSI-Aufgabenbereichs.
3. **C3A setzt C5-Erfüllung des Cloud-Service-Providers voraus.** Ohne belastbare C5-Grundlage darf der Radar keine formale C3A-Erfüllung behaupten. Einzelne C3A-Kriterien können trotzdem als Methoden-/Anforderungsquelle genutzt werden.
4. **Criterion (`C`) und Additional Criterion (`AC`) sind keine Reifegradstufen.** AC werden nur aktiviert, wenn der Kunde sie entsprechend seinem Souveränitätsbedarf verlangt.
5. **EU- und Deutschland-Varianten sind alternative Anforderungsprofile, keine Score-Leiter.** Deutschlandrestriktionen müssen dort, wo C3A dies anspricht, begründet und insbesondere im Beschaffungskontext rechtlich zulässig sein.
6. **C3A bewertet einen konkreten Satz von Cloud-Services.** Providername oder Konzernherkunft allein reichen nicht.
7. **C3A SOV-6 Technology Sovereignty beschreibt primär die Fortführungs-/Entwicklungsfähigkeit des Providers.** Kundenseitiger Exit/Portabilität bleibt primär Data-Act-/DORA-/Bitkom-/Radar-Thema.
8. **C3A-Datenklassen werden getrennt behandelt:** Account Data, Cloud Service Customer Data, Cloud Service Derived Data, Cloud Service Provider Data.

## Priorisierung für die sichtbare Beratungsmethode

1. Kundenentscheidungsfrage, Ziele und Optionen verstehen.
2. Bitkom-/Souveränitätslogik für Handlungsfähigkeit und Trade-offs nutzen.
3. EU-CSF für den breiten Provider-/Service-Souveränitätsrahmen nutzen.
4. C3A kriterienscharf als Provider-/Service-Autonomieprofil aktivieren, wenn dies für den Kundenfall relevant ist.
5. C5-/Security-Voraussetzungen und Security-/Resilienzanforderungen separat prüfen.
6. BSI 200-3 / IT-Grundschutz bei Bedarf als Security-/Resilienz-Deep-Dive und Vollständigkeitscheck nutzen.
7. Data Act für Exit-/Switching-Aspekte prüfen.
8. Nur die für Kunde/Workload tatsächlich einschlägigen Compliance-Overlays aktivieren.

## Prüffragen vor einer kundenseitigen Aussage

1. Quelle aktuell?
2. richtige Version?
3. richtige Service-/Region-/Offering-/Legal-Entity-Scope?
4. direkte Quelle oder eigene Ableitung?
5. regulatorisch/formal tatsächlich anwendbar oder nur Methodenquelle?
6. bei C3A: Criterion oder Additional Criterion – und vom Kunden tatsächlich gefordert?
7. bei C3A: EU- oder Deutschland-Anforderungsvariante – und sachlich/rechtlich begründet?
8. bei C3A-Konformitätsaussage: C5-Voraussetzung für denselben Scope belastbar nachgewiesen?
9. ist ein Vertrag/Test/Attest statt Provider-Selbstauskunft erforderlich?
10. kann die Aussage die Empfehlung materiell verändern – und ist dafür die Evidenztiefe angemessen?

## Verbotsregeln

- Eine Aussage wie „US-Provider = unsouverän“ oder „deutscher Provider = souverän“ ist keine zulässige Methodenregel. Herkunft/Jurisdiktion sind Fakten, die in konkrete, prüfbare Risiko- und Abhängigkeitsszenarien übersetzt werden müssen.
- Eine C3A-Deutschlandvariante darf nicht automatisch als „höhere Souveränitätsstufe“ als die EU-Variante gewertet werden.
- Ein erfülltes C3A-Einzelkriterium darf nicht als C3A-Gesamtkonformität ausgegeben werden.
- C3A SOV-6 darf nicht pauschal als Beleg für kundenseitige Exit-Portabilität zitiert werden.
