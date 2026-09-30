#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PDF_PORT="${PDF_PORT:-8766}"
PDF_URL="http://127.0.0.1:${PDF_PORT}/presentacion-vigente.html?print=1"
OUTPUT="$ROOT_DIR/presentacion-vigente.pdf"

if command -v google-chrome >/dev/null 2>&1; then
  BROWSER="$(command -v google-chrome)"
elif command -v chromium >/dev/null 2>&1; then
  BROWSER="$(command -v chromium)"
else
  echo "No se encontró Google Chrome ni Chromium." >&2
  exit 1
fi

cd "$ROOT_DIR"
python3 -m http.server "$PDF_PORT" --bind 127.0.0.1 >/tmp/win2apk-pdf-server.log 2>&1 &
SERVER_PID=$!
trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT

for _ in 1 2 3 4 5; do
  if curl -fsS "$PDF_URL" >/dev/null; then
    break
  fi
  sleep 0.2
done

"$BROWSER" \
  --headless=new \
  --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="$OUTPUT" \
  "$PDF_URL"

echo "$OUTPUT"
