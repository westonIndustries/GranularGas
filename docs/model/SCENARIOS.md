# Scenario Configuration Guide

## Overview

Scenarios are the primary way to run the model. Each scenario is a JSON file that defines a named set of assumptions about the future — how fast housing grows, how quickly equipment electrifies, how much efficiency improves. The model runs each scenario independently and writes all results to a dedicated output folder.

---

## Running Scenarios

```bash
# Run a single scenario
python -m src.main scenarios/baseline.json

# Run with a custom output directory
python -m src.main scenarios/baseline.json --output-dir output/my_run

# Run two scenarios and compare them
python -m src.main scenarios/baseline.json scenarios/high_electrification.json --compare

# Run baseline only (skip comparison even if multiple configs given)
python -m src.main scenarios/baseline.json scenarios/alt.json --baseline-only

# Enable verbose logging
python -m src.main scenarios/baseline.json --verbose
```

Each scenario writes its results to `scenarios/{scenario_name}/` next to the JSON config file.

---

## Scenario JSON Structure

```json
{
    "name": "Baseline",
    "description": "Business as usual — moderate growth, low electrification",
    "base_year": 2025,
    "forecast_horizon": 10,
    "housing_growth_rate": 0.01,
    "electrification_rate": 0.02,
    "efficiency_improvement": 0.01,
    "weather_assumption": "normal",
    "initial_gas_pct": 76.0,
    "use_recs_ratios": true,
    "end_use_scope": "space_heating",
    "max_premises": 0,
    "vectorized": true
}
```

---

## Parameter Reference

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Scenario name. Used as the output folder name. Must be filesystem-safe (no slashes). |
| `base_year` | int | Base year for simulation. Should match the calibration year (2025). |
| `forecast_horizon` | int | Number of years to project forward. `10` produces 2025–2035. |

### Demand Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `housing_growth_rate` | float or curve | `0.01` | Annual housing stock growth rate. `0.01` = 1%/year. |
| `electrification_rate` | float or curve | `0.02` | Fraction of equipment replacements that switch to electric. `0.02` = 2% of replacements electrify each year. |
| `efficiency_improvement` | float or curve | `0.01` | Annual efficiency improvement applied to newly installed gas equipment. `0.01` = 1%/year improvement in new equipment AFUE. |
| `weather_assumption` | string | `"normal"` | Weather basis for simulation. Currently `"normal"` uses actual historical HDD. `"warm"` and `"cold"` are planned for future work. |

### Calibration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `initial_gas_pct` | float | `76.0` | Percentage of all housing units (gas + non-gas) that use natural gas as primary heat. Used to estimate total territory housing units from the model's gas-customer count. |

### Output Control Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_recs_ratios` | bool | `true` | If `true`, adds RECS-derived non-heating end-use estimates to produce an estimated total UPC alongside the space-heating-only UPC. |
| `end_use_scope` | string | `"space_heating"` | Which end-uses to simulate. Currently only `"space_heating"` is implemented. `"all"` is planned for future work. |
| `max_premises` | int | `0` | Limit simulation to the first N premises. `0` = use all premises. Useful for fast development runs (e.g., `max_premises: 1000`). |
| `vectorized` | bool | `true` | Use vectorized (NumPy/Pandas) simulation instead of row-by-row iteration. Vectorized is ~10–50× faster. Set to `false` only for debugging. |

---

## Parameter Curves

Any numeric parameter can be specified as a year-indexed curve instead of a scalar. This allows parameters to change over the forecast horizon.

### Scalar (constant over time)
```json
"housing_growth_rate": 0.01
```

### Year-indexed curve (changes over time)
```json
"housing_growth_rate": {
    "2025": 0.008,
    "2028": 0.012,
    "2032": 0.010,
    "2035": 0.009
}
```

The `src/parameter_curves.py` module resolves curves using linear interpolation between defined years. Years before the first key use the first value; years after the last key use the last value.

**Example**: For the curve above, the resolved values are:
- 2025: 0.008
- 2026: 0.009 (interpolated)
- 2027: 0.011 (interpolated)
- 2028: 0.012
- 2030: 0.011 (interpolated)
- 2032: 0.010
- 2035: 0.009

This is useful for modeling policy ramp-ups (e.g., electrification rate starts low and accelerates) or economic cycles (e.g., housing growth slows during a recession).

---

## Example Scenarios

### Baseline (Business as Usual)
```json
{
    "name": "Baseline",
    "description": "Moderate growth, low electrification, gradual efficiency improvement",
    "base_year": 2025,
    "forecast_horizon": 10,
    "housing_growth_rate": 0.01,
    "electrification_rate": 0.02,
    "efficiency_improvement": 0.01,
    "weather_assumption": "normal",
    "initial_gas_pct": 76.0,
    "use_recs_ratios": true,
    "end_use_scope": "space_heating",
    "max_premises": 0,
    "vectorized": true
}
```

### High Electrification
```json
{
    "name": "High_Electrification",
    "description": "Aggressive heat pump adoption driven by policy incentives",
    "base_year": 2025,
    "forecast_horizon": 10,
    "housing_growth_rate": 0.01,
    "electrification_rate": {
        "2025": 0.03,
        "2028": 0.07,
        "2032": 0.10
    },
    "efficiency_improvement": 0.015,
    "weather_assumption": "normal",
    "initial_gas_pct": 76.0,
    "use_recs_ratios": true,
    "end_use_scope": "space_heating",
    "max_premises": 0,
    "vectorized": true
}
```

### Fast Development Run (subset of premises)
```json
{
    "name": "Dev_Test",
    "description": "Quick test run on 1000 premises",
    "base_year": 2025,
    "forecast_horizon": 3,
    "housing_growth_rate": 0.01,
    "electrification_rate": 0.02,
    "efficiency_improvement": 0.01,
    "weather_assumption": "normal",
    "initial_gas_pct": 76.0,
    "use_recs_ratios": false,
    "end_use_scope": "space_heating",
    "max_premises": 1000,
    "vectorized": true
}
```

---

## Output Folder Structure

Each scenario produces a folder at `scenarios/{scenario_name}/` containing:

```
scenarios/Baseline/
├── Baseline.json              # Copy of the input config
├── SUMMARY.md                 # Human-readable summary report
├── metadata.json              # Run metadata and all parameter values
├── results.csv                # Full results (year × end-use × segment × district)
├── results.json               # Same data in JSON format
├── yearly_summary.csv         # Year-by-year aggregated summary
├── irp_comparison.csv         # Model UPC vs IRP UPC comparison
├── estimated_total_upc.csv    # Space heating + RECS non-heating estimates
├── equipment_stats.csv        # Equipment fleet statistics by year
├── premise_distribution.csv   # Per-premise therms distribution by year
├── segment_demand.csv         # Demand by segment over time
├── sample_rates.csv           # Replacement, efficiency, electrification rates by year
├── vintage_demand.csv         # Demand breakdown by vintage cohort
├── housing_stock.csv          # Housing stock projection with segment breakdown
├── hdd_info.csv               # HDD calibration info
├── hdd_history.csv            # Historical HDD by station and year
├── census_summary_b25024.csv  # Census B25024 SF/MF summary
├── census_summary_b25034.csv  # Census B25034 vintage summary
├── census_summary_b25040.csv  # Census B25040 heating fuel summary
└── recs_summary.csv           # RECS end-use benchmark summary
```

See [OUTPUT_FILES.md](OUTPUT_FILES.md) for a full description of every file and column.

---

## Comparing Scenarios

When two or more scenario configs are passed with `--compare`, the model generates a comparison report showing the difference in UPC, total therms, and electrification rate between scenarios.

```bash
python -m src.main scenarios/baseline.json scenarios/high_electrification.json --compare
```

The comparison is written to `scenarios/comparison/` and includes side-by-side tables and charts.

---

## Scenario Validation

Before running, the model validates the scenario config and logs any issues:

- `name` must be non-empty and filesystem-safe
- `base_year` must be between 2020 and 2030
- `forecast_horizon` must be between 1 and 50
- `housing_growth_rate` must be between 0.0 and 0.05 (0–5%/year)
- `electrification_rate` must be between 0.0 and 1.0
- `efficiency_improvement` must be between 0.0 and 0.05
- `weather_assumption` must be one of: `"normal"`, `"warm"`, `"cold"`
- `initial_gas_pct` must be between 1.0 and 100.0

Validation errors are logged and the run is aborted. Validation warnings (e.g., unusually high growth rate) are logged but do not stop the run.

---

## Related Documentation

- **[ALGORITHM.md](ALGORITHM.md)** — How scenarios drive the simulation loop
- **[FORMULAS.md](FORMULAS.md)** — Parameter definitions and formulas
- **[OUTPUT_FILES.md](OUTPUT_FILES.md)** — Full description of every output file
