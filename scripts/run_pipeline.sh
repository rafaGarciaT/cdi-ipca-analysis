#!/bin/bash

# Ativa ambiente virtual (se existir)
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Define variáveis de ambiente (se necessário)
declare PYTHONPATH
PYTHONPATH="${PYTHONPATH}:$(pwd)"
export PYTHONPATH

# Executa a pipeline com os argumentos passados
python main.py "$@"

# Captura o código de saída
declare EXIT_CODE
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Pipeline executada com sucesso!"
else
    echo "Erro na execução da pipeline (código: $EXIT_CODE)"
fi

exit $EXIT_CODE
