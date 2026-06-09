#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

set -a
source .env
set +a

CONNECTION_ID="${1:-${BENCHCHEF_DIAGNOSTICS_CONNECTION_ID:-1}}"

curl -fsS \
  -X POST \
  "http://localhost:${BENCHCHEF_BACKEND_PORT}/api/connections/${CONNECTION_ID}/diagnostics-history/" \
  -H 'Content-Type: application/json' \
  -d '{
    "repeat_count": 5,
    "delay_ms": 500
  }'
