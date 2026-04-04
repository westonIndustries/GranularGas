# Implementation Plan: NW Natural End-Use Forecasting Model

## Overview

Build a bottom-up residential end-use demand forecasting model in Python. The implementation follows the pipeline architecture: data ingestion â†’ housing stock model â†’ end-use simulation â†’ aggregation/output. Each task builds incrementally, wiring modules together as they are completed. All code lives under `src/` with CSV data read from `Data/`.

## Tasks

**Task rules:**
- Each sub-task has a maximum of 6 bullet items
- Every property test must output results to the `output/` folder as both HTML and Markdown (.md)
- Property test outputs include pass/fail status, data summaries, and any generated plots

- [x] 1. Set up project structure and configuration module

  - [x] 1.1 Create `src/` package structure
    - Create `src/__init__.py`
    - Create `src/loaders/__init__.py`
    - Create `src/loaders/_helpers.py` with `save_diagnostics()` and `save_quality_report()` (HTML + MD)
    - Create `src/validation/__init__.py`
    - _Requirements: 7.5, 7.6_

  - [x] 1.2 Define end-use and equipment mappings in `src/config.py`
    - Define `END_USE_MAP` dictionary mapping equipment_type_code to end-use categories
    - Define `DEFAULT_EFFICIENCY` dictionary by end-use category
    - Define `USEFUL_LIFE` dictionary by end-use category
    - Define `WEIBULL_BETA` dictionary with shape parameters by end-use category
    - Define `DISTRICT_WEATHER_MAP` dictionary mapping district codes to weather station SiteIds
    - _Requirements: 1.1, 1.4, 3.2_

  - [x] 1.3 Define NW Natural proprietary file paths in `src/config.py`
    - Define `NWN_DATA_DIR` pointing to `Data/NWNatural Data/`
    - Define paths: `PREMISE_DATA`, `EQUIPMENT_DATA`, `EQUIPMENT_CODES`, `SEGMENT_DATA`
    - Define paths: `BILLING_DATA`, `BILLING_DATA_SMALL`
    - Define paths: `WEATHER_CALDAY`, `WEATHER_GASDAY`, `WATER_TEMP`, `PORTLAND_SNOW`
    - _Requirements: 7.1, 7.2_

  - [x] 1.4 Define tariff and rate file paths in `src/config.py`
    - Define paths: `OR_RATES`, `OR_RATE_CASE_HISTORY`, `OR_WACOG_HISTORY`
    - Define paths: `WA_RATES`, `WA_RATE_CASE_HISTORY`, `WA_WACOG_HISTORY`
    - Define `OR_CURRENT_RATE` (1.41220) and `WA_CURRENT_RATE` (1.24164)
    - _Requirements: 7.1, 7.3_

  - [x] 1.5 Define external data source paths in `src/config.py`
    - Define RBSA 2022 paths: `RBSA_2022_DIR`, `RBSA_2022_SITE_DETAIL`, `RBSA_2022_HVAC`, `RBSA_2022_WATER_HEATER`, `RBSA_2022_STOVE_OVEN`, `RBSA_2022_LAUNDRY`, `RBSA_2022_BUILDING_SHELL`
    - Define ASHRAE paths: `ASHRAE_DIR`, `ASHRAE_OR_SERVICE_LIFE`, `ASHRAE_WA_SERVICE_LIFE`, `ASHRAE_OR_MAINTENANCE_COST`, `ASHRAE_WA_MAINTENANCE_COST`
    - Define IRP/calibration paths: `IRP_LOAD_DECAY_FORECAST`, `LOAD_DECAY_DESCRIPTION`, `LOAD_DECAY_RECONSTRUCTED`, `LOAD_DECAY_SIMULATED`
    - Define baseload/proxy paths: `BASELOAD_FACTORS_CSV`, `NW_ENERGY_PROXIES_CSV`, `IRP_CONTEXT`, `EQUIPMENT_LIFE_MATH`
    - Define RBSA metering paths: `RBSAM_Y1_DIR`, `RBSAM_Y2_DIR`, `RBSAM_DATA_DICT`, `RBSA_2017_DIR`
    - _Requirements: 3.1, 3.2, 8.3_

  - [x] 1.6 Define API and Census constants in `src/config.py`
    - Define `GBR_API_BASE_URL`, `GBR_API_KEY_ENV_VAR`
    - Define Census constants: `CENSUS_API_BASE`, `CENSUS_ACS1_TEMPLATE`, `CENSUS_ACS5_TEMPLATE`, `CENSUS_B25034_GROUP`, `CENSUS_B25040_GROUP`, `CENSUS_B25024_GROUP`
    - Define Census file paths: `NWN_SERVICE_TERRITORY_CSV`, `B25034_BACKUP_DIR`, `B25034_COUNTY_DIR`, `B25040_COUNTY_DIR`, `B25024_COUNTY_DIR`, `PSU_PROJECTION_DIR`
    - Define WA OFM path: `OFM_HOUSING_XLSX`
    - Define NOAA constants: `NOAA_NORMALS_DIR`, `NOAA_CDO_API_BASE`, `NOAA_CDO_TOKEN_ENV_VAR`, `ICAO_TO_GHCND`
    - Define RECS constants: `RECS_DIR`, `RECS_2020_CSV`, `RECS_2015_CSV`, `RECS_2009_CSV`, `RECS_2005_CSV`, `RECS_PACIFIC_DIVISION`, `RECS_FUELHEAT_GAS`
    - _Requirements: 2.4, 7.2, 7.4_

  - [x] 1.7 Define simulation parameters in `src/config.py`
    - Define `BASE_YEAR` (2025)
    - Define `DEFAULT_BASE_TEMP` (65.0Â°F), `DEFAULT_HOT_WATER_TEMP` (120.0Â°F)
    - Define `DEFAULT_COLD_WATER_TEMP` (55.0Â°F), `DEFAULT_DAILY_HOT_WATER_GALLONS` (64.0)
    - Define `LOG_LEVEL`, `LOG_FORMAT`, `OUTPUT_DIR`
    - _Requirements: 4.2_

  - [x] 1.8 Write property test for config completeness with diagnostic output
    - **Property 1: All equipment_type_codes in END_USE_MAP resolve to a valid end-use category string**
    - Verify all END_USE_MAP values are non-empty strings
    - Verify all DEFAULT_EFFICIENCY keys match END_USE_MAP values, and all values are in (0, 1]
    - Verify all USEFUL_LIFE keys match END_USE_MAP values, and all values are positive integers
    - Verify all DISTRICT_WEATHER_MAP values are valid ICAO station codes present in ICAO_TO_GHCND
    - Verify all file path constants reference files that exist on disk (report missing as warnings)
    - Output: `output/config_validation/config_completeness.html` and `.md` with pass/fail per check
    - **Validates: Requirements 1.1, 1.4**

- [ ] 2. Implement data ingestion module
  - [x] 2.1 Create `src/loaders/` package with individual data loaders (one file per data source)
    - Each loader is a standalone script: `python -m src.loaders.<name>` loads data, prints summary, saves diagnostics to `output/loaders/`
    - Shared helper `_helpers.py` provides `save_diagnostics(df, name)` for consistent output
    - `data_ingestion.py` re-exports all loaders for backward compatibility
    - Log warnings for missing or malformed rows
    - _Requirements: 2.2, 2.4, 3.1, 3.2, 7.1, 7.2, 7.3, 7.4, 8.3_

    - [x] 2.1.1 Core NW Natural data loaders (7 files in `src/loaders/`)
      - `load_premise_data.py` â€” load and filter to active residential premises (custtype='R', status_code='AC')
      - `load_equipment_data.py` â€” load equipment inventory CSV
      - `load_segment_data.py` â€” load and filter segment data to residential customers
      - `load_equipment_codes.py` â€” load equipment code lookup table
      - `load_weather_data.py` â€” load daily weather CSV (CalDay or GasDay), parse dates
      - `load_water_temperature.py` â€” load Bull Run water temperature CSV, parse dates
      - `load_snow_data.py` â€” load Portland daily snow data (1985-2025)
      - _Requirements: 2.2, 7.2_

    - [x] 2.1.2 Billing and tariff data loaders (6 files in `src/loaders/`)
      - `load_billing_data.py` â€” load billing_data_blinded.csv, parse utility_usage from dollar strings, parse GL_revenue_date to year/month
      - `load_or_rates.py` â€” load or_rates_oct_2025.csv. OR Schedule 2 = $1.41220/therm
      - `load_wa_rates.py` â€” load wa_rates_nov_2025.csv. WA Schedule 2 = $1.24164/therm
      - `load_wacog_history.py` â€” load or_wacog_history.csv / wa_wacog_history.csv
      - `load_rate_case_history.py` â€” load or_rate_case_history.csv / wa_rate_case_history.csv
      - `load_billing_to_therms.py` â€” build_historical_rate_table + convert_billing_to_therms
      - _Requirements: 7.1, 7.3_

    - [x] 2.1.3 RBSA building stock data loaders (6 files in `src/loaders/`)
      - `load_rbsa_site_detail.py` â€” load 2022 RBSA SiteDetail.csv, filter to NWN service territory
      - `load_rbsa_hvac.py` â€” load Mechanical_HeatingAndCooling.csv
      - `load_rbsa_water_heater.py` â€” load Mechanical_WaterHeater.csv
      - `load_rbsa_distributions.py` â€” build_rbsa_distributions from site_detail + hvac + water_heater
      - `load_rbsam_metering.py` â€” load RBSA sub-metered end-use data (~300MB TXT files), chunked reading
      - `load_rbsa_2017.py` â€” load 2017 RBSA-II SiteDetail.csv for temporal comparison
      - _Requirements: 3.1, 3.2, 7.4_

    - [x] 2.1.4 ASHRAE equipment life and maintenance data loaders (3 files in `src/loaders/`)
      - `load_ashrae_service_life.py` â€” load ASHRAE service life XLS for OR and WA
      - `load_ashrae_maintenance_cost.py` â€” load ASHRAE maintenance cost XLS for OR and WA
      - `load_useful_life_table.py` â€” build state-specific useful life lookup from ASHRAE data
      - _Requirements: 3.2_

    - [x] 2.1.5 IRP load decay and calibration data loaders (5 files in `src/loaders/`)
      - `load_load_decay_forecast.py` â€” load NW Natural 2025 IRP 10-Year Load Decay Forecast
      - `load_historical_upc.py` â€” load prior load decay data (reconstructed + simulated txt files)
      - `load_baseload_factors.py` â€” load Baseload Consumption Factors.csv + calculate_site_baseload
      - `load_nw_energy_proxies.py` â€” load nw_energy_proxies.csv (envelope UA, Weibull params, baseload)
      - _Requirements: 8.3_

    - [x] 2.1.6 Green Building Registry API integration (1 file in `src/loaders/`)
      - `load_gbr_properties.py` â€” fetch_gbr_properties + build_gbr_building_profiles. Requires GBR_API_KEY env var
      - _Requirements: 3.1_

    - [x] 2.1.7 Census ACS housing data loaders (5 files in `src/loaders/`)
      - `load_service_territory_fips.py` â€” load NW Natural Service Territory Census data.csv (16 counties)
      - `load_census_b25034.py` â€” fetch Census ACS B25034 via API + build_vintage_distribution
      - `load_b25034_county.py` â€” load offline B25034 county CSVs from Data/B25034-5y-county/
      - `load_b25040_county.py` â€” load B25040 (House Heating Fuel) county CSVs
      - `load_b25024_county.py` â€” load B25024 (Units in Structure) county CSVs
      - _Requirements: 2.4, 7.4_

    - [x] 2.1.8 Population and housing growth forecast loaders (2 files in `src/loaders/`)
      - `load_psu_forecasts.py` â€” load PSU Population Research Center county forecasts (3 CSV format variants)
      - `load_ofm_housing.py` â€” load WA OFM postcensal housing estimates from xlsx
      - _Requirements: 2.4_

    - [x] 2.1.9 NOAA climate normals and weather adjustment (1 file in `src/loaders/`)
      - `load_noaa_normals.py` â€” load daily + monthly normals, compute_weather_adjustment. Replace -7777 with NaN
      - _Requirements: 7.2_

    - [x] 2.1.10 EIA RECS microdata loaders and benchmarks (1 file in `src/loaders/`)
      - `load_recs_microdata.py` â€” load RECS CSV + build_recs_enduse_benchmarks. Handle column name differences across survey years
      - _Requirements: 8.3_

  - [x] 2.2 Implement `build_premise_equipment_table` join function
    - Join premise, equipment, segment, and equipment_codes DataFrames on `blinded_id` and `equipment_type_code`
    - Derive `end_use` column using `END_USE_MAP` from config
    - Derive `efficiency` column using `DEFAULT_EFFICIENCY` where not available
    - Derive `weather_station` column using `DISTRICT_WEATHER_MAP`
    - Document assumptions for missing data as log warnings
    - _Requirements: 1.4, 2.1, 3.1, 7.4, 8.1_

  - [x] 2.3 Write data ingestion validation suite with diagnostic outputs
    - All outputs saved to `output/data_quality/` as both HTML and Markdown (.md)
    - **Property 2: Filtering preserves only active residential premises â€” output contains only custtype='R' and status_code='AC'**
    - **Validates: Requirements 1.2, 7.1, 7.4**

    - [x] 2.3.1 Per-loader data quality reports
      - For each loader, generate an HTML + MD report with: row count, column dtypes, null counts per column, unique value counts, min/max/mean for numerics, top-10 value frequencies for categoricals
      - Include filter pass rates (e.g. "72% of premises are active residential", "85% of equipment codes map to END_USE_MAP")
      - Flag columns with >10% nulls as warnings, >50% as errors
      - Output: `output/data_quality/{loader_name}_quality_report.html` and `.md`

    - [x] 2.3.2 Cross-loader join audit
      - Count blinded_ids in premises vs equipment vs segment vs billing â€” how many match, how many orphans in each direction
      - Count equipment_type_codes that map to END_USE_MAP vs unmapped codes (list the unmapped ones)
      - Count district_code_IRP values that map to DISTRICT_WEATHER_MAP vs unmapped
      - Produce a join summary table: source, total_ids, matched_ids, orphan_ids, match_rate
      - Output: `output/data_quality/join_audit.html` and `.md`

    - [x] 2.3.3 Sample mismatches export
      - Export CSV of rows that fail key validations: null end_use, zero/negative efficiency, missing weather_station, unparseable billing amounts, missing blinded_id joins
      - Include the reason for each flagged row
      - Output: `output/data_quality/validation_failures.csv`

    - [x] 2.3.4 Column coverage matrix
      - For each NW Natural file (premise, equipment, segment, codes, billing, weather), list expected columns vs actual columns present
      - Flag missing expected columns, unexpected extra columns
      - Output: `output/data_quality/column_coverage.html` and `.md`

    - [x] 2.3.5 Data freshness and date range check
      - For each time-series file (weather, billing, WACOG, rate cases, water temp, snow), report min/max dates and total record count
      - Flag files that don't extend to 2025 as potentially stale
      - Output: `output/data_quality/date_ranges.html` and `.md`

    - [x] 2.3.6 Distribution plots for key fields
      - Histogram: equipment age distribution (from install year)
      - Histogram: efficiency values by end-use category
      - Histogram: billing utility_usage amounts (log scale)
      - Histogram: annual HDD by weather station
      - Bar chart: premises by district_code_IRP
      - Bar chart: equipment count by end_use category
      - Bar chart: segment distribution (RESSF vs RESMF vs MOBILE)
      - Pie chart: fuel type mix from RBSA HVAC data
      - All saved as PNG + embedded in HTML/MD summary
      - Output: `output/data_quality/distributions/` (PNGs) + `output/data_quality/distribution_summary.html` and `.md`

  - [ ] 2.4 Write join integrity validation suite with diagnostic outputs
    - All outputs saved to `output/join_integrity/` as both HTML and Markdown (.md)
    - **Property 3: Every row in premise_equipment_table has a non-null end_use category and a valid efficiency > 0**
    - **Validates: Requirements 1.4, 3.1**

    - [ ] 2.4.1 Joined table quality report
      - Build `premise_equipment_table` from all four source tables
      - Generate HTML + MD report with: total row count, unique premises, unique equipment codes, column dtypes, null counts, value distributions for derived columns (end_use, efficiency, weather_station)
      - Report join expansion factor (rows in joined table / unique premises)
      - Output: `output/join_integrity/joined_table_quality_report.html` and `.md`

    - [ ] 2.4.2 End-use mapping completeness audit
      - For every unique equipment_type_code in the joined table, show: code, mapped end_use (or UNMAPPED), row count, % of total
      - Summarize: total mapped vs unmapped codes, total mapped vs unmapped rows
      - List all unmapped codes with their equipment_class and description from equipment_codes
      - Output: `output/join_integrity/enduse_mapping_audit.html` and `.md` + `enduse_mapping_detail.csv`

    - [ ] 2.4.3 Efficiency validation report
      - For each end_use category, show: count, min/max/mean/median efficiency, % using default vs data-supplied efficiency
      - Flag rows with efficiency <= 0 or > 1.0 (out of valid range)
      - Flag rows where efficiency was filled from DEFAULT_EFFICIENCY (show how many per end_use)
      - Histogram: efficiency distribution by end_use category (PNG)
      - Output: `output/join_integrity/efficiency_validation.html` and `.md` + PNGs

    - [ ] 2.4.4 Weather station assignment audit
      - For each district_code_IRP, show: district, assigned weather_station, premise count, % of total
      - Flag districts with no weather station mapping
      - Map visualization: premises by weather station (bar chart)
      - Output: `output/join_integrity/weather_station_audit.html` and `.md`

    - [ ] 2.4.5 Join integrity summary dashboard
      - Single-page HTML + MD combining all 2.4 checks into a pass/fail dashboard
      - Property 3 check: % of rows with non-null end_use AND efficiency > 0 (target: 100%)
      - Traffic light indicators: green (>95%), yellow (80-95%), red (<80%) for each check
      - Links to detailed reports from 2.4.1-2.4.4
      - Output: `output/join_integrity/join_integrity_dashboard.html` and `.md`

- [ ] 3. Checkpoint â€” Verify data ingestion pipeline
  - All outputs saved to `output/checkpoint_ingestion/` as HTML + MD

  - [ ] 3.1 Pipeline readiness dashboard
    - Check which of the 53 data sources loaded successfully vs missing/errored
    - Compute overall readiness score (% of sources available)
    - Traffic-light status per data source group (NW Natural, tariff, RBSA, Census, etc.)
    - List blocking issues (sources required for simulation that are missing)
    - Output: `output/checkpoint_ingestion/pipeline_readiness.html` and `.md`
    - _Requirements: 7.4, 8.1_

  - [ ] 3.2 Data volume summary report
    - For each loaded table: row count, column count, memory usage
    - Expected vs actual row counts where known (e.g. ~500K premises, ~1M equipment)
    - Flag tables with zero rows or unexpectedly low counts
    - Output: `output/checkpoint_ingestion/data_volumes.html` and `.md`
    - _Requirements: 7.1, 10.1_

  - [ ] 3.3 Premise-equipment table profile
    - Run `build_premise_equipment_table` on actual data
    - Report: total rows, unique premises, join expansion factor, end_use coverage %, efficiency coverage %
    - Top-10 equipment types by count, top-10 districts by premise count
    - Output: `output/checkpoint_ingestion/pet_profile.html` and `.md`
    - _Requirements: 1.4, 2.1, 3.1_

  - [ ] 3.4 Service territory geographic coverage map
    - Map of NW Natural service territory counties color-coded by premise count
    - Weather station markers with district assignments
    - Table: county, state, premise count, % of total, assigned weather station
    - Output: `output/checkpoint_ingestion/service_territory_map.html` and `.md` (map as PNG)
    - _Requirements: 2.2, 4.1_

  - [ ] 3.5 Equipment and vintage distribution charts
    - Bar chart: equipment count by end-use category (space_heating, water_heating, cooking, drying, fireplace, other)
    - Histogram: premise vintage (construction year) distribution by decade
    - Stacked bar: equipment fuel type by end-use (gas vs electric)
    - Treemap or sunburst: equipment types nested by end-use category
    - Output: `output/checkpoint_ingestion/equipment_vintage_charts.html` and `.md` (PNGs embedded)
    - _Requirements: 1.4, 3.1_

  - [ ] 3.6 Cross-validation against external benchmarks
    - Compare model premise counts by county vs Census B25034 housing unit counts (bar chart, side-by-side)
    - Compare model gas heating share by county vs Census B25040 utility gas share (scatter plot)
    - Compare model end-use consumption split vs RECS 2020 Pacific division benchmarks (stacked bar)
    - Report discrepancies > 10% as warnings
    - Output: `output/checkpoint_ingestion/cross_validation.html` and `.md` (PNGs embedded)
    - _Requirements: 5.3, 10.2, 10.3_

- [ ] 4. Implement housing stock module

  - [x] 4.1 Create `src/housing_stock.py` â€” HousingStock dataclass
    - Define `HousingStock` dataclass: year, premises DataFrame, total_units, units_by_segment, units_by_district
    - Implement `build_baseline_stock(premise_equipment, base_year)`
    - Compute `total_units`, `units_by_segment`, `units_by_district` from unique blinded_ids
    - _Requirements: 2.1, 2.2, 5.4_

  - [x] 4.2 Implement `project_stock` for future year projection
    - Apply housing growth rate from scenario config to project total units
    - Simulate new construction additions proportional to existing segment distribution
    - _Requirements: 2.3, 6.1_

  - [ ] 4.3 Property test: housing stock projection
    - **Property 4: Projected total_units = baseline Ã— (1 + growth_rate)^(years), within rounding tolerance**
    - Line graph: baseline vs projected total units over time
    - Bar chart: segment distribution comparison (baseline vs projected)
    - Bar chart: district distribution comparison (baseline vs projected)
    - Output: `output/housing_stock_projections/property4_results.html` and `.md` (PNGs embedded)
    - **Validates: Requirements 2.3, 6.3**


- [x] 5. Implement equipment module

  - [x] 5.1 Create `src/equipment.py` — EquipmentProfile and Weibull functions
    - Define `EquipmentProfile` dataclass: equipment_type_code, end_use, efficiency, install_year, useful_life, fuel_type
    - Implement `weibull_survival(t, eta, beta)` — S(t) = exp(-(t/eta)^beta)
    - Implement `median_to_eta(median_life, beta)`
    - Implement `replacement_probability(age, eta, beta)`
    - Implement `build_equipment_inventory(premise_equipment)`
    - _Requirements: 3.1, 3.2_

  - [x] 5.2 Implement `apply_replacements` for equipment transitions
    - Compute replacement probability using Weibull survival model
    - Use probabilistic replacement (not deterministic age cutoff)
    - Replace units based on scenario adoption rates
    - Apply electrification switching rates (gas → electric/heat pump)
    - Apply efficiency improvements from scenario config
    - _Requirements: 3.3, 3.4, 6.1_

  - [ ] 5.3 Property test: Weibull survival monotonicity
    - **Property 5: S(t) <= S(t-1) for all t > 0, and S(0) = 1.0**
    - **Property 5b: replacement_probability is always in [0, 1]**
    - Line graph: Weibull survival curves by end-use category
    - Line graph: replacement probability by equipment age per end-use
    - Scatter: equipment age distribution with replacement probability overlay
    - Output: `output/equipment_replacement/property5_results.html` and `.md`
    - **Validates: Requirements 3.3**

  - [ ] 5.4 Property test: fuel switching conservation
    - **Property 6: Total equipment count before and after apply_replacements is equal**
    - Pie chart: fuel type split before vs after replacements
    - Bar chart: fuel switching volume by end-use category
    - Stacked bar: equipment count by end-use before vs after
    - Output: `output/fuel_switching/property6_results.html` and `.md`
    - **Validates: Requirements 3.3, 3.4**

- [x] 6. Implement weather processing module

  - [x] 6.1 Create `src/weather.py` — HDD/CDD and station mapping
    - Implement `compute_hdd(daily_temps, base_temp=65.0)`
    - Implement `compute_cdd(daily_temps, base_temp=65.0)`
    - Implement `compute_annual_hdd(weather_df, site_id, year)`
    - Implement `compute_water_heating_delta(water_temp_df, target_temp=120.0, year=None)`
    - Implement `assign_weather_station(district_code)`
    - _Requirements: 4.1, 7.2_

  - [ ] 6.2 Property test: HDD computation
    - **Property 7: HDD >= 0, exactly one of HDD/CDD is positive (or both zero at base temp)**
    - Line graph: daily HDD and CDD by day of year for KPDX
    - Heatmap: monthly average HDD by station
    - Box plot: annual HDD distribution across all 11 stations
    - Map: weather stations on OpenStreetMap with HDD color coding
    - Output: `output/weather_analysis/property7_results.html` and `.md`
    - **Validates: Requirements 4.1, 4.2**

  - [ ] 6.3 Property test: water heating delta
    - **Property 8: delta_t > 0 when cold water temp < target_temp**
    - Line graph: daily delta-T by day of year (2008-2025 overlay)
    - Seasonal pattern: monthly delta-T with min/max bands
    - Scatter: water temp vs air temp (KPDX) with regression line
    - Bar chart: estimated annual WH therms per customer by station
    - Output: `output/water_heating/property8_results.html` and `.md`
    - **Validates: Requirements 4.1, 4.2**

- [ ] 7. Checkpoint — Verify core model components
  - All outputs saved to `output/checkpoint_core/` as HTML + MD

  - [ ] 7.1 Housing stock verification report
    - Run `build_baseline_stock` on actual data
    - Report total units, segment split, district split
    - Compare premise counts vs Census B25034 county totals
    - Bar chart: premises by segment
    - Output: `output/checkpoint_core/housing_verification.html` and `.md`
    - _Requirements: 2.1, 2.2_

  - [ ] 7.2 Equipment module verification report
    - Run `build_equipment_inventory` on actual data
    - Report equipment counts by end-use, Weibull params per end-use
    - Histogram: equipment age distribution
    - Output: `output/checkpoint_core/equipment_verification.html` and `.md`
    - _Requirements: 3.1, 3.2_

  - [ ] 7.3 Weather module verification report
    - Compute annual HDD for all 11 stations for 2024
    - Compare to NOAA normals, report weather adjustment factors
    - Heatmap: monthly HDD by station
    - Output: `output/checkpoint_core/weather_verification.html` and `.md`
    - _Requirements: 4.1, 7.2_

- [ ] 8. Implement end-use energy simulation module

  - [ ] 8.1 Create `src/simulation.py` — per-end-use functions
    - Implement `simulate_space_heating(equipment, annual_hdd, heating_factor)`
    - Implement `simulate_water_heating(equipment, delta_t, gallons_per_day=64.0)`
    - Implement `simulate_baseload(equipment, annual_consumption)`
    - _Requirements: 4.1, 4.2, 4.4_

  - [ ] 8.2 Implement `simulate_all_end_uses` orchestrator
    - Dispatch to simulation function per premise based on end_use
    - Collect weather data (HDD, delta-T) per premise's weather station
    - Return DataFrame: blinded_id, end_use, annual_therms, efficiency, year
    - Maintain separation between end uses (no double-counting)
    - _Requirements: 1.4, 4.2, 4.3, 5.4_

  - [ ] 8.3 Property test: simulation non-negativity
    - **Property 9: All simulated annual_therms >= 0**
    - Histogram: annual therms distribution by end-use
    - Box plot: annual therms by end-use (median, quartiles)
    - Stacked bar: average therms by end-use and vintage era
    - Map: average therms per customer by district (choropleth)
    - Output: `output/simulation/property9_results.html` and `.md`
    - **Validates: Requirements 4.2**

  - [ ] 8.4 Property test: efficiency impact monotonicity
    - **Property 10: Higher efficiency → lower or equal therms**
    - Line graph: therms vs efficiency by end-use
    - Bar chart: efficiency improvement potential by end-use
    - Scatter: equipment age vs efficiency rating
    - Output: `output/simulation/property10_results.html` and `.md`
    - **Validates: Requirements 4.2, 3.2**

- [ ] 9. Implement aggregation and output module

  - [ ] 9.1 Create `src/aggregation.py` — rollup functions
    - Implement `aggregate_by_end_use(simulation_results)`
    - Implement `aggregate_by_segment(simulation_results, segments)`
    - Implement `aggregate_by_district(simulation_results, premises)`
    - Implement `compute_use_per_customer(total_demand, customer_count)`
    - Implement `compare_to_irp_forecast(model_upc, irp_forecast)`
    - Implement `export_results(results, output_path, format='csv')`
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 9.1_

  - [ ] 9.2 Property test: aggregation conservation
    - **Property 11: Sum across end uses = total demand (no therms lost/created)**
    - Bar chart: total demand by aggregation level — all should match
    - Waterfall: end-use contributions summing to total
    - Output: `output/aggregation/property11_results.html` and `.md`
    - **Validates: Requirements 5.1, 5.4**

  - [ ] 9.3 Property test: use-per-customer
    - **Property 12: UPC = total / count for count > 0, handles count == 0**
    - Line graph: model UPC vs IRP forecast UPC (2025-2035)
    - Bar chart: UPC by vintage era vs anchors (820/720/650)
    - Output: `output/aggregation/property12_results.html` and `.md`
    - **Validates: Requirements 5.2**

- [ ] 10. Checkpoint — Verify simulation and aggregation
  - All outputs saved to `output/checkpoint_simulation/` as HTML + MD

  - [ ] 10.1 Simulation results summary
    - Run baseline simulation on actual data
    - Report: total demand, UPC, demand by end-use and segment
    - Stacked bar: end-use composition of total demand
    - Output: `output/checkpoint_simulation/simulation_summary.html` and `.md`
    - _Requirements: 5.1, 10.1_

  - [ ] 10.2 Model vs IRP comparison
    - Compare model UPC to IRP 10-year forecast
    - Line graph: model UPC vs IRP UPC (2025-2035)
    - Report: year-by-year difference and % deviation
    - Output: `output/checkpoint_simulation/irp_comparison.html` and `.md`
    - _Requirements: 10.2, 10.3_

  - [ ] 10.3 Billing calibration check
    - Compare simulated vs billing-derived therms per premise
    - Scatter: simulated vs billed therms (with 1:1 line)
    - Report: MAE, mean bias, R²
    - Output: `output/checkpoint_simulation/billing_calibration.html` and `.md`
    - _Requirements: 7.1, 10.2_

- [ ] 11. Implement scenario management module

  - [ ] 11.1 Create `src/scenarios.py` — ScenarioConfig and validation
    - Define `ScenarioConfig` dataclass: name, base_year, forecast_horizon, housing_growth_rate, electrification_rate, efficiency_improvement, weather_assumption
    - Implement `validate_scenario(config)`
    - _Requirements: 6.1, 6.4, 8.1_

  - [ ] 11.2 Implement `run_scenario` pipeline orchestrator
    - Load base data, build baseline housing stock
    - For each year: project stock, apply replacements, simulate, aggregate
    - Store per-year results with scenario_name label
    - Log significant events
    - _Requirements: 6.2, 6.3, 8.2_

  - [ ] 11.3 Implement `compare_scenarios`
    - Merge results from multiple runs into comparison DataFrame
    - Columns: year, end_use, scenario_name, total_therms, use_per_customer
    - _Requirements: 6.2, 9.4_

  - [ ]* 11.4 Property test: scenario determinism
    - **Property 13: Same config twice → identical results**
    - Table: side-by-side comparison of two runs
    - Report: max absolute difference (should be 0)
    - Output: `output/scenarios/property13_results.html` and `.md`
    - **Validates: Requirements 6.2, 6.3**

  - [ ]* 11.5 Property test: scenario validation
    - **Property 14: validate_scenario warns for rates outside [0,1] and horizon <= 0**
    - Table: test cases with expected vs actual results
    - Output: `output/scenarios/property14_results.html` and `.md`
    - **Validates: Requirements 6.4**

- [ ] 12. Implement CLI entry point

  - [ ] 12.1 Create `src/main.py` as CLI entry point
    - Parse args: scenario config path, output dir, --baseline-only, --compare
    - Wire pipeline: config → ingest → stock → simulate → aggregate → export
    - Print summary statistics to stdout
    - _Requirements: 8.2, 9.1, 9.2_

  - [ ] 12.2 Create default scenario configs
    - Create `scenarios/baseline.json` with reference case parameters
    - Create `scenarios/high_electrification.json` for demonstration
    - Document parameters with inline comments
    - _Requirements: 6.1, 8.1_

  - [ ]* 12.3 Property test: full pipeline integration
    - **Test: load → stock → simulate → aggregate → export produces valid CSV**
    - Verify output has expected columns and non-empty rows
    - Report: row count, column list, sample values
    - Output: `output/integration/pipeline_test.html` and `.md`
    - **Validates: Requirements 5.1, 9.1, 10.2**

- [ ] 13. Implement validation and limitation reporting

  - [ ] 13.1 Billing-based calibration
    - Load billing data and build historical rate table
    - Convert billing dollars to therms
    - Compare simulated vs billing-derived therms per premise
    - Compute MAE, mean bias, R²
    - Flag premises with divergence > threshold
    - _Requirements: 7.1, 10.2, 10.3_

  - [ ] 13.2 Range-checking and IRP comparison
    - Flag results outside expected ranges
    - Compare model UPC vs IRP 10-year forecast
    - Compare vintage-cohort UPC vs era anchors (820/720/650)
    - Log and report discrepancies
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

  - [ ] 13.3 Documentation and limitation metadata
    - Include metadata with each export: scenario name, run date, parameters
    - Document data gaps encountered during ingestion
    - State outputs are for illustrative/academic purposes
    - _Requirements: 8.1, 8.2, 8.4, 10.4_

- [ ] 14. Final checkpoint — Full integration verification
  - All outputs saved to `output/checkpoint_final/` as HTML + MD

  - [ ] 14.1 End-to-end run on actual data
    - Run baseline scenario on full NW Natural dataset
    - Report: total demand, UPC, demand by end-use/segment/district
    - Output: `output/checkpoint_final/baseline_results.html` and `.md`
    - _Requirements: 10.1, 10.2_

  - [ ] 14.2 Multi-scenario comparison
    - Run baseline + high electrification scenarios
    - Line graph: UPC trajectories (2025-2035)
    - Stacked bar: end-use composition under each scenario
    - Output: `output/checkpoint_final/scenario_comparison.html` and `.md`
    - _Requirements: 6.2, 9.4_

  - [ ] 14.3 Final validation dashboard
    - Traffic-light summary of all property tests (pass/fail)
    - Summary of all checkpoint results
    - List of known limitations and data gaps
    - Output: `output/checkpoint_final/final_dashboard.html` and `.md`
    - _Requirements: 10.1, 10.4_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP delivery
- Each sub-task has a maximum of 6 bullet items
- Every property test outputs results to `output/` as both HTML and Markdown (.md)
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation against actual data
- All code uses Python with pandas, dataclasses, and standard library logging
