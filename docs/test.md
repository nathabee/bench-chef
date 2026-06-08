# Smoke Tests

## Purpose

This document provides basic validation steps after starting BenchChef.

## Verify Backend

```bash
curl -fsS http://localhost:18071/api/connections/
```

## Verify Prometheus

Open:

```text
http://localhost:18073/targets
```

Expected:

```text
benchchef-backend UP
node-exporter     UP
process-exporter  UP
```

## Generate Probe Data

Run diagnostics:

```bash
curl -fsS \
  -X POST \
  http://localhost:18071/api/connections/3/diagnostics/
```

Generate dashboard responsiveness data:

```bash
curl -fsS \
  -X POST \
  http://localhost:18071/api/connections/3/dashboard-responsiveness/ \
  -H 'Content-Type: application/json' \
  -d '{
    "repeat_count": 20,
    "delay_ms": 100
  }'
```

## Verify Prometheus Metrics

Open:

```text
http://localhost:18073
```

Useful queries:

```text
benchchef_probe_requests_total
benchchef_probe_failures_total
benchchef_probe_duration_seconds
benchchef_probe_http_status_total
benchchef_probe_timeout_total
benchchef_spaghettichef_up
node_memory_MemAvailable_bytes
rate(namedprocess_namegroup_cpu_seconds_total[5m])
```

## Verify Grafana

Open:

```text
http://localhost:18074
```

Navigate to:

```text
BenchChef First Dashboard
```

Expected:

```text
SpaghettiChef status visible
probe counters visible
latency graph visible
HTTP status graph visible
timeout count visible
dashboard asset latency visible
```
