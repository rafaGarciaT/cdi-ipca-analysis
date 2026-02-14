@echo off
setlocal enabledelayedexpansion

set PYTHON_ARGS=

REM Ativa ambiente virtual
if exist venv\Scripts\activate.bat (
    echo [INFO] Ativando ambiente virtual...
    call venv\Scripts\activate.bat
) else if exist .venv\Scripts\activate.bat (
    echo [INFO] Ativando ambiente virtual ^(.venv^)...
    call .venv\Scripts\activate.bat
) else (
    echo [WARN] Nenhum ambiente virtual encontrado
)

REM Define variáveis de ambiente
set PYTHONPATH=%PYTHONPATH%;%CD%

REM Executar pipeline
echo [INFO] Executando pipeline...
py main.py %PYTHON_ARGS%

if %ERRORLEVEL% EQU 0 (
    echo Pipeline executada com sucesso!
) else (
    echo Erro na execucao da pipeline ^(codigo: %ERRORLEVEL%^)
)

exit /b %ERRORLEVEL%
