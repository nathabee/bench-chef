# 0.11.x TODO — Windows System Metrics

## Status

```text
PLANNED
```

## Purpose

Add Windows host and process metrics so Grafana system panels have data on
Windows BenchChef Local installs.

The Linux local stack already uses `node_exporter` and `process-exporter`.
Windows release installs intentionally do not start those Linux exporters,
because Docker Desktop Windows does not expose the same host filesystem and
process model.

## Current Gap

On Windows release installs, these Grafana panels may be empty:

```text
Host CPU Busy
Host RAM Available
Filesystem Available
Disk Read
Disk Write
Process CPU
Process RAM
```

The existing dashboard queries Linux exporter metrics such as:

```text
node_cpu_seconds_total
node_memory_MemAvailable_bytes
node_filesystem_avail_bytes
namedprocess_namegroup_cpu_seconds_total
namedprocess_namegroup_memory_bytes
```

## Planned Scope

```text
choose Windows exporter strategy
document Windows exporter installation
add Prometheus scrape job for Windows host metrics
add Windows metric queries or Windows dashboard row
keep Linux node_exporter/process-exporter behavior unchanged
update Grafana panels so unsupported metrics are clear
update install documentation
```

Likely exporter:

```text
windows_exporter
```

Candidate Windows metrics:

```text
windows_cpu_time_total
windows_memory_available_bytes
windows_logical_disk_free_bytes
windows_logical_disk_size_bytes
windows_process_cpu_time_total
windows_process_working_set_private_bytes
```

## Design Direction

Prefer a Windows-native exporter installed on the Windows host.

Prometheus may continue to run in Docker, but it should scrape the Windows
exporter through a host-accessible URL.

Do not force Linux exporters into Windows Docker Desktop.

## Documentation To Update

```text
docs/system-metrics.md
docs/grafana.md
docs/install-remote.md
docs/install.md
README.md
```

## Acceptance Direction

```text
Windows install documentation says how to start Windows host metrics
Prometheus target for Windows host metrics is UP
Grafana has Windows CPU and memory data
Grafana clearly separates Linux exporter panels from Windows exporter panels
Linux local system metrics still work
```

## Non-Goals

```text
no SpaghettiChef code changes
no printer control
no camera control
no BenchChef Central dependency
no requirement to run Linux node_exporter/process-exporter on Windows
```
