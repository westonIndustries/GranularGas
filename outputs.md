# Model Outputs: NW Natural End-Use Forecasting Model

## Overview

The model produces a comprehensive set of outputs spanning premise-level simulations, aggregated demand projections, validation metrics, and scenario comparisons. All outputs are written to a user-specified output directory and include metadata for traceability and reproducibility.

## Output Directory Structure

```
outputs/
+-- {scenario_name}/
|   +-- simulation_results_{year}.csv          # Premise-level end-use consumption
|   +-- aggregated_by_enduse_{year}.csv        # Demand rollup by end-use category
|   +-- aggregated_by_segment_{year}.csv       # Demand rollup by customer segment
|   +-- aggregated_by_district_{year}.csv      # Demand rollup by IRP district
|   +-- upc_comparison_{year}.csv              # Model UPC vs. IRP forecast
|   +-- calibration_metrics.csv                # Billing-based validation metrics
|   +-- scenario_metadata.json                 # Scenario parameters and run info
+-- comparison/
|   +-- scenario_comparison.csv                # Side-by-side results across scenarios
|   +-- enduse_trends.csv                      # End-use share trends by scenario
+-- logs/
|   +-- {scenario_name}_{timestamp}.log        # Execution log with warnings/errors
```

## Premise-Level Simulation Results

### simulation_results_{year}.csv
**Purpose**: Detailed premise-level energy consumption by end-use for a given year.

**Columns**:
| Column | Type | Description |
|--------|------|-------------|
| blinded_id | int | Anonymized premise identifier |
| year | int | Simulation year |
| end_use | str | End-use category ('space_heating', 'water_heating', 'cooking', 'drying', 'fireplace', 'other') |
| annual_therms | float | Simulated annual consumption (therms) |
| equipment_type_code | str | Equipment type code |
| efficiency | float | Equipment efficiency rating used in simulation |
| fuel_type | str | Fuel type ('gas', 'electric', 'dual') |
| scenario_name | str | Scenario identifier |

**Row Count**: One row per premise per end-use per year. For a baseline year with 600,000 premises and 6 end-uses, expect ~3.6M rows.

**Data Quality**:
- `annual_therms` is always ≥ 0 (property-based test validates this)
- Premises with no equipment for an end-use are excluded (not zero-filled)
- Missing weather data results in NaN for weather-sensitive end-uses (space heating, water heating)

**Usage**: Detailed analysis, premise-level validation, debugging, research.

## Aggregated Demand by End-Use

### aggregated_by_enduse_{year}.csv
**Purpose**: Total residential gas demand by end-use category for a given year.

**Columns**:
| Column | Type | Description |
|--------|------|-------------|
| year | int | Projection year |
| end_use | str | End-use category |
| total_therms | float | Total demand (therms) |
| customer_count | int | Number of premises with this end-use |
| use_per_customer | float | Average therms per customer (total_therms / customer_count) |
| scenario_name | str | Scenario identifier |

**Row Count**: 6 end-uses × forecast_horizon years × number of scenarios.

**Example Output** (baseline scenario, 2025):
```
year,end_use,total_therms,customer_count,use_per_customer,scenario_name
2025,space_heating,250000000,600000,416.67,baseline
2025,water_heating,75000000,600000,125.00,baseline
2025,cooking,18000000,600000,30.00,baseline
2025,drying,12000000,600000,20.00,baseline
2025,fireplace,33000000,600000,55.00,baseline
2025,other,6000000,600000,10.00,baseline
```

**Validation**: Sum of all end-uses equals total system demand (property-based test).

## Aggregated Demand by Customer Segment

### aggregated_by_segment_{year}.csv
**Purpose**: Total residential gas demand by customer segment (SF vs. MF) for a given year.

**Columns**:
| Column | Type | Description |
|--------|------|-------------|
| year | int | Projection year |
| segment | str | Customer segment ('RESSF' = single-family, 'RESMF' = multi-family, 'MOBILE' = mobile home) |
| end_use | str | End-use category |
| total_therms | float | Total demand (therms) |
| customer_count | int | Number of premises in this segment with this end-use |
| use_per_customer | float | Average therms per customer |
| scenario_name | str | Scenario identifier |

**Row Count**: 3 segments × 6 end-uses × forecast_horizon years × number of scenarios.

**Example Output** (baseline scenario, 2025):
```
year,segment,end_use,total_therms,customer_count,use_per_customer,scenario_name
2025,RESSF,space_heating,200000000,480000,416.67,baseline
2025,RESSF,water_heating,60000000,480000,125.00,baseline
2025,RESMF,space_heating,40000000,100000,400.00,baseline
2025,RESMF,water_heating,12500000,100000,125.00,baseline
2025,MOBILE,space_heating,10000000,20000,500.00,baseline
2025,MOBILE,water_heating,2500000,20000,125.00,baseline
```

**Usage**: Segment-level planning, rate design analysis, targeted efficiency programs.

## Aggregated Demand by IRP District

### aggregated_by_district_{year}.csv
**Purpose**: Total residential gas demand by geographic district (IRP district code) for a given year.

**Columns**:
| Column | Type | Description |
|--------|------|-------------|
| year | int | Projection year |
| district_code_IRP | str | IRP district code (e.g., 'PORC', 'EUGN') |
| end_use | str | End-use category |
| total_therms | float | Total demand (therms) |
| customer_count | int | Number of premises in this district with this end-use |
| use_per_customer | float | Average therms per customer |
| scenario_name | str | Scenario identifier |

**Row Count**: ~15-20 districts × 6 end-uses × forecast_horizon years × number of scenarios.

**Example Output** (baseline scenario, 2025):
```
year,district_code_IRP,end_use,total_therms,customer_count,use_per_customer,scenario_name
2025,PORC,space_heating,80000000,200000,400.00,baseline
2025,PORC,water_heating,25000000,200000,125.00,baseline
2025,EUGN,space_heating,60000000,150000,400.00,baseline
2025,EUGN,water_heating,18750000,150000,125.00,baseline
```

**Usage**: Regional planning, district-level forecasting, infrastructure capacity planning.

## Use Per Customer (UPC) Comparison

### upc_comparison_{year}.csv
**Purpose**: Compare model-generated UPC projections against NW Natural's IRP load decay forecast.

**Columns**:
| Column | Type | Description |
|--------|------|-------------|
| year | int | Projection year |
| model_upc | float | Model-generated Use Per Customer (therms) |
| irp_upc | float | NW Natural IRP forecast UPC (therms) |
| difference | float | Absolute difference (model_upc - irp_upc) |
| pct_difference | float | Percentage difference ((model_upc - irp_upc) / irp_upc × 100) |
| scenario_name | str | Scenario identifier |

**Row Count**: forecast_horizon years × number of scenarios.

**Example Output** (baseline scenario, 2025-2035):
```
year,model_upc,irp_upc,difference,pct_difference,scenario_name
2025,394.0,394.0,0.0,0.0,baseline
2026,390.0,389.0,1.0,0.26,baseline
2027,386.0,384.0,2.0,0.52,baseline
2028,382.0,379.0,3.0,0.79,baseline
2029,378.0,374.0,4.0,1.07,baseline
2030,374.0,369.0,5.0,1.35,baseline
```

**Validation**: Compares bottom-up model against top-down IRP forecast. Differences > 5% warrant investigation.

**Usage**: Model validation, forecast reconciliation, scenario credibility assessment.

## Billing-Based Calibration Metrics

### calibration_metrics.csv
**Purpose**: Premise-level validation comparing simulated consumption against billing-derived therms.

**Columns**:
| Column | Type | Description |
|--------|------|-------------|
| blinded_id | int | Premise identifier |
| year | int | Calibration year |
| simulated_therms | float | Model-simulated annual consumption (therms) |
| billed_therms | float | Billing-derived annual consumption (therms) |
| absolute_error | float | \|simulated - billed\| (therms) |
| percent_error | float | (simulated - billed) / billed × 100 (%) |
| scenario_name | str | Scenario identifier |

**Row Count**: One row per premise per year (subset of premises with valid billing data).

**Aggregated Metrics** (summary statistics):
| Metric | Type | Description |
|--------|------|-------------|
| mean_absolute_error | float | Average absolute error across all premises (therms) |
| mean_bias | float | Average signed error (model bias: positive = overestimate) |
| rmse | float | Root mean squared error (therms) |
| r_squared | float | R² correlation between simulated and billed (0-1) |
| percentile_90_error | float | 90th percentile absolute error (therms) |
| premises_flagged | int | Count of premises with error > threshold (e.g., 50%) |

**Example Output** (baseline scenario, 2025):
```
blinded_id,year,simulated_therms,billed_therms,absolute_error,percent_error,scenario_name
123456,2025,385.0,380.0,5.0,1.32,baseline
123457,2025,420.0,410.0,10.0,2.44,baseline
123458,2025,350.0,360.0,-10.0,-2.78,baseline
...
```

**Summary Statistics** (appended to file or separate summary):
```
Metric,Value
mean_absolute_error,18.5
mean_bias,2.3
rmse,24.1
r_squared,0.87
percentile_90_error,42.0
premises_flagged,1250
```

**Usage**: Model calibration, identification of systematic biases, data quality assessment.

## Scenario Metadata

### scenario_metadata.json
**Purpose**: Document scenario parameters, run configuration, and execution metadata.

**Structure**:
```json
{
  "scenario_name": "baseline",
  "description": "Reference case with historical trends",
  "run_timestamp": "2026-03-17T14:30:00Z",
  "model_version": "1.0.0",
  "base_year": 2025,
  "forecast_horizon": 10,
  "housing_growth_rate": 0.01,
  "electrification_rate": {
    "space_heating": 0.02,
    "water_heating": 0.015,
    "cooking": 0.01,
    "drying": 0.02
  },
  "efficiency_improvement": {
    "space_heating": 0.01,
    "water_heating": 0.01,
    "cooking": 0.005,
    "drying": 0.005
  },
  "weather_assumption": "normal",
  "data_sources": {
    "premises": "Data/NWNatural Data/premise_data_blinded.csv",
    "equipment": "Data/NWNatural Data/equipment_data_blinded.csv",
    "weather": "Data/NWNatural Data/DailyCalDay1985_Mar2025.csv",
    "rbsa": "Data/2022 RBSA Datasets/",
    "ashrae": "Data/ashrae/",
    "irp_forecast": "Data/10-Year Load Decay Forecast (2025-2035).csv"
  },
  "execution_summary": {
    "total_premises": 650000,
    "premises_with_equipment": 648500,
    "premises_excluded": 1500,
    "total_equipment_units": 1250000,
    "simulation_years": 10,
    "total_rows_generated": 23400000,
    "execution_time_seconds": 1245,
    "warnings": 342,
    "errors": 0
  },
  "data_quality_notes": [
    "1,250 premises flagged for missing equipment data",
    "342 billing records with non-numeric utility_usage values",
    "15 weather stations with >5% missing daily data in 2024"
  ],
  "limitations": [
    "Model is for illustrative/academic purposes only",
    "Blinded premise data prevents geographic granularity below IRP district level",
    "Weather normalization uses 1991-2020 normals; future climate change not modeled",
    "Electrification rates are scenario assumptions, not empirically derived",
    "Equipment replacement timing uses Weibull model; actual replacement behavior may vary"
  ]
}
```

**Usage**: Reproducibility, audit trail, scenario documentation.

## Scenario Comparison

### comparison/scenario_comparison.csv
**Purpose**: Side-by-side comparison of key metrics across multiple scenarios.

**Columns**:
| Column | Type | Description |
|--------|------|-------------|
| year | int | Projection year |
| end_use | str | End-use category |
| scenario_name | str | Scenario identifier |
| total_therms | float | Total demand (therms) |
| use_per_customer | float | Average therms per customer |
| customer_count | int | Number of premises |

**Row Count**: forecast_horizon years × 6 end-uses × number of scenarios.

**Example Output** (comparing baseline vs. high_electrification):
```
year,end_use,scenario_name,total_therms,use_per_customer,customer_count
2025,space_heating,baseline,250000000,416.67,600000
2025,space_heating,high_electrification,250000000,416.67,600000
2026,space_heating,baseline,247500000,412.50,600000
2026,space_heating,high_electrification,245000000,408.33,600000
2027,space_heating,baseline,245000000,408.33,600000
2027,space_heating,high_electrification,240000000,400.00,600000
```

**Usage**: Scenario analysis, sensitivity testing, strategic planning.

## End-Use Trends

### comparison/enduse_trends.csv
**Purpose**: Track end-use share (%) of total demand across scenarios and years.

**Columns**:
| Column | Type | Description |
|--------|------|-------------|
| year | int | Projection year |
| end_use | str | End-use category |
| scenario_name | str | Scenario identifier |
| share_of_total | float | End-use share of total demand (%) |

**Row Count**: forecast_horizon years × 6 end-uses × number of scenarios.

**Example Output**:
```
year,end_use,scenario_name,share_of_total
2025,space_heating,baseline,63.3
2025,water_heating,baseline,19.0
2025,cooking,baseline,4.6
2025,drying,baseline,3.0
2025,fireplace,baseline,8.4
2025,other,baseline,1.5
2026,space_heating,baseline,63.5
2026,water_heating,baseline,18.8
2026,cooking,baseline,4.5
2026,drying,baseline,3.1
2026,fireplace,baseline,8.3
2026,other,baseline,1.8
```

**Usage**: End-use portfolio analysis, electrification impact assessment, demand composition trends.

## Execution Logs

### logs/{scenario_name}_{timestamp}.log
**Purpose**: Detailed execution log with warnings, errors, and data quality notes.

**Format**: Plain text with timestamps and severity levels.

**Example Content**:
```
2026-03-17 14:30:00 INFO: Starting simulation for scenario 'baseline'
2026-03-17 14:30:05 INFO: Loaded 650,000 premises from premise_data_blinded.csv
2026-03-17 14:30:10 INFO: Loaded 1,250,000 equipment records from equipment_data_blinded.csv
2026-03-17 14:30:15 WARNING: 1,250 premises have no equipment records (excluded from simulation)
2026-03-17 14:30:20 INFO: Loaded 2,500,000 billing records from billing_data_blinded.csv
2026-03-17 14:30:25 WARNING: 342 billing records have non-numeric utility_usage values (parsed as NaN)
2026-03-17 14:30:30 INFO: Loaded weather data for 11 stations (1985-2025)
2026-03-17 14:30:35 WARNING: KPDX station missing 15 days of data in 2024 (0.4%)
2026-03-17 14:30:40 INFO: Loaded RBSA 2022 data: 450 NWN-filtered sites
2026-03-17 14:30:45 INFO: Loaded ASHRAE service life data for OR and WA
2026-03-17 14:30:50 INFO: Building baseline housing stock (year 2025)
2026-03-17 14:30:55 INFO: Baseline stock: 650,000 premises, 648,500 with equipment
2026-03-17 14:31:00 INFO: Running simulation for year 2025
2026-03-17 14:31:30 INFO: Year 2025 complete: 3,900,000 simulation rows generated
2026-03-17 14:31:35 INFO: Running simulation for year 2026
...
2026-03-17 14:45:00 INFO: Simulation complete. Total execution time: 1,245 seconds
2026-03-17 14:45:05 INFO: Writing aggregated results to outputs/baseline/
2026-03-17 14:45:10 INFO: Comparing model UPC against IRP forecast
2026-03-17 14:45:15 INFO: Model UPC 2025: 394.0 therms, IRP forecast: 394.0 therms (0.0% difference)
2026-03-17 14:45:20 INFO: Calibration metrics: MAE=18.5 therms, R²=0.87
2026-03-17 14:45:25 INFO: All tests passed. Execution successful.
```

**Usage**: Debugging, data quality assessment, execution monitoring.

## Summary Statistics

### Summary Output to Console/Stdout
**Purpose**: High-level summary printed at end of execution.

**Example Output**:
```
========================================
NW Natural End-Use Forecasting Model
Scenario: baseline
Run Date: 2026-03-17 14:45:25
========================================

BASELINE YEAR (2025):
  Total Premises: 650,000
  Total Demand: 394.0 therms/customer
  By End-Use:
    Space Heating: 63.3% (250.0 therms/customer)
    Water Heating: 19.0% (75.0 therms/customer)
    Cooking: 4.6% (18.0 therms/customer)
    Drying: 3.0% (12.0 therms/customer)
    Fireplace: 8.4% (33.0 therms/customer)
    Other: 1.5% (6.0 therms/customer)

FORECAST YEAR (2035):
  Total Premises: 715,000 (+10.0%)
  Total Demand: 374.0 therms/customer (-5.1%)
  By End-Use:
    Space Heating: 62.0% (232.0 therms/customer)
    Water Heating: 19.5% (73.0 therms/customer)
    Cooking: 4.5% (17.0 therms/customer)
    Drying: 3.2% (12.0 therms/customer)
    Fireplace: 8.3% (31.0 therms/customer)
    Other: 2.0% (7.5 therms/customer)

VALIDATION:
  Model vs. IRP Forecast (2025): 0.0% difference
  Billing Calibration (R²): 0.87
  Premises Flagged: 1,250 (0.2%)

EXECUTION:
  Total Time: 1,245 seconds
  Warnings: 342
  Errors: 0
  Status: SUCCESS

Output files written to: outputs/baseline/
========================================
```

## Output File Naming Convention

All output files follow a consistent naming pattern:

- **Premise-level**: `simulation_results_{year}.csv`
- **Aggregated by end-use**: `aggregated_by_enduse_{year}.csv`
- **Aggregated by segment**: `aggregated_by_segment_{year}.csv`
- **Aggregated by district**: `aggregated_by_district_{year}.csv`
- **UPC comparison**: `upc_comparison_{year}.csv`
- **Calibration**: `calibration_metrics.csv` (all years combined)
- **Metadata**: `scenario_metadata.json`
- **Logs**: `logs/{scenario_name}_{YYYYMMDD_HHMMSS}.log`

## Data Quality and Validation

### Property-Based Test Results
All outputs are validated against correctness properties:

1. **Non-negativity**: All `annual_therms` and `total_therms` ≥ 0
2. **Conservation**: Sum of end-uses equals total demand (no therms lost/created)
3. **UPC Calculation**: `use_per_customer = total_therms / customer_count` (verified)
4. **Consistency**: Premise-level rows sum to aggregated totals
5. **Completeness**: All forecast years present; no missing data

### Metadata Inclusion
Every output file includes:
- Scenario name and parameters
- Run timestamp
- Data source versions
- Known limitations and caveats

## Output Limitations and Disclaimers

All outputs include the following disclaimer:

> **Model Limitations**: This model is a proof-of-concept prototype for academic capstone delivery. Outputs are for illustrative and research purposes only and should not be used for regulatory, financial, or operational decisions without expert review. The model makes simplifying assumptions about equipment replacement, electrification rates, and weather normalization that may not reflect actual market behavior. Blinded premise data prevents geographic granularity below IRP district level. Future climate change is not modeled.

## Summary

The model produces a comprehensive set of outputs spanning:
1. **Premise-level simulations**: Detailed end-use consumption per premise
2. **Aggregated demand**: By end-use, segment, and district
3. **Validation metrics**: UPC comparison and billing calibration
4. **Scenario analysis**: Comparison across multiple scenarios
5. **Execution metadata**: Parameters, data sources, and quality notes
6. **Logs and summaries**: Detailed execution logs and console output

All outputs are organized by scenario, include comprehensive metadata, and are validated against correctness properties to ensure data integrity and reproducibility.
