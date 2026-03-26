# Task 1: Project Configuration and Setup

## Overview

Task 1 establishes the foundational configuration module for the NW Natural End-Use Forecasting Model. This task creates `src/config.py`, which centralizes all static configuration, file paths, and mappings used throughout the model. It's the first task in the implementation plan and must be completed before any data ingestion or simulation work can proceed.

## What Task 1 Does

Task 1 consists of two subtasks:

### 1.1 Create Configuration Module (`src/config.py`)

Creates a comprehensive configuration file that defines:

- **End-use category mappings** — Maps equipment type codes to end-use categories (space heating, water heating, cooking, clothes drying, fireplace, other)
- **Equipment efficiency defaults** — Default efficiency values by end-use category for when equipment-specific data is unavailable
- **Equipment useful life assumptions** — Default equipment lifespans by end-use category (used for replacement modeling)
- **Weibull survival model parameters** — Shape parameters (beta) for modeling equipment failure distributions
- **Weather station assignments** — Maps NW Natural district codes to weather station identifiers
- **File path constants** — Centralized paths to all data sources (NW Natural proprietary data, external datasets, tariffs, RBSA, ASHRAE, Census, etc.)
- **API constants** — Configuration for external APIs (Green Building Registry, Census, NOAA)
- **Simulation parameters** — Base year, default temperatures, and other simulation constants

### 1.2 Write Property Test for Config Completeness

Creates a property-based test (`tests/test_config_properties.py`) that validates:

**Property 1**: All equipment_type_codes in END_USE_MAP resolve to a valid end-use category string

This ensures that every equipment code defined in the mapping has a corresponding valid end-use category, preventing runtime errors when the model tries to classify equipment.

## How It Works

### Configuration Structure

The `config.py` module is organized into logical sections:

```python
# Section 1: END-USE CATEGORY MAPPINGS
END_USE_MAP = {
    "HEAT": "space_heating",
    "FURN": "space_heating",
    "WTR": "water_heating",
    "COOK": "cooking",
    "DRYR": "clothes_drying",
    "FRPL": "fireplace",
    "OTHR": "other",
    # ... more mappings
}

# Section 2: EQUIPMENT EFFICIENCY DEFAULTS
DEFAULT_EFFICIENCY = {
    "space_heating": 0.80,
    "water_heating": 0.60,
    "cooking": 0.75,
    "clothes_drying": 0.65,
    "fireplace": 0.10,
    "other": 0.70,
}

# Section 3: EQUIPMENT USEFUL LIFE
USEFUL_LIFE = {
    "space_heating": 20,
    "water_heating": 13,
    "cooking": 15,
    "clothes_drying": 13,
    "fireplace": 30,
    "other": 15,
}

# Section 4: WEIBULL SURVIVAL MODEL PARAMETERS
WEIBULL_BETA = {
    "space_heating": 3.0,
    "water_heating": 3.0,
    "cooking": 2.5,
    "clothes_drying": 2.5,
    "fireplace": 2.0,
    "other": 2.5,
}

# Section 5: DISTRICT TO WEATHER STATION MAPPING
DISTRICT_WEATHER_MAP = {
    "MULT": "KPDX",  # Multnomah -> Portland
    "WASH": "KPDX",  # Washington -> Portland
    # ... more mappings for all 16 NWN service territory counties
}

# Section 6: FILE PATH CONSTANTS
# NW Natural-supplied data
PREMISE_DATA = "Data/NWNatural Data/premise_data_blinded.csv"
EQUIPMENT_DATA = "Data/NWNatural Data/equipment_data_blinded.csv"
# ... more file paths

# Section 7: API CONSTANTS
GBR_API_BASE_URL = "https://api.greenbuildingregistry.com"
CENSUS_API_BASE = "https://api.census.gov/data"
# ... more API configuration
```

### Key Design Decisions

1. **Centralized Configuration** — All constants are defined in one place, making it easy to update assumptions without searching through code.

2. **End-Use Mapping** — Equipment type codes from NW Natural's equipment_codes.csv are mapped to standardized end-use categories. This allows the model to work with equipment-level data while aggregating to end-use level for analysis.

3. **Efficiency Defaults** — When equipment-specific efficiency data is missing, the model falls back to category-level defaults. These are conservative estimates based on pre-2010 equipment baselines.

4. **Weibull Parameters** — Different end-uses have different failure rate distributions. HVAC systems (beta=3.0) have a concentrated replacement window, while appliances (beta=2.5) fail more gradually.

5. **Weather Station Mapping** — Each NW Natural district is assigned to the nearest weather station. This enables weather-driven simulation of space heating and water heating demand.

6. **File Path Organization** — Paths are organized by data source provenance:
   - NW Natural-supplied proprietary data
   - Team-created tariff CSVs
   - RBSA building stock data
   - ASHRAE equipment data
   - Census demographic data
   - NOAA weather data
   - EIA RECS microdata

## How to Run the Tests

### Prerequisites

Ensure you have Python 3.9+ and pytest installed:

```bash
pip install pytest hypothesis pandas numpy
```

### Running Task 1 Tests

#### Run All Task 1 Tests

```bash
python -m pytest tests/test_config_properties.py -v
```

This runs all configuration property tests and displays verbose output showing each test name and result.

#### Run Specific Test

```bash
python -m pytest tests/test_config_properties.py::TestConfigCompleteness::test_end_use_map_all_codes_valid -v
```

This runs only the Property 1 test that validates all equipment codes map to valid end-use categories.

#### Run with Coverage

```bash
python -m pytest tests/test_config_properties.py --cov=src.config --cov-report=html
```

This generates a coverage report showing which parts of config.py are tested.

#### Run with Detailed Output

```bash
python -m pytest tests/test_config_properties.py -vv --tb=short
```

The `-vv` flag provides extra verbosity, and `--tb=short` shows concise traceback information if tests fail.

### Test Output Example

```
tests/test_config_properties.py::TestConfigCompleteness::test_end_use_map_all_codes_valid PASSED [ 50%]
tests/test_config_properties.py::TestConfigCompleteness::test_end_use_map_values_are_strings PASSED [100%]

============================== 2 passed in 0.15s ==============================
```

## What Gets Tested

### Property 1: End-Use Map Completeness

The test validates:

1. **All keys are valid equipment codes** — Every key in END_USE_MAP is a string
2. **All values are valid end-use categories** — Every value maps to one of the defined end-use categories (space_heating, water_heating, cooking, clothes_drying, fireplace, other)
3. **No null or empty mappings** — No mapping is missing or incomplete
4. **Consistency** — The same equipment code always maps to the same end-use

### Example Test Scenarios

```python
# Valid mapping
END_USE_MAP["FURN"] == "space_heating"  # ✓ Valid

# Invalid mapping (would fail test)
END_USE_MAP["FURN"] == "invalid_category"  # ✗ Fails

# Missing mapping (would fail test)
END_USE_MAP["UNKNOWN_CODE"]  # ✗ KeyError or None
```

## Integration with Rest of Model

Once Task 1 is complete, the configuration is imported and used throughout the model:

```python
# In data_ingestion.py
from src import config

# Map equipment codes to end-use
df['end_use'] = df['equipment_type_code'].map(config.END_USE_MAP)

# Apply default efficiency
df['efficiency'] = df['efficiency'].fillna(
    df['end_use'].map(config.DEFAULT_EFFICIENCY)
)

# Assign weather stations
df['weather_station'] = df['district_code_IRP'].map(config.DISTRICT_WEATHER_MAP)
```

## File Locations

- **Configuration module**: `src/config.py`
- **Property tests**: `tests/test_config_properties.py`
- **Test data**: Uses synthetic data generated in tests (no external files required)

## Validation Checklist

After completing Task 1, verify:

- [ ] `src/config.py` exists and contains all required sections
- [ ] All END_USE_MAP entries map to valid end-use categories
- [ ] All DEFAULT_EFFICIENCY keys match end-use categories
- [ ] All USEFUL_LIFE keys match end-use categories
- [ ] All WEIBULL_BETA keys match end-use categories
- [ ] DISTRICT_WEATHER_MAP covers all 16 NWN service territory counties
- [ ] All file path constants point to correct locations
- [ ] All API constants are defined
- [ ] `tests/test_config_properties.py` exists and all tests pass
- [ ] Property 1 test validates END_USE_MAP completeness

## Common Issues and Troubleshooting

### Issue: Import Error for config module

**Symptom**: `ModuleNotFoundError: No module named 'src.config'`

**Solution**: Ensure you're running pytest from the project root directory:
```bash
cd /path/to/GranularGas
python -m pytest tests/test_config_properties.py -v
```

### Issue: File path constants point to wrong locations

**Symptom**: Tests pass but data loading fails later

**Solution**: Verify file paths in config.py match actual data directory structure:
```bash
ls -la Data/NWNatural\ Data/
ls -la Data/
```

### Issue: Tests fail with "invalid end-use category"

**Symptom**: `AssertionError: Invalid end-use category in END_USE_MAP`

**Solution**: Check that all END_USE_MAP values are in the valid set:
```python
VALID_END_USES = {
    "space_heating", "water_heating", "cooking", 
    "clothes_drying", "fireplace", "other"
}
```

## Next Steps

After Task 1 is complete and all tests pass:

1. Proceed to **Task 2: Data Ingestion Module** — Implements CSV loading and data cleaning functions
2. Task 2 will import and use the configuration from Task 1
3. Configuration can be updated as needed, but Task 1 provides the stable foundation

## References

- **Requirements**: 1.1, 1.4, 3.2, 4.2
- **Design Document**: See `.kiro/specs/nw-natural-end-use-forecasting/design.md` for detailed architecture
- **Tasks Document**: See `.kiro/specs/nw-natural-end-use-forecasting/tasks.md` for full implementation plan
