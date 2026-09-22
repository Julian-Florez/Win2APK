#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

for required in \
  index.html styles.css presentation.js \
  assets/logo/win2apk-symbol.svg \
  assets/logo/win2apk-logo.svg \
  assets/video/demo-redmi-bomb-rush-18s.mp4 \
  docs/guion.md docs/preguntas-y-respuestas.md docs/fuentes.md \
  docs/auditoria-proyecto.md docs/estructura-presentacion.md \
  docs/revision-rubrica.md; do
  test -s "$required" || { echo "Falta o está vacío: $required" >&2; exit 1; }
done

if rg -n '(src|href)="https?://|//cdn|fonts\.googleapis' index.html styles.css presentation.js; then
  echo "Se encontraron referencias de red en los archivos de ejecución." >&2
  exit 1
fi

for asset in $(rg -o 'assets/[A-Za-z0-9_./-]+' index.html | sort -u); do
  test -f "$asset" || { echo "Asset inexistente: $asset" >&2; exit 1; }
done

SLIDES=$(rg -c '<section class="slide' index.html)
BACKUP=$(rg -c 'slide-no">B[0-9]+' index.html)
MAIN=$((SLIDES - BACKUP))

test "$MAIN" -eq 12 || { echo "Se esperaban 12 diapositivas principales; hay $MAIN" >&2; exit 1; }
test "$BACKUP" -eq 9 || { echo "Se esperaban 9 diapositivas de respaldo; hay $BACKUP" >&2; exit 1; }
test "$SLIDES" -eq 21 || { echo "Se esperaban 21 diapositivas; hay $SLIDES" >&2; exit 1; }

ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 \
  assets/video/demo-redmi-bomb-rush-18s.mp4 | rg '^18(\.0+)?$' >/dev/null

echo "Verificación estática superada: $MAIN principales, $BACKUP backup, video 18 s."
