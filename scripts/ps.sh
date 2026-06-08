#!/usr/bin/env bash

set -a
source .env
set +a

echo
echo "=== SpaghettiChef ==="
ps -ef | grep -v grep | grep "spaghettichef.Main" || echo "Not running"

echo
echo "=== BenchChef Django ==="
ps -ef | grep -v grep | grep "manage.py runserver" || echo "Not running"

echo
echo "=== BenchChef Angular ==="
ps -ef | grep -v grep | grep "ng serve" || echo "Not running"

echo
echo "=== Listening Ports ==="
ss -ltnp | grep -E ":${PORTSPAGHETTICHEF}|:${BENCHCHEF_BACKEND_PORT}|:${BENCHCHEF_FRONTEND_PORT}|:${PROMETHEUS_PORT}|:${GRAFANA_PORT}|:${NODE_EXPORTER_PORT}|:${PROCESS_EXPORTER_PORT}" || echo "No matching ports"

echo
echo "=== Docker Containers ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
