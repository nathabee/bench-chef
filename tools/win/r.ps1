$ErrorActionPreference = 'Stop'

$Root = 'C:\benchchef'
$AppDir = Join-Path $Root 'app'
$DataDir = Join-Path $Root 'data'
$LogDir = Join-Path $Root 'log'
$RunLog = Join-Path $LogDir 'start.log'
$EnvPath = Join-Path $DataDir 'run.env'
$AppEnvPath = Join-Path $AppDir '.env'

function Read-RunEnv {
    param(
        [string]$Path
    )

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
    param(
        [hashtable]$Values,
        [string]$Name,
        [string]$Default
    )

    if ($Values.ContainsKey($Name) -and $Values[$Name]) {
        return $Values[$Name]
    }
    return $Default
}

function Write-FrontendConfig {
    param(
        [string]$Path,
        [hashtable]$Values
    )

    $backendPort = EnvValue $Values 'BENCHCHEF_BACKEND_PORT' '18071'
    $frontendPort = EnvValue $Values 'BENCHCHEF_FRONTEND_PORT' '18072'
    $prometheusPort = EnvValue $Values 'PROMETHEUS_PORT' '18073'
    $grafanaPort = EnvValue $Values 'GRAFANA_PORT' '18074'
    $spaghettiChefUrl = EnvValue $Values 'SPAGHETTICHEF_BASE_URL' 'http://localhost:18080'

    @"
window.BenchChefConfig = {
  backendUrl: 'http://localhost:$backendPort',
  frontendUrl: 'http://localhost:$frontendPort',
  prometheusUrl: 'http://localhost:$prometheusPort',
  grafanaUrl: 'http://localhost:$grafanaPort',
  spaghettiChefUrl: '$spaghettiChefUrl',
};
"@ | Set-Content -LiteralPath $Path -Encoding UTF8
}

function Start-BackgroundProcess {
    param(
        [string]$Name,
        [string]$FilePath,
        [string[]]$ArgumentList,
        [string]$WorkingDirectory,
        [string]$LogPath,
        [string]$PidPath
    )

    $errorLogPath = "$LogPath.err"

    $process = Start-Process `
        -FilePath $FilePath `
        -ArgumentList $ArgumentList `
        -WorkingDirectory $WorkingDirectory `
        -RedirectStandardOutput $LogPath `
        -RedirectStandardError $errorLogPath `
        -PassThru `
        -WindowStyle Hidden

    $process.Id | Set-Content -LiteralPath $PidPath
    Write-Host "$Name started with PID $($process.Id)."
}

New-Item -ItemType Directory -Force -Path $DataDir | Out-Null
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

if (-not (Test-Path -LiteralPath (Join-Path $AppDir 'docker-compose.yml'))) {
    Write-Error "BenchChef app directory is missing docker-compose.yml: $AppDir"
    exit 1
}

if (-not (Test-Path -LiteralPath $EnvPath)) {
    $examplePath = Join-Path $DataDir 'run.env.example'
    $legacyExamplePath = Join-Path $Root 'bin\run.env.example'
    $appExamplePath = Join-Path $AppDir '.env.example'
    if (Test-Path -LiteralPath $examplePath) {
        Copy-Item -LiteralPath $examplePath -Destination $EnvPath -Force
    }
    elseif (Test-Path -LiteralPath $legacyExamplePath) {
        Copy-Item -LiteralPath $legacyExamplePath -Destination $EnvPath -Force
    }
    elseif (Test-Path -LiteralPath $appExamplePath) {
        Copy-Item -LiteralPath $appExamplePath -Destination $EnvPath -Force
    }
    else {
        Write-Error "Missing run.env. Expected $EnvPath or $examplePath"
        exit 1
    }
}

$values = Read-RunEnv $EnvPath
$backendPort = EnvValue $values 'BENCHCHEF_BACKEND_PORT' '18071'
$frontendPort = EnvValue $values 'BENCHCHEF_FRONTEND_PORT' '18072'
$spaghettiChefUrl = (EnvValue $values 'SPAGHETTICHEF_BASE_URL' 'http://localhost:18080').TrimEnd('/')

Copy-Item -LiteralPath $EnvPath -Destination $AppEnvPath -Force

"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] starting BenchChef" | Add-Content -LiteralPath $RunLog

try {
    Invoke-WebRequest -Uri "$spaghettiChefUrl/health" -UseBasicParsing -TimeoutSec 2 | Out-Null
    Write-Host "SpaghettiChef is reachable at $spaghettiChefUrl."
}
catch {
    Write-Host "SpaghettiChef is not available at $spaghettiChefUrl."
    Write-Host "BenchChef will start, but probes will fail until SpaghettiChef is running."
}

Set-Location $AppDir
docker compose up -d --no-deps prometheus grafana | Tee-Object -FilePath $RunLog -Append

$backendDir = Join-Path $AppDir 'backend-django'
$managePy = Join-Path $backendDir 'manage.py'
$venvPython = Join-Path $backendDir '.venv\Scripts\python.exe'
$requirementsMarker = Join-Path $backendDir '.venv\.benchchef-requirements-installed'

if (-not (Test-Path -LiteralPath $venvPython)) {
    Write-Host "Creating BenchChef backend Python virtual environment..."
    python -m venv (Join-Path $backendDir '.venv')
}

if (-not (Test-Path -LiteralPath $requirementsMarker)) {
    Write-Host "Installing BenchChef backend Python dependencies..."
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install -r (Join-Path $backendDir 'requirements.txt')
    New-Item -ItemType File -Force -Path $requirementsMarker | Out-Null
}

Write-Host "Applying BenchChef database migrations..."
& $venvPython $managePy migrate --noinput

Write-Host "Initializing default SpaghettiChef connection profile..."
& $venvPython $managePy init_default_connection

Start-BackgroundProcess `
    -Name 'BenchChef backend' `
    -FilePath $venvPython `
    -ArgumentList @($managePy, 'runserver', "0.0.0.0:$backendPort") `
    -WorkingDirectory $backendDir `
    -LogPath (Join-Path $LogDir 'backend.log') `
    -PidPath (Join-Path $DataDir 'benchchef-backend.pid')

$frontendDistDir = Join-Path $AppDir 'dist\frontend-angular\browser'
$frontendConfig = Join-Path $frontendDistDir 'benchchef-config.js'
if (-not (Test-Path -LiteralPath (Join-Path $frontendDistDir 'index.html'))) {
    Write-Error "BenchChef frontend build not found at $frontendDistDir"
    exit 1
}

Write-FrontendConfig -Path $frontendConfig -Values $values

Start-BackgroundProcess `
    -Name 'BenchChef frontend' `
    -FilePath 'python' `
    -ArgumentList @((Join-Path $AppDir 'scripts\serve_frontend.py'), $frontendDistDir, $frontendPort) `
    -WorkingDirectory $AppDir `
    -LogPath (Join-Path $LogDir 'frontend.log') `
    -PidPath (Join-Path $DataDir 'benchchef-frontend.pid')

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
Write-Host "Frontend: http://localhost:$frontendPort"
Write-Host "Backend: http://localhost:$backendPort"
