# 2.1.x TODO — Support Reports And PDF Workflow

## Status

```text
PLANNED
```

## Purpose

Add a support-oriented incident/report workflow useful for Level-2
troubleshooting.

## Planned Scope

```text
Angular incident form
form validation
Django incident API
incident storage
PDF generation
PDF download from Angular
support handover report
```

## Reserved API Names

Keep these planned names stable unless the interface is intentionally redesigned:

```text
POST /api/incidents/
GET  /api/incidents/{id}/
GET  /api/incidents/{id}/pdf/
```

## Draft Subtasks

### TODO 2.1.0 — Angular Incident Form

```text
customer/system name
affected service
steps to reproduce
expected result
actual result
severity
notes
```

### TODO 2.1.1 — Angular Validation

```text
required fields
severity enum
minimum text length for reproduction steps
```

### TODO 2.1.2 — Django Incident API

```text
create incident records
read incident records
serve generated incident PDFs
```

### TODO 2.1.3 — PDF Export

```text
generate support PDF
include timestamp, health status, and metrics snapshot
download from Angular
```
