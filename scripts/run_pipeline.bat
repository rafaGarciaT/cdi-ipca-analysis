@echo off

REM Ativa ambiente virtual (se existir)
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Define variáveis de ambiente
set PYTHONPATH=%PYTHONPATH%;%CD%

REM Executa a pipeline
python main.py %*

if %ERRORLEVEL% EQU 0 (
    echo Pipeline executada com sucesso!
) else (
    echo Erro na execucao da pipeline ^(codigo: %ERRORLEVEL%^)
)

exit /b %ERRORLEVEL%
