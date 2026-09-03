#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
[[ -f .env ]]||{ echo "Keine .env gefunden. Zuerst ./install.sh ausführen." >&2;exit 1; }
docker compose up -d
source .env
./test.sh
echo "Souveränitäts-Radar: http://localhost:${APP_PORT:-8080}"
