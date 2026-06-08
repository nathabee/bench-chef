# 0.7.x TODO — External System Metrics

## Status

```text
PLANNED
```

## Purpose

Monitor CPU, RAM, disk, and process behavior from outside SpaghettiChef.

BenchChef should be able to correlate probe latency and failures with machine
or process pressure.

## Planned Scope

```text
node_exporter setup
process-exporter setup
optional cAdvisor setup
Prometheus scrape configuration
metric documentation
```

## Candidate Metric Sources

```text
node_exporter       machine CPU/RAM/disk
process-exporter    SpaghettiChef process CPU/RAM
cAdvisor            container metrics, if Docker is used
blackbox_exporter   external HTTP reachability, optional
BenchChef exporter  benchmark-specific metrics
```

## Acceptance Direction

```text
Prometheus can scrape external system metrics
Grafana can later combine system metrics with BenchChef probe metrics
SpaghettiChef does not need code changes for this step
```
