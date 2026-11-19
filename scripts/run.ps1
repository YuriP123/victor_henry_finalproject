# Start the app on Windows (PowerShell). Opens at http://localhost:8501
#   powershell -ExecutionPolicy Bypass -File scripts\run.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv is not installed. Run scripts\setup.ps1 first."
    exit 1
}

uv run streamlit run streamlit_app.py @args
