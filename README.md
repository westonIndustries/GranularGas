# NW Natural End-Use Forecasting Model

A bottom-up residential natural gas demand forecasting model for NW Natural's Integrated Resource Planning (IRP) process.

## Overview

This project builds a Python-based prototype that disaggregates residential natural gas demand by end-use (space heating, water heating, cooking, clothes drying, fireplaces, and other), enabling scenario analysis for technology adoption, electrification, and efficiency improvements.

The model ingests NW Natural's blinded premise, equipment, segment, and weather data, constructs a housing stock model with equipment inventories, simulates per-unit energy consumption driven by weather and equipment characteristics, and aggregates results to system-level demand projections.

**Status**: Academic capstone project for proof-of-concept delivery.

## Quick Links

### Documentation

- **[Project Scope](SCOPE.md)** — Final project scope, objectives, deliverables, team structure, and research plan
- **[Requirements](requirements.md)** — 10 functional and non-functional requirements defining model scope, data inputs, simulation capabilities, and output formats
- **[Design](design.md)** — Complete system architecture with 24 design decisions, module interfaces, data models, and mathematical foundations (Weibull survival model, HDD/CDD calculations, end-use disaggregation)
- **[Algorithm](ALGORITHM.md)** — Detailed algorithm explanation with step-by-step process flows and mermaid diagrams
- **[Inputs](inputs.md)** — Comprehensive specification of all input datasets: NW Natural proprietary data, tariff rates, building stock characteristics, Census demographics, weather normals, RECS microdata, and scenario configuration
- **[Outputs](outputs.md)** — Detailed specification of all model outputs: premise-level simulations, aggregated demand by end-use/segment/district, UPC validation, calibration metrics, and scenario comparisons
- **[Future Data Sources](FUTURE_DATA_SOURCES.md)** — Additional data sources that would enhance the model, organized by priority and implementation phase
- **[Tasks](tasks.md)** — Implementation plan with 14 top-level tasks, property-based tests, and checkpoints for incremental development

## Key Features

### Data Integration
- **NW Natural proprietary data**: 650,000+ active residential premises with equipment inventories, billing history, and weather data
- **Building stock proxy**: 2022 NEEA Residential Building Stock Assessment (RBSA) for Pacific Northwest characteristics
- **Equipment service life**: ASHRAE public database for state-specific equipment lifetimes
- **Validation benchmarks**: NW Natural IRP load decay forecast, EIA RECS microdata, Census housing data
- **Weather normalization**: NOAA 30-year climate normals for 11 weather stations
- **Population forecasts**: PSU (Oregon) and WA OFM (Washington) housing growth projections

### Simulation Engine
- **Weibull survival model** for equipment replacement timing (realistic failure rate distribution)
- **HDD-driven space heating** (base 65°F) scaled by equipment efficiency
- **Water heating** based on temperature differential and hot water demand
- **Baseload end-uses** (cooking, drying, fireplace) as flat annual consumption with vintage adjustments
- **Scenario-driven projections** with configurable electrification rates, efficiency improvements, and housing growth

### Validation and Calibration
- **Billing-based calibration**: Compare simulated consumption against billing-derived therms
- **IRP forecast comparison**: Validate bottom-up UPC projections against NW Natural's top-down econometric forecast
- **Property-based testing**: 14 correctness properties ensure data integrity and conservation laws
- **Vintage-cohort analysis**: Compare against era-based calibration anchors (pre-2010 ~820, 2011-2019 ~720, 2020+ ~650 therms)

## Architecture

```
Data Ingestion & Cleaning
    ↓
Housing Stock & Equipment Model
    ↓
End-Use Energy Simulation
    ↓
Aggregation & Output
```

**Modules**:
- `config.py` — Constants, file paths, end-use mappings, default parameters
- `data_ingestion.py` — CSV loading, joining, filtering, tariff processing
- `housing_stock.py` — Housing stock construction and projection
- `equipment.py` — Equipment inventory, Weibull survival, replacement cycles
- `weather.py` — Weather data processing, HDD/CDD calculation, station mapping
- `simulation.py` — End-use energy consumption calculation engine
- `aggregation.py` — Demand rollup, output formatting, comparison utilities
- `scenarios.py` — Scenario definition, parameter validation, runner
- `main.py` — CLI entry point, orchestrates pipeline

## Data Organization

```
Data/
├── NWNatural Data/              # Proprietary blinded data (premises, equipment, billing, weather)
├── 2022 RBSA Datasets/          # NEEA building stock assessment
├── ashrae/                      # ASHRAE service life and maintenance cost data
├── Residential Energy Consumption Servey/  # EIA RECS microdata (1993-2020)
├── PSU projection data/         # Population forecasts (Oregon)
├── noaa_normals/                # NOAA 30-year climate normals
├── B25034-5y-county/            # Census ACS housing vintage data
├── B25040-5y-county/            # Census ACS heating fuel data
├── B25024-5y-county/            # Census ACS housing type data
├── ofm_april1_housing.xlsx      # WA OFM housing estimates
├── Baseload Consumption Factors.csv  # DOE/RECS/RBSA baseload parameters
├── nw_energy_proxies.csv        # Compact parameter set (envelope UA, Weibull, baseload)
├── 10-Year Load Decay Forecast (2025-2035).csv  # IRP validation target
└── [tariff CSVs]                # OR/WA rate schedules and WACOG history
```

## Getting Started

### Prerequisites
- Python 3.8+
- pandas, numpy, scipy
- openpyxl (for Excel files)
- Standard library: logging, dataclasses, json

### Installation
```bash
git clone <repo>
cd Capstone-NWNatural
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### Running a Scenario
```bash
python src/main.py scenarios/baseline.json --output outputs/
```

### Development
Start with Task 1 in [tasks.md](tasks.md):
1. Set up project structure and configuration module
2. Implement data ingestion module
3. Build housing stock model
4. Implement equipment module
5. Add weather processing
6. Implement end-use simulation
7. Add aggregation and output
8. Implement scenario management
9. Create CLI entry point
10. Add validation and calibration
11. Final integration testing

Each task includes property-based tests and checkpoints for incremental validation.

## Model Outputs

The model produces:
- **Premise-level simulations**: Detailed end-use consumption per premise per year
- **Aggregated demand**: By end-use, customer segment, and IRP district
- **UPC comparison**: Model vs. IRP forecast validation
- **Calibration metrics**: Billing-based validation (MAE, R², bias)
- **Scenario analysis**: Side-by-side comparison across multiple scenarios
- **Execution logs**: Detailed logs with warnings, errors, and data quality notes

See [outputs.md](outputs.md) for complete output specifications.

## Key Design Decisions

1. **End-use categories** derived from equipment_codes.csv
2. **Weather station assignment** by IRP district
3. **HDD-driven space heating** (base 65°F)
4. **Bull Run water temperature** for water heating
5. **Baseload end-uses** as flat annual consumption
6. **Tariff-based billing conversion** using historical rate reconstruction
7. **Scenario parameters** as configuration dictionaries
8. **RBSA 2022** as building characteristics proxy
9. **ASHRAE service life** for equipment replacement timing
10. **Weibull survival model** for realistic failure rate distribution
11. **NW Natural IRP data** as validation and calibration target
12. **Green Building Registry API** for supplemental building data
13. **Baseload consumption factors** from DOE/RECS/RBSA/NEEA
14. **NW Energy Proxies** as compact parameter reference
15. **Portland snow data** for peak day analysis
16. **RBSA sub-metered data** for load shape validation
17. **2017 RBSA-II** as supplemental building stock reference
18. **Census ACS B25034** for housing vintage distribution
19. **Census ACS B25040** for gas market share tracking
20. **Census ACS B25024** for housing type distribution
21. **PSU Population Research Center** forecasts for Oregon housing growth
22. **WA OFM postcensal estimates** for Washington housing growth
23. **NOAA 30-year Climate Normals** for weather-normalized baseline
24. **EIA RECS microdata** as independent end-use validation benchmark

See [design.md](design.md) for detailed rationale and mathematical foundations.

## Limitations and Disclaimers

- **Academic prototype**: For illustrative and research purposes only; not for regulatory or financial decisions
- **Blinded data**: Prevents geographic granularity below IRP district level
- **Simplifying assumptions**: Equipment replacement, electrification rates, and weather normalization may not reflect actual market behavior
- **No climate change modeling**: Uses 1991-2020 normals; future climate change not included
- **Scenario assumptions**: Electrification and efficiency rates are user-defined, not empirically derived

## Service Territory

**Oregon** (13 counties): Multnomah, Washington, Clackamas, Lane, Marion, Yamhill, Polk, Benton, Linn, Columbia, Clatsop, Lincoln, Coos

**Washington** (3 counties): Clark, Skamania, Klickitat

## Contact

For questions or feedback, contact the capstone team or NW Natural IRP planning staff.

---

**Documentation Structure**:
- [Project Scope](SCOPE.md) — Project objectives, deliverables, and team
- [Requirements](requirements.md) — What the model must do
- [Design](design.md) — How the model works
- [Algorithm](ALGORITHM.md) — Step-by-step algorithm explanation
- [Inputs](inputs.md) — What data the model needs
- [Outputs](outputs.md) — What the model produces
- [Future Data Sources](FUTURE_DATA_SOURCES.md) — Additional data sources for enhancement
- [Tasks](tasks.md) — How to build it
