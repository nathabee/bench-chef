$ErrorActionPreference = 'Stop'

$Root = 'C:\benchchef'
$AppDir = Join-Path $Root 'app'
$DataDir = Join-Path $Root 'data'

foreach ($pidFileName in @('benchchef-frontend.pid', 'benchchef-backend.pid')) {
    $pidPath = Join-Path $DataDir $pidFileName
    if (Test-Path -LiteralPath $pidPath) {
        $processId = Get-Content -LiteralPath $pidPath -ErrorAction SilentlyContinue
        if ($processId) {
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
        Remove-Item -LiteralPath $pidPath -Force -ErrorAction SilentlyContinue
    }
}

if (-not (Test-Path -LiteralPath (Join-Path $AppDir 'docker-compose.yml'))) {
    Write-Host "BenchChef app directory is not installed: $AppDir"
    exit 0
}

Set-Location $AppDir
$ComposeEnvPath = Join-Path $AppDir '.compose.env'
if (Test-Path -LiteralPath $ComposeEnvPath) {
    docker compose --env-file $ComposeEnvPath down
}
else {
    docker compose down
}
Write-Host "BenchChef stopped."
