# Output Files Reference

## Overview

Each scenario run produces a folder at `scenarios/{scenario_name}/` containing all results, diagnostics, and metadata. This document describes every output file, its columns, and how to interpret it.

---

## Folder Structure

```
scenarios/Baseline/
├── Baseline.json                  # Copy of the input scenario config
├── SUMMARY.md                     # Human-readable summary report
├── metadata.json                  # Run metadata and all parameter values
├── results.csv                    # Full simulation results
├── results.json                   # Same data in JSON format
├── yearly_summary.csv             # Year-by-year aggregated summary
├── irp_comparison.csv             # Model UPC vs IRP UPC comparison
├── estimated_total_upc.csv        # Space heating + RECS non-heating estimates
├── equipment_stats.csv            # Equipment fleet statistics by year
├── premise_distribution.csv       # Per-premise therms distribution by year
├── segment_demand.csv             # Demand by segment over time
├── sample_rates.csv               # Replacement, efficiency, electrification rates
├── vintage_demand.csv             # Demand breakdown by vintage cohort
├── housing_stock.csv              # Housing stock projection
├── hdd_info.csv                   # HDD calibration info
├── hdd_history.csv                # Historical HDD by station and year
├── census_summary_b25024.csv      # Census B25024 SF/MF summary
├── census_summary_b25034.csv      # Census B25034 vintage summary
├── census_summary_b25040.csv      # Census B25040 heating fuel summary
└── recs_summary.csv               # RECS end-use benchmark summary
```

---

## Core Results Files

### results.csv

The primary output. One row per year × end-use × segment × district combination.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Simulation year (e.g., 2025, 2026, ..., 2035) |
| `end_use` | str | End-use category: `space_heating`, `water_heating`, `cooking`, `clothes_drying`, `fireplace`, `other` |
| `segment` | str | Customer segment: `RESSF`, `RESMF`, `MOBILE`, `Unclassified` |
| `district` | str | IRP district code (e.g., `MULT`, `LANE`, `MARI`) |
| `total_therms` | float | Total annual gas consumption in therms for this group |
| `premise_count` | int | Number of premises in this group |
| `use_per_customer` | float | Average therms per customer (`total_therms / premise_count`) |
| `scenario_name` | str | Scenario identifier (matches folder name) |
| `irp_upc_therms` | float | IRP forecast UPC for this year (same value for all rows in a year) |

**Note**: In the current implementation, only `space_heating` rows have non-zero `total_therms`. Other end-uses are present in the schema but not yet simulated.

### results.json

Same data as `results.csv` in JSON format. Useful for programmatic consumption.

---

### yearly_summary.csv

Aggregated year-by-year summary across all end-uses, segments, and districts.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Simulation year |
| `total_therms` | float | Total system therms across all end-uses and premises |
| `use_per_customer` | float | System-level UPC (total_therms / premise_count) |
| `premise_count` | int | Total active premises in this year |
| `irp_upc_therms` | float | IRP forecast UPC for this year |
| `scenario_name` | str | Scenario identifier |

**How to read it**: This is the primary table for comparing model UPC against the IRP forecast year by year.

---

### irp_comparison.csv

Direct comparison of model UPC against NW Natural's IRP load decay forecast.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Simulation year |
| `model_upc` | float | Bottom-up model UPC (space heating only) |
| `irp_upc` | float | NW Natural IRP forecast UPC (all end-uses) |
| `estimated_total_upc` | float | Model UPC + RECS non-heating estimates (if `use_recs_ratios=true`) |
| `total_therms` | float | Total system therms |
| `premise_count` | int | Total active premises |
| `diff_therms` | float | `model_upc - irp_upc` |
| `diff_pct` | float | `diff_therms / irp_upc × 100` |
| `model_upc_label` | str | Always `"space_heating_only"` — reminder that model UPC is not all-end-use |

**How to read it**: Positive `diff_pct` means the model is higher than the IRP. The model's space heating UPC is expected to be ~23–26% lower than the IRP's all-end-use UPC. The `estimated_total_upc` column adds RECS non-heating estimates to make the comparison more apples-to-apples.

---

### estimated_total_upc.csv

Estimated total UPC combining space heating simulation with RECS-derived non-heating end-use estimates.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Simulation year |
| `space_heating_upc` | float | Simulated space heating UPC |
| `water_heating_upc` | float | Estimated water heating UPC (space_heating × 0.704) |
| `cooking_upc` | float | Estimated cooking UPC (space_heating × 0.055) |
| `clothes_drying_upc` | float | Estimated clothes drying UPC (space_heating × 0.034) |
| `fireplace_upc` | float | Estimated fireplace UPC (space_heating × 0.085) |
| `other_upc` | float | Estimated other UPC (space_heating × 0.131) |
| `estimated_total_upc` | float | Sum of all end-use UPCs |
| `irp_upc` | float | IRP forecast UPC for reference |

**How to read it**: The `estimated_total_upc` is the best available comparison against the IRP's all-end-use forecast. It is higher than the IRP because RECS Pacific division ratios include California, which inflates non-heating shares. See [CENSUS_RECS_INTEGRATION.md](CENSUS_RECS_INTEGRATION.md).

---

## Equipment and Fleet Files

### equipment_stats.csv

Equipment fleet statistics by year, showing how the fleet composition changes over the forecast horizon.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Simulation year |
| `total_premises` | int | Total active premises |
| `total_equipment` | int | Total equipment units across all premises |
| `gas_units` | int | Equipment units with `fuel_type = 'gas'` |
| `electric_units` | int | Equipment units with `fuel_type = 'electric'` |
| `gas_pct` | float | Percentage of equipment that is gas |
| `electric_pct` | float | Percentage of equipment that is electric |
| `avg_efficiency` | float | Fleet-average equipment efficiency (AFUE) |
| `replacements` | int | Equipment units replaced this year |
| `electrifications` | int | Equipment units that switched to electric this year |

**How to read it**: Watch `electric_pct` grow over time as electrification accumulates. Watch `avg_efficiency` rise as old low-efficiency equipment is replaced with new high-efficiency units.

### premise_distribution.csv

Per-premise therms distribution by year. Useful for understanding the spread of consumption across the fleet.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Simulation year |
| `p10` | float | 10th percentile of premise-level annual therms |
| `p25` | float | 25th percentile |
| `p50` | float | Median premise-level annual therms |
| `p75` | float | 75th percentile |
| `p90` | float | 90th percentile |
| `mean` | float | Mean premise-level annual therms |
| `std` | float | Standard deviation |
| `min` | float | Minimum premise-level annual therms |
| `max` | float | Maximum premise-level annual therms |

### sample_rates.csv

Sample-derived yearly rates showing how key model parameters evolve over the forecast horizon.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Simulation year |
| `replacement_rate` | float | Fraction of equipment replaced this year |
| `electrification_rate` | float | Fraction of replacements that switched to electric |
| `avg_new_efficiency` | float | Average efficiency of newly installed equipment |
| `avg_fleet_efficiency` | float | Fleet-average efficiency across all equipment |

---

## Segment and Vintage Files

### segment_demand.csv

Demand broken down by customer segment over time.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Simulation year |
| `segment` | str | Customer segment: `RESSF`, `RESMF`, `MOBILE` |
| `total_therms` | float | Total therms for this segment in this year |
| `equipment_count` | int | Number of equipment units in this segment |
| `use_per_customer` | float | Average therms per customer in this segment |

**How to read it**: RESMF UPC should be lower than RESSF UPC due to the 0.70× segment multiplier. The gap should remain roughly constant over time unless electrification rates differ by segment.

### vintage_demand.csv

Demand broken down by construction vintage cohort over time.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Simulation year |
| `vintage_era` | str | Vintage cohort: `pre_1980`, `1980_1999`, `2000_2009`, `2010_2014`, `2015_plus` |
| `total_therms` | float | Total therms for this vintage cohort |
| `premise_count` | int | Number of premises in this cohort |
| `use_per_customer` | float | Average therms per customer in this cohort |

**How to read it**: Pre-1980 homes should have the highest UPC (1.35× multiplier). 2015+ homes should have the lowest (0.70× multiplier). The pre-1980 cohort's UPC should decline faster over time as its old equipment gets replaced with high-efficiency units.

---

## Housing Stock File

### housing_stock.csv

Housing stock projection with segment breakdown by year.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Simulation year |
| `total_units` | int | Total projected housing units |
| `RESSF` | int | Projected single-family units |
| `RESMF` | int | Projected multi-family units |
| `growth_rate` | float | Housing growth rate used (from scenario config) |
| `scenario_name` | str | Scenario identifier |

---

## Weather Files

### hdd_info.csv

HDD calibration information for this scenario run.

| Column | Type | Description |
|--------|------|-------------|
| `calibration_year` | int | Year the heating factor was calibrated against |
| `calibration_hdd` | float | Weighted average HDD for the calibration year |
| `actual_weather_year` | int | Weather year used in simulation (may differ from calibration year) |
| `actual_hdd` | float | Weighted average HDD for the actual weather year |
| `hdd_ratio` | float | `calibration_hdd / actual_hdd` |
| `config_heating_factor` | float | Heating factor from scenario config |
| `effective_heating_factor` | float | Adjusted heating factor after HDD normalization |

### hdd_history.csv

Historical weighted average HDD by year across all 11 weather stations.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Calendar year |
| `weighted_avg_hdd` | float | Weighted average HDD across all 11 stations |
| `station_count` | int | Number of stations with data for this year |

---

## Census and RECS Reference Files

### census_summary_b25024.csv

Census B25024 (Units in Structure) summary for NW Natural service territory counties.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | ACS survey year |
| `county` | str | County name |
| `total_units` | int | Total housing units |
| `sf_units` | int | Single-family units (1-unit detached + attached) |
| `mf_units` | int | Multi-family units (2+ units) |
| `mobile_units` | int | Mobile homes |
| `sf_pct` | float | Single-family share (%) |
| `mf_pct` | float | Multi-family share (%) |

### census_summary_b25034.csv

Census B25034 (Year Structure Built) summary.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | ACS survey year |
| `county` | str | County name |
| `total_units` | int | Total housing units |
| `pre_1980` | int | Units built before 1980 |
| `1980_1999` | int | Units built 1980–1999 |
| `2000_2009` | int | Units built 2000–2009 |
| `2010_plus` | int | Units built 2010 or later |
| `pre_1980_pct` | float | Pre-1980 share (%) |

### census_summary_b25040.csv

Census B25040 (House Heating Fuel) summary.

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | ACS survey year |
| `county` | str | County name |
| `total_units` | int | Total occupied housing units |
| `gas_units` | int | Units using utility gas as primary heat |
| `electric_units` | int | Units using electricity as primary heat |
| `other_units` | int | Units using other fuels |
| `gas_pct` | float | Gas heating market share (%) |

### recs_summary.csv

RECS end-use benchmark summary for Pacific division gas-heated homes.

| Column | Type | Description |
|--------|------|-------------|
| `survey_year` | int | RECS survey year (2005, 2009, 2015, 2020) |
| `end_use` | str | End-use category |
| `avg_therms` | float | Weighted average annual therms for this end-use |
| `share_of_total` | float | This end-use as a fraction of total gas consumption |
| `ratio_to_space_heating` | float | This end-use as a ratio to space heating consumption |

---

## Metadata and Config Files

### metadata.json

Complete run metadata including all scenario parameters and execution statistics.

```json
{
    "scenario_name": "Baseline",
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
    "vectorized": true,
    "total_rows": 110,
    "years_simulated": 11,
    "end_uses": ["space_heating"],
    "run_timestamp": "2026-04-27T10:30:00"
}
```

### SUMMARY.md

Human-readable summary report with:
- Configuration parameters table
- Yearly demand table (with IRP comparison if available)
- End-use breakdown table
- List of all output files

### {scenario_name}.json

Copy of the input scenario JSON config, preserved in the output folder for reproducibility.

---

## Validation Output Files

The validation suite writes additional reports to `output/` (not inside the scenario folder):

| Path | Description |
|------|-------------|
| `output/data_quality/{loader}_quality_report.html` | Per-loader data quality report |
| `output/data_quality/join_audit.html` | Cross-loader join audit |
| `output/join_integrity/join_integrity_dashboard.html` | Pass/fail dashboard |
| `output/loaders/{loader}_summary.txt` | Standalone loader diagnostic output |
| `output/loaders/{loader}_sample.csv` | Sample rows from each loader |

---

## Related Documentation

- **[SCENARIOS.md](SCENARIOS.md)** — How to configure and run scenarios
- **[ALGORITHM.md](ALGORITHM.md)** — How outputs are generated
- **[MODEL_VS_IRP_COMPARISON.md](MODEL_VS_IRP_COMPARISON.md)** — How to interpret irp_comparison.csv
- **[CENSUS_RECS_INTEGRATION.md](CENSUS_RECS_INTEGRATION.md)** — How to interpret census and RECS summary files
