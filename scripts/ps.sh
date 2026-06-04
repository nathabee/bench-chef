#!/usr/bin/env bash

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
ss -ltnp | grep -E ":18080|:18090|:4200|:9090|:3000|:3001" || echo "No matching ports"

echo
echo "=== Docker Containers ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"