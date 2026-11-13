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

rem Free port 8082 if an old instance is still running
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr /r ":8082 " ^| findstr LISTENING') do (
    echo [INFO] Releasing port 8082 from previous process (PID %%a)...
    taskkill /f /pid %%a >nul 2>&1
)

cd /d "%PROXY_DIR%"

echo [Gateway] Running from: %PROXY_DIR%
echo [Gateway] Local Anthropic Endpoint: http://127.0.0.1:8082
echo [Gateway] Starting server...

uv run python -m uvicorn server:app --host 127.0.0.1 --port 8082
