# Intake- und Kontextquellen für den Souveränitäts-Radar

Status: **Methoden-/Architekturentwurf**  
Issue: #67  
Provenienz: `internal-method` / `INT-05`  
Reviewklasse: B – Methode/Architektur

## 1. Ziel

Der Radar soll vorhandene Informationen der Kundenorganisation möglichst gut nutzen, ohne ein bestimmtes Enterprise-Architecture-, CMDB-, ISMS- oder Cloud-Tool vorauszusetzen.

Leitprinzip:

> Vorhandene Artefakte vorbefüllen lassen, dann kurze Interviews führen, danach nur noch entscheidungsrelevante Lücken gezielt mit Evidence schließen.

Kein Input-Kanal ist allein ausreichend oder verpflichtend.

---

## 2. Kanonischer Intake-Ablauf

```text
Customer artifacts / Provider Intelligence / Interview
        ↓
Parsing / Strukturierung / Human Review
        ↓
Context Facts
        ↓
DecisionCase + Shared Facts + ArchitectureOption Facts
        ↓
Relevance / Screening
        ↓
Targeted Evidence Requests
        ↓
Claims / Applied Capability / Risks / Gates
```

**Kontext-Fact ≠ Evidence** bleibt bestehen. Eine Information kann Scope und Folgefragen vorbefüllen, ohne bereits einen ausreichenden Nachweis für eine Gate- oder Risikoaussage darzustellen.

---

## 3. Unterstützte bzw. geplante Quelltypen

| Quelle | Typischer Nutzen | Typische Grenzen |
|---|---|---|
| **Interview / Workshop** | Ziele, Sorgen, organisatorische Realität, geplante Architektur, Risikoappetit | Aussagen können unvollständig oder subjektiv sein; Evidence ggf. nachfordern |
| **Servicekatalog / CMDB** | Services, Systeme, Owner, Lifecycle, Beziehungen, Standorte | Datenqualität/Abdeckungsgrad variiert |
| **ArchiMate / EA-Modell** | Business–Application–Technology-Beziehungen, Abhängigkeiten, Verantwortlichkeiten | Modell kann veraltet/unvollständig sein; semantische Profile toolabhängig |
| **Architekturdiagramm** | Komponenten, Datenflüsse, Netze, Regionen, Trust Boundaries | beschreibt häufig Sollbild; keine automatische Konfigurations-Evidence |
| **BIA / BCM** | Business-Kritikalität, MTPD, RTO/RPO, Wiederanlaufprioritäten | eventuell nur auf Prozess-, nicht Workload-Ebene vorhanden |
| **ISMS / Risikoregister** | Schutzbedarf, bestehende Risiken, Controls, Risk Owner, akzeptierte Risiken | Risikosicht kann andere Taxonomie/Scope besitzen |
| **Verträge / SLA / AVV / Policies** | Legal Entity, Recht, Datenorte, Audit, Exit, Haftung, Kündigung, Subprocessor | Vertragsauslegung kann Legal Review erfordern |
| **IaC** | tatsächliche oder beabsichtigte Cloud-/Infrastrukturkonfiguration, Regionen, Ressourcen, Netzbeziehungen | nicht jede manuelle Laufzeitänderung sichtbar; Secrets vermeiden |
| **Kubernetes / Helm / GitOps** | Workloads, Abhängigkeiten, Storage/Ingress, deklarative Plattformkonfiguration | externe Services/Verträge oft nicht sichtbar |
| **IAM / PKI / KMS** | Trust Anchors, Schlüsselkontrolle, Rollen-/Admin-Abhängigkeiten | hochsensitiv; Redaction und Processing Profile beachten |
| **FinOps / Kostenberichte** | Betriebskosten, Preis-/Nutzungsprofile, Commitments | zukünftige Exit-/Remediation-Kosten müssen oft geschätzt werden |
| **Backup-/Restore-/DR-/Exit-Test** | praktisch getestete Resilienz und Wechselfähigkeit | nur für getesteten Scope/Zeitraum belastbar |
| **Provider Intelligence** | wiederverwendbare Provider-/Service-Capabilities und Assurance | belegt nicht automatisch die konkrete Kundenkonfiguration |

---

## 4. ArchiMate

ArchiMate ist ein **optionaler, hochwertiger Kontextkanal**, wenn die Kundenorganisation bereits damit arbeitet.

### 4.1 Standardisierter Austausch

The Open Group veröffentlicht das ArchiMate Model Exchange File Format als Standard zum Austausch von ArchiMate-Modellen zwischen Tools (`SRC-56`). Das Format transportiert u. a. Modellelemente und Beziehungen; zusätzlich können View-/Diagramminformationen enthalten sein.

Der Radar soll bevorzugt ein standardisiertes Austauschformat nutzen, wenn es verfügbar ist.

### 4.2 YAML

Ein generisches, normatives „ArchiMate YAML“ wird im Radar **nicht vorausgesetzt**. Tool- oder kundenspezifische YAML-/JSON-Exporte können über Adapter unterstützt werden, sofern ihre Semantik dokumentiert und auf das generische Kontextmodell gemappt wird.

### 4.3 ADOIT und andere EA-Tools

ADOIT bleibt ein Referenz-/Showcase-Adapter, aber keine Produktvoraussetzung. Dasselbe gilt für andere EA-Werkzeuge. Adapter dürfen nur strukturieren/übersetzen und keine eigene Risk Engine enthalten.

---

## 5. Evidence-Stärke ist nicht identisch mit Maschinenlesbarkeit

Maschinenlesbare Daten sind oft effizient, aber nicht automatisch belastbarer.

Beispiele:

- aktuelles Terraform/Cloud-Export kann stärkere Evidence für eine konkrete Konfiguration liefern als ein veraltetes Diagramm;
- ein erfolgreicher Restore-Test ist stärkere Evidence für Wiederherstellbarkeit als ein Backup-Konzept;
- ein vertragliches Dokument kann für eine Legal-/Exit-Aussage stärker sein als ein technischer Export;
- Provider-Dokumentation kann eine Servicefähigkeit belegen, aber nicht die tatsächliche Nutzung durch den Kunden.

Trust, Scope, Aktualität, Applied State und Human Review bleiben deshalb für alle Quellen erhalten.

---

## 6. Minimaler Beratungsmodus

Der Radar muss auch ohne strukturierte Artefakte funktionieren.

Minimalmodus:

1. Entscheidungsfrage klären.
2. Workload und Varianten grob beschreiben.
3. 15–25 Screening-Fragen beantworten.
4. nur entscheidungsrelevante Dokumente/Nachweise nachfordern.
5. Empfehlung mit Evidence Gaps ausgeben.

Damit wird vermieden, dass eine Organisation erst CMDB, ArchiMate oder IT-Grundschutz „fertig machen“ muss, bevor eine Souveränitätsentscheidung möglich ist.

---

## 7. Deep-Dive-Modus

Bei hoher Kritikalität, regulatorischen Anforderungen oder knappen Vergleichsergebnissen kann die Tiefe steigen:

- vollständiger Dependency Graph
- detaillierte Datenflüsse
- Service-/Region-/Legal-Entity-Auflösung
- IaC-/Konfigurationsprüfung
- Vertrags-/Assurance-Review
- BSI-/C5-/C3A-/DORA-/NIS2-Overlay
- Exit-/Restore-/Failover-Test
- Portfolio-/Common-Cause-Betrachtung

Die Tiefe wird durch **Entscheidungsrelevanz**, nicht durch die maximale Menge verfügbarer Daten gesteuert.

---

## 8. LLM-/AI-Nutzung

LLMs dürfen Intake unterstützen, z. B.:

- Dokumente strukturieren
- Architekturelemente/Beziehungen vorschlagen
- Claims/Evidence-Kandidaten extrahieren
- Widersprüche und Lücken markieren
- Folgefragen vorschlagen

Sie dürfen ohne Human Review weder:

- kundenspezifische Facts als bestätigt markieren
- Legal Conclusions erzeugen
- Risk Acceptance durchführen
- Hard Gates verändern

Das bestehende Processing-Profile- und Datenschutzprinzip bleibt erhalten.
