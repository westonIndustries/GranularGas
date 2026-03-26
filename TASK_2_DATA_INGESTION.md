# Task 2: Data Ingestion Module

## Overview

Task 2 implements the data ingestion layer for the NW Natural End-Use Forecasting Model. This task creates `src/data_ingestion.py`, which handles loading, cleaning, and joining data from multiple sources including NW Natural's proprietary premise/equipment data, external datasets (RBSA, ASHRAE, Census, NOAA, EIA RECS), and tariff information. It's the critical foundation for all downstream simulation work.

## What Task 2 Does

Task 2 consists of four subtasks:

### 2.1 Create Data Ingestion Module (`src/data_ingestion.py`)

Implements 40+ functions organized into logical groups:

**NW Natural Proprietary Data Loading**
- `load_premise_data()` — Load and filter to active residential premises (custtype='R', status_code='AC')
- `load_equipment_data()` — Load equipment inventory CSV
- `load_segment_data()` — Load and filter segment data to residential customers
- `load_equipment_codes()` — Load equipment code lookup table
- `load_billing_data()` — Load billing data, parse dollar amounts to float, parse dates

**Weather Data Loading**
- `load_weather_data()` — Load daily weather CSV, parse dates
- `load_water_temperature()` — Load Bull Run water temperature CSV
- `load_snow_data()` — Load Portland daily snow data (1985-2025)

**Tariff and Rate Data**
- `load_or_rates()` — Load Oregon tariff rates (Schedule, Type, Rate/Value)
- `load_wa_rates()` — Load Washington tariff rates
- `load_wacog_history()` — Load WACOG (Weighted Average Cost of Gas) history
- `load_rate_case_history()` — Load rate case history for both states
- `build_historical_rate_table()` — Reconstruct historical $/therm by working backward from current rates
- `convert_billing_to_therms()` — Convert billing dollars to estimated therms using historical rates

**RBSA Building Stock Data**
- `load_rbsa_site_detail()` — Load 2022 RBSA site characteristics, filter to NWN service territory
- `load_rbsa_hvac()` — Load RBSA HVAC system data
- `load_rbsa_water_heater()` — Load RBSA water heater data
- `build_rbsa_distributions()` — Compute weighted distributions of building characteristics

**ASHRAE Equipment Data**
- `load_ashrae_service_life()` — Load ASHRAE equipment service life data for OR and WA
- `load_ashrae_maintenance_cost()` — Load ASHRAE maintenance cost data
- `build_useful_life_table()` — Build state-specific useful life lookup from ASHRAE data

**Load Decay and Baseload Data**
- `load_load_decay_forecast()` — Load NW Natural 2025 IRP 10-Year Load Decay Forecast
- `load_historical_upc()` — Load historical UPC data back to 2005
- `load_baseload_factors()` — Load baseload consumption factors (cooking, drying, fireplace, pilot loads)
- `calculate_site_baseload()` — Calculate total non-weather-sensitive baseload per site
- `load_nw_energy_proxies()` — Load compact NW energy proxy parameter set

**Green Building Registry API**
- `fetch_gbr_properties()` — Query GBR API for properties by zip code
- `build_gbr_building_profiles()` — Extract building shell characteristics from GBR data

**RBSA Sub-Metered Data**
- `load_rbsam_metering()` — Load RBSA sub-metered end-use data (15-minute intervals, ~600MB)
- `load_rbsa_2017_site_detail()` — Load 2017 RBSA-II for temporal comparison

**Census Data**
- `load_service_territory_fips()` — Load NW Natural service territory FIPS codes
- `fetch_census_b25034()` — Fetch Census ACS B25034 (Year Structure Built) via API
- `build_vintage_distribution()` — Convert B25034 counts to percentage distributions
- `load_b25034_county_files()` — Load downloaded ACS 5-year B25034 county CSVs (offline fallback)
- `load_b25040_county_files()` — Load ACS 5-year B25040 (House Heating Fuel) county data
- `load_b25024_county_files()` — Load ACS 5-year B25024 (Units in Structure) county data

**Population and Housing Forecasts**
- `load_psu_population_forecasts()` — Load PSU Population Research Center county forecasts (handles 3 CSV formats)
- `load_ofm_housing()` — Load WA OFM postcensal housing unit estimates

**NOAA Weather Normals**
- `load_noaa_daily_normals()` — Load NOAA 30-year daily climate normals
- `load_noaa_monthly_normals()` — Load NOAA monthly climate normals
- `compute_weather_adjustment()` — Compute weather adjustment factor (actual/normal HDD ratio)

**EIA RECS Microdata**
- `load_recs_microdata()` — Load EIA RECS public-use microdata for given survey year (2005-2020)
- `build_recs_enduse_benchmarks()` — Compute weighted-average gas consumption by end use

### 2.2 Implement Join Function (`build_premise_equipment_table`)

Creates a unified dataset by joining premise, equipment, segment, and equipment_codes tables:

- Performs left joins on `blinded_id` and `equipment_type_code` to preserve all records
- Derives `end_use` column using `END_USE_MAP` from config
- Derives `efficiency` column using equipment data or `DEFAULT_EFFICIENCY` fallback
- Derives `weather_station` column using `DISTRICT_WEATHER_MAP`
- Logs warnings for missing data and unmapped codes
- Returns unified DataFrame with all columns plus derived columns

### 2.3 Write Property Tests for Data Ingestion

Creates `tests/test_data_ingestion_properties.py` with property-based tests:

**Property 2**: Filtering preserves only active residential premises — output contains only custtype='R' and status_code='AC'

Tests verify:
- Only residential customers (custtype='R') are included
- Only active premises (status_code='AC') are included
- No duplicates are introduced
- Required columns are preserved
- Data types are maintained
- Handles missing columns gracefully
- Handles null values correctly
- Case sensitivity is handled properly

### 2.4 Write Property Test for Join Integrity

Creates additional property tests for the join function:

**Property 3**: Every row in premise_equipment_table has a non-null end_use category and a valid efficiency > 0

Tests verify:
- All rows have non-null end_use values
- All rows have efficiency > 0
- All rows have efficiency ≤ 1.0
- Defaults are applied correctly when data is missing
- Join preserves all premise records (left join semantics)

## How It Works

### Data Loading Pipeline

The data ingestion module follows a consistent pattern for each data source:

```python
def load_<data_source>(path):
    """
    Load and validate <data_source> data.
    
    Args:
        path: File path to CSV or other data file
        
    Returns:
        Cleaned and validated DataFrame
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If required columns are missing
    """
    try:
        # 1. Load CSV
        df = pd.read_csv(path)
        
        # 2. Validate required columns
        required_cols = ['col1', 'col2', ...]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        
        # 3. Parse data types (dates, numbers, etc.)
        df['date_col'] = pd.to_datetime(df['date_col'])
        df['numeric_col'] = pd.to_numeric(df['numeric_col'])
        
        # 4. Filter/clean data
        df = df[df['status'] == 'ACTIVE']
        
        # 5. Log results
        logger.info(f"Loaded {len(df)} records from {path}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error loading {path}: {e}")
        raise
```

### Key Data Transformations

**Billing to Therms Conversion**

Billing data contains dollar amounts, not therms. The conversion process:

1. Load billing data with `utility_usage` (dollars) and `GL_revenue_date`
2. Load tariff rates (OR Schedule 2 = $1.41220/therm, WA = $1.24164/therm)
3. Load rate case history and WACOG history
4. Reconstruct historical rates by working backward from current rates using rate case granted percentages
5. Join billing with historical rate table by rate_schedule, state, and date
6. Calculate: `estimated_therms = utility_usage / rate_per_therm`

**RBSA Filtering to NWN Service Territory**

RBSA data covers the entire Pacific Northwest. Filter to NWN by:

```python
# Filter to NWN service territory
df = df[
    (df['NWN_SF_StrataVar'] == 'NWN') | 
    (df['Gas_Utility'] == 'NW NATURAL GAS')
]

# Use Site_Case_Weight for population-level estimates
weighted_avg = (df['value'] * df['Site_Case_Weight']).sum() / df['Site_Case_Weight'].sum()
```

**Census API Queries**

Fetch Census ACS data via API:

```python
# Build query for multiple counties
fips_codes = ['41051', '41067', '53011', ...]  # County FIPS codes
ucgid_list = ','.join([f'0500000US{fips}' for fips in fips_codes])

# Query ACS 5-year B25034 (Year Structure Built)
url = f"{CENSUS_API_BASE}/2023/acs/acs5"
params = {
    'get': 'NAME,group(B25034)',
    'ucgid': ucgid_list,
    'key': CENSUS_API_KEY
}
response = requests.get(url, params=params)
```

**PSU Population Forecast Parsing**

Handle three different CSV formats:

```python
# Format 1: 2025 files (YEAR, POPULATION, TYPE)
df = pd.read_csv(path)  # Columns: YEAR, POPULATION, TYPE

# Format 2: 2024 files (YEAR, POPULATION)
df = pd.read_csv(path)  # Columns: YEAR, POPULATION

# Format 3: 2023 Coos (wide format: areas as rows, years as columns)
df = pd.read_csv(path, index_col=0)  # Extract county total row
df = df.melt(var_name='year', value_name='population')
```

### Join Operation

The `build_premise_equipment_table` function orchestrates the join:

```python
# Start with premises
df = premises.copy()

# Join equipment (left join preserves all premises)
df = df.merge(equipment, on='blinded_id', how='left')

# Join segments (left join)
df = df.merge(segments, on='blinded_id', how='left')

# Join equipment codes (left join)
df = df.merge(codes, on='equipment_type_code', how='left')

# Derive end_use from equipment_type_code
df['end_use'] = df['equipment_type_code'].map(config.END_USE_MAP)

# Fill missing efficiency with defaults
for end_use, default_eff in config.DEFAULT_EFFICIENCY.items():
    mask = (df['end_use'] == end_use) & (df['efficiency'].isna())
    df.loc[mask, 'efficiency'] = default_eff

# Assign weather stations
df['weather_station'] = df['district_code_IRP'].map(config.DISTRICT_WEATHER_MAP)

return df
```

## How to Run the Tests

### Prerequisites

Ensure you have required packages installed:

```bash
pip install pytest hypothesis pandas numpy requests
```

### Running All Task 2 Tests

```bash
python -m pytest tests/test_data_ingestion_properties.py -v
```

This runs all data ingestion property tests with verbose output.

### Running Specific Test Classes

**Run filtering tests only:**
```bash
python -m pytest tests/test_data_ingestion_properties.py::TestDataIngestionFiltering -v
```

**Run join integrity tests only:**
```bash
python -m pytest tests/test_data_ingestion_properties.py::TestDataIngestionJoinIntegrity -v
```

### Running Specific Tests

**Run Property 2 test (filtering):**
```bash
python -m pytest tests/test_data_ingestion_properties.py::TestDataIngestionFiltering::test_load_premise_data_filters_to_residential_active -v
```

**Run Property 3 test (join integrity):**
```bash
python -m pytest tests/test_data_ingestion_properties.py::TestDataIngestionJoinIntegrity::test_premise_equipment_table_combined_integrity -v
```

### Running with Coverage

```bash
python -m pytest tests/test_data_ingestion_properties.py --cov=src.data_ingestion --cov-report=html
```

Generates an HTML coverage report in `htmlcov/index.html`.

### Running with Detailed Output

```bash
python -m pytest tests/test_data_ingestion_properties.py -vv --tb=short
```

The `-vv` flag provides extra verbosity, and `--tb=short` shows concise traceback information.

### Running with Markers

```bash
# Run only fast tests
python -m pytest tests/test_data_ingestion_properties.py -m "not slow" -v

# Run only slow tests
python -m pytest tests/test_data_ingestion_properties.py -m "slow" -v
```

### Test Output Example

```
tests/test_data_ingestion_properties.py::TestDataIngestionFiltering::test_load_premise_data_filters_to_residential_active PASSED [ 10%]
tests/test_data_ingestion_properties.py::TestDataIngestionFiltering::test_premise_filtering_preserves_required_columns PASSED [ 20%]
tests/test_data_ingestion_properties.py::TestDataIngestionFiltering::test_premise_filtering_no_duplicates PASSED [ 30%]
tests/test_data_ingestion_properties.py::TestDataIngestionJoinIntegrity::test_join_preserves_premise_count_left_join PASSED [ 40%]
tests/test_data_ingestion_properties.py::TestDataIngestionJoinIntegrity::test_premise_equipment_table_end_use_non_null PASSED [ 50%]
tests/test_data_ingestion_properties.py::TestDataIngestionJoinIntegrity::test_premise_equipment_table_efficiency_valid PASSED [ 60%]
tests/test_data_ingestion_properties.py::TestDataIngestionJoinIntegrity::test_premise_equipment_table_combined_integrity PASSED [ 70%]

============================== 7 passed in 1.23s ==============================
```

## What Gets Tested

### Property 2: Filtering Preserves Residential Active Premises

Tests validate:

1. **Only residential customers** — custtype='R' only
2. **Only active premises** — status_code='AC' only
3. **No duplicates** — Each premise appears once
4. **Required columns preserved** — All expected columns present
5. **Data types maintained** — Columns have correct types
6. **Handles missing columns** — Graceful error if required columns missing
7. **Handles null values** — Null values handled correctly
8. **Case sensitivity** — Filters work regardless of case
9. **Empty results** — Handles case where no records match filter
10. **All match** — Handles case where all records match filter

### Property 3: Join Integrity

Tests validate:

1. **Non-null end_use** — Every row has a valid end_use category
2. **Valid efficiency** — Every row has efficiency > 0 and ≤ 1.0
3. **Defaults applied** — Missing efficiency values get defaults
4. **Left join semantics** — All premises preserved even without equipment
5. **No data loss** — All equipment records preserved even if unmapped
6. **Combined integrity** — Both conditions satisfied simultaneously

### Example Test Scenarios

```python
# Property 2: Filtering
premises = pd.DataFrame({
    'blinded_id': ['P001', 'P002', 'P003'],
    'custtype': ['R', 'C', 'R'],  # Mix of residential and commercial
    'status_code': ['AC', 'AC', 'IN'],  # Mix of active and inactive
})

filtered = load_premise_data(premises)
# Result: Only P001 (custtype='R' AND status_code='AC')

# Property 3: Join Integrity
result = build_premise_equipment_table(premises, equipment, segments, codes)
# All rows have non-null end_use AND efficiency > 0
assert result['end_use'].notna().all()
assert (result['efficiency'] > 0).all()
```

## Integration with Rest of Model

Once Task 2 is complete, data ingestion functions are used throughout:

```python
# In main.py or scenario runner
from src import data_ingestion, config

# Load all data
premises = data_ingestion.load_premise_data(config.PREMISE_DATA)
equipment = data_ingestion.load_equipment_data(config.EQUIPMENT_DATA)
segments = data_ingestion.load_segment_data(config.SEGMENT_DATA)
codes = data_ingestion.load_equipment_codes(config.EQUIPMENT_CODES)

# Build unified table
premise_equipment = data_ingestion.build_premise_equipment_table(
    premises, equipment, segments, codes
)

# Load weather data
weather = data_ingestion.load_weather_data(config.WEATHER_CALDAY)
water_temp = data_ingestion.load_water_temperature(config.WATER_TEMP)

# Load RBSA for building characteristics
rbsa_sites = data_ingestion.load_rbsa_site_detail(config.RBSA_SITE_DETAIL)
rbsa_hvac = data_ingestion.load_rbsa_hvac(config.RBSA_HVAC)

# Load Census data for vintage distribution
b25034 = data_ingestion.load_b25034_county_files(config.B25034_COUNTY_DIR)
vintage_dist = data_ingestion.build_vintage_distribution(b25034)

# Load RECS for validation benchmarks
recs = data_ingestion.load_recs_microdata(config.RECS_2020_CSV, year=2020)
benchmarks = data_ingestion.build_recs_enduse_benchmarks(recs)
```

## File Locations

- **Data ingestion module**: `src/data_ingestion.py`
- **Property tests**: `tests/test_data_ingestion_properties.py`
- **Data files**: `Data/` (organized by source provenance)
- **Configuration**: `src/config.py` (imported by data_ingestion)

## Validation Checklist

After completing Task 2, verify:

- [ ] `src/data_ingestion.py` exists with all 40+ functions
- [ ] All NW Natural data loading functions implemented
- [ ] All external data loading functions implemented (RBSA, ASHRAE, Census, NOAA, RECS)
- [ ] `build_premise_equipment_table` joins all tables correctly
- [ ] All functions have docstrings with Args, Returns, Raises
- [ ] All functions log significant events and warnings
- [ ] `tests/test_data_ingestion_properties.py` exists with all tests
- [ ] Property 2 tests validate filtering (10+ test cases)
- [ ] Property 3 tests validate join integrity (3+ test cases)
- [ ] All tests pass: `pytest tests/test_data_ingestion_properties.py -v`
- [ ] Code coverage > 80% for critical paths

## Common Issues and Troubleshooting

### Issue: FileNotFoundError when loading data

**Symptom**: `FileNotFoundError: [Errno 2] No such file or directory: 'Data/NWNatural Data/premise_data_blinded.csv'`

**Solution**: Verify data files exist and paths in config.py are correct:
```bash
ls -la "Data/NWNatural Data/"
```

### Issue: Missing required columns

**Symptom**: `ValueError: Missing required columns: ['blinded_id']`

**Solution**: Check that CSV files have expected columns:
```bash
head -1 "Data/NWNatural Data/premise_data_blinded.csv"
```

### Issue: Date parsing errors

**Symptom**: `ParserError: Unable to parse date column`

**Solution**: Check date format in CSV and adjust parsing:
```python
# Try different date formats
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
# or
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
```

### Issue: Join produces unexpected number of rows

**Symptom**: Result has more rows than expected

**Solution**: Remember that left joins can produce multiple rows per premise if equipment has multiple records:
```python
# P001 has 2 equipment items -> 2 rows in result
# P002 has 1 equipment item -> 1 row in result
# P003 has 0 equipment items -> 1 row in result (NaN for equipment columns)
```

### Issue: Tests fail with "unmapped equipment code"

**Symptom**: `AssertionError: {unmapped_codes} have unmapped equipment_type_code values`

**Solution**: Add missing equipment codes to END_USE_MAP in config.py:
```python
END_USE_MAP = {
    # ... existing mappings
    "NEW_CODE": "appropriate_end_use",
}
```

## Next Steps

After Task 2 is complete and all tests pass:

1. Proceed to **Task 3: Checkpoint — Verify Data Ingestion** — Verify all tests pass and data loads correctly
2. Then proceed to **Task 4: Housing Stock Module** — Build housing stock representation using ingested data
3. Task 4 will import and use data_ingestion functions to load and process data

## References

- **Requirements**: 2.2, 2.4, 3.1, 3.2, 7.1, 7.2, 7.3, 7.4, 8.3
- **Design Document**: See `.kiro/specs/nw-natural-end-use-forecasting/design.md` for detailed data source documentation
- **Tasks Document**: See `.kiro/specs/nw-natural-end-use-forecasting/tasks.md` for full implementation plan
- **Data Organization**: See design.md "Data Folder Organization" section for complete data source structure
