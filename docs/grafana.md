# Grafana Integration

## Purpose

This document explains how Grafana is connected to BenchChef and how dashboards are built.

## Architecture

```text
SpaghettiChef
      ↓
BenchChef Django Backend
      ↓
Prometheus
      ↓
Grafana
```

Grafana never communicates directly with SpaghettiChef.

Grafana queries Prometheus.

Prometheus scrapes BenchChef metrics.

BenchChef collects and exports measurements.

## Provisioning

BenchChef uses Grafana provisioning.

This allows dashboards and datasources to be versioned in Git.

### Datasource Provisioning

File:

```text
grafana/provisioning/datasources/prometheus-datasource.yml
```

Purpose:

```text
Automatically configure Prometheus as a Grafana datasource.
```

Typical configuration:

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    uid: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

### Dashboard Provisioning

File:

```text
grafana/provisioning/dashboards/benchchef.yml
```

Purpose:

```text
Tell Grafana where dashboard JSON files are stored.
```

Typical configuration:

```yaml
apiVersion: 1

providers:
  - name: BenchChef
    folder: BenchChef
    type: file
    options:
      path: /var/lib/grafana/dashboards
```

## Dashboard Files

Dashboard definitions are stored in:

```text
grafana/dashboards/
```

Current dashboard:

```text
benchchef-first-dashboard.json
```

The dashboard is loaded automatically at startup.

No manual import is required.

## Start And Open Grafana

Start the local BenchChef stack:

```bash
./scripts/start.sh
```

Open:

```text
Prometheus   http://localhost:18073
Grafana      http://localhost:18074
```

Default Grafana login:

```text
user: admin
password: admin
```

After login, open:

```text
Dashboards
BenchChef
BenchChef First Dashboard
```

Grafana should already have:

```text
Prometheus datasource
BenchChef dashboard folder
BenchChef First Dashboard
```

No manual datasource setup or dashboard import should be required.

## Generate Test Data

The dashboard needs recent BenchChef probe samples. Use your real connection id
from:

```bash
curl -fsS http://localhost:18071/api/connections/
```

Run one health probe:

```bash
curl -fsS -X POST http://localhost:18071/api/connections/{connection-id}/test-health/
```

Run diagnostics:

```bash
curl -fsS -X POST http://localhost:18071/api/connections/{connection-id}/diagnostics/
```

Generate dashboard responsiveness data:

```bash
curl -fsS \
  -X POST \
  http://localhost:18071/api/connections/{connection-id}/dashboard-responsiveness/ \
  -H 'Content-Type: application/json' \
  -d '{
    "repeat_count": 10,
    "delay_ms": 100
  }'
```

Optional camera polling:

```bash
curl -fsS \
  -X POST \
  http://localhost:18071/api/connections/{connection-id}/camera-active-job-polling/ \
  -H 'Content-Type: application/json' \
  -d '{
    "printer_id": "lux01",
    "repeat_count": 5,
    "delay_ms": 1000
  }'
```

## Expected Dashboard Panels

The first dashboard uses only BenchChef Prometheus metrics.

Expected panels:

```text
SpaghettiChef up/down
probe request count
probe failure count
probe latency
HTTP status count
timeout count
dashboard asset latency
```

This dashboard does not include CPU, RAM, disk, or process metrics yet.

No external exporters are required for this dashboard.

## Prometheus Queries

Grafana panels use PromQL.

Examples:

### Total Probe Requests

```promql
sum(benchchef_probe_requests_total)
```

### Total Probe Failures

```promql
sum(benchchef_probe_failures_total)
```

### SpaghettiChef Availability

```promql
benchchef_spaghettichef_up
```

### Probe Latency

```promql
histogram_quantile(
  0.95,
  sum by (le, probe_type)
  (
    rate(benchchef_probe_duration_seconds_bucket[5m])
  )
)
```

### HTTP Status Count

```promql
sum by (status_code) (benchchef_probe_http_status_total)
```

### Timeout Count

```promql
sum(benchchef_probe_timeout_total)
```

### Dashboard Asset Latency

```promql
histogram_quantile(
  0.95,
  sum by (le)
  (
    rate(benchchef_probe_duration_seconds_bucket{probe_type="DASHBOARD_ASSET_PROBE"}[5m])
  )
)
```

## Adding a New Panel

Typical workflow:

### 1. Add measurement in Django

Example:

```text
ProbeSample
```

or

```text
new benchmark metric
```

### 2. Export metric

Update:

```text
backend-django/probes/metrics.py
```

Expose:

```text
Counter
Gauge
Histogram
```

### 3. Verify metric

Open:

```text
http://localhost:18071/metrics
```

or query Prometheus:

```promql
metric_name
```

### 4. Add Grafana panel

Update dashboard JSON.

Choose:

```text
panel type
title
PromQL query
layout position
```

Restart Grafana if required.

## Current Dashboard Scope

Current dashboard focuses on:

```text
SpaghettiChef availability
probe counts
probe failures
probe latency
HTTP status distribution
dashboard responsiveness
```

Not included yet:

```text
CPU usage
RAM usage
disk usage
system metrics
external exporter metrics
```
