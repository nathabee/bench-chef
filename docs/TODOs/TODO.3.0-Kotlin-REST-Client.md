# 3.0.x TODO — Kotlin REST Client

## Status

```text
PLANNED
```

## Purpose

Create a small Kotlin client that consumes BenchChef REST APIs.

Start with a Kotlin console client, not Android.

## Planned Scope

```text
Kotlin project folder
call BenchChef health/status endpoints
parse JSON responses
print diagnostic summary
document how to run it
```

## Reserved API Names

These names are planned for the client contract and should stay stable once
introduced:

```text
GET /api/health
GET /api/services/status
```

## Draft Subtasks

### TODO 3.0.0 — Kotlin Console Client

```text
call GET /api/health
call GET /api/services/status
print result
```

### TODO 3.0.1 — Kotlin Data Models

```text
HealthResponse
ServiceStatus
IncidentSummary
```

### TODO 3.0.2 — Optional Android Preparation

```text
simple status screen concept
button to open Grafana
button to open incident PDF
```
