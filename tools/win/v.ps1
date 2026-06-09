$ErrorActionPreference = 'Stop'

$Root = 'C:\benchchef'
$AppDir = Join-Path $Root 'app'
$EnvPath = Join-Path $Root 'data\run.env'

function Read-RunEnv {
    param([string]$Path)

    $values = @{}
    if (Test-Path -LiteralPath $Path) {
        Get-Content -LiteralPath $Path | ForEach-Object {
            $line = $_.Trim()
            if ($line -eq '' -or $line.StartsWith('#')) {
                return
            }
            if ($line -match '^([^=]+)=(.*)$') {
                $values[$Matches[1].Trim()] = $Matches[2].Trim()
            }
        }
    }
    return $values
}

function EnvValue {
    param([hashtable]$Values, [string]$Name, [string]$Default)

    if ($Values.ContainsKey($Name) -and $Values[$Name]) {
        return $Values[$Name]
    }
    return $Default
}

$values = Read-RunEnv $EnvPath
$ports = @{
    Backend = EnvValue $values 'BENCHCHEF_BACKEND_PORT' '18071'
    Frontend = EnvValue $values 'BENCHCHEF_FRONTEND_PORT' '18072'
    Prometheus = EnvValue $values 'PROMETHEUS_PORT' '18073'
    Grafana = EnvValue $values 'GRAFANA_PORT' '18074'
}

Write-Host "BenchChef root exists: $(Test-Path -LiteralPath $Root)"
Write-Host "App dir exists: $(Test-Path -LiteralPath $AppDir)"
Write-Host "run.env exists: $(Test-Path -LiteralPath $EnvPath)"

Write-Host ""
Write-Host "--- BenchChef processes ---"
foreach ($pidFileName in @('benchchef-backend.pid', 'benchchef-frontend.pid')) {
    $pidPath = Join-Path $Root "data\$pidFileName"
    if (Test-Path -LiteralPath $pidPath) {
        $processId = Get-Content -LiteralPath $pidPath
        $running = Get-Process -Id $processId -ErrorAction SilentlyContinue
        Write-Host "$pidFileName -> PID $processId running: $($null -ne $running)"
    }
    else {
        Write-Host "$pidFileName -> missing"
    }
}

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
