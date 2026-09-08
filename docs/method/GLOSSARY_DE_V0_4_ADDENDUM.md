# Glossar-Modul – Methodenkern v0.4

Status: **aktueller Bestandteil der Terminologiereferenz**  
Basis: `docs/method/GLOSSARY_DE.md`  
Provenienz: überwiegend `[METHOD]`, siehe Begriff  
Issue: #67  
Review-Gate: #68 / NEXT-120

Dieses Modul ergänzt das Basisglossar um Begriffe des Decision-Support-Methodenkerns v0.4. **`GLOSSARY_DE.md` und dieses Modul gelten gemeinsam als aktuelle Terminologiereferenz.** Nach dem C3A-Volltextreview (#68) wird geprüft, ob C3A-Begriffe ergänzt oder Definitionen angepasst werden müssen; bis dahin werden keine C3A-Detailbegriffe aus unvollständig geprüftem Material vorweggenommen.

---

## Handlungsfähigkeit (`Agency` / im Radar meist ohne festen Code-Alias)
**Herkunft:** `[EXT] [METHOD]`

Die reale Fähigkeit einer Organisation, technologische Entscheidungen bewusst zu treffen, Systeme und Daten angemessen zu kontrollieren, Abhängigkeiten zu steuern und bei veränderten Rahmenbedingungen wirksame Alternativen auszuüben.

Im Radar ist Handlungsfähigkeit wichtiger als die Vorstellung vollständiger Autarkie.

**Beispiel:** Eine Organisation besitzt formal volle On-Prem-Kontrolle, kann ein kritisches System aber wegen fehlender Skills und fehlender Ersatzteile nicht zuverlässig betreiben. Die formale Kontrolle ist hoch, die praktische Handlungsfähigkeit dagegen begrenzt.

---

## Status-quo-/Nichtstun-Variante (`StatusQuoOption` / `DoNothingOption`)
**Herkunft:** `[METHOD]`

Die realistische Alternative, den heutigen Betriebszustand zunächst beizubehalten. Sie wird bei Migrations- und Modernisierungsentscheidungen als echte Variante betrachtet, damit auch Risiken und Chancen des Nichtstuns sichtbar werden.

**Nicht verwechseln mit:** „risikofrei“. Der Status quo kann z. B. EOL-, Security-, Skill-, Kosten- oder Innovationsrisiken enthalten.

---

## Geschäftlicher / strategischer Nutzen (`Business Value` / `Strategic Opportunity`)
**Herkunft:** `[EXT] [METHOD]`

Fachlicher oder strategischer Mehrwert einer Variante, z. B. schnellere Bereitstellung, bessere Skalierbarkeit, Zugang zu neuen Plattform-/KI-Funktionen, geringerer Betriebsaufwand oder höhere Innovationsfähigkeit.

Nutzen wird als eigener Entscheidungsinput sichtbar gemacht, darf aber nicht automatisch nicht kompensierbare Mindestkriterien oder unakzeptable Restrisiken überstimmen.

---

## Entscheidungsrelevanz (`Decision Relevance`)
**Herkunft:** `[METHOD]`

Maß dafür, ob eine zusätzliche Information, Frage oder Evidence die Entscheidung bzw. Empfehlung materiell verändern kann.

Eine Vertiefung ist insbesondere entscheidungsrelevant, wenn sie:

- einen Variantenunterschied klärt;
- ein Mindestkriterium betrifft;
- ein wesentliches Risiko oder einen wesentlichen Vorteil verändert;
- eine wichtige Unsicherheit/Evidence Gap schließt.

Entscheidungsrelevanz steuert die Tiefe des adaptiven Assessments.

---

## Fragenbibliothek (`Question Library`)
**Herkunft:** `[REPO] [METHOD]`

Die vollständige interne Sammlung methodischer Fragen. Sie dient als Wissens- und Deep-Dive-Bestand und ist **kein Pflichtfragebogen**.

Der Radar wählt für einen konkreten Fall nur den Teil aus, der für Screening, Mindestkriterien, Risiken, Variantenunterschiede und Evidence Gaps benötigt wird.

---

## Adaptives Assessment (`Adaptive Assessment`)
**Herkunft:** `[METHOD]`

Assessment-Vorgehen, bei dem die Prüftiefe nicht für jeden Fall vorab vollständig feststeht, sondern aus Scope, Kritikalität, Varianten, Antworten und Evidence Gaps abgeleitet wird.

Standardidee:

`Vorbefüllung -> 15–25 Screening-Fragen -> gezielte Deep Dives -> Evidence -> Vergleich`

Die vollständige Fragenbibliothek bleibt auditierbar, auch wenn nicht jede Frage aktiv bearbeitet werden muss.

---

## Screening / Kernscreening (`Screening`)
**Herkunft:** `[REPO] [METHOD]`

Kurze erste Erhebungsphase zur Klärung der Entscheidungsfrage, Varianten, kritischen Anforderungen, wesentlichen Unterschiede und wichtigsten Unsicherheiten.

Methodenkern v0.4 verwendet als Zielkorridor ungefähr 15–25 sichtbare Kernfragen. Diese Zahl ist eine interne Designhypothese und muss in Referenzfällen kalibriert werden.

---

## Deep Dive / Vertiefung (`Deep Dive`)
**Herkunft:** `[REPO] [METHOD]`

Gezielte zusätzliche Prüfung eines Bereichs, wenn das Screening keine ausreichende Entscheidungsgrundlage liefert.

Ein Deep Dive kann z. B. BSI-Gefährdungen, C3A/C5-Evidence, Vertragsprüfung, IaC-Auswertung, Exit-Test oder ein regulatorisches Overlay aktivieren.

---

## Framework-Rolle (`Framework Role`)
**Herkunft:** `[METHOD]`

Die konkrete Funktion, die ein Standard, Leitfaden oder Regulierungsrahmen im Radar erfüllt.

Beispiele:

- Orientierung / Entscheidungslogik
- Provider-/Service-Souveränität
- Security-/Risiko-Deep-Dive
- Assurance
- Exit / Switching
- Compliance-Overlay

**Grundsatz:** Mehrere Quellen müssen nicht als mehrere vollständige Audits gestapelt werden.

---

## Compliance-Overlay (`Compliance Overlay`)
**Herkunft:** `[METHOD] [SW]`

Zusätzliche Prüf- und Anforderungsschicht, die nur aktiviert wird, wenn ein regulatorischer oder interner Rahmen für den konkreten Kunden oder Workload tatsächlich einschlägig ist.

**Beispiele:** DORA für betroffene Finanzunternehmen, spezifische NIS2-Anforderungen, BSI-Mindeststandard für einschlägige Bundesstellen, AI-Act-spezifische Anforderungen.

Ein Framework kann als Methoden-/Fragenquelle verwendet werden, ohne dass daraus automatisch ein Compliance-Overlay entsteht.

---

## Kontextquelle (`Context Source`)
**Herkunft:** `[METHOD] [SW]`

Artefakt oder Informationskanal, aus dem Scope-, Architektur-, Organisations- oder Abhängigkeitsinformationen für den Entscheidungsfall gewonnen werden.

Beispiele:

- Interview
- Servicekatalog / CMDB
- ArchiMate / EA-Modell
- Architekturdiagramm
- BIA / BCM
- ISMS / Risikoregister
- IaC / GitOps
- FinOps

Eine Kontextquelle kann Informationen vorbefüllen, ist aber nicht automatisch ausreichende Evidence für eine Gate- oder Risikoaussage.

---

## Kontext-Fakt (`Context Fact`)
**Herkunft:** `[REPO] [METHOD]`

Strukturierte Information über den Scope oder die Architektur, die die Fragenwahl und Analyse steuert.

**Beispiel:** „Der Workload verwendet einen externen Identity Provider.“

**Nicht gleichsetzen mit Evidence:** Ein aus einem Interview oder LLM extrahierter Kontext-Fakt kann Folgefragen aktivieren, ohne die Aussage bereits belastbar zu beweisen.

---

## Artefaktgestützter Intake (`Artifact-Assisted Intake`)
**Herkunft:** `[METHOD]`

Erhebungsweise, bei der vorhandene Kundenartefakte zunächst zur Vorbefüllung des Kontextmodells genutzt werden und Interviews anschließend vor allem Lücken und Unklarheiten klären.

Der Radar soll auch ohne strukturierte Artefakte funktionieren.

---

## Geopolitisches Prüfszenario (`Geopolitical Scenario`)
**Herkunft:** `[METHOD]`

Konkretes, prüfbares Szenario, in das eine politische oder geopolitische Sorge übersetzt wird.

Beispiele:

- staatlich erzwungener Zugriff
- Sanktionen / Exportkontrollen
- Serviceentzug oder Servicebeschränkung
- Verlust von Support oder Updates
- Change of Control
- erhebliche Preis-/Vertragsänderung

Das Szenario wird auf alle relevanten Varianten angewandt. Die nationale Herkunft eines Providers ersetzt diese Analyse nicht.

---

## Providerherkunft / Jurisdiktionsbezug (`Provider Origin / Jurisdiction Fact`)
**Herkunft:** `[METHOD] [SW]`

Fakt über Sitz, Konzernkontrolle, Vertragspartner- oder sonstige relevante Jurisdiktionen eines Providers bzw. beteiligter Legal Entities.

**Wichtig:** Providerherkunft ist **kein Souveränitätsscore**. Erst konkrete Rechts-, Kontroll-, Lieferketten- und Fortführungsszenarien machen daraus einen bewertbaren Entscheidungsfaktor.

---

## Risiko des Nichtstuns (`Risk of Inaction`)
**Herkunft:** `[EXT] [METHOD]`

Risiko, das entsteht, wenn eine bestehende Lösung oder Betriebsweise beibehalten wird, obwohl relevante technologische, organisatorische, wirtschaftliche oder Security-Rahmenbedingungen sich verändern.

Beispiele:

- End-of-Life-Technologien
- Fachkräftemangel
- steigende Lizenz-/Betriebskosten
- fehlende Skalierbarkeit
- Sicherheitsdefizite
- entgangene Modernisierungs-/Innovationsmöglichkeiten

---

## Provider-/Service-Souveränitätslayer (`Provider / Service Sovereignty Layer`)
**Herkunft:** `[METHOD]`

Methodische Ebene, die Eigenschaften eines konkreten Cloud-Angebots, Services, seiner Region, Legal Entities und dokumentierten Capabilities beschreibt. EU Cloud Sovereignty Framework, BSI C3A und Provider/Assurance-Evidence sind wichtige Quellen für diese Ebene.

Sie ist getrennt vom workload- und organisationsspezifischen Souveränitätsrisiko.

**C3A-Hinweis:** Die genaue C3A-Begrifflichkeit und das Detailmapping werden erst nach Issue #68 / NEXT-120 als vollständig behandelt.

---

## BSI-Deep-Dive / BSI-Vollständigkeitscheck
**Herkunft:** `[BSI] [METHOD]`

Gezielter Einsatz von BSI 200-3 bzw. IT-Grundschutz zur detaillierten Prüfung von Security-/Resilienzrisiken, Gefährdungen und Risikobehandlung oder zur Kontrolle, ob relevante klassische Gefährdungen übersehen wurden.

Der Begriff bezeichnet **nicht** die Behauptung, dass das gesamte Radar-Verfahren automatisch eine vollständige Risikoanalyse nach BSI 200-3 darstellt.

---

# Zusätzliche Nicht-Gleichsetzungen für v0.4

| Nicht gleichsetzen | Warum |
|---|---|
| Question Library = Fragebogen | Die Bibliothek enthält Deep-Dive-Wissen; der konkrete Fall nutzt nur den entscheidungsrelevanten Teil. |
| Framework-Quelle = Compliance-Pflicht | Eine Quelle kann eine gute Frage liefern, ohne für den Kunden rechtlich anwendbar zu sein. |
| Kontext-Fakt = Evidence | Kontext steuert die Analyse; Evidence belegt entscheidungsrelevante Aussagen. |
| Providerherkunft = geopolitisches Risiko | Herkunft ist nur ein Fakt; das Risiko entsteht aus konkreten Rechts-, Kontroll-, Lieferketten- oder Fortführungsszenarien. |
| Status quo = risikofrei | Auch Nichtstun kann Security-, Kosten-, Skill- und Innovationsrisiken erzeugen. |
| Business Value = Risikoakzeptanz | Nutzen ist Entscheidungsinput; Risikoakzeptanz bleibt eine bewusste Managemententscheidung. |
| Maschinenlesbar = belastbar | IaC/CMDB/ArchiMate erleichtern Intake, ihre Aktualität, Scope und Qualität müssen dennoch geprüft werden. |
