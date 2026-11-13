@echo off
setlocal

set "CHOOSE_SCRIPT=%USERPROFILE%\.claude\choose_model.py"
if not exist "%CHOOSE_SCRIPT%" set "CHOOSE_SCRIPT=%~dp0..\.claude\choose_model.py"

python "%CHOOSE_SCRIPT%" %*

endlocal
