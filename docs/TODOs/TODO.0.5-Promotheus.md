# 0.5.x TODO — Prometheus Integration


## TODO 0.5.0 — BenchChef Metrics Endpoint

### Purpose

Expose BenchChef probe data through a Prometheus-compatible `/metrics` endpoint.

### Work To Do

- add Prometheus metrics response endpoint in Django
- expose probe request counters
- expose probe failure counters
- expose probe latency metrics
- expose SpaghettiChef up/down metric from latest health probe
- do not change SpaghettiChef
- do not add Grafana dashboards yet

### Impacted Files

```text
backend-django/probes/metrics.py
backend-django/probes/views.py
backend-django/probes/urls.py
```

---

## TODO 0.5.1 — Probe Metrics

### Purpose

Convert stored `ProbeSample` rows into Prometheus metrics.

### Work To Do

Expose:

```text
benchchef_probe_requests_total
benchchef_probe_failures_total
benchchef_probe_duration_seconds
benchchef_probe_timeout_total
benchchef_probe_http_status_total
```

Labels:

```text
probe_type
connection_name
success
status_code
```

### Acceptance Criteria

```text
/metrics returns valid Prometheus text format
probe count appears
failure count appears
latency metric appears
timeout count appears
HTTP status count appears
```

---

## TODO 0.5.2 — SpaghettiChef Availability Metric

### Purpose

Expose a simple availability metric for the latest health probe.

### Work To Do

Expose:

```text
benchchef_spaghettichef_up
```

Meaning:

```text
1 = latest health probe succeeded
0 = latest health probe failed or no health probe exists
```

Labels:

```text
connection_name
base_url
```

### Acceptance Criteria

```text
metric returns 1 when latest health probe succeeded
metric returns 0 when latest health probe failed
metric is visible in Prometheus
```

---

## TODO 0.5.3 — Camera Observation Metrics

### Purpose

Expose camera observation metrics from stored camera active-job probe samples.

### Work To Do

Read `response_json` from `CAMERA_JOB_ACTIVE_PROBE`.

Expose when available:

```text
benchchef_camera_active
benchchef_camera_latest_snapshot_id
```

Labels:

```text
connection_name
printer_id
```

Optional later:

```text
benchchef_camera_snapshots_per_second
```

Only if enough repeated samples exist.

### Acceptance Criteria

```text
camera active metric appears when active-job samples exist
latest snapshot id metric appears when latestSnapshotId is numeric
missing camera data does not crash /metrics
```

---

## TODO 0.5.4 — Benchmark Run Metrics

### Purpose

Expose basic `BenchmarkRun` status metrics.

### Work To Do

Expose:

```text
benchchef_benchmark_runs_total
benchchef_benchmark_run_status_total
```

Labels:

```text
scenario_name
status
```

### Acceptance Criteria

```text
benchmark run count appears
benchmark run status count appears
metrics work even if no benchmark runs exist
```

---

## TODO 0.5.5 — Prometheus Scrape Configuration

### Purpose

Configure Prometheus to scrape BenchChef Django.

### Work To Do

Update:

```text
prometheus/prometheus.yml
```

Add BenchChef backend scrape job:

```yaml
  - job_name: 'benchchef-backend'
    static_configs:
      - targets: ['host.docker.internal:18090']
```

For Linux Docker, if `host.docker.internal` does not resolve, add to `docker-compose.yml`:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

### Acceptance Criteria

```text
Prometheus targets page shows benchchef-backend
benchchef-backend target is UP
Prometheus can query benchchef_probe_requests_total
```

---

## TODO 0.5.6 — Metrics Smoke Test

### Purpose

Verify the full BenchChef → Prometheus path.

### Work To Do

Run probes:

```bash
curl -fsS -X POST http://localhost:18090/api/connections/3/test-health/
curl -fsS -X POST http://localhost:18090/api/connections/3/diagnostics/
curl -fsS -X POST http://localhost:18090/api/connections/3/dashboard-responsiveness/ \
  -H 'Content-Type: application/json' \
  -d '{"repeat_count": 5, "delay_ms": 100}'
```

Check Django metrics:

```bash
curl -fsS http://localhost:18090/metrics
```

Check Prometheus:

```text
http://localhost:9090
```

Queries:

```text
benchchef_probe_requests_total
benchchef_probe_failures_total
benchchef_probe_duration_seconds
benchchef_spaghettichef_up
```

### Acceptance Criteria

```text
Django /metrics works
Prometheus scrape works
Prometheus stores BenchChef metrics
no Grafana dashboard yet
```

---

## Suggested Commit

```bash
git status
git add .
git commit -m 'Add Prometheus metrics integration'
```
 