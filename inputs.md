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
9. **Scenario configuration**: User-defined parameters for projection runs

All inputs are organized by source provenance in the `Data/` directory and are documented in the design.md and tasks.md files.
