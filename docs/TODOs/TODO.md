TODO overviews

---

## TODO 0.1.x — Project Foundation

### TODO 0.1.0 — Repository Skeleton
- create repository benchchef
- create backend-django/
- create frontend-angular/
- create prometheus/
- create grafana/
- create scenarios/
- create reports/
- create docs/
- add docker-compose.yml
- add README.md
- add .env.example
- add .gitignore
- commit skeleton

### TODO 0.1.1 — Django Backend Bootstrap
- create Python virtual environment in backend-django/
- install Django
- install Django REST Framework
- create Django project
backend-django/
├── benchchef/          # Django project config: settings, urls, wsgi/asgi
├── accounts/           # later: users, roles, authentication
├── connections/        # SpaghettiChef connection profiles
├── probes/             # black-box HTTP probes and probe samples
├── benchmarks/         # benchmark runs, scenarios, run status
├── reports/            # generated reports and exports
└── manage.py
- add requirements.txt
- add backend .env.example if needed
- add GET /api/health
- verify python manage.py runserver works
- commit Django bootstrap

### TODO 0.1.2 — Angular Frontend Bootstrap
- create Angular app inside frontend-angular/
- add base layout
- add app title BenchChef
- add placeholder navigation
- add placeholder pages:
  - Dashboard
  - Connections
  - Probes
  - Benchmarks
  - Reports
  - Settings
- verify npm start works
- commit Angular bootstrap

### TODO 0.1.3 — Local Stack Smoke Test
- add basic Prometheus config
- add basic Grafana provisioning folders
- make docker compose start Prometheus and Grafana
- verify Prometheus opens on 9090
- verify Grafana opens on 3000
- document local startup commands
- commit monitoring stack bootstrap

---


## TODO 0.2.x BenchChef Backend Domain Foundation

### TODO 0.2.0
- create Django apps: connections, probes, benchmarks, reports
- add ConnectionProfile model
- add Django admin registration
- add serializers
- add basic REST endpoints

### TODO 0.2.1
- add ProbeSample model
- store URL, method, status code, latency, timeout, error message
- expose probe samples through API

### TODO 0.2.2
- add BenchmarkRun model
- add BenchmarkRun status lifecycle
- expose benchmark run list/detail API

### TODO 0.2.3
- add ReportRecord model
- store title, report type, status, output format, file path, message
- add Django admin registration
- add serializer
- expose report record list/detail API

### TODO 0.2.4
- extend ConnectionProfile for probe configuration
- store request timeout, health path, version path, monitoring path
- make connection settings editable from Django admin
- keep `.env` only for optional defaults

 
## TODO 0.3.x SpaghettiChef Connection

### TODO 0.3.0
- add backend service for SpaghettiChef HTTP calls
- use ConnectionProfile as target configuration
- call GET /health
- measure latency
- store result as ProbeSample
- expose connection test endpoint

### TODO 0.3.1
- add GET /version probe
- store version response
- store HTTP status, latency, success, timeout, error message
- expose version probe result through API

### TODO 0.3.2
- add GET /monitoring probe
- store monitoring response summary
- store HTTP status, latency, success, timeout, error message
- expose monitoring probe result through API

### TODO 0.3.3
- add dashboard asset probe
- call GET /dashboard/index.html
- measure dashboard response time
- store result as ProbeSample
- expose dashboard probe result through API

### TODO 0.3.4
- add camera job active probe
- call GET /printers/{printerId}/camera/jobs/active
- support printerId input
- store result as ProbeSample
- expose camera active-job probe result through API

### TODO 0.3.5
- add camera job progress probe
- call GET /admin/printers/{printerId}/camera/jobs/{cameraJobId}/progress
- support printerId and cameraJobId input
- store result as ProbeSample
- expose camera progress probe result through API

### TODO 0.3.6
- add camera job timeline probe
- call GET /admin/printers/{printerId}/camera/jobs/{cameraJobId}/timeline
- support printerId and cameraJobId input
- store result as ProbeSample
- expose camera timeline probe result through API

### TODO 0.3.7
- add timeout and error normalization
- define default request timeout
- distinguish timeout, connection refused, HTTP error, invalid JSON
- store normalized error message in ProbeSample

### TODO 0.3.8
- add basic connection diagnostics endpoint
- run health, version, monitoring, and dashboard probes together
- return combined online/offline/degraded status
- store individual ProbeSample rows
 