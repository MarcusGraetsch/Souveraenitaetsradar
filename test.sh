#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
[[ -f .env ]]&&source .env
APP_PORT="${APP_PORT:-8080}";BASE="http://127.0.0.1:${APP_PORT}"
api_diagnostics(){
  echo "--- API container status ---" >&2
  docker compose ps api >&2 || true
  echo "--- API logs (last 80 lines) ---" >&2
  docker compose logs --no-color --tail=80 api >&2 || true
}

for i in $(seq 1 40);do
  if curl -fsS "$BASE/api/health" >/tmp/sovradar-health.json 2>/dev/null;then
    break
  fi

  api_container="$(docker compose ps --all -q api 2>/dev/null || true)"
  if [[ -n "$api_container" ]];then
    api_state="$(docker inspect --format '{{.State.Status}}' "$api_container" 2>/dev/null || true)"
    case "$api_state" in
      restarting|exited|dead)
        echo "API-Container ist im Zustand '$api_state'; der Healthcheck wird frühzeitig beendet." >&2
        api_diagnostics
        exit 1
        ;;
    esac
  fi

  if [[ "$i" == "40" ]];then
    echo "API Healthcheck timeout nach 40 Sekunden ($BASE/api/health)" >&2
    api_diagnostics
    exit 1
  fi
  sleep 1
done
curl -fsS "$BASE/" >/dev/null
python3 - <<'PY'
import json
with open('/tmp/sovradar-health.json',encoding='utf-8') as f:x=json.load(f)
assert x['status']=='ok',x
assert x['method_questions']>=100,x
print(f"✔ API healthy · {x['method_questions']} Methodenfragen geladen")
PY
echo "✔ Web erreichbar";docker compose ps --status running >/dev/null;echo "✔ Docker-Services laufen"
