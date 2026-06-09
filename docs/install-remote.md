# Remote Windows Install And Update

## Purpose

This document describes how to install or update BenchChef Local on a Windows
host from a Linux admin machine.

BenchChef is the observer/workbench. SpaghettiChef remains a separate local
runtime and is not installed by these scripts.

## Release Assets

BenchChef release tags use:

```text
v<version>
```

Expected GitHub release assets:

```text
bench-chef-<version>-release.tar.gz
bench-chef-<version>-linux.tar.gz
bench-chef-<version>-windows.zip
bench-chef-<version>-admin.zip
SHA256SUMS.txt
```

The Windows package contains the BenchChef app files.

The admin package contains:

```text
benchchef/bin/       Windows PowerShell scripts
benchchef/data/      runtime configuration example
benchchef/ops/       Linux admin helper scripts
benchchef/README.md
```

## GitHub Release Publishing

The Jenkins pipeline can publish these assets when:

```text
PUBLISH_GITHUB_RELEASE=true
```

Publishing uses the same Jenkins Secret Text credential convention as
SpaghettiChef:

```text
credential id: github-token
bound variable: GITHUB_TOKEN
```

For a packaging-only test, leave:

```text
PUBLISH_GITHUB_RELEASE=false
```

## Windows Host Layout

```text
C:\benchchef\
├── app\
├── bin\
├── data\
├── log\
├── rel\
└── tmp\
```

Meaning:

```text
app\   current BenchChef release files
bin\   operational PowerShell scripts
data\  local configuration and persistent runtime data
log\   start/update logs
rel\   downloaded release archives
tmp\   temporary extraction and diagnostics
```

## Windows Requirements

Install these once on the Windows host:

```text
Docker Desktop
PowerShell
OpenSSH Server, if remote administration is wanted
Git is optional
```

BenchChef uses Docker Compose for Prometheus, Grafana, node-exporter, and
process-exporter. The BenchChef app package contains the Django backend source,
the built Angular frontend, scripts, dashboards, and documentation. BenchChef
does not ship a jar.

## One-Time Windows Bootstrap

Create directories:

```powershell
New-Item -ItemType Directory -Force -Path C:\benchchef\app
New-Item -ItemType Directory -Force -Path C:\benchchef\bin
New-Item -ItemType Directory -Force -Path C:\benchchef\data
New-Item -ItemType Directory -Force -Path C:\benchchef\log
New-Item -ItemType Directory -Force -Path C:\benchchef\rel
New-Item -ItemType Directory -Force -Path C:\benchchef\tmp
```

Download the admin package:

```text
bench-chef-<version>-admin.zip
```

Extract it into:

```text
C:\
```

Do not extract this archive into `C:\benchchef`; otherwise it will create a
nested path such as:

```text
C:\benchchef\benchchef\bin\
```

The archive contains a `benchchef\` directory, so extracting it into `C:\`
creates or updates:

```text
C:\benchchef\bin\
C:\benchchef\data\run.env.example
C:\benchchef\ops\
```

It does not contain `C:\benchchef\data\run.env`, so an existing runtime
configuration is not overwritten.

Create the runtime config only if it does not already exist:

```powershell
if (-not (Test-Path C:\benchchef\data\run.env)) {
    Copy-Item C:\benchchef\data\run.env.example C:\benchchef\data\run.env
}
```

Review `C:\benchchef\data\run.env` and adjust ports if needed.

Register the scheduled task:

```powershell
C:\benchchef\bin\t.ps1
```

## First App Install

Download and extract:

```text
bench-chef-<version>-windows.zip
```

Copy the extracted `bench-chef\` content into:

```text
C:\benchchef\app\
```

Start:

```powershell
C:\benchchef\bin\r.ps1
```

Verify:

```powershell
C:\benchchef\bin\v.ps1
```

Open:

```text
BenchChef Angular  http://localhost:18072
BenchChef Backend  http://localhost:18071
Prometheus         http://localhost:18073
Grafana            http://localhost:18074
```

## Linux Admin Helpers

From a Linux admin machine, copy or add `tools/ops` to `PATH`.

The helpers use:

```text
BCHEF_HOST
BCHEF_USER
```

Example:

```bash
export BCHEF_HOST=192.168.1.42
export BCHEF_USER=myadmin
```

Check status:

```bash
tools/ops/bchefv
```

Update:

```bash
tools/ops/bchefu 0.10.0
```

Collect diagnostics:

```bash
tools/ops/bchefdiag
```

Diagnostics are downloaded to:

```text
response.txt
```

## What The Update Script Does

`u.ps1`:

```text
downloads bench-chef-<version>-windows.zip
extracts it under C:\benchchef\tmp
stops the current BenchChef stack if installed
replaces C:\benchchef\app
optionally refreshes admin scripts from bench-chef-<version>-admin.zip
creates C:\benchchef\data\run.env from the example when missing
starts BenchChef
```

Persistent local data under `C:\benchchef\data` is not replaced.

## Non-Goals

```text
no VPS BenchChef Central install yet
no SpaghettiChef install or update
no printer control
no camera control
no public exposure of LAN printer/camera APIs
```
