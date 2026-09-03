# Security Policy

## Grundsatz

Der Souveränitätsradar verlangt im Standardprozess **keine Cloud-Credentials, Root-, Owner- oder Subscription-Admin-Zugänge** von Kunden.

## Nicht in GitHub committen

- Passwörter, API Keys, Access Tokens, Session Credentials
- Kundendaten/Fachdaten
- unredigierte Architektur-, IAM-, Netzwerk- oder Vertragsdokumente
- Cloud-Account-/Tenant-/Subscription-spezifische Raw Exporte, sofern nicht explizit als synthetische Fixture freigegeben
- eingeschränkt nutzbare Assurance-Berichte (z. B. aus geschützten Portalen), sofern keine Ablagefreigabe besteht

## Evidence Packs

Evidence Packs werden standardmäßig außerhalb des Repositories verarbeitet. Nur:

- Templates
- Schemas
- synthetische Fixtures
- redigierte Beispiele

sind für Git vorgesehen.

## Provider-spezifische Parser

Parser müssen dateibasiert und credential-frei sein. Ein zukünftiger kundenseitig ausgeführter Exporter kann separat entwickelt werden, darf aber nie Voraussetzung der Methode werden und benötigt eigenes Security Review.

## Meldung

Security-Probleme mit minimal notwendigen Details melden. Secrets sofort rotieren; nicht in Issues kopieren.
