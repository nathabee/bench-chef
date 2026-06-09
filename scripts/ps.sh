#!/usr/bin/env bash

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

set -a
source .env
set +a

echo
echo "=== SpaghettiChef ==="
SPAGHETTICHEF_BASE_URL="${SPAGHETTICHEF_BASE_URL:-http://localhost:18080}"
SPAGHETTICHEF_BASE_URL="${SPAGHETTICHEF_BASE_URL%/}"
if curl -fsS "$SPAGHETTICHEF_BASE_URL/health" >/dev/null 2>&1; then
  echo "Reachable at $SPAGHETTICHEF_BASE_URL"
else
  echo "Not reachable at $SPAGHETTICHEF_BASE_URL"
fi

echo
echo "=== BenchChef Django ==="
ps -ef | grep -v grep | grep "manage.py runserver" || echo "Not running"

echo
echo "=== BenchChef Angular ==="
ps -ef | grep -v grep | grep -E "ng serve|http.server ${BENCHCHEF_FRONTEND_PORT}" || echo "Not running"

echo
echo "=== Listening Ports ==="
ss -ltnp | grep -E ":${BENCHCHEF_BACKEND_PORT}|:${BENCHCHEF_FRONTEND_PORT}|:${PROMETHEUS_PORT}|:${GRAFANA_PORT}|:${NODE_EXPORTER_PORT}|:${PROCESS_EXPORTER_PORT}" || echo "No matching ports"

echo
echo "=== Docker Containers ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
