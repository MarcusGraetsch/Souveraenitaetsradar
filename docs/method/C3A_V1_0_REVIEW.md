# C3A v1.0 – Volltextreview gegen Methodenkern v0.4

Status: **abgeschlossenes Methodenreview vor weiterer Runtime-Entwicklung**  
Datum: 08.09.2026  
Quelle: `SRC-04` – BSI, *Criteria enabling Cloud Computing Autonomy (C3A)*, v1.0, 27.04.2026  
Issue: #68  
Reviewklasse: B – Methode/Architektur

## 1. Ergebnis in einem Satz

C3A bestätigt die Grundrichtung des Souveränitäts-Radars deutlich: **Souveränität ist eine risikokontextabhängige Anforderung an die selbstbestimmte Nutzung konkreter Cloud-Services und muss über objektive, prüfbare Kriterien und Evidence beurteilt werden.** C3A ersetzt jedoch weder den workload-/organisationsspezifischen Variantenvergleich noch Exit-/Business-/Kostenbewertung. Der Radar bleibt deshalb Decision Support; C3A wird ein besonders wichtiger **Provider-/Service-Autonomie- und Evidence-Layer**.

## 2. Was C3A ausdrücklich ist – und was nicht

C3A beschreibt digitale Souveränität als Fähigkeit und Möglichkeit, im digitalen Raum unabhängig, selbstbestimmt und sicher zu handeln. Ausgangspunkt ist das Shared-Responsibility-Modell: Cloud-Nutzung begrenzt den unmittelbaren Entscheidungsspielraum des Kunden; der Provider kann Kundenautonomie ermöglichen oder einschränken.

C3A ist ein **nicht bindender Guiding Framework** mit objektiven und verifizierbaren Kriterien. Cloud-Service-Kunden wählen abhängig vom Use Case und ihren Anforderungen aus, welche Kriterien relevant sind. Provider können für einen konkreten Satz von Cloud-Services die Erfüllung ausgewählter Kriterien durch Evidence/Audit nachweisen.

Daraus folgen für den Radar fünf Leitregeln:

1. keine pauschale Providerbewertung, sondern Service-/Offering-/Scope-Bezug;
2. Kundensouveränität beginnt mit kundenseitig festgelegten Anforderungen;
3. Kriterienerfüllung braucht Evidence, nicht Marketingbehauptungen;
4. C3A-Kriterien sind nicht automatisch für jeden Workload gleich relevant;
5. ein C3A-Ergebnis ist nicht identisch mit der gesamten Managemententscheidung.

## 3. Verhältnis EU CSF, C3A und C5

C3A übernimmt Struktur und Ziele des EU Cloud Sovereignty Frameworks, deckt aber bewusst nur **SOV-1 bis SOV-6** ab:

- SOV-1 Strategic Sovereignty
- SOV-2 Legal & Jurisdictional Sovereignty
- SOV-3 Data Sovereignty
- SOV-4 Operational Sovereignty
- SOV-5 Supply Chain Sovereignty
- SOV-6 Technology Sovereignty

SOV-7 Security & Compliance wird nicht in C3A wiederholt, weil BSI hierfür insbesondere C5:2026, IT-Grundschutz und weitere BSI-Publikationen nennt. SOV-8 Environmental Sustainability liegt außerhalb des BSI-Aufgabenbereichs.

**Wichtig:** C3A setzt voraus, dass der Cloud-Service-Provider die C5-Kriterien erfüllt. Deshalb darf der Radar eine formale C3A-Erfüllung nicht behaupten, wenn diese Voraussetzung für den betrachteten Scope nicht belastbar festgestellt wurde. Einzelne C3A-Kriterien dürfen trotzdem als Methoden-/Anforderungsquelle verwendet werden; daraus entsteht aber keine C3A-Konformitätsaussage.

## 4. C3A Criterion vs. Additional Criterion

C3A unterscheidet:

- **Criterion (C):** Kriterium zur Konkretisierung autonomer Cloud-Nutzung.
- **Additional Criterion (AC):** verschärft oder erweitert ein Kriterium; der Kunde entscheidet abhängig von seinem Souveränitätsbedarf, ob es gefordert wird.
- **Supplementary Information (SI):** Erläuterungen zu Scope, Ausnahmen oder externen Bezügen.

Für den Radar bedeutet das:

- `C` und `AC` sind **keine numerische Reifegradleiter**.
- Ein AC ist nicht automatisch für jeden Kunden „besser“ oder verpflichtend.
- EU- und Deutschland-Varianten (`C1`, `C2` usw.) sind **alternative Anforderungsprofile**, keine Scorestufen.
- Einschränkungen auf Deutschland müssen nach C3A in geeigneten Fällen begründet und insbesondere bei Beschaffung auf rechtliche Zulässigkeit geprüft werden.

Damit ist die heutige interne 0–4-Gate-Skala weiterhin möglich, darf aber nie als C3A-Level ausgegeben werden.

## 5. Konsequenz für Hard Gates: dynamische Kundenanforderungen vor festen Gate-Defaults

Die acht heutigen Hard Gates bleiben für den aktuellen MVP als interne Gruppierung und deterministische Operationalisierung bestehen. C3A zeigt aber, dass die zukünftige Decision-Support-Runtime stärker von einem **Requirement Profile** ausgehen sollte:

```text
Kundenanforderung / Use Case
        -> ausgewählte C3A-/andere Kriterien
        -> nicht kompensierbare Anforderungen markieren
        -> Evidence je ArchitectureOption
        -> Gate-/Requirement-Ergebnis
```

Beispiel: `SOV-1-01-C1` (EU-Jurisdiktion) und `SOV-1-01-C2` (deutsche Jurisdiktion) sind nicht Level 3 und 4 derselben Skala. Der Kunde legt fest, welches Anforderungsprofil einschlägig und zulässig ist. Erst daraus entsteht ggf. ein Hard Gate.

**Folge:** Langfristig sollen die acht Gate-Domänen als verständliche Gruppierung erhalten bleiben, konkrete K.O.-Kriterien aber aus kundenspezifischen Anforderungen/Profilen instanziiert werden. Keine sofortige Runtime-Migration vor NEXT-119.

## 6. Konsequenz für Provider Intelligence

C3A bestätigt die Provider-Intelligence-Idee besonders stark. Ein Provider-Claim benötigt künftig zusätzlich zu den bereits geplanten Scope-/Version-/Evidence-Feldern mindestens:

- `framework = C3A`
- `framework_version = 1.0`
- `criterion_id`
- `criterion_kind = criterion|additional_criterion`
- `service_set_scope`
- `offering_scope`
- `region_scope`
- `legal_entity_scope`
- `applicability_statement`
- `evidence_type`
- `audit_scope`
- `audit_period`
- `review_state`
- `last_checked_at`

Provider-Selbstaussage, Vertrag, technische Dokumentation und unabhängiges Audit bleiben getrennte Evidence-Arten.

## 7. Datenmodell: C3A-Datenklassen explizit abbilden

C3A unterscheidet vier Datenklassen, die im Radar nicht in einer einzigen generischen Kategorie verschwinden sollten:

1. **Account Data** – Verwaltungs-/Abrechnungs-/Kontaktdaten des Kundenkontos unter Providerkontrolle.
2. **Cloud Service Customer Data** – Kundendaten einschließlich Credentials und durch die veröffentlichte Schnittstelle erzeugter Ergebnisse.
3. **Cloud Service Derived Data** – durch Nutzung entstehende providerkontrollierte Daten, z. B. Nutzungs-/Log-/Konfigurationsinformationen.
4. **Cloud Service Provider Data** – providerinterne Betriebsdaten des Services.

Gerade `SOV-3-01` stellt für diese Klassen unterschiedliche Lokationsanforderungen. Provider Intelligence und Customer Intake brauchen deshalb künftig einen `data_class_type` statt nur „Daten liegen in Region X“.

## 8. Fachliche Prüfung nach C3A-Domänen

### SOV-1 Strategic Sovereignty

Bestätigt bestehende Radar-Themen:

- Jurisdiktion und Vertrags-/Streitbeilegungsrahmen
- eingetragener Sitz
- effektive Kontrolle durch Unternehmen
- Change of Control

Korrektur: EU/Deutschland sind kundenseitig zu wählende Anforderungsvarianten. `SOV-1-04` verlangt 90 Tage Vorabinformation bei relevanten Kontrolländerungen; diese Frist muss im C3A-Deep-Dive explizit geprüft werden.

### SOV-2 Legal & Jurisdictional Sovereignty

Bestätigt `G z.S1`, `G z.S2`, Audit-/Evidence- und geopolitische Szenariologik.

Zu präzisieren:

- Der Provider soll relevante nicht-EU-Rechtsnormen mindestens jährlich identifizieren und strukturiert hinsichtlich Verfügbarkeit sowie Vertraulichkeit/Integrität von Kundendaten bewerten.
- C3A Audit Rights beziehen sich spezifisch auf zuständige nationale/föderale Cybersecurity-Behörden bzw. die deutsche Bundesverwaltung; allgemeine Kundenauditrechte sind ein eigener Radar-Prüfgegenstand.
- State-of-Defense-Takeover ist ein spezielles öffentliches/verteidigungsrelevantes Kriterium und kein generelles Kunden-Hard-Gate.

### SOV-3 Data Sovereignty

Hier ist der größte Datenmodellbedarf:

- Residence muss nach C3A-Datenklassen getrennt geprüft werden.
- External Key Management verlangt für IaaS/PaaS Schlüsselgenerierung/-management/-speicherung außerhalb der Providerumgebung oder funktional gleichwertige Mechanismen; SaaS ist ein Additional Criterion.
- External IdP umfasst neben grundsätzlicher Föderation zusätzliche Anforderungen an offene Standards, stateless Authentication und dynamische Claims/Attribute.
- Logging/Monitoring umfasst Management- und Datenzugriffe, Zeit/Identität/operativen Kontext; Additional Criteria adressieren Echtzeitzugriff über standardisierte offene APIs und granulare Filterung.
- Client-Side Encryption ist stärker als „CMK vorhanden“: für den relevanten Scope bleibt der private Schlüssel ausschließlich beim Kunden außerhalb der Providerumgebung.

### SOV-4 Operational Sovereignty

C3A ist hier deutlich konkreter als die bisherige allgemeine Radar-Sprache. Zu prüfen bzw. zu korrigieren sind:

- Staatsangehörigkeit/Hauptwohnsitz sowie organisatorische Zugehörigkeit relevanten Betriebs-/Support-/Managementpersonals;
- **administrative access paths** und technische Sperren für Remote-Administration außerhalb EU/Deutschland, nicht nur der Arbeitsort des Personals;
- unabhängige redundante Connectivity inklusive EU-Bezug;
- SOC-Standort plus äquivalentes Stand-alone-SOC im Disconnect-Fall;
- Provider-seitige kontrollierte Ingress-Zone für Updates/Betriebsdaten, Vulnerability Checks und Change Management;
- risikobasierte Security-Analyse von Third-Party-Software vor Deployment;
- dokumentierte Überwachung aller Datenflüsse zu Dritten;
- Data Flow Diagrams und bekannte Gateways mit Ursprung/Ziel/Protokoll/Datentyp/Schutzmechanismen;
- vollständiger Disconnect aller nicht-EU-Verbindungen ohne Beeinträchtigung von Verfügbarkeit, Integrität, Authentizität und Vertraulichkeit, inklusive jährlich getesteter, von Nicht-EU-Einheiten unabhängiger Prozedur;
- getesteter Reconnect und Update-Nachholung nach bis zu 90 Tagen Disconnect.

Das ist **kein neuer Risikotyp**: diese Punkte operationalisieren vor allem `G z.S3`, `G z.S5`, `G z.S6`, `G z.S7`, `G z.S10`, `G z.S11`, `G z.S12` und `OperationalAutonomyCapability`.

### SOV-5 Supply Chain Sovereignty

Bestätigt den Dependency-/Common-Cause-/Substituierbarkeitsansatz. Provider Intelligence soll getrennt erfassen:

- Softwarekomponenten und relevante Lieferanten/Herkunftsländer, möglichst SBOM-basiert;
- Hardwarekomponenten, Lieferanten und Herkunftsländer;
- funktional erforderliche externe Cloud-Services und deren Provider-/Länderbezug;
- risikobasierte Mitigation und architektonische Substituierbarkeit für kritische Abhängigkeiten;
- Exportrestriktions-/Supply-Chain-Disruption-Prozess und Kundeninformation;
- Standort des Capacity Managements (EU oder Deutschland) gemäß C5-Bezug.

### SOV-6 Technology Sovereignty

C3A SOV-6 ist **nicht gleich Kundenausstieg/Portabilität**. Dieser Punkt korrigiert eine bisher zu breite Radar-Zuordnung.

C3A fokussiert Provider-Fortführungsfähigkeit:

- aktuelles Source-Code-Backup in der EU, max. 24 Stunden alt, mindestens fünf Versionen;
- Einschluss von IaC-, Build- und Deployment-Toolchains;
- Dokumentation zur unabhängigen Weiterentwicklung;
- sichere Servicefortführung bei Ausfall externer Dritter;
- bei Additional Criterion eigene Fähigkeit, Schwachstellen zu beheben, inklusive spezialisiertem Engineering-Talent und lokalen Build-Umgebungen;
- Zugriff auf Entwicklungswerkzeuge und dokumentierte Kontingenzverfahren bei Ausfall kritischer Entwicklungsabhängigkeiten.

**Kundenseitige Exit-/Switching-/Portabilitätsfragen bleiben deshalb primär bei Data Act, DORA, Bitkom und der internen Radar-Methodik.** C3A darf dafür nur verwendet werden, wenn ein konkreter C3A-Fortführungsaspekt tatsächlich passt.

## 9. Auswirkungen auf bestehende Question Library

Die vorhandene Question Library hat bereits viele C3A-Bezüge und bleibt wertvoll. Der Volltextreview zeigt aber mehrere **Provenienz-/Präzisionskorrekturen**:

- `OA-12` ist zu kundenorientiert formuliert; C3A SOV-4-05 beschreibt primär den Provider-Ingress-/Update-Kontrollprozess.
- `OA-13` muss Third-Party-Software-/Malware-Analyse vor Deployment statt nur „neue externe Abhängigkeiten“ erfassen.
- `OA-14` bündelt SOV-4-07/08 zu grob; Data-Exchange-Monitoring und Data-Flow-/Gateway-Dokumentation sollten im C3A-Deep-Dive getrennt sein.
- `OA-15` muss „alle nicht-EU-Verbindungen“, unabhängige Prozedur, CIA+A-Erhalt und jährlichen Test präziser abbilden.
- `OA-16` muss den C3A-Zeitraum von bis zu 90 Tagen und getestete Update-Nachholung berücksichtigen.
- `SP-12` fragt die Exposition, C3A SOV-5-04 zusätzlich nach Providerprozess zur Identifikation/Mitigation und Kundeninformation.
- `SP-13` bildet Capacity Management nicht präzise ab; C3A fragt nach Durchführung in EU bzw. Deutschland gemäß C5.
- `TE-01`, `TE-02`, `TE-07`, `TE-12` dürfen C3A SOV-6 nicht pauschal als Quelle für Kundenausstieg/Open-Standards-Portabilität verwenden.
- `TE-09`/`TE-10` müssen die konkreten Source-Code-/Toolchain-/Engineering-/Continuity-Anforderungen des C3A präzisieren.
- `LJ-12`/`SE-11` müssen zwischen Behörden-Auditrecht nach C3A und allgemeinem Kundenauditrecht unterscheiden.
- `GV-02` darf C3A nicht als allgemeines „SOV-1–8 + Schwellenwert“-Modell darstellen; C3A nutzt SOV-1–6 und auswählbare Kriterien.

Die kanonische Korrekturliste liegt in `data/method/c3a_v1_0_crosswalk.csv`. Vor der späteren Runtime-/Question-Migration hat diese Crosswalk-Datei Vorrang vor älteren pauschalen C3A-Zuordnungen.

## 10. Auswirkungen auf Risikotaxonomie

Der Volltextreview rechtfertigt derzeit **keine neuen `G z.S`-Risiko-IDs**. Die C3A-Kriterien konkretisieren bestehende Risiken und Capabilities ausreichend.

Mögliche spätere Unter-Szenarien, nicht neue Top-Level-Risiken:

- non-EU disconnect dependency
- external development dependency loss
- update supply-chain compromise
- inability to operate/develop service independently
- hidden third-party data exchange
- insufficient supplier substitution

Damit vermeiden wir Taxonomie-Inflation.

## 11. Was C3A nicht abdeckt und im Radar bleiben muss

C3A beantwortet nicht vollständig:

- welcher Workload für welche Option besser geeignet ist;
- Risiko des Status quo / Nichtstuns;
- Business Value, Time-to-Market und Innovation;
- kundenseitige Exit-Zeit/-Kosten und alternative Zielplattform;
- Portfoliokonzentration über mehrere Workloads;
- Organisationsskills des Kunden;
- kundenspezifische Security-/Business-Impact-Risiken;
- allgemeine regulatorische Pflichten außerhalb C3A;
- Umwelt-/Nachhaltigkeitsaspekte des EU-CSF SOV-8.

Der Decision-Support-Kern v0.4 bleibt daher notwendig.

## 12. Freigabeentscheidung nach Review

**Bestätigt:**

- DecisionCase / ArchitectureOptions
- Provider Intelligence
- Provider Capability ≠ Applied Capability
- Evidence Confidence separat
- adaptive Question Library
- Framework-Overlays statt Framework-Stapeln
- sieben verständliche Managementdimensionen als interne Präsentationsschicht
- Status-quo-/Business-Value-Betrachtung
- bestehende G-z.S-Risikotaxonomie

**Zu ändern/ergänzen:**

- C3A als eigener kriterienspezifischer Provider-/Service-Deep-Dive
- C5-Prerequisite bei C3A-Konformitätsaussage
- C3A-Datenklassen
- C/AC und EU/DE als Anforderungsvarianten, nicht Levels
- dynamisches Requirement Profile als Zielbild für spätere Hard-Gate-Runtime
- präzisere Operational-/Supply-Chain-/Technology-Capabilities
- korrigierte C3A-Provenienz in der Question Library

**Nicht erforderlich:**

- neuer kompletter Methodenneustart
- zusätzliche Top-Level-Souveränitätsrisiken
- Übernahme eines pauschalen C3A-Gesamtscores
- automatische Bevorzugung Deutschland > EU > Drittstaat

## 13. Reihenfolge nach diesem Review

1. Repository-Hygiene und Provenienz vollständig schließen.
2. NEXT-118 manuelle Consultant-Evaluation mit Hinweis auf aktuelle Runtime-vs.-v0.4-Grenze.
3. NEXT-119 Referenzfallvalidierung inkl. C3A Requirement Profile.
4. Erst danach Question-Library-/Schema-/Runtime-Migration.
5. Provider Intelligence anschließend C3A-kriterienscharf operationalisieren.
