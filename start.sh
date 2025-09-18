#!/bin/bash
set -euo pipefail

PORT="${PORT:-8080}"
RUNTIME="${APP_RUNTIME:-python}"

case "$RUNTIME" in
  python)
    exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
    ;;
  *)
    echo "Unsupported APP_RUNTIME: $RUNTIME" >&2
    exit 1
    ;;
esac
