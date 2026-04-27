# Top-Down vs Bottom-Up Forecast Comparison

## Overview

This document compares NW Natural's official IRP (Integrated Resource Plan) top-down forecast against the bottom-up end-use model developed in this project. The two approaches use fundamentally different methodologies to project residential natural gas demand, and the differences in their outputs reveal important insights about the drivers of demand decline.

## Methodology Comparison

### NW Natural IRP (Top-Down)

NW Natural's IRP uses a Use Per Customer (UPC) decay model:

```
UPC(year) = 648 × (1 - 0.0119)^(year - 2025)
```

- Starts from a 2025 baseline of 648 therms/customer/year
- Applies a fixed annual decay rate of -1.19%
- The decay rate is derived from historical UPC trends (2005-2025)
- No visibility into what drives the decline — it's a statistical trend extrapolation
- Includes all residential end-uses (space heating, water heating, cooking, drying, fireplaces, other)

### Bottom-Up End-Use Model

The model simulates demand from first principles:

```
therms = (HDD × heating_factor) / efficiency
```

Then applies year-over-year changes through:
- **Equipment replacement** via Weibull survival model (~5% of fleet per year)
- **Efficiency degradation** at 0.5%/year for aging equipment
- **Repair recovery** at 85% for serviced equipment past half-life
- **New equipment efficiency** at 92% AFUE (current code minimum)
- **Electrification** at 2% of replaced units switching to electric
- **Housing growth** at 1% per year

The model currently simulates space heating only. Non-heating end-uses (water heating, cooking, drying, fireplaces) are estimated using RECS Pacific division proportions.

## Results Comparison

### Space Heating Only (Model Scope)

| Year | Model SH UPC | IRP Total UPC | Model as % of IRP |
|------|-------------|--------------|-------------------|
| 2025 | 499 therms | 648 therms | 77% |
| 2030 | 459 therms | 610 therms | 75% |
| 2035 | 425 therms | 575 therms | 74% |

The model's space heating UPC is 77% of the IRP's total UPC in 2025, declining to 74% by 2035. This is consistent with RECS data showing space heating represents 60-77% of total residential gas consumption in the Pacific Northwest.

### Estimated Total (Model + RECS Non-Heating)

| Year | Model Estimated Total | IRP Total | Difference | Diff % |
|------|----------------------|-----------|-----------|--------|
| 2025 | 819 therms | 648 therms | +171 therms | +26.3% |
| 2027 | 787 therms | 633 therms | +155 therms | +24.4% |
| 2030 | 753 therms | 610 therms | +143 therms | +23.4% |
| 2033 | 722 therms | 589 therms | +133 therms | +22.5% |
| 2035 | 697 therms | 575 therms | +122 therms | +21.2% |

The model's estimated total is 21-26% higher than the IRP, with the gap narrowing over time.

### Decline Rates

| Metric | IRP | Model |
|--------|-----|-------|
| Annual decline rate | -1.19% (fixed) | -1.6% (average, accelerating) |
| 10-year total decline | -11.3% | -14.9% |
| 2025-2030 decline | -5.8% | -8.0% |
| 2030-2035 decline | -5.8% | -7.5% |

The model projects a steeper decline than the IRP, driven by the compounding effects of equipment replacement, efficiency improvements, and electrification.

## Why the Model is Higher

### 1. RECS Non-Heating Estimates Are Inflated

The model estimates non-heating end-uses (water heating, cooking, drying, fireplaces) using RECS 2020 Pacific division ratios. The Pacific division includes California, which has:
- Higher water heating demand (warmer incoming water but more outdoor pools/spas)
- Different cooking patterns
- Lower space heating share (milder climate)

This makes the non-heating-to-space-heating ratio higher than what Oregon/Washington actually experiences. The fix: implement the water heating, cooking, and drying modules using NW Natural's actual billing data and Bull Run water temperature data instead of RECS estimates.

### 2. Partial Year Calibration

The heating factor was calibrated against 2025 billing data, which only covers January-March (the coldest quarter). This partial-year calibration may not perfectly represent the full annual relationship between HDD and therms. A full-year calibration against 2024 data would be more robust.

### 3. No Behavioral Response Modeling

The model assumes constant thermostat behavior and occupancy patterns. In reality, rising gas prices and efficiency awareness may cause customers to reduce consumption beyond what equipment efficiency alone would predict. The IRP's historical decay rate implicitly captures these behavioral effects.

## Why the Model Declines Faster

### 1. Equipment Replacement Creates Step-Changes

When a 25-year-old furnace at 74% AFUE (degraded from 80% rated) gets replaced with a new 92% AFUE unit, that's a 24% efficiency jump for that premise. The IRP's smooth -1.19% decay doesn't capture these discrete jumps — it averages them into a trend.

### 2. Efficiency Degradation Compounds

The model applies 0.5%/year degradation to all equipment. Over 10 years, a non-replaced unit loses ~5% of its efficiency. This creates a growing gap between old and new equipment, making replacements more impactful over time.

### 3. Electrification Removes Gas Load Entirely

When a unit electrifies (2% of replacements), it removes 100% of that premise's gas space heating demand — not just a percentage reduction. This is a stronger effect than the IRP's blended decay rate.

## Key Insight

The narrowing gap (26% → 21%) suggests the two approaches are converging. The model's steeper decline brings its trajectory closer to the IRP over time. If the non-heating estimates were calibrated to NW Natural's actual data instead of RECS averages, the gap would likely close to within 5-10%.

The model's value is not in matching the IRP exactly — it's in providing visibility into the *drivers* of demand decline:
- How much comes from equipment replacement vs degradation vs electrification
- Which customer segments are declining fastest
- What happens under different policy scenarios (higher electrification, stricter efficiency codes)
- Where the IRP's assumptions may be too conservative or too aggressive

## Recommendations

1. **Implement water heating module** using Bull Run water temperature data — this is the largest non-heating end-use (~25% of total) and would replace the RECS estimate with actual physics-based simulation.

2. **Recalibrate heating factor** against a full year of billing data (2024) instead of partial 2025.

3. **Add behavioral response** — a price elasticity parameter that reduces consumption when rates increase.

4. **Run high-electrification scenario** — the model can show what happens at 5% or 10% electrification rates, which the IRP's fixed decay rate cannot.

5. **Validate against 2024 actual billing** — compare the model's 2024 simulation against actual 2024 billing data to quantify the calibration accuracy.
