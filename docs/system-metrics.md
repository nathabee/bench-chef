# External System Metrics

## Purpose

BenchChef can collect host and process metrics from outside the observed
runtime.

This allows Grafana dashboards to later correlate probe latency, failures,
timeouts, and derived observations with CPU, RAM, disk, and process pressure.

SpaghettiChef code is not changed for this step.

## Metric Sources

```text
node_exporter       host CPU/RAM/disk/filesystem/network metrics
process-exporter    selected local process CPU/RAM metrics
BenchChef exporter  probe, benchmark, availability, and latency metrics
```

cAdvisor remains optional for a later container-focused deployment.

## Local Stack

Start BenchChef:

```bash
./scripts/start.sh
```

The Docker stack starts:

```text
Prometheus
Grafana
node-exporter
process-exporter
```

Default local URLs:

```text
Prometheus        http://localhost:18073
Grafana           http://localhost:18074
node_exporter     http://localhost:18075/metrics
process-exporter  http://localhost:18076/metrics
```

The external exporter ports are configured in `.env`:

```text
NODE_EXPORTER_PORT=18075
PROCESS_EXPORTER_PORT=18076
```

## Prometheus Scrape Jobs

Prometheus is generated from:

```text
prometheus/prometheus.yml.template
```

Current scrape jobs:

```text
benchchef-backend
node-exporter
process-exporter
```

Open:

```text
http://localhost:18073/targets
```

Expected:

```text
node-exporter      UP
process-exporter   UP
```

SpaghettiChef is not scraped as a Prometheus target. BenchChef observes
SpaghettiChef through REST/JSON probes, and `process-exporter` observes the
SpaghettiChef process from outside.

## Useful Queries

Host CPU:

```promql
rate(node_cpu_seconds_total[5m])
```

Host memory available:

```promql
node_memory_MemAvailable_bytes
```

Filesystem available:

```promql
node_filesystem_avail_bytes
```

Named process CPU:

```promql
rate(namedprocess_namegroup_cpu_seconds_total[5m])
```

Named process memory:

```promql
namedprocess_namegroup_memory_bytes
```

Configured process groups:

```text
spaghettichef
benchchef-django
benchchef-angular
```

## Non-Goals

```text
no SpaghettiChef code changes
no printer control
no camera control
no Grafana dashboard changes in this step
no requirement for cAdvisor yet
```
