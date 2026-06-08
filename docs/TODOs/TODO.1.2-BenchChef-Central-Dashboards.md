# 1.2.x TODO — BenchChef Central Dashboards

## Status

```text
PLANNED
```

## Purpose

Provide central visibility across multiple LAN farms.

BenchChef Central should make it possible to compare availability, latency,
errors, and benchmark observations across BenchChef Local instances.

## Planned Scope

```text
central frontend overview
farm list
BenchChef Local node list
runtime status summaries
central Prometheus metrics
central Grafana datasource
central Grafana dashboard
cross-farm availability view
cross-farm latency view
cross-farm error view
```

## Acceptance Direction

```text
central UI shows registered farms and local nodes
central Prometheus exposes imported observation metrics
central Grafana can visualize multiple LAN farms
dashboards do not require direct SpaghettiChef Local access
```
