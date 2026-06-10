$ErrorActionPreference = 'Stop'

$Root = 'C:\benchchef'
$AppDir = Join-Path $Root 'app'
$DataDir = Join-Path $Root 'data'

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

function Write-ComposeEnv {
    param([string]$Path)

    $values = Read-RunEnv (Join-Path $DataDir 'run.env')
    $prometheusPort = EnvValue $values 'PROMETHEUS_PORT' '18073'
    $grafanaPort = EnvValue $values 'GRAFANA_PORT' '18074'
    $nodeExporterPort = EnvValue $values 'NODE_EXPORTER_PORT' '18075'
    $processExporterPort = EnvValue $values 'PROCESS_EXPORTER_PORT' '18076'

    @"
PROMETHEUS_PORT=$prometheusPort
GRAFANA_PORT=$grafanaPort
NODE_EXPORTER_PORT=$nodeExporterPort
PROCESS_EXPORTER_PORT=$processExporterPort
"@ | Set-Content -LiteralPath $Path -Encoding ASCII
}

function Stop-PidFile {
    param(
        [string]$Path
    )

    if (Test-Path -LiteralPath $Path) {
        $processId = Get-Content -LiteralPath $Path -ErrorAction SilentlyContinue
        if ($processId) {
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
        Remove-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    }
}

function Stop-PortListener {
    param(
        [string]$Name,
        [string]$Port
    )

    if (-not $Port) {
        return
    }

    $connections = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    foreach ($connection in $connections) {
        $processId = $connection.OwningProcess
        if ($processId) {
            Write-Host "Stopping $Name listener on port $Port with PID $processId."
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
    }
}

$values = Read-RunEnv (Join-Path $DataDir 'run.env')
$backendPort = EnvValue $values 'BENCHCHEF_BACKEND_PORT' '18071'
$frontendPort = EnvValue $values 'BENCHCHEF_FRONTEND_PORT' '18072'

foreach ($pidFileName in @('benchchef-frontend.pid', 'benchchef-backend.pid')) {
    Stop-PidFile (Join-Path $DataDir $pidFileName)
}

Stop-PortListener 'BenchChef backend' $backendPort
Stop-PortListener 'BenchChef frontend' $frontendPort

if (-not (Test-Path -LiteralPath (Join-Path $AppDir 'docker-compose.yml'))) {
    Write-Host "BenchChef app directory is not installed: $AppDir"
    exit 0
}

Set-Location $AppDir
$ComposeEnvPath = Join-Path $AppDir '.compose.env'
if (-not (Test-Path -LiteralPath $ComposeEnvPath)) {
    Write-ComposeEnv $ComposeEnvPath
}

if (Test-Path -LiteralPath $ComposeEnvPath) {
    docker compose --env-file $ComposeEnvPath down
}
else {
    docker compose down
}
Write-Host "BenchChef stopped."
