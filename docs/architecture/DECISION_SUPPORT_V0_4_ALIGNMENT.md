# Architektur-Alignment – Methodenkern v0.4

Status: **Architektur-Delta / noch keine Runtime-Migration**  
Issue: #67  
Provenienz: `internal-method` / `INT-05`

## 1. Zweck

Dieses Dokument übersetzt den fachlichen Methodenkern `METHOD_CORE_V0_4_DE.md` in Konsequenzen für das bestehende Domain-/DecisionCase-Modell, ohne bereits DB, API, Schema oder UI zu ändern.

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

Der v0.4-Kern ist deshalb kein Architektur-Neustart.

## 3. Fachliche Erweiterungen für spätere Schemas

### 3.1 Status-quo-Markierung

`ArchitectureOption` benötigt später eine explizite Kennzeichnung, ob sie den heutigen Zustand repräsentiert, z. B.:

```text
is_status_quo: true|false
```

Dies ist semantisch besser als ein pauschaler `option_type`, weil auch ein heutiges Public-Cloud- oder Hybridmodell Status quo sein kann.

### 3.2 Business-/Strategic-Value-Profil

Je Option soll ein sichtbares Nutzenprofil abbildbar werden, mindestens qualitativ:

- fachlicher Nutzen
- Time-to-Market
- Modernisierungs-/Innovationsnutzen
- Skalierbarkeit/Flexibilität
- Betriebsentlastung
- Opportunity Cost / Risiko des Nichtstuns

Diese Werte dürfen Hard Gates nicht kompensieren.

### 3.3 Sichtbare Decision Dimensions

`ComparisonResult` benötigt eine Präsentationsschicht für die sieben Managementdimensionen:

1. business_innovation
2. security_resilience
3. legal_data_control
4. technology_exit
5. organization_skills
6. supply_chain_geopolitics
7. economics_contract

`evidence_confidence` bleibt separat.

Die bestehenden internen Risiko-/Capability-Achsen werden **nicht ersetzt**, sondern auf diese verständlichere Managementsicht projiziert.

### 3.4 Compliance-/Deep-Dive-Profile

Später soll ein Entscheidungsfall oder eine Option aktivierte Profile referenzieren können, z. B.:

```text
assessment_profiles:
  - core_sovereignty
  - bsi_security_deep_dive
  - c3a_provider_deep_dive
  - data_act_switching
  - dora_overlay
```

Ein Profil braucht mindestens:

- ID / Version
- Aktivierungsgrund
- Scope
- Provenienz
- `method_source` vs. `compliance_applicable`

Damit kann DORA als Methodenquelle dienen, ohne fälschlich DORA-Anwendbarkeit zu behaupten.

### 3.5 Context Sources

Vorhandene Artefakte sollen als Kontextquellen modellierbar sein, ohne sie automatisch zu Evidence aufzuwerten.

Spätere abstrakte Entität:

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

### 3.6 Geopolitical Scenario

Kein eigenes Länder-Ranking. Stattdessen wird `RiskScenario` um ein klar erkennbares geopolitisches/externes Szenarioprofil erweitert bzw. damit klassifiziert.

Beispiele:

- compelled_access
- sanctions_export_control
- service_withdrawal
- support_update_loss
- change_of_control
- contract_price_shock

Die betroffenen Dependencies, Legal Entities, Services und Controls werden wie bei anderen Risikoszenarien referenziert.

### 3.7 Decision Relevance

Fragen und Evidence Requests benötigen perspektivisch eine Priorisierungsmetadatenebene, die nicht mit Applicability gleichgesetzt wird.

Mögliche Faktoren:

- affects_hard_gate
- differentiates_options
- material_risk_or_benefit
- closes_material_evidence_gap
- recommendation_sensitivity

Diese Metadaten steuern die Arbeitsreihenfolge, nicht die fachliche Wahrheit.

## 4. Adaptive Question Library

Die bestehende Question Bank bleibt vollständig erhalten. Für spätere Runtime-/UI-Änderungen braucht sie zusätzliche Metadaten für:

- `core_screening_candidate`
- relevante Decision Dimension
- shared vs. option-specific
- Deep-Dive-/Overlay-Zugehörigkeit
- Decision-Relevance-Trigger
- erwartete Evidence-Klasse

Ziel ist nicht, Fragen endgültig zu löschen, sondern den sichtbaren Einstieg auf etwa 15–25 Kernfragen zu reduzieren und danach gezielt zu verzweigen.

## 5. Provider Intelligence bleibt unverändert wichtig

Provider Intelligence versorgt ArchitectureOptions mit wiederverwendbaren Provider-/Service-Capability-Claims und Evidence. Neu ist vor allem die Priorisierung:

- EU-CSF/C3A/C5/Provider-Primärdokumentation werden stärker als Provider-/Service-Layer genutzt;
- kunden- bzw. workload-spezifische Anwendung bleibt separate Applied Capability;
- Providerherkunft/Jurisdiktion wird als Fact/Dependency modelliert, nicht als Score.

## 6. Output-Artefakt

Die Runtime soll später nicht nur einen Assessment-Report, sondern eine **Decision Template / Entscheidungsvorlage** erzeugen können. Struktur: `docs/product/DECISION_TEMPLATE_V0_4_DE.md`.

## 7. Migrationsreihenfolge

Noch **nicht implementieren**, bevor NEXT-119 die Methode validiert hat.

Danach bevorzugt:

1. Question-Library-Metadaten und Screeningkern
2. DecisionCase/ArchitectureOption Schema inkl. Status quo
3. Business-/Opportunity-Profil und sieben Decision Dimensions
4. Profile/Overlay-Aktivierung
5. ContextSource-/Adaptermodell
6. Geopolitical Scenario Classification
7. Decision Template / Recommendation UI
8. Provider Intelligence Runtime

Jeder Schritt benötigt Backward-Compatibility- und Boundary-Tests.
