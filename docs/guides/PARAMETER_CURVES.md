# Parameter Curves: Time-Varying Scenario Inputs

## Overview

Any numeric scenario parameter can be replaced with a set of control points to create any shape you want. The model interpolates linearly between your points and holds flat beyond the endpoints. If you don't specify a curve, the model uses its default fixed value.

## How It Works

In your scenario JSON, replace any number with a `points` object:

### Fixed Value (default — no change needed)
```json
{
  "electrification_rate": 0.02
}
```

### Custom Curve (any shape)
```json
{
  "electrification_rate": {
    "points": {
      "2025": 0.02,
      "2028": 0.04,
      "2030": 0.08,
      "2033": 0.05,
      "2035": 0.03
    }
  }
}
```

This creates: 2% in 2025, ramps to 4% by 2028, spikes to 8% by 2030, drops back to 5% by 2033, then 3% by 2035. Any shape — ramps, spikes, dips, plateaus.

### Shorthand (year keys directly)
```json
{
  "electrification_rate": {
    "2025": 0.02,
    "2028": 0.04,
    "2030": 0.08
  }
}
```
Same as above but without the `points` wrapper. Works the same way.

## Interpolation Rules

- Between control points: linear interpolation
- Before first point: holds first value
- After last point: holds last value
- You only need to specify the years where the value changes — the model fills in the rest

## Parameters That Support Curves

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| `electrification_rate` | 0.02 | Gas→electric switching rate per replacement |
| `hybrid_adoption_rate` | 0.03 | Gas→hybrid switching rate per replacement |
| `efficiency_improvement` | 0.01 | Annual efficiency gain rate |
| `housing_growth_rate` | 0.01 | Annual housing unit growth |
| `demolition_rate` | 0.002 | Annual demolition rate |
| `annual_degradation_rate` | 0.005 | Equipment efficiency loss per year |
| `new_equipment_efficiency` | 0.92 | AFUE of new equipment installs |
| `hybrid_gas_usage_factor` | 0.35 | Gas usage of hybrid homes (fraction of gas-only) |

## Examples

### Policy Ramp-Up (Heat Pump Incentives Start 2028)
```json
{
  "electrification_rate": {
    "points": {"2025": 0.02, "2028": 0.02, "2030": 0.06, "2035": 0.08}
  }
}
```
Flat at 2% until 2028, then ramps to 8% by 2035 as incentive programs kick in.

### Housing Boom Then Slowdown
```json
{
  "housing_growth_rate": {
    "points": {"2025": 0.015, "2028": 0.02, "2031": 0.01, "2035": 0.005}
  }
}
```
Growth peaks at 2% in 2028, then slows to 0.5% by 2035.

### Code Change Step (2028 Condensing Mandate)
```json
{
  "new_equipment_efficiency": {
    "points": {"2025": 0.92, "2027": 0.92, "2028": 0.95, "2035": 0.97}
  }
}
```
Jumps from 92% to 95% in 2028 when the DOE mandate takes effect, then gradually improves.

### Aggressive Electrification Spike Then Pullback
```json
{
  "electrification_rate": {
    "points": {"2025": 0.02, "2027": 0.03, "2029": 0.10, "2031": 0.06, "2035": 0.04}
  }
}
```
Spikes to 10% in 2029 (maybe a big incentive program), then pulls back as the easy conversions are done.

### Full Scenario with Multiple Curves
```json
{
  "name": "policy_ramp",
  "base_year": 2025,
  "forecast_horizon": 10,
  "heating_factor": 0.187502,
  "electrification_rate": {
    "points": {"2025": 0.02, "2028": 0.04, "2032": 0.08}
  },
  "hybrid_adoption_rate": {
    "points": {"2025": 0.03, "2028": 0.05, "2032": 0.10}
  },
  "housing_growth_rate": {
    "points": {"2025": 0.01, "2030": 0.008, "2035": 0.005}
  },
  "new_equipment_efficiency": {
    "points": {"2025": 0.92, "2028": 0.95, "2032": 0.96}
  }
}
```
Any parameter you don't specify as a curve uses its fixed default.

## How to Preview a Curve

```python
from src.parameter_curves import resolve

curve = {"points": {"2025": 0.02, "2028": 0.04, "2030": 0.08, "2033": 0.05}}
for year in range(2025, 2036):
    print(f"{year}: {resolve(curve, year):.4f}")
```

Output:
```
2025: 0.0200
2026: 0.0267
2027: 0.0333
2028: 0.0400
2029: 0.0600
2030: 0.0800
2031: 0.0700
2032: 0.0600
2033: 0.0500
2034: 0.0500
2035: 0.0500
```
