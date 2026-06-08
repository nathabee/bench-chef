# API Contract

## Purpose

This document lists the HTTP interfaces that matter for BenchChef and
SpaghettiChef compatibility.

It has two parts:

```text
BenchChef API
SpaghettiChef API called by BenchChef probes
```

The second part is the compatibility checklist for SpaghettiChef.

## BenchChef API

BenchChef exposes these endpoints from the Django backend.

Default local backend:

```text
http://localhost:18090
```

### Connection Profiles

| Method | Path                                      | Purpose                         |
| ------ | ----------------------------------------- | ------------------------------- |
| GET    | /api/connections/                         | List configured targets         |
| POST   | /api/connections/                         | Create a target connection      |
| GET    | /api/connections/{id}/                    | Read one target connection      |
| PUT    | /api/connections/{id}/                    | Replace one target connection   |
| PATCH  | /api/connections/{id}/                    | Update one target connection    |
| DELETE | /api/connections/{id}/                    | Delete one target connection    |
| POST   | /api/connections/{id}/test-health/        | Run one SpaghettiChef health probe |
| POST   | /api/connections/{id}/test-version/       | Run one SpaghettiChef version probe |
| POST   | /api/connections/{id}/test-monitoring/    | Run one SpaghettiChef monitoring probe |
| POST   | /api/connections/{id}/test-dashboard-index/ | Run one SpaghettiChef dashboard index probe |
| POST   | /api/connections/{id}/test-camera-active-job/ | Run one active camera job probe |
| POST   | /api/connections/{id}/test-camera-job-progress/ | Run one camera job progress probe |
| POST   | /api/connections/{id}/test-camera-job-timeline/ | Run one camera job timeline probe |
| POST   | /api/connections/{id}/diagnostics/        | Run health, version, monitoring, and dashboard probes |
| POST   | /api/connections/{id}/repeat-probe/       | Repeat one supported probe type |
| POST   | /api/connections/{id}/diagnostics-history/ | Repeat diagnostics and attach samples to a benchmark run |
| POST   | /api/connections/{id}/dashboard-responsiveness/ | Repeat dashboard index probes |
| POST   | /api/connections/{id}/camera-active-job-polling/ | Poll active camera job state |

Connection profile fields:

| Field              | Type    | Notes |
| ------------------ | ------- | ----- |
| id                 | integer | Read-only |
| name               | string  | Unique profile name |
| base_url           | URL     | SpaghettiChef base URL |
| role_header        | string  | Optional value sent as `X-User-Role` |
| health_path        | string  | Default `/health` |
| version_path       | string  | Default `/version` |
| monitoring_path    | string  | Default `/monitoring` |
| dashboard_index_path | string | Default `/dashboard/index.html` |
| request_timeout_ms | integer | Per-request timeout |
| enabled            | boolean | Whether this profile is active |
| created_at         | datetime | Read-only |
| updated_at         | datetime | Read-only |

Probe response shape:

```json
{
  "connection": {
    "id": 1,
    "name": "Local SpaghettiChef",
    "base_url": "http://localhost:18080"
  },
  "probe": {
    "id": 123,
    "probe_type": "HEALTH_PROBE",
    "method": "GET",
    "url": "http://localhost:18080/health",
    "status_code": 200,
    "latency_ms": 12,
    "timed_out": false,
    "success": true,
    "error_message": "",
    "response_json": {}
  }
}
```

Camera probe request bodies:

| BenchChef endpoint | Required body fields |
| ------------------ | -------------------- |
| /api/connections/{id}/test-camera-active-job/ | `printer_id` |
| /api/connections/{id}/test-camera-job-progress/ | `printer_id`, `camera_job_id` |
| /api/connections/{id}/test-camera-job-timeline/ | `printer_id`, `camera_job_id` |
| /api/connections/{id}/camera-active-job-polling/ | `printer_id` |

Repeat request body fields:

| BenchChef endpoint | Body fields |
| ------------------ | ----------- |
| /api/connections/{id}/repeat-probe/ | `probe_type`, optional `repeat_count`, optional `delay_ms` |
| /api/connections/{id}/diagnostics-history/ | optional `repeat_count`, optional `delay_ms` |
| /api/connections/{id}/dashboard-responsiveness/ | optional `repeat_count`, optional `delay_ms` |
| /api/connections/{id}/camera-active-job-polling/ | `printer_id`, optional `repeat_count`, optional `delay_ms` |

`repeat-probe` currently supports:

```text
HEALTH_PROBE
VERSION_PROBE
MONITORING_PROBE
DASHBOARD_ASSET_PROBE
```

### Probe Samples

| Method | Path                                      | Purpose |
| ------ | ----------------------------------------- | ------- |
| GET    | /api/probe-samples/                       | List stored probe samples |
| POST   | /api/probe-samples/                       | Create a probe sample |
| GET    | /api/probe-samples/{id}/                  | Read one probe sample |
| PUT    | /api/probe-samples/{id}/                  | Replace one probe sample |
| PATCH  | /api/probe-samples/{id}/                  | Update one probe sample |
| DELETE | /api/probe-samples/{id}/                  | Delete one probe sample |
| GET    | /api/probe-samples/latency-summary/       | Summarize latency |
| GET    | /api/probe-samples/error-summary/         | Summarize failures |
| GET    | /api/probe-samples/slowdown-summary/      | Compare first and last latency |

Supported filters:

```text
probe_type
url
success=true
success=false
```

Probe sample fields:

| Field              | Type    | Notes |
| ------------------ | ------- | ----- |
| id                 | integer | Read-only |
| probe_type         | string  | Probe type name |
| connection_profile | integer | Connection profile id |
| benchmark_run      | integer | Benchmark run id |
| method             | string  | Usually `GET` |
| url                | URL     | Target URL called |
| status_code        | integer or null | HTTP status from target |
| latency_ms         | integer or null | Measured latency |
| timed_out          | boolean | Whether the request timed out |
| success            | boolean | True for successful probe result |
| error_message      | string  | Normalized failure text |
| response_json      | object, array, or null | Parsed JSON response when available |
| created_at         | datetime | Read-only |

Probe types:

```text
HEALTH_PROBE
VERSION_PROBE
MONITORING_PROBE
DASHBOARD_ASSET_PROBE
CAMERA_JOB_ACTIVE_PROBE
CAMERA_JOB_PROGRESS_PROBE
CAMERA_JOB_TIMELINE_PROBE
```

### Prometheus Metrics

| Method | Path     | Purpose |
| ------ | -------- | ------- |
| GET    | /metrics | Prometheus text exposition endpoint |
| GET    | /api/metrics | Same metrics endpoint under the API prefix |

### Benchmark Runs

| Method | Path                       | Purpose |
| ------ | -------------------------- | ------- |
| GET    | /api/benchmark-runs/       | List benchmark runs |
| POST   | /api/benchmark-runs/       | Create a benchmark run |
| GET    | /api/benchmark-runs/{id}/  | Read one benchmark run |
| PUT    | /api/benchmark-runs/{id}/  | Replace one benchmark run |
| PATCH  | /api/benchmark-runs/{id}/  | Update one benchmark run |
| DELETE | /api/benchmark-runs/{id}/  | Delete one benchmark run |

### Report Records

| Method | Path                     | Purpose |
| ------ | ------------------------ | ------- |
| GET    | /api/report-records/     | List report records |
| POST   | /api/report-records/     | Create a report record |
| GET    | /api/report-records/{id}/ | Read one report record |
| PUT    | /api/report-records/{id}/ | Replace one report record |
| PATCH  | /api/report-records/{id}/ | Update one report record |
| DELETE | /api/report-records/{id}/ | Delete one report record |

## SpaghettiChef API Called By BenchChef

BenchChef builds target URLs from:

```text
ConnectionProfile.base_url + configured path
```

If `role_header` is configured, BenchChef sends:

```text
X-User-Role: {role_header}
```

All current SpaghettiChef probes use `GET`.

| Probe type | Method | Default SpaghettiChef path | JSON expected | BenchChef trigger |
| ---------- | ------ | -------------------------- | ------------- | ----------------- |
| HEALTH_PROBE | GET | /health | yes | /api/connections/{id}/test-health/ |
| VERSION_PROBE | GET | /version | yes | /api/connections/{id}/test-version/ |
| MONITORING_PROBE | GET | /monitoring | yes | /api/connections/{id}/test-monitoring/ |
| DASHBOARD_ASSET_PROBE | GET | /dashboard/index.html | no | /api/connections/{id}/test-dashboard-index/ |
| CAMERA_JOB_ACTIVE_PROBE | GET | /printers/{printer_id}/camera/jobs/active | yes | /api/connections/{id}/test-camera-active-job/ |
| CAMERA_JOB_PROGRESS_PROBE | GET | /admin/printers/{printer_id}/camera/jobs/{camera_job_id}/progress | yes | /api/connections/{id}/test-camera-job-progress/ |
| CAMERA_JOB_TIMELINE_PROBE | GET | /admin/printers/{printer_id}/camera/jobs/{camera_job_id}/timeline | yes | /api/connections/{id}/test-camera-job-timeline/ |

Compatibility requirements:

```text
2xx response = successful probe
non-2xx response = failed probe with HTTP_ERROR
timeout = failed probe with TIMEOUT
connection failure = failed probe with CONNECTION_REFUSED
invalid JSON on JSON probes = failed probe with INVALID_JSON
dashboard index probe may return HTML
```

Camera active job polling reads these optional fields when the response is a
JSON object:

```text
latestSnapshotId
latestCaptureAt
```

Those fields are used only for BenchChef polling summaries.

## Metrics Relationship

API probe results are stored as `ProbeSample` rows. Prometheus metrics are then
derived from those stored samples.

See [metrics.md](metrics.md) for the Prometheus metric names and dashboard usage.
