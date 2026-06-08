# TODO 0.3.x - Connection to SpaghettiChef

SpaghettiChef compatibility contract: [../spaghettichef-compatibility.md](../spaghettichef-compatibility.md).

## TODO(DONE) 0.3.0 — SpaghettiChef Health Connection Probe

### Purpose

Implement the first real BenchChef black-box probe against SpaghettiChef.

This step tests one configured SpaghettiChef connection by calling:

```text
GET /health
```

BenchChef must measure latency, normalize the result, and store it as a `ProbeSample`.

 

### Work To Do

#### 1. Add HTTP client dependency

Use `requests` for the first implementation.

```bash
cd ~/coding/github/bench-chef/backend-django
source .venv/bin/activate

pip install requests
pip freeze > requirements.txt
```
 
 
#### 2. Add SpaghettiChef client service

Create:

```text
backend-django/connections/services.py
```

 
Responsibilities implemented:

```text
build full URL from base_url + health_path
call GET /health
apply timeout from request_timeout_ms
measure latency
normalize HTTP success / failure
handle timeout without crashing
handle connection refused without crashing
return normalized result object
```

---

#### 3. Add connection health-test endpoint

Update:

```text
backend-django/connections/views.py
```
 
This creates the endpoint:

```text
POST /api/connections/{id}/test-health/
```

Behavior:

```text
loads ConnectionProfile by id
calls SpaghettiChef GET /health through services.py
stores one ProbeSample
returns connection summary and probe result
```

---

#### 4. Store result as `ProbeSample`

The endpoint creates a `ProbeSample` row here:

```python
probe_sample = ProbeSample.objects.create(
    method=probe_result.method,
    url=probe_result.url,
    status_code=probe_result.status_code,
    latency_ms=probe_result.latency_ms,
    timed_out=probe_result.timed_out,
    success=probe_result.success,
    error_message=probe_result.error_message,
)
```

Stored fields:

```text
method
url
status_code
latency_ms
timed_out
success
error_message
```

Not stored yet:

```text
response_json
```

Reason:

```text
ProbeSample is currently a lightweight technical measurement row.
The parsed JSON response is returned to the caller, but not persisted yet.
```

No report generation yet.

No Prometheus export yet.

---

#### 5. Test with curl

Make sure the backend is running:

```bash
python manage.py runserver 0.0.0.0:18090
```

Make sure the default connection exists:

```bash
python manage.py init_default_connection
```

List connections and take a valid {connection-id} in the list :

```bash
curl -fsS http://localhost:18090/api/connections/
```

Run health probe :

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/{connection-id}/test-health/
```

Check stored probe samples:

```bash
curl -fsS http://localhost:18090/api/probe-samples/
```
 

#### 6. Test health probe

Run backend:

```bash
python manage.py runserver 0.0.0.0:18090
```

Call:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/{connection-id}/test-health/
```

Check stored samples:

```bash
curl -fsS http://localhost:18090/api/probe-samples/
```

### Expected Result

If SpaghettiChef is running:

```json
{
  "connection": {
    "id": {connection-id},
    "name": "Local SpaghettiChef"
  },
  "probe": {
    "method": "GET",
    "url": "http://localhost:18080/health",
    "status_code": 200,
    "latency_ms": 12,
    "timed_out": false,
    "success": true,
    "error_message": ""
  }
}
```

If SpaghettiChef is not running:

```json
{
  "connection": {
    "id": {connection-id},
    "name": "Local SpaghettiChef"
  },
  "probe": {
    "method": "GET",
    "url": "http://localhost:18080/health",
    "status_code": null,
    "latency_ms": null,
    "timed_out": false,
    "success": false,
    "error_message": "Connection refused"
  }
}
```

### Acceptance Criteria

```text
requests dependency is installed
SpaghettiChef client service exists
POST /api/connections/{id}/test-health/ exists
endpoint calls configured base_url + health_path
endpoint applies configured request_timeout_ms
endpoint measures latency
endpoint handles connection refused without crashing
endpoint handles timeout without crashing
endpoint stores one ProbeSample per call
GET /api/probe-samples/ shows stored health probe result
no .env value is required for target URL
no Prometheus export is implemented yet
```

### Suggested Commit

```bash
git status
git add .
git commit -m '0.3.0 Add SpaghettiChef health connection probe'
```

---
 
## TODO(DONE) 0.3.1 — SpaghettiChef Version Probe

### Purpose

Add a second black-box probe against SpaghettiChef.

This step tests one configured SpaghettiChef connection by calling:

```text
GET /version
```

BenchChef must measure latency, normalize the result, store it as a `ProbeSample`, and return the parsed version response when available.
 

### Work To Do

#### 1. Refactor service to support generic GET probes

Update:

```text
backend-django/connections/services.py
```
 
#### 2. Add reusable ProbeSample creation helper

Update:

```text
backend-django/connections/views.py
```
 

#### 3. Verify SpaghettiChef version endpoint directly

Make sure SpaghettiChef is running on the configured port.

Example:

```bash
curl -fsS http://localhost:18080/version
```

Expected result depends on SpaghettiChef, but should be JSON or text response with version information.

#### 4. Test BenchChef version probe

Start BenchChef backend:

```bash
python manage.py runserver 0.0.0.0:18090
```

Call:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-version/
```

Use the actual `ConnectionProfile.id` from:

```bash
curl -fsS http://localhost:18090/api/connections/
```

#### 5. Check stored probe samples

```bash
curl -fsS http://localhost:18090/api/probe-samples/
```

You should see a new row for:

```text
GET http://localhost:18080/version
```

### Expected Result

If SpaghettiChef is running:

```json
{
  "connection": {
    "id": 3,
    "name": "Local SpaghettiChef",
    "base_url": "http://localhost:18080"
  },
  "probe": {
    "id": 5,
    "method": "GET",
    "url": "http://localhost:18080/version",
    "status_code": 200,
    "latency_ms": 4,
    "timed_out": false,
    "success": true,
    "error_message": "",
    "response_json": {
      "version": "1.0.5"
    }
  }
}
```

If SpaghettiChef is not running:

```json
{
  "connection": {
    "id": 3,
    "name": "Local SpaghettiChef",
    "base_url": "http://localhost:18080"
  },
  "probe": {
    "id": 6,
    "method": "GET",
    "url": "http://localhost:18080/version",
    "status_code": null,
    "latency_ms": 0,
    "timed_out": false,
    "success": false,
    "error_message": "Connection refused or target unreachable",
    "response_json": null
  }
}
```

### Acceptance Criteria

```text
generic probe_get service exists
probe_health still works after refactor
probe_version exists
POST /api/connections/{id}/test-version/ exists
endpoint calls configured base_url + version_path
endpoint applies configured request_timeout_ms
endpoint measures latency
endpoint handles connection refused without crashing
endpoint handles timeout without crashing
endpoint stores one ProbeSample per call
GET /api/probe-samples/ shows stored version probe result
health probe still works
no Prometheus export is implemented yet
```

### Suggested Commit

```bash
git add .
git status
git commit -m '0.3.1 - Add SpaghettiChef version connection probe'
```
 
 
## TODO(DONE) 0.3.2–0.3.6 — Extended SpaghettiChef Read-Only Probes


### Scope

This step adds:

```text
GET /monitoring probe
GET /dashboard/index.html probe
GET /printers/{printerId}/camera/jobs/active probe
GET /admin/printers/{printerId}/camera/jobs/{cameraJobId}/progress probe
GET /admin/printers/{printerId}/camera/jobs/{cameraJobId}/timeline probe
```

BenchChef stores each call as a `ProbeSample`.

No Prometheus export yet.

No report generation yet.

No Angular integration yet.

---

### Code impact :

- `backend-django/connections/services.py`
- `backend-django/connections/views.py`
 

---

### Test commands

Use the real connection id from:

```bash
curl -fsS http://localhost:18090/api/connections/
```

Example below assumes:

```text
ConnectionProfile.id = 3
```

#### Monitoring probe

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-monitoring/
```

#### Dashboard index probe

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-dashboard-index/
```

#### Camera active job probe

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-camera-active-job/ \
  -H 'Content-Type: application/json' \
  -d '{
    "printer_id": "pex01"
  }'
```

#### Camera job progress probe

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-camera-job-progress/ \
  -H 'Content-Type: application/json' \
  -d '{
    "printer_id": "pex01",
    "camera_job_id": "1"
  }'
```

#### Camera job timeline probe

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-camera-job-timeline/ \
  -H 'Content-Type: application/json' \
  -d '{
    "printer_id": "pex01",
    "camera_job_id": "1"
  }'
```

#### Check stored probe samples

```bash
curl -fsS http://localhost:18090/api/probe-samples/
```

---

### Notes

If a SpaghettiChef endpoint does not exist yet, BenchChef should still store the result.

Example:

```text
status_code = 404
success = false
```

That is not a BenchChef bug. It means the observed SpaghettiChef endpoint is not available.

### Acceptance Criteria

```text
health probe still works
version probe still works
monitoring probe works
dashboard index probe works
camera active-job probe accepts printer_id
camera job progress probe accepts printer_id and camera_job_id
camera job timeline probe accepts printer_id and camera_job_id
each probe stores one ProbeSample
connection refused is handled without crashing
timeout is handled without crashing
HTTP 404 is stored as failed ProbeSample, not as backend crash
no Prometheus export is implemented yet
no report generation is implemented yet
```

### Suggested Commit

```bash
git status
git add .
git commit -m '0.3.2 bis 0.3.6 Add extended SpaghettiChef read-only probes'
```
0.3.5 = implemented, expected 404 until SpaghettiChef 0.8.1


---

## TODO(DONE) 0.3.7 — Timeout And Error Normalization

### Purpose

Make probe failures readable and stable.

Before this step, some failed probes may store long low-level Python or `requests` exception messages.

After this step, BenchChef should store normalized probe errors such as:

```text
TIMEOUT
CONNECTION_REFUSED
HTTP_ERROR
INVALID_JSON
REQUEST_ERROR
```

This makes probe results easier to read in Django admin, API responses, Angular, and later reports.

### Scope

This step updates the probe service layer only.

It does not add new probe endpoints.

It does not add Prometheus export.

It does not add report generation.

### Work To Do

#### 1. Define normalized error categories

Use these categories:

```text
NONE
TIMEOUT
CONNECTION_REFUSED
HTTP_ERROR
INVALID_JSON
REQUEST_ERROR
```

Meaning:

```text
NONE
successful HTTP request with acceptable response

TIMEOUT
target did not respond before request_timeout_ms

CONNECTION_REFUSED
host/port unreachable or connection refused

HTTP_ERROR
target answered but returned non-2xx status code

INVALID_JSON
target answered with 2xx but response body was expected to be JSON and could not be parsed

REQUEST_ERROR
other request-layer failure
```

#### 2. Decide what is stored in `ProbeSample`

Keep the existing `ProbeSample` model for now.

Store the normalized category in:

```text
error_message
```

Examples:

```text
TIMEOUT: Request timed out
CONNECTION_REFUSED: Target unreachable
HTTP_ERROR: HTTP 404
INVALID_JSON: Response is not valid JSON
REQUEST_ERROR: Unexpected request failure
```

No model migration is required for this step.

Later, if needed, BenchChef can add a dedicated `error_type` field.

#### 3. Update `connections/services.py`

Replace the probe service implementation so that:

```text
connection refused does not store the full requests stack-like message
timeout is clearly marked
HTTP 404/500 is stored as HTTP_ERROR
2xx HTML response is still success for dashboard index
JSON parse failure does not break dashboard index probes
latency_ms is always measured
```

Important rule:

```text
A non-JSON response is not always an error.
```

For example:

```text
/dashboard/index.html
```

returns HTML, so `response_json = null` is normal.

#### 4. Add JSON expectation flag

Update the generic GET probe so it can distinguish:

```text
JSON endpoint
HTML/static endpoint
```

Recommended function signature:

```python
def probe_get(
    connection: ConnectionProfile,
    path: str,
    expect_json: bool = True,
) -> ProbeResult:
```

Use:

```text
expect_json=True
```

for:

```text
/health
/version
/monitoring
camera JSON endpoints
```

Use:

```text
expect_json=False
```

for:

```text
/dashboard/index.html
```

#### 5. Update dashboard probe

Update:

```python
def probe_dashboard_index(connection: ConnectionProfile) -> ProbeResult:
    return probe_get(
        connection,
        connection.dashboard_index_path,
        expect_json=False,
    )
```

This prevents HTML dashboard response from being treated as invalid JSON.

#### 6. Keep failed HTTP responses as stored probe samples

For HTTP 404, 500, etc.:

```text
status_code = real HTTP status code
success = false
timed_out = false
error_message = HTTP_ERROR: HTTP 404
```

This is important because a 404 from SpaghettiChef is still a valid observation.

BenchChef should not crash.

#### 7. Test success case

Start SpaghettiChef and BenchChef.

Run:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-health/
```

Expected:

```text
status_code = 200
success = true
error_message = ''
response_json is present
```

#### 8. Test dashboard HTML case

Run:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-dashboard-index/
```

Expected:

```text
status_code = 200
success = true
error_message = ''
response_json = null
```

This is correct because the dashboard returns HTML.

#### 9. Test connection refused case

Stop SpaghettiChef or change the connection profile to an unused port.

Run:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-health/
```

Expected:

```text
status_code = null
success = false
timed_out = false
error_message = CONNECTION_REFUSED: Target unreachable
```

#### 10. Test HTTP error case

Call a future/not-yet-implemented endpoint such as camera progress when SpaghettiChef returns 404:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-camera-job-progress/ \
  -H 'Content-Type: application/json' \
  -d '{
    "printer_id": "lux01",
    "camera_job_id": "3"
  }'
```

Expected until SpaghettiChef implements this endpoint:

```text
status_code = 404
success = false
timed_out = false
error_message = HTTP_ERROR: HTTP 404
```

#### 11. Verify stored probe samples

Run:

```bash
curl -fsS http://localhost:18090/api/probe-samples/
```

Check that stored rows have readable error messages.

Also verify in Django admin:

```text
http://localhost:18090/admin
```

### Acceptance Criteria

```text
timeout errors are normalized
connection refused errors are normalized
HTTP 4xx/5xx errors are normalized
dashboard HTML response is accepted
invalid JSON does not crash the probe
latency_ms is still stored
status_code is still stored when available
ProbeSample rows remain readable in Django admin
existing health probe still works
existing version probe still works
existing monitoring probe still works
existing dashboard probe still works
existing camera probes still work
no database migration is required
```

### Suggested Commit

```bash
git status
git add .
git commit -m 'Normalize probe timeout and error handling'
```
 
---

## TODO(DONE) 0.3.8 — Connection Diagnostics Endpoint

### Purpose

Add one endpoint that runs several read-only SpaghettiChef probes together.

This endpoint gives BenchChef a simple connection diagnosis:

```text
ONLINE
DEGRADED
OFFLINE
````

### Work To Do

* add diagnostics endpoint
* run health, version, monitoring, and dashboard probes together
* store one `ProbeSample` per probe
* return combined status
* do not add Prometheus export yet
* do not add Angular integration yet

````

impact :

```text
backend-django/connections/views.py
``` 

Test:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/diagnostics/
```

Check stored samples:

```bash
curl -fsS http://localhost:18090/api/probe-samples/
```

Expected if SpaghettiChef is running:

```text
diagnostic_status = ONLINE
```

Suggested commit:

```bash
git status
git add .
git commit -m 'Add connection diagnostics endpoint'
```
