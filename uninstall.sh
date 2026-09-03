#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)";cd "$ROOT"
cat <<'WARN'

Souveränitäts-Radar – vollständige Deinstallation

Dieser Vorgang löscht unwiderruflich:
  • alle Assessments und Antworten in PostgreSQL
  • alle lokal hochgeladenen Evidence-Dateien
  • alle LLM-Bridge-Imports
  • .runtime/ inklusive Exporte/Temp-Daten
  • Docker-Container, Netzwerk, DB-Volume und lokal gebaute Images
  • die lokale .env

Git-Repository und Quellcode werden standardmäßig NICHT gelöscht.
WARN
read -rp "Tippe DELETE, um fortzufahren: " CONFIRM;[[ "$CONFIRM" == "DELETE" ]]||{ echo "Abgebrochen.";exit 0; }
docker compose down -v --remove-orphans --rmi local||true;rm -rf -- .runtime;rm -f -- .env;echo "✔ Anwendung und alle durch sie erzeugten Daten wurden entfernt."
read -rp "Auch den geklonten Repository-Ordner löschen? [j/N]: " REMOVE_REPO
if [[ "$REMOVE_REPO" =~ ^[jJyY]$ ]];then PARENT="$(dirname "$ROOT")";NAME="$(basename "$ROOT")";cd "$PARENT";rm -rf -- "$NAME";echo "✔ Repository-Ordner gelöscht.";fi
