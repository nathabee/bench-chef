TODO 0.1.x — Project Foundation

TODO 0.1.0 — Repository Skeleton
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

TODO 0.1.1 — Django Backend Bootstrap
- create Python virtual environment in backend-django/
- install Django
- install Django REST Framework
- create Django project
- add requirements.txt
- add backend .env.example if needed
- add GET /api/health
- verify python manage.py runserver works
- commit Django bootstrap

TODO 0.1.2 — Angular Frontend Bootstrap
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

TODO 0.1.3 — Local Stack Smoke Test
- add basic Prometheus config
- add basic Grafana provisioning folders
- make docker compose start Prometheus and Grafana
- verify Prometheus opens on 9090
- verify Grafana opens on 3000
- document local startup commands
- commit monitoring stack bootstrap



TODO 0.2 BenchChef Backend Domain Foundation

TODO 0.2.0
- create Django apps: connections, probes, benchmarks, reports
- add ConnectionProfile model
- add Django admin registration
- add serializers
- add basic REST endpoints

TODO 0.2.1
- add ProbeSample model
- store URL, method, status code, latency, timeout, error message
- expose probe samples through API

TODO 0.2.2
- add BenchmarkRun model
- add BenchmarkRun status lifecycle
- expose benchmark run list/detail API

 

TODO 0.3 — SpaghettiChef Connection And Black-Box Probing

TODO 0.2.0
- create Django apps: connections, probes, benchmarks, reports
- add ConnectionProfile model
- add Django admin registration
- add serializers
- add basic REST endpoints

TODO 0.2.1
- add ProbeSample model
- store URL, method, status code, latency, timeout, error message
- expose probe samples through API

TODO 0.2.2
- add BenchmarkRun model
- add BenchmarkRun status lifecycle
- expose benchmark run list/detail API

TODO 0.3.0
- implement SpaghettiChef connection test
- call /health
- call /version
- call /monitoring
- store status, latency, error message
