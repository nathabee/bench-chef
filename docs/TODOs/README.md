# BenchChef TODOs

Use this folder for implementation-level planning.

```text
roadmap.md          current architecture direction
TODOs/README.md    index and planning rules
TODO.*.md          detailed work notes for one version line
spaghettichef-compatibility.md  BenchChef expectations for SpaghettiChef
```

## Rule Of Thumb

Keep [../roadmap.md](../roadmap.md) focused on the current architecture
direction. It should not become a second detailed TODO list.

Put detailed work, commands, acceptance criteria, and draft endpoint names in
the version-specific TODO file.

If a future API name might already affect SpaghettiChef or a client, keep the
planned name in the relevant TODO file and later promote it to
[../spaghettichef-compatibility.md](../spaghettichef-compatibility.md)
or the relevant boundary document when implemented.

## Version Files

| Version | Status | File |
| ------- | ------ | ---- |
| 0.1.x | DONE | [TODO.0.1-Foundation.md](TODO.0.1-Foundation.md) |
| 0.2.x | DONE | [TODO.0.2-Backend.md](TODO.0.2-Backend.md) |
| 0.3.x | DONE | [TODO.0.3-SpaghettiChef-Connect.md](TODO.0.3-SpaghettiChef-Connect.md) |
| 0.4.x | DONE | [TODO.0.4-BlackBox.md](TODO.0.4-BlackBox.md) |
| 0.5.x | DONE | [TODO.0.5-Prometheus.md](TODO.0.5-Prometheus.md) |
| 0.6.x | IN PROGRESS | [TODO.0.6-Grafana1.md](TODO.0.6-Grafana1.md) |
| 0.7.x | DONE | [TODO.0.7-External-System-Metrics.md](TODO.0.7-External-System-Metrics.md) |
| 0.8.x | DONE | [TODO.0.8-Grafana-Observability.md](TODO.0.8-Grafana-Observability.md) |
| 0.9.x | PLANNED | [TODO.0.9-Angular-Workbench.md](TODO.0.9-Angular-Workbench.md) |
| 0.10.x | PLANNED | [TODO.0.10-Benchmark-Scenario-Runner.md](TODO.0.10-Benchmark-Scenario-Runner.md) |
| 1.0.x | PLANNED | [TODO.1.0-BenchChef-Central-Sync-Boundary.md](TODO.1.0-BenchChef-Central-Sync-Boundary.md) |
| 1.1.x | PLANNED | [TODO.1.1-BenchChef-Central-Backend.md](TODO.1.1-BenchChef-Central-Backend.md) |
| 1.2.x | PLANNED | [TODO.1.2-BenchChef-Central-Dashboards.md](TODO.1.2-BenchChef-Central-Dashboards.md) |
| 2.0.x | PLANNED | [TODO.2.0-Reports-Release.md](TODO.2.0-Reports-Release.md) |
| 2.1.x | PLANNED | [TODO.2.1-Support-Reports-PDF.md](TODO.2.1-Support-Reports-PDF.md) |
| 3.0.x | PLANNED | [TODO.3.0-Kotlin-REST-Client.md](TODO.3.0-Kotlin-REST-Client.md) |
| 3.1.x | PLANNED | [TODO.3.1-Android-Support-Client.md](TODO.3.1-Android-Support-Client.md) |
