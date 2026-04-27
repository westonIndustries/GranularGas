# Installation and Setup Guide

## Overview

This guide walks you through setting up the NW Natural End-Use Forecasting Model on your local machine for development and testing. The model is a Python-based bottom-up residential natural gas demand forecasting system.

---

## System Requirements

### Minimum Requirements
- **Python**: 3.9 or higher
- **RAM**: 8GB (laptop development), 16GB+ (server deployment)
- **Disk Space**: 10GB (data + code + outputs)
- **OS**: Windows, macOS, or Linux

### Recommended Requirements
- **Python**: 3.11 or higher
- **RAM**: 16GB+
- **Disk Space**: 20GB+
- **Git**: For version control

### Optional Requirements
- **Docker**: For containerized deployment
- **PostgreSQL**: For production data persistence
- **Redis**: For caching and async task queuing

---

## Quick Start (5 minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/nwnatural/forecast-model.git
cd forecast-model
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
python -m pytest tests/ -v
```

Expected output: All tests pass with green checkmarks.

### 5. Run Baseline Scenario

```bash
python src/main.py scenarios/baseline.json --output outputs/
```

Expected output: CSV files in `outputs/baseline/` directory.

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
# Using HTTPS (recommended for first-time users)
git clone https://github.com/nwnatural/forecast-model.git
cd forecast-model

# Or using SSH (if you have SSH keys configured)
git clone git@github.com:nwnatural/forecast-model.git
cd forecast-model
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

# Install development dependencies (optional, for testing/linting)
pip install -r requirements-dev.txt
```

### Step 5: Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Run tests
python -m pytest tests/ -v

# Check code style (optional)
python -m flake8 src/ --max-line-length=100
```

---

## Data Setup

### Directory Structure

The model expects data files in a specific directory structure:

```
forecast-model/
├── Data/
│   ├── NWNatural Data/
│   │   ├── premise_data_blinded.csv
│   │   ├── equipment_data_blinded.csv
│   │   ├── segment_data_blinded.csv
│   │   ├── billing_data_blinded.csv
│   │   └── DailyCalDay1985_Mar2025.csv
│   ├── 2022 RBSA Datasets/
│   │   ├── [RBSA building characteristics files]
│   ├── ashrae/
│   │   ├── [ASHRAE service life data]
│   ├── Baseload Consumption Factors.csv
│   ├── nw_energy_proxies.csv
│   ├── or_rates_oct_2025.csv
│   ├── or_wacog_history.csv
│   ├── ofm_april1_housing.xlsx
│   ├── NW Natural Service Territory Census data.csv
│   ├── 10-Year Load Decay Forecast (2025–2035).csv
│   └── [other data files]
├── src/
├── tests/
├── scenarios/
└── outputs/
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

### Minimal Data Setup (for testing)

If you don't have all data files, you can run tests with synthetic data:

```bash
# Generate synthetic test data
python scripts/generate_test_data.py

# Run tests with synthetic data
python -m pytest tests/ -v -k "synthetic"
```

---

## First Run

### Run Baseline Scenario

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # macOS/Linux
# or
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Run baseline scenario
python src/main.py scenarios/baseline.json --output outputs/

# Expected output:
# ========================================
# NW Natural End-Use Forecasting Model
# Scenario: baseline
# Run Date: 2026-03-17 14:45:25
# ========================================
# [... execution details ...]
# Output files written to: outputs/baseline/
```

### View Results

```bash
# List output files
ls outputs/baseline/

# View aggregated demand by end-use
head -20 outputs/baseline/aggregated_by_enduse_2025.csv

# View UPC comparison
head -20 outputs/baseline/upc_comparison_2025.csv

# View execution log
tail -50 outputs/baseline/logs/baseline_*.log
```

### Run Custom Scenario

```bash
# Create custom scenario file
cat > scenarios/my_scenario.json << 'EOF'
{
  "name": "High Electrification",
  "description": "Aggressive heat pump adoption",
  "base_year": 2025,
  "forecast_horizon": 10,
  "housing_growth_rate": 0.015,
  "electrification_rates": {
    "space_heating": 0.10,
    "water_heating": 0.15,
    "cooking": 0.02
  },
  "efficiency_improvements": {
    "space_heating": 0.02,
    "water_heating": 0.015,
    "cooking": 0.01
  },
  "weather_assumption": "normal"
}
EOF

# Run custom scenario
python src/main.py scenarios/my_scenario.json --output outputs/
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
python -m pytest tests/ -k "weibull" -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

### Code Quality Checks

```bash
# Check code style (PEP 8)
python -m flake8 src/ --max-line-length=100

# Check type hints
python -m mypy src/ --ignore-missing-imports

# Format code (auto-fix)
python -m black src/ tests/

# Check for security issues
python -m bandit -r src/
```

### Running Linter

```bash
# Install linting tools
pip install flake8 black mypy bandit

# Run all checks
flake8 src/ && black --check src/ && mypy src/
```

### Building Documentation

```bash
# Install documentation tools
pip install sphinx sphinx-rtd-theme

# Build HTML documentation
cd docs/
make html

# View documentation
open _build/html/index.html  # macOS
# or
start _build/html/index.html  # Windows
```

---

## Docker Setup (Optional)

### Build Docker Image

```bash
# Build image
docker build -t nw-natural-forecast:latest .

# Verify image
docker images | grep nw-natural-forecast
```

### Run Container

```bash
# Run baseline scenario in container
docker run -v $(pwd)/outputs:/app/outputs \
  nw-natural-forecast:latest \
  python src/main.py scenarios/baseline.json --output outputs/

# On Windows (PowerShell):
docker run -v ${PWD}/outputs:/app/outputs `
  nw-natural-forecast:latest `
  python src/main.py scenarios/baseline.json --output outputs/
```

### Docker Compose (Multi-Container)

```bash
# Start all services (API, database, cache)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
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

# Generate synthetic test data
python scripts/generate_test_data.py

# Run tests with synthetic data
python -m pytest tests/ -v
```

#### 4. Insufficient Memory
```
Error: MemoryError: Unable to allocate 8.00 GiB for an array
```

**Solution**:
- Increase available RAM
- Run on a machine with 16GB+ RAM
- Process data in smaller chunks (modify config)
- Use Docker with memory limits adjusted

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

#### 6. Port Already in Use (API)
```
Error: Address already in use: ('127.0.0.1', 8000)
```

**Solution**:
```bash
# Use different port
python src/api.py --port 8001

# Or kill process using port 8000
lsof -i :8000  # macOS/Linux
# or
netstat -ano | findstr :8000  # Windows
```

### Getting Help

If you encounter issues:

1. **Check the logs**: `outputs/{scenario_name}/logs/`
2. **Review documentation**: See [README.md](README.md) and [ALGORITHM.md](ALGORITHM.md)
3. **Run tests**: `python -m pytest tests/ -v`
4. **Check GitHub Issues**: https://github.com/nwnatural/forecast-model/issues
5. **Contact support**: support@nwnatural-forecast.example.com

---

## Environment Variables

### Configuration

Create a `.env` file in the project root:

```bash
# Data paths
DATA_DIR=./Data
OUTPUT_DIR=./outputs
SCENARIO_DIR=./scenarios

# Model parameters
BASE_YEAR=2025
FORECAST_HORIZON=10
HOUSING_GROWTH_RATE=0.012

# API configuration
API_HOST=127.0.0.1
API_PORT=8000
API_DEBUG=False

# Database (optional)
DATABASE_URL=postgresql://user:password@localhost/forecast_db
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/forecast.log
```

### Load Environment Variables

```python
# In Python code
import os
from dotenv import load_dotenv

load_dotenv()

data_dir = os.getenv('DATA_DIR', './Data')
output_dir = os.getenv('OUTPUT_DIR', './outputs')
```

---

## Next Steps

### After Installation

1. **Read the documentation**:
   - [README.md](README.md) — Project overview
   - [ALGORITHM.md](ALGORITHM.md) — Algorithm details
   - [API_DOCUMENTATION.md](API_DOCUMENTATION.md) — REST API reference

2. **Explore the code**:
   - `src/main.py` — CLI entry point
   - `src/config.py` — Configuration and constants
   - `src/data_ingestion.py` — Data loading
   - `src/simulation.py` — Core simulation engine

3. **Run examples**:
   - Baseline scenario: `python src/main.py scenarios/baseline.json`
   - Custom scenario: Create your own in `scenarios/`
   - API server: `python src/api.py` (if implemented)

4. **Start development**:
   - See [tasks.md](.kiro/specs/nw-natural-end-use-forecasting/tasks.md) for implementation plan
   - Run tests: `python -m pytest tests/ -v`
   - Check code quality: `flake8 src/`

### Development Resources

- **Specification**: `.kiro/specs/nw-natural-end-use-forecasting/`
- **Requirements**: `.kiro/specs/nw-natural-end-use-forecasting/requirements.md`
- **Design**: `.kiro/specs/nw-natural-end-use-forecasting/design.md`
- **Tasks**: `.kiro/specs/nw-natural-end-use-forecasting/tasks.md`

---

## Uninstallation

To remove the project and clean up:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv  # macOS/Linux
# or
rmdir /s venv  # Windows

# Remove project directory
cd ..
rm -rf forecast-model  # macOS/Linux
# or
rmdir /s forecast-model  # Windows
```

---

## Support and Contact

For installation issues or questions:
- **Documentation**: See links above
- **Issues**: GitHub Issues (when repository is public)
- **Email**: support@nwnatural-forecast.example.com

---

## Summary

You now have the NW Natural End-Use Forecasting Model installed and ready to use. The next steps are:

1. Verify installation: `python -m pytest tests/ -v`
2. Run baseline scenario: `python src/main.py scenarios/baseline.json --output outputs/`
3. Explore results: `ls outputs/baseline/`
4. Read documentation: Start with [README.md](README.md)
5. Begin development: See [tasks.md](.kiro/specs/nw-natural-end-use-forecasting/tasks.md)

Happy forecasting!
