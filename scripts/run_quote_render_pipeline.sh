#!/bin/sh
set -eu

if [ "$#" -ne 3 ]; then
  echo "Usage: sh scripts/run_quote_render_pipeline.sh <payload.json> <render_script.py> <output.png>" >&2
  exit 2
fi

PAYLOAD="$1"
RENDER_SCRIPT="$2"
OUT="$3"

python3 "$(dirname "$0")/validate_quote_payload.py" "$PAYLOAD"
python3 "$RENDER_SCRIPT" "$PAYLOAD" "$OUT"
echo "$OUT"
