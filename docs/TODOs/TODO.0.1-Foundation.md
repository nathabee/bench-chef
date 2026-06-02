# 0.1.x TODO 0.1.x — Project Foundation



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
 
## TODO 0.1.2 — Angular Frontend Bootstrap

### Purpose

Create the initial Angular frontend inside `frontend-angular/`.

This step only bootstraps the user interface shell. It does not yet connect to the Django backend or to SpaghettiChef.

### Work To Do

### 1. Create Angular application

From the repository root:

```bash
cd ~/coding/github/bench-chef
rm -rf frontend-angular/.gitkeep
npx @angular/cli new frontend-angular --routing --style=css
````

When Angular asks about server-side rendering, answer:

```text
No
```

### 2. Start Angular development server

```bash
cd frontend-angular
npm install zone.js
npm start
```

Expected local URL:

```text
http://localhost:4200
```

### 3. Set application title

Set the visible application title to:

```text
BenchChef
```

In Angular, set it in:

```text
frontend-angular/src/app/app.html
```

Replace the default content.
After changing the name of the App it is necessary to modify and adapt the app.spec.ts


 
### 4. Generate initial Angular pages, components, and services

From the Angular project folder:

```bash
cd ~/coding/github/bench-chef/frontend-angular

ng generate component pages/dashboard
ng generate component pages/connections
ng generate component pages/probes
ng generate component pages/benchmarks
ng generate component pages/reports
ng generate component pages/settings

ng generate component components/status-card
ng generate component components/metric-card
ng generate component components/run-summary-card

ng generate service services/backend-api
ng generate service services/connection-api
ng generate service services/probe-api
```

### 5. Configure application routes

Edit:

```text
frontend-angular/src/app/app.routes.ts
```

Use:

```ts
import { Routes } from '@angular/router';

import { Dashboard } from './pages/dashboard/dashboard';
import { Connections } from './pages/connections/connections';
import { Probes } from './pages/probes/probes';
import { Benchmarks } from './pages/benchmarks/benchmarks';
import { Reports } from './pages/reports/reports';
import { Settings } from './pages/settings/settings';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: Dashboard },
  { path: 'connections', component: Connections },
  { path: 'probes', component: Probes },
  { path: 'benchmarks', component: Benchmarks },
  { path: 'reports', component: Reports },
  { path: 'settings', component: Settings },
  { path: '**', redirectTo: 'dashboard' },
];
```

you need to update the app.ts to make routing active:

```ts
import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {}
```

and app.config.ts , called from the main.ts must provide the router:

```ts

import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
  ],
};

```


### 6. Replace the default app shell

Edit:

```text
frontend-angular/src/app/app.html
```

Use:

```html
<div class="app-shell">
  <aside class="sidebar">
    <div class="brand">
      <h1>BenchChef</h1>
      <p>Performance Workbench</p>
    </div>

    <nav>
      <a routerLink="/dashboard" routerLinkActive="active">Dashboard</a>
      <a routerLink="/connections" routerLinkActive="active">Connections</a>
      <a routerLink="/probes" routerLinkActive="active">Probes</a>
      <a routerLink="/benchmarks" routerLinkActive="active">Benchmarks</a>
      <a routerLink="/reports" routerLinkActive="active">Reports</a>
      <a routerLink="/settings" routerLinkActive="active">Settings</a>
    </nav>
  </aside>

  <main class="content">
    <router-outlet></router-outlet>
  </main>
</div>
```

### 7. Add simple placeholder page content

Each generated page should show:

```text
page title
short purpose text
Planned
```

Use this content idea:

```text
Dashboard
Overview of BenchChef status, probe results, and benchmark summaries.

Connections
SpaghettiChef connection profiles and connection status.

Probes
Black-box probes for backend, dashboard, and camera-job responsiveness.

Benchmarks
Repeatable benchmark scenarios and run history.

Reports
Generated benchmark reports and export links.

Settings
Local BenchChef configuration.
```

### 8. Keep Angular independent for now

Do not call Django yet.

Do not call SpaghettiChef yet.

This step is only the frontend shell.

### 9. Verify frontend works

Run:

```bash
cd frontend-angular

ng serve --open
```

Open:

```text
http://localhost:4200
```

Also check:

```text
http://localhost:4200/dashboard
http://localhost:4200/connections
http://localhost:4200/probes
http://localhost:4200/benchmarks
http://localhost:4200/reports
http://localhost:4200/settings
```

Expected result:

```text
/ redirects to /dashboard
all navigation links work
all placeholder pages render
```

### Acceptance Criteria

```text
Angular application exists inside frontend-angular
Angular development server starts on port 4200
application title is BenchChef
navigation exists
placeholder pages exist
routes exist for dashboard, connections, probes, benchmarks, reports, settings
no backend API call is implemented yet
no SpaghettiChef API call is implemented yet
npm start works
git status is clean after commit
```

### Suggested Commit

```bash
git status
git add .
git commit -m "0.1.2 - Bootstrap Angular frontend"
```
 

 
---

## TODO 0.1.3 — Local Monitoring Stack Smoke Test

### Purpose

Start the first local monitoring stack for BenchChef.

This step verifies that Prometheus and Grafana can run locally through Docker Compose.

It does not yet monitor SpaghettiChef.

It does not yet monitor BenchChef Django.

### Work To Do

### 1. Verify Docker is available

```bash
docker --version
docker compose version
```

### 2. Verify Prometheus config exists

Expected file:

```text
prometheus/prometheus.yml
```

Expected minimal content:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

### 3. Verify Docker Compose file exists

Expected file:

```text
docker-compose.yml
```

Expected services:

```text
prometheus
grafana
```

### 4. Start monitoring stack

From repository root:

```bash
cd ~/coding/github/bench-chef
docker compose up -d

sudo systemctl start docker
```

### 5. Check containers

```bash
docker compose ps
```

Expected:

```text
benchchef-prometheus running
benchchef-grafana running
```

### 6. Open Prometheus

Open:

```text
http://localhost:9090
```

Check:

```text
Status -> Targets
```

Expected:

```text
prometheus target is UP
```

### 7. Open Grafana

Open:

```text
http://localhost:3000
```

Default login:

```text
user: admin
password: admin
```

Grafana may ask to change the password.

### 8. Stop monitoring stack

```bash
docker compose down
```

### 9. Document local startup commands

Add to `README.md`:

````markdown
## Local monitoring stack

Start Prometheus and Grafana:

```bash
docker compose up -d
````

Open:

```text
Prometheus: http://localhost:9090
Grafana:    http://localhost:3000
```

Stop:

```bash
docker compose down
```


### Acceptance Criteria

```text
docker compose starts Prometheus
docker compose starts Grafana
Prometheus opens on port 9090
Prometheus target page shows prometheus as UP
Grafana opens on port 3000
README documents start/stop commands
SpaghettiChef is not monitored yet
BenchChef Django is not monitored yet
git status is clean after commit
```

### Suggested Commit

```bash
git status
git add .
git commit -m "0.1.3 - Bootstrap local monitoring stack"
```


Then run:

```bash
cd ~/coding/github/bench-chef
docker compose up -d
docker compose ps
```
