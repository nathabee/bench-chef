# 0.2.x TODO  BenchChef Backend Domain Foundation

## TODO 0.2.0 — Connection Profile Foundation

### Purpose

Create the first persistent backend domain layer for BenchChef.

This step introduces the connection configuration model used to describe a target SpaghettiChef runtime.

### Work To Do


#### 0. Create superuser django admin

 

```bash
python manage.py createsuperuser
# start server:


python manage.py runserver 0.0.0.0:18090
```

Open:

```text
http://localhost:18090/admin
```

and login with the credentials you created.




#### 1. Use existing Django apps

Apps already created:

```text
connections
probes
benchmarks
reports
```

This step focuses primarily on the `connections` app.

#### 2. Add `ConnectionProfile` model

Create:

```text
backend-django/connections/models.py
```

Add a first model representing a SpaghettiChef connection configuration.

Suggested fields:

```text
name
base_url
role_header
enabled
created_at
updated_at
```

 

Example intent:

```text
BenchChef Local Runtime
http://localhost:18080
ADMIN
enabled=true
```

#### 3. Create database migration

After each models.py change, run :
```bash
cd backend-django 
source .venv/bin/activate

python manage.py makemigrations
python manage.py migrate
```

#### 4. Register model in Django admin

Create or update:

```text
backend-django/connections/admin.py
```

Register:

```text
ConnectionProfile
```

The model should become visible in:

```text
/admin
```

#### 5. Add serializer

Create:

```text
backend-django/connections/serializers.py
```

Add:

```text
ConnectionProfileSerializer
```

#### 6. Add REST API views

Create:

```text
backend-django/connections/views.py
```

Add basic API endpoints for:

```text
connection profile list
connection profile detail
```

#### 7. Register API routes

Create:

```text
backend-django/connections/urls.py
```

Expose routes similar to:

```text
GET    /api/connections
POST   /api/connections
GET    /api/connections/{id}
PUT    /api/connections/{id}
DELETE /api/connections/{id}
```

Register the app URLs in:

```text
backend-django/benchchef/urls.py
```




#### 8. Verify API behavior

Start backend:

```bash
python manage.py runserver 0.0.0.0:18090
```

Test:

```bash
curl -fsS http://localhost:18090/api/connections
```

Expected:

```text
valid JSON response
```

### Acceptance Criteria

```text
ConnectionProfile model exists
database migration succeeds
model visible in Django admin
serializer exists
REST endpoints exist
GET /api/connections works
POST /api/connections works
backend starts successfully
```


Use this small full CRUD test sequence, to routes similar to:

```text
GET    /api/connections
POST   /api/connections
GET    /api/connections/{id}
PUT    /api/connections/{id}
DELETE /api/connections/{id}
```

#### 1. GET — list connections

Should return an array.

```bash
curl -fsS http://localhost:18090/api/connections/
```

Expected initially:

```json
[]
```

or existing objects.

---

#### 2. POST — create connection

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/ \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Local SpaghettiChef",
    "base_url": "http://localhost:18080",
    "role_header": "ADMIN",
    "enabled": true
  }'
```

Expected:

```json
{
  "id": 1,
  "name": "Local SpaghettiChef",
  ...
}
```

Note the returned `id`.

---

### 3. GET — list again

Verify persistence.

```bash
curl -fsS http://localhost:18090/api/connections/
```

Should now contain your created profile.

---

### 4. GET — detail by id

Replace `1` if needed.

```bash
curl -fsS http://localhost:18090/api/connections/1/
```

Expected:

```json
{
  "id": 1,
  "name": "Local SpaghettiChef",
  ...
}
```

---

#### 5. PUT — full update

```bash
curl -fsS \
  -X PUT \
  http://localhost:18090/api/connections/1/ \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Local SpaghettiChef Updated",
    "base_url": "http://localhost:18180",
    "role_header": "OPERATOR",
    "enabled": false
  }'
```

Then verify:

```bash
curl -fsS http://localhost:18090/api/connections/1/
```

---

#### 6. DELETE — remove object

```bash
curl -fsS \
  -X DELETE \
  http://localhost:18090/api/connections/1/
```

Expected:

```text
empty response
```

---

#### 7. Final GET — verify deletion

```bash
curl -fsS http://localhost:18090/api/connections/
```

Should be empty again.

If all 7 work, your **0.2.0 CRUD layer is proven**.



### Suggested Commit

```bash
git status
git add .
git commit -m '0.2.0 - Add connection profile foundation'
```


 
## TODO 0.2.1 — Probe Sample Foundation

### Purpose

Add the first model for storing black-box probe measurements.

A `ProbeSample` represents one observed HTTP request made by BenchChef against an external target, usually SpaghettiChef.

This step stores probe results only. It does not yet execute probes automatically.

### Work To Do

#### 1. Add `ProbeSample` model

Create or replace:

```text
backend-django/probes/models.py
```
 

#### 2. Create and apply migration

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 3. Register model in Django admin

Create or replace:

```text
backend-django/probes/admin.py
```
 

#### 4. Add serializer

Create:

```text
backend-django/probes/serializers.py
```
 

#### 5. Add REST API views

Create or replace:

```text
backend-django/probes/views.py
```
 

#### 6. Add app routes

Create:

```text
backend-django/probes/urls.py
```
 

#### 7. Register routes in project URLs

Update:

```text
backend-django/benchchef/urls.py
```
 

#### 8. Verify API behavior

Start backend:

```bash
python manage.py runserver 0.0.0.0:18090
```

List samples:

```bash
curl -fsS http://localhost:18090/api/probe-samples/
```

Create sample:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/probe-samples/ \
  -H 'Content-Type: application/json' \
  -d '{
    "method": "GET",
    "url": "http://localhost:18080/health",
    "status_code": 200,
    "latency_ms": 42,
    "timed_out": false,
    "success": true,
    "error_message": ""
  }'
```

Detail sample:

```bash
curl -fsS http://localhost:18090/api/probe-samples/1/
```

Update sample:

```bash
curl -fsS \
  -X PUT \
  http://localhost:18090/api/probe-samples/1/ \
  -H 'Content-Type: application/json' \
  -d '{
    "method": "GET",
    "url": "http://localhost:18080/health",
    "status_code": 503,
    "latency_ms": 1500,
    "timed_out": false,
    "success": false,
    "error_message": "Service unavailable"
  }'
```

Delete sample:

```bash
curl -fsS \
  -X DELETE \
  http://localhost:18090/api/probe-samples/1/
```

### Acceptance Criteria

```text
ProbeSample model exists
database migration succeeds
model visible in Django admin
serializer exists
REST endpoints exist
GET /api/probe-samples/ works
POST /api/probe-samples/ works
GET /api/probe-samples/{id}/ works
PUT /api/probe-samples/{id}/ works
DELETE /api/probe-samples/{id}/ works
sample stores URL, method, status code, latency, timeout state, success state, error message
backend starts successfully
```

### Suggested Commit

```bash
git status
git add .
git commit -m '0.2.1 - Add probe sample foundation'
```
 
---
## TODO 0.2.2 — Benchmark Run Foundation

### Purpose

Add the first persistent model for BenchChef benchmark runs.

A `BenchmarkRun` represents one planned, running, completed, failed, or cancelled benchmark scenario.

This step stores benchmark run metadata only. It does not yet execute benchmark scenarios.

### Work To Do

#### 1. Add `BenchmarkRun` model

Create or replace:

```text
backend-django/benchmarks/models.py
```
 

#### 2. Create and apply migration

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 3. Register model in Django admin

Create or replace:

```text
backend-django/benchmarks/admin.py
```
 

#### 4. Add serializer

Create:

```text
backend-django/benchmarks/serializers.py
```
  

#### 5. Add REST API views

Create or replace:

```text
backend-django/benchmarks/views.py
```
 

#### 6. Add app routes

Create:

```text
backend-django/benchmarks/urls.py
```
 

#### 7. Register routes in project URLs

Update:

```text
backend-django/benchchef/urls.py
```

 

#### 8. Verify API behavior

Start backend:

```bash
python manage.py runserver 0.0.0.0:18090
```

List benchmark runs:

```bash
curl -fsS http://localhost:18090/api/benchmark-runs/
```

Create benchmark run:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/benchmark-runs/ \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Health endpoint smoke benchmark",
    "scenario_name": "HEALTH_PROBE",
    "status": "CREATED",
    "target_base_url": "http://localhost:18080",
    "message": "Initial benchmark run placeholder"
  }'
```

Detail benchmark run:

```bash
curl -fsS http://localhost:18090/api/benchmark-runs/1/
```

Update benchmark run:

```bash
curl -fsS \
  -X PUT \
  http://localhost:18090/api/benchmark-runs/1/ \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Health endpoint smoke benchmark",
    "scenario_name": "HEALTH_PROBE",
    "status": "COMPLETED",
    "target_base_url": "http://localhost:18080",
    "started_at": "2026-06-02T12:00:00Z",
    "finished_at": "2026-06-02T12:01:00Z",
    "message": "Placeholder run completed manually"
  }'
```

Delete benchmark run:

```bash
curl -fsS \
  -X DELETE \
  http://localhost:18090/api/benchmark-runs/1/
```

### Acceptance Criteria

```text
BenchmarkRun model exists
status lifecycle exists: CREATED, QUEUED, RUNNING, COMPLETED, FAILED, CANCELLED
database migration succeeds
model visible in Django admin
serializer exists
REST endpoints exist
GET /api/benchmark-runs/ works
POST /api/benchmark-runs/ works
GET /api/benchmark-runs/{id}/ works
PUT /api/benchmark-runs/{id}/ works
DELETE /api/benchmark-runs/{id}/ works
backend starts successfully
no benchmark execution logic is implemented yet
```

### Suggested Commit

```bash
git status
git add .
git commit -m '0.2.3 - Add benchmark run foundation'
```
 

---

## TODO 0.2.3 — Report Record Foundation

### Purpose

Add the first persistent model for BenchChef report metadata.

A `ReportRecord` represents a generated or planned benchmark report.

This step stores report metadata only. It does not yet generate report files.

### Work To Do

#### 1. Add `ReportRecord` model

Create or replace:

```text
backend-django/reports/models.py
```
 

#### 2. Create and apply migration

```bash
cd ~/coding/github/bench-chef/backend-django
source .venv/bin/activate

python manage.py makemigrations
python manage.py migrate
```

#### 3. Register model in Django admin

Create or replace:

```text
backend-django/reports/admin.py
```
 

#### 4. Add serializer

Create:

```text
backend-django/reports/serializers.py
```
 

#### 5. Add REST API views

Create or replace:

```text
backend-django/reports/views.py
```
 

#### 6. Add app routes

Create:

```text
backend-django/reports/urls.py
```
 

#### 7. Register routes in project URLs

Update:

```text
backend-django/benchchef/urls.py
```

Add:

```python
path('api/', include('reports.urls')),
```

 

#### 8. Verify API behavior

Start backend:

```bash
python manage.py runserver 0.0.0.0:18090
```

List report records:

```bash
curl -fsS http://localhost:18090/api/report-records/
```

Create report record:

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/report-records/ \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Health Probe Smoke Report",
    "report_type": "PROBE",
    "status": "CREATED",
    "output_format": "MARKDOWN",
    "file_path": "reports/health-probe-smoke-report.md",
    "message": "Initial report placeholder"
  }'
```

Detail report record:

```bash
curl -fsS http://localhost:18090/api/report-records/1/
```

Update report record:

```bash
curl -fsS \
  -X PUT \
  http://localhost:18090/api/report-records/1/ \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Health Probe Smoke Report",
    "report_type": "PROBE",
    "status": "READY",
    "output_format": "MARKDOWN",
    "file_path": "reports/health-probe-smoke-report.md",
    "message": "Report metadata marked ready manually"
  }'
```

Delete report record:

```bash
curl -fsS \
  -X DELETE \
  http://localhost:18090/api/report-records/1/
```

### Browser Verification

Open Django admin:

```text
http://localhost:18090/admin
```

Check:

```text
Report records is visible
you can add a report record
you can save it
it appears in the list
```

Example values:

```text
Title: Health Probe Smoke Report
Report type: Probe
Status: Created
Output format: Markdown
File path: reports/health-probe-smoke-report.md
Message: Initial report placeholder
```

### Acceptance Criteria

```text
ReportRecord model exists
database migration succeeds
model visible in Django admin
serializer exists
REST endpoints exist
GET /api/report-records/ works
POST /api/report-records/ works
GET /api/report-records/{id}/ works
PUT /api/report-records/{id}/ works
DELETE /api/report-records/{id}/ works
record stores title, report type, status, output format, file path, message
backend starts successfully
no report generation logic is implemented yet
```

### Suggested Commit

```bash
git status
git add .
git commit -m '0.2.3 - Add report record foundation'
```
 
---
## TODO 0.2.4 — Connection Probe Configuration

### Purpose

Extend `ConnectionProfile` so BenchChef can store the SpaghettiChef target configuration in the database.

This allows the connection to be edited in Django admin now, and later from the Angular UI.

`.env` should only provide optional defaults. The real active connection should be stored in `ConnectionProfile`.

### Work To Do

#### 1. Extend `ConnectionProfile`

Update:

```text
backend-django/connections/models.py
````

 

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

 

#### 4. Update Django admin

Update:

```text
backend-django/connections/admin.py
```

Add these fields to `list_display`:

```text
health_path
request_timeout_ms
```

Add these fields to editable admin form through `fieldsets` or normal model fields:

```text
health_path
version_path
monitoring_path
dashboard_index_path
request_timeout_ms
```

#### 5. Verify in Django admin

Start backend:

```bash
python manage.py runserver 0.0.0.0:18090
```

Open:

```text
http://localhost:18090/admin
```

Edit or create a connection profile:

```text
Name: Local SpaghettiChef
Base url: http://localhost:18080
Role header: ADMIN
Enabled: checked
Health path: /health
Version path: /version
Monitoring path: /monitoring
Dashboard index path: /dashboard/index.html
Request timeout ms: 3000
```

#### 6. Verify through API

List connections:

```bash
curl -fsS http://localhost:18090/api/connections/
```

Create a connection if needed:

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
    "version_path": "/version",
    "monitoring_path": "/monitoring",
    "dashboard_index_path": "/dashboard/index.html",
    "request_timeout_ms": 3000
  }'
```
 
#### 7. Add default connection initialization command

Create folders:

```bash
mkdir -p connections/management/commands
touch connections/management/__init__.py
touch connections/management/commands/__init__.py
````

Create:

```text
backend-django/connections/management/commands/init_default_connection.py
```
 
Run:

```bash
python manage.py init_default_connection
```

Verify:

```bash
curl -fsS http://localhost:18090/api/connections/
```

Expected: one default line exists:

```text
Local SpaghettiChef
http://localhost:18080
```

### Acceptance Criteria

```text
management command init_default_connection exists
command creates or updates Local SpaghettiChef profile
command is idempotent
default connection appears in Django admin
default connection appears in GET /api/connections/
ConnectionProfile stores health_path
ConnectionProfile stores version_path
ConnectionProfile stores monitoring_path
ConnectionProfile stores dashboard_index_path
ConnectionProfile stores request_timeout_ms
Django migration succeeds
Django admin shows the new fields
REST serializer exposes the new fields
GET /api/connections/ returns the new fields
POST /api/connections/ accepts the new fields
SpaghettiChef target can be configured without editing .env
```


### Suggested Commit

```bash
git status
git add .
git commit -m '0.2.4 - Add connection probe configuration'
```
  