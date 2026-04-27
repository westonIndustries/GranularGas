# Model Formulas: NW Natural End-Use Forecasting

This document defines every mathematical formula used in the model, with variable definitions and units. All formulas correspond to implemented code in `src/`.

---

## 1. Space Heating Consumption

The core formula for annual space heating demand at a single premise:

```
therms(i, y) = (HDD(s, y) × heating_factor × vintage_mult(era) × segment_mult(seg) × qty) / efficiency(i, y)
```

| Variable | Description | Units | Source |
|----------|-------------|-------|--------|
| `HDD(s, y)` | Annual heating degree days (base 65°F) for weather station `s` in year `y` | degree-days | NW Natural DailyCalDay |
| `heating_factor` | Calibrated therms-per-HDD-per-unit | therms / (HDD × unit) | Billing data calibration (~0.1875) |
| `vintage_mult(era)` | Building age multiplier by construction era | dimensionless | RBSA building shell data |
| `segment_mult(seg)` | Segment multiplier (SF vs MF) | dimensionless | RBSA building shell data |
| `qty` | Number of heating units at the premise | units | NW Natural equipment data |
| `efficiency(i, y)` | Equipment AFUE in year `y` (changes with replacement/degradation) | dimensionless (0–1) | Equipment codes / ASHRAE |

### Vintage Multipliers

| Construction Era | Multiplier | Rationale |
|-----------------|-----------|-----------|
| Pre-1980 | 1.35 | Poor insulation, single-pane windows |
| 1980–1999 | 1.15 | First energy codes, better insulation |
| 2000–2009 | 1.00 | Baseline calibration era |
| 2010–2014 | 0.85 | Improved codes, better windows |
| 2015+ | 0.70 | Current code, condensing furnaces, tight envelope |

### Segment Multipliers

| Segment | Multiplier | Rationale |
|---------|-----------|-----------|
| RESSF | 1.05 | Single-family: larger, more exposed |
| RESMF | 0.70 | Multi-family: shared walls reduce heat loss ~30% |
| Unclassified | 1.00 | Fleet average |

---

## 2. Heating Degree Days (HDD)

```
HDD_daily = max(0, 65°F − daily_avg_temp)
HDD_annual(s, y) = Σ HDD_daily  for all days in year y at station s
```

| Variable | Description | Units |
|----------|-------------|-------|
| `daily_avg_temp` | Daily average temperature | °F |
| `65°F` | Base temperature (standard for residential heating) | °F |
| `HDD_annual` | Sum of daily HDD over the year | degree-days |

---

## 3. Weibull Survival Model

Equipment replacement timing uses a Weibull survival function:

```
S(t) = exp(−(t / η)^β)
```

Replacement probability at age `t` given survival to age `t−1`:

```
P_replace(t) = 1 − S(t) / S(t−1)
```

Weibull scale parameter derived from ASHRAE median service life `L`:

```
η = L / (ln 2)^(1/β)
```

| Variable | Description | Units |
|----------|-------------|-------|
| `S(t)` | Probability of surviving to age `t` | dimensionless (0–1) |
| `t` | Equipment age | years |
| `η` (eta) | Scale parameter | years |
| `β` (beta) | Shape parameter (controls failure rate distribution) | dimensionless |
| `L` | Median service life from ASHRAE data | years |
| `P_replace(t)` | Conditional probability of replacement at age `t` | dimensionless (0–1) |

### Default Weibull Parameters

| End-Use | β (shape) | Default L (median life) | Derived η |
|---------|-----------|------------------------|-----------|
| space_heating | 3.0 | 20 years | 22.6 years |
| water_heating | 3.0 | 13 years | 14.7 years |
| cooking | 2.5 | 15 years | 17.7 years |
| clothes_drying | 2.5 | 13 years | 15.3 years |
| fireplace | 2.0 | 30 years | 37.5 years |
| other | 2.5 | 15 years | 17.7 years |

Higher `β` means failures are more concentrated around the median life (sharper peak). Lower `β` means a wider spread of failure ages.

---

## 4. Equipment Efficiency Over Time

### 4a. Degradation (all surviving equipment)

```
efficiency(t+1) = efficiency(t) × (1 − degradation_rate)
```

| Variable | Default | Description |
|----------|---------|-------------|
| `degradation_rate` | 0.005 | Annual efficiency loss (0.5%/yr) |

### 4b. Replacement (failed equipment)

```
efficiency_new = new_equipment_efficiency(y)
```

New equipment efficiency trajectory:

```
y < 2028:   new_eff = 0.92   (current code minimum, condensing furnace)
2028–2031:  new_eff = 0.92 + (y − 2028) × 0.003   (DOE condensing mandate)
2032+:      new_eff = min(0.98, 0.95 + (y − 2032) × 0.001)
```

### 4c. Electrification (subset of replacements)

```
If random() < electrification_rate:
    fuel_type = "electric"
    efficiency = electric_equivalent_efficiency
```

---

## 5. Housing Stock Projection

```
total_units(y) = baseline_units × (1 + housing_growth_rate)^(y − base_year)
```

### Segment Share Shift (Census B25024)

SF/MF shares shift based on historical Census B25024 trend (2009–2023 linear regression):

```
sf_pct(y) = base_sf_pct + sf_annual_pp × (y − base_year)
mf_pct(y) = base_mf_pct + mf_annual_pp × (y − base_year)
```

Where `sf_annual_pp` and `mf_annual_pp` are the annual percentage-point shift rates computed from Census data (typically sf_annual_pp ≈ −0.064 pp/yr, mf_annual_pp ≈ +0.142 pp/yr).

---

## 6. Use Per Customer (UPC)

```
UPC(y) = total_therms(y) / premise_count(y)
```

| Variable | Description | Units |
|----------|-------------|-------|
| `total_therms(y)` | Sum of all end-use therms across all premises in year `y` | therms/year |
| `premise_count(y)` | Count of unique active residential premises in year `y` | premises |
| `UPC(y)` | Average annual gas consumption per customer | therms/customer/year |

---

## 7. IRP Load Decay Forecast (Reference)

NW Natural's 2025 IRP top-down forecast:

```
IRP_UPC(y) = 648 × (1 − 0.0119)^(y − 2025)
```

| Variable | Value | Description |
|----------|-------|-------------|
| `648` | therms | 2025 baseline UPC |
| `0.0119` | per year | Annual decay rate (−1.19%/yr) |

---

## 8. Estimated Total UPC (RECS Non-Heating Ratios)

When `use_recs_ratios=true`, non-heating end-uses are estimated from RECS Pacific division data:

```
total_upc(y) = sh_upc(y) × (1 + Σ non_heating_ratios)
```

| End-Use | Ratio to Space Heating | Source |
|---------|----------------------|--------|
| Water Heating | 0.704 | RECS 2009/2015/2020 weighted |
| Cooking | 0.055 | RECS 2015/2020 |
| Clothes Drying | 0.034 | RECS 2015/2020 |
| Fireplace | 0.085 | RECS 2020 |
| Other | 0.131 | RECS 2020 |
| **Total multiplier** | **2.009** | Space heating × 2.009 ≈ total |

---

## 9. HDD Normalization (Weather Year Adjustment)

When the simulation uses a different weather year than the calibration year:

```
effective_heating_factor = config_heating_factor × (calibration_HDD / actual_HDD)
```

This ensures the model produces consistent annual therms regardless of which weather year is used. See [HDD_NORMALIZATION.md](HDD_NORMALIZATION.md) for full details.

---

## 10. Weather Adjustment Factor

```
weather_adjustment_factor(s, y) = actual_HDD(s, y) / normal_HDD(s)
```

Where `normal_HDD(s)` is the NOAA 30-year Climate Normal (1991–2020) for station `s`. Values > 1.0 indicate a colder-than-normal year; values < 1.0 indicate warmer-than-normal.

---

## 11. Key Scenario Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `heating_factor` | 0.1875 | calibrated | therms per HDD per unit |
| `housing_growth_rate` | 0.01 | 0.00–0.05 | Annual housing stock growth rate |
| `electrification_rate` | 0.02 | 0.00–0.10 | Fraction of replacements that switch to electric |
| `efficiency_improvement` | 0.01 | 0.00–0.05 | Annual efficiency improvement for new equipment |
| `new_equipment_efficiency` | 0.92 | 0.80–0.98 | AFUE of newly installed gas equipment |
| `annual_degradation_rate` | 0.005 | 0.002–0.010 | Annual efficiency loss for aging equipment |
| `base_year` | 2025 | — | Calibration and simulation base year |
| `forecast_horizon` | 10 | 1–50 | Number of years to project forward |

All parameters support either a scalar value or a year-indexed curve dict resolved by `src/parameter_curves.py`.

---

## Data Sources

| Data | Source | Coverage |
|------|--------|---------|
| Premise/Equipment/Segment | NW Natural (blinded) | ~213K premises, ~247K equipment records |
| Weather (HDD) | NW Natural DailyCalDay | 11 stations, 1985–2025 |
| ASHRAE Service Life | ASHRAE (OR/WA) | Equipment median life by category |
| Census B25024 (SF/MF) | ACS 5-year | 16 NWN counties, 2009–2023 |
| Census B25034 (Vintage) | ACS 5-year | 16 NWN counties, 2009–2023 |
| Census B25040 (Heating Fuel) | ACS 5-year | 16 NWN counties, 2009–2023 |
| RECS (End-Use Shares) | EIA | Pacific division, 1993–2020 |
| IRP Load Decay Forecast | NW Natural | 2025–2035 |
| NOAA Climate Normals | NOAA CDO | 11 stations, 1991–2020 |
