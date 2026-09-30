#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PRESENTATION_PORT="${PRESENTATION_PORT:-8765}"
URL="http://127.0.0.1:${PRESENTATION_PORT}/presentacion-vigente.html"

cd "$SCRIPT_DIR"

if command -v xdg-open >/dev/null 2>&1; then
  (sleep 0.8; xdg-open "$URL" >/dev/null 2>&1 || true) &
elif command -v google-chrome >/dev/null 2>&1; then
  (sleep 0.8; google-chrome "$URL" >/dev/null 2>&1 || true) &
fi

echo "Win2APK: $URL"
echo "Detener servidor: Ctrl+C"
python3 -m http.server "$PRESENTATION_PORT" --bind 127.0.0.1
