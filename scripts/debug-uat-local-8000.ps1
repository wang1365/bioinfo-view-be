param(
    [string]$SettingsModule = "bioinformatics.settings.uat",
    [string]$WebPort = "8000",
    [string]$BindAddress = "127.0.0.1",
    [string]$DisableJobRun = "1",
    [string]$DbConnMaxAge = "0",
    [switch]$NoReload = $false,
    [switch]$NoThreading = $true,
    [string]$AuthDisabled = ""
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repoRoot ".venv\\Scripts\\python.exe"
if (!(Test-Path $python)) { $python = "python" }

$env:DJANGO_SETTINGS_MODULE = $SettingsModule
$env:WEB_PORT = $WebPort
$env:DISABLE_JOB_RUN = $DisableJobRun
$env:DB_CONN_MAX_AGE = $DbConnMaxAge
$env:PYTHONUNBUFFERED = "1"
if ($AuthDisabled -ne "") { $env:AUTH_DISABLED = $AuthDisabled }

$managePy = "$repoRoot\\bioinformatics-analysis\\manage.py"
$runserverArgs = @("runserver", "$BindAddress`:$WebPort")
if ($NoReload) { $runserverArgs += "--noreload" }
if ($NoThreading) { $runserverArgs += "--nothreading" }

Write-Host "[debug-uat-local] DJANGO_SETTINGS_MODULE=$env:DJANGO_SETTINGS_MODULE"
Write-Host "[debug-uat-local] DISABLE_JOB_RUN=$env:DISABLE_JOB_RUN"
Write-Host "[debug-uat-local] DB_CONN_MAX_AGE=$env:DB_CONN_MAX_AGE"
Write-Host "[debug-uat-local] runserver args: $($runserverArgs -join ' ')"

& $python $managePy @runserverArgs
