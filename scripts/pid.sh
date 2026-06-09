#!/usr/bin/env bash

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

check_pid() {
    local name=$1
    local file=$2

    if [ -f "$file" ]; then
        pid=$(cat "$file")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo "$name : RUNNING (PID $pid)"
        else
            echo "$name : DEAD (stale pid file)"
        fi
    else
        echo "$name : NOT STARTED"
    fi
}

echo "=== Processes ==="

check_pid "SpaghettiChef" "/tmp/spaghettichef.pid"
check_pid "BenchChef Backend" "/tmp/benchchef-backend.pid"
check_pid "BenchChef Frontend" "/tmp/benchchef-frontend.pid"

echo
echo "=== Docker ==="
docker compose ps
