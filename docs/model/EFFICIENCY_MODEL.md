# Equipment Efficiency Model

## Overview

The model tracks three distinct efficiency states for every piece of equipment in the fleet. Each year, equipment falls into one of three categories based on the Weibull survival model and age:

1. **Aging (no intervention)** — equipment degrades naturally
2. **Repaired** — old equipment gets serviced, partially recovering efficiency
3. **Replaced** — equipment is swapped for a new unit at current code-minimum efficiency

These three states create a realistic distribution of equipment performance across the fleet, rather than assuming all equipment operates at its rated efficiency forever.

---

## The Three Efficiency Tiers

### Tier 1: Aging Equipment (Degradation)

Every piece of equipment loses efficiency each year due to normal wear and tear.

```
degraded_efficiency = current_efficiency × (1 - annual_degradation_rate)
```

**Default:** `annual_degradation_rate = 0.005` (0.5% per year)

**What causes degradation:**
- Heat exchanger fouling and corrosion
- Burner deposits reducing combustion efficiency
- Duct leakage increasing over time (connections loosen, seals fail)
- Thermostat calibration drift
- Fan motor bearing wear (reduced airflow)
- Insulation settling in older homes (increases heat loss, equipment works harder)

**Example:** A furnace rated at 80% AFUE when installed in 2010:
- 2015 (age 5): 80% × (1 - 0.005)^5 = 78.0%
- 2020 (age 10): 80% × (1 - 0.005)^10 = 76.1%
- 2025 (age 15): 80% × (1 - 0.005)^15 = 74.2%

Over 15 years, the furnace has lost ~7% of its rated efficiency. This means it uses ~7% more gas than a new unit of the same model.

### Tier 2: Repaired Equipment (Partial Recovery)

Equipment that is past half its useful life and survives the Weibull replacement draw gets repaired. A repair restores some but not all of the lost efficiency.

```
repaired_efficiency = degraded_efficiency + (degradation_loss × repair_recovery)
```

Where:
- `degradation_loss` = the efficiency lost to degradation this year
- `repair_recovery` = fraction of that loss recovered by repair

**Default:** `repair_efficiency_recovery = 0.85` (85% of annual degradation recovered)

**What a repair includes:**
- Burner cleaning and adjustment
- Heat exchanger cleaning
- Filter replacement
- Thermostat recalibration
- Basic duct sealing
- Safety inspection

**What a repair does NOT fix:**
- Fundamental heat exchanger corrosion
- Duct system deterioration beyond the furnace
- Building envelope degradation
- Outdated control systems
- Oversized equipment (original design issue)

**Example:** That same 15-year-old furnace at 74.2%:
- Annual degradation loss: 74.2% × 0.005 = 0.37%
- Repair recovers: 0.37% × 0.85 = 0.31%
- Post-repair efficiency: 74.2% - 0.37% + 0.31% = 74.1%
- Net annual loss after repair: only 0.06% instead of 0.37%

Repairs slow the degradation significantly but don't stop it entirely.

### Tier 3: Replaced Equipment (New Code-Minimum)

Equipment that fails the Weibull survival draw gets replaced with a brand new unit at the current building code minimum efficiency.

```
new_efficiency = new_equipment_efficiency
```

**Default:** `new_equipment_efficiency = 0.92` (92% AFUE, current code minimum for gas furnaces)

**Why 92%:**
- DOE minimum efficiency standard for residential gas furnaces (effective 2015) is 92% AFUE for non-weatherized units
- Most new installations in the PNW are condensing furnaces at 92-96% AFUE
- 92% is conservative — many new installs are 95-96%

**Example:** That 15-year-old furnace at 74.2% gets replaced:
- Old efficiency: 74.2%
- New efficiency: 92.0%
- Efficiency jump: +17.8 percentage points
- Gas savings: (92 - 74.2) / 74.2 = 24% less gas for the same heat output

This is the primary mechanism driving demand reduction in the model — as old equipment fails and gets replaced with modern high-efficiency units, the fleet average efficiency rises.

---

## How the Three Tiers Interact

Each year, the model processes the entire equipment fleet:

```
Step 1: DEGRADE all equipment
        every unit loses 0.5% efficiency

Step 2: REPAIR old equipment that survived
        units past half their useful life get 85% of the degradation back

Step 3: REPLACE failed equipment
        units that fail Weibull draw get set to 92% efficiency
        (some of these switch to electric via electrification rate)
```

### Fleet Composition Over Time

In a typical year with ~5% replacement rate:

| Category | % of Fleet | Avg Efficiency | Trend |
|----------|-----------|---------------|-------|
| Recently replaced (0-5 yrs) | ~25% | 90-92% | Stable (minimal degradation) |
| Mid-life (5-15 yrs) | ~45% | 82-90% | Slowly declining |
| Old, repaired (15+ yrs) | ~20% | 74-82% | Declining, partially offset by repairs |
| Old, unrepaired (15+ yrs) | ~10% | 70-78% | Declining fastest |

### Fleet Average Efficiency Trajectory

With the default parameters:

```
Year 2025: 80.0% (baseline — all equipment at rated efficiency)
Year 2026: 80.5% (first replacements jump to 92%, offsets degradation)
Year 2027: 81.3% (more replacements accumulate)
...
Year 2035: 84.3% (10 years of fleet turnover)
```

The fleet average *increases* over time because the replacement-to-92% effect is stronger than the degradation effect. This is realistic — the national fleet efficiency has been rising steadily as old 80% AFUE furnaces are replaced with 92%+ condensing units.

---

## Impact on Gas Demand

Higher efficiency means less gas consumed for the same heat output:

```
therms = (HDD × heating_factor) / efficiency
```

As fleet efficiency rises from 80% to 84.3%:
- Demand reduction from efficiency alone: (84.3 - 80.0) / 80.0 = 5.4%
- Combined with electrification (1% of fleet switching to electric): ~6.4% total reduction
- Over 10 years, this produces a UPC decline from 499 to 425 therms (-14.9%)

Compare to NW Natural's IRP forecast: 648 to 575 therms (-11.3% decline). The model's steeper decline is because:
1. The model only covers space heating (IRP includes all end-uses, some of which decline slower)
2. The 92% new-equipment efficiency is a larger jump than the IRP's blended assumption

---

## Scenario Parameters

These three parameters are configurable in the scenario JSON:

```json
{
    "annual_degradation_rate": 0.005,
    "repair_efficiency_recovery": 0.85,
    "new_equipment_efficiency": 0.92
}
```

### Sensitivity Analysis

| Parameter | Low | Default | High | Effect on 2035 UPC |
|-----------|-----|---------|------|-------------------|
| annual_degradation_rate | 0.002 | 0.005 | 0.010 | ±3-5% |
| repair_efficiency_recovery | 0.70 | 0.85 | 0.95 | ±1-2% |
| new_equipment_efficiency | 0.88 | 0.92 | 0.96 | ±2-4% |

The most sensitive parameter is `new_equipment_efficiency` — the code-minimum for new installations. If new furnaces average 96% instead of 92%, the fleet turns over faster toward high efficiency.

---

## Data Sources

| Parameter | Source | Confidence |
|-----------|--------|-----------|
| Degradation rate (0.5%/yr) | DOE/LBNL residential equipment studies, ASHRAE maintenance data | Medium — varies widely by maintenance quality |
| Repair recovery (85%) | Industry rule of thumb — a tune-up recovers most but not all performance | Low — limited empirical data |
| New equipment efficiency (92%) | DOE minimum efficiency standard, ENERGY STAR database | High — regulatory requirement |
| Weibull replacement timing | ASHRAE service life data, DOE/NEMS parameters | Medium — based on median service life |

---

## Limitations

1. **Uniform degradation** — All equipment degrades at the same rate regardless of maintenance quality, climate severity, or usage intensity. In reality, a furnace in the Gorge (high HDD) degrades faster than one in Portland.

2. **Binary repair model** — Equipment is either "repaired" or "not repaired." In reality, there's a spectrum from basic filter changes to full tune-ups to major component replacement.

3. **No efficiency-dependent failure** — The Weibull model doesn't account for efficiency affecting failure probability. In reality, poorly maintained equipment fails sooner.

4. **Single new-equipment efficiency** — All replacements get the same 92%. In reality, some customers install 80% AFUE (minimum for weatherized units) while others install 96%+ premium models.

5. **No retrofit modeling** — Building envelope improvements (insulation, air sealing, windows) are not modeled. These reduce the heating load independent of equipment efficiency.

These limitations are documented as future work enhancements.
