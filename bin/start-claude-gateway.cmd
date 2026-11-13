@echo off
setlocal enabledelayedexpansion

echo =========================================================
echo    Starting Claude Code Tool Gateway on port 8082...
echo =========================================================

set "SCRIPT_DIR=%~dp0"
set "PROXY_DIR=%SCRIPT_DIR%..\proxy"
if not exist "%PROXY_DIR%\server.py" set "PROXY_DIR=%USERPROFILE%\.claude\proxy"

if not exist "%PROXY_DIR%\server.py" (
    echo [ERROR] Proxy directory not found at "%PROXY_DIR%"!
    echo Please run install.bat or install.ps1 first.
    exit /b 1
)

cd /d "%PROXY_DIR%"

echo [Gateway] Running from: %PROXY_DIR%
echo [Gateway] Local Anthropic Endpoint: http://127.0.0.1:8082
echo [Gateway] Starting server...

uv run python -m uvicorn server:app --host 127.0.0.1 --port 8082
