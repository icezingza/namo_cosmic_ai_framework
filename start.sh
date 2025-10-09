#!/usr/bin/env bash
set -euo pipefail

RUNTIME="${APP_RUNTIME:-python}"
MODULE="${APP_MODULE:-main:app}"

case "$RUNTIME" in
  python|uvicorn)
    exec uvicorn "$MODULE"
    ;;
  *)
    echo "Unsupported APP_RUNTIME: $RUNTIME" >&2
    exit 1
    ;;
esac
