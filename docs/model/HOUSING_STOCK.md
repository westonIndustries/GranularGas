# Housing Stock Model

## Overview

The housing stock model represents NW Natural's residential customer base as a collection of premises with known characteristics — segment, vintage, district, and equipment inventory. It provides the foundation for all demand projections: every simulated therm traces back to a specific premise with a specific building age, segment type, and weather station assignment.

The model builds a baseline stock from NW Natural's actual blinded premise and segment data, then projects it forward year by year using scenario-defined growth rates and Census-derived segment shift rates.

---

## Baseline Stock Construction

### Data Sources

| Source | File | Key Fields Used |
|--------|------|----------------|
| NW Natural premise data | `premise_data_blinded.csv` | `blinded_id`, `district_code_IRP`, `service_state` |
| NW Natural segment data | `segment_data_blinded.csv` | `blinded_id`, `segment`, `subseg`, `mktseg`, `set_year` |

### Filtering

Only active residential premises are included:
- `custtype = 'R'` (residential)
- `status_code = 'AC'` (active)

Commercial, industrial, and inactive premises are excluded from all calculations.

### Premise Attributes

Each premise in the baseline stock carries:

| Attribute | Source | Description |
|-----------|--------|-------------|
| `blinded_id` | premise_data | Anonymized unique identifier |
| `district_code_IRP` | premise_data | IRP district for geographic grouping and weather station assignment |
| `service_state` | premise_data | OR or WA (used for state-specific ASHRAE service life lookup) |
| `segment` | segment_data | Housing type: RESSF, RESMF, or MOBILE |
| `subseg` | segment_data | Construction type: FRAME, MFG, MASONRY |
| `mktseg` | segment_data | Market segment: RES-CONV, RES-SFNC, etc. |
| `set_year` | segment_data | Year the premise was connected — used as construction vintage proxy |

### Baseline Counts (approximate)

| Segment | Count | Share |
|---------|-------|-------|
| RESSF (single-family) | ~170,000 | ~80% |
| RESMF (multi-family) | ~32,000 | ~15% |
| MOBILE | ~11,000 | ~5% |
| **Total** | **~213,000** | **100%** |

---

## Vintage Cohorts

The `set_year` field (year the premise was connected to NW Natural) is used as a proxy for construction vintage. Premises are grouped into five vintage eras that drive the `VINTAGE_HEATING_MULTIPLIER`:

| Era | Years | Heating Multiplier | Rationale |
|-----|-------|--------------------|-----------|
| Pre-1980 | before 1980 | 1.35× | Poor insulation, single-pane windows, no energy codes |
| 1980–1999 | 1980–1999 | 1.15× | First energy codes, better insulation |
| 2000–2009 | 2000–2009 | 1.00× | Baseline calibration era |
| 2010–2014 | 2010–2014 | 0.85× | Improved codes, better windows |
| 2015+ | 2015 onward | 0.70× | Current code, condensing furnaces, tight envelope |

These multipliers are applied in the space heating simulation formula:

```
therms = (HDD × heating_factor × vintage_mult × segment_mult × qty) / efficiency
```

A pre-1980 home uses 35% more gas per HDD than a 2000–2009 home of the same segment type, all else equal. A 2015+ home uses 30% less.

---

## Segment Multipliers

Multi-family homes share walls, floors, and ceilings with adjacent units, reducing their exposed envelope area and therefore their heating load per unit. The `SEGMENT_HEATING_MULTIPLIER` captures this:

| Segment | Multiplier | Rationale |
|---------|-----------|-----------|
| RESSF | 1.05× | Single-family: slightly above average (larger, more exposed) |
| RESMF | 0.70× | Multi-family: shared walls reduce heat loss ~30% |
| Unclassified | 1.00× | Fleet average |

---

## Housing Stock Projection

### Growth Rate

Total housing units are projected forward using a compound growth formula:

```
total_units(y) = baseline_units × (1 + housing_growth_rate)^(y − base_year)
```

`housing_growth_rate` is a scenario parameter that can be a scalar (e.g., `0.01` for 1%/year) or a year-indexed curve (e.g., `{"2025": 0.01, "2030": 0.015}`). Year-indexed curves are resolved by `src/parameter_curves.py` using linear interpolation between defined years.

### Segment Share Shift

The SF/MF split does not stay fixed — Census B25024 data shows a long-run trend toward more multi-family construction. The model projects segment shares forward using historical shift rates computed from Census data:

```
sf_pct(y) = base_sf_pct + sf_annual_pp × (y − base_year)
mf_pct(y) = base_mf_pct + mf_annual_pp × (y − base_year)
```

Where `sf_annual_pp` and `mf_annual_pp` are the annual percentage-point shift rates derived from Census B25024 county-level data (2009–2023) for the 16 NW Natural service territory counties. Typical values: sf_annual_pp ≈ −0.064 pp/yr, mf_annual_pp ≈ +0.142 pp/yr.

This means by 2035 (10 years out), the MF share is projected to be roughly 1.4 percentage points higher than in 2025 — a modest but directionally correct shift.

### New Construction Vintage

New units added each year are assigned to the current vintage era (2015+) with the corresponding heating multiplier of 0.70×. This means new construction is more efficient than the existing fleet average, which gradually pulls the fleet average efficiency up over time.

---

## HousingStock Dataclass

The `HousingStock` dataclass in `src/housing_stock.py` holds the stock for a single year:

```python
@dataclass
class HousingStock:
    year: int                          # Simulation year
    premises: pd.DataFrame             # Full premise-equipment DataFrame
    total_units: int                   # Count of unique blinded_ids
    units_by_segment: dict[str, int]   # {'RESSF': 170000, 'RESMF': 32000, ...}
    units_by_district: dict[str, int]  # {'MULT': 85000, 'LANE': 42000, ...}
```

`build_baseline_stock(premise_equipment, base_year)` constructs the 2025 baseline from the premise-equipment table.

`project_stock(baseline, target_year, scenario)` applies the growth rate and segment shift to produce the stock for any future year.

---

## Census Validation

The model cross-validates the housing stock against three Census ACS tables:

| Census Table | What It Validates |
|-------------|------------------|
| B25034 (Year Structure Built) | Vintage distribution — does the model's pre-1980/1980-2000/etc. mix match Census counts? |
| B25040 (House Heating Fuel) | Gas market share — what fraction of housing units use utility gas as primary heat? |
| B25024 (Units in Structure) | SF/MF split — does the model's RESSF/RESMF ratio match Census structure type counts? |

These comparisons are exported to `census_summary_*.csv` in each scenario output folder. Discrepancies > 10% are flagged as warnings in the data quality reports.

---

## Output Files

Each scenario produces `housing_stock.csv` with columns:

| Column | Description |
|--------|-------------|
| `year` | Simulation year |
| `total_units` | Total projected housing units |
| `RESSF` | Projected single-family units |
| `RESMF` | Projected multi-family units |
| `growth_rate` | Housing growth rate used (from scenario config) |
| `scenario_name` | Scenario identifier |

---

## Limitations

1. **`set_year` as vintage proxy** — The year a premise was connected to NW Natural is not the same as the year it was built. New construction is typically connected within 1–2 years of completion, but older homes may have been connected decades after construction. This introduces noise in the vintage distribution.

2. **No demolition modeling** — The model does not remove premises from the stock over time. In reality, ~0.2–0.5% of housing units are demolished each year, with older units demolished at higher rates. This slightly overstates the pre-1980 share in later years.

3. **Flat new construction vintage** — All new units are assigned to the 2015+ era. In reality, some new construction may be built to lower standards (e.g., manufactured homes). This slightly understates demand from new construction.

4. **No geographic redistribution** — The district distribution is held constant over the forecast horizon. In reality, growth is not uniform — some districts grow faster than others.

---

## Related Documentation

- **[ALGORITHM.md](ALGORITHM.md)** — Where housing stock fits in the simulation pipeline
- **[FORMULAS.md](FORMULAS.md)** — Housing stock projection formula and segment shift equations
- **[CENSUS_RECS_INTEGRATION.md](CENSUS_RECS_INTEGRATION.md)** — How Census data validates and informs the housing stock
