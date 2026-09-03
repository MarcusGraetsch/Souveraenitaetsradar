# Security Policy

## Sensible Inhalte

Nicht in GitHub committen oder in Issues/PRs posten:

- AWS Access Keys, Tokens, Session Credentials
- Kundendaten/Fachdaten
- unredigierte Prompts/Outputs aus Kundenworkloads
- interne IAM-/Netzwerkdetails, sofern das Repository nicht der dafür freigegebene Ablageort ist
- C5-/SOC-Berichte aus Portalen mit eingeschränkten Nutzungsbedingungen, sofern keine Freigabe zur Ablage besteht

## Evidence Collector

Der R6 Collector ist absichtlich read-only und konfigurationsorientiert. Änderungen daran, die `Create`, `Update`, `Delete`, `Put`, `Invoke`, Payload- oder Log-Event-Zugriffe einführen, gelten als Security-sensitive und benötigen Architektur- und Security-Review.

## Meldung

Security-relevante Probleme nicht mit sensitiven Details in einem öffentlichen Issue beschreiben. Bei privatem Repository dennoch minimale notwendige Informationen verwenden.
