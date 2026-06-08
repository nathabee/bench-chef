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
