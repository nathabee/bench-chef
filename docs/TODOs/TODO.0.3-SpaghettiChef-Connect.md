## TODO 0.3.x  — SpaghettiChef Connection
## TODO 0.3.0 — SpaghettiChef Health Connection Probe

### Purpose

Implement the first real BenchChef black-box probe against SpaghettiChef.

This step tests one configured SpaghettiChef connection by calling:

```text
GET /health
````

BenchChef must measure latency, normalize the result, and store it as a `ProbeSample`.

### Design Decision

Connection configuration is stored in Django through `ConnectionProfile`.

Use `.env` only for optional local defaults.

Reason:

```text
ConnectionProfile can be edited in Django admin
later it can be edited from Angular
multiple SpaghettiChef targets can be supported
BenchChef does not require code changes for another IP/port
```

### Work To Do

#### 1. Extend `ConnectionProfile`

Update:

```text
backend-django/connections/models.py
```

Add fields:

```text
health_path
request_timeout_ms
```

Recommended defaults:

```text
health_path = /health
request_timeout_ms = 3000
```

#### 2. Create and apply migration

```bash
cd ~/coding/github/bench-chef/backend-django
source .venv/bin/activate

python manage.py makemigrations
python manage.py migrate
```

#### 3. Update serializer

Update:

```text
backend-django/connections/serializers.py
```

Expose:

```text
health_path
request_timeout_ms
```

#### 4. Update Django admin

Update:

```text
backend-django/connections/admin.py
```

Show and edit:

```text
base_url
role_header
health_path
request_timeout_ms
enabled
```

#### 5. Add HTTP client dependency

Use `requests` for the first implementation.

```bash
pip install requests
pip freeze > requirements.txt
```

#### 6. Add SpaghettiChef client service

Create:

```text
backend-django/connections/services.py
```

Responsibilities:

```text
build full URL from base_url + health_path
call GET /health
apply timeout
measure latency
return normalized result
do not crash on connection errors
```

The service should return:

```text
url
method
status_code
latency_ms
timed_out
success
error_message
response_json, if available
```

#### 7. Add connection test endpoint

In:

```text
backend-django/connections/views.py
```

Add a custom action:

```text
POST /api/connections/{id}/test-health/
```

Behavior:

```text
load ConnectionProfile
call SpaghettiChef GET /health
store ProbeSample
return connection profile + probe result
```

#### 8. Store result as `ProbeSample`

The created `ProbeSample` should store:

```text
method = GET
url = full health URL
status_code
latency_ms
timed_out
success
error_message
```

No report generation yet.

No Prometheus export yet.

#### 9. Test with curl

Create or verify a connection profile:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/ \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Local SpaghettiChef",
    "base_url": "http://localhost:18080",
    "role_header": "ADMIN",
    "enabled": true,
    "health_path": "/health",
    "request_timeout_ms": 3000
  }'
```

Run health test:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/1/test-health/
```

Check stored probe samples:

```bash
curl -fsS http://localhost:18090/api/probe-samples/
```

### Expected Result

If SpaghettiChef is running:

```json
{
  "connection": {
    "id": 1,
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
    "id": 1,
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
ConnectionProfile stores health_path
ConnectionProfile stores request_timeout_ms
Django admin can edit health_path and request_timeout_ms
serializer exposes new fields
POST /api/connections/{id}/test-health/ exists
endpoint calls SpaghettiChef GET /health
endpoint measures latency
endpoint handles connection refused without crashing
endpoint handles timeout without crashing
endpoint stores one ProbeSample per call
GET /api/probe-samples/ shows stored health probe result
.env is not required for connection target configuration
```

### Suggested Commit

```bash
git status
git add .
git commit -m 'Add SpaghettiChef health connection probe'
```

```
```
