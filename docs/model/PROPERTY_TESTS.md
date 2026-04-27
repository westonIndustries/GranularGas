# Property-Based Tests

## Overview

The model uses property-based testing (PBT) to verify mathematical correctness. Unlike unit tests that check specific inputs and outputs, property tests define invariants that must hold for *any* valid input — then automatically generate hundreds of random inputs to try to find a counterexample.

The model uses the [Hypothesis](https://hypothesis.readthedocs.io/) library for Python. Each property test saves its results to `output/` as both HTML and Markdown reports.

---

## Why Property-Based Testing?

The model contains several mathematical relationships that must hold regardless of input values:

- The Weibull survival function must always be monotonically decreasing
- Equipment counts must be conserved through replacement (you can't create or destroy equipment)
- Housing stock growth must follow the compound growth formula exactly
- Simulated therms must never be negative

Unit tests with fixed inputs might pass while these invariants are violated for edge cases (e.g., very old equipment, zero HDD, 100% electrification rate). Property tests find these edge cases automatically.

---

## Running the Tests

```bash
# Run all property tests
python -m pytest src/ -v

# Run a specific property test module
python -m src.equipment_property_test
python -m src.fuel_switching_property_test
python -m src.scenario_property_tests
python -m src.weather_property_report
python -m src.water_heating_property_report
```

Each module can also be run standalone, which generates the HTML/MD report and prints a summary to console.

---

## Property 1: Weibull Survival Monotonicity

**Module**: `src/equipment_property_test.py`

**What it tests**: The Weibull survival function `S(t) = exp(-(t/eta)^beta)` must be monotonically non-increasing — survival probability can only stay the same or decrease as equipment ages.

**Formal property**:
```
For all t > 0, eta > 0, beta > 0:
    S(t) <= S(t-1)
    S(0) = 1.0
```

**Why it matters**: If S(t) > S(t-1) for any age, the replacement probability `P = 1 - S(t)/S(t-1)` would be negative, which is physically impossible. The Weibull function is mathematically guaranteed to be monotone, but floating-point arithmetic can introduce violations for extreme parameter values.

**Test parameters**: Hypothesis generates random values of `t` (0–100 years), `eta` (1–50 years), and `beta` (0.5–5.0).

**Output**: `output/equipment_replacement/property_weibull_results.html` and `.md`

---

## Property 2: Replacement Probability Bounds

**Module**: `src/equipment_property_test.py`

**What it tests**: The conditional replacement probability must always be in [0, 1].

**Formal property**:
```
For all t >= 0, eta > 0, beta > 0:
    0 <= replacement_probability(t, eta, beta) <= 1
```

**Why it matters**: `replacement_probability` is used as a probability in a Bernoulli draw. Values outside [0, 1] would cause the simulation to either never replace equipment (< 0) or always replace it (> 1), both of which are wrong.

**Output**: `output/equipment_replacement/property_weibull_results.html` and `.md`

---

## Property 3: Fuel Switching Conservation

**Module**: `src/fuel_switching_property_test.py`

**What it tests**: The total equipment count must be conserved through `apply_replacements`. Replacing a gas furnace with an electric heat pump changes the fuel type but does not change the count.

**Formal property**:
```
For any equipment inventory and any scenario:
    count(inventory_before) == count(inventory_after)
```

**Why it matters**: If equipment is accidentally created or destroyed during replacement, the simulation would produce incorrect premise counts and UPC calculations. This is a conservation law — equipment is replaced, not added or removed.

**Test parameters**: Hypothesis generates random equipment inventories (varying sizes, ages, fuel types) and random scenario electrification rates (0–100%).

**Output**: `output/fuel_switching/property_fuel_switching_results.html` and `.md`

---

## Property 4: Housing Stock Growth

**Module**: `src/scenario_property_tests.py`

**What it tests**: The projected housing stock must follow the compound growth formula exactly (within integer rounding tolerance).

**Formal property**:
```
For any baseline_units, growth_rate, and year_offset:
    |projected_units - round(baseline_units × (1 + growth_rate)^year_offset)| <= 1
```

**Why it matters**: If the housing stock projection deviates from the compound growth formula, the model's premise counts will drift from the scenario's intended growth trajectory, causing systematic errors in total therms and UPC.

**Test parameters**: Hypothesis generates random baseline unit counts (1,000–1,000,000), growth rates (−5% to +5%), and year offsets (0–50 years).

**Output**: `output/housing_stock_projections/property_growth_results.html` and `.md`

---

## Property 5: Simulation Non-Negativity

**Module**: `src/scenario_property_tests.py`

**What it tests**: All simulated `total_therms` values must be non-negative.

**Formal property**:
```
For any valid scenario and any year:
    total_therms(year) >= 0
    use_per_customer(year) >= 0
```

**Why it matters**: Negative therms would indicate a bug in the simulation formula (e.g., negative HDD, negative efficiency, or a sign error). Gas consumption cannot be negative.

**Test parameters**: Hypothesis generates random scenario configurations (varying growth rates, electrification rates, efficiency improvements) and runs the simulation.

**Output**: `output/scenario_validation/property_nonneg_results.html` and `.md`

---

## Property 6: HDD Non-Negativity

**Module**: `src/weather_property_report.py`

**What it tests**: Heating Degree Days must be non-negative for all days and all stations.

**Formal property**:
```
For any daily temperature:
    HDD_daily = max(0, 65 - temp) >= 0
    HDD_annual = sum(HDD_daily) >= 0
```

**Why it matters**: HDD is defined as `max(0, 65 - temp)`, so it is mathematically guaranteed to be non-negative. But if the temperature data contains invalid values (NaN, infinity, or extreme outliers), the HDD calculation could produce unexpected results.

**Test parameters**: Hypothesis generates random daily temperatures (−50°F to +120°F) including edge cases at exactly 65°F.

**Output**: `output/weather_validation/property_weather_results.html` and `.md`

---

## Property 7: Weather Adjustment Factor Validity

**Module**: `src/weather_property_report.py`

**What it tests**: The weather adjustment factor must be positive for all stations with valid normal HDD.

**Formal property**:
```
For any station with normal_hdd > 0:
    weather_adjustment_factor = actual_hdd / normal_hdd > 0
```

**Why it matters**: The weather adjustment factor is used as a multiplier on the heating factor. A zero or negative factor would eliminate or invert the heating demand calculation.

**Output**: `output/weather_validation/property_weather_results.html` and `.md`

---

## Property 8: Water Temperature Delta Validity

**Module**: `src/water_heating_property_report.py`

**What it tests**: The water heating temperature differential must be positive (incoming cold water must be cooler than the target hot water temperature).

**Formal property**:
```
For any valid water temperature record:
    delta_t = target_temp (120°F) - cold_water_temp > 0
```

**Why it matters**: If cold water temperature exceeds the target temperature, the delta-T would be negative, producing negative water heating demand. This would indicate either a data error or an unrealistic scenario.

**Output**: `output/water_heating_validation/property_water_heating_results.html` and `.md`

---

## Report Format

Each property test report contains:

1. **Summary table**: Pass/fail status for each property, number of examples tested, any counterexamples found
2. **Parameter distributions**: Histograms of the randomly generated input values
3. **Result distributions**: Histograms of the output values (e.g., survival probabilities, replacement counts)
4. **Counterexamples**: If a property fails, the minimal counterexample that caused the failure
5. **Timing**: How long the test took to run

### Example Summary Table

| Property | Status | Examples Tested | Counterexamples |
|----------|--------|----------------|----------------|
| Weibull monotonicity | ✅ PASS | 500 | 0 |
| Replacement probability bounds | ✅ PASS | 500 | 0 |
| Fuel switching conservation | ✅ PASS | 200 | 0 |
| Housing stock growth | ✅ PASS | 300 | 0 |
| Simulation non-negativity | ✅ PASS | 100 | 0 |
| HDD non-negativity | ✅ PASS | 1000 | 0 |
| Weather adjustment validity | ✅ PASS | 500 | 0 |
| Water temperature delta | ✅ PASS | 500 | 0 |

---

## Hypothesis Configuration

The `.hypothesis/` directory at the project root stores Hypothesis's database of previously found counterexamples. This means:

- If a property test fails and finds a counterexample, Hypothesis remembers it
- On subsequent runs, Hypothesis always re-tests the known counterexample first
- This prevents regressions — a bug that was once found will always be re-checked

The `.hypothesis/constants/` directory stores internal Hypothesis state. The `.hypothesis/examples/` directory stores saved counterexamples.

---

## Adding New Property Tests

To add a new property test:

1. Create a new file in `src/` (e.g., `src/aggregation_property_test.py`)
2. Import `hypothesis` and `hypothesis.strategies`
3. Define the property using `@given` decorator
4. Save results to `output/{test_name}/` as HTML and MD using `src/loaders/_helpers.py`

```python
from hypothesis import given, settings
import hypothesis.strategies as st

@given(
    total_therms=st.floats(min_value=0, max_value=1e9),
    premise_count=st.integers(min_value=1, max_value=1000000)
)
@settings(max_examples=500)
def test_upc_non_negative(total_therms, premise_count):
    upc = total_therms / premise_count
    assert upc >= 0, f"UPC must be non-negative, got {upc}"
```

---

## Related Documentation

- **[ALGORITHM.md](ALGORITHM.md)** — The simulation logic that property tests verify
- **[FORMULAS.md](FORMULAS.md)** — The mathematical formulas that properties are derived from
- **[EFFICIENCY_MODEL.md](EFFICIENCY_MODEL.md)** — Equipment replacement logic tested by Properties 1–3
