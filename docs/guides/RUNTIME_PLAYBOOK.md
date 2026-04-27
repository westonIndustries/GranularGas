# NW Natural End-Use Forecasting Model — Runtime Playbook

A step-by-step guide to set up, run, and interpret the bottom-up residential end-use demand forecasting model on a new system.

**Last Updated:** April 2026  
**Model Version:** Current Implementation  
**Status:** Active Development

---

## Part 1: System Setup

### Prerequisites

- **Python 3.9+** (check: `python --version`)
- **8GB+ RAM** (for full dataset processing)
- **~10GB disk space** (for data + outputs)
- **Git** (to clone the repository)
- **pip** (Python package manager)

### Step 1: Clone and Navigate

```bash
git clone <repository-url>
cd nw-natural-forecasting
```

### Step 2: Create Virtual Environment

```bash
# Create isolated Python environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed pandas==1.5.0 numpy==1.23.0 matplotlib==3.5.0 pytest==7.0.0 pytest-cov==4.0.0
```

If you see errors, check:
- Python version is 3.9+
- Virtual environment is activated
- Internet connection is available

### Step 4: Verify Data Directory

```bash
# Check that Data/ folder exists with required files
ls -la Data/NWNatural\ Data/

# You should see:
# - premise_data_blinded.csv
# - equipment_data_blinded.csv
# - segment_data_blinded.csv
# - equipment_codes.csv
# - DailyCalDay1985_Mar2025.csv (or DailyGasDay2008_Mar2025.csv)
# - BullRunWaterTemperature.csv
# - Portland_snow.csv
# - billing_data_blinded.csv
```

If files are missing, the model will log warnings but may not run the full simulation.

### Step 5: Create Output Directory

```bash
mkdir -p output
```

---

## Part 2: Running the Model

### Quick Start (Baseline Scenario)

```bash
# Run the full pipeline with default baseline scenario
python -m src.main scenarios/baseline.json

# Expected runtime: 5-10 minutes on a laptop with 8GB RAM
```

**What happens:**
1. Loads all data files
2. Builds housing stock model
3. Simulates end-use consumption
4. Aggregates results
5. Generates HTML + Markdown reports

### Monitoring Progress

The model prints progress to console:

```
[2026-04-27 10:30:45] INFO: Loading pipeline data...
[2026-04-27 10:30:47] INFO: Loaded 487,234 premises
[2026-04-27 10:30:48] INFO: Loading equipment data...
[2026-04-27 10:30:52] INFO: Loaded 1,203,456 equipment records
...
[2026-04-27 10:35:12] INFO: Running scenario: Baseline
[2026-04-27 10:35:15] INFO: Scenario complete: Baseline
[2026-04-27 10:35:18] INFO: Results exported to scenarios/baseline/
```

### Running Specific Scenarios

```bash
# Run high electrification scenario
python -m src.main scenarios/high_electrification.json

# Compare multiple scenarios
python -m src.main scenarios/baseline.json scenarios/high_electrification.json --compare

# Run with custom output directory
python -m src.main scenarios/baseline.json --output-dir output/my_run
```

### Running Individual Property Tests

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

### Running NW Natural Source Data Validation Suite

```bash
# Run all 12 data validation checks with HTML + MD + PNG output
python -m tests.test_nwn_data_validation

# Expected runtime: 5-12 minutes (loads all NW Natural source files)
```

**What happens:**
1. Runs 12 validation checks across all NW Natural source data
2. Generates HTML + Markdown reports with embedded charts
3. Exports CSV files for flagged records (duplicates, suspicious quantities)
4. Produces a summary dashboard linking all individual reports

**Output:** `output/nwn_data_validation/` (see Part 3 for full listing)

---

## Part 3: Understanding the Output Structure

After running, check the `output/` directory:

```
output/
├── config_validation/           # Configuration validation tests
│   ├── config_completeness.html
│   └── config_completeness.md
├── data_quality/                # Data ingestion quality reports
│   ├── premise_data_quality_report.html
│   ├── equipment_data_quality_report.html
│   ├── join_audit.html
│   ├── validation_failures.csv
│   ├── column_coverage.html
│   ├── date_ranges.html
│   ├── distribution_summary.html
│   └── distributions/           # PNG charts
├── join_integrity/              # Join validation reports
│   ├── joined_table_quality_report.html
│   ├── enduse_mapping_audit.html
│   ├── efficiency_validation.html
│   ├── weather_station_audit.html
│   └── join_integrity_dashboard.html
├── nwn_data_validation/         # NW Natural source data validation (12 checks)
│   ├── validation_dashboard.html  # Summary dashboard with all 12 checks
│   ├── validation_dashboard.md
│   ├── referential_integrity.html # 15.1 Orphan blinded_ids across tables
│   ├── equipment_code_validity.html # 15.2 Equipment codes vs equipment_codes.csv
│   ├── duplicate_detection.html   # 15.3 Duplicate premise-equipment rows
│   ├── duplicate_equipment.csv    # Export of all duplicate rows
│   ├── weather_station_coverage.html # 15.4 District → weather station mapping
│   ├── billing_coverage.html      # 15.5 Billing data coverage by premise/district
│   ├── weather_continuity.html    # 15.6 Missing dates and gaps per station
│   ├── segment_consistency.html   # 15.7 One segment per premise check
│   ├── equipment_quantity.html    # 15.8 QTY sanity (suspicious values)
│   ├── suspicious_quantities.csv  # Export of QTY > 5 rows
│   ├── state_district_crosscheck.html # 15.9 OR/WA state vs district consistency
│   ├── billing_reasonableness.html # 15.10 Therm values < 1 or > 500
│   ├── temperature_bounds.html    # 15.11 Temps outside -10°F to 115°F
│   ├── temporal_alignment.html    # 15.12 Date range overlap across datasets
│   └── *.png                      # Charts embedded in reports
├── checkpoint_core/             # Core model verification
│   ├── housing_verification.html
│   ├── equipment_verification.html
│   ├── weather_verification.html
│   └── zone_verification_map.html
├── housing_stock_projections/   # Housing stock tests
│   └── property4_results.html
├── equipment_replacement/       # Equipment replacement tests
│   └── property5_results.html
├── fuel_switching/              # Fuel switching tests
│   └── property6_results.html
├── weather_analysis/            # Weather processing tests
│   └── property7_results.html
├── water_heating/               # Water heating tests
│   └── property8_results.html
├── simulation/                  # Simulation tests
│   ├── property9_results.html
│   └── property10_results.html
├── aggregation/                 # Aggregation tests
│   ├── property11_results.html
│   └── property12_results.html
├── scenarios/                   # Scenario tests
│   ├── property13_results.html
│   └── property14_results.html
├── checkpoint_final/            # Final results
│   ├── baseline_results.html
│   ├── scenario_comparison.html
│   └── final_dashboard.html
└── validation/                  # Validation reports
    ├── VALIDATION_REPORT.html
    ├── VALIDATION_REPORT.md
    ├── irp_comparison.csv
    └── metadata.json
```

### Scenario Results Structure

When you run a scenario, results are saved to `scenarios/{scenario_name}/`:

```
scenarios/baseline/
├── baseline.json                # Input configuration (copy)
├── results.csv                  # Full results (year x end-use)
├── results.json                 # Same data in JSON format
├── yearly_summary.csv           # Year-by-year aggregated summary
├── metadata.json                # Scenario configuration and run metadata
├── SUMMARY.md                   # Human-readable summary
├── housing_stock.csv            # Housing stock projection with segment breakdown
├── equipment_stats.csv          # Equipment stats over time (gas vs electric, efficiency)
├── premise_distribution.csv     # Per-premise therms distribution by year
├── segment_demand.csv           # Demand by segment over time
├── sample_rates.csv             # Sample-derived yearly rates (replacement, efficiency, electrification)
├── vintage_demand.csv          # Vintage demand breakdown
├── estimated_total_upc.csv      # Estimated total UPC with end-use breakdown
├── hdd_history.csv             # HDD info and history
├── irp_comparison.csv          # IRP comparison (model vs NW Natural forecast)
└── census_summary/             # Census ACS summary CSVs (if Census data loaded)
```

---

## Part 4: Key Commands Reference

### Basic Commands

```bash
# Activate environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run baseline scenario
python -m src.main scenarios/baseline.json

# Run specific scenario
python -m src.main scenarios/high_electrification.json

# Compare scenarios
python -m src.main scenarios/baseline.json scenarios/high_electrification.json --compare

# Run with custom output
python -m src.main scenarios/baseline.json --output-dir output/my_run

# Run baseline-only (skip comparison)
python -m src.main scenarios/baseline.json --baseline-only

# Run individual data loader
python -m src.loaders.load_premise_data

# Run NW Natural source data validation suite
python -m tests.test_nwn_data_validation

# Run all tests
pytest tests/ -v
```

### Testing Commands

```bash
# Run specific property test
python -m tests.test_config_properties
python -m tests.test_data_ingestion_properties
python -m tests.test_housing_stock_property4
python -m tests.test_equipment_property5
python -m tests.test_fuel_switching_conservation
python -m tests.test_weather_hdd_property_visualizations
python -m tests.test_simulation_property9
python -m tests.test_simulation_property10
python -m tests.test_aggregation_property11
python -m tests.test_aggregation_property12
python -m tests.test_scenario_properties

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Utility Commands

```bash
# Generate comparison charts
python generate_comparison.py

# Generate pipeline report
python generate_pipeline_report.py

# Create charts from results
python create_charts.py

# Run checkpoint verification
python run_checkpoint_core.py

# Run scenario comparison
python run_scenario_comparison.py
```

---

## Part 5: Interpreting Results

### Key Metrics to Monitor

1. **Use Per Customer (UPC)** - Average annual natural gas consumption per residential customer (therms/year)
   - Typical values: 6.0-8.5 therms/yr depending on vintage
   - Compare to IRP forecast in `irp_comparison.csv`

2. **End-Use Breakdown** - Distribution of demand across end-uses
   - Space heating: 60-70% of total residential gas demand
   - Water heating: 15-25%
   - Cooking: 5-8%
   - Drying: 3-5%
   - Fireplaces/decorative: 2-4%
   - Other/miscellaneous: 1-3%

3. **Electrification Impact** - Reduction in gas demand from fuel switching
   - Each 1% electrification rate = 0.5-1.0% reduction in gas space heating demand
   - Heat pump adoption reduces space heating by 30-50%

### Property Test Interpretation

| Test | Purpose | Key Metric | Good | Problem |
|------|---------|-----------|------|---------|
| Property 1 | Configuration completeness | All constants defined | 100% | Missing config |
| Property 2 | Data filtering | Active residential premises | >95% | Data quality issues |
| Property 3 | Join integrity | Valid end-use + efficiency | 100% | Invalid equipment |
| Property 4 | Housing stock projection | Formula match | ±0.1% | Projection bug |
| Property 5 | Weibull survival | Monotonic decreasing | Yes | Survival increases |
| Property 6 | Fuel switching | Equipment conservation | 0 difference | Equipment lost/created |
| Property 7 | HDD computation | Non-negative, exclusive | Yes | Calculation bug |
| Property 9 | Simulation | Non-negative therms | All ≥ 0 | Negative consumption |
| Property 10 | Efficiency impact | Monotonic decreasing | Yes | Efficiency bug |
| Property 11 | Aggregation | Sum matches total | 0 difference | Therms lost/created |
| Property 12 | UPC calculation | Valid with count=0 | Handled | Division error |
| Property 13 | Scenario determinism | Identical results | 0 difference | Non-deterministic |
| Property 14 | Scenario validation | Catches invalid params | All tests pass | Validation bug |

### NW Natural Source Data Validation Checks

The model includes 12 comprehensive validation checks for source data quality:

| Check | What it catches | Key metric | Action if fails |
|-------|----------------|-----------|-----------------|
| 15.1 Referential Integrity | Orphan blinded_ids | Match rate per table | Investigate data gaps |
| 15.2 Equipment Code Validity | Unknown equipment codes | % valid codes | Update equipment_codes.csv |
| 15.3 Duplicate Detection | Exact duplicate rows | Duplication rate | Check for data entry errors |
| 15.4 Weather Station Coverage | Unmapped districts | Unmapped premise count | Update DISTRICT_WEATHER_MAP |
| 15.5 Billing Coverage | Premises without billing | Coverage % | Check billing data completeness |
| 15.6 Weather Continuity | Missing dates | Gap count per station | Check weather data quality |
| 15.7 Segment Consistency | 0 or 2+ segments per premise | Count by category | Investigate segment data |
| 15.8 Equipment Quantity | QTY ≤ 0 or > 5 | Suspicious row count | Verify equipment counts |
| 15.9 State-District Cross-Check | OR/WA state mismatch | Mismatch count | Check district assignments |
| 15.10 Billing Reasonableness | Therms < 1 or > 500 | % flagged | Investigate billing anomalies |
| 15.11 Temperature Bounds | Temps outside -10°F to 115°F | Out-of-range count | Check weather data quality |
| 15.12 Temporal Alignment | Date range gaps | Overlap period | Check data freshness |

---

## Part 6: Troubleshooting

### Common Issues and Solutions

#### Issue: "FileNotFoundError: Data/NWNatural Data/premise_data_blinded.csv"

**Cause:** Data files are missing or in wrong location.

**Fix:**
```bash
# Check data directory structure
ls -la Data/NWNatural\ Data/

# If files are missing, copy them from the source
# (Ask your data provider for the files)
```

#### Issue: "MemoryError: Unable to allocate X GB"

**Cause:** Not enough RAM to load all data.

**Fix:**
```bash
# Run with smaller dataset (if available)
python -m src.main scenarios/baseline.json --baseline-only

# Or increase system RAM
# (Minimum 8GB recommended, 16GB preferred)
```

#### Issue: "Property test failed: All therms >= 0"

**Cause:** Simulation produced negative consumption (bug).

**Fix:**
1. Check `output/simulation/property9_results.html` for details
2. Look for premises with negative therms
3. Check if efficiency values are > 1.0 (invalid)
4. Review simulation logic in `src/simulation.py`

#### Issue: "Model UPC is >10% different from IRP forecast"

**Cause:** Model assumptions don't match historical data.

**Fix:**
1. Check `output/checkpoint_simulation/irp_comparison.html`
2. Review baseline assumptions in `scenarios/baseline.json`
3. Check data quality reports in `output/data_quality/`
4. Adjust parameters (e.g., efficiency, baseload factors)
5. Re-run simulation

#### Issue: "ImportError: No module named 'src'"

**Cause:** Python path issue or virtual environment not activated.

**Fix:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Ensure you're in the project root directory
cd nw-natural-forecasting

# Install dependencies
pip install -r requirements.txt
```

#### Issue: "JSONDecodeError: Expecting value: line 1 column 1 (char 0)"

**Cause:** Scenario JSON file is empty or corrupted.

**Fix:**
```bash
# Check the JSON file
cat scenarios/baseline.json

# Recreate from template if needed
cp scenarios/_template.json scenarios/baseline.json
```

### Debugging Tips

1. **Enable verbose logging:**
   ```bash
   python -m src.main scenarios/baseline.json --verbose
   ```

2. **Check logs:** Look for ERROR or WARNING messages in console output

3. **Review property test results:** They indicate where problems are

4. **Check data quality reports:** Look for missing or invalid data

5. **Verify assumptions:** Review scenario parameters and defaults

---

## Part 7: Customizing Scenarios

### Scenario Configuration

Edit `scenarios/baseline.json`:

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

Or shorthand:
```json
{
  "electrification_rate": {
    "2025": 0.02,
    "2028": 0.04,
    "2030": 0.08
  }
}
```

### Creating New Scenarios

1. Copy an existing scenario:
   ```bash
   cp scenarios/baseline.json scenarios/my_scenario.json
   ```

2. Edit the parameters:
   ```json
   {
     "name": "My Scenario",
     "base_year": 2025,
     "forecast_horizon": 10,
     "housing_growth_rate": 0.015,
     "electrification_rate": 0.05,
     "efficiency_improvement": 0.02,
     "weather_assumption": "warm"
   }
   ```

3. Run the scenario:
   ```bash
   python -m src.main scenarios/my_scenario.json
   ```

---

## Part 8: Advanced Usage

### Running with Census Integration

The model can integrate Census ACS data for more accurate projections:

```bash
# Ensure Census data is available in Data/B25034-5y/, Data/B25040-5y-county/, etc.
python -m src.main scenarios/baseline.json
```

Census integration provides:
- Vintage distribution (B25034)
- Heating fuel mix (B25040)
- Segment distribution (B25024)
- Historical trends for calibration

### Running with RECS Integration

The model can use EIA RECS data for end-use benchmarking:

```bash
# Ensure RECS data is available in Data/Residential Energy Consumption Survey/
python -m src.main scenarios/baseline.json
```

RECS integration provides:
- End-use share trends (1993-2020)
- Non-heating ratios relative to space heating
- Regional benchmarks (Pacific division)

### Batch Processing

```bash
# Run multiple scenarios sequentially
for scenario in baseline high_electrification policy_ramp_test; do
  echo "Running $scenario..."
  python -m src.main scenarios/$scenario.json --output-dir output/$scenario
done
```

### Automated Testing

```bash
# Run all tests with coverage report
pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run specific test category
pytest tests/test_*.py -k "property"  # All property tests
pytest tests/test_*.py -k "validation"  # Validation tests
pytest tests/test_*.py -k "integration"  # Integration tests
```

### Performance Optimization

For large datasets, enable vectorized operations:

```json
{
  "name": "Baseline Vectorized",
  "vectorized": true,
  "max_premises": 100000
}
```

Vectorized mode:
- Processes premises in batches
- Reduces memory usage
- Faster for large datasets

---

## Part 9: Development Workflow

### Adding New Features

1. **Update requirements:** Add dependencies to `requirements.txt`
2. **Update config:** Add constants to `src/config.py`
3. **Implement feature:** Add code to appropriate module
4. **Add tests:** Create tests in `tests/test_*.py`
5. **Update documentation:** Update this playbook and other docs
6. **Run validation:** Ensure all tests pass

### Code Structure

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

### Testing Strategy

1. **Unit tests:** Test individual functions
2. **Property tests:** Validate correctness properties
3. **Integration tests:** Test pipeline integration
4. **Validation tests:** Check data quality and assumptions
5. **Performance tests:** Monitor runtime and memory usage

---

## Part 10: Support Resources

### Documentation

- **This playbook:** Runtime instructions and troubleshooting
- **Parameter Curves Guide:** `docs/guides/PARAMETER_CURVES.md`
- **API Documentation:** `docs/api/API_DOCUMENTATION.md` (for web dashboard)
- **Model Documentation:** `docs/model/` (algorithm details)
- **Scope Documentation:** `docs/scope/` (project scope and limitations)
- **Task Documentation:** `docs/tasks/` (implementation details)

### Data Sources

- **NW Natural Data:** Proprietary customer and equipment data
- **Census ACS:** Housing characteristics and fuel mix
- **NOAA Normals:** Climate data for weather stations
- **EIA RECS:** End-use consumption benchmarks
- **ASHRAE:** Equipment service life and maintenance costs
- **PSU Forecasts:** Population and housing growth projections

### Getting Help

If you encounter issues:

1. **Check the logs** — Look for ERROR or WARNING messages
2. **Review property test results** — They indicate where problems are
3. **Check data quality reports** — Look for missing or invalid data
4. **Verify assumptions** — Review scenario parameters and defaults
5. **Check documentation** — Review relevant guides and references
6. **Contact the development team** — Provide error messages and output files

### Known Limitations

1. **Current scope:** Space heating simulation is primary focus
2. **Data vintage:** RBSA data is 2022, may not reflect current conditions
3. **Weather assumption:** Uses NOAA normals, not actual weather
4. **Behavioral changes:** Does not account for occupant behavior changes
5. **Economic factors:** No economic optimization or market dynamics
6. **Regional variation:** Equipment efficiency data from ASHRAE may vary

---

## Quick Reference

### Command Cheat Sheet

```bash
# Basic workflow
source venv/bin/activate
python -m src.main scenarios/baseline.json
python -m src.main scenarios/baseline.json scenarios/high_electrification.json --compare

# Testing
pytest tests/ -v
python -m tests.test_nwn_data_validation

# Development
pytest tests/ --cov=src --cov-report=html
python generate_comparison.py
python create_charts.py
```

### Output File Quick Reference

| File | Purpose | Key Metric |
|------|---------|-----------|
| `validation_dashboard.html` | NW Natural source data validation | All 12 checks OK? |
| `config_completeness.html` | Configuration validation | All constants defined? |
| `join_integrity_dashboard.html` | Data quality | 100% valid end-uses? |
| `property12_results.html` | UPC calculation | Model vs IRP match? |
| `irp_comparison.html` | Forecast comparison | Within ±5% of IRP? |
| `billing_calibration.html` | Billing validation | R² > 0.8? |
| `final_dashboard.html` | Overall status | All tests pass? |
| `scenarios/{name}/SUMMARY.md` | Scenario results | Key metrics summary |

### Interpretation Quick Guide

| Metric | Good | Acceptable | Problem |
|--------|------|-----------|---------|
| Property tests | All 🟢 | 1-2 🟡 | Any 🔴 |
| Source data validation | 12/12 OK | 10-11 OK | <10 OK |
| Model vs IRP UPC | ±2% | ±5% | >±10% |
| Billing R² | >0.85 | 0.75-0.85 | <0.75 |
| Data filter rate | >95% | 85-95% | <85% |
| Join integrity | 100% | 99%+ | <99% |
| Electrification impact | 0.5-1.0%/1% | 0.3-0.5%/1% | <0.3%/1% |

---

**Remember:** This model is for illustrative and academic purposes. Results should be validated against actual utility data and used in conjunction with professional judgment.

For questions or issues, refer to the documentation or contact the development team.