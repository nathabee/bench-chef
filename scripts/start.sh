#!/usr/bin/env bash
set -euo pipefail

cd ~/coding/github/bench-chef

set -a
source .env
set +a
 


envsubst < prometheus/prometheus.yml.template > prometheus/prometheus.yml

cd ~/coding/github/spaghetti-chef/develop
nohup mvn \
  -Dexec.mainClass="spaghettichef.Main" \
  -Dspaghettichef.databaseFile=spaghettichef-local.db \
  -Dspaghettichef.api.port="$PORTSPAGHETTICHEF" \
  exec:java > spaghettichef.log 2>&1 &

echo $! > /tmp/spaghettichef.pid

cd ~/coding/github/bench-chef
docker compose up -d

cd ~/coding/github/bench-chef/backend-django
nohup python manage.py runserver \
  0.0.0.0:"$BENCHCHEF_BACKEND_PORT" \
  > backend.log 2>&1 &

echo $! > /tmp/benchchef-backend.pid

cd ~/coding/github/bench-chef/frontend-angular
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

echo "Starting diagnostics loop..."

while true; do
  curl -fsS -X POST "http://localhost:$BENCHCHEF_BACKEND_PORT/api/connections/3/diagnostics/" >/dev/null || true
  sleep 5
done