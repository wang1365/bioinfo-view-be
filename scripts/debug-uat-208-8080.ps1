param(
    [string]$SettingsModule = "bioinformatics.settings.uat",
    [string]$WebPort = "8080",
    [string]$BindAddress = "0.0.0.0",
    [string]$DisableJobRun = "1",
    [string]$AuthDisabled = ""
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repoRoot ".venv\\Scripts\\python.exe"
if (!(Test-Path $python)) { $python = "python" }

$env:DJANGO_SETTINGS_MODULE = $SettingsModule
$env:WEB_PORT = $WebPort
$env:DISABLE_JOB_RUN = $DisableJobRun
$env:PYTHONUNBUFFERED = "1"
if ($AuthDisabled -ne "") { $env:AUTH_DISABLED = $AuthDisabled }

& $python "$repoRoot\\bioinformatics-analysis\\manage.py" runserver "$BindAddress`:$WebPort"
