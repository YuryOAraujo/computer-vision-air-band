@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Execute preparar_windows.bat primeiro.
  pause
  exit /b 1
)
set "AIRBAND_STAGE=%~1"
if "%AIRBAND_STAGE%"=="" (
  if exist "versions\instructor\project.py" (
    set "AIRBAND_STAGE=instructor"
  ) else (
    if exist "versions\starter\project.py" (
      set "AIRBAND_STAGE=starter"
    ) else (
      set "AIRBAND_STAGE=day1"
    )
  )
)
set "AIRBAND_INPUT=%~2"
if "%AIRBAND_INPUT%"=="" set "AIRBAND_INPUT=camera"
".venv\Scripts\python.exe" app.py --version "%AIRBAND_STAGE%" --input "%AIRBAND_INPUT%"
if errorlevel 1 (
  pause
  exit /b 1
)

