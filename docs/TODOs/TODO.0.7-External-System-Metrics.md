# 0.7.x TODO — External System Metrics

## Status

```text
DONE
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

## Implemented Files

```text
docker-compose.yml
prometheus/prometheus.yml.template
prometheus/process-exporter.yml
docs/system-metrics.md
docs/install.md
docs/test.md
README.md
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

## Test

Start the stack:

```bash
./scripts/start.sh
```

Open:

```text
http://localhost:18073/targets
```

Expected targets:

```text
node-exporter      UP
process-exporter   UP
```

Useful Prometheus queries:

```text
node_memory_MemAvailable_bytes
rate(node_cpu_seconds_total[5m])
rate(namedprocess_namegroup_cpu_seconds_total[5m])
namedprocess_namegroup_memory_bytes
```
