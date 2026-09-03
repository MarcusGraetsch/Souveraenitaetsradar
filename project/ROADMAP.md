# Roadmap

## R1 – BSI-200-3-Abgleich – abgeschlossen

- vorhandene Kategorien gegen BSI 200-3 gemappt
- fehlende elementare Gefährdungen ergänzt
- Cloud-/KI-spezifische Risiken als eigene Radar-Risikotypen getrennt

## R2 – Souveränitätsmethodik / Fragen – abgeschlossen

- G z.S1–G z.S12
- 128 atomare Fragen / acht Domänen
- Provenienz- und Evidence-Modell
- Objektmodell

## R3 – Szenariokalibrierung – abgeschlossen

Sechs Szenarien. Kernergebnis: Security, Souveränität und Evidence müssen getrennt bleiben.

## R4 – Bewertungslogik – abgeschlossen / weiter zu kalibrieren

- Hard Gates
- Requirement-/Capability-Level
- Evidence Gate
- Exit-/Autonomie-/Konzentrations-/KI-Portabilitätsfaktoren
- deterministische Decision States

## R5 – Public Evidence Pilot – abgeschlossen

Amazon Bedrock wurde als realer Provider-Evidence-Fall verwendet. Wichtigste Erkenntnisse:

- Provider Capability ≠ Applied Capability
- Claims können modell-/region-/vertragsabhängig sein
- Featureanzahl ist keine Security-Metrik
- Assurance braucht Scope/Version/Periode

R5 bleibt **Beispiel**, nicht Providerfokus.

## R6 – Customer-mediated, cloud-agnostic Evidence – aktuell

### R6A

- Evidence Pack Schema
- Evidence Request Catalog
- lokaler Validator/Normalizer
- generische Domain-Modelle
- Gate -> Claim -> Evidence Mapping
- synthetischer providerneutraler Pilot

### R6B

- erster Provider Adapter als reine Übersetzungsschicht
- zweiter Adapter eines anderen Provider-Typs zur Agnostik-Prüfung
- Dokument-/Vertrags-/Assurance-Pipeline

## R7 – Validierung und Compliance-Vertiefung

- C5:2026 Detailmapping
- Framework-Versionierung
- Portfolio-/Dependency-Graph
- Inter-Rater-Tests
- Kundenpilot mit redigiertem Evidence Pack

## MVP

- Assessment CLI/API
- Evidence Pack Intake
- Rule Engine
- Question-/Follow-up Engine
- AI-assisted Extraction/Conflict Detection/Explanation
- Human Review Workflow
- Radar-/Management Report

## Später

- Web UI
- DataGerry/CMDB-Import
- DORA-RoI-artige Imports
- Provider Adapter Library
- Continuous Reassessment aus wiederholten kundenbereitgestellten Snapshots
