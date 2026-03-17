@echo off
setlocal

REM Start backend in local debug mode with UAT profile
set "REPO_ROOT=%~dp0"
set "PYTHON=%REPO_ROOT%.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
  set "PYTHON=python"
)

set "DJANGO_SETTINGS_MODULE=bioinformatics.settings.uat"
set "WEB_PORT=8000"

echo [start_dev] PYTHON=%PYTHON%
echo [start_dev] DJANGO_SETTINGS_MODULE=%DJANGO_SETTINGS_MODULE%
echo [start_dev] WEB_PORT=%WEB_PORT%

echo [start_dev] Starting Django server...
"%PYTHON%" "%REPO_ROOT%bioinformatics-analysis\manage.py" runserver 127.0.0.1:%WEB_PORT%

endlocal
