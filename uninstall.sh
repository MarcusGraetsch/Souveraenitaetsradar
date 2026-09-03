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
# Evidence-Dateien werden vom API-Container erzeugt und können auf Linux dem
# Container-Root gehören. Lösche Runtime-Inhalte deshalb vor `compose down`
# einmal innerhalb des API-Images; anschließend kann der Host den leeren
# Mountpoint zuverlässig entfernen. Fehler hier werden nicht verschluckt,
# wenn danach die Host-Löschung ebenfalls scheitert.
if [[ -d .runtime ]];then
  docker compose run --rm --no-deps api sh -c 'rm -rf /app/.runtime/* /app/.runtime/.[!.]* /app/.runtime/..?*' || true
fi
docker compose down -v --remove-orphans --rmi local||true
rm -rf -- .runtime
rm -f -- .env
echo "✔ Anwendung und alle durch sie erzeugten Daten wurden entfernt."
read -rp "Auch den geklonten Repository-Ordner löschen? [j/N]: " REMOVE_REPO
if [[ "$REMOVE_REPO" =~ ^[jJyY]$ ]];then PARENT="$(dirname "$ROOT")";NAME="$(basename "$ROOT")";cd "$PARENT";rm -rf -- "$NAME";echo "✔ Repository-Ordner gelöscht.";fi
