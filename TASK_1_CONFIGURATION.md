# Task 1: Project Structure and Configuration

## Status: ✅ Complete (1.1-1.7), 🔲 1.8 pending

## Overview

Task 1 sets up the `src/` package structure and `src/config.py` with all static configuration. Broken into 8 sub-tasks (max 6 items each). Sub-tasks 1.1-1.7 define the code structure and constants. Sub-task 1.8 is a property test that validates everything is wired correctly.

---

## Sub-task Details

### 1.1 Create `src/` package structure ✅

Creates the Python package scaffolding so all modules can import each other.

| File | Purpose |
|------|---------|
| `src/__init__.py` | Makes `src` a Python package |
| `src/loaders/__init__.py` | Makes `src.loaders` a package for individual data loaders |
| `src/loaders/_helpers.py` | Shared functions: `save_diagnostics()` (txt + CSV), `save_quality_report()` (HTML + MD) |
| `src/validation/__init__.py` | Makes `src.validation` a package for validation scripts |

**How to verify:** Run `python -c "from src import config; print('OK')"` — should print `OK` with no import errors.

---

### 1.2 Define end-use and equipment mappings ✅

These dictionaries are the core lookup tables that drive the entire model. They live in `src/config.py`.

| Constant | What it does | Example |
|----------|-------------|---------|
| `END_USE_MAP` | Maps equipment_type_code → end-use category | `"HEAT" → "space_heating"`, `"WTR" → "water_heating"` |
| `DEFAULT_EFFICIENCY` | Fallback efficiency when data is missing | `"space_heating" → 0.80`, `"water_heating" → 0.60` |
| `USEFUL_LIFE` | Default equipment lifespan (years) | `"space_heating" → 20`, `"water_heating" → 13` |
| `WEIBULL_BETA` | Shape parameter for Weibull survival model | `"space_heating" → 3.0`, `"appliances" → 2.5` |
| `DISTRICT_WEATHER_MAP` | Maps IRP district → weather station ICAO code | `"MULT" → "KPDX"`, `"LANE" → "KEUG"` |

**How to verify:** Run `python -c "from src.config import END_USE_MAP, DEFAULT_EFFICIENCY, USEFUL_LIFE, DISTRICT_WEATHER_MAP; print(f'{len(END_USE_MAP)} end-use codes, {len(DEFAULT_EFFICIENCY)} efficiency defaults, {len(USEFUL_LIFE)} life defaults, {len(DISTRICT_WEATHER_MAP)} district mappings')"` — should show counts for all four dicts (e.g. `12 end-use codes, 6 efficiency defaults, 6 life defaults, 17 district mappings`).

---

### 1.3 Define NW Natural proprietary file paths ✅

Points to the blinded/anonymized data files supplied by NW Natural in `Data/NWNatural Data/`.

| Constant | File | Content |
|----------|------|---------|
| `PREMISE_DATA` | `premise_data_blinded.csv` | ~500K residential premises |
| `EQUIPMENT_DATA` | `equipment_data_blinded.csv` | ~1M equipment records |
| `EQUIPMENT_CODES` | `equipment_codes.csv` | Equipment type lookup table |
| `SEGMENT_DATA` | `segment_data_blinded.csv` | Customer segment/vintage info |
| `BILLING_DATA` | `billing_data_blinded.csv` | Historical billing (full) |
| `BILLING_DATA_SMALL` | `small_billing_data_blinded.csv` | Billing (dev subset) |
| `WEATHER_CALDAY` | `DailyCalDay1985_Mar2025.csv` | Daily weather (calendar day) |
| `WEATHER_GASDAY` | `DailyGasDay2008_Mar2025.csv` | Daily weather (gas day) |
| `WATER_TEMP` | `BullRunWaterTemperature.csv` | Incoming cold water temp |
| `PORTLAND_SNOW` | `Portland_snow.csv` | Daily snowfall/depth |

**How to verify:** Run `python -c "from src import config; import os; missing = [k for k in ['PREMISE_DATA','EQUIPMENT_DATA','EQUIPMENT_CODES','SEGMENT_DATA','WEATHER_CALDAY','WATER_TEMP','PORTLAND_SNOW'] if not os.path.exists(getattr(config, k))]; print(f'{len(missing)} missing: {missing}' if missing else 'All NWN files present')"` — will show which files are missing (expected until NW Natural data is placed).

---

### 1.4 Define tariff and rate file paths ✅

Points to team-created CSVs extracted from NW Natural rate PDFs. These are in `Data/` (root).

| Constant | File | Content |
|----------|------|---------|
| `OR_RATES` | `or_rates_oct_2025.csv` | Oregon current rates (14 rows) |
| `OR_RATE_CASE_HISTORY` | `or_rate_case_history.csv` | Oregon rate cases 1975-2025 (22 rows) |
| `OR_WACOG_HISTORY` | `or_wacog_history.csv` | Oregon WACOG 2018-2025 (16 rows) |
| `WA_RATES` | `wa_rates_nov_2025.csv` | Washington current rates (14 rows) |
| `WA_RATE_CASE_HISTORY` | `wa_rate_case_history.csv` | Washington rate cases (16 rows) |
| `WA_WACOG_HISTORY` | `wa_wacog_history.csv` | Washington WACOG 2018-2025 (16 rows) |
| `OR_CURRENT_RATE` | — | `1.41220` $/therm (OR Schedule 2) |
| `WA_CURRENT_RATE` | — | `1.24164` $/therm (WA Schedule 2) |

**How to verify:** Run `python -c "from src import config; import os; files = ['OR_RATES','WA_RATES','OR_WACOG_HISTORY','WA_WACOG_HISTORY','OR_RATE_CASE_HISTORY','WA_RATE_CASE_HISTORY']; present = sum(1 for f in files if os.path.exists(getattr(config, f))); print(f'{present}/{len(files)} tariff files present')"` — should show `6/6 tariff files present`.

---

### 1.5 Define external data source paths ✅

Points to public/external datasets (RBSA, ASHRAE, IRP calibration, baseload factors, metering).

| Group | Key Constants | Source |
|-------|--------------|--------|
| RBSA 2022 | `RBSA_2022_SITE_DETAIL`, `RBSA_2022_HVAC`, `RBSA_2022_WATER_HEATER`, etc. | NEEA building stock assessment |
| ASHRAE | `ASHRAE_OR_SERVICE_LIFE`, `ASHRAE_WA_SERVICE_LIFE`, etc. | Equipment service life/maintenance |
| IRP/Calibration | `IRP_LOAD_DECAY_FORECAST`, `LOAD_DECAY_RECONSTRUCTED`, `LOAD_DECAY_SIMULATED` | NW Natural IRP UPC forecast |
| Baseload | `BASELOAD_FACTORS_CSV`, `NW_ENERGY_PROXIES_CSV` | DOE/RECS/RBSA consumption factors |
| Metering | `RBSAM_Y1_DIR`, `RBSAM_Y2_DIR`, `RBSA_2017_DIR` | RBSA sub-metered end-use data |

**How to verify:** Run `python -c "from src import config; import os; print('IRP forecast:', os.path.exists(config.IRP_LOAD_DECAY_FORECAST)); print('Baseload factors:', os.path.exists(config.BASELOAD_FACTORS_CSV)); print('Energy proxies:', os.path.exists(config.NW_ENERGY_PROXIES_CSV))"` — IRP forecast, baseload factors, and energy proxies should all show `True`.

---

### 1.6 Define API and Census constants ✅

API endpoints and Census data paths for runtime data fetching and offline fallback files.

| Group | Key Constants | Notes |
|-------|--------------|-------|
| GBR API | `GBR_API_BASE_URL`, `GBR_API_KEY_ENV_VAR` | Requires `GBR_API_KEY` env var |
| Census API | `CENSUS_API_BASE`, `CENSUS_ACS1_TEMPLATE`, `CENSUS_ACS5_TEMPLATE` | No API key needed |
| Census tables | `CENSUS_B25034_GROUP`, `CENSUS_B25040_GROUP`, `CENSUS_B25024_GROUP` | Year Built, Heating Fuel, Units in Structure |
| Census files | `B25034_COUNTY_DIR`, `B25040_COUNTY_DIR`, `B25024_COUNTY_DIR` | Offline county-level CSVs |
| Service territory | `NWN_SERVICE_TERRITORY_CSV` | 16 county FIPS codes |
| PSU forecasts | `PSU_PROJECTION_DIR` | Oregon county population forecasts |
| WA OFM | `OFM_HOUSING_XLSX` | Washington housing estimates |
| NOAA | `NOAA_NORMALS_DIR`, `NOAA_CDO_API_BASE`, `ICAO_TO_GHCND` | 11 weather stations |
| RECS | `RECS_DIR`, `RECS_2020_CSV`, etc. | EIA survey microdata |

**How to verify:** Run `python -c "from src import config; print(f'Service territory: {config.NWN_SERVICE_TERRITORY_CSV}'); print(f'ICAO stations: {len(config.ICAO_TO_GHCND)}'); print(f'Census API: {config.CENSUS_API_BASE}')"` — should show the service territory path, 11 ICAO stations, and the Census API URL.

---

### 1.7 Define simulation parameters ✅

Core constants used by the simulation engine.

| Constant | Value | Purpose |
|----------|-------|---------|
| `BASE_YEAR` | 2025 | Starting year for projections |
| `DEFAULT_BASE_TEMP` | 65.0°F | HDD/CDD base temperature |
| `DEFAULT_HOT_WATER_TEMP` | 120.0°F | Target hot water temperature |
| `DEFAULT_COLD_WATER_TEMP` | 55.0°F | Assumed incoming cold water temp |
| `DEFAULT_DAILY_HOT_WATER_GALLONS` | 64.0 | Average daily hot water usage per household |
| `LOG_LEVEL`, `LOG_FORMAT`, `OUTPUT_DIR` | — | Logging and output configuration |

**How to verify:** Run `python -c "from src.config import BASE_YEAR, DEFAULT_BASE_TEMP, DEFAULT_HOT_WATER_TEMP; print(f'Base year: {BASE_YEAR}, HDD base: {DEFAULT_BASE_TEMP}F, WH target: {DEFAULT_HOT_WATER_TEMP}F')"` — should show `Base year: 2025, HDD base: 65.0F, WH target: 120.0F`.

---

### 1.8 Property test: config completeness 🔲

Validates that all config dictionaries are internally consistent and all file paths point to real files.

**What it checks:**
1. All `END_USE_MAP` values are non-empty strings
2. All `DEFAULT_EFFICIENCY` keys match `END_USE_MAP` values, all values in (0, 1]
3. All `USEFUL_LIFE` keys match `END_USE_MAP` values, all values are positive integers
4. All `DISTRICT_WEATHER_MAP` values are valid ICAO codes present in `ICAO_TO_GHCND`
5. All file path constants reference files that exist on disk (missing = warning, not failure)

**Output:** `output/config_validation/config_completeness.html` and `.md` with pass/fail per check

**How to run:** `python -m src.validation.run_config_completeness`

**How to verify output:** Open `output/config_validation/config_completeness.html` in a browser. Each check should show ✅ (pass) or ❌ (fail) with details. File existence checks will show ⚠️ for missing files — that's expected until all data is placed.
