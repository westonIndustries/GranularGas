# Model Calibration

## Overview

Calibration is the process of adjusting the model's `heating_factor` so that the base-year (2025) simulated UPC matches NW Natural's observed UPC. Without calibration, the model would produce whatever UPC falls out of the raw HDD × equipment efficiency calculation — which may be far from the actual 648 therms/customer that NW Natural observed in 2025.

The calibration is implemented in `src/calibration.py` and runs as part of the pipeline before the forecast loop begins.

---

## The Heating Factor

The `heating_factor` is the single most important calibration parameter. It converts annual HDD into annual therms per heating unit:

```
therms = (HDD × heating_factor × vintage_mult × segment_mult × qty) / efficiency
```

The heating factor absorbs everything the model doesn't explicitly represent:
- Building size (square footage)
- Insulation quality beyond what vintage multipliers capture
- Thermostat setpoints and occupancy patterns
- Duct losses and distribution inefficiency
- Infiltration and air leakage

A heating factor of 0.1875 means: for every HDD, a typical heating unit consumes 0.1875 therms (before vintage, segment, and efficiency adjustments).

---

## Calibration Target: NW Natural IRP Load Decay Data

NW Natural's 2025 IRP provides the calibration target. Four files capture the historical and projected UPC:

| File | Content |
|------|---------|
| `prior load decay data reconstructed.txt` | Historical UPC by year, 2005–2025 |
| `prior load decay data simulated.txt` | Year-by-year UPC multipliers vs 2025 baseline |
| `prior load decay data description.txt` | Three-era framework documentation |
| `10-Year Load Decay Forecast (2025–2035).csv` | Forward UPC projection, 2025–2035 |

### The Three-Era Framework

NW Natural's historical UPC data follows a three-era pattern that provides vintage-level calibration anchors:

| Era | Years | Typical UPC | Dominant Equipment | Decay Rate |
|-----|-------|-------------|-------------------|-----------|
| Era 1 | 2005–2015 | ~820 → ~720 therms | 80% AFUE furnaces | −1.15%/yr |
| Era 2 | 2015–2020 | ~720 → ~648 therms | 90%+ AFUE condensing | −1.55%/yr |
| Era 3 | 2020–2025 | ~648 therms (stable) | Heat pump hybrids entering | −1.19%/yr |

The 2025 baseline UPC of **648 therms/customer** is the primary calibration target.

### IRP Forward Forecast

```
IRP_UPC(y) = 648 × (1 − 0.0119)^(y − 2025)
```

This produces:
- 2025: 648 therms
- 2030: 610 therms
- 2035: 575 therms

The model's bottom-up UPC projections are compared against this forecast in `irp_comparison.csv`.

---

## Calibration Process

### Step 1: Run Base-Year Simulation

Run the simulation for `base_year = 2025` with the initial `heating_factor` from the scenario config (default: 0.1875).

```
model_upc_2025 = total_therms_2025 / premise_count_2025
```

### Step 2: Compute Calibration Residual

```
residual = model_upc_2025 - target_upc_2025
pct_residual = residual / target_upc_2025 × 100
```

Where `target_upc_2025 = 648` therms (from IRP data).

### Step 3: Adjust Heating Factor

If the residual is outside an acceptable tolerance (±5%), adjust the heating factor:

```
calibrated_heating_factor = config_heating_factor × (target_upc / model_upc)
```

This is a simple proportional scaling — if the model produces 700 therms but the target is 648, scale the heating factor down by 648/700 = 0.926.

### Step 4: Re-run and Verify

Re-run the base-year simulation with the calibrated heating factor and verify the residual is within tolerance.

---

## Current Calibration State

The model's current calibrated heating factor is approximately **0.1875 therms/HDD/unit**.

This was derived by:
1. Running the simulation against 2025 partial-year weather data (Jan–Mar 2025)
2. Comparing against 2025 billing data (also Jan–Mar)
3. Adjusting the heating factor until the model UPC matched the billing-implied UPC for the same period

**Important caveat**: The calibration uses partial-year (Jan–Mar) data because the 2025 weather file ends in March. This means the heating factor is calibrated against the coldest quarter of the year, which may not perfectly represent the full annual relationship. See [HDD_NORMALIZATION.md](HDD_NORMALIZATION.md) for how the model handles this.

---

## Calibration Outputs

Each scenario produces `irp_comparison.csv` with:

| Column | Description |
|--------|-------------|
| `year` | Simulation year |
| `model_upc` | Bottom-up model UPC (space heating only) |
| `irp_upc` | NW Natural IRP forecast UPC (all end-uses) |
| `estimated_total_upc` | Model UPC + RECS non-heating estimates (if `use_recs_ratios=true`) |
| `diff_therms` | `model_upc - irp_upc` |
| `diff_pct` | `diff_therms / irp_upc × 100` |
| `total_therms` | Total system therms |
| `premise_count` | Number of active premises |

---

## Billing-Based Calibration

In addition to IRP-based calibration, the model can calibrate against actual billing data. The `src/validation/billing_calibration.py` module:

1. Loads historical billing records (`billing_data_blinded.csv`)
2. Validates that `utility_usage` is already in therms (not dollars — NW Natural's billing data stores therms directly)
3. Computes annual therms per premise from billing records
4. Compares against simulated therms for the same premises and years
5. Reports calibration metrics: mean absolute error, mean bias, RMSE, R²

**Note**: Billing data covers 2009–2025 (~48M records). The model uses 2024 or 2025 billing as the primary calibration year.

---

## Envelope Efficiency Calibration

The `src/envelope_efficiency.py` module projects building envelope efficiency over time using:

1. RBSA 2022 building shell data (insulation levels, window types, air leakage)
2. NW energy proxies (envelope UA values by vintage era from `nw_energy_proxies.csv`)
3. Oregon Energy Code history (tightening standards over time)

Envelope UA values by vintage era (from RBSA 2022):

| Vintage Era | Envelope UA (BTU/hr·°F·ft²) | Relative to 2000–2009 baseline |
|-------------|---------------------------|-------------------------------|
| Pre-1950 | 0.250 | 4.5× worse |
| 1951–1980 | 0.081 | 1.4× worse |
| 1981–2010 | 0.056 | 1.0× (baseline) |
| 2011+ | 0.038 | 0.68× better |

These values inform the `VINTAGE_HEATING_MULTIPLIER` in `src/config.py` and can be used to project envelope improvements over the forecast horizon as weatherization programs take effect.

---

## Sensitivity to Calibration Parameters

The model's 2035 UPC is most sensitive to:

| Parameter | ±10% change → UPC change |
|-----------|--------------------------|
| `heating_factor` | ±10% (direct proportional) |
| `new_equipment_efficiency` | ±2–4% |
| `electrification_rate` | ±1–8% (depends on rate) |
| `annual_degradation_rate` | ±3–5% |

The heating factor is the dominant parameter. A 10% error in calibration propagates directly to a 10% error in all projected UPC values.

---

## Recommendations for Improving Calibration

1. **Full-year calibration**: Calibrate against a complete year of billing data (2024) rather than partial 2025. This would produce a more robust heating factor.

2. **Premise-level calibration**: Instead of calibrating to the fleet average UPC, calibrate at the premise level — compare simulated therms for each `blinded_id` against that premise's actual billing therms. This would reveal systematic biases by segment, vintage, or district.

3. **Weather-normalized calibration**: Use NOAA climate normals to normalize both the billing data and the simulation to "typical weather" before comparing. This removes the effect of year-to-year weather variation from the calibration.

4. **Vintage-stratified calibration**: Calibrate the heating factor separately for each vintage era (pre-1980, 1980–1999, etc.) rather than using a single fleet-average factor. This would improve accuracy for the tails of the vintage distribution.

---

## Related Documentation

- **[HDD_NORMALIZATION.md](HDD_NORMALIZATION.md)** — How partial-year weather data is handled
- **[MODEL_VS_IRP_COMPARISON.md](MODEL_VS_IRP_COMPARISON.md)** — Calibration residuals and comparison to IRP
- **[FORMULAS.md](FORMULAS.md)** — Heating factor formula and calibration equations
- **[DATA_SOURCES.md](DATA_SOURCES.md)** — IRP load decay data file descriptions
