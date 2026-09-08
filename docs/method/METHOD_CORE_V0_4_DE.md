# Methodenkern v0.4 – Entscheidungsunterstützung für digitale Souveränität

Status: **Methodenentwurf / interne Arbeitsgrundlage**  
Sprache: Deutsch  
Provenienz: `internal-method` mit externen Referenzquellen  
Reviewklasse: B – Methode/Architektur

## 1. Ziel der Methode

Der Souveränitäts-Radar soll keine abstrakte Aussage wie „Cloud ist souverän“ oder „On-Prem ist souveräner“ erzeugen. Er soll eine **nachvollziehbare Entscheidungsvorlage** für einen konkreten Workload oder IT-Service liefern.

Die Leitfrage lautet:

> Welche realistischen Betriebs-/Architekturvarianten stehen für diesen Workload zur Verfügung, welche Handlungsfähigkeit gewinnen oder verlieren wir jeweils, welche Risiken und Chancen entstehen, wie gut sind unsere Aussagen belegt – und welche Variante empfehlen wir unter den Zielen und Grenzen dieser Organisation?

Die Methode darf eine begründete Empfehlung erzeugen. Die finale Entscheidung, Risikoakzeptanz und rechtliche Würdigung bleiben beim Kunden.

---

## 2. Grundprinzip: Souveränität ist Handlungsfähigkeit, nicht Autarkie

Digitale Souveränität wird im Radar nicht als maximale Unabhängigkeit verstanden. Maßgeblich ist die Fähigkeit einer Organisation, technologische Entscheidungen bewusst zu treffen, Daten und Systeme angemessen zu kontrollieren, auf geänderte Rahmenbedingungen reagieren zu können und erforderliche Wechsel- oder Fortführungsoptionen praktisch auszuüben.

Der Bitkom-Leitfaden 2026 betont ausdrücklich Wahlfreiheit, Kontrolle und Fähigkeiten sowie das gemeinsame Denken von technischen, vertraglichen und organisatorischen Optionen (`SRC-17`). Er stellt ebenso heraus, dass auch Nichtstun bzw. übertriebene Vorsicht strategische Risiken erzeugen kann. Daraus folgt für den Radar:

- On-Prem erhält keinen automatischen Souveränitätsbonus.
- Ein ausländischer oder außereuropäischer Provider erhält keinen pauschalen Malus.
- Ein hoher Grad formaler Kontrolle zählt nur, wenn die Organisation diese Kontrolle praktisch ausüben kann.
- Souveränität wird als Spektrum und als Fähigkeit zur bewussten Steuerung von Abhängigkeiten betrachtet.
- Chancen, Innovation und Risiken des Status quo werden mitbewertet.

**Provenienz:** `external-derived` aus `SRC-17`, ergänzt durch `internal-method`.

---

## 3. Was wird verglichen?

Ein Entscheidungsfall vergleicht mehrere Betriebs-/Architekturvarianten für denselben Workload oder eng abgegrenzten Workload-Verbund.

Typische Varianten:

- bestehendes On-Prem
- modernisiertes On-Prem / Private Cloud
- Colocation / Managed Private Cloud
- Public Cloud bei US-, europäischen, deutschen oder chinesischen Providern
- Sovereign-Cloud-Angebot
- SaaS
- Hybrid-/Multi-Cloud
- hypothetische Soll-/Referenzarchitektur

Der Variantentyp selbst ist nur eine Beschreibung. Er erzeugt keine automatische Bewertung.

Bei einer Migrations- oder Modernisierungsentscheidung soll die **Status-quo-/Nichtstun-Variante** grundsätzlich explizit betrachtet werden, sofern sie realistisch ist. Damit werden auch Innovations-, Modernisierungs-, Skill-, Security- und Betriebsrisiken sichtbar, die aus dem Verbleib im Ist-Zustand entstehen.

**Provenienz:** `internal-method`, gestützt durch `SRC-17`.

---

## 4. Die sieben sichtbaren Entscheidungsdimensionen

Die Managementsicht soll bewusst einfacher sein als die interne Methoden- und Frameworkschicht.

| Dimension | Leitfrage |
|---|---|
| **1. Geschäft & Innovation** | Welchen fachlichen Nutzen, Time-to-Market, Modernisierungs- oder Innovationsvorteil gewinnen oder verlieren wir mit dieser Variante – einschließlich Nichtstun? |
| **2. Security & Resilienz** | Kann der Workload sicher, verfügbar, wiederherstellbar und gegenüber relevanten Störungen robust betrieben werden? |
| **3. Recht, Daten & Kontrolle** | Wer kann rechtlich, technisch oder organisatorisch auf Daten, Schlüssel, Administration und Betrieb einwirken? |
| **4. Technologie & Exit** | Können Daten, Anwendungen und wesentliche Funktionen in akzeptabler Zeit und zu vertretbaren Kosten ersetzt, verlagert oder weiterbetrieben werden? |
| **5. Organisation & Skills** | Besitzt die Organisation die erforderlichen Fähigkeiten, Verantwortlichkeiten und Betriebsmodelle, um die Variante tatsächlich zu steuern? |
| **6. Lieferkette & Geopolitik** | Von welchen Providern, Konzernen, Staaten, Subunternehmern, Hardware-/Softwarekomponenten und gemeinsamen Abhängigkeiten hängt die Variante ab? |
| **7. Wirtschaft & Vertrag** | Welche laufenden Kosten, Preis-/Lizenzrisiken, Vertragsabhängigkeiten, Wechselkosten und Behandlungsaufwände entstehen? |

Daneben wird separat ausgewiesen:

> **Belastbarkeit der Erkenntnisse / Evidence Confidence** – Wie gut sind die Aussagen über die jeweilige Variante tatsächlich belegt?

Evidence Confidence ist keine achte Risikodimension und darf Risikohöhe nicht ersetzen.

**Provenienz:** `internal-method`; Dimensionen werden durch `SRC-03`, `SRC-04`, `SRC-08`, `SRC-12`, `SRC-17` fachlich gestützt.

---

## 5. Ablauf des Assessments

### Schritt 1 – Entscheidungsfrage und Scope klären

Zu Beginn werden nur die Informationen erhoben, die für den Vergleich wirklich gemeinsam gelten:

- Geschäftsprozess / Business Function
- Workload / IT-Service
- Zweck und fachliche Bedeutung
- Kritikalität
- Schutzbedarf Vertraulichkeit, Integrität, Verfügbarkeit
- Datenklassen
- RTO/RPO bzw. fachliche Ausfalltoleranz, soweit bekannt
- regulatorischer / vertraglicher Kontext
- Risikoappetit und nicht kompensierbare Mindestkriterien
- strategische Ziele und gewünschter Nutzen
- vorhandene Organisation-Capabilities und Skills

Das BSI fordert für Risikoanalysen Scope, Zielobjekte, Schutzbedarf, Risikoakzeptanzkriterien und Leitungsverantwortung (`SRC-01`). Der Radar nutzt diese Logik, ohne vorauszusetzen, dass der Kunde bereits vollständigen IT-Grundschutz umgesetzt hat.

### Schritt 2 – realistische Varianten definieren

Jede Variante wird ausreichend konkret beschrieben, z. B.:

- Provider / Betreiber / Legal Entity
- Angebot / Service / Region
- zentrale Architekturkomponenten
- Daten- und Kontrollpfade
- IAM / Key Control
- Backup / Restore / Failover
- wesentliche externe Abhängigkeiten
- Vertrags-/Supportmodell
- erwartete Betriebsorganisation

Für On-Prem gelten dieselben Prinzipien: Hersteller-, Lizenz-, Hardware-, Support- und Skill-Abhängigkeiten werden nicht ausgeblendet.

### Schritt 3 – vorhandene Informationen vorbefüllen

Bevor Interviews geführt werden, werden vorhandene Kundenartefakte soweit wirtschaftlich sinnvoll ausgewertet. Ziel ist nicht ein vollständiges Enterprise-Architecture- oder ISMS-Projekt, sondern die Verringerung unnötiger Fragen.

Mögliche Inputs:

- Servicekatalog / CMDB
- ArchiMate / Enterprise-Architecture-Modelle
- Architekturdiagramme
- BIA / BCM-Dokumente
- ISMS / Risikoregister
- Verträge, SLA, AVV, Exit-/Kündigungsklauseln
- Terraform / OpenTofu / Bicep / CloudFormation
- Kubernetes, Helm, Argo CD und andere deklarative Plattformartefakte
- IAM-/PKI-/KMS-Dokumentation
- FinOps-/Kosteninformationen
- Backup-/Restore-/DR-/Exit-Testprotokolle

Keiner dieser Inputs ist Pflicht. Der Radar muss auch mit Interviews und wenigen vorhandenen Dokumenten funktionieren.

### Schritt 4 – kurzes Screening-Interview

Das Standardassessment startet nicht mit allen Detailfragen. Ziel sind ca. **15–25 Kernfragen**, abhängig von Fall und bereits vorhandenen Informationen.

Das Screening klärt vor allem:

- Welche Varianten sind realistisch?
- Welche Anforderungen sind nicht verhandelbar?
- Wo bestehen wesentliche Unterschiede zwischen den Varianten?
- Welche Behauptungen sind bereits belegt?
- Welche Sorgen oder politischen/geopolitischen Annahmen beeinflussen die Entscheidung?

### Schritt 5 – adaptive Vertiefung

Die bestehende Fragenbank bleibt als **Question Library** erhalten. Sie ist kein Standardfragebogen.

Eine Frage wird vertieft, wenn mindestens eines gilt:

1. die Antwort kann die Empfehlung materiell verändern;
2. ein Hard Gate / Mindestkriterium hängt davon ab;
3. ein erhebliches Risiko oder ein wesentlicher Vorteil ist ungeklärt;
4. die Varianten unterscheiden sich gerade in diesem Punkt;
5. die Evidence ist für eine entscheidungsrelevante Aussage unzureichend oder widersprüchlich.

Wenn eine Variante an einem echten nicht kompensierbaren Mindestkriterium scheitert, muss sie nicht in allen Nebendimensionen bis zur gleichen Tiefe weiteranalysiert werden. Sie kann für Vergleichs- und Lernzwecke weiterhin sichtbar bleiben.

### Schritt 6 – Sorgen in prüfbare Szenarien übersetzen

Politische, geopolitische oder ideologisch aufgeladene Aussagen werden weder pauschal bestätigt noch verworfen.

Beispiel:

> „Seit den politischen Entwicklungen in den USA ist eine US-Cloud zu riskant.“

Der Radar übersetzt dies in prüfbare Szenarien, etwa:

- staatlich erzwungener Daten-/Systemzugriff
- Exportkontrolle oder Sanktion
- erzwungene Servicebeschränkung oder -einstellung
- Verlust von Support oder Updates
- Änderung von Eigentum / Kontrolle
- Vertrags- oder Preisanpassung

Für jedes Szenario wird geprüft:

- Welche Variante ist tatsächlich exponiert?
- Welche technischen, rechtlichen, vertraglichen oder organisatorischen Maßnahmen bestehen?
- Wie lange kann der Workload ohne den betroffenen Akteur weiterbetrieben werden?
- Gibt es reale Alternativen oder Exit-Pfade?
- Welche Evidenz stützt die Aussage?

Dasselbe Szenario wird auch auf On-Prem angewandt, wenn dort z. B. ausländische Hardware-, Software-, Lizenz-, Support- oder Trust-Anchor-Abhängigkeiten bestehen.

**Provenienz:** `internal-method`, gestützt durch `SRC-03`, `SRC-17` und die bestehenden Souveränitätsrisiken.

### Schritt 7 – Varianten vergleichen und behandeln

Je Variante werden mindestens getrennt dargestellt:

- Hard-Gate-/Mindestkriteriumsstatus
- sieben Entscheidungsdimensionen
- Workload Sovereignty Risk
- Security / Operational Risk
- Evidence Confidence
- wesentliche Chancen / Nutzen
- erforderliche Maßnahmen
- Kosten / Aufwand / Umsetzungszeit
- Restrisiko nach Behandlung
- offene Evidence Gaps

Ein einzelner Wahrheitsscore ist nicht erforderlich. Optionale Scores dienen nur der Managementorientierung und dürfen Hard-Gate-Fails nicht kompensieren.

### Schritt 8 – Empfehlung und Kundenentscheidung

Die Entscheidungsvorlage soll eine bevorzugte Variante oder Ranggruppe nennen können und transparent begründen:

- warum
- unter welchen Annahmen
- mit welchen Bedingungen / Maßnahmen
- welche Trade-offs bestehen
- welche Restrisiken verbleiben
- welche Erkenntnisse unsicher sind
- wie sensitiv die Empfehlung gegenüber geänderten Prioritäten ist

Die finale Entscheidung bleibt beim Kunden.

---

## 6. Rolle der Frameworks: weniger sichtbar, gezielter eingesetzt

Die Methode verwendet Frameworks **funktionsbezogen**, nicht kumulativ. Ein Kunde muss nicht mehrere vollständige Assessments parallel durchlaufen.

### 6.1 Bitkom Cloud-Souveränität 2026 – Orientierungs- und Entscheidungsrahmen

`SRC-17` ist für den Radar eine zentrale konzeptionelle Referenz, weil der Leitfaden:

- Souveränität als Wahlfreiheit, Kontrolle und Fähigkeiten beschreibt;
- technische, vertragliche und organisatorische Optionen gemeinsam betrachtet;
- organisatorische Risiken, technologische Interdependenzen, Skills, wirtschaftliche Interdependenzen/Exit und politisch-regulatorische Risiken diskutiert;
- Chancen und Innovationsfähigkeit ausdrücklich mitdenkt;
- die Integration in bestehende Risikomanagementprozesse empfiehlt.

Der Leitfaden ist kein vollständiger normativer Risikokatalog. Seine Rolle ist Orientierungs-, Fragen- und Maßnahmenquelle.

### 6.2 EU Cloud Sovereignty Framework – Provider-/Service-Souveränität

`SRC-03` liefert acht Sovereignty Objectives (SOV-1 bis SOV-8) und eine Evidence-basierte Provider-/Servicebewertung. Diese Dimensionen werden als wichtige Quelle für Provider Intelligence und Service-Capability-Fragen genutzt.

Der Radar übernimmt **nicht automatisch** die Gewichtung oder den Sovereignty Score des konkreten EU-Beschaffungsverfahrens als universelle Bewertungsformel.

### 6.3 BSI C3A – prüfbare Cloud-Autonomieeigenschaften

`SRC-04` wird als wichtige deutsche Provider-/Service-Referenz genutzt. C3A hilft, Souveränitätseigenschaften von Cloud-Diensten prüfbar zu machen.

C3A ersetzt nicht das workload- und organisationsspezifische Variantenassessment.

### 6.4 BSI 200-3 – Anschlussfähigkeit, Deep Dive und Vollständigkeitscheck

`SRC-01` bleibt relevant für:

- Zielobjekt-/Scope-Logik
- Schutzbedarf und Risikoappetit
- Gefährdungsidentifikation
- zusätzliche Gefährdungen
- Risikoeinschätzung / -bewertung
- Risikobehandlung / Restrisiko

Der Radar behauptet jedoch nicht, dass jedes Souveränitätsassessment vollständig „nach BSI 200-3“ durchgeführt wird.

Die 47 elementaren Gefährdungen dienen vor allem als:

- Referenz- und Vollständigkeitskatalog
- Deep-Dive-Quelle bei Security-/Resilienzfragen
- Anschlussstelle für IT-Grundschutz-Kunden

Sie müssen nicht als 47 sichtbare Interviewblöcke abgearbeitet werden.

### 6.5 Data Act – allgemeiner Exit-/Switching-Layer

`SRC-12` ist für Cloud-Souveränität besonders relevant, weil Kapitel VI den Wechsel zwischen Datenverarbeitungsdiensten bzw. zurück zu On-Prem, Portierung, Vertragsbedingungen, Informationen zu Wechselverfahren und Interoperabilität adressiert.

Der Data Act wird deshalb als allgemeine Rechts-/Exit-Referenz geführt, soweit der konkrete Dienst in seinen Anwendungsbereich fällt.

### 6.6 C5 und BSI-Mindeststandard – Evidence / öffentliche Verwaltung

`SRC-05` dient vor allem als Assurance-/Control-Evidence-Quelle für Cloud-Dienste. Ein Testat wird nicht als pauschaler Beweis für die Eignung eines konkreten Workloads behandelt.

`SRC-21` ist bei Bundesverwaltung bzw. einschlägigen öffentlichen Auftraggebern ein spezifisches Compliance-/Governance-Overlay.

### 6.7 NIS2 und DORA – aktivierbare Overlays und Methodenquellen

`SRC-06` bestätigt Anforderungen an ein dokumentiertes Risikomanagementverfahren, Behandlung und Managementakzeptanz. Diese Logik unterstützt den Radar, wird aber nicht als zusätzliche vollständige Prüfung für jeden Kunden ausgeführt.

`SRC-08` ist besonders wertvoll für Drittparteien-, Substituierbarkeits-, Konzentrations- und Exit-Fragen. Für Finanzunternehmen kann daraus ein DORA-Compliance-Overlay entstehen; für andere Kunden bleiben einzelne Erkenntnisse methodische Quellen, ohne DORA-Anwendbarkeit zu behaupten.

### 6.8 Weitere Overlays

Je nach Kunde und Workload können weitere Profile aktiviert werden, z. B.:

- DSGVO / EDPB Transfer Assessment
- AI Act
- BSI-/KI-spezifische Kriterien
- sektorspezifische Aufsicht
- interne Policies / Vergabevorgaben

Grundregel:

> Ein Framework wird nur dann als Compliance-Overlay aktiviert, wenn es für den konkreten Kunden oder Workload anwendbar ist. Andernfalls darf es als Methoden-/Fragenquelle dienen, aber nicht als behauptete Pflicht.

---

## 7. Daten- und Intake-Prinzip

Der Radar soll möglichst viel vorhandenes Wissen verwenden, ohne die Nutzung von Enterprise-Architecture-, CMDB- oder IaC-Werkzeugen vorauszusetzen.

### 7.1 Bevorzugte Reihenfolge

```text
vorhandene Artefakte einlesen
        -> vorläufiges Kontextbild
        -> Screening-Interview
        -> Entscheidungslücken
        -> gezielte Evidence Requests
        -> Vergleich / Empfehlung
```

### 7.2 ArchiMate

ArchiMate-Modelle sind eine wertvolle optionale Quelle für Beziehungen zwischen Business-, Application- und Technology-Layer. Standardisierte ArchiMate-Austauschformate oder tool-spezifische Exporte können über Adapter in das generische Kontextmodell überführt werden.

Ein ArchiMate-Modell ist **keine Voraussetzung**. Ist es unvollständig oder veraltet, wird dies als Kontext-/Evidence-Grenze sichtbar gemacht.

### 7.3 Diagramme und natürliche Sprache

Architekturdiagramme und Interviews sind ebenfalls zulässige Intake-Kanäle. Ein Diagramm kann Architekturkontext liefern, ist aber nicht automatisch technische Evidence für die tatsächliche Konfiguration.

### 7.4 Maschinenlesbare Artefakte

Deklarative Infrastruktur- und Plattformartefakte können besonders wertvoll sein, weil sie näher an der realen Konfiguration liegen. Dennoch gelten Scope, Aktualität und Review.

---

## 8. Evidence und Erkenntnissicherheit

Das bestehende Prinzip bleibt unverändert:

> Provider-/Service Capability ≠ Applied Capability.

Providerdokumentation kann zeigen, dass eine Funktion verfügbar ist. Erst kundenspezifische Architektur-, Konfigurations-, Vertrags- oder Test-Evidence zeigt, ob sie im konkreten Workload tatsächlich wirksam genutzt wird.

Fehlende Evidence führt zu `UNVERIFIED`, nicht automatisch zu PASS oder FAIL.

Menschlich geprüfte Claims bleiben die Brücke zwischen Evidence und deterministischer Gate-/Regelauswertung.

---

## 9. Was der Radar ausdrücklich nicht sein soll

Der Radar ist nicht:

- ein politisches Ranking von Staaten oder Providern
- ein Zertifizierungsersatz
- ein vollständiges BSI-/NIS2-/DORA-/DSGVO-Audit für jeden Kunden
- ein 128-Fragen-Pflichtfragebogen
- ein einzelner Souveränitäts-Score ohne Kontext
- eine automatische rechtliche Entscheidung
- eine automatische Risikoakzeptanz
- ein Zwang, ArchiMate, CMDB oder Cloud-Credentials bereitzustellen

---

## 10. Minimales Beispiel

**Entscheidungsfrage:** Wo soll ein kritisches Fachverfahren zukünftig betrieben werden?

**Gemeinsame Fakten:** hohe Verfügbarkeit, personenbezogene Daten, RTO vier Stunden, begrenzte 24x7-Betriebsfähigkeit, Wunsch nach schneller Modernisierung.

**Varianten:**

A. heutiges On-Prem  
B. US-Hyperscaler in EU-Region  
C. deutscher/europäischer Cloud-Provider

**Möglicher Vergleich:**

- A besitzt hohe unmittelbare technische Kontrolle, aber schwache geografische Redundanz und Skill-/Personalausfallrisiken.
- B besitzt starke Resilienz und schnelle Managed-Service-Fähigkeiten, aber höhere rechtliche, technologische und Provider-Abhängigkeiten.
- C reduziert bestimmte Jurisdiktions-/Kontrollrisiken, kann aber bei Servicebreite, Resilienz oder Skills andere Nachteile besitzen.

Die Empfehlung entsteht nicht aus Herkunft oder Bauchgefühl, sondern aus den konkreten Anforderungen, belegten Eigenschaften, Risiken, Chancen, Kosten und realen Behandlungsoptionen.

---

## 11. Methodische Leitregel

> **So wenig Erhebung wie möglich, so viel Vertiefung wie für eine belastbare Entscheidung nötig.**

Die interne Methoden-, Fragen- und Frameworktiefe darf groß sein. Die sichtbare Beratungsmethode soll dagegen fokussiert, verständlich und entscheidungsorientiert bleiben.
