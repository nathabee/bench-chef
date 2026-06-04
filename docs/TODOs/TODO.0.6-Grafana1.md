# 0.6.x — Grafana First Dashboard




## TODO(DONE)  0.6.0 — Grafana Datasource Provisioning

### Purpose

Configure Grafana so it automatically knows Prometheus as a datasource.

### Work To Do

- create Grafana datasource provisioning file
- connect Grafana to Prometheus
- avoid manual datasource setup in the browser
- verify datasource appears in Grafana UI

### Impacted Files

```text
grafana/provisioning/datasources/prometheus.yml
````

### Test

Restart stack:

```bash
docker compose down
docker compose up -d
```

Open:

```text
http://localhost:3000
```

Check:

```text
Connections / Data sources
Prometheus datasource exists
Prometheus datasource is working
```

---


## TODO 0.6.1 — Grafana Dashboard Provisioning

### Purpose

Configure Grafana so it automatically loads BenchChef dashboards from the repository.

### Work To Do

* create Grafana dashboard provisioning file
* point Grafana to `grafana/dashboards`
* avoid manual dashboard import
* keep dashboard JSON versioned in Git

### Impacted Files

```text
grafana/provisioning/dashboards/benchchef.yml
grafana/dashboards/
```

### Test

Restart stack:

```bash
docker compose down
docker compose up -d
```

Open:

```text
http://localhost:3000
```

Check:

```text
Dashboards
BenchChef folder exists
BenchChef dashboard appears
```

---

## TODO 0.6.2 — First BenchChef Grafana Dashboard

### Purpose

Create the first Grafana dashboard using existing BenchChef Prometheus metrics.

### Panels

Add panels for:

```text
SpaghettiChef up/down
probe request count
probe failure count
probe latency
HTTP status count
timeout count
dashboard asset latency
```

### Metrics Used

```text
benchchef_spaghettichef_up
benchchef_probe_requests_total
benchchef_probe_failures_total
benchchef_probe_duration_seconds
benchchef_probe_http_status_total
benchchef_probe_timeout_total
```

### Impacted Files

```text
grafana/dashboards/benchchef-first-dashboard.json
```

### Test

Open Grafana:

```text
http://localhost:3000
```

Expected:

```text
BenchChef First Dashboard opens
panels are visible
panels query Prometheus successfully
no "No data source" error
```

---

## TODO(DONE) 0.6.3 — Generate Fresh Probe Data For Dashboard

### Purpose

Create enough live data so Grafana panels show useful values.

### Work To Do

* run BenchChef health probe
* run diagnostics
* run dashboard responsiveness scenario
* optionally run camera active-job polling
* verify Prometheus receives updated data
* verify Grafana panels update
* start/stop scripts to start grafana,prometheus,spaghettichef, benchchef django and angular

### Commands

Use your real connection id.

Example:

```bash
curl -fsS -X POST http://localhost:18090/api/connections/3/test-health/

curl -fsS -X POST http://localhost:18090/api/connections/3/diagnostics/

curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/dashboard-responsiveness/ \
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
  http://localhost:18090/api/connections/3/camera-active-job-polling/ \
  -H 'Content-Type: application/json' \
  -d '{
    "printer_id": "lux01",
    "repeat_count": 5,
    "delay_ms": 1000
  }'
```

### Test

Prometheus query:

```text
benchchef_probe_requests_total
```

Grafana:

```text
refresh dashboard
values change
```

---

## TODO 0.6.4 — Document Grafana Usage

### Purpose

Document how to start the stack and open the dashboard.

### Work To Do

* update README or docs
* document Prometheus URL
* document Grafana URL
* document default Grafana login
* document first useful Prometheus queries
* document how to generate test data

### Impacted Files

```text
README.md
docs/
```

### Test

A reader can start the stack and open the dashboard by following the documentation.

---

## Acceptance Criteria

```text
Grafana starts through docker compose
Prometheus datasource is provisioned automatically
BenchChef dashboard is provisioned automatically
dashboard uses BenchChef Prometheus metrics
SpaghettiChef up/down panel works
probe request count panel works
probe failure count panel works
probe latency panel works
HTTP status panel works
timeout panel works
dashboard asset latency panel works
no CPU/RAM/disk metrics are included yet
no external exporters are required yet
```

---

## Suggested Commit

```bash
git status
git add .
git commit -m 'Add first Grafana dashboard'
```
 
