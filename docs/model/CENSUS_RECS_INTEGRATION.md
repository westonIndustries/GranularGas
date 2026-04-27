# Census and RECS Integration

## Overview

The model integrates two major external data sources — U.S. Census ACS housing data and EIA RECS microdata — to ground the housing stock and end-use estimates in independent, publicly available benchmarks. Census data validates and informs the housing stock model. RECS data provides end-use share benchmarks for estimating total UPC when only space heating is simulated.

---

## Census ACS Integration

### Why Census Data?

NW Natural's premise data covers only gas customers. To understand the full housing market — including homes that use electricity or other fuels for heating — the model uses Census ACS data for the 16 counties in NW Natural's service territory.

Three ACS tables are used:

| Table | Topic | Key Use |
|-------|-------|---------|
| B25024 (Units in Structure) | SF vs MF housing | Validate segment split; project SF→MF shift |
| B25034 (Year Structure Built) | Housing vintage | Validate vintage distribution |
| B25040 (House Heating Fuel) | Heating fuel type | Track gas market share; calibrate `initial_gas_pct` |

All three tables use ACS 5-year estimates for 2009–2023, covering all 16 NW Natural service territory counties regardless of population size.

### Service Territory Counties

The 16 counties are identified by FIPS codes in `Data/NW Natural Service Territory Census data.csv`:

| State | Counties |
|-------|---------|
| Oregon (13) | Multnomah, Washington, Clackamas, Lane, Marion, Yamhill, Polk, Benton, Linn, Columbia, Clatsop, Lincoln, Coos |
| Washington (3) | Clark, Skamania, Klickitat |

---

### B25024: Units in Structure (SF/MF Split)

**File location**: `Data/B25024-5y-county/B25024_acs5_{year}.csv` (2009–2023)

**Loader**: `src/loaders/load_b25024_county.py`

**What it contains**: County-level counts of housing units by structure type:
- 1-unit detached (maps to RESSF)
- 1-unit attached (maps to RESSF)
- 2 units (maps to RESMF)
- 3–4 units (maps to RESMF)
- 5–9 units (maps to RESMF)
- 10–19 units (maps to RESMF)
- 20–49 units (maps to RESMF)
- 50+ units (maps to RESMF)
- Mobile home (maps to MOBILE)

**How it's used**:

1. **Validate segment split**: Compare the model's RESSF/RESMF/MOBILE ratio against Census B25024 proportions for the same counties. Discrepancies > 10% are flagged as warnings.

2. **Project SF→MF segment shift**: The 2009–2023 time series shows a long-run trend toward more multi-family construction. `compute_segment_shift_rates()` fits a linear trend to the SF and MF shares over time, producing annual percentage-point shift rates:
   - `sf_annual_pp` ≈ −0.064 pp/yr (SF share declining)
   - `mf_annual_pp` ≈ +0.142 pp/yr (MF share increasing)

   These rates are applied in `project_segment_shares()` to project the SF/MF split forward over the forecast horizon.

**Integration point**: `src/census_integration.py`
- `load_b25024_segment_trend()` — loads the time series
- `compute_segment_shift_rates()` — fits the trend
- `project_segment_shares(base_sf_pct, base_mf_pct, shift_rates, horizon)` — projects forward

---

### B25034: Year Structure Built (Vintage Distribution)

**File location**: `Data/B25034-5y-county/B25034_acs5_{year}.csv` (2009–2023)

**Loader**: `src/loaders/load_b25034_county.py`

**What it contains**: County-level housing unit counts by decade of construction:
- 2020 or later
- 2010–2019
- 2000–2009
- 1990–1999
- 1980–1989
- 1970–1979
- 1960–1969
- 1950–1959
- 1940–1949
- 1939 or earlier

**How it's used**:

1. **Validate vintage distribution**: Compare the model's vintage mix (derived from `set_year` in NW Natural segment data) against Census B25034 proportions. The model's pre-1980 share should roughly match the Census pre-1980 share for the same counties.

2. **Inform new construction volume**: The year-over-year change in the 2010–2019 and 2020+ bins provides an independent estimate of new construction volume, which can inform the `housing_growth_rate` scenario parameter.

**Integration point**: `src/loaders/load_census_b25034.py`
- `fetch_census_b25034()` — live Census API fetch (no API key required)
- `build_vintage_distribution()` — converts raw counts to percentage distributions

---

### B25040: House Heating Fuel (Gas Market Share)

**File location**: `Data/B25040-5y-county/B25040_acs5_{year}.csv` (2009–2023)

**Loader**: `src/loaders/load_b25040_county.py`

**What it contains**: County-level counts of occupied housing units by primary heating fuel:
- Utility gas
- Bottled/tank/LP gas
- Electricity
- Fuel oil/kerosene
- Coal/coke
- Wood
- Solar energy
- Other fuel
- No fuel used

**How it's used**:

1. **Track gas market share**: The utility gas share (`B25040_002E / B25040_001E`) by county and year shows how gas heating penetration has changed from 2009 to 2023. This is a direct measure of the electrification trend already underway.

2. **Calibrate `initial_gas_pct`**: The `initial_gas_pct` scenario parameter represents the fraction of all housing units (gas + non-gas) that use natural gas. B25040 provides the empirical basis for this parameter. For NW Natural's service territory, the gas share is approximately 70–80% depending on county.

3. **Validate electrification scenario assumptions**: If the model projects 2% of replacements electrifying per year, the resulting gas share decline should be consistent with the historical B25040 trend.

**Integration point**: `src/census_integration.py`
- `load_census_distributions()` — loads all three Census tables into a dict
- `enrich_premise_equipment()` — adds Census-derived attributes to the premise-equipment table

---

### Census Summary Output

Each scenario exports Census summary CSVs to the scenario output folder:

- `census_summary_b25024.csv` — SF/MF/mobile share by county and year
- `census_summary_b25034.csv` — vintage distribution by county and year
- `census_summary_b25040.csv` — heating fuel share by county and year

These are reference files for analysts who want to compare model assumptions against Census data directly.

---

## RECS Integration

### Why RECS Data?

The model currently simulates space heating only. But NW Natural's IRP forecast covers all residential end-uses (space heating + water heating + cooking + drying + fireplaces + other). To produce a total UPC estimate comparable to the IRP, the model uses EIA RECS data to estimate the non-heating end-uses as a ratio of space heating.

### Data Source

**EIA Residential Energy Consumption Survey (RECS)** — nationally representative household-level microdata with modeled natural gas consumption disaggregated by end use.

| Survey Year | File | Geography | Key NG Columns |
|-------------|------|-----------|----------------|
| 2020 | `recs2020_public_v7.csv` | State-level (OR/WA filterable) | `BTUNGSPH`, `BTUNGWTH`, `BTUNGCOK`, `BTUNGCDR`, `BTUNGNEC`, `BTUNGOTH` |
| 2015 | `recs2015_public_v4.csv` | Division-level only | Same columns |
| 2009 | `2009/recs2009_public.csv` | Division-level only | `BTUNGSPH`, `BTUNGWTH`, `BTUNGOTH` |
| 2005 | `2005/RECS05alldata.csv` | Division-level only | `BTUNGSPH`, `BTUNGWTH`, `BTUNGAPL` |

**Filter**: Pacific division (`DIVISION = 9`), utility gas heating (`FUELHEAT = 1`).

**Weights**: `NWEIGHT` (primary survey weight) is used for all population-level estimates.

### End-Use Ratios

`build_recs_enduse_benchmarks()` computes weighted-average gas consumption by end-use for Pacific division gas-heated homes, then expresses each non-heating end-use as a ratio to space heating:

| End-Use | Ratio to Space Heating | Source |
|---------|----------------------|--------|
| Water Heating | 0.704 | RECS 2009/2015/2020 weighted |
| Cooking | 0.055 | RECS 2015/2020 |
| Clothes Drying | 0.034 | RECS 2015/2020 |
| Fireplace | 0.085 | RECS 2020 |
| Other | 0.131 | RECS 2020 |
| **Sum** | **1.009** | |

This means total residential gas consumption is approximately 2.009× space heating consumption for Pacific division gas-heated homes.

### Applying RECS Ratios

When `use_recs_ratios=true` in the scenario config:

```
estimated_total_upc(y) = space_heating_upc(y) × (1 + 0.704 + 0.055 + 0.034 + 0.085 + 0.131)
                       = space_heating_upc(y) × 2.009
```

This produces an `estimated_total_upc.csv` alongside the space-heating-only results, allowing direct comparison against the IRP's all-end-use forecast.

### Limitations of RECS Ratios

1. **Pacific division includes California**: California has a milder climate (lower space heating share) and different cooking/water heating patterns than Oregon/Washington. This inflates the non-heating-to-space-heating ratio, making the estimated total UPC higher than NW Natural's actual all-end-use UPC.

2. **Ratios are static**: The RECS ratios don't change over the forecast horizon. In reality, water heating electrification (heat pump water heaters) would reduce the water heating ratio over time.

3. **No vintage stratification**: The ratios are fleet averages. Older homes have higher water heater standby losses; newer homes have lower pilot light loads. These differences are not captured.

These limitations are why the estimated total UPC is 21–26% higher than the IRP forecast. See [MODEL_VS_IRP_COMPARISON.md](MODEL_VS_IRP_COMPARISON.md) for a full discussion.

### RECS Trend Analysis

`load_recs_enduse_trend()` loads all four survey years and computes end-use shares over time (1993–2020). This trend shows:
- Space heating share declining from ~65% (2005) to ~60% (2020) as water heating and other end-uses grow
- Cooking and drying shares relatively stable
- Fireplace share growing slightly as gas fireplaces became more common

The trend is exported to `recs_summary.csv` in each scenario output folder.

---

## Integration Module

All Census and RECS integration is handled by two modules:

**`src/census_integration.py`**:
- `load_census_distributions()` — loads B25024, B25034, B25040 into a dict
- `enrich_premise_equipment(premise_equipment, census)` — adds Census-derived attributes
- `export_census_summary(census, output_dir)` — writes summary CSVs
- `load_b25024_segment_trend()` — loads B25024 time series
- `compute_segment_shift_rates(b25024_trend)` — fits SF/MF trend
- `project_segment_shares(base_sf_pct, base_mf_pct, shift_rates, horizon)` — projects forward

**`src/recs_integration.py`**:
- `load_recs_enduse_trend()` — loads RECS microdata for 2005/2009/2015/2020
- `compute_non_heating_ratios(recs_trend)` — computes non-heating ratios
- `export_recs_summary(recs_trend, output_dir)` — writes RECS summary CSV

---

## Related Documentation

- **[HOUSING_STOCK.md](HOUSING_STOCK.md)** — How Census B25024 drives segment shift projection
- **[DATA_SOURCES.md](DATA_SOURCES.md)** — File locations and loader details
- **[MODEL_VS_IRP_COMPARISON.md](MODEL_VS_IRP_COMPARISON.md)** — Why RECS ratios cause the model to be higher than the IRP
- **[FORMULAS.md](FORMULAS.md)** — RECS ratio formula for estimated total UPC
