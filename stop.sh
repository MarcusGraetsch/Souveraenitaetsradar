#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
docker compose stop
echo "Souveränitäts-Radar gestoppt. PostgreSQL-Volume und .runtime bleiben erhalten."
