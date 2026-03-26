# Implementation Plan: NW Natural End-Use Forecasting Model

## Overview

Build a bottom-up residential end-use demand forecasting model in Python. The implementation follows the pipeline architecture: data ingestion → housing stock model → end-use simulation → aggregation/output. Each task builds incrementally, wiring modules together as they are completed. All code lives under `src/` with CSV data read from `Data/`.

## Tasks

- [x] 1. Set up project structure and configuration module
  - [x] 1.1 Create `src/` directory and `src/config.py` with all static configuration
    - Define `END_USE_MAP` dictionary mapping equipment_type_code to end-use categories
    - Define `DEFAULT_EFFICIENCY` dictionary by end-use category
    - Define `USEFUL_LIFE` dictionary by end-use category
    - Define `DISTRICT_WEATHER_MAP` dictionary mapping district codes to weather station SiteIds
    - Define file path constants pointing to `Data/NWNatural Data/` for NW Natural-supplied files (`premise_data_blinded.csv`, `equipment_data_blinded.csv`, `equipment_codes.csv`, `segment_data_blinded.csv`, `billing_data_blinded.csv`, `small_billing_data_blinded.csv`, `DailyCalDay1985_Mar2025.csv`, `DailyGasDay2008_Mar2025.csv`, `BullRunWaterTemperature.csv`, `Portland_snow.csv`)
    - Define file path constants pointing to `Data/` for team-created tariff CSVs (`or_rate_case_history.csv`, `or_rates_oct_2025.csv`, `or_wacog_history.csv`, `wa_rate_case_history.csv`, `wa_rates_nov_2025.csv`, `wa_wacog_history.csv`)
    - Define file path constants for RBSA 2022 dataset in `Data/2022 RBSA Datasets/` (key files: `SiteDetail.csv`, `Mechanical_HeatingAndCooling.csv`, `Mechanical_WaterHeater.csv`, `Appliance_Stove_Oven.csv`, `Appliance_Laundry.csv`, `Building_Shell_One_Line.csv`)
    - Define file path constants for ASHRAE data in `Data/ashrae/` (`OR-ASHRAE_Service_Life_Data.xls`, `WA-ASHRAE_Service_Life_Data.xls`, `OR-ASHRAE_Maintenance_Cost_Data.xls`, `WA-ASHRAE_Maintenance_Cost_Data.xls`)
    - Define file path constant for NW Natural IRP load decay forecast: `Data/10-Year Load Decay Forecast (2025-2035).csv`
    - Define file path constants for load decay companion files: `Data/prior load decay data description.txt`, `Data/prior load decay data reconstructed.txt`, `Data/prior load decay data simulated.txt`
    - Define file path constants for baseload consumption factors: `Data/Baseload Consumption Factors.csv`, `Data/Baseload Consumption factors.py`, `Data/Baseload Consumption factors explanation.txt`
    - Define file path constants for NW energy proxies: `Data/nw_energy_proxies.csv`, `Data/nw_energy_proxies.py`, `Data/nw_energy_proxies explanation.txt`
    - Define file path constants for IRP context and equipment life docs: `Data/Integrated Resource Plan (IRP),.txt`, `Data/equipment life math.txt`
    - Define `GBR_API_BASE_URL` and `GBR_API_KEY_ENV_VAR` constants for Green Building Registry API
    - Define file path constants for RBSA metering data: `RBSAM_Y1_DIR` (`Data/rbsam_y1`), `RBSAM_Y2_DIR` (`Data/rbsam_y2`), `RBSAM_DATA_DICT` (`Data/rbsa-metering-data-dictionary-2016-2017.xlsx`)
    - Define file path constants for 2017 RBSA-II: `RBSA_2017_DIR` (`Data/2017-RBSA-II-Combined-Database`), `RBSA_2017_USER_MANUAL` (`Data/2017-RBSA-II-Database-User-Manual.pdf`)
    - Define Census API constants: `CENSUS_API_BASE`, `CENSUS_ACS1_TEMPLATE`, `CENSUS_ACS5_TEMPLATE`, `CENSUS_B25034_GROUP`, `NWN_SERVICE_TERRITORY_CSV` (`Data/NW Natural Service Territory Census data.csv`), `B25034_BACKUP_DIR` (`Data/B25034-5y`), `B25034_COUNTY_DIR` (`Data/B25034-5y-county`), `B25040_COUNTY_DIR` (`Data/B25040-5y-county`), `B25024_COUNTY_DIR` (`Data/B25024-5y-county`), `PSU_FORECAST_URL`, `PSU_PROJECTION_DIR` (`Data/PSU projection data`)
    - Define `OFM_HOUSING_XLSX` (`Data/ofm_april1_housing.xlsx`) for WA OFM postcensal housing estimates
    - Define `NOAA_NORMALS_DIR` (`Data/noaa_normals`), `NOAA_CDO_API_BASE`, `NOAA_CDO_TOKEN_ENV_VAR`, and `ICAO_TO_GHCND` mapping dictionary for NOAA Climate Normals (11 stations: KPDX, KEUG, KSLE, KAST, KDLS, KOTH, KONP, KCVO, KHIO, KTTD, KVUO)
    - Define `RECS_DIR` (`Data/Residential Energy Consumption Servey`), `RECS_2020_CSV`, `RECS_2015_CSV`, `RECS_2009_CSV`, `RECS_2005_CSV`, `RECS_PACIFIC_DIVISION` (9), `RECS_FUELHEAT_GAS` (1) for EIA RECS microdata
    - Define `BASE_YEAR`, `DEFAULT_BASE_TEMP`, `DEFAULT_HOT_WATER_TEMP` constants
    - _Requirements: 1.1, 1.4, 3.2, 4.2_

  - [x] 1.2 Write property test for config completeness
    - **Property 1: All equipment_type_codes in END_USE_MAP resolve to a valid end-use category string**
    - **Validates: Requirements 1.1, 1.4**

- [ ] 2. Implement data ingestion module
  - [x] 2.1 Create `src/data_ingestion.py` with CSV loading functions
    - Implement `load_premise_data(path)` — load and filter to active residential premises (custtype='R', status_code='AC')
    - Implement `load_equipment_data(path)` — load equipment inventory CSV
    - Implement `load_segment_data(path)` — load and filter segment data to residential customers
    - Implement `load_equipment_codes(path)` — load equipment code lookup table
    - Implement `load_weather_data(path)` — load daily weather CSV, parse dates
    - Implement `load_water_temperature(path)` — load Bull Run water temperature CSV, parse dates
    - Implement `load_snow_data(path)` — load Portland daily snow data (1985-2025) with Year, Month, Day, Date, snow (inches), snwd (snow depth). Used for peak day identification and weather severity flagging
    - Implement `load_billing_data(path)` — load billing_data_blinded.csv (or small_billing_data_blinded.csv for dev), parse `utility_usage` from dollar strings to float, parse `GL_revenue_date` to year/month
    - Implement `load_or_rates(path)` — load or_rates_oct_2025.csv (Schedule, Type, Description, Rate/Value, Unit). OR Schedule 2 residential = $1.41220/therm
    - Implement `load_wa_rates(path)` — load wa_rates_nov_2025.csv (Schedule, Type, Description, Value). WA Schedule 2 residential = $1.24164/therm
    - Implement `load_wacog_history(path)` — load or_wacog_history.csv and wa_wacog_history.csv (Effective Date, Rate per Therm, Type). Annual and Winter WACOG rates 2018–2025
    - Implement `load_rate_case_history(path)` — load or_rate_case_history.csv and wa_rate_case_history.csv (Date Applied, Date Effective, Granted Percent, etc.)
    - Implement `build_historical_rate_table(rate_cases, wacog, current_rates, state)` — reconstruct historical $/therm by working backward from current rates using rate case granted percentages and WACOG history
    - Implement `convert_billing_to_therms(billing, rate_table)` — join billing with historical rate table by rate_schedule, state, and date; compute estimated_therms = utility_usage / rate_per_therm
    - Implement `load_rbsa_site_detail(path)` — load `Data/2022 RBSA Datasets/SiteDetail.csv`, filter to NWN service territory (`NWN_SF_StrataVar = 'NWN'` or `Gas_Utility = 'NW NATURAL GAS'`). Key fields: Conditioned_Area, Home_Vintage, Qty_Bedrooms, Heating_Zone, Building_Type, Site_Case_Weight
    - Implement `load_rbsa_hvac(path)` — load `Mechanical_HeatingAndCooling.csv`. Key fields: System_Type, Fuel, COP_or_AFUE, Year_of_Manufacture, Heating_Size_BTUh
    - Implement `load_rbsa_water_heater(path)` — load `Mechanical_WaterHeater.csv`. Key fields: Fuel_Type, Water_Heater_Efficiency, Technology_Description, Size, Year_Manufactured
    - Implement `build_rbsa_distributions(site_detail, hvac, water_heater)` — compute weighted distributions of building characteristics (sqft, efficiency, vintage) by building type and vintage bin, using Site_Case_Weight for population-level estimates
    - Implement `load_ashrae_service_life(or_path, wa_path)` — load ASHRAE service life XLS files for OR and WA, map equipment categories to model end-use categories, return DataFrame with equipment_category, median_service_life, state
    - Implement `load_ashrae_maintenance_cost(or_path, wa_path)` — load ASHRAE maintenance cost XLS files for OR and WA, return DataFrame with equipment_category, annual_maintenance_cost, state
    - Implement `build_useful_life_table(ashrae_service_life)` — build state-specific useful life lookup dict from ASHRAE data, falling back to config.USEFUL_LIFE defaults for unmapped categories
    - Implement `load_load_decay_forecast(path)` — load NW Natural 2025 IRP 10-Year Load Decay Forecast (2025-2035) CSV. Contains UPC projections from top-down econometric model, used as validation/comparison target
    - Implement `load_historical_upc(path)` — load prior load decay data (reconstructed and simulated txt files). Provides historical UPC by year back to 2005 and era-based calibration anchors: pre-2010 (~820 therms), 2011-2019 (~720 therms), 2020+ (~650 therms)
    - Implement `load_baseload_factors(path)` — load Baseload Consumption Factors.csv with Category/SubCategory/Parameter/Value/Unit/Source columns. Covers cooking (30 therms), drying (20 therms), fireplace (55 therms), pilot loads, WH standby losses by vintage, adjustment multipliers
    - Implement `calculate_site_baseload(site_vintage, is_gorge, has_pipe_insulation, factors)` — calculate total non-weather-sensitive baseload per site using vintage-stratified standby losses, pilot loads (pre-2015), and adjustment multipliers (1.2x thermosiphon, 1.15x Gorge). Reference implementation in `Data/Baseload Consumption factors.py`
    - Implement `load_nw_energy_proxies(path)` — load nw_energy_proxies.csv compact parameter set with building envelope UA values by vintage era, Weibull parameters, and baseload factors
    - Implement `fetch_gbr_properties(zip_codes, api_key)` — query Green Building Registry API for properties by zip code. Returns Home Energy Score, estimated annual energy use, insulation levels, window types. Requires API key from environment variable
    - Implement `build_gbr_building_profiles(gbr_data)` — extract building shell and efficiency characteristics from GBR data to supplement RBSA distributions
    - Implement `load_rbsam_metering(directory, year)` — load RBSA sub-metered end-use data from tab-delimited TXT files (~300MB each). Parses SAS datetime timestamps. Returns long-format DataFrame with siteid, timestamp, end_use, kwh. Use chunked reading for memory efficiency
    - Implement `load_rbsa_2017_site_detail(path)` — load 2017 RBSA-II SiteDetail.csv for temporal comparison with 2022 RBSA building characteristics
    - Implement `load_service_territory_fips(path)` — load NW Natural Service Territory Census data.csv, return list of state/county/FIPS for the 16 service territory counties
    - Implement `fetch_census_b25034(fips_codes, year, acs_type)` — fetch Census ACS B25034 (Year Structure Built) via Census API using ucgid predicate for county-level data. acs_type='acs5' for all counties, 'acs1' for large counties only. No API key required
    - Implement `build_vintage_distribution(b25034_data)` — convert B25034 counts to percentage distributions by county and decade, map to model vintage eras
    - Implement `load_b25034_county_files(directory)` — load all downloaded ACS 5-year B25034 county CSVs from `Data/B25034-5y-county/` (2009-2023, 16 counties each). Offline fallback and historical time-series analysis
    - Implement `load_b25040_county_files(directory)` — load ACS 5-year B25040 (House Heating Fuel) county CSVs from `Data/B25040-5y-county/`. Key metric: utility gas share per county per year for calibrating gas equipment penetration and tracking electrification trends
    - Implement `load_b25024_county_files(directory)` — load ACS 5-year B25024 (Units in Structure) county CSVs from `Data/B25024-5y-county/`. Validates SF/MF segment split against NW Natural segment data
    - Implement `load_psu_population_forecasts(directory)` — load PSU Population Research Center county population forecasts from `Data/PSU projection data/`. Handle three CSV formats: 2025 files (YEAR, POPULATION, TYPE), 2024 files (YEAR, POPULATION), and 2023 Coos (wide format with areas as rows, years as columns — extract county total row). Parse comma-formatted population to int. Returns combined DataFrame with county, year, population, forecast_year, and derived annual growth rate. Covers all 13 NWN Oregon counties
    - Implement `load_ofm_housing(path)` — load WA OFM postcensal housing unit estimates from `Data/ofm_april1_housing.xlsx`. Read 'Housing Units' sheet, filter to county-total rows (Filter=1) for Clark, Skamania, Klickitat. Unpivot years 2020-2025 from wide to long format. Returns DataFrame with county, year, total_units, one_unit, two_or_more, mobile_home
    - Implement `load_noaa_daily_normals(directory, station)` — load NOAA 30-year daily climate normals from `Data/noaa_normals/{station}_daily_normals.csv`. Replace -7777 sentinel values with NaN. Returns DataFrame with date, tavg_normal, tmax_normal, tmin_normal, hdd_normal, cdd_normal
    - Implement `load_noaa_monthly_normals(directory, station)` — load NOAA monthly climate normals from `Data/noaa_normals/{station}_monthly_normals.csv`
    - Implement `compute_weather_adjustment(actual_hdd, normal_hdd)` — compute weather adjustment factor (actual/normal HDD ratio) for normalizing space heating demand. Returns 1.0 if normal_hdd is zero
    - Implement `load_recs_microdata(path, year)` — load EIA RECS public-use microdata CSV for a given survey year (2005-2020). Handle column name differences across years. Standardize key columns to common names: division, fuelheat, typehuq, yearmaderange, totsqft, btung, btungsph, btungwth, nweight
    - Implement `build_recs_enduse_benchmarks(recs_data, division=9, fuelheat=1)` — compute weighted-average gas consumption by end use for gas-heated homes in Pacific division using NWEIGHT. Returns DataFrame with end_use, avg_therms, weighted_count, share_of_total. Used as independent validation of model end-use disaggregation
    - Log warnings for missing or malformed rows
    - _Requirements: 2.2, 2.4, 3.1, 3.2, 7.1, 7.2, 7.3, 7.4, 8.3_

  - [x] 2.2 Implement `build_premise_equipment_table` join function
    - Join premise, equipment, segment, and equipment_codes DataFrames on `blinded_id` and `equipment_type_code`
    - Derive `end_use` column using `END_USE_MAP` from config
    - Derive `efficiency` column using `DEFAULT_EFFICIENCY` where not available
    - Derive `weather_station` column using `DISTRICT_WEATHER_MAP`
    - Document assumptions for missing data as log warnings
    - _Requirements: 1.4, 2.1, 3.1, 7.4, 8.1_

  - [x] 2.3 Write property tests for data ingestion
    - **Property 2: Filtering preserves only active residential premises — output contains only custtype='R' and status_code='AC'**
    - **Validates: Requirements 1.2, 7.1**

  - [x] 2.4 Write property test for join integrity
    - **Property 3: Every row in premise_equipment_table has a non-null end_use category and a valid efficiency > 0**
    - **Validates: Requirements 1.4, 3.1**

- [x] 3. Checkpoint — Verify data ingestion
  - Ensure all tests pass, ask the user if questions arise.
  - Verify that `build_premise_equipment_table` produces a valid DataFrame from the actual CSV files in `Data/`.

- [ ] 4. Implement housing stock module
  - [x] 4.1 Create `src/housing_stock.py` with `HousingStock` dataclass and baseline builder
    - Define `HousingStock` dataclass with fields: year, premises DataFrame, total_units, units_by_segment, units_by_district
    - Implement `build_baseline_stock(premise_equipment, base_year)` — construct baseline stock from premise-equipment data
    - Compute `total_units`, `units_by_segment`, `units_by_district` from unique blinded_ids
    - _Requirements: 2.1, 2.2, 5.4_

  - [x] 4.2 Implement `project_stock` for future year projection
    - Apply housing growth rate from scenario config to project total units
    - Simulate new construction additions proportional to existing segment distribution
    - _Requirements: 2.3, 6.1_

  - [x] 4.3 Write property test for housing stock projection with visualizations
    - **Property 4: Projected total_units equals baseline total_units × (1 + growth_rate)^(target_year - base_year), within rounding tolerance**
    - **Validates: Requirements 2.3, 6.3**
    - Generate comparison graphs:
      - Line graph: Baseline vs projected total units over time
      - Bar chart: Segment distribution comparison (baseline vs projected)
      - Bar chart: District distribution comparison (baseline vs projected)
    - Generate growth rate analysis graph:
      - Line graph showing projected vs expected growth rates by year
    - Generate service territory map:
      - Choropleth map of NW Natural service territory by county
      - Color-coded by projected housing growth rate (low/medium/high)
      - Include district boundaries and weather station locations
    - All visualizations saved to `output/housing_stock_projections/` directory
    - Test verifies graphs are created, files exist, and contain expected data

- [x] 5. Implement equipment module
  - [x] 5.1 Create `src/equipment.py` with `EquipmentProfile` dataclass and inventory builder
    - Define `EquipmentProfile` dataclass with fields: equipment_type_code, end_use, efficiency, install_year, useful_life, fuel_type
    - Define `WEIBULL_BETA` dictionary with default shape parameters by end-use category (space_heating/water_heating: 3.0, appliances: 2.5)
    - Implement `weibull_survival(t, eta, beta)` — compute S(t) = exp(-(t/eta)^beta)
    - Implement `median_to_eta(median_life, beta)` — convert ASHRAE median service life to Weibull scale parameter: eta = median_life / (ln(2))^(1/beta)
    - Implement `replacement_probability(age, eta, beta)` — compute conditional failure probability: P = 1 - S(t)/S(t-1)
    - Implement `build_equipment_inventory(premise_equipment)` — derive efficiency, install_year, useful_life, fuel_type from data and config defaults; use ASHRAE service life for eta derivation
    - _Requirements: 3.1, 3.2_

  - [x] 5.2 Implement `apply_replacements` for equipment transitions
    - For each equipment unit, compute replacement probability using Weibull survival model based on age and end-use-specific eta/beta parameters
    - Use probabilistic replacement (compare replacement_probability against a threshold or random draw) rather than deterministic age cutoff
    - Replace selected units with new equipment based on scenario technology adoption rates
    - Apply electrification switching rates (gas → electric/heat pump) from scenario config
    - Apply efficiency improvements from scenario config
    - _Requirements: 3.3, 3.4, 6.1_

  - [x] 5.3 Write property test for equipment replacement logic with visualizations
    - **Property 5: Weibull survival function is monotonically decreasing — S(t) <= S(t-1) for all t > 0, and S(0) = 1.0**
    - **Property 5b: replacement_probability is always in [0, 1] for valid inputs**
    - **Validates: Requirements 3.3**
    - Generate comparison graphs:
      - Line graph: Weibull survival curves by end-use category (space_heating, water_heating, appliances)
      - Line graph: Replacement probability by equipment age for each end-use category
      - Scatter plot: Equipment age distribution in baseline stock (histogram with overlay of replacement probability curve)
      - Line graph: Cumulative replacement rate over equipment lifetime by end-use category
    - Generate equipment transition visualizations:
      - Stacked bar chart: Equipment fuel type distribution before and after replacements (gas vs electric)
      - Stacked bar chart: Equipment efficiency distribution before and after replacements (by efficiency tier)
      - Sankey diagram: Equipment transitions showing gas→electric, old→new efficiency paths
    - All visualizations saved to `output/equipment_replacement/` directory
    - Test verifies graphs are created, files exist, and contain expected data

  - [x] 5.4 Write property test for fuel switching conservation with visualizations
    - **Property 6: Total equipment count before and after apply_replacements is equal (replacements don't create or destroy units)**
    - **Validates: Requirements 3.3, 3.4**
    - Generate conservation verification graphs:
      - Line graph: Total equipment count before and after replacements by year (verify conservation)
      - Pie chart: Equipment count by fuel type before and after replacements (gas vs electric split)
      - Stacked area chart: Equipment count by end-use category over time (before and after)
      - Bar chart: Fuel switching volume by end-use category (gas units converted to electric)
    - Generate geographic visualizations:
      - Choropleth map: Electrification rate by district (% of gas equipment converted to electric)
      - Choropleth map: Equipment replacement rate by district (% of equipment replaced)
      - Scatter plot: District-level equipment count before vs after replacements (verify 1:1 line)
    - Generate detailed transition analysis:
      - Waterfall chart: Equipment count changes by transition type (gas→electric, efficiency upgrade, no change)
      - Heatmap: Fuel switching rates by end-use category and efficiency tier
      - Box plot: Equipment age distribution before and after replacements (by end-use)
    - All visualizations saved to `output/fuel_switching_conservation/` directory
    - Test verifies graphs are created, files exist, and contain expected data

- [x] 6. Implement weather processing module
  - [x] 6.1 Create `src/weather.py` with HDD/CDD computation and station mapping
    - Implement `compute_hdd(daily_temps, base_temp=65.0)` — HDD = max(0, base_temp - daily_avg)
    - Implement `compute_cdd(daily_temps, base_temp=65.0)` — CDD = max(0, daily_avg - base_temp)
    - Implement `compute_annual_hdd(weather_df, site_id, year)` — sum daily HDD for a station/year
    - Implement `compute_water_heating_delta(water_temp_df, target_temp=120.0, year=None)` — average annual (target - cold water temp)
    - Implement `assign_weather_station(district_code)` — lookup from DISTRICT_WEATHER_MAP
    - _Requirements: 4.1, 7.2_

  - [x] 6.2 Write property test for HDD computation with visualizations
    - **Property 7: HDD values are always non-negative, and HDD + CDD + abs(daily_avg - base_temp) relationship holds: for any temperature, exactly one of HDD or CDD is positive (or both zero when temp equals base)**
    - **Validates: Requirements 4.1, 4.2**
    - Generate weather station visualizations:
      - OpenStreetMap-based map showing all 11 weather stations classified by source (NW Natural, NOAA, proxy)
      - Color-coded markers: NW Natural stations (blue), NOAA stations (green), proxy stations (orange)
      - Include station names, ICAO codes, and GHCND IDs in popup tooltips
      - Show service territory boundaries and district assignments
    - Generate HDD/CDD analysis graphs:
      - Line graph: Daily HDD and CDD by day of year for a representative station (KPDX)
      - Stacked area chart: Cumulative HDD and CDD over the year
      - Heatmap: Monthly average HDD by station (rows=stations, columns=months)
      - Heatmap: Monthly average CDD by station (rows=stations, columns=months)
      - Box plot: Annual HDD distribution across all 11 stations (2015-2025)
      - Box plot: Annual CDD distribution across all 11 stations (2015-2025)
    - Generate water temperature analysis graphs:
      - Line graph: Daily Bull Run water temperature by day of year (2008-2025 overlay)
      - Seasonal pattern: Average monthly water temperature with min/max bands
      - Scatter plot: Water temperature vs. air temperature (KPDX) with regression line
    - Generate animated moving map display:
      - Interactive animated map showing HDD/CDD progression throughout the year
      - Monthly snapshots with color-coded weather stations (intensity = HDD/CDD magnitude)
      - Play/pause controls to animate through 12 months
      - Slider to jump to specific month
      - Legend showing HDD/CDD scale and color mapping
      - Station markers update color intensity as HDD/CDD changes by month
      - Popup shows current month's HDD/CDD value for each station
    - All visualizations saved to `output/weather_analysis/` directory
    - Test verifies graphs are created, files exist, and contain expected data

  - [x] 6.3 Write property test for water heating delta with visualizations
    - **Property 8: Water heating delta_t is always positive when cold water temp < target_temp, and equals target_temp - avg_cold_water_temp**
    - **Validates: Requirements 4.1, 4.2**
    - Generate water heating demand analysis graphs:
      - Line graph: Daily water heating delta-T by day of year (2008-2025 overlay with average)
      - Seasonal pattern: Average monthly delta-T with min/max confidence bands
      - Scatter plot: Water temperature vs. air temperature (KPDX) with regression line and R² value
      - Heatmap: Monthly average delta-T by weather station (rows=stations, columns=months)
      - Box plot: Annual delta-T distribution across all 11 stations (2015-2025)
      - Violin plot: Distribution of daily delta-T values by month (seasonal variation)
    - Generate water heating demand maps with OpenStreetMap background:
      - Choropleth map: Average annual water heating delta-T by district (color intensity = delta-T magnitude)
      - Choropleth map: Seasonal variation in delta-T by district (winter vs. summer comparison)
      - Marker map: Weather stations color-coded by average delta-T (blue=low, red=high)
      - Heatmap overlay: District-level water heating demand intensity
      - Animated moving map: Monthly delta-T progression throughout the year
        * Interactive layer control to select month (January-December)
        * Color-coded markers showing delta-T intensity by month
        * Marker colors change from blue (low) to red (high) based on delta-T value
        * Opacity indicates delta-T magnitude
        * Popup shows station name, ICAO code, current month, delta-T value, and WH demand estimate
        * Title and legend display delta-T scale and color mapping
        * OpenStreetMap background with zoom and pan controls
    - Generate water heating energy demand graphs:
      - Line graph: Estimated annual water heating therms per customer by station (assuming 64 gal/day usage)
      - Bar chart: Comparison of water heating demand across all 11 stations
      - Stacked bar chart: Water heating demand by district (baseline vs. high-efficiency scenario)
      - Time series: Monthly water heating demand pattern (showing seasonal peaks)
    - All visualizations saved to `output/water_heating_analysis/` directory
    - Test verifies graphs are created, files exist, and contain expected data

- [ ] 7. Checkpoint — Verify core model components
  - Ensure all tests pass, ask the user if questions arise.
  - Verify housing stock, equipment, and weather modules work with actual data from `Data/`.

- [ ] 8. Implement end-use energy simulation module
  - [ ] 8.1 Create `src/simulation.py` with per-end-use simulation functions
    - Implement `simulate_space_heating(equipment, annual_hdd, heating_factor)` — therms = (HDD × heating_factor × qty) / efficiency per premise
    - Implement `simulate_water_heating(equipment, delta_t, gallons_per_day=64.0)` — therms based on energy to heat water volume through delta_t, adjusted by efficiency
    - Implement `simulate_baseload(equipment, annual_consumption)` — flat annual therms per unit by end use (cooking, drying, fireplace, other), adjusted by efficiency
    - _Requirements: 4.1, 4.2, 4.4_

  - [ ] 8.2 Implement `simulate_all_end_uses` orchestrator function
    - For each premise, dispatch to appropriate simulation function based on end_use category
    - Collect weather data (annual HDD, water temp delta) per premise's assigned weather station
    - Return DataFrame with columns: blinded_id, end_use, annual_therms, equipment_type_code, efficiency, year, scenario_name
    - Maintain separation between end uses to prevent double-counting
    - _Requirements: 1.4, 4.2, 4.3, 4.4, 5.4_

  - [ ] 8.3 Write property test for simulation non-negativity with visualizations
    - **Property 9: All simulated annual_therms values are non-negative**
    - **Validates: Requirements 4.2**
    - Generate end-use consumption analysis graphs:
      - Histogram: Distribution of annual therms by end-use category (showing non-negativity)
      - Box plot: Annual therms by end-use category (median, quartiles, outliers)
      - Violin plot: Distribution of annual therms by end-use and building type (SF vs MF)
      - Line graph: Cumulative distribution function (CDF) of annual therms by end-use
      - Stacked bar chart: Average annual therms by end-use category and vintage era
      - Scatter plot: Annual therms vs. conditioned area by end-use (with regression line)
    - Generate premise-level consumption analysis graphs:
      - Histogram: Distribution of total annual therms per premise (all end-uses combined)
      - Box plot: Total annual therms by customer segment (RESSF, RESMF, mobile home)
      - Box plot: Total annual therms by district (showing geographic variation)
      - Scatter plot: Total annual therms vs. conditioned area (with regression line)
      - Scatter plot: Total annual therms vs. equipment age (by end-use category)
    - Generate consumption validation graphs:
      - Line graph: Average annual therms per customer by end-use (baseline vs. scenario comparison)
      - Stacked area chart: End-use contribution to total demand over time (showing composition)
      - Waterfall chart: Breakdown of total demand by end-use category (showing contribution magnitude)
      - Heatmap: Average annual therms by end-use and vintage era (rows=end-uses, columns=eras)
    - Generate geographic consumption maps with OpenStreetMap background:
      - Choropleth map: Average annual therms per customer by district (color intensity = consumption)
      - Choropleth map: End-use composition by district (stacked color layers for each end-use)
      - Marker map: Premises color-coded by total annual therms (blue=low, red=high consumption)
      - Heatmap overlay: District-level consumption intensity with zoom/pan controls
      - Animated moving map: Monthly consumption progression throughout the year
        * Interactive layer control to select month (January-December)
        * Color-coded markers showing consumption intensity by month
        * Marker colors change from blue (low) to red (high) based on consumption value
        * Opacity indicates consumption magnitude
        * Popup shows district name, average therms, end-use breakdown, and consumption tier
        * Title and legend display consumption scale and color mapping
        * OpenStreetMap background with zoom and pan controls
    - Generate end-use comparison maps:
      - Multi-panel choropleth maps: One map per end-use category showing geographic distribution
      - Difference map: Comparison of space heating vs. water heating demand by district
      - Ratio map: Space heating as percentage of total demand by district
    - All visualizations saved to `output/simulation_non_negativity/` directory
    - Test verifies:
      - All annual_therms values are >= 0 (non-negativity property)
      - No NaN or infinite values in results
      - Graphs are created and files exist
      - Data in visualizations matches simulation results
      - Geographic maps display all districts with valid coordinates

  - [ ] 8.4 Write property test for efficiency impact with visualizations
    - **Property 10: For identical premises and weather, higher equipment efficiency produces lower or equal therms consumption**
    - **Validates: Requirements 4.2, 3.2**
    - Generate efficiency impact analysis graphs:
      - Line graph: Annual therms vs. equipment efficiency (by end-use category, showing monotonic decrease)
      - Scatter plot: Consumption reduction vs. efficiency improvement (% change in therms per % efficiency gain)
      - Box plot: Annual therms distribution by efficiency tier (low/medium/high) for each end-use
      - Stacked bar chart: Average annual therms by end-use and efficiency tier (showing efficiency benefit)
      - Line graph: Cumulative savings from efficiency improvements (baseline vs. high-efficiency scenario)
      - Heatmap: Annual therms by end-use and efficiency rating (rows=end-uses, columns=efficiency tiers)
    - Generate efficiency comparison graphs:
      - Waterfall chart: Consumption reduction breakdown by end-use (showing which end-uses benefit most)
      - Violin plot: Distribution of consumption by efficiency tier and building type (SF vs MF)
      - Scatter plot: Equipment age vs. efficiency rating (showing correlation with vintage)
      - Line graph: Average therms per customer by vintage era and efficiency tier
      - Bar chart: Efficiency improvement potential by end-use category (max savings possible)
    - Generate efficiency scenario comparison graphs:
      - Line graph: Total annual demand under baseline vs. high-efficiency scenario (by year)
      - Stacked area chart: Demand composition by efficiency tier over time (showing transition)
      - Comparison chart: Baseline vs. efficient equipment consumption by end-use (side-by-side bars)
      - Percentage change chart: Consumption reduction (%) by end-use when upgrading to high-efficiency
    - Generate geographic efficiency impact maps with OpenStreetMap background:
      - Choropleth map: Average equipment efficiency rating by district (color intensity = efficiency level)
      - Choropleth map: Potential therms savings by district (color intensity = savings magnitude)
      - Difference map: Consumption difference between low-efficiency and high-efficiency scenarios by district
      - Marker map: Districts color-coded by average efficiency improvement potential (blue=low, red=high)
      - Heatmap overlay: District-level efficiency distribution with zoom/pan controls
      - Animated moving map: Efficiency improvement progression by end-use category
        * Interactive layer control to select end-use (space heating, water heating, cooking, drying, etc.)
        * Color-coded markers showing efficiency level by district for selected end-use
        * Marker colors change from blue (low efficiency) to green (high efficiency)
        * Opacity indicates efficiency rating magnitude
        * Popup shows district name, current efficiency, potential efficiency, and estimated savings
        * Title and legend display efficiency scale and color mapping
        * OpenStreetMap background with zoom and pan controls
    - Generate efficiency distribution maps:
      - Multi-panel choropleth maps: One map per end-use category showing efficiency distribution
      - Efficiency gap map: Comparison of current vs. potential efficiency by district
      - Savings potential map: Estimated annual therms savings if all equipment upgraded to high-efficiency
    - All visualizations saved to `output/efficiency_impact/` directory
    - Test verifies:
      - Efficiency monotonicity: higher efficiency always produces lower or equal consumption
      - No negative efficiency values or consumption values
      - Efficiency improvements are consistent across identical premises
      - Graphs are created and files exist
      - Data in visualizations matches simulation results
      - Geographic maps display all districts with valid coordinates
      - Savings calculations are accurate and non-negative

- [ ] 9. Implement aggregation and output module
  - [ ] 9.1 Create `src/aggregation.py` with rollup and export functions
    - Implement `aggregate_by_end_use(simulation_results)` — group by end_use, sum annual_therms
    - Implement `aggregate_by_segment(simulation_results, segments)` — group by segment, sum annual_therms
    - Implement `aggregate_by_district(simulation_results, premises)` — group by district_code_IRP, sum annual_therms
    - Implement `compute_use_per_customer(total_demand, customer_count)` — UPC metric
    - Implement `compare_to_irp_forecast(model_upc, irp_forecast)` — compare bottom-up model UPC projections against NW Natural IRP load decay forecast; return year, model_upc, irp_upc, difference, pct_difference
    - Implement `export_results(results, output_path, format='csv')` — write aggregated results to CSV
    - Include metadata columns: year, scenario_name
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 9.1, 9.2, 9.3_

  - [ ]* 9.2 Write property test for aggregation conservation
    - **Property 11: Sum of aggregated demand across all end uses equals total demand from simulation results (no therms lost or created during aggregation)**
    - **Validates: Requirements 5.1, 5.4**

  - [ ]* 9.3 Write property test for use-per-customer
    - **Property 12: compute_use_per_customer(total, count) == total / count for count > 0, and handles count == 0 gracefully**
    - **Validates: Requirements 5.2**

- [ ] 10. Checkpoint — Verify simulation and aggregation pipeline
  - Ensure all tests pass, ask the user if questions arise.
  - Run a baseline simulation on actual data and verify aggregated outputs are reasonable.

- [ ] 11. Implement scenario management module
  - [ ] 11.1 Create `src/scenarios.py` with ScenarioConfig and validation
    - Define `ScenarioConfig` dataclass with fields: name, description, base_year, forecast_horizon, housing_growth_rate, electrification_rate (dict by end use), efficiency_improvement (dict by end use), weather_assumption
    - Implement `validate_scenario(config)` — check rates are in [0,1], forecast_horizon > 0, weather_assumption in allowed set, return list of warnings
    - _Requirements: 6.1, 6.4, 8.1_

  - [ ] 11.2 Implement `run_scenario` pipeline orchestrator
    - Load base data via data_ingestion
    - Build baseline housing stock
    - For each year in forecast horizon: project stock, apply equipment replacements, run simulation, aggregate results
    - Store per-year results with scenario_name label
    - Log significant events (data gaps, assumption applications)
    - _Requirements: 6.2, 6.3, 8.2, 8.3_

  - [ ] 11.3 Implement `compare_scenarios` for side-by-side analysis
    - Merge results from multiple scenario runs into a single comparison DataFrame
    - Include columns: year, end_use, scenario_name, total_therms, use_per_customer
    - _Requirements: 6.2, 9.4_

  - [ ]* 11.4 Write property test for scenario isolation
    - **Property 13: Running the same scenario config twice produces identical results (deterministic execution)**
    - **Validates: Requirements 6.2, 6.3**

  - [ ]* 11.5 Write property test for scenario validation
    - **Property 14: validate_scenario returns warnings for any rate outside [0, 1] and for forecast_horizon <= 0**
    - **Validates: Requirements 6.4**

- [ ] 12. Implement CLI entry point and pipeline wiring
  - [ ] 12.1 Create `src/main.py` as CLI entry point
    - Parse command-line arguments: scenario config file path, output directory, optional flags (--baseline-only, --compare)
    - Wire full pipeline: load config → ingest data → build stock → run simulation → aggregate → export
    - Implement baseline-only mode (single year, no projections)
    - Implement multi-scenario comparison mode
    - Print summary statistics to stdout
    - _Requirements: 8.2, 9.1, 9.2, 9.3, 9.4_

  - [ ] 12.2 Create default scenario configuration files
    - Create `scenarios/baseline.py` or `scenarios/baseline.json` with reference case parameters
    - Create at least one alternative scenario (e.g., high electrification) for demonstration
    - Document scenario parameters with inline comments
    - _Requirements: 6.1, 8.1_

  - [ ]* 12.3 Write integration test for full pipeline
    - Test end-to-end: load data → build stock → simulate → aggregate → export
    - Verify output CSV is produced with expected columns and non-empty rows
    - _Requirements: 5.1, 9.1, 10.2_

- [ ] 13. Implement validation and limitation reporting
  - [ ] 13.1 Add billing-based calibration and validation
    - Load billing data via `load_billing_data` and build historical rate table from tariff CSVs
    - Convert billing dollars to therms using `convert_billing_to_therms`
    - Compare simulated annual therms against billing-derived therms per premise
    - Compute calibration metrics: mean absolute error, mean bias, R² between simulated and billed therms
    - Flag premises where simulated vs. billed divergence exceeds a configurable threshold
    - _Requirements: 7.1, 10.2, 10.3_

  - [ ] 13.2 Add validation and range-checking utilities
    - In `simulation.py` or a new `validation.py`, add functions to flag results outside expected ranges
    - Compare bottom-up totals to any available historical aggregate data
    - Compare model UPC projections against NW Natural IRP 10-Year Load Decay Forecast (2025-2035) using `compare_to_irp_forecast`
    - Compare vintage-cohort UPC against era-based calibration anchors from load decay description (pre-2010 ~820, 2011-2019 ~720, 2020+ ~650 therms)
    - Log and report discrepancies with quantified differences
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

  - [ ] 13.3 Add documentation and limitation metadata to outputs
    - Include a metadata header or companion file with each export: scenario name, run date, key parameters, known limitations
    - Document data gaps encountered during ingestion
    - State that outputs are for illustrative/academic purposes
    - _Requirements: 8.1, 8.2, 8.4, 10.1, 10.4_

- [ ] 14. Final checkpoint — Full integration verification
  - Ensure all tests pass, ask the user if questions arise.
  - Run baseline scenario end-to-end on actual NW Natural data files.
  - Verify output CSVs are produced with demand by end use, segment, and district.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation against actual data
- Property tests validate universal correctness properties from the design
- All code uses Python with pandas, dataclasses, and standard library logging
- The `Data/` folder is organized by provenance: `Data/NWNatural Data/` contains NW Natural-supplied blinded/proprietary files; `Data/` root contains team-created tariff CSVs; `Data/2022 RBSA Datasets/` contains NEEA RBSA data; `Data/ashrae/` contains ASHRAE public database exports
- `Data/NWNatural Data/billing_data_blinded.csv` is the full billing dataset; `Data/NWNatural Data/small_billing_data_blinded.csv` is a smaller version for development and testing
- Tariff rate CSVs (`or_rate_case_history.csv`, `or_rates_oct_2025.csv`, `or_wacog_history.csv`, `wa_rate_case_history.csv`, `wa_rates_nov_2025.csv`, `wa_wacog_history.csv`) were manually extracted from the OR/WA rate PDF files in `Data/`
- `Data/2022 RBSA Datasets/` contains the 2022 NEEA Residential Building Stock Assessment with building characteristics, HVAC, water heater, and appliance data for the Pacific Northwest. Filter to NWN service territory sites for proxy distributions.
- `Data/ashrae/` contains ASHRAE public database exports (XLS format) with equipment service life and maintenance cost data for Oregon and Washington. Service life data replaces hardcoded useful life defaults; maintenance cost data supports economic analysis in scenario modeling.
- `Data/10-Year Load Decay Forecast (2025-2035).csv` contains NW Natural's 2025 IRP Use Per Customer (UPC) load decay forecast, serving as the primary validation target for comparing bottom-up model projections against the existing top-down econometric approach.
- `Data/prior load decay data description.txt` defines three eras of UPC decline with RBSA vintage mapping and historical decay rates (-1.15%/yr 2005-2015, -1.55%/yr 2015-2020, -1.19%/yr 2020-2025). `Data/prior load decay data reconstructed.txt` and `Data/prior load decay data simulated.txt` provide year-by-year historical UPC values back to 2005 for calibration.
- `Data/Baseload Consumption Factors.csv` contains DOE/RECS/RBSA/NEEA baseload parameters: cooking 30 therms, drying 20 therms, fireplace 55 therms, pilot loads (46-82 therms pre-2015), WH standby losses by vintage (75/55/40/20 therms), and adjustment multipliers (1.2x thermosiphon, 1.15x Gorge). `Data/Baseload Consumption factors.py` provides a reference implementation. `Data/Baseload Consumption factors explanation.txt` documents methodology.
- `Data/nw_energy_proxies.csv` provides a compact parameter set with building envelope UA values by vintage era (pre-1950 U=0.250, 1951-1980 U=0.081, 1981-2010 U=0.056, 2011+ U=0.038), DOE/NEMS Weibull parameters, and key baseload factors. `Data/nw_energy_proxies explanation.txt` documents the full methodology.
- `Data/Integrated Resource Plan (IRP),.txt` provides IRP UPC forecast context (-1.19% net decline, -0.40% gross, +0.39% customer growth). `Data/equipment life math.txt` documents DOE/NEMS Weibull parameters for equipment replacement modeling.
- Green Building Registry (GBR) API data is fetched at runtime via `fetch_gbr_properties()`. Requires `GBR_API_KEY` environment variable. Provides Home Energy Score and building characteristics to supplement RBSA data.
- `Data/rbsam_y1/` and `Data/rbsam_y2/` contain NEEA RBSA sub-metered 15-minute interval electric end-use data (~400 homes, ~300MB per TXT file). Year 1 covers Sep 2012 – Sep 2013; Year 2 covers Apr 2013 – Apr 2014. Although electric (not gas), this data validates baseload assumptions, provides diurnal/seasonal load shapes, and informs end-use disaggregation ratios. `Data/rbsa-metering-data-dictionary-2016-2017.xlsx` maps column names to end-use categories.
- `Data/2017-RBSA-II-Combined-Database/` contains the 2017 NEEA RBSA-II site-level survey data (43 CSVs) providing a temporal comparison point against the 2022 RBSA for tracking building stock evolution. `Data/2017-RBSA-II-Database-User-Manual.pdf` documents the survey methodology.
- Census ACS table B25034 (Year Structure Built) provides county-level housing unit counts by decade of construction. Fetched via Census API at runtime for the 16 NW Natural service territory counties (FIPS codes in `Data/NW Natural Service Territory Census data.csv`). ACS 5-year covers all counties; ACS 1-year only covers counties with 65,000+ population (~7-8 of 16). Used to validate housing stock vintage distribution and inform growth rate assumptions. `Data/B25034-5y/` contains downloaded national-level backup data (2010-2024). `Data/B25034-5y-county/` contains pre-downloaded ACS 5-year county-level data for all 16 service territory counties (2009-2023, 15 annual files). No API key required.
- Census ACS table B25040 (House Heating Fuel) in `Data/B25040-5y-county/` provides county-level housing unit counts by primary heating fuel (utility gas, electricity, propane, oil, wood, etc.) for 2009-2023. Tracks gas heating market share over time for calibrating equipment penetration rates and monitoring electrification trends.
- Census ACS table B25024 (Units in Structure) in `Data/B25024-5y-county/` provides county-level housing unit counts by structure type (1-unit detached, multi-family, mobile home, etc.) for 2009-2023. Validates the model's SF/MF segment split against independent Census data.
- PSU Population Research Center publishes official Oregon county-level population and housing unit forecasts (https://www.pdx.edu/population-research/past-forecasts). Covers all 13 Oregon NW Natural counties with projections to 2070+. Tables are xlsx files on Google Drive (manual download required). Most authoritative source for `housing_growth_rate` scenario parameter. Washington counties need separate sources.
- `Data/PSU projection data/2025/` contains downloaded PSU population forecasts for 6 NW Natural Oregon counties (Benton, Lane, Lincoln, Linn, Marion, Polk). CSV format: YEAR, POPULATION (comma-formatted), TYPE (Estimate/Forecast). Historical estimates 1990-2020 plus forecasts to 2075.
- `Data/PSU projection data/2024/` contains PSU population forecasts for 6 more NW Natural Oregon counties (Clackamas, Clatsop, Columbia, Multnomah, Washington, Yamhill). CSV format: YEAR, POPULATION (no TYPE column). Forecasts to 2074. Multnomah uses UGB-level format (different parsing needed).
- `Data/PSU projection data/2023/` contains PSU population forecast for Coos County. Wide CSV format: areas as rows, select years (2022-2072) as columns. Extract the "Coos County" row for county total. All 13 Oregon NW Natural counties are now covered across the three folders.
- `Data/ofm_april1_housing.xlsx` contains WA Office of Financial Management postcensal housing unit estimates (April 1, 2020-2025). Sheet "Housing Units" has 28 columns: Line, Filter, County, Jurisdiction, then 6 years × 4 metrics (Total, One Unit, Two or More, Mobile Homes). Filter=1 rows are county totals. Covers all WA counties; model uses Clark (line 41), Skamania (line 316), Klickitat (line 200) for the 3 WA NW Natural service territory counties. Fills the gap left by PSU forecasts (Oregon-only) for WA housing growth rates and structure-type validation.
- `Data/noaa_normals/` contains NOAA 30-year Climate Normals (1991-2020) for all 11 NW Natural weather stations, downloaded via the NOAA CDO API. Each station has daily normals (365 rows: date, avg/max/min temp, HDD, CDD) and monthly normals (12 rows). Stations: KPDX (Portland), KEUG (Eugene), KSLE (Salem), KAST (Astoria), KDLS (Dallesport/The Dalles), KOTH (North Bend/Coos Bay), KONP (Newport), KCVO (Corvallis), KHIO (Hillsboro), KTTD (Troutdale), KVUO (Vancouver WA). Used for weather-normalizing baseline simulations, computing weather adjustment factors (actual HDD / normal HDD), and providing a consistent reference for scenario projections. NOAA sentinel value -7777 means insufficient data (treat as missing/zero).
- `Data/Residential Energy Consumption Servey/` contains EIA Residential Energy Consumption Survey (RECS) microdata spanning 7 survey cycles (1993-2020). The model uses 2005-2020 CSV files; 1993-2001 are fixed-width reference only. Key survey: 2020 RECS (`recs2020_public_v7.csv`, 799 columns) has state-level geography (`STATE_FIPS`) enabling OR/WA filtering, plus NG end-use BTU columns (`BTUNGSPH`, `BTUNGWTH`, `BTUNGCOK`, `BTUNGCDR`, `BTUNGNEC`, `BTUNGOTH`). 2015 RECS (`recs2015_public_v4.csv`, 759 columns) has division-level geography only. 2009 and 2005 have progressively less end-use granularity. Filter to Pacific division (`DIVISION=9`) and gas-heated homes (`FUELHEAT=1`) for NW Natural comparison. RECS provides independent validation benchmarks for the model's end-use disaggregation ratios and per-customer consumption estimates. Note: folder name has a typo ("Servey" instead of "Survey") — use actual path as-is.


- [ ] 15. Implement visualization module with Mapbox integration
  - [ ] 15.1 Create `src/visualization.py` with geographic aggregation functions
    - Implement `aggregate_by_microclimate(simulation_results, premises, weather_stations)` — aggregate demand by weather station service area
    - Implement `aggregate_by_microresidential(simulation_results, premises)` — aggregate demand by segment + subsegment + vintage cohort
    - Implement `aggregate_by_microadoption(simulation_results, premises, equipment_inventory, scenario)` — aggregate demand by microclimate + microresidential + adoption cohort
    - Implement `compute_adoption_cohort(heat_pump_penetration)` — classify into Early Adopters (0-20%), Growth Phase (20-50%), Mature Phase (50-80%), Saturation (80%+)
    - Implement `compute_composite_score(demand_intensity, adoption_rate, efficiency_gap, climate_severity)` — multi-dimensional scoring (40% demand + 30% adoption + 20% efficiency + 10% climate)
    - Implement `compute_opportunity_score(demand_intensity, adoption_rate)` — high demand + low adoption = high opportunity
    - Implement `compute_success_score(adoption_rate, demand_intensity)` — high adoption + low demand = successful transition
    - _Requirements: 13.1, 13.2, 13.3_

  - [ ] 15.2 Implement GeoJSON generation functions
    - Implement `generate_microclimate_geojson(weather_stations, service_areas)` — create GeoJSON with weather station service areas (Voronoi or buffered circles)
    - Implement `generate_microresidential_geojson(microresidential_data, premise_locations)` — create GeoJSON with microresidential clusters (hexbins or custom polygons)
    - Implement `generate_microadoption_geojson(microadoption_data, microclimate_geojson, microresidential_geojson)` — create GeoJSON with microadoption areas
    - Implement `generate_composite_cell_geojson(composite_cell_data, cell_geometry='hexagon', cell_size_km=7.5)` — create GeoJSON with hexagonal cells combining all dimensions
    - Implement `generate_county_geojson(counties_data, county_boundaries_path)` — create GeoJSON with county boundaries
    - _Requirements: 13.1, 13.2, 13.3_

  - [ ] 15.3 Implement filtering and comparison functions
    - Implement `filter_composite_cells(composite_cell_data, microclimate=None, microresidential=None, adoption_cohort=None, demand_intensity=None, min_opportunity_score=None, min_success_score=None)` — filter cells by multiple attributes
    - Implement `export_visualization_data(results, output_dir)` — export aggregated results as JSON files for Mapbox visualization at all geographic levels
    - _Requirements: 13.1, 13.2_

  - [ ]* 15.4 Write property test for composite cell scoring
    - **Property 15: Composite score is always in [0, 100] for valid inputs**
    - **Property 15b: Opportunity score + Success score relationship: high opportunity cells have low success scores and vice versa**
    - **Validates: Requirements 13.1, 13.2**

- [ ] 16. Implement REST API module
  - [ ] 16.1 Create `src/api.py` with FastAPI application and scenario endpoints
    - Set up FastAPI app with OpenAPI documentation
    - Implement `POST /api/v1/scenarios` — create new scenario with validation
    - Implement `GET /api/v1/scenarios` — list scenarios with filtering and pagination
    - Implement `GET /api/v1/scenarios/{scenario_id}` — get scenario details
    - Implement `PUT /api/v1/scenarios/{scenario_id}` — update scenario (if not running)
    - Implement `DELETE /api/v1/scenarios/{scenario_id}` — delete scenario and results
    - Implement `POST /api/v1/scenarios/{scenario_id}/validate` — validate without running
    - Use Pydantic models for request/response validation
    - _Requirements: 11.1, 11.2, 11.3, 12.1_

  - [ ] 16.2 Implement execution endpoints
    - Implement `POST /api/v1/scenarios/{scenario_id}/run` — submit for execution (async or sync)
    - Implement `GET /api/v1/runs/{run_id}` — get execution status and progress
    - Implement `POST /api/v1/runs/{run_id}/cancel` — cancel running scenario
    - Support background task execution using Celery or APScheduler
    - Track execution progress (current step, overall progress, estimated time remaining)
    - _Requirements: 11.2, 12.1_

  - [ ] 16.3 Implement results retrieval endpoints
    - Implement `GET /api/v1/runs/{run_id}/results` — get aggregated results (JSON, CSV, Parquet)
    - Implement `GET /api/v1/runs/{run_id}/results/download` — download results as file
    - Implement `GET /api/v1/runs/{run_id}/results/timeseries` — get time-series for specific area
    - Implement `GET /api/v1/runs/{run_id}/results/comparison` — compare multiple areas
    - Implement `GET /api/v1/runs/{run_id}/results/geojson` — get GeoJSON for map visualization
    - Implement `GET /api/v1/runs/{run_id}/metadata` — get execution metadata and summary statistics
    - Support multiple aggregation levels: county, district, microclimate, microresidential, microadoption, composite-cell
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

  - [ ] 16.4 Implement comparison and configuration endpoints
    - Implement `POST /api/v1/comparisons` — create comparison of multiple scenarios
    - Implement `GET /api/v1/comparisons/{comparison_id}` — get comparison results
    - Implement `GET /api/v1/comparisons/{comparison_id}/download` — download comparison
    - Implement `GET /api/v1/config/defaults` — get default scenario parameters
    - Implement `GET /api/v1/config/parameters` — get all parameters and valid ranges
    - Implement `GET /api/v1/data/geographic-areas` — list available geographic areas
    - Implement `GET /api/v1/data/weather-stations` — get weather station information
    - _Requirements: 9.4, 11.3_

  - [ ] 16.5 Implement health and status endpoints
    - Implement `GET /api/v1/health` — health check endpoint
    - Implement `GET /api/v1/status` — system status and statistics
    - Include database connectivity, data loaded status, queue length
    - _Requirements: 12.1_

  - [ ] 16.6 Implement error handling and authentication
    - Standardize error responses with error codes and detailed messages
    - Implement optional JWT token authentication for production
    - Implement rate limiting (1000 req/hr authenticated, 100 req/hr unauthenticated)
    - Add request/response logging
    - _Requirements: 11.1, 12.1_

  - [ ]* 16.7 Write integration test for API endpoints
    - Test scenario creation, validation, execution, and results retrieval
    - Verify response formats and error handling
    - _Requirements: 11.1, 11.2, 12.1_

- [ ] 17. Implement web visualization frontend
  - [ ] 17.1 Create HTML/JavaScript visualization interface
    - Create `static/index.html` with Mapbox GL JS integration
    - Implement interactive county/district map with choropleth coloring
    - Implement drill-down navigation: county → district → microarea
    - Implement view toggle: microclimate, microresidential, microadoption, composite-cell
    - Implement time-series slider with play/pause controls
    - Implement scenario dropdown selector
    - Implement detail panel showing area metrics and charts
    - _Requirements: 13.1, 13.2, 13.3_

  - [ ] 17.2 Implement visualization controls and interactions
    - Implement year slider (2025-2035) with animation
    - Implement scenario selector dropdown
    - Implement view toggle buttons (county, district, microclimate, microresidential, microadoption, composite-cell)
    - Implement breadcrumb navigation showing current drill-down level
    - Implement multi-area comparison chart (line chart with multiple series)
    - Implement end-use breakdown stacked bar chart
    - Implement demand trend line chart
    - _Requirements: 13.1, 13.2, 13.3_

  - [ ] 17.3 Implement data loading and caching
    - Load GeoJSON from `/api/v1/runs/{run_id}/results/geojson` endpoint
    - Load time-series data from `/api/v1/runs/{run_id}/results/timeseries` endpoint
    - Implement client-side caching to reduce API calls
    - Implement error handling for failed API requests
    - _Requirements: 13.1, 13.2_

  - [ ]* 17.4 Write frontend tests
    - Test map rendering and interaction
    - Test data loading and caching
    - Test chart rendering
    - _Requirements: 13.1, 13.2_

- [ ] 18. Implement deployment and containerization
  - [ ] 18.1 Create Docker configuration
    - Create `Dockerfile` with Python 3.9+ base image
    - Install all dependencies from `requirements.txt`
    - Copy source code and data into container
    - Expose port 8000 for API server
    - Set entrypoint to start FastAPI server
    - _Requirements: 12.1, 12.2, 12.3_

  - [ ] 18.2 Create docker-compose configuration
    - Create `docker-compose.yml` with model service
    - Add optional PostgreSQL service for production data storage
    - Add optional Redis service for caching and task queue
    - Configure environment variables for scenario parameters and API settings
    - _Requirements: 12.1, 12.2, 12.3_

  - [ ] 18.3 Create requirements.txt and setup.py
    - List all Python dependencies with pinned versions
    - Include: pandas, numpy, fastapi, uvicorn, pydantic, sqlalchemy, celery, redis, shapely, geopandas, folium, requests, openpyxl, xlrd, pyarrow
    - Create `setup.py` for pip installation
    - _Requirements: 12.1, 12.2_

  - [ ] 18.4 Create deployment documentation
    - Create `DEPLOYMENT.md` with Docker setup instructions
    - Document environment variable configuration
    - Document data mounting for local development
    - Document cloud deployment options (AWS, Azure, GCP, Heroku)
    - Document health checks and monitoring
    - _Requirements: 12.1, 12.2, 12.3, 18.1_

  - [ ]* 18.5 Create cloud deployment templates
    - Create AWS CloudFormation template for ECS deployment
    - Create Azure Resource Manager template for App Service deployment
    - Create Kubernetes manifests for GKE deployment
    - _Requirements: 12.1, 12.2_

- [ ] 19. Implement monitoring and logging
  - [ ] 19.1 Add structured logging throughout codebase
    - Use Python logging module with JSON formatter
    - Log all significant events: data loading, simulation progress, aggregation, output generation
    - Include execution time tracking for each major step
    - _Requirements: 16.1, 16.2_

  - [ ] 19.2 Implement monitoring endpoints and metrics
    - Add Prometheus metrics for request count, latency, errors
    - Implement health check endpoint with database and data status
    - Add execution time metrics for scenario runs
    - _Requirements: 16.1, 16.2_

  - [ ] 19.3 Create monitoring dashboard
    - Create Grafana dashboard for system metrics
    - Display request rates, error rates, execution times
    - Display queue length and active runs
    - _Requirements: 16.1, 16.2_

- [ ] 20. Implement testing and quality assurance
  - [ ] 20.1 Create comprehensive test suite
    - Unit tests for all modules (data_ingestion, housing_stock, equipment, weather, simulation, aggregation, scenarios, visualization, api)
    - Integration tests for full pipeline
    - Property-based tests for correctness properties
    - Target 80%+ code coverage for critical paths
    - _Requirements: 17.1, 17.2_

  - [ ] 20.2 Set up CI/CD pipeline
    - Create GitHub Actions workflow for automated testing
    - Run tests on every commit
    - Run linting and type checking (pylint, mypy)
    - Build Docker image on successful tests
    - _Requirements: 17.1, 17.2_

  - [ ] 20.3 Create performance benchmarks
    - Benchmark single scenario execution time on laptop (target: <5 minutes)
    - Benchmark on server with 16GB RAM and 4 CPU cores (target: <2 minutes)
    - Benchmark API response times (target: <500ms for most endpoints)
    - _Requirements: 15.1, 15.2_

- [ ] 21. Create documentation and user guides
  - [ ] 21.1 Create README with quick-start instructions
    - Installation steps for local development
    - Running first scenario
    - Accessing visualization interface
    - _Requirements: 18.1, 18.2_

  - [ ] 21.2 Create API documentation
    - Document all endpoints with request/response examples
    - Create OpenAPI/Swagger documentation
    - Create SDK examples (Python, JavaScript)
    - _Requirements: 11.1, 11.2, 11.3_

  - [ ] 21.3 Create user guide
    - Explain scenario definition and parameters
    - Explain result interpretation
    - Provide common analysis workflows
    - Document geographic levels and cells (REGIONS_AND_CELLS.md)
    - _Requirements: 18.1, 18.2_

  - [ ] 21.4 Create operational documentation
    - Deployment guide (DEPLOYMENT.md)
    - Configuration guide
    - Troubleshooting guide
    - Monitoring and alerting setup
    - _Requirements: 12.1, 12.2, 12.3_

  - [ ] 21.5 Create example notebooks
    - Jupyter notebook demonstrating scenario creation and execution
    - Jupyter notebook demonstrating results analysis and visualization
    - Jupyter notebook demonstrating API usage
    - _Requirements: 18.1, 18.2_

- [ ] 22. Final integration and delivery
  - [ ] 22.1 End-to-end testing on actual data
    - Run all scenarios on full NW Natural dataset
    - Verify outputs are reasonable and match expectations
    - Verify visualization renders correctly
    - Verify API responds correctly
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

  - [ ] 22.2 Performance optimization
    - Profile code to identify bottlenecks
    - Optimize data loading and aggregation
    - Implement caching where appropriate
    - _Requirements: 15.1, 15.2_

  - [ ] 22.3 Final documentation review
    - Review all documentation for completeness and accuracy
    - Update REGIONS_AND_CELLS.md and API_DOCUMENTATION.md
    - Create final project summary
    - _Requirements: 18.1, 18.2, 18.3_

  - [ ] 22.4 Delivery and handoff
    - Package all code, documentation, and data
    - Create deployment guide for production
    - Provide training materials for stakeholders
    - _Requirements: 12.1, 12.2, 12.3, 18.1, 18.2_
