# TODO 0.3.x - Connection to SpaghettiChef
## TODO 0.3.0 — SpaghettiChef Health Connection Probe

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
 
## TODO 0.3.1 — SpaghettiChef Version Probe

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
 
