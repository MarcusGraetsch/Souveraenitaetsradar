# NEXT-118 – Runtime-Permission-Fund

Datum: 2026-09-09

## Kontext

Beim ersten manuellen Product-Owner-/Test-Consultant-Durchlauf auf einer VMware-Linux-VM wurde nach Bereinigung eines verwaisten PostgreSQL-Volumes die Installation erneut gestartet.

Der Installer kam bis zur lokalen Runtime-Vorbereitung und brach dann ab:

```text
mkdir: cannot create directory ‘.runtime/exports’: Permission denied
mkdir: cannot create directory ‘.runtime/temp’: Permission denied
```

## Einordnung

- Typ: Produkt-/Installer-Fund
- Phase: NEXT-118
- Schwere: UX/Operational; blockiert Installation auf dem betroffenen Host
- Human Gate: keines für die technische Fehlerbehebung

## Vermutung / zu verifizieren

Das lokale `.runtime`-Verzeichnis oder Unterverzeichnisse stammen aus einer früheren containerisierten Ausführung und sind nicht durch den aktuellen Host-Benutzer beschreibbar. Die API läuft derzeit im Container als root und bind-mountet `./.runtime` nach `/app/.runtime`, wodurch hostseitige Eigentümer-/Rechteprobleme entstehen können.

## Erwartete Produktreaktion

Der Installer soll vor `mkdir -p .runtime/...` explizit prüfen, ob ein vorhandenes `.runtime` durch den aktuellen Benutzer beschreibbar ist, und in diesem Fall einen sicheren, verständlichen Recovery-Hinweis ausgeben. Er darf bestehende Evidence-/Exportdaten nicht automatisch löschen oder umchownen.

Langfristig sollte zusätzlich geprüft werden, ob der API-Container mit einem nicht-root Benutzer bzw. hostkompatiblen UID/GID-Modell betrieben werden sollte.
