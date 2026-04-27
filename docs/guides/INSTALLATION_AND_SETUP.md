# Installation and Setup Guide

## Overview

This guide walks you through setting up the NW Natural End-Use Forecasting Model on your local machine for development and testing. The model is a Python-based bottom-up residential natural gas demand forecasting system.

---

## System Requirements

### Minimum Requirements
- **Python**: 3.9 or higher
- **RAM**: 8GB (laptop development)
- **Disk Space**: 10GB (data + code + outputs)
- **OS**: Windows, macOS, or Linux

### Recommended Requirements
- **Python**: 3.11 or higher
- **RAM**: 16GB+
- **Disk Space**: 20GB+
- **Git**: For version control

---

## Quick Start (5 minutes)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd nw-natural-forecasting
```

### 2. Create Virtual Environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Run a simple test to verify installation
python -c "import pandas; import numpy; import matplotlib; print('Dependencies installed successfully')"
```

### 5. Run Baseline Scenario

```bash
python -m src.main scenarios/baseline.json
```

Expected output: Results saved to `scenarios/baseline/` directory.

---

## Detailed Installation

### Step 1: System Setup

#### macOS
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Verify installation
python3 --version
```

#### Windows
```bash
# Download Python 3.11 from https://www.python.org/downloads/
# Run installer and check "Add Python to PATH"

# Verify installation
python --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3.11-dev

# Verify installation
python3.11 --version
```

### Step 2: Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd nw-natural-forecasting
```

### Step 3: Create Virtual Environment

A virtual environment isolates project dependencies from your system Python.

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt):
venv\Scripts\activate.bat
```

You should see `(venv)` prefix in your terminal prompt.

### Step 4: Install Dependencies

```bash
# Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r requirements.txt
```

### Step 5: Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Run a simple test
python -c "import sys; print(f'Python {sys.version}'); import pandas as pd; import numpy as np; print('Pandas:', pd.__version__); print('NumPy:', np.__version__)"
```

---

## Data Setup

### Directory Structure

The model expects data files in a specific directory structure:

```
nw-natural-forecasting/
├── Data/
│   ├── NWNatural Data/
│   │   ├── premise_data_blinded.csv
│   │   ├── equipment_data_blinded.csv
│   │   ├── segment_data_blinded.csv
│   │   ├── equipment_codes.csv
│   │   ├── DailyCalDay1985_Mar2025.csv (or DailyGasDay2008_Mar2025.csv)
│   │   ├── BullRunWaterTemperature.csv
│   │   ├── Portland_snow.csv
│   │   └── billing_data_blinded.csv
│   ├── 2022 RBSA Datasets/
│   │   ├── [RBSA building characteristics files]
│   ├── ashrae/
│   │   ├── OR-ASHRAE_Service_Life_Data.xls
│   │   ├── OR-ASHRAE_Maintenance_Cost_Data.xls
│   │   ├── WA-ASHRAE_Service_Life_Data.xls
│   │   └── WA-ASHRAE_Maintenance_Cost_Data.xls
│   ├── B25034-5y/
│   │   ├── [Census ACS B25034 data files]
│   ├── B25040-5y-county/
│   │   ├── [Census ACS B25040 data files]
│   ├── B25024-5y-county/
│   │   ├── [Census ACS B25024 data files]
│   ├── noaa_normals/
│   │   ├── [NOAA climate normals data]
│   ├── Residential Energy Consumption Survey/
│   │   ├── [EIA RECS data files]
│   ├── PSU projection data/
│   │   ├── [PSU population forecasts]
│   ├── Baseload Consumption Factors.csv
│   ├── nw_energy_proxies.csv
│   ├── or_rates_oct_2025.csv
│   ├── or_wacog_history.csv
│   ├── or_rate_case_history.csv
│   ├── wa_rates_nov_2025.csv
│   ├── wa_wacog_history.csv
│   ├── wa_rate_case_history.csv
│   ├── ofm_april1_housing.xlsx
│   ├── NW Natural Service Territory Census data.csv
│   ├── 10-Year Load Decay Forecast (2025–2035).csv
│   └── [other data files]
├── src/
├── tests/
├── scenarios/
├── output/
└── docs/
```

### Obtaining Data Files

**NW Natural Proprietary Data** (blinded premise, equipment, segment, billing):
- Contact NW Natural directly
- Data is anonymized/blinded for privacy
- Required for full model execution

**Public Data Sources**:
- RBSA 2022: Available from NEEA (Northwest Energy Efficiency Alliance)
- ASHRAE: Available from ASHRAE (American Society of Heating, Refrigerating and Air-Conditioning Engineers)
- Census ACS: Available from Census Bureau (data.census.gov)
- NOAA Climate Normals: Available from NOAA
- EIA RECS: Available from EIA (Energy Information Administration)
- PSU Forecasts: Available from Portland State University Population Research Center

### Data File Checklist

**Required for basic operation:**
- `Data/NWNatural Data/premise_data_blinded.csv`
- `Data/NWNatural Data/equipment_data_blinded.csv`
- `Data/NWNatural Data/segment_data_blinded.csv`
- `Data/NWNatural Data/equipment_codes.csv`
- `Data/NWNatural Data/DailyCalDay1985_Mar2025.csv` (or GasDay version)
- `Data/NWNatural Data/billing_data_blinded.csv`

**Optional but recommended:**
- RBSA 2022 datasets for building characteristics
- Census ACS data for demographic distributions
- ASHRAE data for equipment life estimates
- RECS data for end-use benchmarking

---

## First Run

### Run Baseline Scenario

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # macOS/Linux
# or
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Run baseline scenario
python -m src.main scenarios/baseline.json

# Expected output:
# [2026-04-27 10:30:45] INFO: Loading pipeline data...
# [2026-04-27 10:30:47] INFO: Loaded 487,234 premises
# [2026-04-27 10:30:48] INFO: Loading equipment data...
# [2026-04-27 10:30:52] INFO: Loaded 1,203,456 equipment records
# ...
# [2026-04-27 10:35:12] INFO: Running scenario: Baseline
# [2026-04-27 10:35:15] INFO: Scenario complete: Baseline
# [2026-04-27 10:35:18] INFO: Results exported to scenarios/baseline/
```

### View Results

```bash
# List output files
ls scenarios/baseline/

# View summary
cat scenarios/baseline/SUMMARY.md

# View yearly summary
head -20 scenarios/baseline/yearly_summary.csv

# View full results
head -20 scenarios/baseline/results.csv
```

### Run Custom Scenario

```bash
# Create custom scenario file
cat > scenarios/my_scenario.json << 'EOF'
{
  "name": "High Electrification",
  "base_year": 2025,
  "forecast_horizon": 10,
  "housing_growth_rate": 0.015,
  "electrification_rate": 0.05,
  "efficiency_improvement": 0.02,
  "weather_assumption": "normal",
  "initial_gas_pct": 100.0,
  "use_recs_ratios": true,
  "max_premises": 0,
  "vectorized": false
}
EOF

# Run custom scenario
python -m src.main scenarios/my_scenario.json
```

### Compare Scenarios

```bash
# Compare baseline and high electrification scenarios
python -m src.main scenarios/baseline.json scenarios/high_electrification.json --compare
```

---

## Development Workflow

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_housing_stock.py -v

# Run tests matching pattern
python -m pytest tests/ -k "property" -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

### Running Property Tests

The model includes property-based tests that validate correctness:

```bash
# Run configuration validation (Property 1)
python -m tests.test_config_properties

# Run data ingestion validation (Properties 2-3)
python -m tests.test_data_ingestion_properties

# Run housing stock projection test (Property 4)
python -m tests.test_housing_stock_property4

# Run equipment replacement test (Property 5)
python -m tests.test_equipment_property5

# Run fuel switching conservation test (Property 6)
python -m tests.test_fuel_switching_conservation

# Run weather analysis test (Property 7)
python -m tests.test_weather_hdd_property_visualizations

# Run simulation tests (Properties 9-10)
python -m tests.test_simulation_property9
python -m tests.test_simulation_property10

# Run aggregation tests (Properties 11-12)
python -m tests.test_aggregation_property11
python -m tests.test_aggregation_property12

# Run scenario tests (Properties 13-14)
python -m tests.test_scenario_properties
```

### Running NW Natural Source Data Validation

```bash
# Run all 12 data validation checks
python -m tests.test_nwn_data_validation

# Expected runtime: 5-12 minutes
# Output: output/nwn_data_validation/ with HTML/MD/PNG reports
```

### Code Quality Checks

```bash
# Check for syntax errors
python -m py_compile src/*.py

# Run static type checking (if mypy is installed)
# pip install mypy
python -m mypy src/ --ignore-missing-imports
```

---

## Troubleshooting

### Common Issues

#### 1. Python Version Mismatch
```
Error: Python 3.8 is not supported. Please use Python 3.9+
```

**Solution**:
```bash
# Check Python version
python --version

# If wrong version, specify explicitly
python3.11 -m venv venv
source venv/bin/activate
```

#### 2. Virtual Environment Not Activated
```
Error: ModuleNotFoundError: No module named 'pandas'
```

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Verify activation (should see (venv) prefix)
which python  # macOS/Linux
# or
where python  # Windows
```

#### 3. Missing Data Files
```
Error: FileNotFoundError: Data/NWNatural Data/premise_data_blinded.csv
```

**Solution**:
```bash
# Check data directory structure
ls -la Data/

# Create minimal test data structure
mkdir -p Data/NWNatural\ Data/
touch Data/NWNatural\ Data/premise_data_blinded.csv
touch Data/NWNatural\ Data/equipment_data_blinded.csv
touch Data/NWNatural\ Data/segment_data_blinded.csv
touch Data/NWNatural\ Data/equipment_codes.csv
touch Data/NWNatural\ Data/DailyCalDay1985_Mar2025.csv
touch Data/NWNatural\ Data/billing_data_blinded.csv

# Note: These will be empty files - model will run but with warnings
```

#### 4. Insufficient Memory
```
Error: MemoryError: Unable to allocate 8.00 GiB for an array
```

**Solution**:
- Increase available RAM
- Run on a machine with 16GB+ RAM
- Use `max_premises` parameter to limit data size:
  ```json
  {
    "name": "Baseline Limited",
    "max_premises": 10000
  }
  ```

#### 5. Permission Denied (macOS/Linux)
```
Error: Permission denied: './venv/bin/activate'
```

**Solution**:
```bash
# Make script executable
chmod +x venv/bin/activate

# Then activate
source venv/bin/activate
```

### Getting Help

If you encounter issues:

1. **Check the logs**: Console output shows detailed progress
2. **Review documentation**: See `docs/guides/RUNTIME_PLAYBOOK.md` for runtime instructions
3. **Run tests**: `python -m pytest tests/ -v` to identify issues
4. **Check data quality**: Run `python -m tests.test_nwn_data_validation` to validate source data
5. **Review property test results**: Check `output/` directory for validation reports

---

## Environment Configuration

### Configuration File

The main configuration is in `src/config.py`:

```python
# Base year for simulation
BASE_YEAR = 2025

# Default output directory
OUTPUT_DIR = "output"

# File paths for data sources
NWN_DATA_DIR = "Data/NWNatural Data/"
PREMISE_DATA = f"{NWN_DATA_DIR}premise_data_blinded.csv"
EQUIPMENT_DATA = f"{NWN_DATA_DIR}equipment_data_blinded.csv"
EQUIPMENT_CODES = f"{NWN_DATA_DIR}equipment_codes.csv"
SEGMENT_DATA = f"{NWN_DATA_DIR}segment_data_blinded.csv"
BILLING_DATA = f"{NWN_DATA_DIR}billing_data_blinded.csv"
WEATHER_CALDAY = f"{NWN_DATA_DIR}DailyCalDay1985_Mar2025.csv"
WATER_TEMP = f"{NWN_DATA_DIR}BullRunWaterTemperature.csv"
PORTLAND_SNOW = f"{NWN_DATA_DIR}Portland_snow.csv"

# End-use mapping configuration
END_USE_MAP = {
    # Maps equipment_type_code to end-use categories
    # Example: "FUR": "space_heating"
}

# Default efficiency values by end-use
DEFAULT_EFFICIENCY = {
    "space_heating": 0.85,
    "water_heating": 0.80,
    "cooking": 0.50,
    "clothes_drying": 0.70,
    "fireplace": 0.20,
    "other": 0.50
}
```

### Scenario Configuration

Scenarios are configured in JSON files in the `scenarios/` directory:

```json
{
  "name": "Baseline",
  "base_year": 2025,
  "forecast_horizon": 10,
  "housing_growth_rate": 0.012,
  "electrification_rate": 0.02,
  "efficiency_improvement": 0.015,
  "weather_assumption": "normal",
  "initial_gas_pct": 100.0,
  "use_recs_ratios": true,
  "max_premises": 0,
  "vectorized": false
}
```

### Parameter Curves

Any numeric parameter can be replaced with a time-varying curve:

```json
{
  "electrification_rate": {
    "points": {
      "2025": 0.02,
      "2028": 0.04,
      "2030": 0.08,
      "2033": 0.05,
      "2035": 0.03
    }
  }
}
```

See `docs/guides/PARAMETER_CURVES.md` for detailed documentation.

---

## Development Resources

### Project Structure

```
src/
├── config.py                    # Configuration constants
├── main.py                      # CLI entry point
├── data_ingestion.py            # Data loading and joining
├── housing_stock.py             # Housing stock model
├── equipment.py                 # Equipment inventory and replacement
├── weather.py                   # Weather data processing
├── simulation.py                # End-use simulation
├── aggregation.py               # Results aggregation
├── scenarios.py                 # Scenario management
├── validation/                  # Validation and reporting
│   ├── validation_report.py
│   ├── metadata_and_limitations.py
│   └── final_dashboard.py
├── loaders/                     # Individual data loaders
│   ├── load_premise_data.py
│   ├── load_equipment_data.py
│   └── ...
└── visualization.py             # Chart generation
```

### Documentation

- **Runtime Playbook**: `docs/guides/RUNTIME_PLAYBOOK.md` - How to run and use the model
- **Parameter Curves**: `docs/guides/PARAMETER_CURVES.md` - Time-varying parameter documentation
- **Algorithm Documentation**: `docs/model/` - Algorithm details and formulas
- **Scope Documentation**: `docs/scope/` - Project scope and limitations
- **Task Documentation**: `docs/tasks/` - Implementation details

### Specification

- **Requirements**: `.kiro/specs/nw-natural-end-use-forecasting/requirements.md`
- **Design**: `.kiro/specs/nw-natural-end-use-forecasting/design.md`
- **Tasks**: `.kiro/specs/nw-natural-end-use-forecasting/tasks.md`

---

## Next Steps

### After Installation

1. **Verify installation**:
   ```bash
   python -m pytest tests/ -v
   ```

2. **Run baseline scenario**:
   ```bash
   python -m src.main scenarios/baseline.json
   ```

3. **Explore results**:
   ```bash
   ls scenarios/baseline/
   cat scenarios/baseline/SUMMARY.md
   ```

4. **Run validation tests**:
   ```bash
   python -m tests.test_nwn_data_validation
   ```

5. **Create custom scenario**:
   - Copy `scenarios/baseline.json` to `scenarios/my_scenario.json`
   - Modify parameters
   - Run with `python -m src.main scenarios/my_scenario.json`

### Development Tasks

See `.kiro/specs/nw-natural-end-use-forecasting/tasks.md` for implementation plan.

---

## Summary

You now have the NW Natural End-Use Forecasting Model installed and ready to use. The next steps are:

1. Verify installation: `python -m pytest tests/ -v`
2. Run baseline scenario: `python -m src.main scenarios/baseline.json`
3. Explore results: Check `scenarios/baseline/` directory
4. Read documentation: Start with `docs/guides/RUNTIME_PLAYBOOK.md`
5. Begin development: See `.kiro/specs/nw-natural-end-use-forecasting/tasks.md`

Happy forecasting!