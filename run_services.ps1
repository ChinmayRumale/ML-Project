#!/usr/bin/env pwsh
# Run MLflow UI and Uvicorn API concurrently (PowerShell)
# Usage: .\run_services.ps1

$ErrorActionPreference = "Stop"

# Resolve script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Path to the venv python executable (assumes venv at repo root)
$venvPython = Join-Path $scriptDir "venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Warning: venv python not found at $venvPython. Ensure your virtualenv is created and adjust the script." -ForegroundColor Yellow
}

# Start MLflow UI
Start-Process -FilePath $venvPython -ArgumentList "-m mlflow ui --port 5000" -WorkingDirectory $scriptDir

# Start Uvicorn (FastAPI)
Start-Process -FilePath $venvPython -ArgumentList "-m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000" -WorkingDirectory $scriptDir

Write-Host "Started MLflow UI (http://localhost:5000) and Uvicorn (http://localhost:8000)."
