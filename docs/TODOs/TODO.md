TODO overviews

---

## TODO 0.1.x — Project Foundation

### TODO 0.1.0 — Repository Skeleton
- create repository benchchef
- create backend-django/
- create frontend-angular/
- create prometheus/
- create grafana/
- create scenarios/
- create reports/
- create docs/
- add docker-compose.yml
- add README.md
- add .env.example
- add .gitignore
- commit skeleton

### TODO 0.1.1 — Django Backend Bootstrap
- create Python virtual environment in backend-django/
- install Django
- install Django REST Framework
- create Django project
backend-django/
├── benchchef/          # Django project config: settings, urls, wsgi/asgi
├── accounts/           # later: users, roles, authentication
├── connections/        # SpaghettiChef connection profiles
├── probes/             # black-box HTTP probes and probe samples
├── benchmarks/         # benchmark runs, scenarios, run status
├── reports/            # generated reports and exports
└── manage.py
- add requirements.txt
- add backend .env.example if needed
- add GET /api/health
- verify python manage.py runserver works
- commit Django bootstrap

### TODO 0.1.2 — Angular Frontend Bootstrap
- create Angular app inside frontend-angular/
- add base layout
- add app title BenchChef
- add placeholder navigation
- add placeholder pages:
  - Dashboard
  - Connections
  - Probes
  - Benchmarks
  - Reports
  - Settings
- verify npm start works
- commit Angular bootstrap

### TODO 0.1.3 — Local Stack Smoke Test
- add basic Prometheus config
- add basic Grafana provisioning folders
- make docker compose start Prometheus and Grafana
- verify Prometheus opens on 9090
- verify Grafana opens on 3000
- document local startup commands
- commit monitoring stack bootstrap

---


## TODO 0.2.x BenchChef Backend Domain Foundation

### TODO 0.2.0
- create Django apps: connections, probes, benchmarks, reports
- add ConnectionProfile model
- add Django admin registration
- add serializers
- add basic REST endpoints

### TODO 0.2.1
- add ProbeSample model
- store URL, method, status code, latency, timeout, error message
- expose probe samples through API

### TODO 0.2.2
- add BenchmarkRun model
- add BenchmarkRun status lifecycle
- expose benchmark run list/detail API

### TODO 0.2.3
- add ReportRecord model
- store title, report type, status, output format, file path, message
- add Django admin registration
- add serializer
- expose report record list/detail API

### TODO 0.2.4
- extend ConnectionProfile for probe configuration
- store request timeout, health path, version path, monitoring path
- make connection settings editable from Django admin
- keep `.env` only for optional defaults

 
## TODO 0.3.x SpaghettiChef Connection

### TODO 0.3.0
- add backend service for SpaghettiChef HTTP calls
- use ConnectionProfile as target configuration
- call GET /health
- measure latency
- store result as ProbeSample
- expose connection test endpoint

### TODO 0.3.1
- add GET /version probe
- store version response
- store HTTP status, latency, success, timeout, error message
- expose version probe result through API

### TODO 0.3.2
- add GET /monitoring probe
- store monitoring response summary
- store HTTP status, latency, success, timeout, error message
- expose monitoring probe result through API

### TODO 0.3.3
- add dashboard asset probe
- call GET /dashboard/index.html
- measure dashboard response time
- store result as ProbeSample
- expose dashboard probe result through API

### TODO 0.3.4
- add camera job active probe
- call GET /printers/{printerId}/camera/jobs/active
- support printerId input
- store result as ProbeSample
- expose camera active-job probe result through API

### TODO 0.3.5
- add camera job progress probe
- call GET /admin/printers/{printerId}/camera/jobs/{cameraJobId}/progress
- support printerId and cameraJobId input
- store result as ProbeSample
- expose camera progress probe result through API

### TODO 0.3.6
- add camera job timeline probe
- call GET /admin/printers/{printerId}/camera/jobs/{cameraJobId}/timeline
- support printerId and cameraJobId input
- store result as ProbeSample
- expose camera timeline probe result through API

### TODO 0.3.7
- add timeout and error normalization
- define default request timeout
- distinguish timeout, connection refused, HTTP error, invalid JSON
- store normalized error message in ProbeSample

### TODO 0.3.8
- add basic connection diagnostics endpoint
- run health, version, monitoring, and dashboard probes together
- return combined online/offline/degraded status
- store individual ProbeSample rows
 

# 0.4.x TODO



## TODO 0.4.0 — Probe Type Classification

### Purpose

Classify stored `ProbeSample` rows by probe type.

### Work To Do

- add probe type field to `ProbeSample`
- support:
  - `HEALTH_PROBE`
  - `VERSION_PROBE`
  - `MONITORING_PROBE`
  - `DASHBOARD_ASSET_PROBE`
  - `CAMERA_JOB_ACTIVE_PROBE`
  - `CAMERA_JOB_PROGRESS_PROBE`
  - `CAMERA_JOB_TIMELINE_PROBE`
- update serializers
- update Django admin
- update all probe endpoints to store the correct probe type
- keep existing HTTP status, latency, timeout, success, error message

---

## TODO 0.4.1 — Repeated Probe Execution

### Purpose

Run one selected probe multiple times.

### Work To Do

- add endpoint to execute a selected probe repeatedly
- support repeat count
- support delay between requests
- store one `ProbeSample` per request
- return min, max, average latency
- return success count and failure count

---

## TODO 0.4.2 — Diagnostics History

### Purpose

Run diagnostics repeatedly and store the results.

### Work To Do

- run health, version, monitoring, and dashboard probes together
- store individual `ProbeSample` rows
- group run under `BenchmarkRun`
- calculate:
  - online count
  - degraded count
  - offline count
  - average latency

---

## TODO 0.4.3 — Dashboard Responsiveness Scenario

### Purpose

Measure dashboard availability and response time.

### Work To Do

- repeatedly call `/dashboard/index.html`
- store one `ProbeSample` per request
- calculate success rate
- calculate average latency
- calculate p50, p95, p99 latency

---

## TODO 0.4.4 — Camera Active Job Polling Scenario

### Purpose

Observe active camera job state from outside.

### Work To Do

- repeatedly call `/printers/{printerId}/camera/jobs/active`
- support `printerId`
- store one `ProbeSample` per request
- read `jobId`, `state`, `latestSnapshotId`, `latestCaptureAt` from response JSON when available
- calculate basic snapshot progression when possible

---

## TODO 0.4.5 — Camera Progress And Timeline Probes

### Purpose

Keep BenchChef aligned with planned SpaghettiChef 0.8 observability endpoints.

### Work To Do

- keep probing `/admin/printers/{printerId}/camera/jobs/{cameraJobId}/progress`
- keep probing `/admin/printers/{printerId}/camera/jobs/{cameraJobId}/timeline`
- support `printerId`
- support `cameraJobId`
- store one `ProbeSample` per request
- if endpoint returns `404`, store it as normal failed sample:
  - `status_code = 404`
  - `success = false`
  - `error_message = HTTP_ERROR: HTTP 404`
- do not read SpaghettiChef filesystem
- do not read SpaghettiChef SQLite

---

## TODO 0.4.6 — Latency Summary API

### Purpose

Summarize stored probe latency.

### Work To Do

- add API endpoint for latency summary
- filter by:
  - probe type
  - URL
  - success
  - time range
- calculate:
  - count
  - min
  - max
  - average
  - p50
  - p95
  - p99

---

## TODO 0.4.7 — Error Summary API

### Purpose

Summarize stored probe failures.

### Work To Do

- add API endpoint for error summary
- group by:
  - probe type
  - URL
  - error message
  - status code
- count:
  - timeout
  - connection refused
  - HTTP error
  - invalid JSON
  - request error

---

## TODO 0.4.8 — Slowdown Detection Preparation

### Purpose

Prepare basic trend calculation from black-box probe samples.

### Work To Do

- calculate latency trend over time
- calculate snapshot progression trend when active-job JSON contains `latestSnapshotId`
- detect increasing latency
- detect stalled snapshot progress
- do not require `/progress`
- do not require `/timeline`
- do not use white-box access

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
  
---

# 0.6.x — Grafana First Dashboard

## Purpose

Create the first useful Grafana dashboard from the metrics already exposed by BenchChef.

This is an early visualization step.

It uses only existing BenchChef / Prometheus data.

## Scope

```text
Grafana Prometheus datasource
first BenchChef dashboard
probe request count panel
probe failure count panel
probe latency panel
SpaghettiChef up/down panel
HTTP status panel
dashboard asset latency panel
```


# 0.8.x — Grafana Observability Dashboards

## Purpose

Build the complete Grafana observability layer after external system metrics are available.

This is the second Grafana step.

It combines BenchChef probe metrics with machine and process metrics.

## Scope

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