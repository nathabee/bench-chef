# 0.9.x TODO — Angular Workbench UI

## Status

```text
IN PROGRESS
```

## Purpose

Provide the main BenchChef browser interface.

## Planned Scope

### 0.9.1 — Workbench Plan And API Wiring

```text
DONE make this TODO step-by-step
DONE configure Angular HttpClient
DONE define typed BenchChef API services
DONE allow Angular dev port in Django CORS
```

### 0.9.2 — Dashboard Overview

```text
DONE show backend/API status
DONE show connection count
DONE show latest latency summary
DONE show latest error summary
DONE link to Prometheus and Grafana
```

### 0.9.3 — Connections

```text
DONE list connection profiles
DONE show base URL, enabled state, timeout, role header
DONE run health, version, monitoring, dashboard, and diagnostics probes
DONE show latest probe result inline
```

### 0.9.4 — Probes

```text
DONE choose connection
DONE run repeat probe
DONE run dashboard responsiveness
DONE run camera active job polling
DONE show latency summary and failures
```

### 0.9.5 — Benchmarks

```text
list benchmark runs
show status and scenario
link runs to probe samples where available
```

### 0.9.6 — Reports

```text
list report records
show report type/status
prepare links for downloadable reports when backend supports them
```

### 0.9.7 — Settings

```text
show local service URLs
show Grafana, Prometheus, backend, and frontend links
keep operational printer/camera settings out of BenchChef
```

## Original Scope

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

## Acceptance Direction

```text
Angular can call the existing BenchChef API
users can launch common probes without curl
users can navigate to Grafana and reports from the UI
```
