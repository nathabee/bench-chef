param(
    [Parameter(Mandatory = $true)]
    [string]$Version,

    [string]$Owner = 'nathabee',
    [string]$Repo = 'bench-chef'
)

$ErrorActionPreference = 'Stop'

$Root = 'C:\benchchef'
$AppDir = Join-Path $Root 'app'
$BinDir = Join-Path $Root 'bin'
$DataDir = Join-Path $Root 'data'
$LogDir = Join-Path $Root 'log'
$RelDir = Join-Path $Root 'rel'
$TmpDir = Join-Path $Root 'tmp'

foreach ($dir in @($AppDir, $BinDir, $DataDir, $LogDir, $RelDir, $TmpDir)) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

$TagName = "v$Version"
$AssetName = "bench-chef-$Version-windows.zip"
$DownloadUrl = "https://github.com/$Owner/$Repo/releases/download/$TagName/$AssetName"
$ZipPath = Join-Path $RelDir $AssetName
$ExtractDir = Join-Path $TmpDir "bench-chef-$Version"

Write-Host "Downloading $DownloadUrl"
Invoke-WebRequest -Uri $DownloadUrl -OutFile $ZipPath

if (Test-Path -LiteralPath $ExtractDir) {
    Remove-Item -LiteralPath $ExtractDir -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $ExtractDir | Out-Null
Expand-Archive -LiteralPath $ZipPath -DestinationPath $ExtractDir -Force

$SourceDir = Join-Path $ExtractDir 'bench-chef'
if (-not (Test-Path -LiteralPath (Join-Path $SourceDir 'docker-compose.yml'))) {
    Write-Error "Release package does not contain bench-chef/docker-compose.yml"
    exit 1
}

if (Test-Path -LiteralPath (Join-Path $BinDir 's.ps1')) {
    & (Join-Path $BinDir 's.ps1')
}

if (Test-Path -LiteralPath $AppDir) {
    Get-ChildItem -LiteralPath $AppDir -Force | Remove-Item -Recurse -Force
}

Copy-Item -LiteralPath (Join-Path $SourceDir '*') -Destination $AppDir -Recurse -Force

$AdminUrl = "https://github.com/$Owner/$Repo/releases/download/$TagName/bench-chef-$Version-admin.zip"
$AdminZip = Join-Path $RelDir "bench-chef-$Version-admin.zip"
try {
    Invoke-WebRequest -Uri $AdminUrl -OutFile $AdminZip
    $AdminExtractDir = Join-Path $TmpDir "bench-chef-$Version-admin"
    if (Test-Path -LiteralPath $AdminExtractDir) {
        Remove-Item -LiteralPath $AdminExtractDir -Recurse -Force
    }
    Expand-Archive -LiteralPath $AdminZip -DestinationPath $AdminExtractDir -Force
    Copy-Item -LiteralPath (Join-Path $AdminExtractDir 'admin\win\*') -Destination $BinDir -Recurse -Force
    if (Test-Path -LiteralPath (Join-Path $AdminExtractDir 'admin\data\run.env.example')) {
        Copy-Item -LiteralPath (Join-Path $AdminExtractDir 'admin\data\run.env.example') -Destination (Join-Path $DataDir 'run.env.example') -Force
    }
}
catch {
    Write-Warning "Could not download admin package: $($_.Exception.Message)"
}

if (-not (Test-Path -LiteralPath (Join-Path $DataDir 'run.env'))) {
    if (Test-Path -LiteralPath (Join-Path $DataDir 'run.env.example')) {
        Copy-Item -LiteralPath (Join-Path $DataDir 'run.env.example') -Destination (Join-Path $DataDir 'run.env') -Force
    }
    else {
        Copy-Item -LiteralPath (Join-Path $BinDir 'run.env.example') -Destination (Join-Path $DataDir 'run.env') -Force
    }
}

& (Join-Path $BinDir 'r.ps1')
Write-Host "BenchChef update complete for version $Version"
