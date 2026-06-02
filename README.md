
>> WORK IN PROGRESS 


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