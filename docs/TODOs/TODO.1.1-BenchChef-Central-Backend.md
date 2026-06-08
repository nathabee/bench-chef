# 1.1.x TODO — BenchChef Central Backend

## Status

```text
PLANNED
```

## Purpose

Implement the central backend foundation that receives monitoring data from
BenchChef Local instances.

## Planned Scope

```text
central database models
farm registry
BenchChef Local node registry
runtime identity storage
observation import endpoint
probe result import
benchmark result import
status summary import
API token authentication
basic central admin views
```

## Data To Receive

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

## Acceptance Direction

```text
BenchChef Central can register local nodes/farms
BenchChef Central can import observations from BenchChef Local
imports are idempotent or safely deduplicated
central backend stores observation history
central backend does not call SpaghettiChef Local
```
