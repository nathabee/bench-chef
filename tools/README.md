# BenchChef Tools

This directory contains release and operational helper scripts for BenchChef.

```text
tools/
├── check-version.sh
├── sync-version.sh
├── git-hooks/
├── ops/
└── win/
```

## Github tools

From the repo root, run:
```bash
cp tools/git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Then test it manually:
```bash
.git/hooks/pre-commit
```

## Version Tools

`VERSION` is the release version source of truth.

```bash
tools/check-version.sh
tools/sync-version.sh
```

`sync-version.sh` updates the Angular package version from `VERSION`.

## Operations Helpers

`tools/ops/` contains Linux admin-machine helpers for a remote Windows
BenchChef host:

```text
bchefu     run a remote update
bchefv     show remote status
bchefdiag  collect remote diagnostics
```

The helpers use OpenSSH and PowerShell on the remote host.

## Windows Tools

`tools/win/` contains Windows-side scripts intended for the admin package.

They manage a local BenchChef install under:

```text
C:\benchchef
```

BenchChef is a Django/Angular/Docker Compose workbench. The Windows tools do
not launch SpaghettiChef and do not manage printer or camera operations.
