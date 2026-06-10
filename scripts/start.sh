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
BENCHCHEF_BACKEND_URL="http://localhost:$BENCHCHEF_BACKEND_PORT"
BENCHCHEF_FRONTEND_URL="http://localhost:$BENCHCHEF_FRONTEND_PORT"
PROMETHEUS_URL="http://localhost:$PROMETHEUS_PORT"
GRAFANA_URL="http://localhost:$GRAFANA_PORT"

write_frontend_config() {
  local config_file="$1"

  cat > "$config_file" <<EOF
window.BenchChefConfig = {
  backendUrl: '$BENCHCHEF_BACKEND_URL',
  frontendUrl: '$BENCHCHEF_FRONTEND_URL',
  prometheusUrl: '$PROMETHEUS_URL',
  grafanaUrl: '$GRAFANA_URL',
  spaghettiChefUrl: '$SPAGHETTICHEF_BASE_URL',
};
EOF
}

write_compose_env() {
  local config_file="$1"

  cat > "$config_file" <<EOF
PROMETHEUS_PORT=$PROMETHEUS_PORT
GRAFANA_PORT=$GRAFANA_PORT
NODE_EXPORTER_PORT=$NODE_EXPORTER_PORT
PROCESS_EXPORTER_PORT=$PROCESS_EXPORTER_PORT
EOF
}

stop_pid_file() {
  local label="$1"
  local pid_file="$2"

  if [ -f "$pid_file" ]; then
    local pid
    pid="$(cat "$pid_file")"
    if [ -n "$pid" ] && ps -p "$pid" >/dev/null 2>&1; then
      echo "Stopping existing $label process with PID $pid..."
      kill "$pid" >/dev/null 2>&1 || true
      sleep 1
      if ps -p "$pid" >/dev/null 2>&1; then
        kill -9 "$pid" >/dev/null 2>&1 || true
      fi
    fi
    rm -f "$pid_file"
  fi
}

stop_pid_file "BenchChef frontend" /tmp/benchchef-frontend.pid
stop_pid_file "BenchChef backend" /tmp/benchchef-backend.pid

echo "Checking SpaghettiChef at $SPAGHETTICHEF_BASE_URL..."

if curl -fsS "$SPAGHETTICHEF_BASE_URL/health" >/dev/null 2>&1; then
  echo "SpaghettiChef is reachable."
else
  echo "SpaghettiChef is not available at $SPAGHETTICHEF_BASE_URL."
  echo "BenchChef will start, but probes will fail until SpaghettiChef is running."
fi

cd "$ROOT_DIR"
write_compose_env "$ROOT_DIR/.compose.env"
docker compose --env-file "$ROOT_DIR/.compose.env" up -d

cd "$ROOT_DIR/backend-django"
if [ ! -d .venv ]; then
  echo "Creating BenchChef backend Python virtual environment..."
  python3 -m venv .venv
fi

source .venv/bin/activate

if [ ! -f .venv/.benchchef-requirements-installed ]; then
  echo "Installing BenchChef backend Python dependencies..."
  pip install --upgrade pip
  pip install -r requirements.txt
  touch .venv/.benchchef-requirements-installed
fi

echo "Applying BenchChef database migrations..."
python manage.py migrate --noinput

echo "Initializing default SpaghettiChef connection profile..."
python manage.py init_default_connection

nohup python manage.py runserver \
  0.0.0.0:"$BENCHCHEF_BACKEND_PORT" \
  > backend.log 2>&1 &

echo $! > /tmp/benchchef-backend.pid

FRONTEND_SOURCE_DIR="$ROOT_DIR/frontend-angular"
FRONTEND_DIST_DIR="$ROOT_DIR/dist/frontend-angular/browser"
FRONTEND_DEV_DIST_DIR="$ROOT_DIR/frontend-angular/dist/frontend-angular/browser"

if [ -f "$FRONTEND_SOURCE_DIR/package.json" ]; then
  write_frontend_config "$FRONTEND_SOURCE_DIR/public/benchchef-config.js"
  cd "$FRONTEND_SOURCE_DIR"
  if [ ! -d node_modules ]; then
    echo "Installing BenchChef frontend Node dependencies..."
    npm install
  fi

  nohup npx ng serve \
    --host 0.0.0.0 \
    --port "$BENCHCHEF_FRONTEND_PORT" \
    > frontend.log 2>&1 &
elif [ -f "$FRONTEND_DIST_DIR/index.html" ]; then
  write_frontend_config "$FRONTEND_DIST_DIR/benchchef-config.js"
  nohup python3 "$ROOT_DIR/scripts/serve_frontend.py" \
    "$FRONTEND_DIST_DIR" \
    "$BENCHCHEF_FRONTEND_PORT" \
    > "$ROOT_DIR/frontend.log" 2>&1 &
elif [ -f "$FRONTEND_DEV_DIST_DIR/index.html" ]; then
  write_frontend_config "$FRONTEND_DEV_DIST_DIR/benchchef-config.js"
  nohup python3 "$ROOT_DIR/scripts/serve_frontend.py" \
    "$FRONTEND_DEV_DIST_DIR" \
    "$BENCHCHEF_FRONTEND_PORT" \
    > "$ROOT_DIR/frontend.log" 2>&1 &
else
  echo "BenchChef frontend was not found." >&2
  echo "Expected either $FRONTEND_SOURCE_DIR/package.json or $FRONTEND_DIST_DIR/index.html." >&2
  exit 1
fi

echo $! > /tmp/benchchef-frontend.pid

echo "Waiting for BenchChef backend on port $BENCHCHEF_BACKEND_PORT..."

until curl -fsS "http://localhost:$BENCHCHEF_BACKEND_PORT/metrics" >/dev/null 2>&1; do
  sleep 1
done

echo "BenchChef backend is reachable."

echo "Waiting for BenchChef frontend on port $BENCHCHEF_FRONTEND_PORT..."

for _ in $(seq 1 30); do
  if curl -fsS "http://localhost:$BENCHCHEF_FRONTEND_PORT/" >/dev/null 2>&1; then
    echo "BenchChef frontend is reachable."
    break
  fi
  sleep 1
done

if ! curl -fsS "http://localhost:$BENCHCHEF_FRONTEND_PORT/" >/dev/null 2>&1; then
  echo "BenchChef frontend did not become reachable on port $BENCHCHEF_FRONTEND_PORT." >&2
  echo "Check $ROOT_DIR/frontend.log." >&2
  exit 1
fi

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
