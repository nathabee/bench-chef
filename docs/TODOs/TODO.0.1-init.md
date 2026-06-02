# TODO 0.1.0 — BenchChef Repository Skeleton

## Purpose

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
````

## Starting State

```text
bench-chef/
├── docs/
├── LICENSE
└── README.md
```

## Work To Do

### 1. Create project directories

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

### 2. Add placeholder files

```bash
touch backend-django/.gitkeep
touch frontend-angular/.gitkeep
touch prometheus/.gitkeep
touch grafana/dashboards/.gitkeep
touch grafana/provisioning/.gitkeep
touch scenarios/.gitkeep
touch reports/.gitkeep
```

### 3. Add `.gitignore`

```bash
cat > .gitignore <<'EOF'
# OS / editor
.DS_Store
.idea/
.vscode/

# Python / Django
__pycache__/
*.py[cod]
.venv/
venv/
env/
*.sqlite3
db.sqlite3
.env

# Node / Angular
node_modules/
dist/
.angular/
npm-debug.log*
package-lock.json

# Reports generated locally
reports/*
!reports/.gitkeep

# Local runtime data
tmp/
logs/
EOF
```

### 4. Add `.env.example`

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

### 5. Add initial `docker-compose.yml`

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

### 6. Add initial Prometheus config

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

### 7. Update `README.md`

Use this short version for now:

````markdown
# BenchChef

BenchChef is a performance supervision and benchmark workbench for SpaghettiChef.

SpaghettiChef remains the operational product.

BenchChef observes SpaghettiChef from outside, measures performance, stores benchmark results, and visualizes metrics through Prometheus and Grafana.

## Architecture

```text
BenchChef
├── frontend-angular/
├── backend-django/
├── prometheus/
├── grafana/
├── scenarios/
├── reports/
└── docs/
````

## Current Goal

0.1.0 creates the repository skeleton.

No SpaghettiChef runtime action is triggered in this version.

````

## Acceptance Criteria

```text
repository has clean component directories
no generated Angular code yet
no generated Django code yet
Prometheus and Grafana folders exist
docker-compose.yml exists
.env.example exists
README explains the project boundary
git status is clean after commit
````

## Suggested commit

```bash
git status
git add .
git commit -m "Initialize BenchChef project skeleton"
```

```
```
