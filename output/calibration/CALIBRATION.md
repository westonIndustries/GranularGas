# Heating Factor Calibration Report

## What This Does

The simulation computes space heating demand using:

```
therms = (annual_hdd × heating_factor) / efficiency
```

Without calibration, `heating_factor = 1.0` means "1 therm of gas per heating degree day per premise."
This produces ~2,600 therms/customer — about 4x higher than reality.

The **heating_factor** is the calibration constant that bridges the gap between raw HDD
and actual gas consumption. It accounts for:

- **Building envelope** — insulation, windows, air sealing (how fast heat leaks out)
- **Square footage** — larger homes need more heat, but not linearly
- **Thermostat behavior** — not everyone heats to 65°F; setbacks at night/away
- **Duct losses** — 20-30% of furnace output lost in ductwork
- **Occupancy patterns** — homes empty during work hours don't need full heating
- **Equipment sizing** — oversized furnaces cycle on/off, reducing effective output

## Calibration Results

| Parameter | Value |
|-----------|-------|
| Calibration year | 2025 |
| Observed mean UPC (all end-uses) | 542.9 therms/customer |
| Observed median UPC | 488.0 therms/customer |
| Premises in calibration | 203,989 |
| Space heating share assumption | 60% |
| Estimated space heating therms | 325.7 therms/customer |
| Weighted average annual HDD | 1,845.9 degree-days |
| Average equipment efficiency | 63.76% |
| **Heating factor (total UPC)** | **0.187502** |
| **Heating factor (space heating only)** | **0.112501** |

## How the Heating Factor Was Computed

```
heating_factor = observed_therms × efficiency / annual_hdd
```

For total UPC calibration:
```
0.187502 = 542.9 × 0.6376 / 1,845.9
```

For space-heating-only calibration:
```
0.112501 = 325.7 × 0.6376 / 1,845.9
```

## Verification

Using the calibrated heating factor, the model produces:

| Scope | Heating Factor | Model Output | Target | Match? |
|-------|---------------|-------------|--------|--------|
| Total UPC | 0.187502 | 542.9 therms | 542.9 therms | ✅ |
| Space heating only | 0.112501 | 325.7 therms | 325.7 therms | ✅ |

## Comparison to NW Natural IRP

| Metric | Value |
|--------|-------|
| IRP baseline UPC (2025) | 648.0 therms/customer |
| IRP annual decay rate | -1.19% |
| Observed billing UPC (2025) | 542.9 therms/customer |
| Difference | -105.1 therms (-16.2%) |

## Which Heating Factor to Use

- **For current scope (space heating only):** Use `0.112501`
  - This produces space-heating-only therms that, when combined with future water heating/cooking/drying modules, will sum to the total observed UPC.

- **For quick total-UPC matching:** Use `0.187502`
  - This makes the space-heating-only model match total observed billing. Useful for IRP comparison before other end-uses are implemented.

## How to Apply

In `scenarios/baseline.json`, add:

```json
"heating_factor": 0.112501
```

Or for segment-specific factors (recommended):

```json
"heating_factor": {
    "RESSF": 0.123751,
    "RESMF": 0.078751,
    "MOBILE": 0.095626
}
```

(Single-family homes use ~10% more than average, multi-family ~30% less, mobile homes ~15% less.)
