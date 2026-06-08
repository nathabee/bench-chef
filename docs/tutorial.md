# Tutorial Prometheus/Django/Grafana

```text
curl calls BenchChef API
→ BenchChef stores ProbeSample rows in SQLite
→ BenchChef /metrics converts ProbeSample rows into Prometheus metrics
→ Prometheus scrapes /metrics every 15 seconds
→ Grafana reads Prometheus and draws panels
```

## Why Prometheus knows Django exists

Yes: Prometheus mainly knows this from one file:

```text
prometheus/prometheus.yml
```

This part tells Prometheus to scrape Django:

```yaml
- job_name: "benchchef-backend"
  static_configs:
    - targets: ["host.docker.internal:18090"]
```

Prometheus automatically calls:

```text
http://host.docker.internal:18090/metrics
```

because `/metrics` is the default Prometheus scrape path.

So:

```text
Prometheus does not know Django.
Prometheus only knows: scrape this HTTP target every 15 seconds.
```

## Which curl feeds which dashboard card

### SpaghettiChef Up

Panel uses:

```text
benchchef_spaghettichef_up
```

Feed it with:

```bash
curl -fsS -X POST http://localhost:18090/api/connections/3/test-health/
```

or:

```bash
curl -fsS -X POST http://localhost:18090/api/connections/3/diagnostics/
```

Because diagnostics includes health.

---

### Probe Requests

Panel uses:

```text
benchchef_probe_requests_total
```

Any probe feeds it:

```bash
curl -fsS -X POST http://localhost:18090/api/connections/3/diagnostics/
```

or dashboard load:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/dashboard-responsiveness/ \
  -H 'Content-Type: application/json' \
  -d '{"repeat_count": 20, "delay_ms": 100}'
```

---

### Probe Failures

Panel uses:

```text
benchchef_probe_failures_total
```

Feed it by creating a failed probe, for example missing progress endpoint:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-camera-job-progress/ \
  -H 'Content-Type: application/json' \
  -d '{"printer_id": "lux01", "camera_job_id": "3"}'
```

This currently creates:

```text
HTTP_ERROR: HTTP 404
```

---

### Probe Latency

Panel uses:

```text
benchchef_probe_duration_seconds
```

Any successful or failed probe with latency feeds it:

```bash
curl -fsS -X POST http://localhost:18090/api/connections/3/diagnostics/
```

For more visible graph movement:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/dashboard-responsiveness/ \
  -H 'Content-Type: application/json' \
  -d '{"repeat_count": 20, "delay_ms": 100}'
```

---

### HTTP Status

Panel uses:

```text
benchchef_probe_http_status_total
```

Feed `200` statuses:

```bash
curl -fsS -X POST http://localhost:18090/api/connections/3/diagnostics/
```

Feed `404` status:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-camera-job-progress/ \
  -H 'Content-Type: application/json' \
  -d '{"printer_id": "lux01", "camera_job_id": "3"}'
```

---

### Timeout Count

Panel uses:

```text
benchchef_probe_timeout_total
```

You only get data if a request times out. Normal refused connection is **not timeout**. It is:

```text
CONNECTION_REFUSED
```

So timeout may stay zero for now. That is normal.

## Manual data generator

This feeds all main panels every 5 seconds:

```bash
while true; do
  curl -fsS -X POST http://localhost:18090/api/connections/3/diagnostics/ >/dev/null
  sleep 5
done
```

Stop with:

```text
CTRL+C
``` 
