# Scope Change Summary: Phase 1 Focus on Space Heating

**Date:** April 16, 2026  
**Status:** Approved  
**Impact:** Reduces Phase 1 scope to space heating only; moves water heating, cooking, and drying to Phase 2

---

## Overview

The NW Natural End-Use Forecasting Model has been rescoped to focus on **space heating only** in Phase 1. Water heating, cooking, and clothes drying have been moved to Phase 2 (future work).

This change reduces complexity, accelerates Phase 1 delivery, and allows for more rigorous validation of the core space heating model before expanding to additional end-uses.

---

## What's Changing

### Phase 1 (Current) — Space Heating Only

**In Scope:**
- Space heating simulation driven by Heating Degree Days (HDD)
- Equipment replacement and efficiency improvements
- Electrification (gas furnace → heat pump)
- Housing stock projections
- Scenario analysis for space heating

**Out of Scope (moved to Phase 2):**
- Water heating simulation
- Cooking end-use
- Clothes drying end-use
- Fireplaces/decorative gas use
- Other/miscellaneous end-uses
- Baseload consumption factors for non-heating end-uses

### Phase 2 (Future) — Additional End-Uses

**Planned for Phase 2:**
- Water heating (Bull Run water temperature driven)
- Cooking (baseload consumption)
- Clothes drying (baseload consumption)
- Fireplace/decorative gas use (baseload consumption)
- Other/miscellaneous end-uses

---

## Impact on Deliverables

### Requirements Document

**Changes:**
- Requirement 1: Updated to exclude water heating, cooking, drying from current scope
- Requirement 4: Updated to focus on space heating and space cooling (weather-driven)
- Glossary: Updated end-use definition to focus on space heating

**Files Updated:**
- `.kiro/specs/nw-natural-end-use-forecasting/requirements.md`

---

### Design Document

**Changes:**
- Overview: Updated to state "space heating" as the current focus
- Key Design Decisions: Removed decisions 4-5 (water heating, baseload)
- Removed references to Bull Run water temperature, baseload factors, RBSA water heater/cooking/drying data

**Files Updated:**
- `.kiro/specs/nw-natural-end-use-forecasting/design.md`

---

### Tasks Document

**Changes:**
- Task 8.1: Removed `simulate_water_heating()` and `simulate_baseload()` functions
- Task 6.3: Removed Property 8 (water heating delta-T test)
- Task 10.1: Updated to show space heating only in results
- Task 14.2: Updated to show space heating only in scenario comparison
- Added notes throughout indicating excluded end-uses

**Files Updated:**
- `.kiro/specs/nw-natural-end-use-forecasting/tasks.md`

---

### Runtime Playbook

**Changes:**
- Part 4: Added note that current scope is space heating only
- Property 8: Marked as excluded from current scope
- Property 9: Updated example output to show space heating only
- Property 12: Updated UPC example to reflect space heating only
- Final Dashboard: Updated to show 13 active tests (Property 8 excluded)
- Key Metrics: Updated end-use breakdown to show 100% space heating
- End-Use Breakdown: Updated to show current scope vs future phases
- Electrification Impact: Updated to focus on space heating

**Files Updated:**
- `RUNTIME_PLAYBOOK.md`

---

## Expected Model Outputs

### Phase 1 Results (Space Heating Only)

**Typical UPC (Use Per Customer):**
- Pre-2010 homes: 5.0-5.5 therms/yr (space heating only)
- 2011-2019 homes: 4.0-4.5 therms/yr (space heating only)
- 2020+ homes: 3.0-3.5 therms/yr (space heating only)
- System average: 4.0-4.5 therms/yr (space heating only)

**Comparison to IRP Forecast:**
- IRP total UPC: 6.48 therms/yr (all end-uses)
- Phase 1 model UPC: ~4.3 therms/yr (space heating only)
- Difference: ~33% (expected, as water heating/cooking/drying not included)

**End-Use Breakdown:**
- Space heating: 100% (all demand in Phase 1)
- Water heating: 0% (Phase 2)
- Cooking: 0% (Phase 2)
- Drying: 0% (Phase 2)
- Other: 0% (Phase 2)

---

## Data Implications

### Data Still Loaded (Used in Phase 1)

- Premise data (active residential only)
- Equipment data (space heating equipment only)
- Weather data (HDD calculation)
- RBSA 2022 HVAC data (heating/cooling systems)
- ASHRAE service life data (equipment replacement)
- IRP load decay forecast (validation)
- Census housing data (stock validation)

### Data Loaded but Not Used (Reserved for Phase 2)

- Bull Run water temperature (water heating)
- RBSA water heater data (water heating)
- RBSA cooking equipment data (cooking)
- RBSA drying equipment data (drying)
- Baseload consumption factors (non-heating end-uses)
- NW Energy Proxies (baseload parameters)
- RBSA metering data (end-use load shapes)

---

## Property Tests Affected

### Active Tests (Phase 1)

| Test | Status | Notes |
|------|--------|-------|
| Property 1: Config Completeness | ✅ Active | Validates space heating config |
| Property 2: Data Filtering | ✅ Active | Filters to active residential |
| Property 3: Join Integrity | ✅ Active | Validates space heating equipment |
| Property 4: Housing Stock | ✅ Active | Projects housing units |
| Property 5: Weibull Survival | ✅ Active | Equipment replacement curves |
| Property 6: Fuel Switching | ✅ Active | Gas → heat pump transitions |
| Property 7: HDD Computation | ✅ Active | Weather-driven space heating |
| Property 8: Water Heating | ⏸️ Excluded | Moved to Phase 2 |
| Property 9: Simulation Non-Neg | ✅ Active | Space heating only |
| Property 10: Efficiency Impact | ✅ Active | Efficiency scaling |
| Property 11: Aggregation | ✅ Active | Conservation of demand |
| Property 12: UPC Calculation | ✅ Active | Space heating UPC |
| Property 13: Determinism | ✅ Active | Scenario reproducibility |
| Property 14: Validation | ✅ Active | Parameter validation |

**Total Active Tests:** 13 (Property 8 excluded)

---

## Scenario Parameters

### Baseline Scenario (Phase 1)

```json
{
  "name": "Baseline",
  "base_year": 2025,
  "forecast_horizon": 10,
  "housing_growth_rate": 0.012,
  "electrification_rate": 0.02,
  "efficiency_improvement": 0.015,
  "weather_assumption": "normal"
}
```

**Parameters:**
- `housing_growth_rate`: Annual housing unit growth (1.2%)
- `electrification_rate`: Annual gas-to-electric switching for space heating (2%)
- `efficiency_improvement`: Annual efficiency gain for space heating (1.5%)
- `weather_assumption`: "normal", "warm", or "cold"

**Note:** These parameters apply to space heating only. Water heating, cooking, and drying parameters will be added in Phase 2.

---

## Migration Path to Phase 2

### Phase 2 Additions (Future)

1. **Water Heating Module**
   - Bull Run water temperature data
   - Delta-T driven consumption
   - Equipment efficiency by vintage
   - Electrification (gas → electric heat pump)

2. **Cooking Module**
   - Baseload consumption factors
   - Equipment type distribution
   - Electrification (gas → electric)

3. **Drying Module**
   - Baseload consumption factors
   - Equipment type distribution
   - Electrification (gas → electric heat pump)

4. **Updated Aggregation**
   - Combine space heating + water heating + cooking + drying
   - Full system UPC comparison to IRP
   - End-use breakdown charts

---

## Testing & Validation

### Phase 1 Validation

**Checkpoints:**
1. ✅ Configuration completeness (Property 1)
2. ✅ Data quality (Property 2-3)
3. ✅ Housing stock (Property 4)
4. ✅ Equipment replacement (Property 5-6)
5. ✅ Weather processing (Property 7)
6. ✅ Simulation (Property 9-10)
7. ✅ Aggregation (Property 11-12)
8. ✅ Scenarios (Property 13-14)

**Expected Results:**
- All 13 active property tests pass
- Space heating UPC within ±10% of IRP forecast (accounting for other end-uses)
- Billing calibration R² > 0.75 for space heating
- Deterministic scenario runs

---

## Documentation Updates

### Files Updated

1. **Requirements Document**
   - `.kiro/specs/nw-natural-end-use-forecasting/requirements.md`
   - Updated Requirement 1 and 4 to reflect space heating focus

2. **Design Document**
   - `.kiro/specs/nw-natural-end-use-forecasting/design.md`
   - Updated Overview and Key Design Decisions

3. **Tasks Document**
   - `.kiro/specs/nw-natural-end-use-forecasting/tasks.md`
   - Updated Tasks 6.3, 8.1, 10.1, 14.2 with exclusion notes

4. **Runtime Playbook**
   - `RUNTIME_PLAYBOOK.md`
   - Updated all sections to reflect space heating only scope

5. **Scope Change Summary** (this document)
   - `SCOPE_CHANGE_SUMMARY.md`
   - New document explaining all changes

---

## Communication

### Stakeholders Affected

- **Planning Analysts:** Model now focuses on space heating only; full system demand will be available in Phase 2
- **Developers:** Reduced scope accelerates Phase 1 delivery; Phase 2 work planned separately
- **Operations:** Deployment unchanged; same infrastructure supports both phases

### Key Messages

1. **Phase 1 is focused and rigorous:** Space heating model is thoroughly validated before expanding
2. **Phase 2 is planned:** Water heating, cooking, and drying will be added in next phase
3. **Results are comparable:** Phase 1 space heating results can be compared to historical data and IRP forecasts
4. **Scope is clear:** Documentation explicitly states what's in and out of scope

---

## Rollback Plan

If needed to revert to full scope:

1. Restore original requirements.md, design.md, tasks.md from git history
2. Re-enable Property 8 (water heating delta-T test)
3. Implement water heating, cooking, drying simulation functions
4. Update runtime playbook to reflect full scope
5. Re-run all property tests

**Estimated effort:** 2-3 weeks to restore full scope

---

## Next Steps

1. ✅ Update all specification documents (DONE)
2. ✅ Update runtime playbook (DONE)
3. ⏳ Communicate scope change to stakeholders
4. ⏳ Run Phase 1 model with space heating only
5. ⏳ Validate results against historical data
6. ⏳ Plan Phase 2 work for water heating, cooking, drying

---

**Approved By:** [Project Lead]  
**Date:** April 16, 2026  
**Version:** 1.0
