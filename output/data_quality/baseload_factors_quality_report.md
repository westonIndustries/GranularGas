# Data Quality Report: baseload_factors
Generated: 2026-04-03T19:43:00.296781

**Shape**: 15 rows × 6 columns

## Column Summary

| Column | Type | Nulls | Null% | Unique | Details |
|--------|------|-------|-------|--------|---------|
| Category | str | 0 | 0.0% | 6 | Standby (4); Baseload (3); Adjustment (3); Equipment (2); Pilot (2) |
| SubCategory | str | 0 | 0.0% | 13 | Fireplace (2); Climate (2); UPC_Decay (1); Gas_Furnace (1); Gas_Water_Heater (1) |
| Parameter | str | 0 | 0.0% | 7 | Annual_Consumption (5); Base_Loss (4); Median_Life (2); Annual_Net_Rate (1); ... |
| Value | float64 | 0 | 0.0% | 13 | min=-0.0119, max=82.0, mean=30.42 |
| Unit | str | 0 | 0.0% | 5 | Therms (5); Therms/yr (4); Multiplier (3); Years (2); Ratio (1) |
| Source | str | 0 | 0.0% | 12 | DOE_AEO_2026 (2); RECS_2020_PNW (2); NEEA_Metering_Study (2); NWN_2025_IRP (1... |

## Numeric Summary

```
           Value
count  15.000000
mean   30.422540
std    27.260383
min    -0.011900
25%     6.600000
50%    20.000000
75%    50.500000
max    82.000000
```

## Sample Rows (first 5)

| Category   | SubCategory      | Parameter          |   Value | Unit   | Source        |
|:-----------|:-----------------|:-------------------|--------:|:-------|:--------------|
| Building   | UPC_Decay        | Annual_Net_Rate    | -0.0119 | Ratio  | NWN_2025_IRP  |
| Equipment  | Gas_Furnace      | Median_Life        | 18      | Years  | DOE_AEO_2026  |
| Equipment  | Gas_Water_Heater | Median_Life        | 12      | Years  | DOE_AEO_2026  |
| Baseload   | Cooking          | Annual_Consumption | 30      | Therms | RECS_2020_PNW |
| Baseload   | Drying           | Annual_Consumption | 20      | Therms | RECS_2020_PNW |