#!/bin/bash
set -euo pipefail

# Cores para output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

# Função para logging
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Função para limpar dados
clear_data() {
    log_warn "Limpando dados..."
    if [ -d "data/processed" ]; then
        rm -rf data/processed/*
        log_info "Dados processados removidos"
    fi
    if [ -d "data/cache" ]; then
        rm -rf data/cache/*
        log_info "Cache limpo"
    fi
    if [ -d "logs" ]; then
        rm -rf logs/*
        log_info "Logs removidos"
    fi
}

# Parse argumentos
CLEAR_DATA=false
PYTHON_ARGS=()

for arg in "$@"; do
    if [ "$arg" == "--clear-data" ]; then
        CLEAR_DATA=true
    else
        PYTHON_ARGS+=("$arg")
    fi
done

# Executar limpeza se solicitado
if [ "$CLEAR_DATA" = true ]; then
    clear_data
    # Sair se apenas --clear-data foi passado (sem outros argumentos)
    if [ ${#PYTHON_ARGS[@]} -eq 0 ]; then
        log_info "Limpeza concluída. Nenhuma pipeline será executada."
        exit 0
    fi
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    log_error "Python3 não encontrado!"
    exit 1
fi

# Ativa ambiente virtual (se existir)
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    log_info "Ativando ambiente virtual (.venv)..."
    source .venv/bin/activate
else
    log_warn "Nenhum ambiente virtual encontrado"
fi

# Define variáveis de ambiente (se necessário)
declare PYTHONPATH
PYTHONPATH="${PYTHONPATH:-}:$(pwd)"
export PYTHONPATH

# Executa a pipeline com os argumentos passados
log_info "Executando pipeline..."
python3 main.py "${PYTHON_ARGS[@]}"

# Captura o código de saída
declare EXIT_CODE
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    log_info "Pipeline executada com sucesso!"
else
    log_error "Erro na execução da pipeline (código: $EXIT_CODE)"
fi

exit $EXIT_CODE
