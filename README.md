# CDI & IPCA Analysis Pipeline (cdi-ipca-analysis)
[🇺🇸 English Version](README.en.md) | [Changelog](CHANGELOG.md) | [Arquitetura](ARCHITECTURE.md)

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Este projeto implementa uma Pipeline automatizada para coleta, processamento e armazenamento de indicadores econômicos brasileiros (atualmente, CDI e IPCA). 
Ele é feito para ser uma ferramenta de análise e monitoramento para todos os interessados em acompanhar a evolução desses indicadores. 
Junto com a pipeline, são fornecidos notebooks Jupyter com análises exploratórias e visualizações dos dados coletados.

## Funcionalidades
- ✅ Coleta automática de dados da taxa CDI mensal e anual
- ✅ Coleta automática de dados da taxa IPCA mensal
- ✅ Armazenamento de dados brutos em JSON
- ✅ Persistência de dados processados em Excel
- ✅ Cálculo de taxas acumuladas no ano e dos últimos 12 meses
- ✅ Modos de execução para coleta mensal, anual e para preenchimento de lacunas
- ✅ Notebooks Jupyter para análise exploratória


## Funcionalidades Planejadas
- Suporte a persistência em SQLite e PostgreSQL
- Adição de mains indicadores econômicos (Selic, IGP-M, etc.)
- Automação via agendadores (cron, task scheduler)

## Requisitos e Dependências
- Python 3.8+

### Dependências principais:
- pandas>=3.0.0
- requests>=2.31.0
- openpyxl>=3.1.0
- python-dateutil>=2.8.2
- numpy>=1.24.0
- matplotlib>=3.5.0
- colorama>=0.4.4

### Dependências de desenvolvimento:
- pytest>=7.0.0
- pytest-cov>=4.0.0
- pip-audit>=2.6.0
- jupyter>=1.0.0
- ipykernel>=6.0.0

```bash
pip install -r requirements.txt
```

## Uso
Clone o repositório, instale as dependências e considere criar um ambiente virtual. 

### Execução Básica
```bash
py main.py
```

Este comando executa a pipeline no modo padrão (`month`) com persistência em Excel.
Também é possível usar os scripts auxiliares para facilitar a execução.

1. **Windows:** 
```powershell
.\scripts\run_pipeline.bat
```

2. **Linux/Mac:**
```bash
chmod +x scripts/run_pipeline.sh
./scripts/run_pipeline.sh
```

Abaixo estão detalhados os argumentos disponíveis para personalizar a execução.

###  Argumentos do CLI
| Argumento           | Tipo   | Padrão  | Descrição                                                            |
|---------------------|--------|---------|----------------------------------------------------------------------|
| `--mode`            | string | `month` | Modo de execução: `month`, `yearly`, `backfill`                      |
| `--persistence`     | string | `excel` | Modo de persistência: `excel`, `sqlite` (em desenvolvimento)         |
| `--year`            | int    | -       | Ano alvo para o modo `yearly`                                        |
| `--end-year`        | int    | -       | Ano final para processamento de range (opcional, usado com `--year`) |
| `--clear-data`      | flag   | -       | Limpa as pastas de dados brutos e processados antes de executar      |
| `--clear-data-only` | flag   | -       | Apenas limpa as pastas de dados sem executar a pipeline              |

### Modos de Execução
1. `month`: Coleta e processa dados do mês atual.
2. `yearly`: Coleta e processa dados de um ano específico.
3. `backfill`: Preenche lacunas nos dados já coletados.

Cada modo pula automaticamente datas já processadas.

### Exemplos
```bash
# Modo anual com clear-data 
# (os diretórios serão limpos, e a Pipeline vai recolher e processar todos os dados do ano de 2025)
python main.py --mode yearly --year 2025 --clear-data

# Modo backfill 
# (A Pipeline vai checar as lacunas dos dados processados e as preencherá)
python main.py --mode backfill
```

## Desenvolvimento
Veja o arquivo [Architecture.md](ARCHITECTURE.md) para detalhes sobre a arquitetura do projeto, estrutura de pastas e padrões de codificação.

### Fonte de dados
O projeto utiliza as seguintes séries temporais da API do BCB:

### CDI
- **Série 12**: Taxa de Juros CDI (%a.d) (não utilizada)
- **Série 4391**: CDI Acumulado Mensal (% a.m.)
- **Série 4392**: CDI Acumulado Anual (% a.a.)
- **Endpoint**: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie}/dados`

### IPCA
- **Série 433**: IPCA Mensal (%)
- **Endpoint**: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados`

Mais informações sobre as séries temporais podem ser encontradas no [Portal de Séries Temporais do BCB](https://www4.bcb.gov.br/pec/series/port/aviso.asp?frame=1).

### Estrutura da Pipeline
A pipeline segue o padrão ETL (Extract, Transform, Load):

1. **Extract (Fetch)**
   - Busca dados da API do BCB
   - Valida respostas
   - Salva dados brutos em JSON

2. **Transform**
   - Conversão de porcentagens para decimais
   - Calcula fator diário do CDI
   - Calcula taxas acumuladas
   - Formata dados para persistência

3. **Load (Storage)**
   - Persiste em Excel
   - Mantém histórico completo
   - Suporta múltiplas escritas

### Tratamento de Erros
A Pipeline possui tratamento de erros para:

- Falhas na API do BCB
- Dados ausentes ou inválidos
- Dias não úteis
- Dados já processados
- Erros de persistência

## Changelog

Para histórico completo de alterações, consulte [CHANGELOG.md](CHANGELOG.md).

