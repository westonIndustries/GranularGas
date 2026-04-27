# NW Natural End-Use Forecasting Model — Runtime Playbook

A step-by-step guide to set up, run, and interpret the bottom-up residential end-use demand forecasting model on a new system.

---

## Part 1: System Setup

### Prerequisites

- **Python 3.9+** (check: `python --version`)
- **8GB+ RAM** (for full dataset processing)
- **~5GB disk space** (for data + outputs)
- **Git** (to clone the repository)
- **pip** (Python package manager)

### Step 1: Clone and Navigate

```bash
git clone <repository-url>
cd nw-natural-forecasting
```

### Step 2: Create Virtual Environment

```bash
# Create isolated Python environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed pandas==1.5.3 numpy==1.24.0 ... (20+ packages)
```

If you see errors, check:
- Python version is 3.9+
- Virtual environment is activated
- Internet connection is available

### Step 4: Verify Data Directory

```bash
# Check that Data/ folder exists with required files
ls -la Data/NWNatural\ Data/

# You should see:
# - premise_data_blinded.csv
# - equipment_data_blinded.csv
# - segment_data_blinded.csv
# - equipment_codes.csv
# - DailyCalDay1985_Mar2025.csv (or DailyGasDay2008_Mar2025.csv)
# - BullRunWaterTemperature.csv
# - Portland_snow.csv
# - billing_data_blinded.csv
```

If files are missing, the model will log warnings but may not run the full simulation.

### Step 5: Create Output Directory

```bash
mkdir -p output
```

---

## Part 2: Running the Model

### Quick Start (Baseline Scenario)

```bash
# Run the full pipeline with default baseline scenario
python -m src.main

# Expected runtime: 2-5 minutes on a laptop with 8GB RAM
```

**What happens:**
1. Loads all data files
2. Builds housing stock model
3. Simulates end-use consumption
4. Aggregates results
5. Generates HTML + Markdown reports

### Monitoring Progress

The model prints progress to console:

```
[2025-04-15 10:30:45] INFO: Loading premise data...
[2025-04-15 10:30:47] INFO: Loaded 487,234 premises
[2025-04-15 10:30:48] INFO: Loading equipment data...
[2025-04-15 10:30:52] INFO: Loaded 1,203,456 equipment units
...
[2025-04-15 10:35:12] INFO: Simulation complete. Total demand: 3,245,678 therms
[2025-04-15 10:35:15] INFO: Results exported to output/
```

### Running the NW Natural Source Data Validation Suite

```bash
# Run all 12 data validation checks with HTML + MD + PNG output
python -m src.validation.nwn_data_validation

# Expected runtime: 5-12 minutes (loads all NW Natural source files)
```

**What happens:**
1. Runs 12 validation checks across all NW Natural source data
2. Generates HTML + Markdown reports with embedded charts
3. Exports CSV files for flagged records (duplicates, suspicious quantities)
4. Produces a summary dashboard linking all individual reports

**Output:** `output/nwn_data_validation/` (see Part 3 for full listing)

### Running Specific Scenarios

```bash
# Run high electrification scenario
python -m src.main --scenario scenarios/high_electrification.json

# Run baseline only (skip simulation, just load data)
python -m src.main --baseline-only

# Compare multiple scenarios
python -m src.main --compare scenarios/baseline.json scenarios/high_electrification.json
```

---

## Part 3: Understanding the Output Structure

After running, check the `output/` directory:

```
output/
├── config_validation/           # Configuration validation tests
│   ├── config_completeness.html
│   └── config_completeness.md
├── data_quality/                # Data ingestion quality reports
│   ├── premise_data_quality_report.html
│   ├── equipment_data_quality_report.html
│   ├── join_audit.html
│   ├── validation_failures.csv
│   ├── column_coverage.html
│   ├── date_ranges.html
│   ├── distribution_summary.html
│   └── distributions/           # PNG charts
├── join_integrity/              # Join validation reports
│   ├── joined_table_quality_report.html
│   ├── enduse_mapping_audit.html
│   ├── efficiency_validation.html
│   ├── weather_station_audit.html
│   └── join_integrity_dashboard.html
├── nwn_data_validation/          # NW Natural source data validation (Task 15)
│   ├── validation_dashboard.html  # Summary dashboard with all 12 checks
│   ├── validation_dashboard.md
│   ├── referential_integrity.html # 15.1 Orphan blinded_ids across tables
│   ├── equipment_code_validity.html # 15.2 Equipment codes vs equipment_codes.csv
│   ├── duplicate_detection.html   # 15.3 Duplicate premise-equipment rows
│   ├── duplicate_equipment.csv    # Export of all duplicate rows
│   ├── weather_station_coverage.html # 15.4 District → weather station mapping
│   ├── billing_coverage.html      # 15.5 Billing data coverage by premise/district
│   ├── weather_continuity.html    # 15.6 Missing dates and gaps per station
│   ├── segment_consistency.html   # 15.7 One segment per premise check
│   ├── equipment_quantity.html    # 15.8 QTY sanity (suspicious values)
│   ├── suspicious_quantities.csv  # Export of QTY > 5 rows
│   ├── state_district_crosscheck.html # 15.9 OR/WA state vs district consistency
│   ├── billing_reasonableness.html # 15.10 Therm values < 1 or > 500
│   ├── temperature_bounds.html    # 15.11 Temps outside -10°F to 115°F
│   ├── temporal_alignment.html    # 15.12 Date range overlap across datasets
│   └── *.png                      # Charts embedded in reports
├── checkpoint_ingestion/        # Data ingestion checkpoint
│   ├── pipeline_readiness.html
│   ├── data_volumes.html
│   ├── pet_profile.html
│   ├── service_territory_map.html
│   ├── equipment_vintage_charts.html
│   └── cross_validation.html
├── housing_stock_projections/   # Housing stock tests
│   └── property4_results.html
├── equipment_replacement/       # Equipment replacement tests
│   └── property5_results.html
├── fuel_switching/              # Fuel switching tests
│   └── property6_results.html
├── weather_analysis/            # Weather processing tests
│   └── property7_results.html
├── water_heating/               # Water heating tests
│   └── property8_results.html
├── checkpoint_core/             # Core model verification
│   ├── housing_verification.html
│   ├── equipment_verification.html
│   ├── weather_verification.html
│   └── zone_verification_map.html
├── simulation/                  # Simulation tests
│   ├── property9_results.html
│   └── property10_results.html
├── aggregation/                 # Aggregation tests
│   ├── property11_results.html
│   └── property12_results.html
├── scenarios/                   # Scenario tests
│   ├── property13_results.html
│   └── property14_results.html
├── integration/                 # Integration tests
│   └── pipeline_test.html
└── checkpoint_final/            # Final results
    ├── baseline_results.html
    ├── scenario_comparison.html
    └── final_dashboard.html
```

---

## Part 4: Interpreting the Tests

The model runs 14 property-based tests that validate correctness. Here's what each one means:

**Note:** The current scope includes space heating only (furnaces, boilers, heat pumps). Water heating, cooking, clothes drying, fireplaces/decorative, and other/miscellaneous end-uses are excluded and planned for future work.

### Phase 1: Configuration & Data Ingestion

#### **Property 1: Configuration Completeness**
📁 `output/config_validation/config_completeness.html`

**What it tests:** All equipment codes map to valid end-use categories, efficiency values are in valid ranges, file paths exist.

**How to read it:**
- ✅ **Green** — All checks passed. Configuration is complete.
- ⚠️ **Yellow** — Some file paths missing (non-critical). Model will still run.
- ❌ **Red** — Critical configuration missing. Fix before running simulation.

**Example output:**
```
✅ END_USE_MAP completeness: 156/156 equipment codes mapped
✅ DEFAULT_EFFICIENCY values: All in (0, 1] range
✅ DISTRICT_WEATHER_MAP: 47/47 districts mapped
⚠️ File paths: 51/53 files found (2 optional files missing)
```

**Action:** If red, check `src/config.py` for missing constants.

---

#### **Property 2: Data Filtering**
📁 `output/data_quality/` (multiple reports)

**What it tests:** Only active residential premises are loaded (custtype='R', status_code='AC').

**How to read it:**
- Look at `premise_data_quality_report.html`
- Check the "Filter Pass Rate" section

**Example output:**
```
Total premises loaded: 512,456
Active residential (custtype='R', status_code='AC'): 487,234
Filter pass rate: 95.1% ✅

Flagged rows (inactive/commercial): 25,222
```

**Action:** 
- 90%+ pass rate = ✅ Good. Data is clean.
- 70-90% = ⚠️ Investigate. Some data quality issues.
- <70% = ❌ Problem. Check data source.

---

#### **Property 3: Join Integrity**
📁 `output/join_integrity/join_integrity_dashboard.html`

**What it tests:** Every premise-equipment row has a valid end-use and efficiency > 0.

**How to read it:**
- Open the dashboard. Look for traffic lights (🟢 green, 🟡 yellow, 🔴 red).
- Check the "Join Integrity Summary" section.

**Example output:**
```
Rows with non-null end_use: 1,203,456 / 1,203,456 (100%) 🟢
Rows with efficiency > 0: 1,203,456 / 1,203,456 (100%) 🟢
Join expansion factor: 2.47 (equipment per premise)
```

**Action:**
- 100% = ✅ Perfect. All equipment is valid.
- 95-99% = ⚠️ Minor issues. Check `output/data_quality/validation_failures.csv` for details.
- <95% = ❌ Significant issues. Investigate before proceeding.

---

### Phase 1.5: NW Natural Source Data Validation (Task 15)

#### **Validation Dashboard**
📁 `output/nwn_data_validation/validation_dashboard.html`

**What it tests:** 12 checks covering referential integrity, code validity, duplicates, weather coverage, billing coverage, date continuity, segment consistency, quantity sanity, state-district alignment, billing reasonableness, temperature bounds, and temporal alignment.

**How to read it:**
- Open the dashboard — each row shows a check name, status (OK / SKIPPED / ERROR), and details.
- Click any check name to open its detailed report with charts.

**Individual checks at a glance:**

| Check | What it catches | Key metric |
|-------|----------------|------------|
| 15.1 Referential Integrity | Orphan blinded_ids in equipment/segment/billing | Match rate per table |
| 15.2 Equipment Code Validity | Unknown equipment_type_codes | % valid codes |
| 15.3 Duplicate Detection | Exact duplicate equipment rows | Duplication rate |
| 15.4 Weather Station Coverage | Unmapped districts | Unmapped premise count |
| 15.5 Billing Coverage | Premises without billing data | Coverage % |
| 15.6 Weather Continuity | Missing dates in weather time series | Gap count per station |
| 15.7 Segment Consistency | Premises with 0 or 2+ segments | Count by category |
| 15.8 Equipment Quantity | QTY ≤ 0 or > 5 | Suspicious row count |
| 15.9 State-District Cross-Check | OR district with WA state (or vice versa) | Mismatch count |
| 15.10 Billing Reasonableness | Therms < 1 or > 500 per period | % flagged |
| 15.11 Temperature Bounds | Temps outside -10°F to 115°F | Out-of-range count |
| 15.12 Temporal Alignment | Date range gaps between datasets | Overlap period |

**Action:**
- All 12 checks OK = ✅ Source data is clean and consistent.
- Some checks SKIPPED = ⚠️ Data files missing — model will still run but with gaps.
- Any check ERROR = ❌ Investigate the detailed report before trusting simulation results.

**Exported files to review:**
- `duplicate_equipment.csv` — All duplicate rows (check for data entry errors)
- `suspicious_quantities.csv` — Equipment with QTY > 5 (verify these are real)

---

### Phase 2: Core Model Components

#### **Property 4: Housing Stock Projection**
📁 `output/housing_stock_projections/property4_results.html`

**What it tests:** Projected housing units follow the formula: `projected = baseline × (1 + growth_rate)^years`

**How to read it:**
- Look at the line graph: "Baseline vs Projected Total Units"
- Check the "Projection Accuracy" table

**Example output:**
```
Baseline (2025): 487,234 units
Growth rate: 1.2% per year
Projected 2035: 549,876 units
Formula check: 487,234 × (1.012)^10 = 549,876 ✅
```

**Action:**
- If line is straight and matches formula = ✅ Correct.
- If line is curved or doesn't match = ❌ Bug in projection logic.

---

#### **Property 5: Weibull Survival Monotonicity**
📁 `output/equipment_replacement/property5_results.html`

**What it tests:** Equipment survival probability decreases with age (S(t) ≤ S(t-1)), and replacement probability is always in [0, 1].

**How to read it:**
- Look at the "Weibull Survival Curves" graph
- Check the "Replacement Probability Bounds" table

**Example output:**
```
Space heating (furnace):
  Age 0: S(0) = 1.00, P(replace) = 0.00 ✅
  Age 10: S(10) = 0.87, P(replace) = 0.13 ✅
  Age 20: S(20) = 0.42, P(replace) = 0.58 ✅
  Age 30: S(30) = 0.05, P(replace) = 0.95 ✅

All replacement probabilities in [0, 1]: ✅
```

**Action:**
- If curves are monotonically decreasing = ✅ Correct.
- If curves increase or go negative = ❌ Bug in Weibull function.

---

#### **Property 6: Fuel Switching Conservation**
📁 `output/fuel_switching/property6_results.html`

**What it tests:** Total equipment count is conserved before and after replacements (no equipment lost or created).

**How to read it:**
- Look at the "Equipment Count Conservation" table
- Check the pie charts: "Fuel Type Split Before vs After"

**Example output:**
```
Before replacements: 1,203,456 units
After replacements: 1,203,456 units
Difference: 0 ✅

Fuel type split:
  Before: Gas 78%, Electric 22%
  After: Gas 75%, Electric 25%
  (Difference is fuel switching, not equipment loss)
```

**Action:**
- If before == after = ✅ Correct.
- If after < before = ❌ Equipment disappeared (bug).
- If after > before = ❌ Equipment created (bug).

---

#### **Property 7: HDD Computation**
📁 `output/weather_analysis/property7_results.html`

**What it tests:** Heating Degree Days (HDD) are non-negative and exactly one of HDD/CDD is positive (or both zero at base temp).

**How to read it:**
- Look at the "Daily HDD and CDD" graph
- Check the "HDD Bounds Check" table

**Example output:**
```
Daily HDD check (base 65°F):
  Min HDD: 0.0 ✅
  Max HDD: 45.2 ✅
  All HDD >= 0: ✅

HDD/CDD exclusivity:
  Days with HDD > 0 and CDD > 0: 0 ✅
  Days with HDD = 0 and CDD = 0: 0 ✅
```

**Action:**
- If all checks pass = ✅ Weather data is correct.
- If HDD < 0 = ❌ Bug in HDD calculation.
- If both HDD and CDD > 0 = ❌ Data error or calculation bug.

---

#### **Property 8: Water Heating Delta-T**
📁 `output/water_heating/property8_results.html`

**Status:** ⏸️ **EXCLUDED FROM CURRENT SCOPE** — Planned for future work

This test is not run in the current version. Water heating simulation is planned for Phase 2 of development.

---

### Phase 3: Simulation & Aggregation

#### **Property 9: Simulation Non-Negativity**
📁 `output/simulation/property9_results.html`

**What it tests:** All simulated annual therms are non-negative (no negative consumption).

**How to read it:**
- Look at the "Annual Therms Distribution" histogram
- Check the "Non-Negativity Check" table

**Example output:**
```
Total simulated therms: 2,100,000,000 (space heating only)
Min therms per premise: 0.0 ✅
Max therms per premise: 2,456.3 ✅
All therms >= 0: ✅

By end-use (current scope):
  Space heating: 2,100,000,000 therms (100%)

Note: Water heating, cooking, and drying are excluded from current scope
```

**Action:**
- If all therms ≥ 0 = ✅ Correct.
- If any therms < 0 = ❌ Bug in simulation logic.

---

#### **Property 10: Efficiency Impact Monotonicity**
📁 `output/simulation/property10_results.html`

**What it tests:** Higher efficiency equipment produces lower or equal therms (efficiency improvement reduces consumption).

**How to read it:**
- Look at the "Therms vs Efficiency" scatter plot
- Check the "Efficiency Impact" table

**Example output:**
```
Space heating:
  Efficiency 0.70 (old furnace): avg 1,200 therms/yr
  Efficiency 0.85 (standard): avg 1,000 therms/yr
  Efficiency 0.95 (high-eff): avg 850 therms/yr
  Trend: ✅ Monotonically decreasing

Water heating:
  Efficiency 0.50 (old tank): avg 450 therms/yr
  Efficiency 0.80 (standard): avg 280 therms/yr
  Efficiency 0.95 (tankless): avg 240 therms/yr
  Trend: ✅ Monotonically decreasing
```

**Action:**
- If all trends are decreasing = ✅ Correct.
- If any trend increases = ❌ Bug in efficiency scaling.

---

#### **Property 11: Aggregation Conservation**
📁 `output/aggregation/property11_results.html`

**What it tests:** Sum of end-use demand equals total demand (no therms lost or created during aggregation).

**How to read it:**
- Look at the "Aggregation Conservation" waterfall chart
- Check the "Conservation Check" table

**Example output:**
```
Space heating: 2,100,000,000 therms
Water heating: 650,000,000 therms
Cooking: 180,000,000 therms
Drying: 150,000,000 therms
Other: 165,678,234 therms
─────────────────────────────
Total: 3,245,678,234 therms ✅

Difference (should be 0): 0 therms ✅
```

**Action:**
- If total matches sum = ✅ Correct.
- If difference > 0 = ❌ Therms created (bug).
- If difference < 0 = ❌ Therms lost (bug).

---

#### **Property 12: Use-Per-Customer (UPC)**
📁 `output/aggregation/property12_results.html`

**What it tests:** UPC = total demand / customer count, and handles edge cases (count = 0).

**How to read it:**
- Look at the "Model UPC vs IRP Forecast" line graph
- Check the "UPC Calculation" table

**Example output:**
```
Total demand (2025): 2,100,000,000 therms (space heating only)
Total customers: 487,234
Calculated UPC: 4.31 therms/customer/year

IRP forecast UPC (2025): 6.48 therms/customer/year
Model vs IRP difference: -33.6% (expected, as model covers space heating only)

Note: Current model scope is space heating only. Full UPC will include water heating,
cooking, and drying in future phases.
```

**Action:**
- If model UPC is within ±5% of IRP = ✅ Good calibration.
- If model UPC is ±5-10% of IRP = ⚠️ Acceptable. Check assumptions.
- If model UPC is >±10% of IRP = ❌ Investigate. May need recalibration.

---

### Phase 4: Scenarios & Integration

#### **Property 13: Scenario Determinism**
📁 `output/scenarios/property13_results.html`

**What it tests:** Running the same scenario twice produces identical results (deterministic).

**How to read it:**
- Look at the "Run Comparison" table
- Check the "Max Absolute Difference" row

**Example output:**
```
Run 1 (2025): 6.66 therms/customer
Run 2 (2025): 6.66 therms/customer
Difference: 0.00 ✅

Max absolute difference across all years: 0.00 ✅
Determinism check: ✅ PASS
```

**Action:**
- If difference = 0 = ✅ Correct. Model is deterministic.
- If difference > 0 = ❌ Non-deterministic behavior (bug or randomness).

---

#### **Property 14: Scenario Validation**
📁 `output/scenarios/property14_results.html`

**What it tests:** Scenario validation catches invalid parameters (rates outside [0,1], horizon ≤ 0).

**How to read it:**
- Look at the "Validation Test Cases" table
- Check the "Expected vs Actual" results

**Example output:**
```
Test case 1: electrification_rate = 0.5 (valid)
  Expected: ✅ PASS
  Actual: ✅ PASS ✅

Test case 2: electrification_rate = 1.5 (invalid, > 1)
  Expected: ❌ FAIL with warning
  Actual: ❌ FAIL with warning ✅

Test case 3: forecast_horizon = -5 (invalid, < 0)
  Expected: ❌ FAIL with warning
  Actual: ❌ FAIL with warning ✅

All validation tests: ✅ PASS
```

**Action:**
- If all tests pass = ✅ Validation logic is correct.
- If any test fails = ❌ Validation logic has bugs.

---

### Phase 5: Final Results

#### **Checkpoint: Final Dashboard**
📁 `output/checkpoint_final/final_dashboard.html`

**What it shows:**
- Summary of all 14 property tests (pass/fail)
- Key metrics: total demand, UPC, demand by end-use
- Known limitations and data gaps
- Recommendations for next steps

**How to read it:**
1. **Test Summary** — All tests should be 🟢 green.
2. **Key Metrics** — Compare to IRP forecast and historical data.
3. **Limitations** — Understand what the model can and cannot do.

**Example output:**
```
═══════════════════════════════════════════════════════════
FINAL VALIDATION DASHBOARD
═══════════════════════════════════════════════════════════

Property Tests (13 total - Property 8 excluded from current scope):
  ✅ Property 1: Configuration Completeness
  ✅ Property 2: Data Filtering
  ✅ Property 3: Join Integrity
  ✅ Property 4: Housing Stock Projection
  ✅ Property 5: Weibull Survival Monotonicity
  ✅ Property 6: Fuel Switching Conservation
  ✅ Property 7: HDD Computation
  ⏸️ Property 8: Water Heating Delta-T (excluded - future work)
  ✅ Property 9: Simulation Non-Negativity
  ✅ Property 10: Efficiency Impact Monotonicity
  ✅ Property 11: Aggregation Conservation
  ✅ Property 12: Use-Per-Customer
  ✅ Property 13: Scenario Determinism
  ✅ Property 14: Scenario Validation

Overall Status: ✅ ALL TESTS PASSED (13/13 active tests)

Key Metrics (2025 Baseline - Space Heating Only):
  Total demand: 2,100,000,000 therms
  Use per customer: 4.31 therms/yr
  Model vs IRP: -33.6% (expected - space heating only)

Demand by end-use (current scope):
  Space heating: 100%

Known Limitations:
  - Model is for illustrative/academic purposes only
  - Current scope: Space heating only
  - Water heating, cooking, and drying excluded (planned for Phase 2)
  - Assumes constant weather (NOAA normals)
  - Does not account for behavioral changes
  - Equipment efficiency data from ASHRAE (may vary by region)

Next Steps:
  1. Review scenario assumptions in scenarios/baseline.json
  2. Run high_electrification scenario for comparison
  3. Validate space heating results against utility billing data
  4. Plan Phase 2 work for water heating, cooking, and drying
```

**Action:**
- If all tests are 🟢 = ✅ Model is ready for analysis.
- If any test is 🔴 = ❌ Fix issues before using results.

---

## Part 5: Troubleshooting

### Issue: "FileNotFoundError: Data/NWNatural Data/premise_data_blinded.csv"

**Cause:** Data files are missing or in wrong location.

**Fix:**
```bash
# Check data directory structure
ls -la Data/NWNatural\ Data/

# If files are missing, copy them from the source
# (Ask your data provider for the files)
```

---

### Issue: "MemoryError: Unable to allocate X GB"

**Cause:** Not enough RAM to load all data.

**Fix:**
```bash
# Run with smaller dataset (if available)
python -m src.main --baseline-only

# Or increase system RAM
# (Minimum 8GB recommended, 16GB preferred)
```

---

### Issue: "Property test failed: All therms >= 0"

**Cause:** Simulation produced negative consumption (bug).

**Fix:**
1. Check `output/simulation/property9_results.html` for details
2. Look for premises with negative therms
3. Check if efficiency values are > 1.0 (invalid)
4. Review simulation logic in `src/simulation.py`

---

### Issue: "Model UPC is >10% different from IRP forecast"

**Cause:** Model assumptions don't match historical data.

**Fix:**
1. Check `output/checkpoint_simulation/irp_comparison.html`
2. Review baseline assumptions in `scenarios/baseline.json`
3. Check data quality reports in `output/data_quality/`
4. Adjust parameters (e.g., efficiency, baseload factors)
5. Re-run simulation

---

## Part 6: Next Steps

### After First Run

1. **Review all checkpoint reports** in `output/checkpoint_final/`
2. **Check property test results** — all should be 🟢 green
3. **Compare to IRP forecast** — model UPC should be within ±5%
4. **Validate against billing data** — check `output/checkpoint_simulation/billing_calibration.html`

### Running Scenarios

```bash
# Run high electrification scenario
python -m src.main --scenario scenarios/high_electrification.json

# Compare baseline vs high electrification
python -m src.main --compare scenarios/baseline.json scenarios/high_electrification.json
```

### Customizing Scenarios

Edit `scenarios/baseline.json`:

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
- `housing_growth_rate`: Annual housing unit growth (0.012 = 1.2%)
- `electrification_rate`: Annual gas-to-electric switching (0.02 = 2%)
- `efficiency_improvement`: Annual efficiency gain (0.015 = 1.5%)
- `weather_assumption`: "normal", "warm", or "cold"

---

## Part 7: Key Metrics to Watch

### Use Per Customer (UPC)

**What it is:** Average annual natural gas consumption per residential customer (therms/year).

**Why it matters:** Primary metric for utility planning and forecasting.

**Typical values:**
- Pre-2010 homes: 8.0-8.5 therms/yr (older, less efficient)
- 2011-2019 homes: 7.0-7.5 therms/yr (modern, efficient)
- 2020+ homes: 6.0-6.5 therms/yr (new, very efficient)
- System average: 6.5-7.0 therms/yr

**How to interpret:**
- If model UPC < historical = ✅ Good. Efficiency improvements are working.
- If model UPC > historical = ⚠️ Check assumptions. May be too conservative.
- If model UPC matches IRP = ✅ Good calibration.

---

### End-Use Breakdown

**Typical split (current scope - space heating only):**
- Space heating: 100% (all demand in current model)

**Future phases will add:**
- Water heating: 15-25% (Phase 2)
- Cooking: 5-8% (Phase 2)
- Drying: 3-5% (Phase 2)
- Fireplaces/decorative: 2-4% (Phase 2)
- Other/miscellaneous: 1-3% (Phase 2)

**How to interpret:**
- Current model shows space heating demand only
- Full system demand will be higher when other end-uses are added
- Space heating typically represents 60-70% of total residential gas demand

---

### Electrification Impact

**What to expect (space heating only):**
- Each 1% electrification rate = 0.5-1.0% reduction in gas space heating demand
- Heat pump adoption reduces space heating by 30-50%
- Full electrification impact will be higher when water heating is added

**How to interpret:**
- If high electrification scenario shows <5% reduction = ⚠️ Check adoption rates.
- If high electrification scenario shows >20% reduction = ✅ Realistic for space heating.
- Note: Full system electrification impact will be larger in Phase 2

---

## Part 8: Quick Reference

### Command Cheat Sheet

```bash
# Activate environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run baseline
python -m src.main

# Run specific scenario
python -m src.main --scenario scenarios/high_electrification.json

# Compare scenarios
python -m src.main --compare scenarios/baseline.json scenarios/high_electrification.json

# Data ingestion only
python -m src.main --baseline-only

# Run individual data loader
python -m src.loaders.load_premise_data

# Run NW Natural source data validation suite (12 checks)
python -m src.validation.nwn_data_validation

# Run tests
pytest tests/ -v
```

---

### Output File Quick Reference

| File | Purpose | Key Metric |
|------|---------|-----------|
| `validation_dashboard.html` | NW Natural source data validation | All 12 checks OK? |
| `config_completeness.html` | Configuration validation | All constants defined? |
| `join_integrity_dashboard.html` | Data quality | 100% valid end-uses? |
| `property12_results.html` | UPC calculation | Model vs IRP match? |
| `irp_comparison.html` | Forecast comparison | Within ±5% of IRP? |
| `billing_calibration.html` | Billing validation | R² > 0.8? |
| `final_dashboard.html` | Overall status | All tests pass? |

---

### Interpretation Quick Guide

| Metric | Good | Acceptable | Problem |
|--------|------|-----------|---------|
| Property tests | All 🟢 | 1-2 🟡 | Any 🔴 |
| Source data validation | 12/12 OK | 10-11 OK | <10 OK |
| Model vs IRP UPC | ±2% | ±5% | >±10% |
| Billing R² | >0.85 | 0.75-0.85 | <0.75 |
| Data filter rate | >95% | 85-95% | <85% |
| Join integrity | 100% | 99%+ | <99% |

---

## Support & Questions

If you encounter issues:

1. **Check the logs** — Look for ERROR or WARNING messages
2. **Review property test results** — They indicate where problems are
3. **Check data quality reports** — Look for missing or invalid data
4. **Verify assumptions** — Review scenario parameters and defaults
5. **Contact the development team** — Provide error messages and output files

---

**Last Updated:** April 2025  
**Model Version:** 1.0  
**Status:** Production Ready
