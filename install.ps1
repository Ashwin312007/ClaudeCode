<#
.SYNOPSIS
    Installer script for Claude Code Free Models Harness
#>
$ErrorActionPreference = "Stop"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "   Claude Code Free Models Harness Installer (PowerShell)" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetClaude = Join-Path $HOME ".claude"
$TargetBin = Join-Path $HOME ".local\bin"
$TargetProxy = Join-Path $TargetClaude "proxy"

# Step 1: Check Python and uv
Write-Host "[1/5] Checking prerequisites..." -ForegroundColor Yellow
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH! Please install Python 3.11+."
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[INFO] Installing 'uv' package manager via pip..." -ForegroundColor Yellow
    python -m pip install uv
}

# Step 2: Create directories
Write-Host "[2/5] Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $TargetClaude | Out-Null
New-Item -ItemType Directory -Force -Path $TargetBin | Out-Null
New-Item -ItemType Directory -Force -Path $TargetProxy | Out-Null

# Step 3: Copy proxy engine
Write-Host "[3/5] Deploying Tool-Enabled Gateway Proxy..." -ForegroundColor Yellow
Copy-Item -Path "$ScriptDir\proxy\*" -Destination $TargetProxy -Recurse -Force

if (-not (Test-Path "$TargetProxy\.env")) {
    if (Test-Path "$TargetProxy\.env.example") {
        Copy-Item -Path "$TargetProxy\.env.example" -Destination "$TargetProxy\.env" -Force
        Write-Host "[OK] Created $TargetProxy\.env from template." -ForegroundColor Green
    }
}

# Step 4: Install dependencies with uv sync
Write-Host "[4/5] Installing proxy dependencies via uv..." -ForegroundColor Yellow
Push-Location $TargetProxy
try {
    uv sync
    Write-Host "[OK] Python dependencies installed successfully." -ForegroundColor Green
} catch {
    Write-Warning "uv sync failed directly, trying python -m uv sync..."
    python -m uv sync
}
Pop-Location

# Step 5: Deploy config and launcher scripts
Write-Host "[5/5] Deploying scripts and Claude Code settings..." -ForegroundColor Yellow
Copy-Item -Path "$ScriptDir\.claude\settings.json" -Destination $TargetClaude -Force
Copy-Item -Path "$ScriptDir\.claude\choose_model.py" -Destination $TargetClaude -Force
Copy-Item -Path "$ScriptDir\.claude\set_nvidia_key.py" -Destination $TargetClaude -Force

Copy-Item -Path "$ScriptDir\bin\start-claude-gateway.cmd" -Destination $TargetBin -Force
Copy-Item -Path "$ScriptDir\bin\claude-model.cmd" -Destination $TargetBin -Force
Copy-Item -Path "$ScriptDir\bin\set-nvidia-key.cmd" -Destination $TargetBin -Force
Copy-Item -Path "$ScriptDir\bin\cm.cmd" -Destination $TargetBin -Force

# PATH check
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*$TargetBin*") {
    Write-Host "Adding $TargetBin to User PATH..." -ForegroundColor Yellow
    [Environment]::SetEnvironmentVariable("Path", "$UserPath;$TargetBin", "User")
    Write-Host "[OK] Added to User PATH. Reopen your terminal after installation!" -ForegroundColor Green
} else {
    Write-Host "[OK] $TargetBin is already in PATH." -ForegroundColor Green
}

Write-Host ""
Write-Host "=========================================================" -ForegroundColor Green
Write-Host "   Installation Complete!" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
Write-Host " Commands available in any terminal:"
Write-Host "   1. start-claude-gateway  - Starts the gateway on port 8082"
Write-Host "   2. claude-model (or cm)  - Interactively switch active models"
Write-Host "   3. set-nvidia-key        - Updates your NVIDIA NIM API key"
Write-Host "   4. claude                - Launch Claude Code with free models"
Write-Host "========================================================="
