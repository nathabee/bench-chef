# BenchChef Roadmap

BenchChef is a standalone performance supervision and benchmark workbench for SpaghettiChef.

SpaghettiChef remains operational and lightweight. BenchChef observes it from outside.

## Architecture

```text
BenchChef
├── frontend-angular/
│   └── control UI, run history, reports, Grafana links
│
├── backend-django/
│   └── API probing, benchmark runner, result storage, report generation
│
├── prometheus/
│   └── scrape BenchChef, exporters, blackbox probes
│
├── grafana/
│   └── dashboards for latency, availability, CPU, RAM, disk, benchmark runs
│
├── scenarios/
│   └── benchmark definitions
│
├── reports/
│   └── generated benchmark reports
│
└── docs/
    └── architecture, screenshots, portfolio explanation
```

## Core Principle

```text
SpaghettiChef does the work.
BenchChef measures the work.
```

BenchChef uses:

```text
black-box monitoring first
external OS/process metrics second
SpaghettiChef internal metrics only later if really needed
```

---

# 0.1.x — Project Foundation

## Purpose

Create the complete BenchChef project skeleton.

## Scope

```text
Django backend project
Angular frontend project
Docker Compose foundation
Prometheus folder
Grafana folder
scenario folder
report folder
README
environment configuration
```

## Outcome

BenchChef starts as a structured project with clear frontend/backend/monitoring separation.

---

# 0.2.x — Django Backend Foundation

## Purpose

Create the backend/runner layer.

## Scope

```text
Django project
Django REST Framework
SQLite for local development
connection profile model
benchmark run model
benchmark sample model
health endpoint
admin interface
basic API structure
```

## Initial Django Apps

```text
connections
benchmarks
probes
reports
```

## Outcome

Django can store BenchChef configuration and benchmark data.

---

# 0.3.x — SpaghettiChef Connection

## Purpose

Connect BenchChef to a SpaghettiChef runtime.

## Scope

```text
base URL configuration
optional role header
GET /health probe
GET /version probe
GET /monitoring probe
connection status
latency measurement
timeout handling
error handling
```

## SpaghettiChef Read-Only Calls

```text
GET /health
GET /version
GET /monitoring
GET /dashboard/index.html
GET /printers/{printerId}/camera/jobs/active
GET /admin/printers/{printerId}/camera/jobs
GET /admin/printers/{printerId}/camera/jobs/{cameraJobId}/progress
GET /admin/printers/{printerId}/camera/jobs/{cameraJobId}/timeline
```

## Outcome

BenchChef can check whether SpaghettiChef is reachable and responsive.

---

# 0.4.x — Black-Box Performance Probes

## Purpose

Measure SpaghettiChef from outside.

## Scope

```text
HTTP latency
HTTP status
timeout count
error count
p50 / p95 / p99 response time
dashboard asset load time
camera job polling
snapshot count over time
snapshot throughput
slowdown detection
```

## Probe Types

```text
HEALTH_PROBE
VERSION_PROBE
MONITORING_PROBE
DASHBOARD_ASSET_PROBE
CAMERA_JOB_ACTIVE_PROBE
CAMERA_JOB_PROGRESS_PROBE
CAMERA_JOB_TIMELINE_PROBE
```

## Outcome

BenchChef can measure backend and dashboard responsiveness without SpaghettiChef internal metrics.

---

# 0.5.x — Prometheus Integration

## Purpose

Expose BenchChef-measured metrics to Prometheus.

## Scope

```text
BenchChef /metrics endpoint
Prometheus scrape config
benchmark run metrics
HTTP probe metrics
camera throughput metrics
error metrics
timeout metrics
```

## Example Metrics

```text
benchchef_probe_requests_total
benchchef_probe_failures_total
benchchef_probe_duration_seconds
benchchef_spaghettichef_up
benchchef_camera_snapshots_observed_total
benchchef_camera_snapshots_per_second
benchchef_benchmark_run_duration_seconds
```

## Outcome

Prometheus stores BenchChef measurements.

---

# 0.6.x — External System Metrics

## Purpose

Monitor CPU, RAM, disk, and process behavior externally.

## Scope

```text
node_exporter setup
process-exporter setup
optional cAdvisor setup
Prometheus scrape config
metric documentation
```

## Metrics Source

```text
node_exporter       machine CPU/RAM/disk
process-exporter    SpaghettiChef process CPU/RAM
cAdvisor            container metrics, if Docker is used
blackbox_exporter   external HTTP reachability, optional
BenchChef exporter  benchmark-specific metrics
```

## Outcome

BenchChef/Grafana can correlate SpaghettiChef performance with machine/process resource usage.

---

# 0.7.x — Grafana Dashboards

## Purpose

Visualize BenchChef and exporter metrics.

## Scope

```text
SpaghettiChef availability dashboard
API latency dashboard
dashboard asset latency dashboard
camera job throughput dashboard
error/timeout dashboard
CPU/RAM/disk dashboard
benchmark run dashboard
```

## Outcome

Grafana shows whether SpaghettiChef is healthy, degraded, slow, down, or recovering.

---

# 0.8.x — Angular Workbench UI

## Purpose

Provide the portfolio-ready BenchChef interface.

## Scope

```text
connection management
probe launcher
scenario launcher
run status
run history
metric summaries
Grafana links
report browser
settings
```

## Outcome

Angular becomes the main UI for controlling BenchChef.

---

# 0.9.x — Benchmark Scenario Runner

## Purpose

Execute repeatable benchmark scenarios.

## Scope

```text
scenario definition model
scenario registry
health check scenario
dashboard load scenario
camera job observation scenario
engine run observation scenario
backend endurance scenario
concurrent API probe scenario
```

## Outcome

BenchChef can execute controlled performance tests and persist results.

---

# 1.0.x — Reports And Portfolio Release

## Purpose

Make BenchChef demonstrable and documented.

## Scope

```text
benchmark reports
run comparison
CSV export
JSON export
Markdown export
HTML export
README
screenshots
architecture documentation
installation guide
example dashboard screenshots
example benchmark result
```

---

# Non-Goals

BenchChef is not:

```text
a printer control dashboard
a SpaghettiChef replacement
a direct SQLite browser
a direct filesystem browser
an ML training tool
a slicer
a real-time print controller
a safety controller
```

BenchChef must not directly trigger:

```text
heating
movement
homing
fan control
SD-card upload
SD-card delete
print start
pause
resume
cancel
emergency stop
raw G-code
camera capture
```

unless a later explicitly safe SpaghettiChef API is designed for that exact purpose.
