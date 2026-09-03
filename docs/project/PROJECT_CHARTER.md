# Project Charter

## Problem

Cloud- und KI-Souveränität wird häufig entweder rein regulatorisch, rein technisch oder über vereinfachte Providerlabels bewertet. Dadurch verschwinden Zielkonflikte zwischen Sicherheit, Autonomie, Portabilität, Jurisdiktion, Betriebsfähigkeit und Evidenzqualität.

## Ziel

Eine beratungstaugliche und technisch operationalisierbare Methode entwickeln, die:

- workload-spezifisch und cloud-agnostisch arbeitet,
- Informationssicherheit und Souveränität trennt,
- externe Abhängigkeiten transparent macht,
- Exit-/Autonomie-/Konzentrationsrisiken abbildet,
- Quellen und Evidenz nachvollziehbar nachweist,
- keine Cloud-Credentials oder Root-/Owner-Zugänge als Voraussetzung benötigt,
- KI für Extraktion, Planung und Erklärung nutzt, aber Entscheidungen nicht halluciniert.

## Evidence-Grundsatz

Standard ist Customer-mediated Evidence: Verträge, Dokumente, redigierte Konfig-/IaC-/CMDB-Exporte, vom Kunden erzeugte Provider-Exporte, Assurance, Screenshare-Beobachtungen und Testberichte. Provider-spezifische Adapter sind nur Übersetzungsschichten.

## Nicht-Ziele der aktuellen Phase

- Zertifizierungsschema ersetzen
- Rechtsberatung automatisieren
- offizielle EU-SEAL-/C5-Ergebnisse ohne vollständige Anwendung der jeweiligen Verfahren behaupten
- Provider pauschal ranken
- Kundenaccounts automatisiert scannen

## Erfolgsindikatoren

- zwei Berater kommen mit derselben Evidence zu vergleichbaren Ergebnissen
- jede wesentliche Aussage kann auf Quelle/Evidence/Ableitung zurückgeführt werden
- fehlende Information ist explizit
- Tool kann Szenarien mit gegenläufigen Security-/Sovereignty-Profilen korrekt darstellen
- Regeln sind unit-testbar und versioniert
- mindestens zwei Hyperscaler und ein nicht-hyperscaler Szenario nutzen denselben Methodenkern
