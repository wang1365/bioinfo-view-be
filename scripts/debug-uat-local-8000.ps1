$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repoRoot ".venv\\Scripts\\python.exe"
if (!(Test-Path $python)) { $python = "python" }

$env:DJANGO_SETTINGS_MODULE = "bioinformatics.settings.uat"
$env:WEB_PORT = "8000"

& $python "$repoRoot\\bioinformatics-analysis\\manage.py" runserver 127.0.0.1:8000

