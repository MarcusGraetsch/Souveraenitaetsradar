#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="$ROOT/.build"
OUT="$BUILD_DIR/ca-bundle.crt"
mkdir -p "$BUILD_DIR"
chmod 700 "$BUILD_DIR" 2>/dev/null || true
: > "$OUT"

SYSTEM_CA=""
for candidate in \
  /etc/ssl/certs/ca-certificates.crt \
  /etc/pki/tls/certs/ca-bundle.crt \
  /etc/ssl/ca-bundle.pem; do
  if [[ -r "$candidate" && -s "$candidate" ]]; then
    SYSTEM_CA="$candidate"
    break
  fi
done

if [[ -n "$SYSTEM_CA" ]]; then
  cat "$SYSTEM_CA" >> "$OUT"
fi

if [[ -n "${SOVRADAR_CA_CERT:-}" ]]; then
  [[ -r "$SOVRADAR_CA_CERT" ]] || {
    echo "Custom CA-Datei nicht lesbar: $SOVRADAR_CA_CERT" >&2
    exit 2
  }
  printf '\n' >> "$OUT"
  cat "$SOVRADAR_CA_CERT" >> "$OUT"
fi

chmod 600 "$OUT"
printf '%s\n' "$OUT"
