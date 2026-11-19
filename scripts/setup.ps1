# One-time setup for Windows (PowerShell).
# Installs uv (if missing), Python 3.14, and all project dependencies.
# Run from the project folder:
#   powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "==> Installing uv..."
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
}

Write-Host "==> Installing Python and dependencies..."
uv sync
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Setup complete. Start the app with:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\run.ps1"
Write-Host "(If 'uv' is not found in a new terminal, close and reopen the terminal.)"
