# 0.10.x TODO — Release Packaging

## Status

```text
IN PROGRESS - DEVELOPPED - IN TEST
```

## Purpose

Create a repeatable BenchChef Local release process.

This version line is about packaging the local BenchChef stack, publishing
release assets from Jenkins, and providing basic remote install/update helper
scripts for a Windows BenchChef host.

It is not the BenchChef Central/VPS release yet.

## Scope

### 0.10.1 — Version Metadata

Status: DONE

Work:

* add root `VERSION`
* keep Angular package version aligned with `VERSION`
* add `tools/check-version.sh`
* add `tools/sync-version.sh`
* keep the pre-commit version check available

Acceptance:

```text
tools/check-version.sh passes
tools/sync-version.sh updates frontend-angular/package.json
stale SpaghettiChef release references are rejected from BenchChef release tooling
```

### 0.10.2 — Jenkins Release Pipeline

Status: DONE

Work:

* replace copied SpaghettiChef Jenkins behavior with a BenchChef pipeline
* use the Jenkins job checkout as the source tree
* allow Python executable selection
* allow optional Node home override
* allow optional release version override
* run backend tests
* build Angular frontend
* package release assets
* optionally publish a GitHub release with `gh`

Acceptance:

```text
Jenkins can build BenchChef from the branch selected by the Jenkins job
Jenkins can create local release artifacts
Jenkins can publish those artifacts to GitHub Releases when enabled
```

### 0.10.3 — Release Assets

Status: DONE

Work:

* create a Linux package
* create a Windows package
* create an admin-tools package
* create a combined release archive
* create checksums

Release asset names:

```text
bench-chef-<version>-linux.tar.gz
bench-chef-<version>-windows.zip
bench-chef-<version>-admin.zip
bench-chef-<version>-release.tar.gz
SHA256SUMS.txt
```

Acceptance:

```text
release contains BenchChef local application files
release contains Docker Compose, Prometheus, and Grafana configuration
release contains Windows admin scripts
release excludes local virtualenvs, local sqlite database, and runtime logs
```

### 0.10.4 — Windows Admin Tools

Status: DONE

Work:

* adapt Windows scripts for BenchChef
* use `C:\benchchef`
* start and stop BenchChef with Docker Compose
* add a Windows scheduled task helper
* add a release update helper
* add a verification helper
* document Windows tool usage

Acceptance:

```text
tools/win/r.ps1 starts BenchChef Docker services
tools/win/s.ps1 stops BenchChef Docker services
tools/win/t.ps1 creates a Windows startup task
tools/win/u.ps1 installs or updates a BenchChef release
tools/win/v.ps1 checks local service URLs
```

### 0.10.5 — Remote Install Documentation

Status: DONE

Work:

* document the release assets
* document first Windows host bootstrap
* document remote update helpers
* document verification commands
* document what is intentionally not installed by this release

Acceptance:

```text
docs/install-remote.md explains the first remote install
docs/install-remote.md explains release updates
docs/install-remote.md makes clear SpaghettiChef is installed separately
```

### 0.10.6 — Project Status Documentation

Status: DONE

Work:

* update README implementation status
* update TODO index
* keep 0.11 as the benchmark scenario runner line

Acceptance:

```text
README and docs/TODOs/README.md agree that 0.10.x is release packaging
README and docs/TODOs/README.md agree that 0.11.x is benchmark scenario runner
```

## Non-Goals

```text
no BenchChef Central/VPS deployment package yet
no SpaghettiChef install or update package
no printer control
no camera control
no public exposure of LAN printer/camera APIs
no benchmark scenario runner implementation in 0.10.x
```

## Final Acceptance Criteria

```text
version check passes
backend tests pass
frontend build passes
Jenkinsfile packages BenchChef release assets
Windows admin tools are BenchChef-specific
remote install documentation exists
README implementation status is aligned with TODO files
```
