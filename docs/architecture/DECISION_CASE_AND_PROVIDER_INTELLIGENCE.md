# Decision Case, Architecture Options und Provider Intelligence

Status: **Methoden-/Architekturentwurf**  
Issue: #65  
Provenienz: `internal-method`  
Reviewklasse: B – Methode/Architektur

## 1. Ziel

Der bestehende Radar bewertet einen Workload in einem konkreten Provider-/Service-/Architektur-/Vertragskontext. Für die Beratungsentscheidung wird eine Ebene darüber benötigt: Ein IT-Leiter oder eine andere verantwortliche Stelle soll mehrere realistische oder hypothetische Zielarchitekturen desselben Workloads nach derselben Methode vergleichen können.

Beispiele:

- bestehendes On-Prem-Rechenzentrum
- modernisiertes On-Prem / Private Cloud
- US-Hyperscaler in EU-Region
- deutsches oder anderes europäisches Cloud-Angebot
- chinesischer Hyperscaler
- Sovereign-Cloud-Angebot
- Hybrid-/Multi-Cloud-Variante
- hypothetische Zielarchitektur mit gewünschten Souveränitätseigenschaften

Die Methode soll eine **begründete Empfehlung** erzeugen dürfen. Die Entscheidung und Risikoakzeptanz bleiben beim Kunden.

## 2. Bestehende Prinzipien bleiben unverändert

Diese Erweiterung ersetzt den bestehenden Methodenkern nicht. Insbesondere gelten weiter:

- cloud-agnostischer Methodenkern
- Provider Adapter sind Übersetzer, keine Risk Engines
- Security Capability und Sovereignty Capability bleiben getrennt
- Provider/Service Capability ≠ Applied Capability
- Evidence Confidence ≠ Risikohöhe
- Gate first, score second
- fehlende Evidence = `UNVERIFIED`, nicht automatisch `FAIL`
- Human-reviewed Claims sind die Brücke von Evidence zu Hard Gates
- Legal-Schlussfolgerungen und Risikoakzeptanz bleiben menschliche Entscheidungen

## 3. Neue Aggregatebene: DecisionCase

Ein `DecisionCase` beschreibt die konkrete Managemententscheidung für einen Workload oder eine eng abgegrenzte Gruppe von Workloads.

```text
DecisionCase
├── Organization / Shared Organization Facts
├── BusinessFunction / Workload
├── Shared Workload Facts
├── Decision Requirements / Risk Appetite / K.O.-Kriterien
├── ArchitectureOption A
│   └── OptionAssessment A
├── ArchitectureOption B
│   └── OptionAssessment B
├── ArchitectureOption C
│   └── OptionAssessment C
└── ComparisonResult / Recommendation / CustomerDecision
```

Ein bestehendes einzelnes `Assessment` bleibt als Legacy-/Standalone-Fall zulässig. Im Variantenvergleich wird dieselbe Assessment-Semantik als `OptionAssessment` unter einer `ArchitectureOption` verwendet.

### 3.1 DecisionCase – Kernfelder

Konzeptionell mindestens:

- `decision_case_id`
- `name`
- `organization_id`
- `workload_id`
- `business_function_ids`
- `decision_context`
- `risk_appetite_ref`
- `mandatory_requirements`
- `architecture_option_ids`
- `comparison_status`
- `recommendation_state`
- `customer_decision_state`
- `method_version`
- `created_at` / `updated_at`

`mandatory_requirements` enthält nicht kompensierbare Mindestanforderungen und kundenspezifische K.O.-Kriterien. Sie dürfen nicht durch einen guten Gesamtscore ausgeglichen werden.

## 4. ArchitectureOption

Eine `ArchitectureOption` ist eine konkret zu bewertende Betriebs-/Zielarchitektur.

### 4.1 Option-Typen

Der Methodenkern soll mindestens folgende Typen repräsentieren können:

- `on_prem`
- `private_cloud`
- `colocation`
- `managed_private_cloud`
- `public_cloud`
- `sovereign_cloud`
- `saas`
- `hybrid`
- `multi_cloud`
- `hypothetical`

Die Typen dienen der Strukturierung, nicht der Risikobewertung. Ein Typ erhält keinen pauschalen Bonus/Malus.

### 4.2 ArchitectureOption – Kernfelder

Konzeptionell mindestens:

- `architecture_option_id`
- `decision_case_id`
- `name`
- `option_type`
- `description`
- `provider_refs`
- `legal_entity_refs`
- `offering_refs`
- `service_refs`
- `contract_refs`
- `location_refs`
- `dependency_refs`
- `architecture_fact_refs`
- `assumption_refs`
- `option_assessment_id`

Eine Option kann mehrere Provider und Services enthalten. Das ist für Hybrid-/Multi-Cloud- und Supply-Chain-/Common-Cause-Szenarien erforderlich.

## 5. Shared Facts vs. Option-specific Facts

Der Variantenvergleich darf gemeinsame Fakten nicht je Option erneut erheben.

### 5.1 Shared Organization / Workload Facts

Typische gemeinsame Fakten:

- Geschäftsprozess / Business Function
- Workload-Zweck und Scope
- Kritikalität
- Schutzbedarf Vertraulichkeit / Integrität / Verfügbarkeit
- Datenklassen
- RTO/RPO bzw. fachliche Ausfalltoleranz
- regulatorischer Kontext
- Risikoappetit und Risikoakzeptanzkriterien
- kundenspezifische K.O.-Kriterien
- organisatorische Rollen
- vorhandene Organisation-Capabilities / Skills

Diese Fakten werden einmal erhoben und von allen Optionen referenziert.

### 5.2 Option-specific Facts

Typische variantspezifische Fakten:

- konkrete Provider/Legal Entities/Services
- Regionen und Verarbeitungsorte
- Control-Plane-/Support-/Admin-Abhängigkeiten
- Schlüsselkontrolle
- IAM-/Trust-Anchor-Architektur
- tatsächliche Redundanz/Failover/Backup-Architektur
- proprietäre APIs/Formate/Managed Services
- Exit-/Migrationsweg
- Subunternehmer- und Supply-Chain-Abhängigkeiten
- tatsächlich benötigte Skills und Betriebsorganisation
- Verträge/SLA/Audit-/Exit-Klauseln
- Kosten für Betrieb, Migration, Exit und Risikobehandlung

Fragen werden entsprechend als `shared` oder `option_specific` klassifiziert. Das reduziert Wiederholungen und verbessert Vergleichbarkeit.

## 6. Organisation Capability vs. Architecture Skill Demand

Formale Kontrolle ist nicht automatisch praktisch ausübbare Souveränität. Deshalb sollen Organisationsfähigkeiten gegen den Bedarf jeder Option gestellt werden.

Beispiel:

```text
OrganizationCapability
  kubernetes = 3
  postgresql = 4
  aws = 1
  24x7_operations = 0

ArchitectureSkillDemand: Option B
  kubernetes = 4
  postgresql = 3
  aws = 4
  24x7_operations = 3
```

Der Gap ist kein pauschaler Provider-Malus, sondern ein workloadspezifischer Betriebs-/Souveränitätsfaktor.

## 7. Provider Intelligence Knowledge Base

Öffentliche Providerinformationen sollen nicht je Assessment neu recherchiert werden. Dafür wird zusätzlich zur assessmentgebundenen Customer Evidence eine wiederverwendbare, versionierte Provider-Intelligence-Schicht benötigt.

### 7.1 Zweck

Provider Intelligence beantwortet primär:

> Welche Fähigkeit bietet oder dokumentiert ein konkreter Provider/Service/Offering/Region-/Vertragskontext und wie belastbar ist dieser Nachweis?

Sie beantwortet **nicht automatisch**:

> Nutzt der Kunde diese Fähigkeit im konkreten Workload wirksam?

Der bestehende Grundsatz `Provider Capability ≠ Applied Capability` bleibt unverändert.

### 7.2 Zielmodell

```text
Provider
└── LegalEntity
    └── Offering
        └── Region / Location Scope
            └── Service
                └── ProviderCapabilityClaim
                    ├── ProviderEvidenceSource
                    ├── SourceLocator
                    ├── Scope
                    ├── Version / Period
                    ├── Freshness
                    └── Review State
```

### 7.3 Provider-Objekte

#### Provider

- Marken-/Anbieteridentität
- Ultimate Parent / Ownership-Bezug
- keine direkte Souveränitätswertung

#### LegalEntity

- konkrete juristische Einheit
- Sitz / relevante Jurisdiktion als Fakt
- Rolle: Vertragspartner, Betreiber, Support, Subprocessor o. Ä.

#### Offering

Beispiele: Commercial Cloud, Sovereign Cloud, Government Cloud, Managed Private Cloud. Unterschiedliche Offerings desselben Providers dürfen nicht zusammengefasst bewertet werden.

#### Service

Konkreter technischer Dienst. Capabilities gelten nur im dokumentierten Scope.

#### ProviderCapabilityClaim

Eine konkrete, normalisierte Aussage, z. B.:

- Datenlokationssteuerung verfügbar
- kundenseitig kontrollierte Schlüsseloption verfügbar
- Audit-Logs exportierbar
- standardisiertes Datenexportformat verfügbar
- definierte Subprocessor-Transparenz vorhanden

Claim-Metadaten mindestens:

- `claim_id`
- `provider_id`
- `legal_entity_id` optional
- `offering_id` optional
- `service_id` optional
- `region_scope`
- `capability_id`
- `statement`
- `applied_state = available|documented|attested`
- `source_id`
- `locator`
- `document_version`
- `publication_date` optional
- `valid_from` / `valid_to` optional
- `last_checked_at`
- `review_status`
- `scope_notes`

### 7.4 ProviderEvidenceSource

Provider Evidence soll mindestens Quelle, Produzent, Dokumenttyp, Scope, Version/Zeitraum, Fundstelle und Prüfdatum erhalten.

Typische Quellenklassen:

- offizielle Provider-Dokumentation
- Vertrags-/Policy-Muster
- Zertifikat / Prüfbericht / Assurance-Nachweis
- öffentliches Subprocessor-/Location-Dokument
- Produkt-/Service-Dokumentation
- regulatorische oder behördliche Primärquelle, soweit relevant

Provider-Selbstaussage und unabhängige Assurance bleiben als unterschiedliche Evidence-Arten erkennbar.

## 8. Nationale Herkunft ist kein Score

Die Herkunft eines Providers darf im Core keinen pauschalen Bonus oder Malus auslösen.

Nicht zulässig als Methodenregel:

```text
US Provider = -20
DE Provider = +20
CN Provider = -30
```

Stattdessen werden die relevanten Fakten explizit modelliert, z. B.:

- Ultimate-Parent-Jurisdiktion
- Vertragspartner-Jurisdiktion
- Betreiber-/Support-Einheiten
- Daten-/Metadaten-/Control-Plane-Standorte
- Admin-/Support-Zugriffspfade
- Unterauftragnehmer
- effektive Schlüsselkontrolle
- rechtlich/vertraglich relevante Kontroll- und Zugriffsexposition

Diese Fakten werden von den bestehenden Risiko-/Souveränitätsregeln verarbeitet. Rechtliche Schlussfolgerungen erfordern weiterhin angemessenes Human Review.

## 9. Hypothetische Architekturvarianten

Eine `ArchitectureOption` darf `hypothetical` sein. Sie dient als Soll-/Referenzarchitektur oder als Anforderungsprofil für eine Ausschreibung.

Hypothetische Fakten müssen explizit als `project-assumption` bzw. Annahme markiert werden und dürfen nicht als Providerfakten erscheinen.

Beispiel:

```text
Option: Hypothetische EU-Sovereign-Cloud
Assumptions:
- Datenverarbeitung ausschließlich EU/EWR
- Customer-held keys
- offene Exportformate
- Kubernetes + PostgreSQL
- keine proprietäre AI-Agent-Runtime
```

Die Option kann methodisch gut abschneiden, aber ihre `Evidence Confidence` bleibt niedrig, solange kein realer Anbieter/Service die Annahmen belegt.

## 10. Provider Intelligence -> Option -> Applied Capability

Die zentrale Beziehung lautet:

```text
Provider Intelligence
  -> belegt Provider/Service Capability
  -> wird auf ArchitectureOption gescoped
  -> erzeugt keine Applied Capability allein

Customer/Architecture Evidence
  -> belegt konkrete Auswahl/Konfiguration/Nutzung/Test
  -> Human-reviewed Claim
  -> Applied Capability
  -> Hard Gate / Risk Evaluation
```

Beispiel:

```text
Provider Capability: Multi-AZ verfügbar
Architecture Option: Service unterstützt Multi-AZ
Customer Evidence: Multi-AZ nicht konfiguriert
Applied Capability: nicht erfüllt
```

oder:

```text
Provider Capability: Customer-managed keys verfügbar
Customer Evidence: Konfiguration unbekannt
Applied Capability: UNVERIFIED
```

## 11. Vergleichsergebnis

`ComparisonResult` darf die Optionen nicht auf einen einzigen Wahrheitsscore reduzieren.

Mindestens getrennt ausweisen:

- Hard-Gate-/K.O.-Status
- Sovereignty Capability
- Workload Sovereignty Risk
- Security / Operational Risk
- Evidence Confidence
- wirtschaftliche Auswirkungen
- notwendige Risikobehandlung
- Restrisiko nach Behandlung

Optional können transparente, konfigurierbare Scores/Weights als sekundäre Managementhilfe verwendet werden. Ein Hard-Gate-Fail darf dadurch nicht kompensiert werden.

## 12. Remediation und Wirtschaftlichkeit

Jede Option soll sowohl `as_is` als auch ein mögliches `treated` Profil erhalten können.

```text
ArchitectureOption
├── As-Is Assessment
├── RemediationScenario
│   ├── Measures
│   ├── Cost / Effort
│   ├── Time to implement
│   └── dependencies
└── Treated Assessment / Residual Risk
```

Damit kann die Empfehlung z. B. lauten:

> Option B besitzt heute ein relevantes Exit-Risiko. Durch offene Datenformate, externes Backup und getesteten Exit sinkt das Restrisiko bei geringerem Aufwand als die für Option A erforderliche zweite RZ-Infrastruktur.

Kosten sind dabei Entscheidungsinput, keine automatische Risikoakzeptanz.

## 13. Recommendation und CustomerDecision

Der Radar darf eine Empfehlung erzeugen, wenn sie nachvollziehbar aus den Vergleichsdaten abgeleitet wird.

Eine Empfehlung enthält mindestens:

- bevorzugte Option oder Ranggruppe
- Begründung nach nicht kompensierbaren Gates und relevanten Risiko-/Souveränitätsdimensionen
- wesentliche Trade-offs
- notwendige Bedingungen/Maßnahmen
- Evidence Gaps
- verbleibende Restrisiken
- Sensitivität gegenüber kundenspezifischen Gewichtungen/Anforderungen

Die Empfehlung ist nicht die Entscheidung. `CustomerDecision` bleibt ein getrenntes Objekt bzw. ein getrennter Workflowzustand mit Entscheidung, Begründung, akzeptierten Restrisiken und Verantwortlichem.

## 14. Verhältnis zum bestehenden Runtime-Modell

Der aktuelle MVP kann weiterhin einzelne Assessments ausführen. Diese Architekturentscheidung verlangt noch keine sofortige Migration.

Vorgesehene schrittweise Umsetzung:

### Phase A – Methoden-/Architekturmodell

- dieser Architekturentwurf
- Projektentscheidungen
- Referenzfälle für On-Prem, US-Hyperscaler, deutscher/europäischer Provider, chinesischer Hyperscaler und hypothetische Option

### Phase B – Schemas

- `decision-case.schema.json`
- `architecture-option.schema.json`
- `provider-intelligence.schema.json`
- Erweiterung des Assessment-Exports um optionale DecisionCase-Referenzen
- Backward-Compatibility-Plan für bestehende Standalone-Assessments

### Phase C – Runtime

- additive DB-Modelle
- Shared Facts / Option Facts
- OptionAssessment-Orchestrierung
- Vergleichs-API
- Provider-Intelligence-Import/Lookup

### Phase D – Consultant UI

- Decision Case anlegen
- Optionen hinzufügen/klonen
- Shared Facts einmal erfassen
- option-spezifische Guided Questions
- Side-by-Side-Vergleich
- Maßnahmen-/Kostenvergleich
- Empfehlung und dokumentierte Kundenentscheidung

## 15. Nicht-Ziele

Diese Architektur führt ausdrücklich **nicht** ein:

- statisches Provider-Ranking
- Nationalitäts-Score
- automatische Risikoakzeptanz
- automatische juristische Schlussfolgerung
- Credential-basierte Pflichtscanner
- provider-spezifische Gate-Regeln im Core
- automatisches Hochstufen öffentlicher Providerdokumentation zu Applied Capability

## 16. Reviewfragen vor Schema-Implementierung

1. Soll ein `DecisionCase` genau einen Workload oder optional eine eng definierte Workload-Gruppe enthalten?
2. Welche Shared Facts werden kanonisch im DecisionCase gespeichert und welche bleiben referenzierte Domain Entities?
3. Wird `OptionAssessment` als neuer Runtime-Typ implementiert oder bleibt es technisch ein bestehendes `Assessment` mit `architecture_option_id`?
4. Wie werden Provider-Intelligence-Claims versioniert, wenn Dokumente ersetzt oder Services geändert werden?
5. Welche Provider-Evidence darf zentral gespeichert werden (Metadaten/Exzerpte/Volltext) unter Lizenz- und Vertraulichkeitsgesichtspunkten?
6. Wie wird eine bestehende Bewertung markiert, wenn Provider Intelligence nachträglich geändert wird (`sovereignty drift` / reassessment required)?
7. Welche wirtschaftlichen Größen sind für einen fairen Optionsvergleich verpflichtend und welche optional?
