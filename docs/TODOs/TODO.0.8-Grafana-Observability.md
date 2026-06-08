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

## SpaghettiChef REST Dependencies

0.8 does not require SpaghettiChef to expose Prometheus metrics. BenchChef
continues to call SpaghettiChef REST/JSON endpoints, stores observations, and
exports BenchChef-owned Prometheus metrics.

The required SpaghettiChef endpoints for the 0.8 dashboards are already
referenced in `docs/RELATED/rest-api.md` and in
`docs/spaghettichef-compatibility.md`:

| Dashboard area | SpaghettiChef endpoint |
| -------------- | ---------------------- |
| Availability | `GET /health` |
| Runtime/version context | `GET /version` |
| Runtime monitoring context | `GET /monitoring` |
| Dashboard asset latency | `GET /dashboard/index.html` |
| Active camera job observation | `GET /printers/{printer_id}/camera/jobs/active` |
| Camera job throughput/duration | `GET /admin/printers/{printer_id}/camera/jobs/{camera_job_id}/progress` |
| Camera job timeline | `GET /admin/printers/{printer_id}/camera/jobs/{camera_job_id}/timeline` |
| Storage growth and file health | `GET /admin/printers/{printer_id}/camera/storage/summary` |
| Delta set counts/details | `GET /admin/printers/{printer_id}/camera/jobs/{camera_job_id}/delta-sets` |
| Delta frame counts/details | `GET /admin/printers/{printer_id}/camera/delta-sets/{delta_set_id}/frames` |
| Calculation duration/results | `GET /admin/printers/{printer_id}/camera/delta-sets/{delta_set_id}/calculation-runs` |
| Calculation run detail | `GET /admin/camera/calculation-runs/{calculation_run_id}` |
| Calculation result detail | `GET /admin/camera/calculation-runs/{calculation_run_id}/results` |

The CPU, RAM, disk, and process dashboards do not require SpaghettiChef REST
changes. They use `node_exporter` and `process-exporter`.

## Acceptance Direction

```text
Grafana shows whether SpaghettiChef is healthy, degraded, slow, down, or resource-limited
Dashboards use versioned JSON files
Dashboards are provisioned automatically
```
