#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

set -a
source .env
set +a
 


envsubst < prometheus/prometheus.yml.template > prometheus/prometheus.yml

SPAGHETTICHEF_BASE_URL="${SPAGHETTICHEF_BASE_URL:-http://localhost:18080}"
SPAGHETTICHEF_BASE_URL="${SPAGHETTICHEF_BASE_URL%/}"

echo "Checking SpaghettiChef at $SPAGHETTICHEF_BASE_URL..."

if curl -fsS "$SPAGHETTICHEF_BASE_URL/health" >/dev/null 2>&1; then
  echo "SpaghettiChef is reachable."
else
  echo "SpaghettiChef is not available at $SPAGHETTICHEF_BASE_URL."
  echo "BenchChef will start, but probes will fail until SpaghettiChef is running."
fi

cd "$ROOT_DIR"
docker compose up -d

cd "$ROOT_DIR/backend-django"
source .venv/bin/activate
nohup python manage.py runserver \
  0.0.0.0:"$BENCHCHEF_BACKEND_PORT" \
  > backend.log 2>&1 &

echo $! > /tmp/benchchef-backend.pid

cd "$ROOT_DIR/frontend-angular"
nohup ng serve \
  --host 0.0.0.0 \
  --port "$BENCHCHEF_FRONTEND_PORT" \
  > frontend.log 2>&1 &

echo $! > /tmp/benchchef-frontend.pid

echo "Waiting for BenchChef backend on port $BENCHCHEF_BACKEND_PORT..."

until curl -fsS "http://localhost:$BENCHCHEF_BACKEND_PORT/" >/dev/null 2>&1; do
  sleep 1
done

echo "BenchChef backend is reachable."

if [ "${BENCHCHEF_START_DIAGNOSTICS_LOOP:-false}" != "true" ]; then
  echo "Diagnostics loop disabled."
  echo "Use Angular at http://localhost:$BENCHCHEF_FRONTEND_PORT to launch probes."
  exit 0
fi

echo "Starting diagnostics loop for connection $BENCHCHEF_DIAGNOSTICS_CONNECTION_ID..."

while true; do
  curl -fsS -X POST "http://localhost:$BENCHCHEF_BACKEND_PORT/api/connections/$BENCHCHEF_DIAGNOSTICS_CONNECTION_ID/diagnostics/" >/dev/null || true
  sleep "${BENCHCHEF_DIAGNOSTICS_INTERVAL_SECONDS:-5}"
done
