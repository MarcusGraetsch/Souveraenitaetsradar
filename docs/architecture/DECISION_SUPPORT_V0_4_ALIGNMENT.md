# Architektur-Alignment – Methodenkern v0.4 nach C3A-Volltextreview

Status: **Architektur-Delta / noch keine Runtime-Migration**  
Issue: #67  
C3A-Review: #68 / NEXT-120 abgeschlossen  
Provenienz: `internal-method` / `INT-05`, externe Präzisierungen aus `SRC-04`

## 1. Zweck

Dieses Dokument übersetzt den fachlichen Methodenkern `METHOD_CORE_V0_4_DE.md` und den abgeschlossenen C3A-Volltextreview `C3A_V1_0_REVIEW.md` in Konsequenzen für das bestehende Domain-/DecisionCase-Modell, ohne bereits DB, API, Schema oder UI zu migrieren.

Der C3A-Review bestätigt die Grundarchitektur. Es ist **kein Architektur-Neustart** erforderlich. Die wichtigste Ergänzung ist ein kriterienspezifisches Anforderungs-/Evidence-Profil für Provider-/Service-Autonomie.

## 2. Bestehende Objekte bleiben tragfähig

Weiterverwenden:

- `DecisionCase`
- `ArchitectureOption`
- `Assessment` / später `OptionAssessment`
- `Organization`
- `BusinessFunction`
- `Workload`
- `Provider`, `LegalEntity`, `Offering`, `Service`, `Location`, `Contract`
- `Dependency`
- `Evidence`, `Claim`
- `RiskScenario`
- `GateRequirement`, `GateResult`
- Provider Intelligence / Provider Capability

C3A erfordert keine neuen Top-Level-Risikoobjekte. Es präzisiert vor allem Provider-/Service-Capabilities, Requirement-Auswahl, Datenklassen, Evidence-Scope und operative/Supply-Chain-Abhängigkeiten.

## 3. Fachliche Erweiterungen für spätere Schemas

### 3.1 Status-quo-Markierung

`ArchitectureOption` benötigt später eine explizite Kennzeichnung, ob sie den heutigen Zustand repräsentiert:

```text
is_status_quo: true|false
```

Auch ein heutiges Public-Cloud- oder Hybridmodell kann Status quo sein.

### 3.2 Business-/Strategic-Value-Profil

Je Option soll ein sichtbares Nutzenprofil abbildbar werden, mindestens qualitativ:

- fachlicher Nutzen
- Time-to-Market
- Modernisierungs-/Innovationsnutzen
- Skalierbarkeit/Flexibilität
- Betriebsentlastung
- Opportunity Cost / Risiko des Nichtstuns

Diese Werte dürfen nicht kompensierbare Anforderungen nicht überstimmen.

### 3.3 Sichtbare Decision Dimensions

`ComparisonResult` benötigt eine Präsentationsschicht für die sieben Managementdimensionen:

1. `business_innovation`
2. `security_resilience`
3. `legal_data_control`
4. `technology_exit`
5. `organization_skills`
6. `supply_chain_geopolitics`
7. `economics_contract`

`evidence_confidence` bleibt separat.

Die bestehenden internen Risiko-/Capability-Achsen werden nicht ersetzt, sondern auf diese verständlichere Managementsicht projiziert. Die sieben Dimensionen sind interne Methodik und keine unveränderte C3A-/EU-CSF-Taxonomie.

### 3.4 C3A Requirement Profile

C3A zeigt, dass konkrete Autonomieanforderungen nicht als fixe Reifegradleiter modelliert werden sollten. Spätere abstrakte Entität:

```text
C3ARequirementProfile
- framework_version
- selected_criteria[]
- selected_additional_criteria[]
- jurisdiction_profile: eu|de|mixed|not_applicable
- selection_reason
- legal_procurement_note
- service_set_scope
- owner
- approved_at
```

Jeder Eintrag in `selected_criteria` referenziert die originale C3A Criterion-ID. `Additional Criterion` ist nur aktiv, wenn der Kunde dies verlangt.

EU- und Deutschlandvarianten sind alternative Anforderungen; Deutschland ist kein automatisch höheres Level. Dort, wo C3A eine Begründung/rechtliche Zulässigkeit von Deutschlandrestriktionen anspricht, muss diese Information erhalten bleiben.

### 3.5 Dynamische Requirement Gates als Zielbild

Die acht heutigen Hard Gates bleiben für die bestehende Runtime unverändert und dienen weiter als verständliche Gruppierung. Langfristig soll jedoch ein `GateRequirement` aus expliziten Kundenanforderungen/Profilen instanziiert werden können.

Beispiel:

```text
Customer Requirement
  -> C3A SOV-1-01-C1 (EU jurisdiction)
  -> non_compensable = true
  -> applies_to ArchitectureOption B/C
  -> required evidence
  -> PASS / FAIL / UNVERIFIED
```

Ein C3A-C1/C2-Unterschied darf nicht in die interne 0–4-Levelskala als vermeintlicher Reifegrad übersetzt werden.

### 3.6 C3A-Datenklassen

Für Provider Intelligence und Option Facts wird ein expliziter Typ benötigt:

```text
C3ADataClass
- account_data
- cloud_service_customer_data
- cloud_service_derived_data
- cloud_service_provider_data
```

Residence-/Processing-Claims müssen Datenklasse und Service-Scope referenzieren. Eine generische Aussage „Daten liegen in EU“ ist für C3A zu unpräzise.

### 3.7 Compliance-/Deep-Dive-Profile

Ein Entscheidungsfall oder eine Option soll aktivierte Profile referenzieren können:

```text
assessment_profiles:
  - core_sovereignty
  - bsi_security_deep_dive
  - c3a_provider_deep_dive
  - c5_assurance
  - data_act_switching
  - dora_overlay
```

Ein Profil braucht mindestens:

- ID / Version
- Aktivierungsgrund
- Scope
- Provenienz
- `method_source` vs. `compliance_or_conformity_applicable`

Für `c3a_provider_deep_dive` zusätzlich:

- ausgewählte Criterion-/AC-IDs
- C5-Prerequisite-Status
- Service Set Scope
- Audit/Evidence Scope

Damit kann ein C3A-Kriterium als Methodenquelle dienen, ohne C3A-Gesamtkonformität zu behaupten.

### 3.8 C5-Prerequisite-Status

C3A setzt C5-Erfüllung voraus. Provider Intelligence braucht deshalb für C3A-Auswertungen einen expliziten Zustand:

```text
c5_prerequisite_status:
  verified | unverified | not_assessed | scope_mismatch
```

Nur `verified` im passenden Service-/Audit-Scope erlaubt später eine formale C3A-Erfüllungsbehauptung. Die Nutzung einzelner C3A-Kriterien als Requirement-/Methodenquelle bleibt auch ohne formale C3A-Konformitätsaussage möglich.

### 3.9 Context Sources

Vorhandene Artefakte sollen als Kontextquellen modellierbar sein, ohne sie automatisch zu Evidence aufzuwerten:

```text
ContextSource
- type
- origin
- version/time
- scope
- parser/adapter
- review_state
```

Mögliche Typen: interview, cmdb, archimate, diagram, bia_bcm, isms, contract, iac, kubernetes_gitops, iam_pki_kms, finops, test_report.

`ContextFact` referenziert die Quelle. Ein `Claim` braucht weiterhin ausreichende Evidence nach der bestehenden Trust-/Review-Logik.

### 3.10 Geopolitical Scenario

Kein eigenes Länder-Ranking. Stattdessen wird `RiskScenario` um ein externes/geopolitisches Szenarioprofil erweitert:

- `compelled_access`
- `sanctions_export_control`
- `service_withdrawal`
- `support_update_loss`
- `change_of_control`
- `contract_price_shock`
- `non_eu_disconnect_dependency`
- `external_development_dependency_loss`

C3A SOV-4/5/6 liefert für einige dieser Szenarien konkrete Provider-Capability-/Evidence-Prüfgegenstände.

### 3.11 Decision Relevance

Fragen und Evidence Requests benötigen perspektivisch eine Priorisierungsmetadatenebene, die nicht mit Applicability gleichgesetzt wird:

- `affects_hard_gate`
- `differentiates_options`
- `material_risk_or_benefit`
- `closes_material_evidence_gap`
- `recommendation_sensitivity`

Diese Metadaten steuern die Arbeitsreihenfolge, nicht die fachliche Wahrheit.

## 4. Provider Intelligence nach C3A

C3A bestätigt den geplanten Aufbau und ergänzt notwendige Claim-Metadaten.

Ein kriterienspezifischer Provider Claim benötigt perspektivisch mindestens:

```text
ProviderCapabilityClaim
- provider_id
- legal_entity_id
- offering_id
- service_id / service_set_scope
- region_scope
- framework = C3A
- framework_version = 1.0
- criterion_id
- criterion_kind = criterion|additional_criterion
- statement
- applicability_statement
- evidence_refs[]
- audit_scope
- audit_period
- review_state
- last_checked_at
```

Provider-Selbstaussage, Vertrag, technische Dokumentation und unabhängiges Audit bleiben unterscheidbar.

### 4.1 Provider Capability bleibt getrennt von Applied Capability

C3A kann z. B. belegen, dass ein Service eine externe Key-Management-Integration anbietet. Ob der konkrete Workload sie tatsächlich nutzt, bleibt eine separate Applied-Capability-Frage.

### 4.2 Provider-/Service-Scope statt Markenrating

C3A bewertet einen konkreten Satz von Cloud-Services. Deshalb darf eine C3A-Evidence nicht automatisch auf den gesamten Provider, alle Regionen oder alle Offerings hochgezogen werden.

## 5. Adaptive Question Library nach C3A

Die bestehende Question Library bleibt vollständig erhalten. Der Volltextreview hat jedoch mehrere bestehende C3A-Zuordnungen als `partial`, `misaligned` oder `gap` markiert.

Maßgeblich bis zur Migration:

- `data/method/c3a_v1_0_crosswalk.csv`
- `docs/method/C3A_V1_0_REVIEW.md`

Spätere Runtime-/UI-Metadaten:

- `core_screening_candidate`
- relevante Decision Dimension
- shared vs. option-specific
- Deep-Dive-/Overlay-Zugehörigkeit
- Decision-Relevance-Trigger
- erwartete Evidence-Klasse
- `c3a_criterion_ids`
- `c3a_mapping_status`

Die vollständige kriterienscharfe Question-Library-Korrektur erfolgt im Zuge von NEXT-119 und wird nicht vor der Referenzfallkalibrierung blind in die Runtime übernommen.

## 6. C3A beeinflusst die Risikotaxonomie nicht auf Top-Level

Der Review rechtfertigt derzeit keine neuen `G z.S`-IDs. Bestehende Risiken decken die C3A-Szenarien ausreichend ab:

- Jurisdiktion / Extraterritorial Exposure
- Change of Control
- Fortführungs-/Exit-Fähigkeit
- Lock-in
- Operating Autonomy / Skills
- Supply Chain
- Konzentration / Common Cause
- Key Control
- Trust Anchors
- Evidence / Observability
- Sovereignty Drift

C3A liefert konkretere Controls/Capabilities/Evidence, nicht zwingend neue Risikooberkategorien.

## 7. Output-Artefakt

Die Runtime soll später nicht nur einen Assessment-Report, sondern eine **Decision Template / Entscheidungsvorlage** erzeugen können. Struktur: `docs/product/DECISION_TEMPLATE_V0_4_DE.md`.

C3A-Ergebnisse werden dort nicht als pauschaler Provider-Score, sondern als ausgewählte Kriterien mit `PASS/FAIL/UNVERIFIED`, Scope und Evidence dargestellt.

## 8. Migrationsreihenfolge nach abgeschlossenem C3A-Gate

### Gate 1 – NEXT-120

**Abgeschlossen.** C3A-Volltextreview und Crosswalk liegen vor.

### Gate 2 – NEXT-118 / NEXT-119

1. aktuelle Webapp manuell aus Consultant-Sicht evaluieren;
2. Methodenkern v0.4 an Referenzvarianten validieren;
3. C3A Requirement Profile in mindestens einem Cloud-Szenario praktisch testen;
4. Screening-/Deep-Dive-Logik kalibrieren.

### Erst danach implementieren

Bevorzugte Reihenfolge:

1. Question-Library-Metadaten und C3A-kriterienscharfe Korrekturen
2. `DecisionCase`/`ArchitectureOption` Schema inkl. Status quo
3. Requirement Profile / dynamische Requirement Gates
4. C3A-Datenklassen und C5-Prerequisite-Status
5. Business-/Opportunity-Profil und sieben Decision Dimensions
6. Profile/Overlay-Aktivierung
7. `ContextSource`-/Adaptermodell
8. Geopolitical Scenario Classification
9. Decision Template / Recommendation UI
10. Provider Intelligence Runtime

Jeder Schritt benötigt Backward-Compatibility-, Boundary-, Provenienz- und Regressionstests.

## 9. Weiterhin zulässige Arbeiten vor Runtime-Migration

- Security-Hardening ohne Methodenänderung
- Bugfixes
- Repository-/CI-Hygiene
- Dokumentations-/Provenienzkorrekturen
- Provider-/Framework-Research ohne automatische Runtime-Wirkung
- Vorbereitung von Testdaten für NEXT-118/NEXT-119
