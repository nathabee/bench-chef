# 0.1.x TODO



## TODO 0.1.0 — BenchChef Repository Skeleton

### Purpose

Create the clean BenchChef repository structure.

BenchChef is one project with several components:

```text
Angular frontend
Django backend
Prometheus configuration
Grafana dashboards
benchmark scenarios
generated reports
documentation
```

### Starting State

```text
bench-chef/
├── docs/
├── LICENSE
└── README.md
```

### Work To Do

#### 1. Create project directories

```bash
mkdir -p backend-django
mkdir -p frontend-angular
mkdir -p prometheus
mkdir -p grafana/dashboards
mkdir -p grafana/provisioning
mkdir -p scenarios
mkdir -p reports
mkdir -p docs
```

#### 2. Add placeholder files

```bash
touch backend-django/.gitkeep
touch frontend-angular/.gitkeep
touch prometheus/.gitkeep
touch grafana/dashboards/.gitkeep
touch grafana/provisioning/.gitkeep
touch scenarios/.gitkeep
touch reports/.gitkeep
```

#### 3. Add `.gitignore`

```bash
cat > .gitignore <<'EOF'
## OS / editor
.DS_Store
.idea/
.vscode/

## Python / Django
__pycache__/
*.py[cod]
.venv/
venv/
env/
*.sqlite3
db.sqlite3
.env

## Node / Angular
node_modules/
dist/
.angular/
npm-debug.log*
package-lock.json

## Reports generated locally
reports/*
!reports/.gitkeep

## Local runtime data
tmp/
logs/
EOF
```

#### 4. Add `.env.example`

```bash
cat > .env.example <<'EOF'
BENCHCHEF_DEBUG=true
BENCHCHEF_BACKEND_PORT=18090
BENCHCHEF_FRONTEND_PORT=4200

SPAGHETTICHEF_BASE_URL=http://localhost:18080
SPAGHETTICHEF_ROLE_HEADER=ADMIN

PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
EOF
```

#### 5. Add initial `docker-compose.yml`

```bash
cat > docker-compose.yml <<'EOF'
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: benchchef-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro

  grafana:
    image: grafana/grafana-oss:latest
    container_name: benchchef-grafana
    ports:
      - "3000:3000"
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning
      - ./grafana/dashboards:/var/lib/grafana/dashboards
    depends_on:
      - prometheus
EOF
```

#### 6. Add initial Prometheus config

```bash
cat > prometheus/prometheus.yml <<'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
EOF
```

#### 7. Update `README.md`

Use this short version for now:

```markdown
## BenchChef

BenchChef is a performance supervision and benchmark workbench for SpaghettiChef.

SpaghettiChef remains the operational product.

BenchChef observes SpaghettiChef from outside, measures performance, stores benchmark results, and visualizes metrics through Prometheus and Grafana.

### Architecture

```text
BenchChef
├── frontend-angular/
├── backend-django/
├── prometheus/
├── grafana/
├── scenarios/
├── reports/
└── docs/
```
 

### Acceptance Criteria

```text
repository has clean component directories
no generated Angular code yet
no generated Django code yet
Prometheus and Grafana folders exist
docker-compose.yml exists
.env.example exists
README explains the project boundary
git status is clean after commit
```

 

 
## TODO 0.1.1 — Django Backend Bootstrap

### Purpose

Create the initial Django backend inside `backend-django/`.

This step bootstraps the backend structure only. It does not yet implement BenchChef domain models.

### Work To Do

#### 1. Create Python virtual environment

```bash
cd backend-django
python3 -m venv .venv
source .venv/bin/activate
````

#### 2. Install backend dependencies

```bash
pip install --upgrade pip
pip install django djangorestframework django-cors-headers python-decouple
```

#### 3. Save dependencies

```bash
pip freeze > requirements.txt
```

#### 4. Create Django project

```bash
django-admin startproject benchchef .
```

Expected structure:

```text
backend-django/
├── benchchef/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

`asgi.py` may also be generated depending on the Django version. It is acceptable either way.

#### 5. Create Django apps

Target structure:

```text
backend-django/
├── benchchef/          # Django project config: settings, urls, wsgi/asgi
├── health/             # lightweight health/status endpoint
├── accounts/           # later: users, roles, authentication
├── connections/        # SpaghettiChef connection profiles
├── probes/             # black-box HTTP probes and probe samples
├── benchmarks/         # benchmark runs, scenarios, run status
├── reports/            # generated reports and exports
└── manage.py
```

Create apps:

```bash
python manage.py startapp health
python manage.py startapp accounts
python manage.py startapp connections
python manage.py startapp probes
python manage.py startapp benchmarks
python manage.py startapp reports
```

#### 6. Add backend health endpoint

Create or replace:

```text
backend-django/health/views.py
```

with:

```python
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({
        "status": "ok",
        "service": "benchchef-backend",
    })
```

#### 7. Register backend URLs

Replace:

```text
backend-django/benchchef/urls.py
```

with:

```python
from django.contrib import admin
from django.urls import path

from health.views import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health", health_check, name="api-health"),
]
```

Expected endpoint:

```text
GET /api/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "benchchef-backend"
}
```

#### 8. Update Django settings

In:

```text
backend-django/benchchef/settings.py
```

add these apps to `INSTALLED_APPS`:

```python
"rest_framework",
"corsheaders",
"health",
"accounts",
"connections",
"probes",
"benchmarks",
"reports",
```

Add CORS middleware near the top of `MIDDLEWARE`, before `CommonMiddleware`:

```python
"corsheaders.middleware.CorsMiddleware",
```

For local development, add:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
]

CORS_ALLOW_CREDENTIALS = False
 
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', ]

``` 

#### 9. Run migrations

```bash
python manage.py migrate
```

#### 10. Start backend

```bash
python manage.py runserver 0.0.0.0:18090
```

#### 11. Test health endpoint

In another terminal:

```bash
curl -fsS http://localhost:18090/api/health
```

Expected:

```json
{"status": "ok", "service": "benchchef-backend"}
```

### Acceptance Criteria

```text
backend-django contains a valid Django project
virtual environment exists locally but is ignored by git
requirements.txt exists
Django REST Framework is installed
django-cors-headers is installed
apps exist: health, accounts, connections, probes, benchmarks, reports
GET /api/health returns JSON
Django server starts on port 18090
curl health check succeeds
no BenchChef domain model is implemented yet
no app called core is created
```

### Suggested Commit

```bash
git status
git add .
git commit -m "0.1.1 - Bootstrap Django backend"
```

### Commands To Run Now

```bash
cd ~/coding/github/bench-chef
mkdir -p backend-django
cd backend-django

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install django djangorestframework django-cors-headers python-decouple
pip freeze > requirements.txt

django-admin startproject benchchef .

python manage.py startapp health
python manage.py startapp accounts
python manage.py startapp connections
python manage.py startapp probes
python manage.py startapp benchmarks
python manage.py startapp reports
```
 
