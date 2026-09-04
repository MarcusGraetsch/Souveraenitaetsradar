#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; cd "$ROOT"
bold='\033[1m';green='\033[32m';yellow='\033[33m';red='\033[31m';cyan='\033[36m';reset='\033[0m'
ok(){ echo -e "${green}✔${reset} $*"; };warn(){ echo -e "${yellow}⚠${reset} $*"; };fail(){ echo -e "${red}✖${reset} $*" >&2; exit 1; }

echo;echo "  Souveränitäts-Radar · MVP-01";echo "  Consultant Web Application";echo
command -v docker >/dev/null 2>&1||fail "Docker wurde nicht gefunden. Bitte Docker Engine/Desktop installieren."
docker compose version >/dev/null 2>&1||fail "Docker Compose v2 wurde nicht gefunden."
command -v curl >/dev/null 2>&1||fail "curl wird für den Healthcheck benötigt."
command -v python3 >/dev/null 2>&1||fail "python3 wird für den Healthcheck benötigt."
ok "Docker: $(docker --version)";ok "Compose: $(docker compose version --short)"

read -rp "Port [8080]: " APP_PORT;APP_PORT="${APP_PORT:-8080}";[[ "$APP_PORT" =~ ^[0-9]+$ ]]||fail "Ungültiger Port"
printf "Nur lokal erreichbar (empfohlen) oder im Netzwerk?\n  [1] 127.0.0.1\n  [2] 0.0.0.0\n";read -rp "Auswahl [1]: " BIND_CHOICE
if [[ "${BIND_CHOICE:-1}" == "2" ]];then BIND_HOST="0.0.0.0";warn "MVP-01 hat noch keine Authentisierung. Netzwerkfreigabe nur im vertrauenswürdigen Testnetz.";else BIND_HOST="127.0.0.1";fi

# Docker build containers do not automatically inherit enterprise/custom trust
# anchors from the host. Build a local CA bundle and pass it later as a BuildKit
# secret. TLS verification remains enabled for pip and npm.
BUILD_CA_BUNDLE="$(bash "$ROOT/scripts/prepare-build-ca.sh")"
export SOVRADAR_BUILD_CA_BUNDLE="$BUILD_CA_BUNDLE"

check_tls_endpoint(){
  local label="$1" url="$2"
  local curl_args=(-fsS -o /dev/null --connect-timeout 10 --max-time 30)
  if [[ -s "$BUILD_CA_BUNDLE" ]];then curl_args+=(--cacert "$BUILD_CA_BUNDLE");fi
  if curl "${curl_args[@]}" "$url";then
    ok "TLS-Vertrauen: $label"
    return 0
  fi
  echo >&2
  echo "TLS-Vertrauensprüfung für $label fehlgeschlagen: $url" >&2
  if [[ -z "${SOVRADAR_CA_CERT:-}" ]];then
    cat >&2 <<'EOF'
Wenn die Umgebung TLS-Inspection / einen Enterprise-Proxy verwendet, muss
seine Root-/Intermediate-CA als PEM auf dem Host vertrauenswürdig vorliegen.
Alternativ kann sie nur für den Souveränitäts-Radar-Build angegeben werden:

  SOVRADAR_CA_CERT=/pfad/zur/enterprise-ca.pem ./install.sh

TLS-Verifikation wird absichtlich NICHT mit --trusted-host oder ähnlichen
unsicheren Optionen deaktiviert.
EOF
  else
    echo "Die mit SOVRADAR_CA_CERT angegebene CA stellt für diesen Endpunkt noch keine vollständige Vertrauenskette her: $SOVRADAR_CA_CERT" >&2
  fi
  fail "Abbruch vor dem Docker-Build: TLS-Trust zuerst korrigieren."
}

check_tls_endpoint "PyPI" "https://pypi.org/simple/setuptools/"
check_tls_endpoint "npm Registry" "https://registry.npmjs.org/"

if [[ -n "${SOVRADAR_CA_CERT:-}" ]];then
  ok "Custom CA für den Build eingebunden: $SOVRADAR_CA_CERT"
else
  ok "Host-CA-Bundle für den Docker-Build vorbereitet"
fi

if command -v openssl >/dev/null 2>&1;then DB_PASSWORD="$(openssl rand -hex 24)";else DB_PASSWORD="$(python3 -c 'import secrets;print(secrets.token_hex(24))')";fi
cat >.env <<EOF
APP_PORT=$APP_PORT
BIND_HOST=$BIND_HOST
POSTGRES_PASSWORD=$DB_PASSWORD
SOVRADAR_MAX_UPLOAD_BYTES=52428800
EOF
chmod 600 .env
mkdir -p .runtime/documents .runtime/exports .runtime/temp
chmod 700 .runtime||true
ok "Lokale Runtime vorbereitet"

echo -e "${cyan}→${reset} Baue Images …"
docker compose build
echo -e "${cyan}→${reset} Starte PostgreSQL, API und Web …"
docker compose up -d
export APP_PORT BIND_HOST
if ./test.sh;then
  echo;ok "Souveränitäts-Radar ist bereit: http://localhost:${APP_PORT}"
else
  docker compose ps
  fail "Healthcheck fehlgeschlagen. Prüfe docker compose logs"
fi

echo
echo "Befehle: ./start.sh | ./stop.sh | ./test.sh | ./uninstall.sh"
echo "MVP-01 sendet keine Daten an LLM-APIs. LLM Bridge = Copy/Paste."
