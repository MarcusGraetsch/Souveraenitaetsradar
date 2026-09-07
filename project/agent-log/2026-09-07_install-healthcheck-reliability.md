# Install- und Healthcheck-Zuverlässigkeit (2026-09-07)

## Planungsprotokoll

- **Ziel / Problem:** Einen reproduzierbaren API-Restart nach erneutem `install.sh` verhindern und einen fehlschlagenden Container im Healthcheck ohne irreführende Wartezeit diagnostizierbar machen.
- **Scope:** Lokaler Compose-Installationsablauf, API-Healthcheck und Regressionstests für diese Shell-Abläufe.
- **Nicht-Scope:** Änderungen an Methodik, fachlichen Regeln, Datenmodell, Datenbankmigrationen oder Cloud-/Provider-Adaptern.
- **Rolle:** `developer`; abschließende Prüfung als gekennzeichneter Self-Review, da keine Delegation beauftragt ist.
- **Betroffene Dateien:** `install.sh`, `test.sh`, Shell-Regressionstests sowie diese Session-Notiz; Betriebsdokumentation nur falls das Verhalten erklärungsbedürftig bleibt.
- **Quellen / Provenienz:** Repository-Beobachtung und reproduzierbares Compose-Verhalten; keine neue fachliche Regel und keine externe/regulatorische Quelle erforderlich (`evidence-observation`).
- **Daten- / Security-Risiko:** Das bestehende Datenbankpasswort darf bei einer Wiederholung der Installation nicht ausgegeben oder ersetzt werden. Ein fremdes bestehendes Compose-Volume darf nicht automatisch gelöscht werden. Logs können lokale Diagnosedaten enthalten und werden nur im Terminal ausgegeben.
- **Akzeptanzkriterien:** Wiederholte Installation bewahrt das vorhandene Datenbankpasswort; ein verwaistes/anderweitig vorhandenes Projekt-Volume ohne lokale Konfiguration führt vor dem Start zu einer handlungsorientierten Meldung; `test.sh` erkennt einen dauerhaft neu startenden oder beendeten API-Container früh und zeigt dessen Logs; der Erfolgsfall bleibt unverändert.
- **Tests / Reviewklasse:** Shell-Syntax, isolierte Regressionstests mit simuliertem Docker/curl, bestehende Python-/Repository-Validatoren; Reviewklasse A für Betriebs-Shellcode, Self-Review dokumentiert.

## Befund

- **Observation:** `install.sh` erzeugt bei jedem Lauf ein neues `POSTGRES_PASSWORD`, während das benannte Compose-Volume erhalten bleibt. PostgreSQL übernimmt das Passwort nur bei der ersten Volume-Initialisierung. Danach kann die API mit dem neu geschriebenen Passwort nicht mehr verbinden und wird durch `restart: unless-stopped` wiederholt gestartet.
- **Observation:** `test.sh` wartet unabhängig vom Containerzustand bis zu 40 Sekunden und unterdrückt die HTTP-Fehlerausgabe. Die entscheidenden API-Logs werden erst durch einen zusätzlichen manuellen Befehl sichtbar.
- **Inference:** Das vom Nutzer berichtete Muster (gesunde Datenbank, API in `Restarting`, Healthcheck-Timeout) ist mit diesem Passwort-/Volume-Lifecycle konsistent. Die Containerlogs bleiben für die Bestätigung des konkreten Zielsystems maßgeblich.

## Review

- **Erledigt:** Das vorhandene Passwort wird vor dem Neuschreiben der `.env` übernommen. Ein bekanntes Compose-Volume ohne zugehörige lokale Konfiguration wird nicht gelöscht oder mit einem neuen Secret gestartet.
- **Erledigt:** Der Healthcheck prüft während des Pollings den tatsächlichen API-Containerzustand und gibt bei `restarting`, `exited`, `dead` oder Timeout Status und begrenzte API-Logs aus.
- **Erledigt:** Isolierte Shell-Regressionen decken erfolgreiche Wiederholungsinstallation, verwaistes Volume und frühe Restart-Diagnose ab.
- **Self-Review:** Keine fachliche Regel, Schwelle, Providerlogik oder Evidence-Semantik wurde verändert. Secret-Werte werden weder protokolliert noch in Git geschrieben. Der Fix löscht keine Laufzeitdaten automatisch.
- **Open:** Auf dem gemeldeten Zielsystem sollten die nun sichtbaren Containerlogs bestätigen, ob tatsächlich eine PostgreSQL-Passwortabweichung vorlag; andere Startup-Fehler werden durch denselben Diagnosepfad ebenfalls direkt sichtbar.
