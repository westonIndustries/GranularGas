# Implementation Tasks: NW Natural End-Use Forecasting Model

## Overview

This task list reflects the actual implementation of the bottom-up residential end-use demand forecasting model. All tasks correspond to implemented requirements and design components. Future work items (interactive visualization, REST API, Docker, additional end-uses) are tracked separately in the requirements and design documents.

---

## Tasks

- [x] 1. Project Structure and Configuration

  - [x] 1.1 Create `src/` package structure
    - Create `src/__init__.py`, `src/loaders/__init__.py`, `src/validation/__init__.py`
    - Create `src/loaders/_helpers.py` with `save_diagnostics(df, name)` writing HTML + MD to `output/loaders/`
    - _Requirements: 7, 13_

  - [x] 1.2 Define end-use mappings in `src/config.py`
    - Define `END_USE_MAP` mapping all equipment_type_codes to end-use categories
    - Define `DEFAULT_EFFICIENCY`, `USEFUL_LIFE`, `WEIBULL_BETA` by end-use category
    - Define `DISTRICT_WEATHER_MAP` mapping district_code_IRP to ICAO weather station codes
    - Define `VINTAGE_HEATING_MULTIPLIER` and `SEGMENT_HEATING_MULTIPLIER`
    - _Requirements: 1, 4_

  - [x] 1.3 Define all file paths and constants in `src/config.py`
    - NW Natural data paths: `PREMISE_DATA`, `EQUIPMENT_DATA`, `EQUIPMENT_CODES`, `SEGMENT_DATA`, `WEATHER_CALDAY`, `WATER_TEMP`, `BILLING_DATA`, `PORTLAND_SNOW`
    - Tariff paths: `OR_RATES`, `WA_RATES`, `OR_WACOG_HISTORY`, `WA_WACOG_HISTORY`, `OR_RATE_CASE_HISTORY`, `WA_RATE_CASE_HISTORY`
    - External data paths: RBSA 2022, RBSA 2017, ASHRAE, IRP load decay, baseload factors, NW energy proxies, Census, PSU, OFM, NOAA, RECS
    - Simulation constants: `BASE_YEAR`, `DEFAULT_BASE_TEMP`, `DEFAULT_HOT_WATER_TEMP`, `OUTPUT_DIR`
    - _Requirements: 7_

---

- [x] 2. Data Loaders — NW Natural Core Data

  - [x] 2.1 Implement NW Natural premise and equipment loaders
    - `load_premise_data.py` — filter to active residential (`custtype='R'`, `status_code='AC'`)
    - `load_equipment_data.py` — load equipment inventory CSV
    - `load_segment_data.py` — load and filter segment data to residential customers
    - `load_equipment_codes.py` — load equipment code lookup table
    - _Requirements: 1, 7_

  - [x] 2.2 Implement weather and environmental data loaders
    - `load_weather_data.py` — load daily CalDay weather CSV, parse dates, normalize column names
    - `load_water_temperature.py` — load Bull Run water temperature CSV
    - `load_snow_data.py` — load Portland daily snow data (1985–2025)
    - _Requirements: 4, 7_

  - [x] 2.3 Implement billing and tariff data loaders
    - `load_billing_data.py` — load billing CSV, parse `utility_usage` as therms
    - `load_billing_to_therms.py` — validate and clean therm values
    - `load_or_rates.py`, `load_wa_rates.py` — current rate schedules
    - `load_wacog_history.py`, `load_rate_case_history.py` — historical rate data
    - _Requirements: 7_

---

- [x] 3. Data Loaders — External Reference Data

  - [x] 3.1 Implement RBSA building stock loaders
    - `load_rbsa_site_detail.py` — 2022 RBSA SiteDetail.csv
    - `load_rbsa_hvac.py` — Mechanical_HeatingAndCooling.csv
    - `load_rbsa_water_heater.py` — Mechanical_WaterHeater.csv
    - `load_rbsa_distributions.py` — `build_rbsa_distributions()` from site_detail + hvac + water_heater
    - `load_rbsa_2017.py` — 2017 RBSA-II SiteDetail.csv for temporal comparison
    - `load_rbsam_metering.py` — stub loader for future RBSA sub-metered data
    - _Requirements: 7_

  - [x] 3.2 Implement ASHRAE equipment life loaders
    - `load_ashrae_service_life.py` — load OR and WA service life XLS files
    - `load_ashrae_maintenance_cost.py` — load OR and WA maintenance cost XLS files
    - `load_useful_life_table.py` — `build_useful_life_table()` returning state-specific useful life lookup
    - _Requirements: 3, 7_

  - [x] 3.3 Implement IRP calibration data loaders
    - `load_load_decay_forecast.py` — NW Natural 2025 IRP 10-Year Load Decay Forecast
    - `load_historical_upc.py` — historical UPC from reconstructed and simulated txt files
    - `load_baseload_factors.py` — Baseload Consumption Factors.csv + `calculate_site_baseload()`
    - `load_nw_energy_proxies.py` — nw_energy_proxies.csv (envelope UA, Weibull params, baseload)
    - _Requirements: 10_

  - [x] 3.4 Implement Census ACS data loaders
    - `load_service_territory_fips.py` — NW Natural Service Territory Census data.csv (16 counties)
    - `load_census_b25034.py` — Census API fetch + `build_vintage_distribution()`
    - `load_b25034_county.py` — offline B25034 county CSVs (2009–2023)
    - `load_b25040_county.py` — B25040 House Heating Fuel county CSVs
    - `load_b25024_county.py` — B25024 Units in Structure county CSVs
    - _Requirements: 9_

  - [x] 3.5 Implement population and housing growth loaders
    - `load_psu_forecasts.py` — PSU Population Research Center county forecasts (3 CSV format variants)
    - `load_ofm_housing.py` — WA OFM postcensal housing estimates from xlsx
    - _Requirements: 2, 9_

  - [x] 3.6 Implement NOAA and RECS loaders
    - `load_noaa_normals.py` — daily + monthly normals, `compute_weather_adjustment()`, replace -7777 with NaN
    - `load_recs_microdata.py` — RECS CSV loader + `build_recs_enduse_benchmarks()` for 2005/2009/2015/2020
    - `load_gbr_properties.py` — GBR API stub (requires `GBR_API_KEY` env var)
    - _Requirements: 4, 9_

---

- [x] 4. Data Ingestion and Join

  - [x] 4.1 Implement `build_premise_equipment_table` in `src/data_ingestion.py`
    - Join premise, equipment, segment, and equipment_codes on `blinded_id` and `equipment_type_code`
    - Derive `end_use` via `END_USE_MAP`, `efficiency` via `DEFAULT_EFFICIENCY`, `weather_station` via `DISTRICT_WEATHER_MAP`
    - Log warnings for unmapped equipment codes, missing weather station assignments, zero efficiency
    - _Requirements: 1, 7_

  - [x] 4.2 Re-export all loaders from `src/data_ingestion.py`
    - All individual loaders importable from `data_ingestion` for backward compatibility
    - _Requirements: 7_

---

- [x] 5. Data Validation and Quality Reporting

  - [x] 5.1 Implement per-loader data quality reports
    - For each loader: row count, column dtypes, null counts, unique values, min/max/mean, top-10 frequencies
    - Flag columns with >10% nulls as warnings, >50% as errors
    - Output: `output/data_quality/{loader_name}_quality_report.html` and `.md`
    - _Requirements: 8_

  - [x] 5.2 Implement cross-loader join audit
    - Count blinded_ids in premises vs equipment vs segment vs billing — match rates and orphan counts
    - Count equipment_type_codes mapped vs unmapped in END_USE_MAP
    - Count district_code_IRP values mapped vs unmapped in DISTRICT_WEATHER_MAP
    - Output: `output/data_quality/join_audit.html` and `.md`
    - _Requirements: 8_

  - [x] 5.3 Implement join integrity dashboard
    - Build premise_equipment_table and validate: end_use coverage, efficiency > 0, weather_station assigned
    - Traffic-light indicators: green (>95%), yellow (80–95%), red (<80%)
    - Output: `output/join_integrity/join_integrity_dashboard.html` and `.md`
    - _Requirements: 8_

  - [x] 5.4 Implement distribution plots for key fields
    - Histograms: equipment age, efficiency by end-use, billing therms (log scale), annual HDD by station
    - Bar charts: premises by district, equipment count by end-use, segment distribution
    - Output: `output/data_quality/distributions/` (PNGs) + `output/data_quality/distribution_summary.html`
    - _Requirements: 8_

  - [x] 5.5 Implement validation modules in `src/validation/`
    - `data_quality.py` — data quality checks and reporting
    - `join_integrity.py` — join integrity validation
    - `range_checking.py` — value range validation
    - `billing_calibration.py` — billing data calibration checks
    - `nwn_data_validation.py` — NW Natural data-specific validation
    - `validation_report.py` — consolidated validation report generation
    - `final_dashboard.py` — final validation dashboard
    - `metadata_and_limitations.py` — model metadata and limitations documentation
    - _Requirements: 8, 13_

---

- [x] 6. Housing Stock Module

  - [x] 6.1 Implement `HousingStock` dataclass in `src/housing_stock.py`
    - Fields: `year`, `premises` DataFrame, `total_units`, `units_by_segment`, `units_by_district`
    - `build_baseline_stock(premise_equipment, base_year)` — construct from premise-equipment data
    - _Requirements: 2_

  - [x] 6.2 Implement `project_stock` for future year projection
    - Apply `housing_growth_rate` from scenario config (scalar or curve via `parameter_curves.py`)
    - Simulate new construction proportional to existing segment distribution
    - _Requirements: 2_

  - [x] 6.3 Implement Census-driven SF/MF segment shift projection
    - `census_integration.py`: `load_b25024_segment_trend()`, `compute_segment_shift_rates()`, `project_segment_shares()`
    - Apply historical B25024 SF→MF shift rates to project segment composition over forecast horizon
    - _Requirements: 2, 9_

  - [x] 6.4 Property test: housing stock growth
    - **Property: projected `total_units = baseline × (1 + growth_rate)^years` within rounding tolerance**
    - Output: `output/housing_stock_projections/property_growth_results.html` and `.md`
    - _Requirements: 2, 12_

---

- [x] 7. Equipment Module

  - [x] 7.1 Implement `EquipmentProfile` dataclass and Weibull functions in `src/equipment.py`
    - `EquipmentProfile`: `equipment_type_code`, `end_use`, `efficiency`, `install_year`, `useful_life`, `fuel_type`
    - `weibull_survival(t, eta, beta)` — S(t) = exp(-(t/eta)^beta)
    - `median_to_eta(median_life, beta)` — convert ASHRAE median life to Weibull scale parameter
    - `replacement_probability(age, eta, beta)` — conditional failure probability at age t
    - _Requirements: 3_

  - [x] 7.2 Implement `build_equipment_inventory`
    - Build inventory with derived attributes from premise-equipment table
    - Use ASHRAE service life data (state-specific OR/WA) when available, fall back to `USEFUL_LIFE` defaults
    - _Requirements: 3_

  - [x] 7.3 Implement `apply_replacements` for equipment transitions
    - Probabilistic replacement using Weibull survival model each year
    - Apply scenario electrification switching rates (gas → electric/heat pump) at replacement time
    - Apply scenario efficiency improvements to newly installed equipment
    - _Requirements: 3_

  - [x] 7.4 Property test: Weibull survival monotonicity
    - **Property: S(t) <= S(t-1) for all t > 0, and S(0) = 1.0**
    - **Property: replacement_probability is always in [0, 1]**
    - Output: `output/equipment_replacement/property_weibull_results.html` and `.md`
    - _Requirements: 3, 12_

  - [x] 7.5 Property test: fuel switching conservation
    - **Property: total equipment count before and after `apply_replacements` is equal**
    - Output: `output/equipment_replacement/property_fuel_switching_results.html` and `.md`
    - _Requirements: 3, 12_

---

- [x] 8. Weather Module

  - [x] 8.1 Implement HDD calculation in `src/weather.py`
    - `compute_hdd(daily_temps, base_temp=65.0)` — HDD from daily average temperatures
    - `compute_cdd(daily_temps, base_temp=65.0)` — CDD from daily average temperatures
    - `compute_annual_hdd(weather_df, site_id, year)` — total annual HDD for a station and year
    - _Requirements: 4_

  - [x] 8.2 Implement weather station assignment and normalization
    - `assign_weather_station(district_code)` — map district to ICAO station via `DISTRICT_WEATHER_MAP`
    - `compute_water_heating_delta(water_temp_df, target_temp=120.0)` — temperature differential for water heating
    - Load NOAA 30-year Climate Normals and compute weather adjustment factor (`actual_HDD / normal_HDD`)
    - _Requirements: 4_

  - [x] 8.3 Property test: weather normalization
    - **Property: weather adjustment factor > 0 for all stations with valid normal HDD**
    - **Property: HDD is non-negative for all days**
    - Output: `output/weather_validation/property_weather_results.html` and `.md`
    - _Requirements: 4, 12_

---

- [x] 9. Simulation Module

  - [x] 9.1 Implement space heating simulation in `src/simulation.py`
    - `simulate_space_heating(equipment, annual_hdd, heating_factor)` — annual therms per premise
    - Apply `VINTAGE_HEATING_MULTIPLIER` and `SEGMENT_HEATING_MULTIPLIER` from config
    - Formula: `HDD × heating_factor × vintage_multiplier × segment_multiplier / efficiency`
    - _Requirements: 4_

  - [x] 9.2 Implement full end-use simulation runner
    - `simulate_all_end_uses(premise_equipment, weather_data, water_temp_data, year, scenario)` — run all end-uses for all premises in a year
    - Support `end_use_scope` parameter to limit simulation to specific end-uses
    - Support `max_premises` parameter for development/testing with a subset
    - Support `vectorized` parameter for vectorized vs row-by-row execution
    - _Requirements: 4, 6_

  - [x] 9.3 Implement checkpoint simulation in `src/checkpoint_simulation.py`
    - Save intermediate simulation results to disk at configurable checkpoints
    - Resume from checkpoint if simulation is interrupted
    - _Requirements: 4_

  - [x] 9.4 Property test: simulation non-negativity
    - **Property: all `total_therms` values in simulation output are >= 0**
    - **Property: UPC is non-negative for all years**
    - Output: `output/simulation_validation/property_nonneg_results.html` and `.md`
    - _Requirements: 4, 12_

---

- [x] 10. Aggregation Module

  - [x] 10.1 Implement demand aggregation in `src/aggregation.py`
    - `aggregate_by_end_use(simulation_results)` — total therms by end-use and year
    - `aggregate_by_segment(simulation_results, segments)` — total therms by segment and year
    - `aggregate_by_district(simulation_results, premises)` — total therms by district and year
    - `compute_use_per_customer(total_demand, customer_count)` — UPC calculation
    - _Requirements: 5_

  - [x] 10.2 Implement IRP comparison
    - `compare_to_irp_forecast(model_upc, irp_forecast)` — compare model UPC vs IRP load decay forecast
    - Return DataFrame with: `year`, `model_upc`, `irp_upc`, `diff_therms`, `diff_pct`
    - _Requirements: 5, 10_

  - [x] 10.3 Implement result export
    - `export_results(results, output_path, format='csv')` — export to CSV or JSON
    - _Requirements: 5_

---

- [x] 11. Scenario Module

  - [x] 11.1 Implement `ScenarioConfig` dataclass in `src/scenarios.py`
    - Fields: `name`, `base_year`, `forecast_horizon`, `housing_growth_rate`, `electrification_rate`, `efficiency_improvement`, `weather_assumption`, `initial_gas_pct`, `use_recs_ratios`, `end_use_scope`, `max_premises`, `vectorized`
    - `from_dict(data)` classmethod for loading from JSON
    - _Requirements: 6_

  - [x] 11.2 Implement `validate_scenario` and `run_scenario`
    - `validate_scenario(config)` — validate parameter ranges and combinations, return list of errors
    - `run_scenario(config, base_data)` — orchestrate full pipeline for one scenario, return (results_df, metadata)
    - _Requirements: 6_

  - [x] 11.3 Implement `compare_scenarios`
    - `compare_scenarios(results)` — side-by-side comparison of multiple scenario results
    - _Requirements: 6_

  - [x] 11.4 Implement `src/parameter_curves.py`
    - `resolve(param, year, default)` — resolve scalar or year-indexed curve to a value for a given year
    - Support linear interpolation between defined years
    - _Requirements: 6_

  - [x] 11.5 Property test: scenario output consistency
    - **Property: all `total_therms` values are >= 0 across all scenarios**
    - **Property: UPC decreases monotonically under electrification scenarios (given constant housing stock)**
    - Output: `output/scenario_validation/property_scenario_results.html` and `.md`
    - _Requirements: 6, 12_

---

- [x] 12. Census and RECS Integration

  - [x] 12.1 Implement `src/census_integration.py`
    - `load_census_distributions()` — load B25034, B25040, B25024 county data into a dict
    - `enrich_premise_equipment(premise_equipment, census)` — add Census-derived vintage and segment attributes
    - `export_census_summary(census, output_dir)` — write Census summary CSVs to scenario output folder
    - `load_b25024_segment_trend()` — load B25024 time series for SF/MF shift analysis
    - `compute_segment_shift_rates(b25024_trend)` — compute annual SF→MF shift rates from Census data
    - `project_segment_shares(base_sf_pct, base_mf_pct, shift_rates, horizon)` — project segment shares forward
    - _Requirements: 9_

  - [x] 12.2 Implement `src/recs_integration.py`
    - `load_recs_enduse_trend()` — load RECS microdata for 2005, 2009, 2015, 2020 and compute end-use shares
    - `compute_non_heating_ratios(recs_trend)` — compute non-heating end-use ratios relative to space heating
    - `export_recs_summary(recs_trend, output_dir)` — write RECS summary CSV to scenario output folder
    - _Requirements: 9_

---

- [x] 13. Calibration Module

  - [x] 13.1 Implement `src/calibration.py`
    - Load three-era historical UPC framework (pre-2010, 2011–2019, 2020+) from IRP data files
    - `calibrate_heating_factor(model_upc, target_upc)` — adjust heating_factor to align model UPC with observed UPC
    - Report calibration residuals (model UPC vs IRP UPC) for each year
    - _Requirements: 10_

  - [x] 13.2 Implement envelope efficiency module
    - `src/envelope_efficiency.py` — `project_envelope_trend()` for building envelope efficiency over time
    - Use RBSA building shell data and nw_energy_proxies.csv envelope UA values by vintage era
    - _Requirements: 2, 10_

---

- [x] 14. CLI Entry Point

  - [x] 14.1 Implement `src/main.py` CLI
    - `argparse` setup with positional `scenario_configs` and flags: `--output-dir`, `--baseline-only`, `--compare`, `--verbose`
    - `load_scenario_config(path)` — load and validate JSON scenario config
    - `load_pipeline_data()` — load all data sources, build premise-equipment table, enrich with Census and RECS
    - `run_single_scenario(config, ...)` — run one scenario and return (results_df, metadata)
    - `print_summary_statistics(results_df, metadata)` — print formatted summary to stdout
    - _Requirements: 6, 13_

  - [x] 14.2 Implement scenario output export in `main.py`
    - Write all output files to `scenarios/{scenario_name}/`: results.csv, results.json, yearly_summary.csv, metadata.json, SUMMARY.md
    - Write supplemental CSVs: equipment_stats, premise_distribution, segment_demand, sample_rates, vintage_demand, estimated_total_upc, hdd_info, hdd_history, irp_comparison, housing_stock
    - Write Census and RECS summary CSVs
    - _Requirements: 5, 6_

  - [x] 14.3 Implement `_write_summary_report` in `main.py`
    - Write `SUMMARY.md` with: configuration parameters, yearly demand table (with IRP comparison if available), end-use breakdown table, output file list
    - _Requirements: 11, 13_

---

- [x] 15. Static Visualization and Charts

  - [x] 15.1 Implement housing stock visualization in `src/visualization.py`
    - `plot_housing_stock_comparison(baseline_year, baseline_total, projected_data, output_path)` — line chart
    - `plot_segment_distribution_comparison(...)` — grouped bar chart by segment over time
    - `plot_district_distribution_comparison(...)` — grouped bar chart by district over time
    - `plot_growth_rate_analysis(...)` — projected vs expected growth rate chart
    - `plot_service_territory_map(...)` — static choropleth map of NW Natural counties with weather station markers
    - `plot_projection_summary(...)` — generate all charts and save to output directory
    - Use `matplotlib.use('Agg')` for headless execution
    - _Requirements: 11_

  - [x] 15.2 Implement scenario comparison charts in `src/scenario_charts.py`
    - `generate_scenario_charts(scenario_results, output_dir)` — line charts comparing UPC across scenarios
    - Stacked area charts showing end-use composition over time
    - Bar charts comparing scenario outcomes at target years
    - _Requirements: 11_

  - [x] 15.3 Implement housing stock visualizations in `src/housing_stock_visualizations.py`
    - Charts for housing stock composition, vintage distribution, segment trends
    - _Requirements: 11_

  - [x] 15.4 Implement zone visualization in `src/zone_visualization.py`
    - Geographic zone charts for district-level analysis
    - _Requirements: 11_

---

- [x] 16. Property-Based Testing Suite

  - [x] 16.1 Implement equipment property tests in `src/equipment_property_test.py`
    - Weibull survival monotonicity: S(t) <= S(t-1) for all t > 0
    - Replacement probability bounds: always in [0, 1]
    - Output: `output/equipment_replacement/` HTML and MD reports
    - _Requirements: 12_

  - [x] 16.2 Implement fuel switching property tests in `src/fuel_switching_property_test.py`
    - Conservation: total equipment count before and after `apply_replacements` is equal
    - Output: `output/fuel_switching/` HTML and MD reports
    - _Requirements: 12_

  - [x] 16.3 Implement scenario property tests in `src/scenario_property_tests.py`
    - Non-negativity: all `total_therms` >= 0
    - Housing stock growth: projected units = baseline × (1 + rate)^years within rounding tolerance
    - Output: `output/scenario_validation/` HTML and MD reports
    - _Requirements: 12_

  - [x] 16.4 Implement weather property report in `src/weather_property_report.py`
    - HDD non-negativity: HDD >= 0 for all days
    - Weather adjustment factor > 0 for all stations with valid normal HDD
    - Output: `output/weather_validation/` HTML and MD reports
    - _Requirements: 12_

  - [x] 16.5 Implement water heating property report in `src/water_heating_property_report.py`
    - Water temperature delta > 0 for all valid records
    - Output: `output/water_heating_validation/` HTML and MD reports
    - _Requirements: 12_
