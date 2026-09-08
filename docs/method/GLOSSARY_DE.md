# Glossar – Souveränitäts-Radar

Status: **Arbeitsglossar / verbindliche Begriffshilfe für Methode, Beratung und Software**  
Sprache: Deutsch mit englischen/code-nahen Aliasen  
Provenienz: gemischt – siehe Herkunftskennzeichnung je Begriff

## 1. Zweck

Dieses Glossar soll zwei Dinge gleichzeitig ermöglichen:

1. **deutschsprachige, verständliche Kommunikation** in Beratung, Workshops und Management-Unterlagen;
2. **stabile englische bzw. code-nahe Begriffe** für Datenmodell, Software, APIs und LLM-Verarbeitung.

Die englischen Begriffe sind deshalb **keine fachliche Aufwertung** und nicht automatisch Standardbegriffe. Wo ein Begriff aus der Methode des Souveränitäts-Radars stammt, wird das ausdrücklich gekennzeichnet.

### Sprachregel

- In Kundenterminen und Methodendokumenten zuerst den **deutschen Begriff** verwenden.
- Beim ersten Auftreten kann der englische/code-nahe Alias in Klammern ergänzt werden.
- In Code, Schema und API darf der englische Alias stabil bleiben.
- Begriffe aus BSI oder anderen externen Quellen werden nicht stillschweigend in eigene Begriffe umgedeutet.

## 2. Herkunftskennzeichnung

| Kennzeichen | Bedeutung |
|---|---|
| `[BSI]` | Begriff oder Grundlogik ist direkt an BSI-Standard 200-3 / IT-Grundschutz angelehnt. |
| `[EXT]` | Begriff oder Grundlogik stammt aus einem anderen externen Standard, Framework oder Regulierungsrahmen. |
| `[REPO]` | Begriff/Logik war bereits im bestehenden Souveränitäts-Radar modelliert. |
| `[METHOD]` | Eigene methodische Entwicklung des Souveränitäts-Radars. |
| `[SW]` | Primär Software-/Datenmodellierungsentscheidung, nicht normative Fachvorgabe. |
| `[CUSTOMER]` | Entsteht aus konkreten Vorgaben, Anforderungen oder Entscheidungen der Kundenorganisation. |

Ein Begriff kann mehrere Herkünfte haben.

---

# 3. Kernbegriffe

## Entscheidungsfall (`DecisionCase`)
**Herkunft:** `[METHOD] [SW]`

Der gesamte Beratungsfall, in dem für einen Workload oder eine eng abgegrenzte Gruppe mehrere Betriebs- oder Architekturvarianten miteinander verglichen werden.

**Beispiel:**  
„Soll Fachverfahren X weiterhin On-Prem betrieben, zu AWS Frankfurt, zu STACKIT oder in eine andere Zielarchitektur migriert werden?“

**Nicht verwechseln mit:** einem einzelnen Assessment. Ein Entscheidungsfall enthält typischerweise mehrere Variantenbewertungen.

---

## Betriebs-/Architekturvariante (`ArchitectureOption`)
**Herkunft:** `[METHOD] [SW]`

Eine konkrete Alternative innerhalb eines Entscheidungsfalls.

**Beispiele:**
- bestehendes On-Prem-Rechenzentrum
- modernisierte Private Cloud
- AWS in einer bestimmten EU-Region
- STACKIT
- chinesischer Hyperscaler
- Hybrid- oder Multi-Cloud
- hypothetische EU-Sovereign-Cloud

Der Variantentyp selbst erhält **keinen pauschalen Bonus oder Malus**.

---

## Bewertung / Assessment (`Assessment`)
**Herkunft:** `[REPO] [METHOD]`

Die strukturierte Untersuchung eines konkreten Workloads in einem bestimmten Provider-/Service-/Architektur-/Vertragskontext.

Im Variantenvergleich wird dieselbe Bewertungslogik je Betriebs-/Architekturvariante angewendet.

---

## Zielobjekt (`Target Object`)
**Herkunft:** `[BSI]`

Ein Gegenstand, auf den sich eine Risikoanalyse bezieht. Im IT-Grundschutz können dies z. B. Anwendungen, IT-Systeme, Räume, Netze oder auch Geschäftsprozesse sein.

Für den Souveränitäts-Radar ist der Begriff wichtig, weil eine Gefährdung immer **für ein konkretes Zielobjekt** auf Relevanz geprüft werden muss.

---

## Workload
**Herkunft:** `[REPO] [METHOD]`

Die konkrete fachlich-technische Arbeitslast, Anwendung oder Systemfunktion, deren Betriebsmodell bewertet wird.

Typische gemeinsame Eigenschaften:
- Zweck und fachlicher Scope
- Kritikalität
- Schutzbedarf
- Datenklassen
- RTO/RPO bzw. Ausfalltoleranz
- regulatorischer Kontext

**Beispiel:** „Wohngeld-Fachverfahren“ oder „KI-Agent zur Unterstützung der IT-Abteilung“.

---

## Geschäftsprozess / Business Function (`BusinessFunction`)
**Herkunft:** `[BSI] [REPO]`

Die fachliche Funktion, die durch einen oder mehrere Workloads unterstützt wird.

Die Geschäftsprozesssicht ist wichtig, weil sich Schadenshöhe und Kritikalität nicht allein aus Technik, sondern aus der Bedeutung für die Organisation ergeben.

---

## Gemeinsame Rahmenbedingungen (`Shared Facts`)
**Herkunft:** `[METHOD] [SW]`

Informationen, die für alle betrachteten Varianten gleich gelten und deshalb nur einmal erhoben werden.

**Beispiele:**
- Schutzbedarf des Workloads
- Kritikalität
- regulatorische Vorgaben
- Risikoappetit
- kundenspezifische Mindestkriterien
- vorhandene organisatorische Fähigkeiten

---

## Variantenspezifische Angaben (`Option-Specific Facts`)
**Herkunft:** `[METHOD] [SW]`

Informationen, die nur für eine bestimmte Betriebs-/Architekturvariante gelten.

**Beispiele:**
- konkrete Region
- verwendeter Managed Service
- Schlüsselmodell
- Redundanz
- Exit-Pfad
- Vertrag
- Support-/Admin-Zugriffe
- Subunternehmer

---

# 4. Provider- und Servicebegriffe

## Cloud-Anbieter / Provider (`Provider`)
**Herkunft:** `[REPO] [SW]`

Die Anbieter- oder Markenebene, z. B. AWS, Microsoft, Google, IONOS, STACKIT, Alibaba Cloud.

Die Marke allein ist **keine ausreichende Bewertungsgrundlage**.

---

## Juristische Einheit (`LegalEntity`)
**Herkunft:** `[REPO] [SW]`

Die konkrete Gesellschaft oder Organisation, die z. B. Vertragspartner, Betreiber, Supporteinheit oder Unterauftragnehmer ist.

Sie wird getrennt vom Provider modelliert, weil Rechtsraum, Vertragspartner und tatsächliche Betreiberrolle auseinanderfallen können.

---

## Cloud-Angebot / Betriebsangebot (`Offering`)
**Herkunft:** `[METHOD] [SW]`

Ein abgegrenztes Betriebs- oder Vertragsangebot eines Providers.

**Beispiele:**
- Commercial Public Cloud
- Sovereign Cloud
- Government Cloud
- Managed Private Cloud

Unterschiedliche Offerings desselben Providers dürfen nicht automatisch gleich bewertet werden.

---

## Service / Dienst (`Service`)
**Herkunft:** `[REPO] [SW]`

Ein konkreter technischer Cloud- oder IT-Dienst, z. B. Compute, Managed Kubernetes, Datenbank, Object Storage oder KI-Service.

Capabilities und Nachweise gelten nur im dokumentierten Scope des jeweiligen Dienstes.

---

## Region / Standort (`Region`, `Location`)
**Herkunft:** `[REPO] [SW]`

Geografischer oder organisatorischer Ort, an dem Daten, Systeme, Control Plane, Support- oder Administrationsfunktionen angesiedelt sein können.

„EU-Region“ allein beantwortet noch nicht alle Fragen zu Support, Metadaten, Control Plane oder Konzernkontrolle.

---

# 5. Fähigkeiten und tatsächliche Nutzung

## Anbieter-/Servicefähigkeit (`Provider/Service Capability`)
**Herkunft:** `[REPO] [METHOD]`

Eine Funktion oder Eigenschaft, die ein Provider bzw. Service grundsätzlich anbietet oder vertraglich zusichert.

**Beispiel:** „Customer-managed keys sind für Service X verfügbar.“

Eine verfügbare Fähigkeit ist noch kein Nachweis dafür, dass der Kunde sie tatsächlich nutzt.

---

## Tatsächlich genutzte/nachgewiesene Fähigkeit (`Applied Capability`)
**Herkunft:** `[REPO] [METHOD]`

Eine Fähigkeit, die im konkreten Workload bzw. in der konkreten Architektur tatsächlich konfiguriert, beobachtet, getestet oder anderweitig belastbar nachgewiesen ist.

**Beispiel:** Provider unterstützt Multi-AZ, der Workload nutzt Multi-AZ jedoch nicht. Dann ist die Providerfähigkeit vorhanden, die Applied Capability aber nicht erfüllt.

---

## Anbieteraussage zu einer Fähigkeit (`ProviderCapabilityClaim`)
**Herkunft:** `[METHOD] [SW]`

Eine normalisierte, prüfbare Aussage über eine konkrete Fähigkeit eines Providers, Offerings oder Services.

**Beispiel:** „Audit-Logs können für Service X in Region Y exportiert werden.“

Jede solche Aussage benötigt einen Scope und eine Quelle.

---

## Organisationsfähigkeit (`OrganizationCapability`)
**Herkunft:** `[METHOD]`

Die tatsächlich vorhandene Fähigkeit der Kundenorganisation, eine Technologie oder Betriebsaufgabe selbst zu verstehen, zu steuern und auszuüben.

**Beispiele:**
- Kubernetes-Kompetenz
- PostgreSQL-Kompetenz
- 24x7-Betrieb
- IAM-/PKI-Kompetenz
- Exit-/Migrationskompetenz

Formale Kontrolle ohne praktische Fähigkeit ist keine voll wirksame Souveränität.

---

## Fähigkeitsbedarf einer Variante (`ArchitectureSkillDemand`)
**Herkunft:** `[METHOD] [SW]`

Die Kompetenzen und Betriebsfähigkeiten, die eine konkrete Architekturvariante benötigt.

Der Vergleich zwischen Organisationsfähigkeit und Fähigkeitsbedarf macht sichtbar, ob eine technisch kontrollierbare Architektur organisatorisch überhaupt beherrscht werden kann.

---

# 6. Nachweise und Aussagen

## Nachweis / Evidenz (`Evidence`)
**Herkunft:** `[REPO] [METHOD]`

Ein Dokument, Test, Export, Beobachtung oder anderer Beleg, der eine Aussage unterstützt oder ihr widerspricht.

**Beispiele:**
- Vertrag
- Zertifikat oder Prüfbericht
- Architekturdiagramm
- IaC-/Konfigurationsexport
- Testprotokoll
- Provider-Dokumentation
- kundenseitiger Provider-Export
- Workshop-/Screenshare-Beobachtung

Ein Nachweis ist nicht automatisch eine bewertete Wahrheit; Scope, Aktualität und Vertrauenswürdigkeit müssen geprüft werden.

---

## Aussage / Claim (`Claim`)
**Herkunft:** `[REPO] [METHOD]`

Eine konkrete prüfbare Aussage, die durch Nachweise unterstützt oder widerlegt werden kann.

**Beispiel:** „Der Workload verwendet kundenseitig kontrollierte Schlüssel.“

Im bestehenden Radar wirken nur menschlich geprüfte Claims auf deterministische Hard-Gate-Bewertungen.

---

## Belastbarkeit der Nachweise (`Evidence Confidence`)
**Herkunft:** `[REPO] [METHOD]`

Grad der Sicherheit, mit der eine Aussage durch vorhandene Nachweise gestützt ist.

**Beispiel:**
- Interviewaussage „Backup funktioniert“ → geringe bis mittlere Belastbarkeit
- erfolgreicher Restore-Test vom letzten Monat → deutlich höhere Belastbarkeit

**Wichtig:** Evidence Confidence ist nicht dasselbe wie Risikohöhe.

---

## Anbieter-Nachweisdatenbank (`Provider Intelligence`)
**Herkunft:** `[CUSTOMER] [METHOD] [SW]`

Eine zentrale, wiederverwendbare und versionierte Wissensbasis über Provider, juristische Einheiten, Offerings, Regionen, Services, dokumentierte Fähigkeiten und zugehörige Nachweise.

Ziel ist, öffentlich verfügbare Providerinformationen nicht in jedem Kundenassessment erneut recherchieren zu müssen.

Provider Intelligence belegt primär **Provider-/Servicefähigkeit**, nicht automatisch die tatsächliche Kundenkonfiguration.

---

## Menschliche Prüfung (`Human Review`)
**Herkunft:** `[REPO] [METHOD]`

Bewusste fachliche Prüfung einer Aussage oder eines Nachweises durch einen verantwortlichen Menschen.

LLM-Extraktionen oder automatisch erkannte Aussagen dürfen nicht ohne Review in Risikoakzeptanz oder Hard-Gates einfließen.

---

## `UNVERIFIED` / ungeklärt
**Herkunft:** `[REPO] [METHOD]`

Zustand, wenn eine entscheidungsrelevante Aussage noch nicht ausreichend belegt ist.

`UNVERIFIED` bedeutet **nicht automatisch FAIL** und auch nicht PASS. Es macht eine Erkenntnislücke sichtbar.

---

# 7. Risiko- und Souveränitätsbegriffe

## Gefährdung (`Hazard` / `Threat` im weiten Sinn)
**Herkunft:** `[BSI]`

Ein Umstand oder Ereignis, das zu einem nennenswerten Schaden für ein Zielobjekt führen kann.

Der Souveränitäts-Radar übernimmt die elementaren Gefährdungen des BSI als Ausgangspunkt und ergänzt einsatzspezifische Souveränitätsgefährdungen.

---

## Zusätzliche Gefährdung (`Additional Hazard`)
**Herkunft:** `[BSI] [METHOD]`

Eine Gefährdung, die über die generischen elementaren Gefährdungen hinausgeht oder einen besonderen Aspekt des konkreten Einsatzszenarios präzisiert.

BSI 200-3 erlaubt ausdrücklich die Ermittlung zusätzlicher Gefährdungen bei besonderen Einsatzszenarien.

---

## Souveränitätsgefährdung (`Sovereignty-Specific Hazard`, intern `G z.S...`)
**Herkunft:** `[METHOD]`

Eine zusätzliche Gefährdung, die insbesondere strukturelle, rechtliche, organisatorische oder technische Abhängigkeiten digitaler Betriebsmodelle sichtbar macht.

**Beispiele:**
- Jurisdiktionsabhängigkeit
- Exit-/Portabilitätsdefizit
- Lock-in
- Konzentrationsrisiko
- Abhängigkeit von Identitäts-/Trust-Ankern
- Souveränitäts-Drift

Die konkrete Taxonomie ist eine interne Methodenentwicklung und keine offizielle BSI-Liste.

---

## Risikoszenario (`RiskScenario`)
**Herkunft:** `[REPO] [METHOD]`

Die konkrete Beschreibung, wie eine Gefährdung in einem bestimmten Kontext zu einer Konsequenz führen kann.

Für strukturelle Risiken nutzt der Radar bevorzugt die Kette:

`Bedingung/Exposition -> optionaler Trigger -> Konsequenz -> Kontrollen -> Auswirkung`

---

## Bedingung / Exposition (`Condition` / `Exposure`)
**Herkunft:** `[METHOD]`

Ein bereits bestehender Abhängigkeits- oder Risikozustand.

**Beispiel:** 70 % der Datenhaltung nutzt proprietäre APIs eines Providers.

Bei strukturellen Risiken ist dies oft sinnvoller als so zu tun, als müsse der Lock-in erst „eintreten“.

---

## Trigger / Auslöser (`Trigger`)
**Herkunft:** `[METHOD]`

Ein Ereignis, durch das eine bereits bestehende Exposition praktisch wirksam oder schadensrelevant wird.

**Beispiele:**
- Preiserhöhung
- Serviceabkündigung
- regulatorische Änderung
- Sanktion
- Change of Control

---

## Kontrolle / Maßnahme (`Control` / `Measure`)
**Herkunft:** `[BSI] [REPO]`

Technische, organisatorische, vertragliche oder andere Maßnahme, die ein Risiko vermeiden, reduzieren oder anderweitig behandeln soll.

---

## Restrisiko (`Residual Risk`)
**Herkunft:** `[BSI]`

Das nach Umsetzung der vorgesehenen Risikobehandlung verbleibende Risiko.

Die Akzeptanz des Restrisikos bleibt eine Managemententscheidung der Kundenorganisation.

---

## Risikoappetit / Risikobereitschaft (`Risk Appetite`)
**Herkunft:** `[BSI] [CUSTOMER]`

Die grundsätzliche Bereitschaft einer Organisation, bestimmte Risiken zu tragen. Sie beeinflusst insbesondere Risikoakzeptanzkriterien und Behandlungsentscheidungen.

Der Radar darf den Risikoappetit nicht selbst erfinden; er wird von der Kundenorganisation vorgegeben oder gemeinsam geklärt.

---

## Nicht kompensierbares Mindestkriterium (`Hard Gate`)
**Herkunft:** `[METHOD] [CUSTOMER]`

Eine zwingende Bedingung, deren Nichterfüllung nicht durch gute Werte in anderen Bereichen ausgeglichen werden darf.

**Beispiel:** „Personenbezogene Daten dürfen ausschließlich im EU/EWR-Raum verarbeitet werden.“

Die konkrete Gate-Struktur des Radars ist **keine BSI-Vorgabe**, sondern eine interne Operationalisierung von Mindestanforderungen und Risikoakzeptanzkriterien.

---

## Score / Bewertungskennzahl (`Score`)
**Herkunft:** `[METHOD]`

Eine zusammenfassende Kennzahl als sekundäre Managementhilfe.

Scores dürfen keine nicht kompensierbaren Mindestkriterien überstimmen und sollen getrennte Dimensionen nicht stillschweigend zu einer Scheingenauigkeit vermischen.

---

# 8. Ergebnisdimensionen

## Souveränitätsfähigkeit (`Sovereignty Capability`)
**Herkunft:** `[REPO] [METHOD]`

Grad bzw. Profil der verfügbaren Fähigkeiten eines Providers/Services oder einer Architektur, die digitale Selbstbestimmung, Kontrolle, Portabilität und Abhängigkeitsbeherrschung unterstützen.

Nicht identisch mit dem konkreten Workload-Risiko.

---

## Workload-Souveränitätsrisiko (`Workload Sovereignty Risk`)
**Herkunft:** `[REPO] [METHOD]`

Das konkrete Souveränitätsrisiko, das für einen bestimmten Workload aus der gewählten Provider-/Service-/Architektur-/Vertragskonstellation entsteht.

Ein Provider kann hohe Souveränitätsfähigkeiten besitzen und für einen bestimmten Workload dennoch ein relevantes Risiko erzeugen – und umgekehrt.

---

## Sicherheits-/Betriebsrisiko (`Security / Operational Risk`)
**Herkunft:** `[REPO] [BSI]`

Risiko für Informationssicherheit und Betrieb, z. B. durch Ausfall, Fehlkonfiguration, Schwachstellen, Personalausfall oder physische Schäden.

Diese Achse bleibt von Souveränitätsfähigkeit und Evidence Confidence getrennt.

---

## Verbesserungs-/Behandlungsvariante (`RemediationScenario`)
**Herkunft:** `[BSI] [METHOD] [SW]`

Eine konkrete Kombination zusätzlicher Maßnahmen, mit der eine Betriebs-/Architekturvariante verbessert und ihr Restrisiko neu bewertet werden kann.

Typische Zusatzfelder:
- Maßnahmen
- Aufwand/Kosten
- Umsetzungszeit
- Abhängigkeiten
- erwartetes Restrisiko

---

## Vergleichsergebnis (`ComparisonResult`)
**Herkunft:** `[METHOD] [SW]`

Strukturierter Vergleich der betrachteten Architekturvarianten.

Mindestens getrennt sichtbar:
- Hard-Gate-/Mindestkriteriumsstatus
- Souveränitätsfähigkeit
- Workload-Souveränitätsrisiko
- Sicherheits-/Betriebsrisiko
- Belastbarkeit der Nachweise
- wirtschaftliche Auswirkungen
- notwendige Maßnahmen
- Restrisiken

---

## Empfehlung (`Recommendation`)
**Herkunft:** `[METHOD]`

Begründete Empfehlung des Radars bzw. des Beratungsteams auf Basis der transparenten Vergleichsdaten.

Sie enthält nicht nur eine Rangfolge, sondern auch Trade-offs, Bedingungen, Evidence Gaps und Restrisiken.

---

## Kundenentscheidung (`CustomerDecision`)
**Herkunft:** `[METHOD] [CUSTOMER] [SW]`

Die tatsächliche Entscheidung der verantwortlichen Kundenorganisation einschließlich Begründung, akzeptierter Restrisiken und Verantwortlichkeit.

**Grundsatz:** Empfehlung ≠ Entscheidung.

---

# 9. Applied-State-Begriffe

Die bestehende Methode verwendet folgende Zustände als Beschreibung der Nachweis-/Anwendungsnähe einer Fähigkeit:

| Zustand | Deutsche Lesart | Bedeutung |
|---|---|---|
| `available` | verfügbar | Provider bietet die Fähigkeit grundsätzlich an. Provider-seitiger Zustand. |
| `asserted` | behauptet | Die Nutzung/Fähigkeit wurde angegeben, aber noch nicht belastbar dokumentiert. |
| `documented` | dokumentiert | Eine geeignete Dokumentation liegt vor. |
| `observed` | beobachtet | Die Eigenschaft wurde durch geeignete Beobachtung festgestellt. |
| `configured` | konfiguriert | Die konkrete Konfiguration belegt die Nutzung. |
| `tested` | getestet | Die Fähigkeit wurde praktisch getestet. |
| `attested` | attestiert | Geeigneter unabhängiger oder formaler Nachweis liegt vor. |

Diese Zustände sind eine **interne Operationalisierung des Radars**. Sie sind kein offizielles BSI- oder EU-Reifegradmodell und dürfen nicht automatisch als einfache numerische Rangfolge behandelt werden.

---

# 10. Begriffe, die bewusst nicht gleichgesetzt werden dürfen

| Nicht gleichsetzen | Warum |
|---|---|
| Provider = Legal Entity | Marke und konkrete juristische/vertragliche Einheit können auseinanderfallen. |
| Provider Capability = Applied Capability | „Kann angeboten werden“ ist nicht „wird im Workload genutzt“. |
| Evidence = Wahrheit | Ein Nachweis benötigt Scope-, Aktualitäts- und Vertrauensprüfung. |
| Evidence Confidence = Risikohöhe | Unsicherheit über einen Sachverhalt ist nicht dasselbe wie dessen Risiko. |
| Souveränitätsfähigkeit = Workload-Souveränitätsrisiko | Provider-/Architekturfähigkeit und konkretes Einsatzrisiko sind verschiedene Ebenen. |
| Hard Gate = Score | Ein zwingendes Mindestkriterium darf nicht weggemittelt werden. |
| Empfehlung = Kundenentscheidung | Risikoakzeptanz und Entscheidung bleiben beim Kunden. |
| On-Prem = automatisch souverän | Kontrolle kann formal hoch, praktisch aber wegen Skills, Resilienz oder Lieferketten schwach sein. |
| deutscher Provider = automatisch souverän | Herkunft ist ein Fakt, kein pauschaler Score. Jurisdiktion, Konzernkontrolle, Technik, Supply Chain und Betriebsfähigkeit sind getrennt zu prüfen. |

---

# 11. Referenzen im Repository

- `docs/method/METHOD_OVERVIEW.md` – bestehender Methodenkern
- `docs/architecture/DOMAIN_MODEL.md` – bestehendes Domänenmodell
- `docs/architecture/DECISION_CASE_AND_PROVIDER_INTELLIGENCE.md` – Erweiterung um Variantenvergleich und Anbieter-Nachweisdatenbank
- `docs/method/PROVENANCE_AND_EVIDENCE.md` – Nachweis- und Herkunftslogik
- `docs/method/RISK_TAXONOMY.md` – Risikotaxonomie
- `docs/method/SCORING_AND_GATES.md` – Gates und Scoring
- BSI-Standard 200-3 – Zielobjekte, elementare/zusätzliche Gefährdungen, Risikoeinschätzung, -bewertung, -behandlung und Risikoappetit

## Pflegehinweis

Dieses Glossar ist Teil der Methode und soll mitwachsen. Neue zentrale Begriffe sollen erst dann in Code, Schema oder Managementunterlagen eingeführt werden, wenn mindestens folgende Punkte geklärt sind:

1. deutscher Arbeitsbegriff;
2. englischer/code-naher Alias;
3. Herkunft;
4. eindeutige Definition;
5. Abgrenzung zu ähnlich klingenden Begriffen;
6. mindestens ein verständliches Beispiel, sofern der Begriff nicht selbsterklärend ist.
