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

# Die API schreibt in einen Bind-Mount. Auf Linux können dadurch Runtime-Dateien
# und Unterverzeichnisse dem Container-Root gehören. Vor dem Entfernen der
# Container werden daher alle Inhalte innerhalb des Containers gelöscht und der
# Mountpoint für die abschließende Host-Löschung wieder beschreibbar gemacht.
# -T und </dev/null verhindern, dass docker compose die restliche stdin des
# interaktiven Uninstall-Dialogs konsumiert.
if [[ -d .runtime ]];then
  docker compose run -T --rm --no-deps api sh -c '
    find /app/.runtime -mindepth 1 -depth -delete 2>/dev/null || true
    chmod 0777 /app/.runtime 2>/dev/null || true
  ' </dev/null || true
fi

docker compose down -v --remove-orphans --rmi local||true
rm -rf -- .runtime
rm -f -- .env

if [[ -e .runtime ]];then
  echo "✖ .runtime konnte nicht vollständig entfernt werden." >&2
  ls -ld .runtime >&2 || true
  find .runtime -maxdepth 3 -ls >&2 || true
  exit 1
fi
if [[ -e .env ]];then
  echo "✖ .env konnte nicht entfernt werden." >&2
  ls -l .env >&2 || true
  exit 1
fi

echo "✔ Anwendung und alle durch sie erzeugten Daten wurden entfernt."
REMOVE_REPO=""
read -rp "Auch den geklonten Repository-Ordner löschen? [j/N]: " REMOVE_REPO || true
if [[ "$REMOVE_REPO" =~ ^[jJyY]$ ]];then PARENT="$(dirname "$ROOT")";NAME="$(basename "$ROOT")";cd "$PARENT";rm -rf -- "$NAME";echo "✔ Repository-Ordner gelöscht.";fi
exit 0
