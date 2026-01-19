# CDI & IPCA Analysis Pipeline (cdi-ipca-analysis)
[🇺🇸 English Version](README.en.md) | [Changelog](CHANGELOG.md) | [Arquitetura](ARCHITECTURE.md)

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Este projeto implementa uma Pipeline automatizada para coleta, processamento e análise de indicadores econômicos brasileiros (atualmente, CDI e IPCA). 
Ele busca dados diretamente da API oficial do Banco Central do Brasil (BCB), processa as informações e armazena em formato Excel para análise posterior.

## Funcionalidades
- ✅ Coleta automática de dados da taxa CDI mensal anual
- ✅ Coleta automática de dados da taxa IPCA mensal
- ✅ Armazenamento de dados brutos em JSON
- ✅ Persistência de dados processados em Excel
- ✅ Modos de execução para coleta mensal, anual e para preenchimento de lacunas


## Funcionalidades Planejadas
- Suporte a persistência em SQLite e PostgreSQL
- Adição do indicador SELIC
- Integração com dashboards
- Testes unitários e de integração
- Notebooks Jupyter para análise exploratória
- Criação de dashboards interativos
- Automação via agendadores (cron, task scheduler)

## Requisitos e Dependências
- Python 3.8+

- pandas
- requests
- openpyxl
- python-dateutil
- numpy

```bash
pip install pandas requests openpyxl python-dateutil numpy
```

## Uso
Clone o repositório, instale as dependências e considere criar um ambiente virtual. 

### Execução Básica
```bash
python main.py
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
| Argumento       | Tipo   | Padrão  | Descrição                                                                |
|-----------------|--------|---------|--------------------------------------------------------------------------|
| `--mode`        | string | `month` | Modo de execução: `month`, `yearly`, `backfill`                          |
| `--persistence` | string | `excel` | Modo de persistência: `excel`, `sqlite` (em desenvolvimento)             |
| `--year`        | int    | -       | Ano alvo (opcional para modo `yearly`, ano atual selecionado se ausente) |
| `--clear-data`  | flag   | -       | Limpa as pastas de dados brutos processados antes de executar            |

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



