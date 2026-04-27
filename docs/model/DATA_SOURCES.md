# Data Sources

## Overview

The model ingests data from 30+ sources across four categories: NW Natural proprietary data, external building stock surveys, public demographic and housing data, and climate/weather data. This document describes each source, what it contributes to the model, and where it lives on disk.

All data lives under `Data/`. NW Natural proprietary data is blinded (customer identifiers anonymized). Each source has a dedicated loader in `src/loaders/` that can be run standalone for debugging.

---

## Category 1: NW Natural Proprietary Data

These files are supplied by NW Natural and contain blinded/anonymized customer data. They are not committed to source control.

**Directory**: `Data/NWNatural Data/`

| File | Loader | What It Provides |
|------|--------|-----------------|
| `premise_data_blinded.csv` | `load_premise_data.py` | One row per active premise: `blinded_id`, `district_code_IRP`, `service_state`, `custtype`, `status_code`. Filtered to `custtype='R'`, `status_code='AC'` (~213K premises). |
| `equipment_data_blinded.csv` | `load_equipment_data.py` | One row per equipment record: `blinded_id`, `equipment_type_code`, `QTY_OF_EQUIPMENT_TYPE`. ~247K records across all premises. |
| `equipment_codes.csv` | `load_equipment_codes.py` | Lookup table mapping `equipment_type_code` to `equipment_class` and description. Used to derive `end_use` via `END_USE_MAP`. |
| `segment_data_blinded.csv` | `load_segment_data.py` | One row per premise: `blinded_id`, `segment` (RESSF/RESMF/MOBILE), `subseg`, `mktseg`, `set_year`. Provides construction vintage and housing type. |
| `DailyCalDay1985_Mar2025.csv` | `load_weather_data.py` | Daily weather data for 11 NW Natural weather stations, 1985–March 2025. Columns: `SiteId`, `Date`, `TempHA` (daily avg temp °F). Used to compute HDD. |
| `DailyGasDay2008_Mar2025.csv` | `load_weather_data.py` | Alternative weather file in gas-day format (same stations, 2008–2025). Used as fallback or for gas-day analysis. |
| `BullRunWaterTemperature.csv` | `load_water_temperature.py` | Daily Bull Run reservoir water temperature (°F). Used for water heating delta-T calculation (future work). |
| `Portland_snow.csv` | `load_snow_data.py` | Daily snowfall and snow depth for Portland, 1985–2025. Used for peak day identification and weather severity analysis. |
| `billing_data_blinded.csv` | `load_billing_data.py` | Historical billing records: `blinded_id`, `GL_revenue_date`, `utility_usage` (therms), `rate_schedule`. ~48M records. Used for calibration. |
| `small_billing_data_blinded.csv` | `load_billing_data.py` | Smaller subset of billing data for development/testing. |

---

## Category 2: Tariff and Rate Data

Team-created files reconstructing NW Natural's historical rate schedules.

**Directory**: `Data/`

| File | Loader | What It Provides |
|------|--------|-----------------|
| `or_rates_oct_2025.csv` | `load_or_rates.py` | Oregon current rate schedule. Schedule 2 residential = $1.41220/therm. |
| `wa_rates_nov_2025.csv` | `load_wa_rates.py` | Washington current rate schedule. Schedule 2 residential = $1.24164/therm. |
| `or_wacog_history.csv` | `load_wacog_history.py` | Oregon Weighted Average Cost of Gas history, 2018–2025. Annual and winter WACOG rates. |
| `wa_wacog_history.csv` | `load_wacog_history.py` | Washington WACOG history, 2018–2025. |
| `or_rate_case_history.csv` | `load_rate_case_history.py` | Oregon rate case history. Used to reconstruct historical base distribution rates. |
| `wa_rate_case_history.csv` | `load_rate_case_history.py` | Washington rate case history. |

---

## Category 3: Building Stock and Equipment Data

External surveys providing building characteristics and equipment distributions for the Pacific Northwest.

### NEEA RBSA 2022

**Directory**: `Data/2022 RBSA Datasets/`

The 2022 Residential Building Stock Assessment from the Northwest Energy Efficiency Alliance (NEEA) provides building characteristics for ~1,500 Pacific Northwest homes.

| File | Loader | What It Provides |
|------|--------|-----------------|
| `SiteDetail.csv` | `load_rbsa_site_detail.py` | Site-level building characteristics: square footage, year built, structure type, climate zone. |
| `Mechanical_HeatingAndCooling.csv` | `load_rbsa_hvac.py` | HVAC equipment: type, fuel, efficiency, age. Used to validate equipment efficiency assumptions. |
| `Mechanical_WaterHeater.csv` | `load_rbsa_water_heater.py` | Water heater equipment: type, fuel, efficiency, age. |
| `Appliance_Stove_Oven.csv` | (reference) | Cooking appliance data. |
| `Appliance_Laundry.csv` | (reference) | Clothes dryer data. |
| `Building_Shell_One_Line.csv` | (reference) | Building envelope summary: insulation levels, window type, air leakage. |

`load_rbsa_distributions.py` combines site_detail + hvac + water_heater into weighted distributions of building characteristics by type and vintage.

### NEEA RBSA 2017

**Directory**: `Data/2017-RBSA-II-Combined-Database/`

Earlier vintage of the RBSA (43 CSV files). Provides a temporal comparison point for tracking building stock evolution between 2017 and 2022.

| Loader | What It Provides |
|--------|-----------------|
| `load_rbsa_2017.py` | 2017 RBSA-II SiteDetail.csv for temporal comparison. |

### ASHRAE Equipment Service Life

**Directory**: `Data/ashrae/`

ASHRAE public database exports providing empirically grounded equipment median service life and maintenance costs by equipment type, state-specific for Oregon and Washington.

| File | Loader | What It Provides |
|------|--------|-----------------|
| `OR-ASHRAE_Service_Life_Data.xls` | `load_ashrae_service_life.py` | Median service life (years) by equipment type for Oregon. Replaces `USEFUL_LIFE` defaults in config. |
| `WA-ASHRAE_Service_Life_Data.xls` | `load_ashrae_service_life.py` | Median service life (years) by equipment type for Washington. |
| `OR-ASHRAE_Maintenance_Cost_Data.xls` | `load_ashrae_maintenance_cost.py` | Annual maintenance cost by equipment type for Oregon. |
| `WA-ASHRAE_Maintenance_Cost_Data.xls` | `load_ashrae_maintenance_cost.py` | Annual maintenance cost by equipment type for Washington. |

`load_useful_life_table.py` combines OR and WA service life data into a state-specific lookup table used by the equipment inventory builder.

---

## Category 4: IRP Calibration and Validation Data

NW Natural's IRP load decay data and companion files used for model calibration and validation.

**Directory**: `Data/`

| File | Loader | What It Provides |
|------|--------|-----------------|
| `10-Year Load Decay Forecast (2025–2035).csv` | `load_load_decay_forecast.py` | NW Natural's official IRP UPC forecast: 648 therms baseline declining at −1.19%/yr through 2035. Primary validation target. |
| `prior load decay data reconstructed.txt` | `load_historical_upc.py` | Historical UPC by year back to 2005 (835 → 648 therms). Three-era framework calibration anchors. |
| `prior load decay data simulated.txt` | `load_historical_upc.py` | Year-by-year UPC multipliers vs 2025 baseline. |
| `prior load decay data description.txt` | (reference) | Three-era framework documentation: pre-2010 (~820 therms, 80% AFUE), 2011–2019 (~720 therms, 90%+ AFUE), 2020+ (~650 therms, heat pump hybrids). |
| `Baseload Consumption Factors.csv` | `load_baseload_factors.py` | Structured parameter table: cooking (30 therms/yr), drying (20 therms/yr), fireplace (55 therms/yr), pilot light loads, water heater standby losses by vintage. |
| `nw_energy_proxies.csv` | `load_nw_energy_proxies.py` | Compact parameter set: building envelope UA values by vintage era, Weibull parameters, baseload factors. |
| `building_envelope_efficiency_index.csv` | (reference) | Building envelope efficiency index by vintage era and construction type. |
| `segment_heating_multipliers.csv` | (reference) | Segment-based heating multipliers (SF vs MF). |
| `equipment_afue_trajectory.csv` | (reference) | Historical and projected AFUE trajectory for new equipment. |

---

## Category 5: Census ACS Housing Data

U.S. Census Bureau American Community Survey data for all 16 NW Natural service territory counties (13 Oregon, 3 Washington).

**Directory**: `Data/B25034-5y-county/`, `Data/B25040-5y-county/`, `Data/B25024-5y-county/`

| Table | Loader | What It Provides |
|-------|--------|-----------------|
| B25034 (Year Structure Built) | `load_b25034_county.py` | County-level housing unit counts by decade of construction (2020+, 2010–2019, ..., pre-1939). 2009–2023, ACS 5-year. Validates model vintage distribution. |
| B25040 (House Heating Fuel) | `load_b25040_county.py` | County-level counts by primary heating fuel: utility gas, electricity, propane, wood, etc. 2009–2023. Tracks gas market share over time. |
| B25024 (Units in Structure) | `load_b25024_county.py` | County-level counts by structure type: 1-unit detached, 1-unit attached, 2–4 units, 5–9, 10–19, 20–49, 50+, mobile home. 2009–2023. Validates SF/MF split and drives segment shift projection. |

`load_service_territory_fips.py` loads `NW Natural Service Territory Census data.csv` which maps the 16 service territory counties to their Census FIPS codes.

`load_census_b25034.py` provides a live Census API fetch for the most current data (no API key required).

---

## Category 6: Population and Housing Growth Forecasts

Official population and housing forecasts used to calibrate the `housing_growth_rate` scenario parameter.

| Source | Loader | What It Provides |
|--------|--------|-----------------|
| PSU Population Research Center | `load_psu_forecasts.py` | Official Oregon county-level population forecasts (mandated by state law). Covers all 13 NW Natural Oregon counties. Three CSV format variants across 2023/2024/2025 releases. Forecasts to 2074–2075. |
| WA OFM April 1 Housing Estimates | `load_ofm_housing.py` | Washington State Office of Financial Management postcensal housing unit estimates for Clark, Skamania, and Klickitat counties. 2020–2025. Provides structure-type breakdown (one-unit, multi-unit, mobile home). |

**Directory**: `Data/PSU projection data/`, `Data/ofm_april1_housing.xlsx`

---

## Category 7: Climate and Weather Reference Data

### NOAA 30-Year Climate Normals

**Directory**: `Data/noaa_normals/`

NOAA Climate Normals (1991–2020 period) for all 11 NW Natural weather stations. Downloaded via the NOAA CDO API.

| File Pattern | Loader | What It Provides |
|-------------|--------|-----------------|
| `{ICAO}_daily_normals.csv` | `load_noaa_normals.py` | 365 rows per station: date, avg/max/min temp, HDD, CDD. Used for weather normalization. |
| `{ICAO}_monthly_normals.csv` | `load_noaa_normals.py` | 12 rows per station: monthly avg/max/min temp, HDD, CDD. |

Stations: KPDX, KEUG, KSLE, KAST, KDLS, KOTH, KONP, KCVO, KHIO, KTTD, KVUO.

`compute_weather_adjustment(actual_hdd, normal_hdd)` returns the ratio of actual to normal HDD for a given station and year.

---

## Category 8: EIA RECS Microdata

**Directory**: `Data/Residential Energy Consumption Survey/`

Energy Information Administration Residential Energy Consumption Survey microdata. Used to compute end-use share benchmarks for Pacific division gas-heated homes.

| File | Loader | Survey Year | Geography |
|------|--------|-------------|-----------|
| `recs2020_public_v7.csv` | `load_recs_microdata.py` | 2020 | State-level (OR/WA filterable) |
| `recs2015_public_v4.csv` | `load_recs_microdata.py` | 2015 | Division-level only |
| `2009/recs2009_public.csv` | `load_recs_microdata.py` | 2009 | Division-level only |
| `2005/RECS05alldata.csv` | `load_recs_microdata.py` | 2005 | Division-level only |

`build_recs_enduse_benchmarks()` computes weighted-average gas consumption by end-use for Pacific division (Division 9) gas-heated homes (`FUELHEAT=1`), using `NWEIGHT` for population-level estimates.

---

## Running Individual Loaders

Every loader can be run standalone for debugging:

```bash
python -m src.loaders.load_premise_data
python -m src.loaders.load_weather_data
python -m src.loaders.load_b25024_county
python -m src.loaders.load_recs_microdata
# etc.
```

Each standalone run:
1. Loads the data
2. Prints a summary to console (row count, column names, sample rows)
3. Saves diagnostic output to `output/loaders/{loader_name}_summary.txt` and `{loader_name}_sample.csv`

---

## Data Quality Reports

After loading, the validation suite generates quality reports for each loader:

- `output/data_quality/{loader_name}_quality_report.html` — row count, dtypes, null counts, value distributions
- `output/data_quality/join_audit.html` — cross-loader match rates (premise vs equipment vs segment vs billing)
- `output/join_integrity/join_integrity_dashboard.html` — pass/fail dashboard for end-use mapping, efficiency validity, weather station assignment

---

## Related Documentation

- **[CENSUS_RECS_INTEGRATION.md](CENSUS_RECS_INTEGRATION.md)** — How Census and RECS data are used in the model
- **[CALIBRATION.md](CALIBRATION.md)** — How IRP load decay data is used for calibration
- **[ALGORITHM.md](ALGORITHM.md)** — How data sources feed into the simulation pipeline
