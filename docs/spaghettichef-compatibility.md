# SpaghettiChef Compatibility

## Purpose

This document defines what BenchChef Local expects from SpaghettiChef Local.

It belongs to BenchChef because it describes BenchChef requirements, not the
full SpaghettiChef API.

SpaghettiChef owns the authoritative REST API documentation in:

```text
spaghetti-chef/docs/rest-api.md
```

BenchChef keeps a read-only reference note in:

```text
docs/RELATED/
```

## Ownership Boundary

```text
SpaghettiChef provides operational facts.
BenchChef turns those facts into metrics/statistics.
```

SpaghettiChef owns:

```text
health facts
version facts
monitoring facts
printer status facts
camera job facts
delta set facts
calculation run facts
storage facts
```

BenchChef owns:

```text
latency
availability
error rate
snapshot rate
storage growth
frames per second
average processing time
Prometheus /metrics format
Grafana dashboards
benchmark result storage
```

## Required Endpoints

BenchChef currently probes these SpaghettiChef endpoints.

| Probe type | Method | SpaghettiChef path | JSON expected |
| ---------- | ------ | ------------------ | ------------- |
| HEALTH_PROBE | GET | /health | yes |
| VERSION_PROBE | GET | /version | yes |
| MONITORING_PROBE | GET | /monitoring | yes |
| DASHBOARD_ASSET_PROBE | GET | /dashboard/index.html | no |
| CAMERA_JOB_ACTIVE_PROBE | GET | /printers/{printer_id}/camera/jobs/active | yes |
| CAMERA_JOB_PROGRESS_PROBE | GET | /admin/printers/{printer_id}/camera/jobs/{camera_job_id}/progress | yes |
| CAMERA_JOB_TIMELINE_PROBE | GET | /admin/printers/{printer_id}/camera/jobs/{camera_job_id}/timeline | yes |

BenchChef expects these future or planned JSON fact endpoints when the
corresponding observation work starts:

| Method | SpaghettiChef path | Purpose |
| ------ | ------------------ | ------- |
| GET | /printers/{printer_id}/status | Printer operational status |
| GET | /admin/printers/{printer_id}/camera/storage/summary | Camera storage usage summary |
| GET | /admin/printers/{printer_id}/camera/jobs/{camera_job_id}/delta-sets | Delta set list for a camera job |
| GET | /admin/printers/{printer_id}/camera/delta-sets/{delta_set_id} | Delta set detail |
| GET | /admin/printers/{printer_id}/camera/delta-sets/{delta_set_id}/frames | Delta frames for a delta set |
| GET | /admin/printers/{printer_id}/camera/delta-sets/{delta_set_id}/calculation-runs | Calculation runs for a delta set |
| GET | /admin/camera/calculation-runs/{calculation_run_id} | Calculation run detail |
| GET | /admin/camera/calculation-runs/{calculation_run_id}/results | Calculation run results |
| GET | /admin/camera/calculation-runs/{calculation_run_id}/trace | Calculation run trace |
| GET | /admin/camera/calculation-runs/{calculation_run_id}/compare?rightRunId={right_calculation_run_id} | Calculation run comparison |
| GET | /admin/camera/calculation-results/{calculation_result_id}/visual?printerId={printer_id} | Calculation result visual detail |

Not every endpoint must be implemented at once. Missing endpoints are valid
BenchChef observations and are stored as normal HTTP errors.

## Request Rules

BenchChef builds SpaghettiChef target URLs from:

```text
ConnectionProfile.base_url + configured path
```

BenchChef may send:

```text
X-SpaghettiChef-Role: {role_header}
```

All current SpaghettiChef probes use:

```text
GET
```

## Compatibility Rules

```text
2xx response = successful probe
non-2xx response = failed probe with HTTP_ERROR
timeout = failed probe with TIMEOUT
connection failure = failed probe with CONNECTION_REFUSED
invalid JSON on JSON probes = failed probe with INVALID_JSON
dashboard index probe may return HTML
```

## Required JSON Fields

SpaghettiChef JSON responses should prefer stable facts over presentation text.

Useful field families:

```text
ids
state
status
startedAt
finishedAt
durationMs
createdAt
updatedAt
counts
byte sizes
error type
```

Recommended timestamp format:

```text
ISO-8601 strings or Unix timestamps, used consistently per endpoint
```

## Camera Active Job Fields

BenchChef camera active-job polling reads these optional fields when present:

```text
latestSnapshotId
latestCaptureAt
```

## Camera Job Progress Fields

BenchChef expects camera job progress facts such as:

```text
jobId
printerId
cameraId
state
startedAt
finishedAt
durationMs
snapshotCount
deltaCount
latestSnapshotId
latestCaptureAt
errorType
```

## Camera Job Timeline Fields

BenchChef expects ordered event facts such as:

```text
timestamp
eventType
state
message
snapshotId
deltaSetId
```

## Delta Set Fields

BenchChef expects delta set facts such as:

```text
id
deltaSetId
printerId
cameraJobId
methodName
deltaSnapshotStep
sourceSnapshotCount
generatedDeltaCount
createdAt
message
```

The job-scoped delta-set list is:

```text
GET /admin/printers/{printer_id}/camera/jobs/{camera_job_id}/delta-sets
```

The delta-set detail endpoint is:

```text
GET /admin/printers/{printer_id}/camera/delta-sets/{delta_set_id}
```

## Delta Frame Fields

BenchChef expects delta frame facts such as:

```text
id
deltaSetId
printerId
cameraJobId
fromSnapshotId
toSnapshotId
fromCapturedAt
toCapturedAt
deltaPath
deltaScore
changedPixelRatio
averagePixelDelta
createdAt
```

The delta frame list endpoint is:

```text
GET /admin/printers/{printer_id}/camera/delta-sets/{delta_set_id}/frames
```

## Calculation Run Fields

BenchChef expects calculation run facts such as:

```text
id
calculationRunId
printerId
cameraJobId
deltaSetId
methodName
engineName
algorithmVariant
engineVersion
executionDurationMs
engineStatus
parameterJson
createdAt
finishedAt
resultCount
message
```

The delta-set-scoped calculation-run list is:

```text
GET /admin/printers/{printer_id}/camera/delta-sets/{delta_set_id}/calculation-runs
```

The global calculation-run detail endpoint is:

```text
GET /admin/camera/calculation-runs/{calculation_run_id}
```

## Calculation Result Fields

BenchChef expects calculation result facts such as:

```text
id
calculationRunId
deltaFrameId
confidence
suspected
reasonCodes
message
processingTimeMs
createdAt
```

Calculation result endpoints:

```text
GET /admin/camera/calculation-runs/{calculation_run_id}/results
GET /admin/camera/calculation-runs/{calculation_run_id}/trace
GET /admin/camera/calculation-runs/{calculation_run_id}/compare?rightRunId={right_calculation_run_id}
GET /admin/camera/calculation-results/{calculation_result_id}/visual?printerId={printer_id}
```

## Storage Summary Fields

BenchChef expects storage facts such as:

```text
printerId
cameraJobCount
snapshotCount
retainedSnapshotCount
deltaSetCount
deltaFrameCount
calculationRunCount
calculationResultCount
totalSnapshotBytes
totalDeltaBytes
missingFileCount
latestSnapshotAvailable
previousSnapshotAvailable
deltaPreviewAvailable
message
```

SpaghettiChef currently exposes these facts at:

```text
GET /admin/printers/{printer_id}/camera/storage/summary
```

## Non-Goals For SpaghettiChef

Do not implement these inside SpaghettiChef for this boundary:

```text
Prometheus /metrics endpoint
Prometheus text exposition format
Grafana dashboard generation
performance statistics aggregation
benchmark result storage
```

BenchChef owns those concerns.
