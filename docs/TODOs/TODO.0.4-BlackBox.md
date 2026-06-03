# 0.4.x TODO — Black-Box Performance Probes



## TODO(DONE) 0.4.x — Backend Implementation

### Purpose

Turn the existing probe calls into measurable black-box performance data.

This step adds:

- probe type classification
- repeated probe execution
- diagnostics history under `BenchmarkRun`
- dashboard responsiveness scenario
- camera active-job polling scenario
- progress/timeline probes kept as planned endpoint probes
- latency summary API
- error summary API
- basic slowdown/trend summary API

No SpaghettiChef code is changed.

No Prometheus export yet.

No Grafana dashboard yet.

No Angular integration yet.

---

## Impacted Files

```text
backend-django/probes/models.py
backend-django/probes/admin.py
backend-django/probes/serializers.py
backend-django/probes/views.py

backend-django/connections/views.py
````

No change needed in:

```text
backend-django/connections/services.py
```

unless your current file is not the normalized 0.3.7 version.

---

## 1. `backend-django/probes/models.py`
## 2. `backend-django/probes/admin.py`
## 3. `backend-django/probes/serializers.py`
## 4. `backend-django/probes/views.py`
## 5. `backend-django/connections/views.py`



## 6. Run migrations

```bash
cd ~/coding/github/bench-chef/backend-django
source .venv/bin/activate

python manage.py makemigrations
python manage.py migrate
```

---

## 7. Start backend

```bash
python manage.py runserver 0.0.0.0:18090
```

---

## 8. Test existing probes still work

Use your real connection id. Example: `3`.

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-health/
```

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/test-dashboard-index/
```

---

## 9. Test repeated probe execution

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/repeat-probe/ \
  -H 'Content-Type: application/json' \
  -d '{
    "probe_type": "HEALTH_PROBE",
    "repeat_count": 5,
    "delay_ms": 200
  }'
```

---

## 10. Test diagnostics history

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/diagnostics-history/ \
  -H 'Content-Type: application/json' \
  -d '{
    "repeat_count": 3,
    "delay_ms": 500
  }'
```

---

## 11. Test dashboard responsiveness

```bash
curl -fsS \
  -X POST \
  http://localhost:18090/api/connections/3/dashboard-responsiveness/ \
  -H 'Content-Type: application/json' \
  -d '{
    "repeat_count": 10,
    "delay_ms": 100
  }'
```

---

## 12. Test camera active-job polling

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

---

## 13. Test planned progress endpoint remains black-box

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

Expected until SpaghettiChef 0.8.1 implements it:

```text
status_code = 404
success = false
error_message = HTTP_ERROR: HTTP 404
```

---

## 14. Test latency summary API

```bash
curl -fsS \
  'http://localhost:18090/api/probe-samples/latency-summary/?probe_type=HEALTH_PROBE'
```

---

## 15. Test error summary API

```bash
curl -fsS \
  'http://localhost:18090/api/probe-samples/error-summary/'
```

---

## 16. Test slowdown summary API

```bash
curl -fsS \
  'http://localhost:18090/api/probe-samples/slowdown-summary/?probe_type=HEALTH_PROBE'
```

---

## Acceptance Criteria

```text
ProbeSample stores probe_type
ProbeSample can link to ConnectionProfile
ProbeSample can link to BenchmarkRun
ProbeSample stores response_json
all existing single probes still work
repeat-probe endpoint works
diagnostics-history endpoint works
dashboard-responsiveness endpoint works
camera-active-job-polling endpoint works
latency-summary endpoint works
error-summary endpoint works
slowdown-summary endpoint works
missing SpaghettiChef progress/timeline endpoints are stored as normal HTTP_ERROR: HTTP 404 samples
no white-box access is used
no SpaghettiChef filesystem is read
no SpaghettiChef SQLite is read
no Prometheus export is implemented yet
```

---

## Suggested Commit

```bash
git add .
git status
git commit -m '0.4 Add black-box performance probe foundation'
```
 