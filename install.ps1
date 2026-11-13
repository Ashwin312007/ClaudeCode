# =========================================================
# Claude Code Multi-Provider Harness Installer (PowerShell)
# =========================================================

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$TargetClaude = "$HOME\.claude"
$TargetBin = "$HOME\.local\bin"

Write-Host "`n=========================================================" -ForegroundColor Cyan
Write-Host "   Claude Code Multi-Provider Harness Installer" -ForegroundColor Cyan
Write-Host "=========================================================`n" -ForegroundColor Cyan

# 1. Directories
Write-Host "[1/4] Ensuring directories exist..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $TargetClaude -Force | Out-Null
New-Item -ItemType Directory -Path $TargetBin -Force | Out-Null

# 2. Copy .claude
Write-Host "[2/4] Copying config files to $TargetClaude..." -ForegroundColor Yellow
Copy-Item "$ScriptDir\.claude\*" -Destination $TargetClaude -Recurse -Force
if (-not (Test-Path "$TargetClaude\.env")) {
    Copy-Item "$ScriptDir\.claude\.env.example" -Destination "$TargetClaude\.env" -Force
    Write-Host "[OK] Created $TargetClaude\.env from template." -ForegroundColor Green
}

# 3. Copy bin
Write-Host "[3/4] Copying launcher scripts to $TargetBin..." -ForegroundColor Yellow
Copy-Item "$ScriptDir\bin\*" -Destination $TargetBin -Recurse -Force

# 4. PATH check
Write-Host "[4/4] Checking PATH..." -ForegroundColor Yellow
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*$TargetBin*") {
    Write-Host "Adding $TargetBin to User PATH..." -ForegroundColor Green
    $NewPath = if ($UserPath) { "$UserPath;$TargetBin" } else { $TargetBin }
    [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
    Write-Host "[OK] Added to User PATH. Reopen terminal to refresh." -ForegroundColor Green
} else {
    Write-Host "[OK] $TargetBin is already in User PATH." -ForegroundColor Green
}

Write-Host "`n=========================================================" -ForegroundColor Green
Write-Host "   Installation Successful!" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
Write-Host "`nNext Steps:"
Write-Host "  1. set-nvidia-key <key>  - Insert your NVIDIA NIM key" -ForegroundColor Cyan
Write-Host "  2. start-claude-gateway  - Start the background translation proxy" -ForegroundColor Cyan
Write-Host "  3. claude                - Run Claude Code" -ForegroundColor Cyan
Write-Host "  4. cm                    - Open the interactive model picker" -ForegroundColor Cyan
Write-Host ""
