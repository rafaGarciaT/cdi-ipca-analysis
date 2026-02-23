# CDI & IPCA Analysis Pipeline (cdi-ipca-analysis)
[🇧🇷 Versão em Português](README.md) | [Changelog](CHANGELOG.md) | [Architecture](ARCHITECTURE.md)

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

This project implements an automated Pipeline for collecting, processing, and storing Brazilian economic indicators (currently CDI and IPCA). 
It is designed to be an analysis and monitoring tool for anyone interested in tracking the evolution of these indicators. 
Along with the pipeline, Jupyter notebooks are provided with exploratory analysis and visualizations of the collected data.

## Features
- ✅ Automatic collection of monthly and annual CDI rates
- ✅ Automatic collection of monthly IPCA rates
- ✅ Raw data storage in JSON
- ✅ Processed data persistence in Excel
- ✅ Calculation of year-to-date and 12-month accumulated rates
- ✅ Execution modes for monthly, yearly, and gap-filling collection
- ✅ Jupyter notebooks for exploratory analysis

## Planned Features
- Support for SQLite and PostgreSQL persistence
- Addition of more economic indicators (SELIC, IGP-M, etc.)
- Automation via schedulers (cron, task scheduler)

## Requirements and Dependencies
- Python 3.8+

### Main Dependencies:
- pandas>=3.0.0
- requests>=2.31.0
- openpyxl>=3.1.0
- python-dateutil>=2.8.2
- numpy>=1.24.0
- matplotlib>=3.5.0
- colorama>=0.4.4

### Development Dependencies:
- pytest>=7.0.0
- pytest-cov>=4.0.0
- pip-audit>=2.6.0
- jupyter>=1.0.0
- ipykernel>=6.0.0

```bash
pip install -r requirements.txt
```

## Usage
Clone the repository, install the dependencies, and consider creating a virtual environment.

### Basic Execution
```bash
python main.py
```

This command executes the pipeline in default mode (`month`) with Excel persistence.
It's also possible to use the helper scripts to facilitate execution.

1. **Windows:**
```powershell
.\scripts\run_pipeline.bat
```

2. **Linux/Mac:**
```bash
chmod +x scripts/run_pipeline.sh
./scripts/run_pipeline.sh
```

Below are the available arguments to customize execution.

### CLI Arguments
| Argument            | Type   | Default | Description                                                          |
|---------------------|--------|---------|----------------------------------------------------------------------|
| `--mode`            | string | `month` | Execution mode: `month`, `yearly`, `backfill`                        |
| `--persistence`     | string | `excel` | Persistence mode: `excel`, `sqlite` (in development)                 |
| `--year`            | int    | -       | Target year for `yearly` mode                                        |
| `--end-year`        | int    | -       | End year for range processing (optional, used with `--year`)         |
| `--clear-data`      | flag   | -       | Clears raw and processed data folders before execution               |
| `--clear-data-only` | flag   | -       | Only clears data folders without executing the pipeline              |

### Execution Modes
1. `month`: Collects and processes current month data.
2. `yearly`: Collects and processes data for a specific year.
3. `backfill`: Fills gaps in already collected data.

Each mode automatically skips already processed dates.

### Examples
```bash
# Yearly mode with clear-data
# (directories will be cleared, and the pipeline will recollect and process all 2025 data)
python main.py --mode yearly --year 2025 --clear-data

# Backfill mode
# (The pipeline will check for gaps in processed data and fill them)
python main.py --mode backfill
```

## Development
See the [ARCHITECTURE.md](ARCHITECTURE.md) file for details about the project architecture, folder structure, and coding standards.

### Data Source
The project uses the following time series from the BCB API:

#### CDI
- **Series 4391**: Accumulated Monthly CDI (% p.m.)
- **Series 4392**: Accumulated Annual CDI (% p.a.)
- **Endpoint**: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie}/dados`

#### IPCA
- **Series 433**: Monthly IPCA (%)
- **Endpoint**: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados`

More information about time series can be found at the [BCB Time Series Portal](https://www4.bcb.gov.br/pec/series/port/aviso.asp?frame=1).

### Pipeline Architecture
The pipeline follows the ETL (Extract, Transform, Load) pattern:

1. **Extract (Fetch)**
   - Fetches data from BCB API
   - Validates responses
   - Saves raw data in JSON

2. **Transform**
   - Converts percentages to decimals
   - Calculates daily CDI factor
   - Calculates accumulated rates
   - Formats data for persistence

3. **Load (Storage)**
   - Persists in Excel
   - Maintains complete history
   - Supports multiple writes

### Error Handling
The pipeline has error handling for:

- BCB API failures
- Missing or invalid data
- Non-business days
- Already processed data
- Persistence errors

## Changelog

For complete change history, see [CHANGELOG.md](CHANGELOG.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Rafael Garcia Trigo

## 🙏 Acknowledgments

- Central Bank of Brazil for providing the public API
- Python community for the excellent libraries

---

**Developed with ❤️ for Brazilian economic indicators analysis**
