# Future Work: Monthly and Daily Temporal Resolution

## Overview

The current simulation engine computes **annual therms per premise per end-use** for each year in the forecast horizon. Daily weather data (1985–2025) is summed to annual HDD before entering the simulation, discarding all sub-annual granularity. This document describes how to extend the engine to produce **month-by-month** and optionally **day-by-day** demand projections.

Monthly resolution is the practical target — it aligns with billing cycles, captures seasonal demand patterns, and enables comparison against monthly billing data. Daily resolution is a further enhancement for peak-day analysis and load shape modeling.

---

## Current Engine: What It Does Today

```
For each year in [base_year .. base_year + forecast_horizon]:
    For each premise:
        annual_hdd = sum(daily_hdd for all 365 days)
        space_heating_therms = (annual_hdd × heating_factor) / efficiency
        water_heating_therms = (gallons/day × 8.34 × delta_t × 365) / (eff × 100,000)
        baseload_therms = flat_annual_consumption / efficiency
```

Output: one row per premise per end-use per year.

**What's lost**: seasonal peaks (January heating vs. July), monthly billing validation, peak-day demand, load shape profiles.

---

## Target: Monthly Resolution

### Architecture Change

```
For each year in [base_year .. base_year + forecast_horizon]:
    For each month (1..12):
        For each premise:
            monthly_hdd = sum(daily_hdd for days in this month)
            space_heating_therms = (monthly_hdd × heating_factor) / efficiency
            water_heating_therms = (gallons/day × 8.34 × monthly_delta_t × days_in_month) / (eff × 100,000)
            baseload_therms = (annual_consumption × monthly_load_shape[month]) / efficiency
```

Output: one row per premise per end-use per month per year.

### What Needs to Change

#### 1. Weather Processing (`src/weather.py`)

**Current**: `compute_annual_hdd(weather_data, station, year)` → single float

**Needed**: `compute_monthly_hdd(weather_data, station, year)` → dict of 12 floats

```python
def compute_monthly_hdd(weather_data: pd.DataFrame, station: str, year: int) -> Dict[int, float]:
    """Return {month: hdd_total} for the given station and year."""
    station_data = weather_data[
        (weather_data['site_id'] == station) &
        (weather_data['date'].dt.year == year)
    ]
    station_data['hdd'] = (65.0 - station_data['daily_avg_temp']).clip(lower=0)
    return station_data.groupby(station_data['date'].dt.month)['hdd'].sum().to_dict()
```

Similarly for water heating:
```python
def compute_monthly_delta_t(water_temp_data: pd.DataFrame, target_temp: float, year: int) -> Dict[int, float]:
    """Return {month: avg_delta_t} for the given year."""
```

The daily weather data already exists in `DailyCalDay1985_Mar2025.csv` with ~151K records across 11 stations. No new data is needed — just a different aggregation.

#### 2. Monthly Load Shape Profiles (NEW)

Baseload end-uses (cooking, drying, fireplace) are currently flat annual values. For monthly output, each end-use needs a **monthly allocation profile** — what fraction of annual consumption occurs in each month.

**Proposed data structure** (add to `src/config.py` or a new `src/load_shapes.py`):

```python
# Monthly load shape profiles: fraction of annual consumption by month (must sum to 1.0)
MONTHLY_LOAD_SHAPES = {
    "space_heating": {
        # Driven by HDD — no profile needed, computed from weather
    },
    "water_heating": {
        # Driven by delta_t — no profile needed, computed from water temp
    },
    "cooking": {
        # Roughly flat with slight holiday peaks
        1: 0.085, 2: 0.078, 3: 0.082, 4: 0.080, 5: 0.082,
        6: 0.078, 7: 0.080, 8: 0.082, 9: 0.080, 10: 0.085,
        11: 0.090, 12: 0.098  # Thanksgiving + Christmas
    },
    "clothes_drying": {
        # Slightly higher in winter (more laundry, can't line-dry)
        1: 0.092, 2: 0.088, 3: 0.088, 4: 0.082, 5: 0.078,
        6: 0.072, 7: 0.070, 8: 0.072, 9: 0.078, 10: 0.082,
        11: 0.088, 12: 0.092
    },
    "fireplace": {
        # Heavily seasonal — winter only
        1: 0.200, 2: 0.180, 3: 0.120, 4: 0.040, 5: 0.010,
        6: 0.000, 7: 0.000, 8: 0.000, 9: 0.010, 10: 0.060,
        11: 0.150, 12: 0.230
    },
}
```

**Source for these profiles**: RBSA sub-metered data (`Data/Future Work/rbsam_y1/`, `rbsam_y2/`) provides 15-minute interval end-use data that can be aggregated to monthly shapes. RECS microdata also has seasonal consumption patterns. For the initial implementation, use the literature-based defaults above and refine with RBSA metering data later.

#### 3. Simulation Module (`src/simulation.py`)

**Current**: `simulate_space_heating(equipment, annual_hdd, heating_factor)` → float

**Needed**: New function or modified signature:

```python
def simulate_space_heating_monthly(
    equipment: EquipmentProfile,
    monthly_hdd: Dict[int, float],  # {month: hdd}
    heating_factor: float = 1.0
) -> Dict[int, float]:
    """Return {month: therms} for space heating."""
    return {
        month: max(0.0, (hdd * heating_factor) / equipment.efficiency)
        for month, hdd in monthly_hdd.items()
    }
```

Similarly for water heating and baseload. The core formula doesn't change — it's just applied 12 times instead of once.

#### 4. Orchestrator (`src/simulation.py` → `simulate_all_end_uses`)

**Current**: Loops over premises, computes one annual number per end-use.

**Needed**: Add a `temporal_resolution` parameter:

```python
def simulate_all_end_uses(
    premise_equipment, weather_data, water_temp_data, baseload_factors,
    year=2025, heating_factor=1.0,
    temporal_resolution='annual',  # NEW: 'annual', 'monthly', or 'daily'
    monthly_load_shapes=None,      # NEW: dict of load shape profiles
    ...
) -> pd.DataFrame:
```

When `temporal_resolution='monthly'`, the output DataFrame gets a `month` column:

| blinded_id | end_use | year | month | therms | efficiency |
|------------|---------|------|-------|--------|------------|
| 123456 | space_heating | 2025 | 1 | 85.2 | 0.85 |
| 123456 | space_heating | 2025 | 2 | 72.1 | 0.85 |
| ... | | | | | |
| 123456 | space_heating | 2025 | 12 | 78.4 | 0.85 |

#### 5. Scenario Config (`scenarios/baseline.json`)

Add new fields:

```json
{
    "name": "baseline",
    "base_year": 2025,
    "forecast_horizon": 10,
    "temporal_resolution": "monthly",
    "housing_growth_rate": 0.01,
    "electrification_rate": 0.02,
    "efficiency_improvement": 0.01,
    "weather_assumption": "normal",
    "heating_factor": {
        "RESSF": 1.0,
        "RESMF": 0.65,
        "MOBILE": 0.80
    },
    "electrification_rates": {
        "space_heating": 0.02,
        "water_heating": 0.05
    },
    "heat_pump_config": {
        "ashp_fraction": 0.85,
        "gshp_fraction": 0.15,
        "ashp_cop_baseline": 3.0,
        "gshp_cop_baseline": 4.0,
        "hpwh_ef_baseline": 2.75,
        "gorge_penalty": 0.85
    },
    "calibration_target": {
        "irp_upc_baseline": 648,
        "irp_decay_rate": -0.0119
    }
}
```

#### 6. Aggregation Module (`src/aggregation.py`)

**Current**: Aggregates by end-use, segment, district, year.

**Needed**: Add month as a grouping dimension:

```python
def aggregate_by_end_use_monthly(results: pd.DataFrame) -> pd.DataFrame:
    """Aggregate by end_use × year × month."""
    return results.groupby(['end_use', 'year', 'month']).agg(
        total_therms=('therms', 'sum'),
        customer_count=('blinded_id', 'nunique')
    ).reset_index()
```

#### 7. Validation Against Monthly Billing

The billing data has `GL_revenue_date` parsed to year/month. Monthly simulation output can be directly compared against monthly billing therms per premise — a much stronger calibration signal than annual totals.

```python
def calibrate_monthly(sim_results: pd.DataFrame, billing: pd.DataFrame) -> pd.DataFrame:
    """Compare simulated monthly therms against billed monthly therms."""
    merged = sim_results.merge(
        billing, on=['blinded_id', 'year', 'month'], suffixes=('_sim', '_bill')
    )
    merged['error'] = merged['therms_sim'] - merged['therms_bill']
    return merged
```

---

## Extension: Daily Resolution

Daily resolution follows the same pattern but with 365 rows per premise per end-use per year instead of 12. This is primarily useful for:

- **Peak-day analysis**: Identify the coldest days and their demand impact
- **Load shape modeling**: Understand intra-week and weekend patterns
- **Snow event correlation**: Cross-reference with `Portland_snow.csv` for extreme weather events

### Additional Requirements for Daily

1. **Daily load shapes for baseload end-uses** — Cooking has morning/evening peaks, drying is weekend-heavy. The RBSA sub-metered data (`Data/Future Work/rbsam_y1/`, `rbsam_y2/`) has 15-minute interval data that can derive these.

2. **Day-of-week effects** — Weekend vs. weekday consumption differs for cooking and drying. Space heating is relatively constant.

3. **Holiday effects** — Thanksgiving, Christmas, New Year's have elevated cooking and fireplace use.

4. **Output volume** — Daily resolution for 230K premises × 6 end-uses × 365 days × 10 years = ~5 billion rows. This requires chunked processing and Parquet output instead of CSV.

### Daily Simulation Formula

```python
def simulate_space_heating_daily(
    equipment: EquipmentProfile,
    daily_temps: pd.Series,  # Series indexed by date
    heating_factor: float = 1.0
) -> pd.Series:
    """Return daily therms for space heating."""
    daily_hdd = (65.0 - daily_temps).clip(lower=0)
    return (daily_hdd * heating_factor) / equipment.efficiency
```

---

## Implementation Plan

### Phase 1: Monthly Resolution (Estimated: 20-30 hours)

| Step | Task | Effort |
|------|------|--------|
| 1 | Add `compute_monthly_hdd` and `compute_monthly_delta_t` to `src/weather.py` | 2-3 hrs |
| 2 | Define monthly load shape profiles in `src/config.py` | 1-2 hrs |
| 3 | Add `simulate_*_monthly` functions to `src/simulation.py` | 3-4 hrs |
| 4 | Update `simulate_all_end_uses` with `temporal_resolution` parameter | 4-6 hrs |
| 5 | Update `ScenarioConfig` with new fields | 2-3 hrs |
| 6 | Update aggregation module for monthly grouping | 2-3 hrs |
| 7 | Add monthly billing calibration | 3-4 hrs |
| 8 | Property tests for monthly (sum of months = annual, non-negativity) | 3-4 hrs |
| 9 | Update scenario JSON files | 1 hr |

### Phase 2: Daily Resolution (Estimated: 15-20 hours additional)

| Step | Task | Effort |
|------|------|--------|
| 1 | Add daily simulation functions | 3-4 hrs |
| 2 | Derive daily load shapes from RBSA metering data | 4-6 hrs |
| 3 | Implement chunked processing for output volume | 3-4 hrs |
| 4 | Peak-day analysis module | 3-4 hrs |
| 5 | Snow event correlation | 2-3 hrs |

### Phase 3: Enhanced Scenario Parameters (Estimated: 10-15 hours)

| Step | Task | Effort |
|------|------|--------|
| 1 | Per-end-use electrification rates | 2-3 hrs |
| 2 | Heat pump parameters (COP, fractions, Gorge penalty) | 3-4 hrs |
| 3 | Segment-specific heating factors | 2-3 hrs |
| 4 | Calibration target integration | 2-3 hrs |
| 5 | New construction monthly profile | 1-2 hrs |

---

## Key Correctness Properties for Monthly Simulation

These property-based tests should be added when monthly resolution is implemented:

1. **Monthly-to-annual conservation**: Sum of 12 monthly therms = annual therms (within rounding tolerance)
2. **Seasonal monotonicity for space heating**: January therms > July therms for all PNW stations
3. **Monthly non-negativity**: All monthly therms >= 0
4. **Load shape normalization**: Monthly load shape fractions sum to 1.0 for each end-use
5. **Weather-driven seasonality**: Monthly space heating therms correlate with monthly HDD (r² > 0.95)
6. **Billing calibration improvement**: Monthly R² against billing should exceed annual R²

---

## Data Already Available

No new data acquisition is needed for monthly resolution. Everything required already exists:

| Data | Location | Status |
|------|----------|--------|
| Daily weather (11 stations, 1985-2025) | `Data/NWNatural Data/DailyCalDay1985_Mar2025.csv` | ✅ Loaded |
| Daily water temperature | `Data/NWNatural Data/BullRunWaterTemperature.csv` | ✅ Loaded |
| Monthly billing data | `Data/NWNatural Data/billing_data_blinded.csv` | ✅ Loaded (GL_revenue_date has year/month) |
| RBSA sub-metered data (for load shapes) | `Data/Future Work/rbsam_y1/`, `rbsam_y2/` | ✅ Available (not yet processed for load shapes) |
| NOAA monthly normals | `Data/noaa_normals/{ICAO}_monthly_normals.csv` | ✅ Loaded |

---

## Scenario Config Field Reference

Complete list of fields needed for monthly simulation, showing what exists today vs. what's new:

| Field | Current | Monthly | Description |
|-------|---------|---------|-------------|
| `name` | ✅ | ✅ | Scenario identifier |
| `base_year` | ✅ | ✅ | Starting year |
| `forecast_horizon` | ✅ | ✅ | Years to project |
| `temporal_resolution` | ❌ | 🆕 | `"annual"`, `"monthly"`, or `"daily"` |
| `housing_growth_rate` | ✅ | ✅ | Annual growth rate |
| `electrification_rate` | ✅ (flat) | 🔄 Expand | Per-end-use rates |
| `efficiency_improvement` | ✅ | ✅ | Annual improvement rate |
| `weather_assumption` | ✅ | ✅ | `"normal"`, `"warm"`, `"cold"` |
| `heating_factor` | ❌ (hardcoded 1.0) | 🆕 | Per-segment heating factors |
| `heat_pump_config` | ❌ | 🆕 | COP, fractions, penalties |
| `monthly_load_shapes` | ❌ | 🆕 | Per-end-use monthly profiles (or use defaults) |
| `calibration_target` | ❌ | 🆕 | IRP UPC baseline and decay rate |
| `weather_year` | ❌ | 🆕 | Specific year for actual weather (vs. normals) |
