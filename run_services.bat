@echo off
REM Run MLflow UI and Uvicorn API (Windows batch)
REM Usage: run_services.bat

setlocal
set "SCRIPT_DIR=%~dp0"
set "VENV_PY=%SCRIPT_DIR%venv\Scripts\python.exe"

if not exist "%VENV_PY%" (
  echo Warning: virtualenv python not found at %VENV_PY%
)

start "MLflow" "%VENV_PY%" -m mlflow ui --port 5000
start "Uvicorn" "%VENV_PY%" -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

echo Started MLflow UI (http://localhost:5000) and Uvicorn (http://localhost:8000)
endlocal
