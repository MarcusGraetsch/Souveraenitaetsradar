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
  • .build/ inklusive lokalem Build-CA-Bundle
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
rm -rf -- .runtime .build
rm -f -- .env

if [[ -e .runtime ]];then
  echo "✖ .runtime konnte nicht vollständig entfernt werden." >&2
  ls -ld .runtime >&2 || true
  find .runtime -maxdepth 3 -ls >&2 || true
  exit 1
fi
if [[ -e .build ]];then
  echo "✖ .build konnte nicht vollständig entfernt werden." >&2
  ls -ld .build >&2 || true
  find .build -maxdepth 2 -ls >&2 || true
  exit 1
fi
if [[ -e .env ]];then
  echo "✖ .env konnte nicht entfernt werden." >&2
  ls -l .env >&2 || true
  exit 1
fi

echo "✔ Anwendung und alle durch sie erzeugten Daten wurden entfernt."
echo
echo "Optionale Zusatzaktion: lokalen Git-Repository-Ordner löschen."
echo "Standard ist: Repository behalten."
REMOVE_REPO=""
read -rp "Zum Behalten Enter drücken. Zum Löschen exakt DELETE REPO eingeben: " REMOVE_REPO || true
if [[ "$REMOVE_REPO" != "DELETE REPO" ]];then
  echo "✔ Repository-Ordner bleibt erhalten."
  exit 0
fi

DIRTY=""
if command -v git >/dev/null 2>&1 && git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1;then
  DIRTY="$(git -C "$ROOT" status --porcelain --untracked-files=all || true)"
fi
if [[ -n "$DIRTY" ]];then
  echo
  echo "⚠ Im Repository existieren lokale, nicht eingecheckte oder nicht nachverfolgte Änderungen:" >&2
  printf '%s\n' "$DIRTY" >&2
  echo "Diese Änderungen würden beim Löschen verloren gehen." >&2
  CONFIRM_DIRTY=""
  read -rp "Zum endgültigen Löschen trotz lokaler Änderungen exakt DELETE REPO WITH CHANGES eingeben: " CONFIRM_DIRTY || true
  if [[ "$CONFIRM_DIRTY" != "DELETE REPO WITH CHANGES" ]];then
    echo "✔ Repository-Ordner bleibt erhalten."
    exit 0
  fi
fi

PARENT="$(dirname "$ROOT")"
NAME="$(basename "$ROOT")"
cd "$PARENT"
rm -rf -- "$NAME"
echo "✔ Repository-Ordner gelöscht."
exit 0
