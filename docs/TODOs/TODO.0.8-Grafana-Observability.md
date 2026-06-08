# 0.8.x TODO — Grafana Observability Dashboards

## Status

```text
PLANNED
```

## Purpose

Build the full Grafana observability layer after external system metrics are
available.

This is the second Grafana step. It should combine BenchChef probe metrics with
machine and process metrics.

## Planned Scope

```text
SpaghettiChef availability dashboard
API latency dashboard
dashboard asset latency dashboard
camera job observation dashboard
error and timeout dashboard
CPU dashboard
RAM dashboard
disk dashboard
process resource dashboard
benchmark run dashboard
```

## Acceptance Direction

```text
Grafana shows whether SpaghettiChef is healthy, degraded, slow, down, or resource-limited
Dashboards use versioned JSON files
Dashboards are provisioned automatically
```
