@echo off
setlocal enabledelayedexpansion

echo =========================================================
echo    Claude Code Free Models Harness Installer
echo =========================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "TARGET_CLAUDE=%USERPROFILE%\.claude"
set "TARGET_BIN=%USERPROFILE%\.local\bin"
set "TARGET_PROXY=%TARGET_CLAUDE%\proxy"

echo [1/5] Checking prerequisites...
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not found in PATH! Please install Python 3.11+.
    exit /b 1
)

where uv >nul 2>nul
if errorlevel 1 (
    echo [INFO] Installing 'uv' package manager via pip...
    python -m pip install uv
    if errorlevel 1 (
        echo [ERROR] Failed to install uv. Please install uv manually.
        exit /b 1
    )
)

echo [2/5] Creating directories...
if not exist "%TARGET_CLAUDE%" mkdir "%TARGET_CLAUDE%"
if not exist "%TARGET_BIN%" mkdir "%TARGET_BIN%"
if not exist "%TARGET_PROXY%" mkdir "%TARGET_PROXY%"

echo [3/5] Deploying Tool-Enabled Gateway Proxy...
xcopy /E /I /Y /Q "%SCRIPT_DIR%proxy\*" "%TARGET_PROXY%\" >nul

if not exist "%TARGET_PROXY%\.env" (
    if exist "%TARGET_PROXY%\.env.example" (
        copy /Y "%TARGET_PROXY%\.env.example" "%TARGET_PROXY%\.env" >nul
        echo [OK] Created %TARGET_PROXY%\.env from template.
    )
)

echo [4/5] Installing proxy dependencies via uv...
cd /d "%TARGET_PROXY%"
call uv sync
if errorlevel 1 (
    echo [WARN] uv sync failed, retrying via python -m uv sync...
    python -m uv sync
)

echo [5/5] Deploying scripts and Claude Code settings...
copy /Y "%SCRIPT_DIR%.claude\settings.json" "%TARGET_CLAUDE%\" >nul
copy /Y "%SCRIPT_DIR%.claude\choose_model.py" "%TARGET_CLAUDE%\" >nul
copy /Y "%SCRIPT_DIR%.claude\set_nvidia_key.py" "%TARGET_CLAUDE%\" >nul

copy /Y "%SCRIPT_DIR%bin\start-claude-gateway.cmd" "%TARGET_BIN%\" >nul
copy /Y "%SCRIPT_DIR%bin\claude-model.cmd" "%TARGET_BIN%\" >nul
copy /Y "%SCRIPT_DIR%bin\set-nvidia-key.cmd" "%TARGET_BIN%\" >nul
copy /Y "%SCRIPT_DIR%bin\cm.cmd" "%TARGET_BIN%\" >nul

rem Verify PATH
echo %PATH% | findstr /I /C:"%TARGET_BIN%" >nul
if errorlevel 1 (
    echo Adding %TARGET_BIN% to User PATH...
    for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%b"
    if defined USER_PATH (
        setx PATH "!USER_PATH!;%TARGET_BIN%" >nul
    ) else (
        setx PATH "%TARGET_BIN%" >nul
    )
    echo [OK] Added to User PATH. Reopen your terminal after installation!
) else (
    echo [OK] %TARGET_BIN% is already in PATH.
)

echo.
echo =========================================================
echo    Installation Complete!
echo =========================================================
echo  Commands available in any terminal:
echo    1. start-claude-gateway  - Starts the gateway on port 8082
echo    2. claude-model (or cm)  - Interactively switch active models
echo    3. set-nvidia-key        - Updates your NVIDIA NIM API key
echo    4. claude                - Launch Claude Code with free models
echo =========================================================
