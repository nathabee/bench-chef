$ErrorActionPreference = 'Stop'

$TaskName = 'BenchChef'
$Root = 'C:\benchchef'
$BinDir = Join-Path $Root 'bin'
$RunScript = Join-Path $BinDir 'r.ps1'
$TaskCmd = Join-Path $BinDir 'benchchef-task.cmd'

if (-not (Test-Path -LiteralPath $RunScript)) {
    Write-Error "Start script not found: $RunScript"
    exit 1
}

@"
@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\benchchef\bin\r.ps1" >> C:\benchchef\log\benchchef-task-out.log 2>> C:\benchchef\log\benchchef-task-err.log
"@ | Set-Content -LiteralPath $TaskCmd -Encoding ASCII

$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
cmd.exe /c "schtasks /Query /TN BenchChef >NUL 2>NUL"
$TaskExists = ($LASTEXITCODE -eq 0)

if ($TaskExists) {
    Write-Host "Scheduled task '$TaskName' already exists."
    Write-Host "Keeping existing task owner/principal unchanged."
    exit 0
}

schtasks /Create /F /TN $TaskName /SC ONLOGON /TR $TaskCmd /RU $CurrentUser | Out-Null
Write-Host "Scheduled task '$TaskName' registered for $CurrentUser."
