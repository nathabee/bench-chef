#!/usr/bin/env bash

set +e

echo "Stopping Angular..."

if [ -f /tmp/benchchef-frontend.pid ]; then
    kill "$(cat /tmp/benchchef-frontend.pid)"
    rm -f /tmp/benchchef-frontend.pid
fi

echo "Stopping Django..."

if [ -f /tmp/benchchef-backend.pid ]; then
    kill "$(cat /tmp/benchchef-backend.pid)"
    rm -f /tmp/benchchef-backend.pid
fi

echo "Stopping SpaghettiChef..."

if [ -f /tmp/spaghettichef.pid ]; then
    kill "$(cat /tmp/spaghettichef.pid)"
    rm -f /tmp/spaghettichef.pid
fi

echo "Stopping Docker containers..."

cd ~/coding/github/bench-chef
docker compose down

echo "Done."