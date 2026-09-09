# Human-in-the-Loop Governance

Stand: 09.09.2026

Dieses Dokument legt fest, an welchen Stellen im Souveränitäts-Radar menschliche Entscheidungen zwingend erforderlich sind und welche Rolle die Entscheidung verantwortet. Ziel ist nicht, Automatisierung zu verhindern, sondern fachliche, rechtliche und produktbezogene Verantwortung dort explizit zu machen, wo sie nicht an Agenten, LLMs, Tests oder deterministische Regeln delegiert werden darf.

## Grundregel

Automatisierung darf recherchieren, vorstrukturieren, Vorschläge erzeugen, Evidenz extrahieren, Varianten berechnen, Tests ausführen und Inkonsistenzen markieren. Sie darf jedoch keine der unten genannten Human Gates selbst freigeben.

Ein Human Gate hat immer vier Angaben:

- **Entscheidung:** Was muss ein Mensch entscheiden oder bestätigen?
- **Verantwortliche Rolle:** Wer trägt die Verantwortung?
- **Eingang:** Welche Artefakte oder Befunde müssen vorliegen?
- **Freigabe:** Welcher explizite menschliche Output erlaubt den nächsten Schritt?

## Rollen

### Product Owner
Verantwortet Produktziel, Nutzerwert, Priorisierung, sichtbare UX und die Entscheidung, ob ein Ergebnis als Produktfunktion in die Runtime überführt wird.

### Projektleiter
Verantwortet Reihenfolge, Abhängigkeiten, Ressourcen, Einbindung weiterer Personen sowie Go/No-Go zwischen Arbeitsphasen. Der Projektleiter entscheidet nicht automatisch fachliche oder rechtliche Inhalte.

### Method Owner / Lead Consultant
Verantwortet fachliche Konsistenz der Methode, Interviewlogik, Entscheidungsdimensionen, Risikomodell, Requirement-Profile, Hard Gates und die Plausibilität der erzeugten Empfehlung.

### Evidence Reviewer / Consultant
Bestätigt, dass Evidence eine konkrete Claim-Aussage tatsächlich trägt. Kein LLM-Vorschlag darf diese Freigabe ersetzen.

### Legal / Compliance Reviewer
Bewertet Rechtsanwendbarkeit und rechtliche Schlussfolgerungen, wenn das Ergebnis über eine reine methodische Quellenzuordnung hinausgeht. Diese Rolle kann je nach Projekt intern oder kundenseitig besetzt sein.

### Kunde / Risk Owner
Akzeptiert Restrisiken und trifft die finale Betriebs-/Architekturentscheidung. Diese Entscheidung verbleibt beim Kunden und darf weder Product Owner noch Radar automatisiert übernehmen.

## Verbindliche Human Gates

### HITL-01 — Scope und Decision Case freigeben

**Entscheidung:** Ist der zu untersuchende Workload korrekt abgegrenzt und sind die zu vergleichenden Varianten realistisch und entscheidungsrelevant?

**Verantwortliche Rolle:** Method Owner / Lead Consultant; bei Prioritäts- oder Scope-Konflikten zusätzlich Product Owner bzw. Projektleiter.

**Eingang:** Workload-Kontext, vorhandene Architektur, Zielbild, Variantenliste, bekannte Constraints.

**Freigabe:** Explizites `GO` für Decision Case und Varianten. Ohne Freigabe keine finale Variantenbewertung.

### HITL-02 — Requirement Profile und nicht kompensierbare Mindestanforderungen freigeben

**Entscheidung:** Welche Anforderungen sind für den konkreten Kundenfall tatsächlich verbindlich und welche davon sind Hard Gates?

**Verantwortliche Rolle:** Method Owner / Lead Consultant; bei regulatorischer Begründung zusätzlich Legal / Compliance Reviewer; finale geschäftliche Mindestanforderungen mit Kunde / Risk Owner.

**Eingang:** Kundenanforderungen, regulatorische Anwendbarkeit, C3A/C5/BSI/vertragliche Quellen, interne Policies.

**Freigabe:** Versioniertes Requirement Profile mit Begründung. Framework-Kriterien dürfen nicht automatisch zu globalen Hard Gates werden.

### HITL-03 — Evidence -> Claim prüfen

**Entscheidung:** Trägt die vorliegende Evidence die behauptete Aussage für den betrachteten Scope?

**Verantwortliche Rolle:** Evidence Reviewer / Consultant.

**Eingang:** Evidence, extrahierte Fakten, Scope, vorgeschlagener Claim.

**Freigabe:** `reviewed/accepted`, `reviewed/rejected` oder `needs_more_evidence`. Nur akzeptierte Human-reviewed Claims dürfen deterministische Gates beeinflussen.

### HITL-04 — Rechtliche Anwendbarkeit und rechtliche Schlussfolgerung prüfen

**Entscheidung:** Ist ein Compliance-Overlay tatsächlich anwendbar und ist die daraus gezogene rechtliche Schlussfolgerung belastbar?

**Verantwortliche Rolle:** Legal / Compliance Reviewer bzw. zuständige Fachperson beim Kunden.

**Eingang:** Sachverhalt, Rechtsquelle, Scope, Jurisdiktion, Vertragskontext.

**Freigabe:** Dokumentierte Anwendbarkeit/Begründung. Automatisierte Recherche oder LLM-Auslegung ist nur Vorschlag.

### HITL-05 — Methodische Plausibilitätsprüfung der Variantenbewertung

**Entscheidung:** Sind Risiken, Chancen, Unsicherheiten, Hard Gates und Unterschiede zwischen Varianten nachvollziehbar und frei von offensichtlich methodischen Artefakten?

**Verantwortliche Rolle:** Method Owner / Lead Consultant.

**Eingang:** Bewertungsresultate aller Varianten, Evidence Confidence, offene Gaps, Status-quo-Risiken, Business-/Innovationsnutzen.

**Freigabe:** Fachliches `plausible`, `rework` oder `blocked`. Ohne `plausible` keine Management-Empfehlung.

### HITL-06 — Management-Empfehlung freigeben

**Entscheidung:** Ist die Empfehlung inhaltlich vertretbar, verständlich, entscheidungsorientiert und angemessen vorsichtig formuliert?

**Verantwortliche Rolle:** Lead Consultant / Method Owner; Product Owner prüft Produktdarstellung, nicht Kundenrisikoakzeptanz.

**Eingang:** Variantenvergleich, Gates, Risiken, Chancen, Evidence Gaps, Annahmen und offene Entscheidungen.

**Freigabe:** Freigegebene Consultant-Empfehlung. Der Radar darf eine Empfehlung erzeugen, aber nicht ohne menschliche Prüfung final ausgeben.

### HITL-07 — Kundenentscheidung und Risikoakzeptanz

**Entscheidung:** Welche Variante wird gewählt und welche Restrisiken werden akzeptiert?

**Verantwortliche Rolle:** Kunde / Risk Owner.

**Eingang:** Freigegebene Empfehlung, Restrisiken, Kosten, Verträge, Umsetzungsfolgen.

**Freigabe:** Kundenseitige Entscheidung bzw. dokumentierte Risikoakzeptanz. Nicht automatisierbar.

### HITL-08 — Produkt-/Runtime-Migration freigeben

**Entscheidung:** Ist eine fachliche Regel oder neue UX ausreichend validiert, um in Runtime, Scoring, Gates oder Standard-Screening übernommen zu werden?

**Verantwortliche Rolle:** Product Owner; Method Owner muss fachlich zustimmen. Projektleiter koordiniert Umsetzung und Reihenfolge.

**Eingang:** Referenzfallvalidierung, Regressionsergebnisse, offene Methodenfragen, UX-Befunde.

**Freigabe:** Produkt-Go/No-Go mit Scope der Implementierung. Keine automatische Übernahme von Forschungs- oder Crosswalk-Ergebnissen in produktive Regeln.

### HITL-09 — Merge bei substanziellen Methodenänderungen

**Entscheidung:** Ist die Änderung fachlich verstanden und mit Projektziel und Methodenkern vereinbar?

**Verantwortliche Rolle:** Product Owner oder Method Owner. Bei reinen Engineering-/Hygiene-Änderungen reicht technisches Review gemäß Repository-Regeln.

**Eingang:** PR-Diff, Tests, Provenienz, Auswirkungen auf Methode/Runtime.

**Freigabe:** Menschliches Review vor Merge. Grün laufende CI ist notwendig, aber nicht hinreichend für substantielle Methodenänderungen.

## Aktuelle Human Gates für die nächsten Arbeitsschritte

### NEXT-118 — Erste manuelle Consultant-Installation

Hier ist der Human-in-the-Loop **jetzt zwingend**.

Der Nutzer/Projektverantwortliche soll die Anwendung selbst auf einem frischen Zielsystem installieren und als echter Consultant benutzen. Ein synthetischer CI-Walkthrough ersetzt diese Erfahrung nicht.

**Deine Rolle:** gleichzeitig Product Owner und Test-Consultant.

Du musst insbesondere entscheiden bzw. dokumentieren:

1. Ist die Installation aus Consultant-Sicht verständlich und realistisch?
2. Welche Schritte erzeugen unnötige technische Reibung?
3. Wo suggeriert die pre-v0.4-UI eine fachlich falsche Priorität?
4. Welche Informationen oder Fragen fehlen, obwohl du sie in einem echten Kundengespräch erwarten würdest?
5. Würdest du mit diesem Stand vor einen Kunden treten: `ja`, `nur intern`, oder `nein`?

**Gate:** NEXT-118 darf erst als abgeschlossen gelten, wenn diese manuelle Bewertung von einem Menschen dokumentiert wurde.

### NEXT-119 — Methodenkern an Referenzvarianten validieren

Automatisierung kann die Testfälle aufbauen und Ergebnisse vorbereiten. Mehrere Entscheidungen müssen aber menschlich erfolgen.

**Deine Rollen:** primär Method Owner / Lead Consultant, sekundär Product Owner.

Pflichtpunkte für deinen Human Review:

1. **HITL-01:** Referenz-Workload und mindestens drei Varianten freigeben.
2. **HITL-02:** kundenspezifische Mindestanforderungen und Hard Gates bestätigen; keine Framework-Anforderung automatisch übernehmen.
3. Screeningvorschlag auf etwa 15–25 Kernfragen prüfen: Fehlt etwas entscheidungsrelevantes? Ist etwas nur Framework-Overhead?
4. Aktivierungsregeln für BSI-, C3A-, C5- und Compliance-Deep-Dives fachlich bestätigen.
5. **HITL-05:** Ergebnis aller Varianten auf Plausibilität prüfen. Wenn das Modell eine aus deiner Consultant-Sicht absurde Empfehlung erzeugt, wird nicht die Realität an den Score angepasst, sondern die Methodik untersucht.
6. **HITL-06:** Empfehlungstext prüfen: Würdest du ihn einem Kunden gegenüber vertreten und erklären können?
7. **HITL-08:** erst danach entscheiden, welche validierten Regeln in die Runtime migriert werden.

## Spätere zwingende Human Gates

- **NEXT-108 Inter-Rater-Kalibrierung:** mindestens ein weiterer realer Berater muss denselben Fall unabhängig bewerten. Ein zweiter Agent zählt nicht als Inter-Rater.
- **Provider Intelligence:** öffentliche Provider-Aussage darf Capability dokumentieren, aber nicht ohne menschliche Prüfung als kundenseitig konfigurierte Applied Capability gelten.
- **Regulatorische Overlays:** Aktivierung darf vorbereitet werden, die rechtliche Anwendbarkeit benötigt bei relevanten Entscheidungen menschliche Fachprüfung.
- **Kundenevidence:** Raw Evidence darf analysiert werden, aber Claims und Scope-Zuordnung benötigen Human Review.
- **Finale Risikoakzeptanz:** immer Kunde / Risk Owner.

## Kennzeichnung in künftigen Arbeitsständen

Ab sofort sollen Arbeitsberichte und Übergaben, wenn ein Human Gate erreicht wird, explizit mit folgendem Muster enden:

`HUMAN GATE: <ID> | Rolle: <Rolle> | Entscheidung benötigt: <konkrete Frage> | Optionen: <A/B/...> | Empfehlung des Agenten: <Vorschlag + Begründung>`

Wenn kein Human Gate erforderlich ist, soll ausdrücklich `HUMAN GATE: none` angegeben werden.
