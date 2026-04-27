# Requirements Document: NW Natural End-Use Forecasting Model

## Introduction

This document defines requirements for a bottom-up residential end-use demand forecasting model for Northwest Natural's Integrated Resource Planning (IRP) process. The model complements existing top-down econometric models by disaggregating residential demand by end use, providing improved visibility into underlying demand drivers including end-use consumption patterns, equipment efficiency, technology adoption, and policy-driven electrification.

The model is a Python-based prototype built for academic capstone delivery. It is not intended for production deployment or regulatory filings.

## Glossary

- **NW Natural**: Northwest Natural, a regulated natural gas utility serving approximately 2 million customers across Oregon and Southwest Washington
- **IRP**: Integrated Resource Planning, NW Natural's long-term planning process
- **UPC**: Use Per Customer, the aggregate therms-per-customer metric used in NW Natural's top-down forecast
- **End-use**: A specific energy-consuming application (e.g., space heating, water heating, cooking)
- **Housing stock**: The total number and characteristics of residential premises in the service territory
- **Fuel switching**: Transition from natural gas to electricity (e.g., gas furnace to heat pump)
- **Weibull survival model**: A probabilistic model for equipment replacement timing based on age and median service life
- **Scenario**: A named set of parameter assumptions (growth rate, electrification rate, efficiency improvement) used to project future demand
- **Premise-equipment table**: The unified working dataset joining premise, equipment, segment, and code data

---

## Implemented Requirements

### Requirement 1: Model Scope and End-Use Mapping

**User Story:** As a planning analyst, I want the model to clearly define which end uses are simulated and how equipment codes map to them, so that I understand what is included and what is excluded.

#### Acceptance Criteria

1. THE Model SHALL simulate space heating as the primary modeled end use (furnaces, boilers, heat pumps, wall furnaces, floor furnaces, boilers)
2. THE Model SHALL define an `END_USE_MAP` in `src/config.py` mapping every `equipment_type_code` to one of: `space_heating`, `water_heating`, `cooking`, `clothes_drying`, `fireplace`, or `other`
3. THE Model SHALL define `DEFAULT_EFFICIENCY` by end-use category as a fallback when equipment-specific efficiency is unavailable
4. THE Model SHALL define `USEFUL_LIFE` (years) and `WEIBULL_BETA` (shape parameter) by end-use category for equipment replacement modeling
5. THE Model SHALL filter premises to active residential customers only (`custtype='R'`, `status_code='AC'`)
6. THE Model SHALL exclude commercial and industrial premises from all simulations

---

### Requirement 2: Housing Stock Representation

**User Story:** As a planning analyst, I want the model to represent the residential housing stock and project it forward, so that demand projections reflect realistic building counts and segment composition.

#### Acceptance Criteria

1. THE Model SHALL build a baseline housing stock from NW Natural's premise and segment data, keyed by `blinded_id`
2. THE Model SHALL represent premises by: `segment` (RESSF, RESMF, MOBILE), `subseg`, `mktseg`, `set_year` (construction vintage), and `district_code_IRP`
3. THE Model SHALL project total housing units forward using a configurable `housing_growth_rate` (scalar or year-indexed curve)
4. THE Model SHALL apply vintage-based heating multipliers (`VINTAGE_HEATING_MULTIPLIER`) and segment-based multipliers (`SEGMENT_HEATING_MULTIPLIER`) to differentiate demand by building age and type
5. THE Model SHALL use Census ACS B25024 historical data to project the SF/MF segment share shift over the forecast horizon
6. THE Model SHALL export a `housing_stock.csv` per scenario showing total units and segment breakdown by year

---

### Requirement 3: Equipment Inventory and Weibull Replacement Model

**User Story:** As a planning analyst, I want the model to track equipment inventories and simulate realistic replacement timing, so that efficiency improvements and fuel switching are modeled accurately.

#### Acceptance Criteria

1. THE Model SHALL build an equipment inventory from NW Natural's equipment data, joined to premise and segment data
2. THE Model SHALL track per-equipment attributes: `equipment_type_code`, `end_use`, `efficiency`, `install_year`, `useful_life`, `fuel_type`
3. THE Model SHALL implement a Weibull survival function `S(t) = exp(-(t/eta)^beta)` for equipment replacement probability
4. THE Model SHALL derive the Weibull scale parameter `eta` from ASHRAE median service life data (state-specific OR/WA), falling back to `USEFUL_LIFE` defaults
5. THE Model SHALL apply probabilistic replacement (not deterministic age cutoff) — each year, equipment is replaced with probability `1 - S(t)/S(t-1)`
6. THE Model SHALL apply scenario-driven electrification switching rates (gas → electric/heat pump) at replacement time
7. THE Model SHALL apply scenario-driven efficiency improvements to newly installed equipment each year

---

### Requirement 4: Weather-Driven Space Heating Simulation

**User Story:** As a planning analyst, I want space heating demand to be driven by actual weather data, so that projections reflect realistic climate conditions.

#### Acceptance Criteria

1. THE Model SHALL compute Heating Degree Days (HDD, base 65°F) from NW Natural's daily CalDay weather data
2. THE Model SHALL assign each premise to a weather station via `DISTRICT_WEATHER_MAP` in `src/config.py`, mapping `district_code_IRP` to ICAO station codes
3. THE Model SHALL simulate annual space heating consumption as: `HDD × heating_factor × vintage_multiplier × segment_multiplier / efficiency`
4. THE Model SHALL support three weather assumptions in scenario config: `"normal"` (use actual historical HDD), `"warm"` (below-normal HDD), `"cold"` (above-normal HDD)
5. THE Model SHALL load NOAA 30-year Climate Normals (1991–2020) for all 11 NW Natural weather stations to support weather normalization
6. THE Model SHALL compute a weather adjustment factor (`actual_HDD / normal_HDD`) for calibration and comparison

---

### Requirement 5: Demand Aggregation and IRP Comparison

**User Story:** As a planning analyst, I want the model to aggregate demand to system-level totals and compare against NW Natural's IRP forecast, so that I can evaluate the bottom-up model's alignment with existing projections.

#### Acceptance Criteria

1. THE Model SHALL aggregate simulated demand to system totals by: year, end-use, customer segment, and IRP district
2. THE Model SHALL compute Use Per Customer (UPC) as `total_therms / premise_count` for each year
3. THE Model SHALL load NW Natural's 10-Year Load Decay Forecast (2025–2035) and compare model UPC against it
4. THE Model SHALL export an `irp_comparison.csv` per scenario with columns: `year`, `model_upc`, `irp_upc`, `diff_therms`, `diff_pct`
5. THE Model SHALL export an `estimated_total_upc.csv` that adds RECS-derived non-heating end-use estimates to the space-heating-only model UPC
6. THE Model SHALL export a `yearly_summary.csv` with total therms, UPC, and premise count by year

---

### Requirement 6: Scenario Configuration and Execution

**User Story:** As a planning analyst, I want to define scenarios via JSON config files and run them from the command line, so that I can compare multiple demand futures without modifying code.

#### Acceptance Criteria

1. THE Model SHALL accept scenario configuration as a JSON file with required fields: `name`, `base_year`, `forecast_horizon`
2. THE Model SHALL support the following scenario parameters: `housing_growth_rate`, `electrification_rate`, `efficiency_improvement`, `weather_assumption`, `initial_gas_pct`, `use_recs_ratios`, `end_use_scope`, `max_premises`, `vectorized`
3. EACH parameter SHALL support either a scalar value or a year-indexed curve dict (e.g., `{"2025": 0.01, "2030": 0.02}`) resolved by `src/parameter_curves.py`
4. THE CLI SHALL accept one or more scenario JSON paths: `python -m src.main scenarios/baseline.json [scenarios/alt.json --compare]`
5. THE CLI SHALL support flags: `--output-dir`, `--baseline-only`, `--compare`, `--verbose`
6. EACH scenario SHALL write results to its own folder: `scenarios/{scenario_name}/` containing `results.csv`, `results.json`, `yearly_summary.csv`, `metadata.json`, `SUMMARY.md`, and optional supplemental CSVs

---

### Requirement 7: Data Loaders and Ingestion Pipeline

**User Story:** As a developer, I want each data source to have its own standalone loader, so that I can debug individual sources independently and the pipeline is easy to extend.

#### Acceptance Criteria

1. EACH data source SHALL have a dedicated loader in `src/loaders/` (one file per source)
2. EACH loader SHALL be runnable standalone: `python -m src.loaders.<name>` loads data, prints a summary, and saves diagnostics to `output/loaders/`
3. THE `src/loaders/_helpers.py` module SHALL provide `save_diagnostics(df, name)` for consistent diagnostic output across all loaders
4. THE `src/data_ingestion.py` module SHALL re-export all loaders and provide `build_premise_equipment_table(premises, equipment, segments, codes)` as the primary join function
5. THE `build_premise_equipment_table` function SHALL derive: `end_use` (via `END_USE_MAP`), `efficiency` (via `DEFAULT_EFFICIENCY`), and `weather_station` (via `DISTRICT_WEATHER_MAP`)
6. THE Model SHALL load the following NW Natural data: premise, equipment, equipment codes, segment, weather (CalDay), water temperature, billing, snow
7. THE Model SHALL load the following external data: RBSA 2022, RBSA 2017, ASHRAE service life (OR/WA), ASHRAE maintenance cost (OR/WA), IRP load decay forecast, historical UPC, baseload factors, NW energy proxies, Census B25034/B25040/B25024 county files, PSU population forecasts, WA OFM housing estimates, NOAA climate normals, EIA RECS microdata (2005–2020), tariff/rate data (OR/WA)

---

### Requirement 8: Data Validation and Quality Reporting

**User Story:** As a developer, I want automated data quality checks with HTML and Markdown reports, so that I can quickly identify data issues without manual inspection.

#### Acceptance Criteria

1. THE Model SHALL generate per-loader quality reports saved to `output/data_quality/` as both HTML and Markdown
2. EACH quality report SHALL include: row count, column dtypes, null counts, unique value counts, min/max/mean for numerics, top-10 frequencies for categoricals
3. THE Model SHALL generate a cross-loader join audit showing match rates between premise, equipment, segment, and billing tables
4. THE Model SHALL generate a join integrity dashboard at `output/join_integrity/` with pass/fail indicators for: end-use mapping coverage, efficiency validity, and weather station assignment
5. THE Model SHALL flag equipment codes not present in `END_USE_MAP` and report them as unmapped
6. THE Model SHALL generate distribution plots (histograms, bar charts) for key fields: equipment age, efficiency by end-use, HDD by station, premises by district, segment distribution

---

### Requirement 9: Census and RECS Integration

**User Story:** As a planning analyst, I want the model to incorporate Census housing data and EIA RECS benchmarks, so that the housing stock and end-use estimates are grounded in independent external sources.

#### Acceptance Criteria

1. THE Model SHALL load ACS 5-year B25034 (Year Structure Built) county-level data for all 16 NW Natural service territory counties (2009–2023)
2. THE Model SHALL load ACS 5-year B25040 (House Heating Fuel) county-level data to track gas market share over time
3. THE Model SHALL load ACS 5-year B25024 (Units in Structure) county-level data to validate SF/MF segment split
4. THE Model SHALL enrich the premise-equipment table with Census-derived vintage distribution and segment shift rates
5. THE Model SHALL load EIA RECS microdata (2005, 2009, 2015, 2020) and compute weighted-average end-use shares for Pacific division gas-heated homes
6. THE Model SHALL use RECS-derived non-heating ratios to estimate total UPC (space heating + water heating + cooking + drying + fireplace) when `use_recs_ratios=true` in scenario config
7. THE Model SHALL export Census and RECS summary CSVs alongside scenario results for reference

---

### Requirement 10: Calibration Against IRP Load Decay Data

**User Story:** As a planning analyst, I want the model to be calibrated against NW Natural's historical UPC data, so that the baseline simulation is anchored to observed demand trends.

#### Acceptance Criteria

1. THE Model SHALL load the three-era historical UPC framework: pre-2010 (~820 therms, 80% AFUE), 2011–2019 (~720 therms, 90%+ AFUE), 2020+ (~650 therms, heat pump hybrids)
2. THE Model SHALL load year-by-year historical UPC back to 2005 from `prior load decay data reconstructed.txt`
3. THE Model SHALL compare bottom-up UPC projections against the IRP 10-year load decay forecast (-1.19%/yr from 648 therm baseline)
4. THE Model SHALL support a `calibration.py` module for adjusting the `heating_factor` to align base-year model UPC with observed UPC
5. THE Model SHALL report calibration residuals (model UPC vs IRP UPC) in `irp_comparison.csv`

---

### Requirement 11: Static Visualization and Reporting

**User Story:** As a planning analyst, I want the model to generate static charts and summary reports, so that I can review results without running additional analysis scripts.

#### Acceptance Criteria

1. THE Model SHALL generate a `SUMMARY.md` per scenario with: configuration parameters, yearly demand table, end-use breakdown table, and output file list
2. THE Model SHALL generate scenario comparison charts (line charts, stacked area charts) using Matplotlib saved as PNG files
3. THE Model SHALL generate housing stock projection charts: total units over time, segment distribution, district distribution, growth rate analysis
4. THE Model SHALL generate a service territory map (static PNG) showing NW Natural counties with weather station markers
5. THE Model SHALL generate equipment age and efficiency distribution charts saved to `output/` subdirectories
6. ALL chart generation SHALL use a non-interactive Matplotlib backend (`Agg`) suitable for headless/server execution

---

### Requirement 12: Property-Based Testing

**User Story:** As a developer, I want property-based tests that verify mathematical correctness of the model, so that I can catch logic errors that unit tests might miss.

#### Acceptance Criteria

1. THE Model SHALL implement a Weibull survival monotonicity property: `S(t) <= S(t-1)` for all `t > 0`, and `S(0) = 1.0`
2. THE Model SHALL implement a replacement probability bounds property: `replacement_probability` is always in `[0, 1]`
3. THE Model SHALL implement a fuel switching conservation property: total equipment count before and after `apply_replacements` is equal
4. THE Model SHALL implement a housing stock growth property: projected `total_units = baseline × (1 + growth_rate)^years` within rounding tolerance
5. EACH property test SHALL save results to `output/` as both HTML and Markdown with pass/fail status, data summaries, and any generated plots
6. THE Model SHALL implement scenario output non-negativity: all `total_therms` values are >= 0

---

### Requirement 13: Logging and Transparency

**User Story:** As a developer, I want the model to log its execution clearly, so that I can trace what happened during a run and diagnose issues.

#### Acceptance Criteria

1. THE Model SHALL use Python's `logging` module with level `INFO` by default, configurable via `--verbose` flag for `DEBUG`
2. THE Model SHALL log: data load counts, join results, simulation progress by year, and output file paths
3. THE Model SHALL log warnings for: unmapped equipment codes, missing weather station assignments, data files not found, and premises with zero efficiency
4. THE Model SHALL include scenario metadata in `metadata.json`: scenario name, base year, forecast horizon, all parameter values, total rows, years simulated, end-uses, and execution timestamp
5. THE Model SHALL write a human-readable `SUMMARY.md` to each scenario output folder

---

## Future Work Requirements

The following requirements describe capabilities that were designed and partially specified but not implemented in the current capstone prototype. They are documented here to guide future development.

---

### Future Requirement A: Interactive Web Visualization with Geographic Drill-Down

**User Story:** As a stakeholder, I want to explore forecast results interactively on a map, so that I can understand demand patterns across different geographic and demographic segments.

#### Acceptance Criteria

1. THE Visualization SHALL display the NW Natural service territory with county boundaries color-coded by demand intensity (therms/customer)
2. WHEN a user clicks a county, THE Map SHALL zoom to district-level boundaries
3. THE Visualization SHALL support toggling between: county, district, microclimate (weather station service area), and microresidential (segment × vintage cohort) views
4. WHILE the user moves a year slider, THE Map colors SHALL update to reflect demand for that year
5. WHEN a user hovers over an area, THE Visualization SHALL display a tooltip with: demand, UPC, customer count, and electrification rate
6. THE Visualization SHALL support scenario comparison (dropdown to switch between scenarios)
7. THE Visualization SHALL display end-use breakdown as a stacked bar chart for any selected area

---

### Future Requirement B: REST API for Scenario Management

**User Story:** As a developer, I want to programmatically create scenarios, submit runs, and retrieve results via REST API, so that I can integrate the model with other systems.

#### Acceptance Criteria

1. THE API SHALL expose `POST /api/v1/scenarios` to create a new scenario and return a `scenario_id`
2. THE API SHALL expose `GET /api/v1/scenarios` to list all scenarios with status
3. THE API SHALL expose `POST /api/v1/scenarios/{scenario_id}/run` to submit a scenario for execution
4. THE API SHALL expose `GET /api/v1/runs/{run_id}` to return execution status and progress
5. THE API SHALL expose `GET /api/v1/runs/{run_id}/results` to return results in JSON, CSV, or Parquet
6. THE API SHALL expose `GET /api/v1/runs/{run_id}/results/geojson` to return results as GeoJSON for map rendering
7. THE API SHALL return standard HTTP status codes and structured error responses

---

### Future Requirement C: Composite Microregion Cell Analysis

**User Story:** As an analyst, I want to analyze demand at a composite cell level combining microclimate, microresidential, and adoption cohort dimensions, so that I can identify high-opportunity areas for electrification programs.

#### Acceptance Criteria

1. THE Model SHALL define composite cells as the intersection of: microclimate (weather station service area) × microresidential (segment + subsegment + vintage cohort) × adoption cohort (Early Adopters / Growth / Mature / Saturation)
2. THE Model SHALL compute a composite score (0–100) for each cell combining: demand intensity (40%), adoption rate (30%), efficiency gap (20%), climate severity (10%)
3. THE Model SHALL compute an opportunity score (high demand + low adoption) and success score (high adoption + low demand) per cell
4. THE Model SHALL export composite cell data as GeoJSON and CSV for visualization
5. THE Visualization SHALL support filtering cells by microclimate, microresidential, adoption cohort, and demand intensity

---

### Future Requirement D: Additional End-Use Simulation (Water Heating, Cooking, Drying, Fireplace)

**User Story:** As a planning analyst, I want the model to simulate all major residential gas end uses, so that total demand projections are complete.

#### Acceptance Criteria

1. THE Model SHALL simulate water heating consumption driven by Bull Run water temperature and daily hot water usage (64 gallons/day default)
2. THE Model SHALL simulate cooking consumption using RECS-derived baseload factors (~30 therms/year)
3. THE Model SHALL simulate clothes drying consumption using RECS-derived baseload factors (~20 therms/year)
4. THE Model SHALL simulate fireplace consumption using RBSA-metered baseload factors (~55 therms/year)
5. THE Model SHALL apply vintage-stratified water heater standby losses: pre-1990 (75 therms/yr), 1991–2003 (55), 2004–2014 (40), 2015+ (20)
6. THE Model SHALL apply pilot light loads for pre-2015 equipment (46–82 therms/yr depending on equipment type)

---

### Future Requirement E: Docker Containerization and Production Deployment

**User Story:** As an operator, I want the model packaged as a Docker container, so that it can be deployed reliably across different environments.

#### Acceptance Criteria

1. THE Model SHALL be packaged as a Docker container with all Python dependencies included
2. THE Model SHALL include a `docker-compose.yml` for multi-container deployment (model + visualization server)
3. THE Model SHALL support environment variable configuration for data paths, API keys, and scenario parameters
4. THE Model SHALL expose a health check endpoint at `GET /api/v1/health`
5. THE Model SHALL support deployment to common cloud platforms (AWS, Azure, GCP)

---

### Future Requirement F: RBSA Sub-Metered End-Use Data Integration

**User Story:** As a modeler, I want to use RBSA sub-metered 15-minute interval data to validate load shape assumptions, so that the model's baseload factors are empirically grounded.

#### Acceptance Criteria

1. THE Model SHALL load RBSA Metering Year 1 (Sep 2012–Sep 2013) tab-delimited TXT files (~328 MB each) using chunked reading
2. THE Model SHALL load RBSA Metering Year 2 (Apr 2013–Apr 2014) tab-delimited TXT files (~300 MB each)
3. THE Model SHALL parse SAS datetime timestamps from the metering files
4. THE Model SHALL compute diurnal and seasonal load shapes by end-use from the metered data
5. THE Model SHALL compare electric end-use load shapes against gas equivalents to validate baseload factor assumptions

---

### Future Requirement G: Green Building Registry API Integration

**User Story:** As a modeler, I want to supplement RBSA building data with Green Building Registry Home Energy Score data, so that building shell assumptions are more accurate for specific properties.

#### Acceptance Criteria

1. THE Model SHALL query the Green Building Registry API (`api.greenbuildingregistry.com`) by zip code for properties in NW Natural's service territory
2. THE API key SHALL be read from the `GBR_API_KEY` environment variable (never committed to source)
3. THE Model SHALL extract: Home Energy Score, estimated annual energy use, insulation levels, and window types per property
4. THE Model SHALL use GBR data to refine building shell assumptions for premises with matching records

---

### Future Requirement H: CI/CD Pipeline and Automated Testing

**User Story:** As a developer, I want automated tests to run on every code change, so that regressions are caught before they reach production.

#### Acceptance Criteria

1. THE Repository SHALL include a CI/CD pipeline (GitHub Actions or equivalent) that runs all tests on every pull request
2. THE Pipeline SHALL enforce minimum 80% code coverage for critical modules
3. THE Pipeline SHALL run property-based tests with at least 100 examples per property
4. THE Pipeline SHALL build and validate the Docker image on every merge to main
5. THE Pipeline SHALL fail and block merge if any test fails or coverage drops below threshold
