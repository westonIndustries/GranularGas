# Equipment Efficiency Model

## Overview

The model tracks equipment efficiency as a dynamic quantity that changes each year through three mechanisms: degradation (all surviving equipment loses efficiency over time), replacement (failed equipment is swapped for a new unit at current code-minimum efficiency), and electrification (a fraction of replacements switch fuel type entirely).

These three mechanisms create a realistic distribution of equipment performance across the fleet, rather than assuming all equipment operates at its rated efficiency forever.

---

## The Three Efficiency Mechanisms

### 1. Degradation (All Surviving Equipment)

Every piece of equipment loses efficiency each year due to normal wear and tear.

```
efficiency(t+1) = efficiency(t) × (1 − degradation_rate)
```

**Default**: `degradation_rate = 0.005` (0.5% per year)

**What causes degradation:**
- Heat exchanger fouling and corrosion
- Burner deposits reducing combustion efficiency
- Duct leakage increasing over time (connections loosen, seals fail)
- Thermostat calibration drift
- Fan motor bearing wear (reduced airflow)

**Example**: A furnace rated at 80% AFUE when installed in 2010:

| Year | Age | Efficiency |
|------|-----|-----------|
| 2010 | 0 | 80.0% |
| 2015 | 5 | 78.0% |
| 2020 | 10 | 76.1% |
| 2025 | 15 | 74.2% |
| 2030 | 20 | 72.4% |

Over 15 years, the furnace has lost ~7% of its rated efficiency — meaning it uses ~7% more gas than a new unit of the same model to deliver the same heat.

---

### 2. Replacement (Failed Equipment)

Equipment that fails the Weibull survival draw is replaced with a new unit at the current code-minimum efficiency.

```
efficiency_new = new_equipment_efficiency(y)
```

**New equipment efficiency trajectory:**

```
y < 2028:   new_eff = 0.92   (current DOE minimum for non-weatherized gas furnaces)
2028–2031:  new_eff = 0.92 + (y − 2028) × 0.003   (anticipated DOE condensing mandate)
2032+:      new_eff = min(0.98, 0.95 + (y − 2032) × 0.001)
```

**Why 92%**: The DOE minimum efficiency standard for residential gas furnaces (effective 2015) is 92% AFUE for non-weatherized units. Most new installations in the PNW are condensing furnaces at 92–96% AFUE. 92% is the conservative floor.

**Impact of replacement**: That 15-year-old furnace at 74.2% gets replaced:
- Old efficiency: 74.2%
- New efficiency: 92.0%
- Efficiency jump: +17.8 percentage points
- Gas savings: (92 − 74.2) / 74.2 = **24% less gas** for the same heat output

This is the primary mechanism driving demand reduction in the model — as old equipment fails and gets replaced with modern high-efficiency units, the fleet average efficiency rises.

---

### 3. Electrification (Subset of Replacements)

A scenario-configurable fraction of replacements switch fuel type entirely, removing gas demand from those premises.

```
If random() < electrification_rate:
    fuel_type = "electric"
    efficiency = electric_equivalent_efficiency
```

**Default**: `electrification_rate = 0.02` (2% of replacements switch to electric)

When a premise electrifies, its gas space heating demand drops to zero. The electric equivalent efficiency is expressed as a gas-equivalent AFUE for comparison purposes:

```
gas_equivalent_efficiency = COP / 3.412
```

Where 3.412 is the BTU-per-watt conversion factor. An air-source heat pump with COP = 3.0 has a gas-equivalent efficiency of 0.88 — meaning it delivers the same heat as a 88% AFUE gas furnace while using electricity instead of gas.

---

## Fleet Composition Over Time

In a typical year with ~5% annual replacement rate:

| Category | % of Fleet | Avg Efficiency | Trend |
|----------|-----------|---------------|-------|
| Recently replaced (0–5 yrs) | ~25% | 90–92% | Stable |
| Mid-life (5–15 yrs) | ~45% | 82–90% | Slowly declining |
| Old, surviving (15+ yrs) | ~30% | 72–82% | Declining |

### Fleet Average Efficiency Trajectory

With default parameters (degradation 0.5%/yr, replacement to 92%, electrification 2%):

| Year | Fleet Avg Efficiency | Change from 2025 |
|------|---------------------|-----------------|
| 2025 | 80.0% | baseline |
| 2027 | 80.8% | +0.8 pp |
| 2030 | 82.0% | +2.0 pp |
| 2033 | 83.2% | +3.2 pp |
| 2035 | 84.0% | +4.0 pp |

The fleet average *increases* over time because the replacement-to-92% effect is stronger than the degradation effect. This is consistent with observed national trends as old 80% AFUE furnaces are replaced with 92%+ condensing units.

---

## Impact on Gas Demand

Higher efficiency means less gas consumed for the same heat output:

```
therms = (HDD × heating_factor × vintage_mult × segment_mult × qty) / efficiency
```

As fleet efficiency rises from 80% to 84%:
- Demand reduction from efficiency alone: (84 − 80) / 80 = **5.0%**
- Combined with electrification (2% of fleet switching to electric over 10 years): ~**6.5% total reduction**

This produces a model UPC decline from ~499 therms (2025) to ~425 therms (2035), a 14.9% decline — steeper than the IRP's 11.3% because the model captures discrete efficiency jumps at replacement time rather than a smooth trend.

---

## Scenario Parameters

These parameters are configurable in the scenario JSON:

```json
{
    "efficiency_improvement": 0.01,
    "electrification_rate": 0.02
}
```

Both support scalar values or year-indexed curves via `src/parameter_curves.py`.

### Sensitivity Analysis

| Parameter | Low | Default | High | Effect on 2035 UPC |
|-----------|-----|---------|------|-------------------|
| `annual_degradation_rate` | 0.002 | 0.005 | 0.010 | ±3–5% |
| `new_equipment_efficiency` | 0.88 | 0.92 | 0.96 | ±2–4% |
| `electrification_rate` | 0.00 | 0.02 | 0.10 | ±1–8% |

The most sensitive parameter is `new_equipment_efficiency` — the code-minimum for new installations. If new furnaces average 96% instead of 92%, the fleet turns over faster toward high efficiency.

---

## Limitations

1. **Uniform degradation** — All equipment degrades at the same rate regardless of maintenance quality, climate severity, or usage intensity. A furnace in the Gorge (high HDD, more run-hours) likely degrades faster than one in Portland.

2. **No repair modeling** — The current implementation does not model partial efficiency recovery from maintenance/repair. Equipment either degrades or gets replaced.

3. **Single new-equipment efficiency** — All replacements get the same efficiency value. In reality, some customers install 80% AFUE (minimum for weatherized units) while others install 96%+ premium models.

4. **No retrofit modeling** — Building envelope improvements (insulation, air sealing, windows) are not modeled. These reduce the heating load independent of equipment efficiency.

5. **Electrification removes gas demand entirely** — The model assumes electrified premises have zero gas space heating demand. In practice, some dual-fuel heat pump systems retain gas backup.

These limitations are documented as future work enhancements.

---

## Related Documentation

- **[FORMULAS.md](FORMULAS.md)** — Mathematical formulas for efficiency calculations
- **[ALGORITHM.md](ALGORITHM.md)** — Full simulation algorithm including equipment replacement loop
