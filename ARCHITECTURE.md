# Documentação de Arquitetura 

## Estrutura de Diretórios do Projeto

```
cdi-ipca-analysis/
├── main.py                      # Ponto de entrada da aplicação
├── README.md                    # Documentação do projeto
├── LICENSE                      # Licença do projeto
├── ARCHITECTURE.md              # Documentação de arquitetura
├── CONTRIBUTING.md              # Guia de contribuição
├── CHANGELOG.md                 # Histórico de alterações
├── requirements.txt             # Dependências do projeto
│
├── data/                        # Diretório de dados
│   ├── raw/                     # Dados brutos da API
│   │   ├── cdi/                # CDI (JSON com monthly + yearly)
│   │   └── ipca/               # IPCA mensal (JSON)
│   └── processed/              # Dados processados
│       ├── cdi_data.xlsx       # Base CDI processada
│       └── ipca_data.xlsx      # Base IPCA processada
│
├── logs/                        # Logs de execução
│   └── pipeline_YYYYMMDD_HHMMSS.log
│
├── src/                        # Código fonte
│   ├── __init__.py
│   ├── config.py              # Configurações da API e constantes
│   ├── pipeline.py            # Orquestrador da pipeline
│   │
│   ├── fetch/                 # Módulos de coleta
│   │   ├── __init__.py
│   │   ├── base.py           # Fetcher genérico para API BCB
│   │   ├── fetch_cdi.py      # Busca CDI (mensal + anual)
│   │   └── fetch_ipca.py     # Busca IPCA
│   │
│   ├── indicators/            # Indicadores econômicos
│   │   ├── base_indicator.py # Classe base abstrata
│   │   ├── cdi_indicator.py  # Lógica completa do CDI
│   │   └── ipca_indicator.py # Lógica completa do IPCA
│   │
│   ├── transform/             # Módulos de transformação
│   │   ├── __init__.py
│   │   ├── base_transform.py # Funções de cálculo (acumulados)
│   │   └── tax_rates.py      # Tabela IR
│   │
│   ├── storage/               # Módulos de persistência
│   │   ├── __init__.py
│   │   ├── raw/              # Armazenamento de dados brutos
│   │   │   ├── __init__.py
│   │   │   ├── base.py       # Interface abstrata
│   │   │   ├── json_storage.py # Implementação JSON
│   │   │   ├── factory.py    # Factory pattern
│   │   │   └── schema.py     # Schema de dados brutos
│   │   └── processed/        # Armazenamento de dados processados
│   │       ├── __init__.py
│   │       ├── base.py       # Interface abstrata
│   │       ├── excel_storage.py # Implementação Excel
│   │       ├── factory.py    # Factory pattern
│   │       └── schema.py     # Schemas CDI e IPCA
│   │
│   ├── models/                # Modelos de dados
│   │   ├── __init__.py
│   │   └── cdb.py            # Modelo CDB
│   │
│   └── utils/                 # Utilitários
│       ├── __init__.py
│       ├── date_utils.py     # Utilidades de data
│       ├── directory_utils.py # Utilidades de diretório
│       └── logger.py         # Sistema de logging
│
├── scripts/                   # Scripts auxiliares
│   ├── Makefile              # Automação de tarefas
│   ├── run_pipeline.bat      # Script Windows
│   └── run_pipeline.sh       # Script Unix/Linux
│
├── notebooks/                 # Jupyter notebooks
│   ├── 01_introducao.ipynb
│   ├── 02_visualizacao_basica.ipynb
│   ├── 03_outras_visualizacoes.ipynb
│   └── renda_fixa_e_a_inflacao.ipynb
│
├── dashboard/                 # Dashboard (futuro)
│
└── tests/                     # Testes automatizados
    ├── __init__.py
    ├── conftest.py           # Configurações pytest
    ├── unit/                 # Testes unitários
    │   ├── test_indicator_contracts.py
    │   ├── test_pipeline.py
    │   └── test_transforms.py
    └── qa/                   # Testes de qualidade
        ├── test_coverage.py
        ├── test_dependencies.py
        └── test_documentation.py
```


## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                     USUÁRIO / SCHEDULER                         │
│               (Execução Manual ou Automática)                   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          MAIN.PY                                │
│                    ┌──────────────────┐                         │
│                    │  Argumentos CLI  │                         │
│                    │  ─ mode          │                         │
│                    │  ─ persistence   │                         │
│                    │  ─ year          │                         │
│                    │  ─ end-year      │                         │
│                    │  ─ clear-data    │                         │
│                    │  ─ clear-data-   │                         │
│                    │    only          │                         │
│                    └──────────────────┘                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         PIPELINE.PY                             │
│                    ┌──────────────────┐                         │
│                    │  Orquestrador    │                         │
│                    │  ─ _run_month    │                         │
│                    │  ─ _run_year     │                         │
│                    │  ─ _run_backfill │                         │
│                    │  ─ _setup_       │                         │
│                    │    indicators    │                         │
│                    └──────────────────┘                         │
└─┬───────────────────────────┬─────────────────────────┬─────────┘
  │                           │                         │
  │ INDICATORS                │ STORAGE                 │ UTILS
  │                           │                         │
  ▼                           ▼                         ▼
┌────────────────┐    ┌──────────────┐    ┌─────────────────┐
│ BaseIndicator  │    │  Factories   │    │  Utilitários    │
│ (Abstract)     │    │              │    │                 │
│                │    │ RawStorage   │    │ date_utils.py   │
│ ├─CDIIndicator │    │ Factory      │    │ directory_      │
│ │  ├─fetch     │◄───┤              │    │ utils.py        │
│ │  ├─transform │    │ Processed    │    │ logger.py       │
│ │  ├─save_raw  │    │ Storage      │    │                 │
│ │  └─load_     │◄───┤ Factory      │    └─────────────────┘
│ │    processed │    │              │
│ └─IPCAIndicator│    └──────────────┘
│    ├─fetch     │           │
│    ├─transform │           │
│    ├─save_raw  │           ▼
│    └─load_     │    ┌──────────────┐
│      processed │    │   Storage    │
└────────┬───────┘    │              │
         │            │ Raw:         │
         │            │ ├─JSON       │
         │            │              │
         │            │ Processed:   │
         │            │ ├─Excel      │
         │            │ └─SQLite(*)  │
         │            └──────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FETCH & TRANSFORM                            │
│  ┌────────────────┐          ┌────────────────┐                │
│  │  fetch/        │          │  transform/    │                │
│  │  ─ base.py     │          │  ─ base_       │                │
│  │    (fetch_bcb_ │          │    transform   │                │
│  │     data)      │          │  ─ tax_rates   │                │
│  │  ─ fetch_cdi   │          │                │                │
│  │  ─ fetch_ipca  │          │  calc_         │                │
│  │                │          │  accumulated_  │                │
│  │  (API BCB)     │          │  ytd_rate()    │                │
│  └────────────────┘          └────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ARMAZENAMENTO                              │
│  ┌───────────────────┐          ┌───────────────────┐           │
│  │   data/raw/       │          │  data/processed/  │           │
│  │  ─ cdi/           │          │  ─ cdi_data.xlsx  │           │
│  │  ─ ipca/          │          │  ─ ipca_data.xlsx │           │
│  │  (JSON backups)   │          │                   │           │
│  │                   │          │  (Dados limpos)   │           │
│  └───────────────────┘          └───────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

## Fluxo de Dados (ETL)

```
┌──────────┐
│ Extract  │  API do Banco Central do Brasil
└────┬─────┘  ↓
     │        • Série 12: CDI Taxa de juros Diário (não usada)
     │        • Série 4391: CDI Mensal
     │        • Série 4392: CDI Anual
     │        • Série 433: IPCA Mensal
     │
     │        Fetchers genéricos: fetch_bcb_data()
     │        ├─ get_monthly_cdi_rate()
     │        ├─ get_yearly_cdi_rate()
     │        └─ get_monthly_ipca()
     ▼
┌──────────────────────────────────────────┐
│          JSON Response                   │
│  {                                       │
│    "data": "01/01/2025",                 │
│    "valor": "0.87"                       │
│  }                                       │ 
└────┬─────────────────────────────────────┘
     │
     │ CDI: Retorna tupla (monthly, yearly)
     │ IPCA: Retorna valor único
     │
     ▼
┌──────────┐
│Transform │  Processamento pelos Indicators
└────┬─────┘  ↓
     │        • Conversão de tipos (/ 100)
     │        • Cálculo de fatores diários
     │        • Taxas acumuladas YTD
     │        • Taxas acumuladas 12 meses
     │        • Validações
     │
     │        CDIIndicator.transform()
     │        IPCAIndicator.transform()
     ▼
┌──────────────────────────────────────────┐
│       Dados Estruturados                 │
│  CDI: {                                  │
│    "date": "2025-01",                    │
│    "cdi_monthly_rate": 0.0087,           │
│    "cdi_annual_rate": 0.1065,            │
│    "cdi_accumulated_ytd_rate": 0.0087,   │
│    "cdi_12m_rate": 0.1120                │
│  }                                       │
│  IPCA: {                                 │
│    "date": "2025-01",                    │
│    "ipca_monthly_rate": 0.0042,          │
│    "ipca_accumulated_ytd_rate": 0.0042,  │
│    "ipca_12m_rate": 0.0489               │
│  }                                       │
└────┬─────────────────────────────────────┘
     │
     ▼
┌──────────┐
│   Load   │  Persistência via Storage Factories
└────┬─────┘  ↓
     │        Raw Storage:
     │        ├─ JSON (padrão)
     │        └─ JsonRawStorage
     │
     │        Processed Storage:
     │        ├─ Excel (padrão)
     │        ├─ SQLite (futuro)
     │        └─ ExcelProcessedStorage
     ▼
┌───────────────────────────────────────────┐
│        Armazenamento Final                │
│                                           │
│  📊 cdi_data.xlsx                         │
│     (date, cdi_annual_rate,               │
│      cdi_monthly_rate,                    │
│      cdi_accumulated_ytd_rate,            │
│      cdi_12m_rate)                        │
│                                           │
│  📊 ipca_data.xlsx                        │
│     (date, ipca_monthly_rate,             │
│      ipca_accumulated_ytd_rate,           │
│      ipca_12m_rate)                       │
│                                           │
│  📄 data/raw/cdi/cdi_2025-01.json         │
│  📄 data/raw/ipca/ipca_2025-01.json       │
└───────────────────────────────────────────┘
```

## Modos de Execução

### 1️⃣ Month Mode (Modo Mensal)

```
┌─────────────────────────────────────────┐
│  python main.py --mode month            │
└──────────────┬──────────────────────────┘
               │
               ▼
        ┌──────────────┐
        │ Data Atual?  │
        └──────┬───────┘
               │
         ┌─────▼─────┐
         │ Dia Útil? │
         └─────┬─────┘
          Não  │  Sim
               │
         ┌─────▼──────────────────────┐
         │ Para cada Indicator (CDI,  │
         │ IPCA):                     │
         └─────┬──────────────────────┘
               │
         ┌─────▼────────┐
         │Já Processado?│
         └─────┬────────┘
          Não  │  Sim → Pula
               │
         ┌─────▼──────┐
         │   Fetch    │
         │ (API BCB)  │
         └─────┬──────┘
               │
         ┌─────▼─────┐
         │ Save Raw  │
         │  (JSON)   │
         └─────┬─────┘
               │
         ┌─────▼─────┐
         │ Transform │
         └─────┬─────┘
               │
         ┌─────▼─────────┐
         │ Load Processed│
         │   (Excel)     │
         └─────┬─────────┘
               │
               ▼
           Sucesso!
```

### 2️⃣ Yearly Mode (Modo Anual)

```
┌────────────────────────────────────────────────────┐
│  python main.py --mode yearly --year 2025          │
│  [opcional: --end-year 2026 para range]            │
└──────────────┬─────────────────────────────────────┘
               │
               ▼
      ┌────────────────────┐
      │ Para cada ano no   │
      │ range especificado │
      └────────┬───────────┘
               │
               ▼
      ┌────────────────────┐
      │ Range: 01/01/YYYY  │
      │   até: 31/12/YYYY  │
      │   ou data atual    │
      └────────┬───────────┘
               │
               ▼
      ┌────────────────────────┐
      │ Para cada Indicator    │
      │ (CDI, IPCA):           │
      └────────┬───────────────┘
               │
               ▼
      ┌────────────────┐
      │ Fetch ALL Data │
      │  para o range  │
      └────────┬───────┘
               │
               ▼
      ┌────────────────────┐
      │ Para cada entrada: │
      │ ├─ Já processado?  │
      │ │   └─ Sim: Pula   │
      │ │   └─ Não: ↓      │
      │ ├─ Save Raw (JSON) │
      │ ├─ Transform       │
      │ └─ Load Processed  │
      └────────┬───────────┘
               │
               ▼
      Range completo processado!
```

### 3️⃣ Backfill Mode (Preenchimento de lacunas)

```
┌─────────────────────────────────────────┐
│  python main.py --mode backfill         │
└──────────────┬──────────────────────────┘
               │
               ▼
      ┌────────────────────┐
      │ Para cada Indicator│
      │ (CDI, IPCA):       │
      └────────┬───────────┘
               │
               ▼
      ┌────────────────┐
      │ Scan data/raw/ │
      │ Encontra datas │
      │ já processadas │
      └────────┬───────┘
               │
               ▼
      ┌────────────────┐
      │ Identifica     │
      │ Min/Max Date   │
      └────────┬───────┘
               │
               ▼
      ┌────────────────┐
      │ Fetch Range    │
      │ Completo       │
      └────────┬───────┘
               │
               ▼
      ┌────────────────────┐
      │ Para cada data:    │
      │ ├─ Existe?         │
      │ │   └─ Sim: Pula   │
      │ │   └─ Não: ↓      │
      │ ├─ Save Raw (JSON) │
      │ ├─ Transform       │
      │ └─ Load Processed  │
      └────────┬───────────┘
               │
               ▼
        Lacunas preenchidas!
```

## Modelo de Dados

### CDI (Excel)

```
┌──────────┬──────────────────┬──────────────────┬─────────────────────────┬──────────────┐
│   date   │ cdi_annual_rate  │ cdi_monthly_rate │ cdi_accumulated_ytd_rate│  cdi_12m_rate│
├──────────┼──────────────────┼──────────────────┼─────────────────────────┼──────────────┤
│ 2025-01  │      0.1065      │      0.0087      │         0.0087          │    0.1120    │
│ 2025-02  │      0.1120      │      0.0091      │         0.0179          │    0.1156    │
│ 2025-03  │      0.1040      │      0.0085      │         0.0266          │    0.1098    │
└──────────┴──────────────────┴──────────────────┴─────────────────────────┴──────────────┘
```

### IPCA (Excel)

```
┌──────────┬──────────────────┬──────────────────────────┬───────────────┐
│   date   │ipca_monthly_rate │ ipca_accumulated_ytd_rate│ ipca_12m_rate │
├──────────┼──────────────────┼──────────────────────────┼───────────────┤
│ 2025-01  │      0.0042      │         0.0042           │    0.0489     │
│ 2025-02  │      0.0038      │         0.0080           │    0.0502     │
│ 2025-03  │      0.0045      │         0.0126           │    0.0518     │
└──────────┴──────────────────┴──────────────────────────┴───────────────┘
```

### JSON Backup (Raw Data)

**CDI:**
```json
{
  "reference_date": "2025-01",
  "type": "cdi",
  "value": {
    "monthly": 0.0087,
    "yearly": 0.1065
  }
}
```

**IPCA:**
```json
{
  "reference_date": "2025-01",
  "type": "ipca",
  "value": 0.0042
}
```

## Casos de Uso

### 1. Investidor Individual
```
Objetivo: Acompanhar rendimento de CDB
├─ Executar: python main.py (diário)
├─ Analisar: Excel com histórico completo
└─ Calcular: IR, rendimento líquido
```

### 2. Analista Financeiro
```
Objetivo: Análise histórica e comparações
├─ Executar: python main.py --mode yearly --year 2024
├─ Exportar: Dados para ferramentas de análise
└─ Visualizar: Gráficos CDI vs IPCA
```

### 3. Pesquisador
```
Objetivo: Estudos de correlação econômica
├─ Executar: Backfill para dados históricos
├─ Integrar: Pandas/NumPy para análises
└─ Publicar: Resultados de pesquisa
```

### 4. Desenvolvedor
```
Objetivo: Integrar com outras aplicações
├─ Usar: Como módulo Python
├─ Acessar: Dados via Excel ou API
└─ Estender: Novos indicadores
```

## Stack Tecnológico

```
┌─────────────────────────────────────────┐
│           Frontend (Futuro)             │
│   Dashboard Web - Streamlit/Dash        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Camada de Aplicação             │
│                                         │
│  Python 3.8+                            │
│  ├─ CLI (argparse)                      │
│  ├─ Pipeline (ETL)                      │
│  └─ Models (CDB)                        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│        Bibliotecas Core                 │
│                                         │
│  ├─ Pandas >=3.0.0  (Data manipulation) │
│  ├─ Requests >=2.31.0 (HTTP client)     │
│  ├─ OpenPyXL >=3.1.0 (Excel I/O)        │
│  ├─ NumPy >=1.24.0 (Numerical computing)│
│  ├─ Matplotlib >=3.5.0 (Plotting)       │
│  ├─ python-dateutil >=2.8.2 (Dates)     │
│  └─ Colorama (Terminal colors)          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│          Data Sources                   │
│                                         │
│  API BCB (https://api.bcb.gov.br)       │
│  ├─ Série 12: CDI Diário                │
│  ├─ Série 4391: CDI Mensal              │
│  ├─ Série 4392: CDI Anual               │
│  └─ Série 433: IPCA Mensal              │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│          Persistência                   │
│                                         │
│  ├─ Excel (.xlsx)            [Atual]    │
│  ├─ JSON (backups brutos)    [Atual]    │
│  └─ SQLite (.db)             [Futuro]   │
└─────────────────────────────────────────┘
```

## Roadmap

### Versão 0.1.0 (Concluída)
- [x] Pipeline ETL básica
- [x] CDI e IPCA implementados
- [x] Persistência Excel
- [x] Criação dos métodos de execução principais
- [x] Classe CDB
- [x] Documentação básica
- [x] CLI e scripts de execução

### Versão 0.2.0 (Concluída)
- [x] Revisão dos métodos de execução
- [x] Estrutura de fetches escalável e modular
- [x] Estrutura de persistência modular e escalável (factories)
- [x] Estrutura da pipeline escalável
- [x] Cálculo de todas as mensurações de CDI e IPCA (YTD e 12 meses)
- [x] Sistema de logging
- [x] Testes automatizados básicos (pytest)
- [x] Notebooks de demonstração e análises básicos

### Versão 0.3.0 (Atual)
- [ ] Metadados na persistência
- [ ] Mais opções de persistência de dados brutos e processados (SQLite, PostgreSQL)
- [ ] Scripts de automação de execução (scheduler)
- [ ] Mais indicadores (SELIC, etc.)
- [ ] Dashboards básicos
- [ ] Cobertura de testes expandida

### Versão 0.4.0+ (Planejada)
- [ ] Todos os indicadores principais implementados com todas as mensurações
- [ ] Machine Learning (previsões)
- [ ] Classes de outros títulos
- [ ] Simuladores de investimento
- [ ] Dashboard web interativo completo
- [ ] Documentação completa
- [ ] Notebooks educacionais e tutoriais
- [ ] Logo e identidade visual
- [ ] Possível API REST para acesso aos dados processados
- [ ] Possível GUI


---

**Documentação visual mantida por:** rafaGarciaT  
**Última atualização:** 21 de fevereiro de 2026  
**Versão:** 0.3.0

