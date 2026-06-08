# BenchChef Roadmap

BenchChef is a performance supervision and benchmark workbench for
SpaghettiChef.

```text
SpaghettiChef does the work.
BenchChef measures the work.
```

This roadmap describes the next architecture direction. Detailed
implementation tasks live in the per-version TODO files under [TODOs](TODOs/).
The current SpaghettiChef expectations are documented in
[spaghettichef-compatibility.md](spaghettichef-compatibility.md).

## Current Baseline

BenchChef currently focuses on a local deployment close to one SpaghettiChef
runtime.

```text
SpaghettiChef Local
  exposes local REST APIs
  controls printers
  handles cameras
  creates pictures, snapshots, and deltas

BenchChef Local
  calls SpaghettiChef Local REST APIs
  measures availability, HTTP status, latency, errors, and timeouts
  stores probe and benchmark observations
  exposes Prometheus metrics
  supports local Grafana dashboards
```

## Next Major Goal

The next architecture goal is to support a central BenchChef deployment on a
VPS that mirrors monitoring data from one or more LAN-based BenchChef Local
instances.

BenchChef Central must communicate with BenchChef Local, not with
SpaghettiChef Local.

This keeps operational printer and camera APIs inside the LAN. BenchChef Local
is the safe boundary component that may access SpaghettiChef Local. BenchChef
Central should only receive monitoring, benchmark, and observation data that
has already been collected or prepared by BenchChef Local.

## BenchChef Central Architecture

### SpaghettiChef Local

SpaghettiChef Local remains the operational system.

```text
controls printers
handles cameras
creates pictures, snapshots, and deltas
exposes local REST APIs used by BenchChef Local
```

### BenchChef Local

BenchChef Local remains close to SpaghettiChef Local inside the same LAN.

```text
calls local SpaghettiChef REST APIs
measures local REST latency
measures camera job duration
measures image-processing calculation duration where available
measures availability, errors, and timeouts
collects machine and resource indicators where possible
stores or prepares already-computed monitoring observations
may continue to use local Prometheus and Grafana for local debugging
syncs prepared observations outward to BenchChef Central
```

### BenchChef Central

BenchChef Central runs alone on a VPS.

```text
has its own backend
has its own frontend
has its own database
has its own Prometheus
has its own Grafana
receives or imports monitoring data from BenchChef Local instances
keeps a central registry of BenchChef Local nodes and farms
stores central observation history
provides central dashboards across multiple LAN farms
```

BenchChef Central must not directly call SpaghettiChef Local REST APIs.
BenchChef Central must not depend on SpaghettiChef Central.

## Target Architecture

```text
LAN Farm
├── SpaghettiChef Local
│   ├── controls printers
│   ├── handles cameras
│   ├── creates pictures/snapshots/deltas
│   └── exposes local REST APIs
│
└── BenchChef Local
    ├── probes SpaghettiChef Local
    ├── stores/prepares monitoring observations
    ├── may expose local Prometheus/Grafana for debugging
    └── syncs observations outward

VPS
└── BenchChef Central
    ├── receives observations from BenchChef Local
    ├── stores central observation history
    ├── exposes central dashboards
    └── provides Prometheus/Grafana central visualization
```

## Connection Model

Prefer secure outbound sync from BenchChef Local to BenchChef Central.

This avoids exposing LAN services publicly.

The first implementation may use:

```text
HTTPS
API token authentication
idempotent observation import
clear farm/runtime identity fields
```

A later deployment may use WireGuard or another private network. That private
network must remain optional and must not make SpaghettiChef Central mandatory.

The sync payload should contain:

```text
farm identity
BenchChef Local node identity
SpaghettiChef runtime identity
timestamps
probe results
benchmark results
status summaries
latency and duration measurements
availability and error observations
machine/resource indicators where available
```

The sync payload must not include printer-control actions.

## Architectural Assumption

SpaghettiChef Central may never be developed.

BenchChef Central must therefore be architecturally independent. It must not
require a SpaghettiChef Central farm directory, registry, or control plane.

BenchChef Central should maintain its own registry of BenchChef Local nodes and
farms.

## Practical Next Step

The next design work should define the BenchChef Local to BenchChef Central
sync boundary:

```text
local node/farm identity model
central registry model
observation payload shape
authentication model
import/deduplication behavior
central storage model
central dashboard data model
failure and retry behavior for offline LANs
```

Keep SpaghettiChef-facing expectations documented separately in
[spaghettichef-compatibility.md](spaghettichef-compatibility.md).
Only promote new central sync endpoints to the API contract when implementation
starts.

## Non-Goals

Do not make BenchChef Central control printers.

Do not make BenchChef Central call SpaghettiChef Local directly.

Do not require SpaghettiChef Central.

Do not expose local printer or camera REST APIs to the public internet.

Do not duplicate SpaghettiChef operational responsibilities inside BenchChef.

Do not include printer-control actions in central sync payloads.
