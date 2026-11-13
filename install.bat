@echo off
setlocal enabledelayedexpansion

echo =========================================================
echo    Claude Code Multi-Provider Harness Installer
echo =========================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "TARGET_CLAUDE=%USERPROFILE%\.claude"
set "TARGET_BIN=%USERPROFILE%\.local\bin"

echo [1/4] Creating destination directories...
if not exist "%TARGET_CLAUDE%" mkdir "%TARGET_CLAUDE%"
if not exist "%TARGET_BIN%" mkdir "%TARGET_BIN%"

echo [2/4] Copying configuration files to %TARGET_CLAUDE%...
copy /Y "%SCRIPT_DIR%.claude\litellm-config.yaml" "%TARGET_CLAUDE%\" >nul
copy /Y "%SCRIPT_DIR%.claude\settings.json" "%TARGET_CLAUDE%\" >nul
copy /Y "%SCRIPT_DIR%.claude\switch_provider.py" "%TARGET_CLAUDE%\" >nul
copy /Y "%SCRIPT_DIR%.claude\choose_model.py" "%TARGET_CLAUDE%\" >nul
copy /Y "%SCRIPT_DIR%.claude\set_nvidia_key.py" "%TARGET_CLAUDE%\" >nul
copy /Y "%SCRIPT_DIR%.claude\.env.example" "%TARGET_CLAUDE%\" >nul

if not exist "%TARGET_CLAUDE%\.env" (
    copy /Y "%SCRIPT_DIR%.claude\.env.example" "%TARGET_CLAUDE%\.env" >nul
    echo [OK] Created %TARGET_CLAUDE%\.env from template.
)

echo [3/4] Copying launcher scripts to %TARGET_BIN%...
copy /Y "%SCRIPT_DIR%bin\start-claude-gateway.cmd" "%TARGET_BIN%\" >nul
copy /Y "%SCRIPT_DIR%bin\claude-model.cmd" "%TARGET_BIN%\" >nul
copy /Y "%SCRIPT_DIR%bin\claude-provider.cmd" "%TARGET_BIN%\" >nul
copy /Y "%SCRIPT_DIR%bin\set-nvidia-key.cmd" "%TARGET_BIN%\" >nul
copy /Y "%SCRIPT_DIR%bin\cm.cmd" "%TARGET_BIN%\" >nul

echo [4/4] Verifying PATH environment variable...
echo %PATH% | findstr /I /C:"%TARGET_BIN%" >nul
if errorlevel 1 (
    echo Adding %TARGET_BIN% to User PATH...
    for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%b"
    if defined USER_PATH (
        setx PATH "!USER_PATH!;%TARGET_BIN%" >nul
    ) else (
        setx PATH "%TARGET_BIN%" >nul
    )
    echo [OK] Added to User PATH. Note: Reopen your terminal for PATH changes to take effect.
) else (
    echo [OK] %TARGET_BIN% is already in PATH.
)

echo.
echo =========================================================
echo    Installation Complete!
echo =========================================================
echo.
echo Quick Start:
echo   1. Set your NVIDIA API key:  set-nvidia-key ^<your-nvapi-key^>
echo   2. Start the gateway:        start-claude-gateway
echo   3. Run Claude Code:          claude
echo   4. Switch models:            cm  (or claude-model)
echo.
pause
