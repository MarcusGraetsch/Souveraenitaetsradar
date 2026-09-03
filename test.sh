#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
[[ -f .env ]]&&source .env
APP_PORT="${APP_PORT:-8080}";BASE="http://127.0.0.1:${APP_PORT}"
for i in $(seq 1 40);do if curl -fsS "$BASE/api/health" >/tmp/sovradar-health.json 2>/dev/null;then break;fi;sleep 1;if [[ "$i" == "40" ]];then echo "API Healthcheck timeout" >&2;exit 1;fi;done
curl -fsS "$BASE/" >/dev/null
python3 - <<'PY'
import json
with open('/tmp/sovradar-health.json',encoding='utf-8') as f:x=json.load(f)
assert x['status']=='ok',x
assert x['method_questions']>=100,x
print(f"✔ API healthy · {x['method_questions']} Methodenfragen geladen")
PY
echo "✔ Web erreichbar";docker compose ps --status running >/dev/null;echo "✔ Docker-Services laufen"
