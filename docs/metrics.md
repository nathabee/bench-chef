# Metrics Overview

## Purpose

This document explains how BenchChef metrics are produced.

For SpaghettiChef facts required by BenchChef, see
[spaghettichef-compatibility.md](spaghettichef-compatibility.md).

## Data Flow

```text
SpaghettiChef
      ↓
BenchChef Probe
      ↓
ProbeSample
      ↓
Prometheus Metrics
      ↓
Grafana Dashboard
```

## Current Metrics

| Django Source       | Prometheus Metric                 | Type      | Usage             |
| ------------------- | --------------------------------- | --------- | ----------------- |
| Probe execution     | benchchef_probe_requests_total    | Counter   | Total probes      |
| Probe execution     | benchchef_probe_failures_total    | Counter   | Total failures    |
| Probe execution     | benchchef_probe_timeout_total     | Counter   | Total timeouts    |
| Probe status code   | benchchef_probe_http_status_total | Counter   | HTTP distribution |
| Probe latency_ms    | benchchef_probe_duration_seconds  | Histogram | Latency analysis  |
| Health probe result | benchchef_spaghettichef_up        | Gauge     | Availability      |

These are BenchChef-generated metrics. They describe what BenchChef observed
from probes or derived from imported observations.

SpaghettiChef does not expose Prometheus metrics in the current local
architecture. BenchChef converts observations into statistics, Prometheus
metrics, and Grafana dashboards.

## Metric Types

### Counter

Always increases.

Example:

```text
benchchef_probe_requests_total
```

Used for:

```text
requests
failures
timeouts
status counts
```

### Gauge

Represents a current state.

Example:

```text
benchchef_spaghettichef_up

1 = online
0 = offline
```

### Histogram

Used for latency measurements.

Source:

```text
ProbeSample.latency_ms
```

Converted to:

```text
benchchef_probe_duration_seconds
```

Prometheus automatically generates:

```text
_bucket
_count
_sum
```

which allow Grafana to calculate:

```text
average latency
p50 latency
p95 latency
p99 latency
```

## Current Probe Types

```text
HEALTH_PROBE
VERSION_PROBE
MONITORING_PROBE
DASHBOARD_ASSET_PROBE
CAMERA_JOB_ACTIVE_PROBE
CAMERA_JOB_PROGRESS_PROBE
CAMERA_JOB_TIMELINE_PROBE
```

## SpaghettiChef Observation Sources

BenchChef metrics are derived from SpaghettiChef REST/JSON observations and
BenchChef probe timing. SpaghettiChef does not need to expose Prometheus
metrics for the 0.8 Grafana observability work.

| BenchChef observation | SpaghettiChef endpoint | Derived metric/statistic |
| --------------------- | ---------------------- | ------------------------ |
| Health probe | `GET /health` | availability, up/down, error rate, latency |
| Version probe | `GET /version` | runtime version context |
| Monitoring probe | `GET /monitoring` | runtime state context |
| Dashboard asset probe | `GET /dashboard/index.html` | dashboard asset latency and errors |
| Active camera job probe | `GET /printers/{printer_id}/camera/jobs/active` | active job availability and snapshot movement |
| Camera job progress probe | `GET /admin/printers/{printer_id}/camera/jobs/{camera_job_id}/progress` | duration, snapshot count, snapshots per second |
| Camera job timeline probe | `GET /admin/printers/{printer_id}/camera/jobs/{camera_job_id}/timeline` | event timing and state transitions |
| Storage summary observation | `GET /admin/printers/{printer_id}/camera/storage/summary` | storage growth, retained snapshot count, missing file count |
| Delta set observation | `GET /admin/printers/{printer_id}/camera/jobs/{camera_job_id}/delta-sets` | delta set count and generation status |
| Delta frame observation | `GET /admin/printers/{printer_id}/camera/delta-sets/{delta_set_id}/frames` | delta frame count and frame-level scores |
| Calculation run observation | `GET /admin/printers/{printer_id}/camera/delta-sets/{delta_set_id}/calculation-runs` | calculation duration and result count |
| Calculation result observation | `GET /admin/camera/calculation-runs/{calculation_run_id}/results` | suspected result count and processing time |

Host CPU, RAM, disk, and process metrics come from external exporters documented
in [system-metrics.md](system-metrics.md), not from SpaghettiChef REST.
