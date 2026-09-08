# Risk Taxonomy

Die vollständige maschinenlesbare Tabelle liegt in `data/method/risk_taxonomy.csv`.

## Einordnung

Die Risikotaxonomie ist eine **interne Wissens-, Deep-Dive- und Szenariobibliothek**. Sie ist nicht identisch mit dem sichtbaren Standardinterview des Methodenkerns v0.4.

Der Radar führt die elementaren Gefährdungen des BSI als Referenz für klassische Security-/Resilienzrisiken und als Vollständigkeits-/Deep-Dive-Bestand. BSI 200-3 ist damit eine wichtige Anschlussstelle, aber nicht die zwingende Primärmethode jedes Souveränitätsassessments.

Zusätzlich verwendet der Radar souveränitätsspezifische Risikotypen. Diese sind **interne Methodenentwicklungen und keine BSI-Gefährdungsnummern**.

Aktuelle zusätzliche Risikofamilien:

- `G z.S1` jurisdiktionelle / extraterritoriale Exposition
- `G z.S2` Change of Control / Ownership Control
- `G z.S3` Verlust autonomer Fortführungs-/Exit-Fähigkeit
- `G z.S4` technischer Vendor-/Platform-Lock-in
- `G z.S5` Skill-/Operating-Autonomy-Abhängigkeit
- `G z.S6` kritische Supply-Chain-Abhängigkeit
- `G z.S7` Konzentrations-/Common-Cause-Risiko
- `G z.S8` Verlust effektiver kryptographischer Kontrolle
- `G z.S9` KI-/Modell-/Agenten-Lock-in
- `G z.S10` Abhängigkeit von Identity-/Trust Anchors
- `G z.S11` Verlust unabhängiger Evidence-/Observability-Fähigkeit
- `G z.S12` Souveränitäts-Drift

## Verhältnis zu den sieben Decision Dimensions

Die Risikofamilien werden nicht 1:1 als sichtbare Managementdimensionen ausgegeben. Sie speisen je nach Szenario eine oder mehrere der sieben v0.4-Entscheidungsdimensionen und bleiben als fachliche Detailspur erhalten.

Risiko-Taxonomie, Decision Dimensions und Hard Gates sind deshalb drei unterschiedliche Ebenen:

- **Risk Taxonomy:** Welche Gefährdung/Exposition/Szenarien bestehen?
- **Decision Dimensions:** Wie wird der Variantenvergleich verständlich strukturiert?
- **Hard Gates:** Welche kundenspezifischen Mindestanforderungen sind nicht kompensierbar?

## C3A-Review-Gate

Der vollständige BSI-C3A-Kriterienkatalog wird in **NEXT-120 / Issue #68** gegen diese Taxonomie geprüft. Bis dahin wird nicht behauptet, dass `G z.S1–G z.S12` C3A vollständig abdecken oder direkt aus C3A abgeleitet sind.

C3A kann nach Volltextprüfung:

- bestehende Risikotypen fachlich stützen,
- zusätzliche Capability-/Evidence-Fragen nahelegen,
- eine bessere Zuordnung zu Provider Intelligence ermöglichen,
- oder Änderungen/Ergänzungen der Taxonomie erforderlich machen.

Direkte C3A-Begriffe und interne Risikotypen bleiben in jedem Fall getrennt gekennzeichnet.

Für Definitionen, Quellen und Herleitung gelten `data/method/risk_taxonomy.csv`, das Source Register sowie die akzeptierten Decisions. Das Methoden-Workbook ist Entwicklungsreferenz, aber keine gegenüber neueren akzeptierten Decisions höher priorisierte Source of Truth.
