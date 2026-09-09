# NEXT-118 – Erstes Product-Owner-/Consultant-Review: Assessment-Einstieg

Datum: 2026-09-09

## Status des manuellen Durchlaufs

- Installation nach Bereinigung der beiden Installer-Funde erfolgreich.
- Product Owner / Test-Consultant hat den Test bewusst nach dem ersten Formular `Neues Assessment` gestoppt.
- Gesamturteil zum aktuellen Produktstand: **noch nicht einsatzfähig**.
- Grund: Der Assessment-Einstieg bildet die für spätere Souveränitäts- und Compliance-Bewertungen benötigten Kunden-, Organisations- und Workload-Fakten noch nicht sauber genug ab.

## Human Review – dokumentierte Aussagen

### Installation

Bewertung: **gut / einem durchschnittlichen ITM-Consultant zumutbar**, sobald die im selben Durchlauf gefundenen Recovery-Probleme behandelt sind.

### Verständlichkeit

Grundsätzlich verständlich, aber bereits das Formular `Neues Assessment` ist fachlich zu flach bzw. teilweise missverständlich.

### Konkrete Befunde

1. `Name` ist unklar: Projektname, Kunde, Assessment oder Workload?
2. `Kunde` als einfacher String reicht nicht; Unternehmens-/Behördenstammdaten und Standort/Jurisdiktion fehlen.
3. Konzern-/Tochtergesellschaften müssen berücksichtigt werden können, weil Workloads einer oder mehreren juristischen Einheiten zugeordnet sein können.
4. Eine kuratierte Workload-Kategorisierung kann hilfreich sein, sollte aber geprüft werden; natürliche Beschreibung bleibt erforderlich.
5. `Regulatorischer Kontext` als freies manuelles Eingabefeld ist nicht die gewünschte Zielrichtung. Das Tool soll aus strukturierten Fakten Compliance-Kandidaten ableiten und Unsicherheit sichtbar machen.
6. Standort/Adresse allein reicht dafür nicht; Unternehmensgröße, Branche/Tätigkeit, Rechts-/Organisationsform, Rolle und weitere anforderungsspezifische Fakten müssen einfließen.
7. Kritikalität sowie C/I/A sollen nicht zwingend bereits beim Anlegen des Assessments manuell festgelegt werden. Sie sollen später aus Business-Impact-/Schutzbedarfsfakten vorgeschlagen und menschlich bestätigt werden können.
8. LLM-/Regellogik darf aus natürlicher Workload-Beschreibung Vorschläge ableiten, aber keine finale Schutzbedarfs- oder Rechtsfeststellung ohne Human Review erzeugen.

## Produktentscheidung

Der manuelle NEXT-118-Durchlauf wird **nicht** mit den nachfolgenden Tabs fortgesetzt, bevor der Assessment-Einstieg fachlich und UX-seitig neu entworfen wurde.

## Folgearbeit

Vorgeschlagen: neuer P0-Arbeitsschritt `Assessment Intake / Decision Context v0.5` vor der Fortsetzung des manuellen NEXT-118-Reviews.

HUMAN GATE: Product-Owner-Richtung bereits gegeben – Einstieg zuerst überarbeiten; konkrete Feld-/Wizard-/Automatisierungsentscheidungen benötigen noch HITL-08/HITL-09 vor Runtime-Migration.