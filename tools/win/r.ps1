$ErrorActionPreference = 'Stop'

$Root = 'C:\benchchef'
$AppDir = Join-Path $Root 'app'
$LogDir = Join-Path $Root 'log'
$RunLog = Join-Path $LogDir 'start.log'

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

if (-not (Test-Path -LiteralPath (Join-Path $AppDir 'docker-compose.yml'))) {
    Write-Error "BenchChef app directory is missing docker-compose.yml: $AppDir"
    exit 1
}

Set-Location $AppDir
"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] starting BenchChef" | Add-Content -LiteralPath $RunLog

docker compose up -d | Tee-Object -FilePath $RunLog -Append

$backendPort = '18071'
$envPath = Join-Path $Root 'data\run.env'
if (Test-Path -LiteralPath $envPath) {
    Get-Content -LiteralPath $envPath | ForEach-Object {
        if ($_ -match '^BENCHCHEF_BACKEND_PORT=(.+)$') {
            $backendPort = $Matches[1].Trim()
        }
    }
}

$healthy = $false
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    try {
        $resp = Invoke-WebRequest -Uri "http://localhost:$backendPort/" -UseBasicParsing -TimeoutSec 2
        if ($resp.StatusCode -eq 200) {
            $healthy = $true
            break
        }
    }
    catch {
    }
}

if (-not $healthy) {
    Write-Error "BenchChef backend did not become reachable on port $backendPort"
    exit 1
}

Write-Host "BenchChef started."
Write-Host "Backend: http://localhost:$backendPort"
