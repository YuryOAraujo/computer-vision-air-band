@echo off
setlocal
cd /d "%~dp0"
echo Preparando Air Band Lab com Python 3.12 de 64 bits...
py -3.12 -c "import struct; assert struct.calcsize('P') == 8, 'Instale Python de 64 bits'"
if errorlevel 1 goto :erro
if not exist ".venv\Scripts\python.exe" py -3.12 -m venv .venv
if errorlevel 1 goto :erro
".venv\Scripts\python.exe" -c "import sys, struct; assert sys.version_info[:2] == (3, 12) and struct.calcsize('P') == 8, 'O ambiente .venv precisa usar Python 3.12 de 64 bits'"
if errorlevel 1 goto :erro
if exist "wheelhouse" (
  ".venv\Scripts\python.exe" -m pip install --no-index --find-links=wheelhouse --only-binary=:all: -r requirements-lock.txt
) else (
  ".venv\Scripts\python.exe" -m pip install --only-binary=:all: -r requirements-lock.txt
)
if errorlevel 1 goto :erro
".venv\Scripts\python.exe" scripts\generate_sounds.py
if errorlevel 1 goto :erro
".venv\Scripts\python.exe" scripts\prepare_model.py
if errorlevel 1 goto :erro
echo Pronto. Execute iniciar_windows.bat ou consulte README.md.
pause
exit /b 0
:erro
echo A preparacao falhou. Leia a mensagem acima e consulte docs\LAB_SETUP.md.
pause
exit /b 1

