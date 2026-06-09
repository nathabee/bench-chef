$ErrorActionPreference = 'Stop'

$Root = 'C:\benchchef'
$AppDir = Join-Path $Root 'app'

if (-not (Test-Path -LiteralPath (Join-Path $AppDir 'docker-compose.yml'))) {
    Write-Host "BenchChef app directory is not installed: $AppDir"
    exit 0
}

Set-Location $AppDir
docker compose down
Write-Host "BenchChef stopped."
