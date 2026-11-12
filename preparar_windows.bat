@echo off
setlocal
cd /d "%~dp0"
echo Preparando Air Band Lab com Python 3.8.2 ou posterior da serie 3.8, de 64 bits...
if exist ".venv\Scripts\python.exe" goto :ambiente
set "AIRBAND_PYTHON=%~1"
if defined AIRBAND_PYTHON goto :python_encontrado
for /f "delims=" %%P in ('py -3.8 -c "import sys; print(sys.executable)" 2^>nul') do set "AIRBAND_PYTHON=%%P"
if defined AIRBAND_PYTHON goto :python_encontrado
rem Ignorar o atalho que abre a Microsoft Store, procurando instalacoes reais.
for /f "delims=" %%P in ('where python.exe 2^>nul ^| findstr /v /i /l "WindowsApps"') do call :tentar_python "%%P"
if defined AIRBAND_PYTHON goto :python_encontrado
echo Python 3.8 de 64 bits nao encontrado. Informe o caminho da instalacao existente:
echo preparar_windows.bat "C:\caminho\para\python.exe"
goto :erro

:python_encontrado
"%AIRBAND_PYTHON%" -c "import sys, struct; assert (3, 8, 2) <= sys.version_info[:3] < (3, 9, 0) and struct.calcsize('P') == 8, 'Use Python 3.8.2 ou posterior da serie 3.8, de 64 bits'"
if errorlevel 1 goto :erro
"%AIRBAND_PYTHON%" -m venv .venv
if errorlevel 1 goto :erro

:ambiente
".venv\Scripts\python.exe" -c "import sys, struct; assert (3, 8, 2) <= sys.version_info[:3] < (3, 9, 0) and struct.calcsize('P') == 8, 'O ambiente .venv precisa usar Python 3.8.2 ou posterior da serie 3.8, de 64 bits; renomeie o ambiente antigo e execute a preparacao novamente'"
if errorlevel 1 goto :erro
set "AIRBAND_PIP_SOURCE="
if exist "wheelhouse" set "AIRBAND_PIP_SOURCE=--no-index --find-links=wheelhouse"
rem O pip original do Python 3.8.2 nao reconhece todos os wheels atuais no Windows.
".venv\Scripts\python.exe" -m pip install %AIRBAND_PIP_SOURCE% --only-binary=:all: pip==25.0.1
if errorlevel 1 goto :erro
".venv\Scripts\python.exe" -m pip install %AIRBAND_PIP_SOURCE% --only-binary=:all: -r requirements-lock.txt
if errorlevel 1 goto :erro
".venv\Scripts\python.exe" scripts\generate_sounds.py
if errorlevel 1 goto :erro
".venv\Scripts\python.exe" scripts\prepare_model.py
if errorlevel 1 goto :erro
echo Pronto. Execute iniciar_windows.bat ou consulte README.md.
pause
exit /b 0

:tentar_python
if defined AIRBAND_PYTHON exit /b 0
"%~1" -c "import sys, struct; assert (3, 8, 2) <= sys.version_info[:3] < (3, 9, 0) and struct.calcsize('P') == 8" >nul 2>&1
if not errorlevel 1 set "AIRBAND_PYTHON=%~1"
exit /b 0

:erro
echo A preparacao falhou. Leia a mensagem acima e consulte docs\LAB_SETUP.md.
pause
exit /b 1

