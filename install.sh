#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; cd "$ROOT"
bold='\033[1m';green='\033[32m';yellow='\033[33m';red='\033[31m';cyan='\033[36m';reset='\033[0m'
ok(){ echo -e "${green}✔${reset} $*"; };warn(){ echo -e "${yellow}⚠${reset} $*"; };fail(){ echo -e "${red}✖${reset} $*" >&2; exit 1; }
echo;echo "  Souveränitäts-Radar · MVP-01";echo "  Consultant Web Application";echo
command -v docker >/dev/null 2>&1||fail "Docker wurde nicht gefunden. Bitte Docker Engine/Desktop installieren.";docker compose version >/dev/null 2>&1||fail "Docker Compose v2 wurde nicht gefunden.";command -v curl >/dev/null 2>&1||fail "curl wird für den Healthcheck benötigt.";command -v python3 >/dev/null 2>&1||fail "python3 wird für den Healthcheck benötigt."
ok "Docker: $(docker --version)";ok "Compose: $(docker compose version --short)"
read -rp "Port [8080]: " APP_PORT;APP_PORT="${APP_PORT:-8080}";[[ "$APP_PORT" =~ ^[0-9]+$ ]]||fail "Ungültiger Port"
printf "Nur lokal erreichbar (empfohlen) oder im Netzwerk?\n  [1] 127.0.0.1\n  [2] 0.0.0.0\n";read -rp "Auswahl [1]: " BIND_CHOICE
if [[ "${BIND_CHOICE:-1}" == "2" ]];then BIND_HOST="0.0.0.0";warn "MVP-01 hat noch keine Authentisierung. Netzwerkfreigabe nur im vertrauenswürdigen Testnetz.";else BIND_HOST="127.0.0.1";fi
if command -v openssl >/dev/null 2>&1;then DB_PASSWORD="$(openssl rand -hex 24)";else DB_PASSWORD="$(python3 -c 'import secrets;print(secrets.token_hex(24))')";fi
cat >.env <<EOF
APP_PORT=$APP_PORT
BIND_HOST=$BIND_HOST
POSTGRES_PASSWORD=$DB_PASSWORD
SOVRADAR_MAX_UPLOAD_BYTES=52428800
EOF
chmod 600 .env;mkdir -p .runtime/documents .runtime/exports .runtime/temp;chmod 700 .runtime||true;ok "Lokale Runtime vorbereitet"
echo -e "${cyan}→${reset} Baue Images …";docker compose build
echo -e "${cyan}→${reset} Starte PostgreSQL, API und Web …";docker compose up -d
export APP_PORT BIND_HOST
if ./test.sh;then echo;ok "Souveränitäts-Radar ist bereit: http://localhost:${APP_PORT}";else docker compose ps;fail "Healthcheck fehlgeschlagen. Prüfe docker compose logs";fi
echo;echo "Befehle: ./start.sh | ./stop.sh | ./test.sh | ./uninstall.sh";echo "MVP-01 sendet keine Daten an LLM-APIs. LLM Bridge = Copy/Paste."
