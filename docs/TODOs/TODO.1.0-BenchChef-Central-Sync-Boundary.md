# 1.0.x TODO — BenchChef Central Sync Boundary

## Status

```text
PLANNED
```

## Purpose

Define the boundary between BenchChef Local and BenchChef Central.

BenchChef Central must communicate with BenchChef Local, not directly with
SpaghettiChef Local.

## Architecture Rule

```text
SpaghettiChef Local -> operational printer/camera runtime inside LAN
BenchChef Local     -> safe local observer and sync sender
BenchChef Central   -> central receiver, registry, storage, dashboard layer
```

BenchChef Central must not require SpaghettiChef Central.

## Planned Scope

```text
local node identity model
farm identity model
SpaghettiChef runtime identity fields
observation payload shape
central sync endpoint draft
API token authentication model
idempotency and deduplication rules
retry behavior for offline LANs
payload validation
```

## Repository Layout Direction

Before implementing BenchChef Central, decide the repository layout so local
and central code do not drift into the same folders.

Preferred target shape:

```text
bench-chef/
├── VERSION
├── README.md
├── .gitignore
├── Jenkinsfile
├── docs/
├── tools/
├── local/
│   ├── backend-django/
│   ├── frontend-angular/
│   ├── prometheus/
│   ├── grafana/
│   ├── scripts/
│   └── docker-compose.yml
├── central/
│   ├── backend-django/
│   ├── frontend-angular/
│   ├── prometheus/
│   ├── grafana/
│   ├── scripts/
│   └── docker-compose.yml
└── shared/
    └── optional shared code later
```

Root-level files remain the project and release control layer:

```text
VERSION
README
docs
tools/git-hooks
Jenkinsfile
release packaging
global roadmap
```

`local/` should contain the current BenchChef Local application:

```text
local Django backend
local Angular workbench
local Prometheus and Grafana configuration
local start/stop scripts
local docker compose
```

`central/` should contain the future VPS application:

```text
central Django backend
central Angular workbench
central Prometheus and Grafana configuration
central deployment scripts
central docker compose
```

Do not mix central code into the existing local backend/frontend unless the
design proves it is truly the same application. The current expectation is that
they have different responsibilities:

```text
BenchChef Local   -> nearby SpaghettiChef observation and sync sender
BenchChef Central -> multi-farm registry, import, history, and dashboard layer
```

Keep root scripts as friendly wrappers if useful:

```text
scripts/start-local.sh
scripts/stop-local.sh
scripts/start-central.sh
scripts/stop-central.sh
```

The layout migration should happen before central implementation work starts,
but after the local release/install flow is stable.

## Reserved API Direction

These names are draft placeholders for the central sync contract. Keep them
stable once implementation starts, then promote them to the relevant BenchChef
boundary document.

```text
POST /api/central/observations/import/
GET  /api/central/local-nodes/
GET  /api/central/farms/
```

## Non-Goals

```text
no printer control actions
no direct calls from BenchChef Central to SpaghettiChef Local
no public exposure of local printer/camera REST APIs
no dependency on SpaghettiChef Central
```

## Acceptance Direction

```text
sync payload structure is documented
central/local responsibility split is clear
authentication direction is chosen
SpaghettiChef Local remains LAN-only
```
