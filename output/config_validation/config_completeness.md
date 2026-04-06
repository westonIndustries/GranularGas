# Config Completeness — Property Test Results
Generated: 2026-04-02T07:44:47.777221
**Result: 6/7 checks passed, 1 failed ❌**

| Status | Check | Detail |
|--------|-------|--------|
| ✅ | END_USE_MAP values are non-empty strings | 17 codes mapped. All valid. |
| ✅ | DEFAULT_EFFICIENCY keys match END_USE_MAP values | End-uses: ['clothes_drying', 'cooking', 'fireplace', 'other', 'space_heating', 'water_heating']. All keys matched. |
| ✅ | DEFAULT_EFFICIENCY values in (0, 1] | 6 entries. All valid. |
| ✅ | USEFUL_LIFE keys match END_USE_MAP values | Life entries: ['clothes_drying', 'cooking', 'fireplace', 'other', 'space_heating', 'water_heating']. All matched. |
| ✅ | USEFUL_LIFE values are positive integers | 6 entries. All valid. |
| ✅ | DISTRICT_WEATHER_MAP values are valid ICAO codes in ICAO_TO_GHCND | 17 districts, 11 ICAO stations. All valid. |
| ❌ | File paths reference existing files | 11/20 files present. Missing: PREMISE_DATA, EQUIPMENT_DATA, EQUIPMENT_CODES, SEGMENT_DATA, BILLING_DATA, WEATHER_CALDAY, WEATHER_GASDAY, WATER_TEMP, PORTLAND_SNOW |

## Missing Files (warnings)

- ⚠️ `PREMISE_DATA` → `Data/NWNatural Data\premise_data_blinded.csv`
- ⚠️ `EQUIPMENT_DATA` → `Data/NWNatural Data\equipment_data_blinded.csv`
- ⚠️ `EQUIPMENT_CODES` → `Data/NWNatural Data\equipment_codes.csv`
- ⚠️ `SEGMENT_DATA` → `Data/NWNatural Data\segment_data_blinded.csv`
- ⚠️ `BILLING_DATA` → `Data/NWNatural Data\billing_data_blinded.csv`
- ⚠️ `WEATHER_CALDAY` → `Data/NWNatural Data\DailyCalDay1985_Mar2025.csv`
- ⚠️ `WEATHER_GASDAY` → `Data/NWNatural Data\DailyGasDay2008_Mar2025.csv`
- ⚠️ `WATER_TEMP` → `Data/NWNatural Data\BullRunWaterTemperature.csv`
- ⚠️ `PORTLAND_SNOW` → `Data/NWNatural Data\Portland_snow.csv`