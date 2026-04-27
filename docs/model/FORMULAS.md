# Model Formulas: NW Natural End-Use Forecasting

## Core Demand Equation

For each premise `i` in forecast year `y`:

```
therms(i,y) = base_therms(i) × equipment_mult(i,y) × envelope_mult(i,y) × gas_fraction_mult(i,y)
```

Where:
- `base_therms(i)` = simulated space heating demand for premise `i` in the base year (2025)
- `equipment_mult(i,y)` = equipment efficiency adjustment (Weibull-driven)
- `envelope_mult(i,y)` = building envelope improvement (weatherization)
- `gas_fraction_mult(i,y)` = electrification/hybrid adjustment

---

## 1. Base Year Simulation

```
base_therms(i) = HDD(station) × heating_factor × vintage_mult(era) × segment_mult(seg) / efficiency
```

| Variable | Description | Source |
|----------|-------------|--------|
| `HDD(station)` | Annual heating degree days (base 65°F) for the premise's weather station | NW Natural DailyCalDay |
| `heating_factor` | Calibrated therms-per-HDD-per-unit (0.187502) | Billing data calibration |
| `vintage_mult(era)` | Building age multiplier (pre-1980: 1.35, 2015+: 0.70) | RBSA building shell data |
| `segment_mult(seg)` | Segment multiplier (SF: 1.05, MF: 0.70) | RBSA building shell data |
| `efficiency` | Equipment AFUE (default 0.80 for space heating) | Equipment codes |

---

## 2. Equipment Efficiency Multiplier (Weibull-Driven)

Each premise has equipment at age `a = base_year - install_year + year_offset`.

The Weibull model determines failure probability:

```
S(t) = exp(-(t/η)^β)           # Survival function
P(fail|age=t) = 1 - S(t)/S(t-1) # Conditional failure probability
```

Parameters: `η = 22.6 years` (scale), `β = 3.0` (shape), derived from `median_life = 20 years`.

Per-premise equipment multiplier:

```
If equipment fails this year (random draw < P(fail)):
    If age >= useful_life:  REPLACED → equipment_mult = base_eff / new_eff(year)
    If age < useful_life:   REPAIRED → equipment_mult = degraded + (1 - degraded) × recovery
If equipment survives:
    equipment_mult = (1 - degradation_rate) ^ year_offset
```

| Parameter | Value | Description |
|-----------|-------|-------------|
| `base_eff` | 0.80 | Default space heating AFUE |
| `new_eff(year)` | 0.92 (2025-2027), 0.95 (2028+), rising 0.3%/yr | Year-dependent new equipment AFUE |
| `degradation_rate` | 0.005 | Annual efficiency loss (0.5%/yr) |
| `recovery` | 0.85 | Repair efficiency recovery (85% of degradation restored) |
| `useful_life` | 20 years | Space heating equipment useful life |

### New Equipment AFUE Trajectory

```
year < 2028:  new_eff = 0.92 (current code minimum + market premium)
2028-2031:    new_eff = 0.95 + (year - 2028) × 0.003  (DOE condensing mandate)
2032+:        new_eff = 0.96 + (year - 2032) × 0.001  (smart controls, capped at 0.98)
```

---

## 3. Building Envelope Multiplier

Weatherization programs improve older homes' envelopes over time:

```
envelope_mult(i,y) = (1 - weatherization_rate(era)) ^ year_offset
```

| Vintage Era | Weatherization Rate | Description |
|-------------|-------------------|-------------|
| Pre-1980 | 0.45%/yr | Insulation upgrades, window replacement |
| 1980-1999 | 0.30%/yr | Moderate weatherization |
| 2000-2014 | 0.10%/yr | Already decent envelope |
| 2015+ | 0.00%/yr | Already tight, no improvement |

### Envelope Efficiency Index (New Construction)

New homes built in year `y` have an envelope index relative to 2000-2009 baseline (1.0):

```
index(y) = index(2025) × (1 - 0.02) ^ (y - 2025)
```

Starting at 0.62 in 2025, declining 2%/yr from tightening energy codes (Oregon OEESC).

---

## 4. Gas Fraction Multiplier (Electrification + Hybrid)

Each year, a fraction of replaced equipment switches fuel type:

```
leaving_gas = gas_fraction × replacement_rate
new_electric = leaving_gas × electrification_rate
new_hybrid = leaving_gas × hybrid_adoption_rate
gas_fraction(y+1) = gas_fraction(y) - new_electric - new_hybrid
hybrid_fraction(y+1) = hybrid_fraction(y) + new_hybrid
```

Effective gas demand per premise:

```
gas_mult = (gas_fraction + hybrid_fraction × hybrid_gas_usage_factor) / base_gas_fraction
```

Vintage-weighted: older homes electrify 15% faster, newer homes 10% slower.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `electrification_rate` | 0.02 | 2% of replacements go full electric |
| `hybrid_adoption_rate` | 0.03 | 3% of replacements go dual-fuel heat pump |
| `hybrid_gas_usage_factor` | 0.35 | Hybrid homes use 35% of gas-only demand |

---

## 5. Housing Stock Projection

```
total_units(y) = baseline_units × (1 + growth_rate) ^ year_offset
demolished(y) = baseline_units × demolition_rate × year_offset
new_construction(y) = total_units(y) - baseline_units + demolished(y)
```

### Segment Shift (Census B25024)

SF/MF shares shift based on historical Census trend (2009-2023 linear regression):

```
sf_pct(y) = base_sf_pct + sf_annual_pp × year_offset    (sf_annual_pp = -0.064)
mf_pct(y) = base_mf_pct + mf_annual_pp × year_offset    (mf_annual_pp = +0.142)
```

### Vintage Demolition (Age-Weighted)

```
surviving(era, y) = count(era) × (1 - demo_rate(era)) ^ year_offset
```

| Vintage Era | Demolition Rate | Description |
|-------------|----------------|-------------|
| Pre-1980 | 0.50%/yr | Oldest homes demolished fastest |
| 1980-1999 | 0.30%/yr | Moderate demolition |
| 2000-2009 | 0.10%/yr | Low demolition |
| 2010-2014 | 0.04%/yr | Very few demolished |
| 2015+ | 0.00%/yr | Too new |

---

## 6. Estimated Total UPC (Non-Heating End-Uses)

Non-heating end-uses are estimated using RECS 1993-2020 Pacific division ratios relative to space heating:

```
total_upc = sh_upc × (1 + Σ non_heating_ratios)
```

| End-Use | Ratio to SH | Source |
|---------|-------------|--------|
| Water Heating | 0.704 | RECS 2009/2015/2020 weighted |
| Cooking | 0.055 | RECS 2015/2020 |
| Clothes Drying | 0.034 | RECS 2015/2020 |
| Fireplace | 0.085 | RECS 2020 |
| Other | 0.131 | RECS 2020 |

---

## 7. Weibull Age-Cohort Model (Equipment Stats)

For fleet-wide replacement/repair/malfunction counts:

```
For each age cohort (age=0 to 60+):
    failures(age) = count(age) × scale × P(fail|age)
    If age >= useful_life: replacements += failures
    If age < useful_life:  repairs += failures

malfunctioning = total_failures × 0.10  (10% backlog)
working = total_equipment - malfunctioning
```

---

## 8. HDD Normalization

When the simulation uses a different weather year than the calibration year:

```
effective_heating_factor = config_heating_factor × (calibration_hdd / actual_hdd)
```

This ensures annual and monthly resolutions produce identical annual totals despite using different weather years.

---

## 9. Key Scenario Parameters

| Parameter | Baseline Value | Range | Unit |
|-----------|---------------|-------|------|
| `heating_factor` | 0.187502 | calibrated | therms/HDD/unit |
| `housing_growth_rate` | 0.01 | 0.00-0.05 | per year |
| `electrification_rate` | 0.02 | 0.00-0.10 | per replacement |
| `efficiency_improvement` | 0.01 | 0.00-0.05 | per year |
| `hybrid_adoption_rate` | 0.03 | 0.00-0.10 | per replacement |
| `hybrid_gas_usage_factor` | 0.35 | 0.20-0.50 | fraction of gas-only |
| `demolition_rate` | 0.002 | 0.001-0.005 | per year |
| `new_construction_mf_share` | 0.37 | 0.20-0.60 | fraction |
| `annual_degradation_rate` | 0.005 | 0.002-0.010 | per year |
| `repair_efficiency_recovery` | 0.85 | 0.70-0.95 | fraction |
| `new_equipment_efficiency` | 0.92 | 0.80-0.98 | AFUE |

---

## Data Sources

| Data | Source | Years | Records |
|------|--------|-------|---------|
| Premise/Equipment/Segment | NW Natural (blinded) | 2025 | 213K premises, 247K equipment |
| Billing | NW Natural (blinded) | 2009-2025 | 48M records → 3.4M annual |
| Weather (HDD) | NW Natural DailyCalDay | 1985-2025 | 11 stations |
| Census B25024 (SF/MF) | ACS 5-year | 2009-2023 | 16 counties |
| Census B25034 (Vintage) | ACS 5-year | 2009-2023 | 16 counties |
| Census B25040 (Heating Fuel) | ACS 5-year | 2009-2023 | 16 counties |
| RECS (End-Use Shares) | EIA | 1993-2020 | 7 survey years |
| RBSA (Building Shell) | NEEA | 2017, 2022 | PNW region |
| IRP Load Decay Forecast | NW Natural | 2025-2035 | 11 years |
| AFUE Code History | DOE/NAECA | 1992-2028 | Federal minimums |
| Envelope Efficiency | Oregon Energy Code | 1960-2025 | State code history |
