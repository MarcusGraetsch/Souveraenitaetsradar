# Source Guide

Das vollständige Source Register liegt in `data/method/source_register.csv`. Interne Herleitungen liegen ergänzend in `data/method/source_register_addendum_v1.csv`.

## Grundsatz: Frameworks nicht stapeln

Der Radar führt **nicht automatisch mehrere vollständige Framework-Assessments parallel** durch. Quellen werden nach ihrer Funktion eingesetzt. Ein Framework kann eine Methoden-/Fragenquelle sein, ohne dass seine regulatorische Anwendbarkeit für den Kunden behauptet wird.

## Quellenrollen im Souveränitäts-Radar

| Rolle | Wichtige Quellen | Verwendung |
|---|---|---|
| **Orientierung / Entscheidungslogik** | `SRC-17` Bitkom Cloud-Souveränität 2026 | Handlungsfähigkeit, Risiko/Chance, Skills, Interdependenzen, Exit, organisatorische und politisch-regulatorische Risiken |
| **Provider-/Service-Souveränität** | `SRC-03`, `SRC-24` EU Cloud Sovereignty Framework; `SRC-04` BSI C3A | Souveränitätsdimensionen, Fragen, Capability-/Assurance-Evidence |
| **Security-/Risiko-Deep-Dive** | `SRC-01` BSI 200-3; `SRC-02` IT-Grundschutz; `SRC-22` ISO/IEC 27005; `SRC-15` NIST SP 800-30 | Zielobjekte, Gefährdungen, Risikoanalyse/-behandlung, Vollständigkeitscheck |
| **Security Assurance** | `SRC-05` BSI C5 | Provider-Control-/Assurance-Evidence; kein automatischer Workload-Eignungsnachweis |
| **Exit / Switching / Portabilität** | `SRC-12` Data Act | Wechsel zu anderem Provider oder On-Prem, Vertrags-/Portierungs-/Interoperabilitätsfragen |
| **Drittparteien / Konzentration / Exit** | `SRC-08` DORA, `SRC-09`, `SRC-10` | für Finanzunternehmen Compliance-Overlay; sonst methodische Quelle für Substituierbarkeit, Konzentration, Register-/Abhängigkeitsmodell |
| **Cyber-Risikomanagement** | `SRC-06` NIS2-DVO, `SRC-07` ENISA | Compliance-Overlay, wenn anwendbar; sonst Bestätigung für dokumentierte Risiko-/Behandlungsprozesse |
| **Legal / Drittland** | `SRC-11` EDPB | Transfer-/Jurisdiktionsprüfung, soweit einschlägig |
| **Öffentliche Verwaltung** | `SRC-21` BSI Mindeststandard externe Cloud-Dienste | spezifisches Overlay für einschlägige öffentliche Stellen |
| **KI** | `SRC-13`, `SRC-18`, `SRC-19` | KI-spezifische regulatorische/technische Overlays |
| **Enterprise-Architecture-Import** | `SRC-56` ArchiMate Model Exchange File Format | optionaler strukturierter Intake von Elementen/Beziehungen; kein Pflichtformat |
| **Provider Intelligence** | Provider-Primärdokumentation und unabhängige Assurance | wiederverwendbare Provider-/Service-Capability-Evidence mit Scope, Version und Review |

## Priorisierung für die sichtbare Beratungsmethode

1. Kundenentscheidungsfrage, Ziele und Optionen verstehen.
2. Bitkom-/Souveränitätslogik für Handlungsfähigkeit und Trade-offs nutzen.
3. EU-CSF/C3A für Provider-/Serviceeigenschaften heranziehen.
4. BSI 200-3 / IT-Grundschutz bei Bedarf als Security-/Resilienz-Deep-Dive und Vollständigkeitscheck nutzen.
5. Data Act für Exit-/Switching-Aspekte prüfen.
6. Nur die für Kunde/Workload tatsächlich einschlägigen Compliance-Overlays aktivieren.

## Prüffragen vor einer kundenseitigen Aussage

1. Quelle aktuell?
2. richtige Version?
3. richtige Service-/Region-/Offering-/Legal-Entity-Scope?
4. direkte Quelle oder eigene Ableitung?
5. regulatorisch tatsächlich anwendbar oder nur Methodenquelle?
6. ist ein Vertrag/Test/Attest statt Provider-Selbstauskunft erforderlich?
7. kann die Aussage die Empfehlung materiell verändern – und ist dafür die Evidenztiefe angemessen?

## Verbotsregel

Eine Aussage wie „US-Provider = unsouverän“ oder „deutscher Provider = souverän“ ist keine zulässige Methodenregel. Herkunft/Jurisdiktion sind Fakten, die in konkrete, prüfbare Risiko- und Abhängigkeitsszenarien übersetzt werden müssen.
