# Model Inputs: NW Natural End-Use Forecasting Model

## Overview

The model ingests data from multiple sources organized by provenance. All input files are located in the `Data/` directory. This document specifies the format, structure, and requirements for each input dataset.

## NW Natural Proprietary Data

Located in `Data/NWNatural Data/` (blinded/anonymized).

### premise_data_blinded.csv
**Purpose**: Residential premise master file with location and service information.

**Required Columns**:
- `blinded_id` (int): Anonymized premise identifier (primary key)
- `service_state` (str): 'OR' or 'WA'
- `district_code_IRP` (str): IRP district code for geographic grouping (e.g., 'PORC', 'EUGN')
- `status_code` (str): Premise status ('AC' = active, others filtered out)
- `custtype` (str): Customer type ('R' = residential, others filtered out)

**Filtering**: Load only rows where `custtype='R'` AND `status_code='AC'`.

**Expected Volume**: ~500,000-700,000 active residential premises.

### equipment_data_blinded.csv
**Purpose**: Equipment inventory by premise.

**Required Columns**:
- `blinded_id` (int): Foreign key to premise_data_blinded
- `equipment_type_code` (str): Equipment type identifier (e.g., 'RFAU', 'RAWH', 'RRGE')
- `QTY_OF_EQUIPMENT_TYPE` (int): Quantity of this equipment type at the premise

**Constraints**: Must join successfully with premise_data_blinded on `blinded_id`.

### equipment_codes.csv
**Purpose**: Equipment type lookup table mapping codes to end-use categories.

**Required Columns**:
- `equipment_type_code` (str): Equipment type identifier (primary key)
- `equipment_class` (str): Equipment class ('HEAT', 'WTR', 'FRPL', 'OTHR')
- `description` (str): Human-readable equipment description

**Mapping**: Used to derive `end_use` via `END_USE_MAP` in config.py.

### segment_data_blinded.csv
**Purpose**: Customer segment and vintage information.

**Required Columns**:
- `blinded_id` (int): Foreign key to premise_data_blinded
- `custtype` (str): Customer type ('R' for residential)
- `segment` (str): Housing segment ('RESSF' = single-family, 'RESMF' = multi-family)
- `subseg` (str): Sub-segment (e.g., 'FRAME', 'MFG', 'MOBILE')
- `mktseg` (str): Market segment (e.g., 'RES-CONV', 'RES-SFNC')
- `setmonth` (int): Month premise was set/connected (1-12)
- `setday` (int): Day premise was set/connected (1-31)
- `setyear` (int): Year premise was set/connected (e.g., 2015)

**Filtering**: Load only rows where `custtype='R'`.

**Constraints**: Must join successfully with premise_data_blinded on `blinded_id`.

### billing_data_blinded.csv (or small_billing_data_blinded.csv for development)
**Purpose**: Historical billing data for calibration and validation.

**Required Columns**:
- `blinded_id` (int): Foreign key to premise_data_blinded
- `rate_schedule` (str): Rate schedule code (e.g., 'Schedule 2')
- `rate_class` (str): Rate class identifier
- `GL_revenue_date` (int): Date in YYYYMM format (e.g., 202501 for January 2025)
- `utility_usage` (float): Dollar amount of gas charges (to be converted to therms)

**Data Quality**: 
- `utility_usage` may contain non-numeric characters (e.g., '$', commas) — must be parsed to float
- Missing or zero values should be logged as warnings
- Expected volume: millions of billing records spanning 2015-2025

**Note**: `small_billing_data_blinded.csv` is a smaller development version for testing.

### DailyCalDay1985_Mar2025.csv
**Purpose**: Daily weather data (calendar day basis).

**Required Columns**:
- `date` (str or datetime): Date in YYYY-MM-DD format
- `site_id` (str): Weather station identifier (ICAO code, e.g., 'KPDX')
- `temp` (float): Daily average temperature (°F)
- `max_temp` (float): Daily maximum temperature (°F)
- `min_temp` (float): Daily minimum temperature (°F)
- `dewpt_temp` (float): Daily average dew point (°F)
- `humidity_pct` (float): Daily average relative humidity (%)
- `precip` (float): Daily precipitation (inches)

**Coverage**: 1985-2025 (40 years), all 11 NW Natural weather stations.

**Data Quality**: Missing values may be represented as NaN or -9999 — standardize to NaN.

### DailyGasDay2008_Mar2025.csv
**Purpose**: Daily weather data (gas day basis, Oct-Sep fiscal year).

**Format**: Same as DailyCalDay1985_Mar2025.csv but aligned to gas utility fiscal year.

**Coverage**: 2008-2025, all 11 NW Natural weather stations.

### BullRunWaterTemperature.csv
**Purpose**: Incoming cold water temperature for water heating demand calculation.

**Required Columns**:
- `date` (str or datetime): Date in YYYY-MM-DD format
- `bull_run_water_temp` (float): Daily average water temperature (°F)
- `flag` (str): Data quality flag (e.g., 'E' = estimated, blank = measured)

**Coverage**: 1985-2025 (40 years), single source (Bull Run water supply).

**Data Quality**: Missing values should be interpolated or flagged for exclusion.

### Portland_snow.csv
**Purpose**: Daily snowfall and snow depth for peak demand analysis.

**Required Columns**:
- `Year` (int): Calendar year
- `Month` (int): Month (1-12)
- `Day` (int): Day of month (1-31)
- `Date` (str or datetime): Formatted date
- `snow` (float): Daily snowfall (inches)
- `snwd` (float): Snow depth on ground (inches)

**Coverage**: 1985-2025 (40 years), Portland area only.

**Usage**: Flags extreme weather days for validation; correlates with peak gas demand events.

## Tariff and Rate Data

Located in `Data/` (team-created, manually extracted from utility rate PDFs).

### or_rates_oct_2025.csv
**Purpose**: Current Oregon residential gas rates (October 2025).

**Required Columns**:
- `Schedule` (str): Rate schedule (e.g., 'Schedule 2')
- `Type` (str): Rate component type (e.g., 'Distribution', 'WACOG')
- `Description` (str): Human-readable description
- `Rate/Value` (float): Rate per therm or fixed charge
- `Unit` (str): Unit of measurement (e.g., '$/therm', '$/month')

**Key Value**: Schedule 2 residential = $1.41220/therm (as of October 2025).

### wa_rates_nov_2025.csv
**Purpose**: Current Washington residential gas rates (November 2025).

**Format**: Same as or_rates_oct_2025.csv.

**Key Value**: Schedule 2 residential = $1.24164/therm (as of November 2025).

### or_wacog_history.csv
**Purpose**: Oregon WACOG (Weighted Average Cost of Gas) history for rate reconstruction.

**Required Columns**:
- `Effective Date` (str or datetime): Date rate became effective
- `Rate per Therm` (float): WACOG rate ($/therm)
- `Type` (str): Rate type ('Annual' or 'Winter')

**Coverage**: 2018-2025, monthly or quarterly updates.

### wa_wacog_history.csv
**Purpose**: Washington WACOG history.

**Format**: Same as or_wacog_history.csv.

### or_rate_case_history.csv
**Purpose**: Oregon rate case history for reconstructing historical rates.

**Required Columns**:
- `Date Applied` (str or datetime): Date rate case was filed
- `Date Effective` (str or datetime): Date rate became effective
- `Granted Percent` (float): Percentage increase/decrease granted (e.g., 0.05 for +5%)
- `Schedule` (str): Rate schedule affected

**Coverage**: 2010-2025, all major rate cases.

**Usage**: Work backward from current rates using granted percentages to reconstruct historical $/therm.

### wa_rate_case_history.csv
**Purpose**: Washington rate case history.

**Format**: Same as or_rate_case_history.csv.

## Building Stock and Equipment Data

### Data/2022 RBSA Datasets/ (NEEA Residential Building Stock Assessment 2022)

**Key Files**:
- `SiteDetail.csv`: Building characteristics (area, vintage, bedrooms, heating zone, building type, gas utility flag, site case weights)
- `Mechanical_HeatingAndCooling.csv`: HVAC system types, fuel, efficiency (AFUE/COP), vintage, capacity
- `Mechanical_WaterHeater.csv`: Water heater type, fuel, efficiency (EF), capacity, vintage
- `Appliance_Stove_Oven.csv`: Cooking equipment fuel type (gas/electric)
- `Appliance_Laundry.csv`: Dryer fuel type (gas/electric), heat pump flag
- `Building_Shell_One_Line.csv`: Envelope U-values (ceiling, wall, floor, window), whole-house UA

**Filtering**: Load only sites where `NWN_SF_StrataVar='NWN'` OR `Gas_Utility='NW NATURAL GAS'` to match NW Natural service territory.

**Weighting**: Use `Site_Case_Weight` column for population-level estimates.

**Expected Volume**: ~400-600 NWN-filtered sites representing ~500,000 homes.

### Data/ashrae/ (ASHRAE Public Database Exports)

**Files**:
- `OR-ASHRAE_Service_Life_Data.xls`: Median service life (years) by equipment type for Oregon
- `WA-ASHRAE_Service_Life_Data.xls`: Median service life (years) by equipment type for Washington
- `OR-ASHRAE_Maintenance_Cost_Data.xls`: Annual maintenance cost by equipment type for Oregon
- `WA-ASHRAE_Maintenance_Cost_Data.xls`: Annual maintenance cost by equipment type for Washington

**Format**: Excel XLS files with equipment categories and state-specific values.

**Usage**: Replaces hardcoded `USEFUL_LIFE` defaults in config.py with empirically grounded median lifetimes.

## Validation and Calibration Data

### Data/10-Year Load Decay Forecast (2025-2035).csv
**Purpose**: NW Natural's 2025 IRP Use Per Customer (UPC) forecast for validation.

**Required Columns**:
- `Year` (int): Forecast year (2025-2035)
- `UPC` (float): Use Per Customer in therms
- `Segment` (str): Customer segment (optional)

**Usage**: Compare bottom-up model UPC projections against this top-down econometric forecast.

### Data/prior load decay data description.txt
**Purpose**: Documentation of three-era UPC framework and RBSA vintage mapping.

**Content**: Describes historical decay rates and vintage-level calibration anchors:
- Pre-2010: ~820 therms, 80% AFUE
- 2011-2019: ~720 therms, 90%+ AFUE condensing
- 2020+: ~650 therms, heat pump hybrids

### Data/prior load decay data reconstructed.txt
**Purpose**: Historical UPC by year back to 2005.

**Format**: Year, UPC (therms) pairs.

**Coverage**: 2005-2025.

### Data/prior load decay data simulated.txt
**Purpose**: Year-by-year UPC multipliers vs. 2025 baseline.

**Format**: Year, Multiplier pairs.

## Baseload and Parameter Data

### Data/Baseload Consumption Factors.csv
**Purpose**: Non-weather-sensitive end-use consumption parameters.

**Required Columns**:
- `Category` (str): End-use category (e.g., 'Cooking', 'Drying', 'Fireplace')
- `SubCategory` (str): Sub-category (e.g., 'Pilot Light', 'Standby Loss')
- `Parameter` (str): Parameter name (e.g., 'Annual Consumption', 'Vintage Adjustment')
- `Value` (float): Parameter value
- `Unit` (str): Unit of measurement (e.g., 'therms/yr', 'multiplier')
- `Source` (str): Data source (e.g., 'RECS 2020', 'RBSA 2022')

**Key Values**:
- Cooking: 30 therms/yr
- Drying: 20 therms/yr
- Fireplace: 55 therms/yr
- Pilot loads (pre-2015): 46-82 therms/yr
- WH standby losses: 75/55/40/20 therms/yr by vintage

### Data/nw_energy_proxies.csv
**Purpose**: Compact parameter set with building envelope UA values by vintage era.

**Required Columns**:
- `Vintage_Era` (str): Construction era (e.g., 'pre-1950', '1951-1980', '1981-2010', '2011+')
- `Envelope_UA` (float): Building envelope UA value (Btu/h/°F)
- `Weibull_Beta` (float): Weibull shape parameter by equipment type
- `Baseload_Factor` (float): Baseload consumption adjustment

**Envelope UA Values**:
- Pre-1950: U=0.250
- 1951-1980: U=0.081
- 1981-2010: U=0.056
- 2011+: U=0.038

## Census and Demographic Data

### Data/NW Natural Service Territory Census data.csv
**Purpose**: FIPS codes for the 16 NW Natural service territory counties.

**Required Columns**:
- `State` (str): 'OR' or 'WA'
- `County` (str): County name
- `FIPS` (int): County FIPS code

**Coverage**: 13 Oregon counties + 3 Washington counties.

### Data/B25034-5y-county/ (Census ACS 5-Year B25034 County-Level Data)
**Purpose**: Housing unit counts by decade of construction (vintage distribution).

**Files**: `B25034_acs5_{year}.csv` for years 2009-2023 (15 annual files).

**Format**: Census API CSV format with county-level data.

**Coverage**: All 16 NW Natural service territory counties.

**Usage**: Validate model's housing stock vintage distribution against Census counts.

### Data/B25040-5y-county/ (Census ACS 5-Year B25040 County-Level Data)
**Purpose**: Housing unit counts by primary heating fuel (gas market share).

**Files**: `B25040_acs5_{year}.csv` for years 2009-2023.

**Coverage**: All 16 NW Natural service territory counties.

**Usage**: Calibrate baseline gas equipment penetration rates; track electrification trends.

### Data/B25024-5y-county/ (Census ACS 5-Year B25024 County-Level Data)
**Purpose**: Housing unit counts by structure type (SF vs. MF validation).

**Files**: `B25024_acs5_{year}.csv` for years 2009-2023.

**Coverage**: All 16 NW Natural service territory counties.

**Usage**: Validate model's RESSF/RESMF segment split.

## Population and Housing Growth Data

### Data/PSU projection data/ (Portland State University Population Forecasts)

**Folders**:
- `2025/`: Region 4 forecasts (Benton, Lane, Lincoln, Linn, Marion, Polk)
- `2024/`: Region 3 forecasts (Clackamas, Clatsop, Columbia, Multnomah, Washington, Yamhill)
- `2023/`: Region 1 forecast (Coos County)

**Format Variants**:
- 2025 files: CSV with columns YEAR, POPULATION (comma-formatted), TYPE (Estimate/Forecast)
- 2024 files: CSV with columns YEAR, POPULATION (no TYPE)
- 2023 Coos file: Wide CSV with areas as rows, years as columns

**Coverage**: All 13 Oregon NW Natural counties, historical estimates (1990-2020) + forecasts to 2070+.

**Usage**: Most authoritative source for Oregon `housing_growth_rate` scenario parameter.

### Data/ofm_april1_housing.xlsx (WA OFM Postcensal Housing Estimates)
**Purpose**: Washington state housing unit estimates by county and structure type.

**Sheet**: "Housing Units"

**Structure**: 28 columns: Line, Filter, County, Jurisdiction, then 6 years (2020-2025) × 4 metrics (Total, One Unit, Two or More, Mobile Homes).

**Key Rows**:
- Clark County: Line 41
- Skamania County: Line 316
- Klickitat County: Line 200

**Filter**: Use only rows where Filter=1 (county totals).

**Coverage**: 2020-2025 (6 years), all Washington counties.

**Usage**: Housing growth rates and structure-type validation for WA counties.

## Weather Normals Data

### Data/noaa_normals/ (NOAA 30-Year Climate Normals 1991-2020)

**Files per Station**:
- `{ICAO}_daily_normals.csv`: 365 rows with daily normal temperatures (avg/max/min), HDD, CDD
- `{ICAO}_monthly_normals.csv`: 12 rows with monthly normal temperatures, HDD, CDD

**Stations** (11 total):
- KPDX (Portland), KEUG (Eugene), KSLE (Salem), KAST (Astoria), KDLS (Dallesport/The Dalles)
- KOTH (North Bend/Coos Bay), KONP (Newport), KCVO (Corvallis), KHIO (Hillsboro)
- KTTD (Troutdale), KVUO (Vancouver WA)

**Data Quality**: NOAA sentinel value -7777 indicates insufficient data — treat as NaN.

**Usage**: Weather-normalize baseline simulations; compute weather adjustment factors; provide reference for scenario projections.

## EIA RECS Microdata

### Data/Residential Energy Consumption Servey/ (EIA RECS 1993-2020)

**CSV Files** (primary):
- `recs2020_public_v7.csv` (799 columns): State-level geography, full end-use disaggregation
- `recs2015_public_v4.csv` (759 columns): Division-level geography, no `BTUNGOTH`
- `2009/recs2009_public.csv` (940 columns): Division-level, no cooking/drying split
- `2005/RECS05alldata.csv` (1075 columns): Division-level, appliance aggregate

**Fixed-Width Files** (reference only):
- `1993/`, `1997/`, `2001/`: Fixed-width format with codebook pairs

**Key Columns** (2020 RECS):
- Geography: `STATE_FIPS`, `state_postal`, `DIVISION`, `REGIONC`
- Housing: `TYPEHUQ`, `YEARMADERANGE`, `TOTSQFT_EN`
- Equipment: `EQUIPM`, `FUELHEAT`, `FUELH2O`
- NG End-Use BTU: `BTUNG`, `BTUNGSPH`, `BTUNGWTH`, `BTUNGCOK`, `BTUNGCDR`, `BTUNGNEC`, `BTUNGOTH`
- Climate: `HDD65`, `CDD65`, `HDD30YR_PUB`, `CDD30YR_PUB`
- Weights: `NWEIGHT` (primary), `NWEIGHT1-60` (replicate)

**Filtering**: Use `DIVISION=9` (Pacific) and `FUELHEAT=1` (utility gas) for NW Natural comparison.

**Usage**: Independent validation benchmark for end-use disaggregation ratios and per-customer consumption estimates.

## Scenario Configuration

### Scenario Input File (JSON or Python dict)
**Purpose**: Define scenario parameters for projection runs.

**Required Fields**:
- `name` (str): Scenario identifier (e.g., 'baseline', 'high_electrification')
- `description` (str): Human-readable description
- `base_year` (int): Starting year for projections (e.g., 2025)
- `forecast_horizon` (int): Number of years to project (e.g., 10)
- `housing_growth_rate` (float): Annual housing unit growth rate (0.0-0.05)
- `electrification_rate` (dict): Annual electrification rate by end-use (0.0-1.0)
  - Keys: 'space_heating', 'water_heating', 'cooking', 'drying'
  - Values: Annual switching rate (fraction per year)
- `efficiency_improvement` (dict): Annual efficiency improvement by end-use (0.0-0.05)
  - Keys: 'space_heating', 'water_heating', 'cooking', 'drying'
  - Values: Annual efficiency gain (fraction per year)
- `weather_assumption` (str): 'normal', 'warm', or 'cold'

**Example**:
```json
{
  "name": "baseline",
  "description": "Reference case with historical trends",
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
  "weather_assumption": "normal"
}
```

## Data Quality and Validation

### Expected Data Volumes
- Premises: 500,000-700,000 active residential
- Equipment records: 1,000,000-1,500,000 (multiple units per premise)
- Billing records: 10,000,000+ (monthly records per premise, 10+ years)
- Weather records: 150,000+ (daily records × 11 stations × 40 years)

### Missing Data Handling
- Premises with no equipment records: Log warning, exclude from simulation
- Equipment with missing efficiency: Use `DEFAULT_EFFICIENCY` from config
- Billing records with missing/zero usage: Log warning, exclude from calibration
- Weather records with missing values: Interpolate or use normals as fallback

### Data Consistency Checks
- All `blinded_id` in equipment_data must exist in premise_data
- All `equipment_type_code` in equipment_data must exist in equipment_codes
- All `blinded_id` in segment_data must exist in premise_data
- All `blinded_id` in billing_data must exist in premise_data
- Weather station SiteIds must match `DISTRICT_WEATHER_MAP` in config

## Summary

The model expects a comprehensive set of inputs spanning:
1. **NW Natural proprietary data**: Premises, equipment, segments, billing, weather
2. **Tariff and rate data**: Current rates and historical rate cases for billing conversion
3. **Building stock data**: RBSA 2022 and ASHRAE service life/maintenance cost
4. **Validation data**: IRP load decay forecasts and historical UPC
5. **Census and demographic data**: Housing vintage, heating fuel, structure type distributions
6. **Population forecasts**: PSU (Oregon) and OFM (Washington) housing growth projections
7. **Weather normals**: NOAA 30-year climate normals for weather normalization
8. **RECS microdata**: EIA survey data for independent end-use validation
9. **Microclimate terrain data**: DOGAMI/WA DNR LiDAR (elevation, aspect, air drainage), PRISM temperature normals (800 m), Landsat 9 land surface temperature (30 m), MesoWest/NREL wind observations, NLCD impervious surface / asphalt albedo, and ODOT/WSDOT road networks for traffic heat emissions
10. **Scenario configuration**: User-defined parameters for projection runs

All inputs are organized by source provenance in the `Data/` directory and are documented in the design.md and tasks.md files.


## Data Source Inventory — Color-Coded Reference

The table below classifies every data source along two dimensions:
1. **Provenance**: 🟢 NW Natural (proprietary) · 🟡 Team-created (from NWN docs) · 🔵 External/Public
2. **Access method**: 📁 Local file · 🌐 Runtime API call

### 🟢 NW Natural — Proprietary / Blinded (15 sources, all 📁 FILE)

| # | Data Source | Config Constant | Path | Loader |
|---|-----------|----------------|------|--------|
| 1 | Premise data (blinded) | `PREMISE_DATA` | `Data/NWNatural Data/premise_data_blinded.csv` | `load_premise_data()` |
| 2 | Equipment inventory (blinded) | `EQUIPMENT_DATA` | `Data/NWNatural Data/equipment_data_blinded.csv` | `load_equipment_data()` |
| 3 | Equipment codes lookup | `EQUIPMENT_CODES` | `Data/NWNatural Data/equipment_codes.csv` | `load_equipment_codes()` |
| 4 | Segment data (blinded) | `SEGMENT_DATA` | `Data/NWNatural Data/segment_data_blinded.csv` | `load_segment_data()` |
| 5 | Billing data (blinded) | `BILLING_DATA` | `Data/NWNatural Data/billing_data_blinded.csv` | `load_billing_data()` |
| 6 | Daily weather — CalDay | `WEATHER_CALDAY` | `Data/NWNatural Data/DailyCalDay1985_Mar2025.csv` | `load_weather_data()` |
| 7 | Daily weather — GasDay | `WEATHER_GASDAY` | `Data/NWNatural Data/DailyGasDay2008_Mar2025.csv` | `load_weather_data()` |
| 8 | Bull Run water temperature | `WATER_TEMP` | `Data/NWNatural Data/BullRunWaterTemperature.csv` | `load_water_temperature()` |
| 9 | Portland snow data | `PORTLAND_SNOW` | `Data/NWNatural Data/Portland_snow.csv` | `load_snow_data()` |
| 10 | IRP 10-Year Load Decay Forecast | `IRP_LOAD_DECAY_FORECAST` | `Data/10-Year Load Decay Forecast (2025–2035).csv` | `load_load_decay_forecast()` |
| 11 | Prior load decay — description | `LOAD_DECAY_DESCRIPTION` | `Data/prior load decay data description.txt` | `load_historical_upc()` |
| 12 | Prior load decay — reconstructed | `LOAD_DECAY_RECONSTRUCTED` | `Data/prior load decay data reconstructed.txt` | `load_historical_upc()` |
| 13 | Prior load decay — simulated | `LOAD_DECAY_SIMULATED` | `Data/prior load decay data simulated.txt` | `load_historical_upc()` |
| 14 | IRP context document | `IRP_CONTEXT` | `Data/Integrated Resource Plan (IRP),.txt` | *reference only* |
| 15 | Service territory FIPS codes | `NWN_SERVICE_TERRITORY_CSV` | `Data/NW Natural Service Territory Census data.csv` | `load_service_territory_fips()` |

### 🟡 Team-Created — Extracted from NW Natural Rate PDFs (10 sources, all 📁 FILE)

| # | Data Source | Config Constant | Path | Loader |
|---|-----------|----------------|------|--------|
| 16 | Oregon current rates (Oct 2025) | `OR_RATES` | `Data/or_rates_oct_2025.csv` | `load_or_rates()` |
| 17 | Oregon rate case history | `OR_RATE_CASE_HISTORY` | `Data/or_rate_case_history.csv` | `load_rate_case_history()` |
| 18 | Oregon WACOG history | `OR_WACOG_HISTORY` | `Data/or_wacog_history.csv` | `load_wacog_history()` |
| 19 | Washington current rates (Nov 2025) | `WA_RATES` | `Data/wa_rates_nov_2025.csv` | `load_wa_rates()` |
| 20 | Washington rate case history | `WA_RATE_CASE_HISTORY` | `Data/wa_rate_case_history.csv` | `load_rate_case_history()` |
| 21 | Washington WACOG history | `WA_WACOG_HISTORY` | `Data/wa_wacog_history.csv` | `load_wacog_history()` |
| 22 | Baseload consumption factors | `BASELOAD_FACTORS_CSV` | `Data/Baseload Consumption Factors.csv` | `load_baseload_factors()` |
| 23 | Baseload factors reference impl. | `BASELOAD_FACTORS_PY` | `Data/Baseload Consumption factors.py` | *reference only* |
| 24 | NW Energy Proxies (compact params) | `NW_ENERGY_PROXIES_CSV` | `Data/nw_energy_proxies.csv` | `load_nw_energy_proxies()` |
| 25 | Equipment life math documentation | `EQUIPMENT_LIFE_MATH` | `Data/equipment life math.txt` | *reference only* |

### 🔵 External / Public — NEEA RBSA (10 sources, all 📁 FILE)

| # | Data Source | Config Constant | Path | Loader |
|---|-----------|----------------|------|--------|
| 26 | RBSA 2022 — SiteDetail | `RBSA_2022_SITE_DETAIL` | `Data/2022 RBSA Datasets/SiteDetail.csv` | `load_rbsa_site_detail()` |
| 27 | RBSA 2022 — HVAC | `RBSA_2022_HVAC` | `Data/2022 RBSA Datasets/Mechanical_HeatingAndCooling.csv` | `load_rbsa_hvac()` |
| 28 | RBSA 2022 — Water Heater | `RBSA_2022_WATER_HEATER` | `Data/2022 RBSA Datasets/Mechanical_WaterHeater.csv` | `load_rbsa_water_heater()` |
| 29 | RBSA 2022 — Stove/Oven | `RBSA_2022_STOVE_OVEN` | `Data/2022 RBSA Datasets/Appliance_Stove_Oven.csv` | *not yet loaded* |
| 30 | RBSA 2022 — Laundry | `RBSA_2022_LAUNDRY` | `Data/2022 RBSA Datasets/Appliance_Laundry.csv` | *not yet loaded* |
| 31 | RBSA 2022 — Building Shell | `RBSA_2022_BUILDING_SHELL` | `Data/2022 RBSA Datasets/Building_Shell_One_Line.csv` | *not yet loaded* |
| 32 | RBSA sub-metered data Year 1 | `RBSAM_Y1_DIR` | `Data/rbsam_y1/` | `load_rbsam_metering()` |
| 33 | RBSA sub-metered data Year 2 | `RBSAM_Y2_DIR` | `Data/rbsam_y2/` | `load_rbsam_metering()` |
| 34 | RBSA metering data dictionary | `RBSAM_DATA_DICT` | `Data/rbsa-metering-data-dictionary-2016-2017.xlsx` | *reference only* |
| 35 | 2017 RBSA-II Combined Database | `RBSA_2017_DIR` | `Data/2017-RBSA-II-Combined-Database/` | `load_rbsa_2017_site_detail()` |

### 🔵 External / Public — ASHRAE (4 sources, all 📁 FILE)

| # | Data Source | Config Constant | Path | Loader |
|---|-----------|----------------|------|--------|
| 36 | ASHRAE Service Life — Oregon | `ASHRAE_OR_SERVICE_LIFE` | `Data/ashrae/OR-ASHRAE_Service_Life_Data.xls` | `load_ashrae_service_life()` |
| 37 | ASHRAE Service Life — Washington | `ASHRAE_WA_SERVICE_LIFE` | `Data/ashrae/WA-ASHRAE_Service_Life_Data.xls` | `load_ashrae_service_life()` |
| 38 | ASHRAE Maintenance Cost — Oregon | `ASHRAE_OR_MAINTENANCE_COST` | `Data/ashrae/OR-ASHRAE_Maintenance_Cost_Data.xls` | `load_ashrae_maintenance_cost()` |
| 39 | ASHRAE Maintenance Cost — Washington | `ASHRAE_WA_MAINTENANCE_COST` | `Data/ashrae/WA-ASHRAE_Maintenance_Cost_Data.xls` | `load_ashrae_maintenance_cost()` |

### 🔵 External / Public — U.S. Census Bureau (5 sources: 4 📁 FILE + 1 🌐 API)

| # | Data Source | Config Constant | Path / Endpoint | Access | Loader |
|---|-----------|----------------|----------------|--------|--------|
| 40 | Census ACS B25034 — API | `CENSUS_API_BASE` | `https://api.census.gov/data/{year}/acs/acs5` | 🌐 API | `fetch_census_b25034()` |
| 41 | Census B25034 county files (offline) | `B25034_COUNTY_DIR` | `Data/B25034-5y-county/` | 📁 FILE | `load_b25034_county_files()` |
| 42 | Census B25040 (Heating Fuel) | `B25040_COUNTY_DIR` | `Data/B25040-5y-county/` | 📁 FILE | `load_b25040_county_files()` |
| 43 | Census B25024 (Units in Structure) | `B25024_COUNTY_DIR` | `Data/B25024-5y-county/` | 📁 FILE | `load_b25024_county_files()` |
| 44 | Census B25034 national backup | `B25034_BACKUP_DIR` | `Data/B25034-5y/` | 📁 FILE | *fallback only* |

### 🔵 External / Public — Population & Housing Forecasts (2 sources, all 📁 FILE)

| # | Data Source | Config Constant | Path | Loader |
|---|-----------|----------------|------|--------|
| 45 | PSU Population Forecasts (13 OR counties) | `PSU_PROJECTION_DIR` | `Data/PSU projection data/` | `load_psu_population_forecasts()` |
| 46 | WA OFM Housing Estimates (3 WA counties) | `OFM_HOUSING_XLSX` | `Data/ofm_april1_housing.xlsx` | `load_ofm_housing()` |

### 🔵 External / Public — NOAA Climate Normals (2 sources: 1 📁 FILE + 1 🌐 API)

| # | Data Source | Config Constant | Path / Endpoint | Access | Loader |
|---|-----------|----------------|----------------|--------|--------|
| 47 | NOAA daily/monthly normals (11 stations) | `NOAA_NORMALS_DIR` | `Data/noaa_normals/` | 📁 FILE | `load_noaa_daily_normals()`, `load_noaa_monthly_normals()` |
| 48 | NOAA CDO API | `NOAA_CDO_API_BASE` | `https://www.ncei.noaa.gov/cdo-web/api/v2` | 🌐 API | *used for initial download; normals cached locally* |

### 🔵 External / Public — EIA RECS (4 sources, all 📁 FILE)

| # | Data Source | Config Constant | Path | Loader |
|---|-----------|----------------|------|--------|
| 49 | RECS 2020 microdata | `RECS_2020_CSV` | `Data/Residential Energy Consumption Servey/recs2020_public_v7.csv` | `load_recs_microdata()` |
| 50 | RECS 2015 microdata | `RECS_2015_CSV` | `Data/Residential Energy Consumption Servey/recs2015_public_v4.csv` | `load_recs_microdata()` |
| 51 | RECS 2009 microdata | `RECS_2009_CSV` | `Data/Residential Energy Consumption Servey/2009/` | `load_recs_microdata()` |
| 52 | RECS 2005 microdata | `RECS_2005_CSV` | `Data/Residential Energy Consumption Servey/2005/` | `load_recs_microdata()` |

### 🔵 External / Public — Green Building Registry (1 source, 🌐 API)

| # | Data Source | Config Constant | Endpoint | Access | Loader |
|---|-----------|----------------|----------|--------|--------|
| 53 | Green Building Registry API | `GBR_API_BASE_URL` | `https://api.greenbuildingregistry.com` | 🌐 API | `fetch_gbr_properties()` |

### 🔵 External / Public — Microclimate: Terrain, Temperature, Wind, Asphalt & Emissions (9 sources, all 📁 FILE)

These datasets power the terrain position classifier (windward / leeward / valley / ridge), the urban heat island (UHI) correction, wind-chill simulation, and traffic heat emissions described in [MICROCLIMATE_CONVERSION.md](MICROCLIMATE_CONVERSION.md). Raster sources (LiDAR, PRISM, Landsat, NLCD) are delivered as GeoTIFFs — `rasterio` opens them and `numpy` manipulates the pixel values (e.g., converting impervious-surface percentages into effective temperature offsets, or asphalt albedo values into solar absorption heat). Vector sources (ODOT/WSDOT roads) are loaded with `geopandas`.

**Quick-reference table:**

| Data Type | Primary Source | Resolution | Best Use Case |
|-----------|---------------|-----------|---------------|
| Elevation | DOGAMI / WA DNR LiDAR | 1 meter | Modeling air drainage & wind steering |
| Temperature | PRISM / Landsat 9 | 800 m / 30 m | Mapping Urban Heat Islands & rural cooling |
| Wind | MesoWest / NREL | Point / 2 km | Simulating wind-chill & heat dispersal |
| Asphalt | NLCD | 30 meter | Calculating solar absorption (albedo) |
| Emissions | ODOT / WSDOT | Vector (roads) | Adding heat from vehicle traffic |

| # | Data Source | Config Constant | Path | Access | Loader |
|---|-----------|----------------|------|--------|--------|
| 54 | DOGAMI / WA DNR LiDAR DEM (1 m) | `LIDAR_DEM_RASTER` | `Data/terrain/lidar_dem_nwn.tif` | 📁 FILE | `load_lidar_dem()` |
| 55 | PRISM gridded temperature normals (800 m) | `PRISM_TEMP_DIR` | `Data/terrain/prism_tmean/` | 📁 FILE | `load_prism_temperature()` |
| 56 | Landsat 9 Land Surface Temperature (30 m) | `LANDSAT_LST_RASTER` | `Data/terrain/landsat9_lst_nwn.tif` | 📁 FILE | `load_landsat_lst()` |
| 57 | MesoWest station wind observations | `MESOWEST_WIND_DIR` | `Data/terrain/mesowest_wind/` | 📁 FILE | `load_mesowest_wind()` |
| 58 | NREL Wind Resource gridded data (2 km) | `NREL_WIND_RASTER` | `Data/terrain/nrel_wind_nwn.tif` | 📁 FILE | `load_nrel_wind()` |
| 59 | NLCD Impervious Surface / Asphalt (30 m) | `NLCD_IMPERVIOUS_RASTER` | `Data/terrain/nlcd_impervious_nwn.tif` | 📁 FILE | `load_nlcd_impervious()` |
| 60 | ODOT road network (Oregon) | `ODOT_ROADS_SHP` | `Data/terrain/odot_roads_oregon.shp` | 📁 FILE | `load_road_emissions()` |
| 61 | WSDOT road network (Washington) | `WSDOT_ROADS_SHP` | `Data/terrain/wsdot_roads_washington.shp` | 📁 FILE | `load_road_emissions()` |
| 62 | Derived terrain attributes (all sources combined) | `TERRAIN_ATTRIBUTES_CSV` | `Data/terrain/terrain_attributes.csv` | 📁 FILE | `load_terrain_attributes()` |

#### 54 — DOGAMI / WA DNR LiDAR DEM (1 meter)

**Purpose**: High-resolution bare-earth elevation for modeling air drainage (cold air pooling in valleys), wind steering around ridgelines, and precise windward/leeward slope classification. At 1 m resolution, individual hillsides and drainage channels are resolved — far more accurate than the 30 m USGS 3DEP product for terrain-driven microclimate work.

**Format**: GeoTIFF, float32, elevation in meters. Oregon tiles from [DOGAMI Lidar Viewer](https://gis.dogami.oregon.gov/maps/lidarviewer/); Washington tiles from [WA DNR Lidar Portal](https://lidarportal.dnr.wa.gov/). Mosaic and clip to NWN service territory bounding box before use.

**Key Derived Quantities**:
- `aspect` (0–360°): Direction the slope faces. Windward = within ±90° of 225° (SW prevailing wind). Computed from the DEM using numpy gradient.
- `slope` (degrees): Steepness. Ridges > 25°; valleys < 5°.
- `terrain_position`: Classified as `windward`, `leeward`, `valley`, or `ridge` based on aspect and elevation relative to the nearest ridgeline.
- `air_drainage_index`: Identifies low-lying areas where cold air pools overnight, increasing effective HDD.

**Config Constants**: `TERRAIN_DIR`, `LIDAR_DEM_RASTER`

**Loader**: `load_lidar_dem()` in `src/loaders/load_terrain_attributes.py`

---

#### 55 — PRISM Gridded Temperature Normals (800 m)

**Purpose**: PRISM (Parameter-elevation Regressions on Independent Slopes Model) produces spatially continuous temperature grids that already account for terrain effects — the standard reference for Pacific Northwest climate mapping. Monthly mean temperature normals (1991–2020) at 800 m resolution capture valley inversions, coastal cooling, and Gorge channeling that point stations miss.

**Format**: One GeoTIFF per month, float32, values in °C (raw values are °C × 100; divide by 100). Download from [PRISM Climate Group](https://prism.oregonstate.edu/normals/) — select "Monthly Normals", variable `tmean`, all 12 months, 800 m resolution. Free, no account required.

**Required Files**: 12 monthly files named `PRISM_tmean_30yr_normal_800mM4_{MM}_bil.bil` stored in `Data/terrain/prism_tmean/`.

**Key Columns** (after loading):
- `month` (int): 1–12
- `tmean_c` (float): Monthly mean temperature (°C)
- `hdd_contribution` (float): Heating degree days contributed by this month (base 65°F)

**Usage**: Compute a full annual HDD grid independent of point weather stations. Each monthly mean is multiplied by the number of days in that month to produce monthly HDD, then summed to annual HDD. Provides a spatially continuous alternative to the 11-station `DISTRICT_WEATHER_MAP` for sub-district microclimate refinement.

**Config Constant**: `PRISM_TEMP_DIR`

**Loader**: `load_prism_temperature()` in `src/loaders/load_terrain_attributes.py`

---

#### 56 — Landsat 9 Land Surface Temperature (30 m)

**Purpose**: Landsat 9 Band 10 (thermal infrared) provides actual land surface temperature (LST) at 30 m resolution, directly measuring the heat emitted by asphalt, rooftops, and bare soil. Downtown Portland's asphalt surfaces reach 120–140°F on summer afternoons while nearby parks stay 20–30°F cooler. Used to validate and calibrate the NLCD-derived UHI offsets.

**Format**: GeoTIFF, float32, raw digital number values. Apply the Landsat Collection 2 scale factor (`LST_K = pixel × 0.00341802 + 149.0`) to convert to Kelvin, then subtract 273.15 for Celsius. Download from [USGS EarthExplorer](https://earthexplorer.usgs.gov/) — Landsat Collection 2 Level-2, Band ST_B10. Choose cloud-free summer scenes (July–August) for maximum UHI signal. Fill pixels (values < 150 K after scaling) should be treated as missing.

**Key Columns** (after loading):
- `lst_celsius` (float): Land surface temperature (°C)
- `uhi_intensity_c` (float): LST minus rural background temperature — positive values indicate urban warming

**Usage**: Compare LST in urban pixels against rural/forested pixels to empirically measure UHI magnitude for Portland, Salem, and Eugene. Cross-validates the albedo-based UHI estimates derived from NLCD.

**Config Constant**: `LANDSAT_LST_RASTER`

**Loader**: `load_landsat_lst()` in `src/loaders/load_terrain_attributes.py`

---

#### 57 — MesoWest Station Wind Observations

**Purpose**: MesoWest aggregates real-time and historical wind speed/direction from hundreds of surface stations across the Pacific Northwest, including non-NWS sites (fire weather, agricultural, highway sensors). Used to validate wind patterns and calibrate windward/leeward HDD multipliers against observed wind-chill effects.

**Format**: CSV per station with columns `date_time`, `wind_speed_ms`, `wind_direction_deg`, `station_id`, `latitude`, `longitude`, `elevation_m`. Download via [MesoWest / Synoptic API](https://developers.synopticdata.com/mesonet/) — free tier available, requires API token. Store downloaded CSVs in `Data/terrain/mesowest_wind/`.

**Key Columns** (after aggregation):
- `station_id` (str): Station identifier
- `mean_wind_ms` (float): Annual mean wind speed (m/s)
- `p90_wind_ms` (float): 90th percentile wind speed (m/s) — captures peak infiltration events
- `lat`, `lon` (float): Station coordinates

**Usage**: Each 1 m/s of mean wind speed above 3 m/s (typical sheltered suburban baseline) adds approximately 1.5% to the effective heating load through increased envelope infiltration. Stations in the Columbia River Gorge corridor (KDLS area) and coastal headlands show persistently elevated wind speeds that justify higher HDD multipliers.

**Config Constant**: `MESOWEST_WIND_DIR`

**Loader**: `load_mesowest_wind()` in `src/loaders/load_terrain_attributes.py`

---

#### 58 — NREL Wind Resource Gridded Data (2 km)

**Purpose**: Spatially continuous annual mean wind speed at 2 km resolution. Fills gaps where MesoWest has sparse station coverage (rural eastern Oregon, Skamania County) and captures terrain channeling effects like the Columbia River Gorge acceleration zone.

**Format**: GeoTIFF, float32, wind speed in m/s at 80 m hub height. Download from [NREL Wind Prospector](https://maps.nrel.gov/wind-prospector/) or the [NREL Data Catalog](https://data.nrel.gov/). Values are scaled from 80 m to 10 m surface wind using a log-law correction (divide by approximately 1.3 for typical PNW surface roughness).

**Key Columns** (after loading):
- `wind_speed_10m_ms` (float): Annual mean wind speed at 10 m surface height (m/s)

**Usage**: Used where MesoWest station density is insufficient. Combined with MesoWest observations to produce a spatially complete wind speed surface for the NWN service territory.

**Config Constant**: `NREL_WIND_RASTER`

**Loader**: `load_nrel_wind()` in `src/loaders/load_terrain_attributes.py`

---

#### 59 — NLCD Impervious Surface / Asphalt (30 m)

**Purpose**: Quantifies the fraction of each 30 m cell covered by impervious surfaces (roads, parking lots, rooftops). Higher impervious fraction means lower surface albedo, more solar absorption, stronger urban heat island, and fewer effective HDD. Pixel values are integers 0–100 representing percent impervious cover.

**Format**: GeoTIFF, uint8, values 0–100. Projected in Albers Equal Area (EPSG:5070); reproject to match LiDAR DEM CRS before combining. Sentinel values above 100 (e.g., 127 in some releases) indicate no data and should be treated as missing. Download from [MRLC.gov](https://www.mrlc.gov/data) — "NLCD Impervious Surface", 2021, Pacific Northwest region. Free, no account required.

**Albedo conversion**: Asphalt albedo ≈ 0.05 (absorbs 95% of incoming solar radiation) vs. vegetated land ≈ 0.20. The impervious fraction is used to blend these two albedo values. Lower blended albedo → more absorbed solar energy → higher surface temperature → UHI warming → HDD reduction.

**Key Columns** (after loading):
- `impervious_pct` (float): Percent impervious cover (0–100)
- `surface_albedo` (float): Blended effective albedo (0.05–0.20)
- `uhi_offset_f` (float): Estimated UHI temperature offset (°F) above rural baseline
- `hdd_reduction` (float): Annual HDD reduction from UHI warming

**Practical impact reference**:

| Land use | Impervious % | Albedo | UHI offset | HDD reduction |
|----------|-------------|--------|-----------|---------------|
| Dense urban core (downtown Portland) | 85% | 0.07 | ~3.4°F | ~612 HDD (−12.6%) |
| Urban residential (inner SE Portland) | 55% | 0.12 | ~2.2°F | ~396 HDD (−8.2%) |
| Suburban (Beaverton, Gresham) | 40% | 0.14 | ~1.6°F | ~288 HDD (−5.9%) |
| Small city / town center | 30% | 0.16 | ~1.2°F | ~216 HDD (−4.5%) |
| Rural / agricultural | 8% | 0.19 | ~0.3°F | ~54 HDD (−1.1%) |

**Config Constant**: `NLCD_IMPERVIOUS_RASTER`

**Loader**: `load_nlcd_impervious()` in `src/loaders/load_terrain_attributes.py`

---

#### 60 & 61 — ODOT / WSDOT Road Networks (Vector)

**Purpose**: Vehicle traffic generates waste heat through engine exhaust, brake friction, and tire-road friction. In high-traffic corridors (I-5, I-84, US-26), this adds a measurable sensible heat flux to the urban boundary layer — typically 5–20 W/m² along major arterials. Road network data from ODOT (Oregon) and WSDOT (Washington) provides the geometry and traffic volume attributes needed to estimate this heat contribution.

**Format**: Shapefile or GeoJSON, line geometry. Key attributes: `AADT` (Annual Average Daily Traffic, vehicles/day), `road_class` (Interstate, US Highway, State Route, Local), `lanes`, `speed_limit_mph`. Rows with missing AADT are excluded.

**Download**:
- Oregon: [ODOT GIS Data](https://www.oregon.gov/odot/data/pages/gis.aspx) — "Oregon Road Network" shapefile. Free.
- Washington: [WSDOT GIS Open Data](https://gisdata-wsdot.opendata.arcgis.com/) — "All Roads" layer. Free.

**Key Columns** (after loading):
- `AADT` (float): Annual Average Daily Traffic (vehicles/day)
- `road_class` (str): Road classification
- `heat_flux_wm2` (float): Estimated sensible heat flux from traffic (W/m²)
- `temp_offset_f` (float): Estimated air temperature offset from traffic heat (°F)

**Usage**: Each vehicle dissipates approximately 150 kJ/km as waste heat. I-5 through Portland (~150,000 vehicles/day) produces roughly 8 W/m² of road surface heat flux, contributing ~0.1–0.3°F to local air temperature. This is modest individually but additive with asphalt albedo and building HVAC effects in the urban core.

**Config Constants**: `ODOT_ROADS_SHP`, `WSDOT_ROADS_SHP`

**Loader**: `load_road_emissions()` in `src/loaders/load_terrain_attributes.py`

---

#### 62 — Derived Terrain Attributes CSV

**Purpose**: A pre-computed lookup table combining all five microclimate data types into a single flat CSV, so the simulation pipeline does not re-sample rasters or query APIs at runtime. Generated once from all source rasters using `src/loaders/load_terrain_attributes.py` and stored in `Data/terrain/`.

**Format**: CSV with one row per geographic unit (IRP district or Census block group).

**Required Columns**:

| Column | Source | Type | Description |
|--------|--------|------|-------------|
| `geo_id` | — | str | District code or Census block group GEOID |
| `mean_elevation_ft` | LiDAR | float | Mean elevation of premises in this unit (feet) |
| `dominant_aspect_deg` | LiDAR | float | Modal terrain aspect (0–360°, 225° = SW prevailing wind) |
| `terrain_position` | LiDAR | str | `windward`, `leeward`, `valley`, or `ridge` |
| `mean_wind_ms` | MesoWest / NREL | float | Mean annual surface wind speed (m/s) |
| `wind_infiltration_mult` | MesoWest / NREL | float | HDD multiplier from wind-driven infiltration |
| `prism_annual_hdd` | PRISM | float | PRISM-derived annual HDD (°F-days, base 65°F) |
| `lst_summer_c` | Landsat 9 | float | Mean summer land surface temperature (°C) |
| `mean_impervious_pct` | NLCD | float | Mean impervious surface % across the unit |
| `surface_albedo` | NLCD | float | Effective blended surface albedo (0–1) |
| `uhi_offset_f` | NLCD + Landsat | float | UHI temperature offset above rural baseline (°F) |
| `road_heat_flux_wm2` | ODOT / WSDOT | float | Traffic waste heat flux (W/m²) |
| `road_temp_offset_f` | ODOT / WSDOT | float | Air temperature offset from traffic heat (°F) |
| `hdd_terrain_mult` | LiDAR | float | HDD multiplier from terrain position (e.g., 1.07 for windward) |
| `hdd_elev_addition` | LiDAR | float | HDD addition from elevation lapse rate above station |
| `hdd_uhi_reduction` | NLCD + Landsat | float | HDD reduction from UHI warming |
| `effective_hdd` | All sources | float | Final adjusted HDD used in simulation |

**Config Constant**: `TERRAIN_ATTRIBUTES_CSV`

**Loader**: `load_terrain_attributes()` in `src/loaders/load_terrain_attributes.py`

---

### Totals

| Category | Count | 📁 File | 🌐 API |
|----------|-------|---------|--------|
| 🟢 NW Natural (proprietary) | 15 | 15 | 0 |
| 🟡 Team-created (from NWN docs) | 10 | 10 | 0 |
| 🔵 External / Public | 36 | 33 | 3 |
| **Total** | **61** | **58** | **3** |

> API sources requiring runtime credentials: Census ACS B25034 (no key needed), NOAA CDO (`NOAA_CDO_TOKEN`), Green Building Registry (`GBR_API_KEY`). All other sources are local files on disk.
> Microclimate rasters (sources 54–59) are large files (500 MB – 2 GB each for full Pacific Northwest coverage). Clip to the NWN service territory bounding box before committing to the repo or sharing with the team.
