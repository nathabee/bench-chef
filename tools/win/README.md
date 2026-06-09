# BenchChef Windows Tools

These scripts are copied to a Windows BenchChef host under:

```text
C:\benchchef\bin
```

Expected runtime layout:

```text
C:\benchchef\
├── app\
├── bin\
├── data\
├── log\
├── rel\
└── tmp\
```

## Scripts

```text
t.ps1              create the optional BenchChef login scheduled task
r.ps1              start BenchChef through Task Scheduler
s.ps1              stop BenchChef
u.ps1              update BenchChef from a GitHub release ZIP
v.ps1              verify runtime configuration and status
run.env.example    example runtime environment file
```

## Requirements

The Windows host needs:

```text
Docker Desktop
PowerShell
OpenSSH Server, for remote administration
```

BenchChef releases contain the Django backend, built Angular frontend,
Prometheus/Grafana provisioning, Docker Compose file, scripts, and docs.

SpaghettiChef is still installed separately. BenchChef observes SpaghettiChef
over REST and does not replace it.
