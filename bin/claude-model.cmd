@echo off
setlocal

set "PYTHON_EXE=python"
set "CHOOSE_SCRIPT=C:\Users\teash\.claude\choose_model.py"
set "CLAUDE_EXE=C:\Users\teash\.local\bin\claude.exe"

if "%~1"=="" (
    for /f "delims=" %%i in ('%PYTHON_EXE% "%CHOOSE_SCRIPT%"') do set "CHOSEN_MODEL=%%i"
    goto launch
)

rem Check if first argument is a model or a flag
echo %~1 | findstr /r "^-" >nul
if errorlevel 1 (
    rem First argument is a model name
    %PYTHON_EXE% "%CHOOSE_SCRIPT%" "%~1"
    set "CHOSEN_MODEL=%~1"
    shift
    goto launch_with_args
) else (
    rem Arguments are flags for claude
    goto launch_direct
)

:launch
if "%CHOSEN_MODEL%"=="" goto end
echo Launching Claude Code with %CHOSEN_MODEL%...
"%CLAUDE_EXE%" --model "%CHOSEN_MODEL%"
goto end

:launch_with_args
echo Launching Claude Code with %CHOSEN_MODEL%...
"%CLAUDE_EXE%" --model "%CHOSEN_MODEL%" %1 %2 %3 %4 %5 %6 %7 %8 %9
goto end

:launch_direct
"%CLAUDE_EXE%" %*
goto end

:end
endlocal
