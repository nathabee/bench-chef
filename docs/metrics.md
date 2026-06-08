# Metrics Overview

## Purpose

This document explains how BenchChef metrics are produced.

For the HTTP interface contract and the SpaghettiChef endpoints called by
BenchChef, see [API.md](API.md).

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
