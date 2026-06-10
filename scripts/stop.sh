#!/usr/bin/env bash

set +e

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

stop_pid_file() {
    local name="$1"
    local file="$2"

    if [ -f "$file" ]; then
        local pid
        pid="$(cat "$file")"
        if [ -n "$pid" ] && ps -p "$pid" > /dev/null 2>&1; then
            echo "Stopping $name (PID $pid)..."
            kill "$pid" > /dev/null 2>&1 || true
            sleep 1
            if ps -p "$pid" > /dev/null 2>&1; then
                kill -9 "$pid" > /dev/null 2>&1 || true
            fi
        fi
        rm -f "$file"
    fi
}

echo "Stopping Angular..."

stop_pid_file "Angular" /tmp/benchchef-frontend.pid

echo "Stopping Django..."

stop_pid_file "Django" /tmp/benchchef-backend.pid

echo "Stopping Docker containers..."

cd "$ROOT_DIR"
if [ -f "$ROOT_DIR/.compose.env" ]; then
    docker compose --env-file "$ROOT_DIR/.compose.env" down
else
    docker compose down
fi

echo "Done."
