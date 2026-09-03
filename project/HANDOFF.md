# Project Handoff

## Wo stehen wir?

Der Souveränitätsradar ist von einer BSI-200-3-Abgleichstabelle zu einem Methoden- und Toolprojekt gewachsen.

R1–R4 entwickelten Taxonomie, Fragen, Provenienz, Szenariotests und Bewertungslogik. R5 führte erstmals reale öffentliche Provider-Evidence am Beispiel eines Bedrock-KI-Agenten ein. R6 baut darauf einen read-only technischen Evidence-Collector auf.

## Fachlicher Kern

Die Methode bewertet nicht „den Anbieter“ abstrakt, sondern einen **Workload in einer konkreten Provider-/Service-/Architektur-/Vertragskonstellation**.

Wichtige getrennte Ausgaben:

- Security Capability
- Sovereignty Capability
- Workload Sovereignty Risk
- klassisches Informationssicherheits-/Betriebsrisiko
- Evidence Confidence

Wichtige Hard Gates:

- Jurisdiktion & Effective Control
- Datenresidenz & Verarbeitung
- Schlüsselhoheit
- Exit & Portabilität
- Operational Autonomy
- Identity & Trust Anchors
- Supply Chain Critical Dependencies
- Security Minimum

## Was ist bereits implementiert?

- Methodenmodell v0.9 als Excel-Workbook
- CSV-Exporte der wichtigsten Methodentabellen
- erste Python-Regelengine unter `src/sovradar/`
- JSON-Schemas für Evidence/Assessment
- R6 read-only AWS Bedrock Evidence Collector
- R6 Normalizer
- GitHub-Review-/Agenten-/PM-Struktur

## Was darf ein neuer Agent NICHT tun?

- keine Methodenschwelle als externe Normvorgabe ausgeben
- keine öffentliche Provider-Dokumentation als kundenkonfigurierte Applied Capability behandeln
- kein fehlendes Evidence als technisches FAIL erfinden
- keine Raw Kundenevidence committen
- keine Evidence-Collector-Write-/Invoke-Operation ohne neue Architekturentscheidung einführen

## Nächster operative Schritt

`NEXT-001`: Collector in einem autorisierten AWS-Bedrock-Account ausführen. Danach `NEXT-002`: normalized Evidence in die Gate Engine übernehmen.

## Review-Bedarf

Die Bootstrap-Struktur selbst soll per PR reviewed werden. Danach sollten Methodik- und Codeänderungen getrennte PRs erhalten, damit fachlicher Review und Software-Review unabhängig möglich bleiben.
