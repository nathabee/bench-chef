$ErrorActionPreference = 'Stop'

$Root = 'C:\benchchef'
$AppDir = Join-Path $Root 'app'
$EnvPath = Join-Path $Root 'data\run.env'

$ports = @{
    Backend = '18071'
    Frontend = '18072'
    Prometheus = '18073'
    Grafana = '18074'
}

if (Test-Path -LiteralPath $EnvPath) {
    Get-Content -LiteralPath $EnvPath | ForEach-Object {
        if ($_ -match '^BENCHCHEF_BACKEND_PORT=(.+)$') { $ports.Backend = $Matches[1].Trim() }
        if ($_ -match '^BENCHCHEF_FRONTEND_PORT=(.+)$') { $ports.Frontend = $Matches[1].Trim() }
        if ($_ -match '^PROMETHEUS_PORT=(.+)$') { $ports.Prometheus = $Matches[1].Trim() }
        if ($_ -match '^GRAFANA_PORT=(.+)$') { $ports.Grafana = $Matches[1].Trim() }
    }
}

Write-Host "BenchChef root exists: $(Test-Path -LiteralPath $Root)"
Write-Host "App dir exists: $(Test-Path -LiteralPath $AppDir)"
Write-Host "run.env exists: $(Test-Path -LiteralPath $EnvPath)"

Write-Host ""
Write-Host "--- Docker Compose ---"
if (Test-Path -LiteralPath (Join-Path $AppDir 'docker-compose.yml')) {
    Set-Location $AppDir
    docker compose ps
}
else {
    Write-Host "docker-compose.yml not found."
}

Write-Host ""
Write-Host "--- HTTP checks ---"
foreach ($name in $ports.Keys) {
    $port = $ports[$name]
    try {
        $resp = Invoke-WebRequest -Uri "http://localhost:$port/" -UseBasicParsing -TimeoutSec 3
        Write-Host "$name http://localhost:$port -> HTTP $($resp.StatusCode)"
    }
    catch {
        Write-Host "$name http://localhost:$port -> not reachable"
    }
}
