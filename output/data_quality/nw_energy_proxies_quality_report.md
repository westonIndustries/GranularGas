# Data Quality Report: nw_energy_proxies
Generated: 2026-04-01T14:28:37.366398

**Shape**: 12 rows × 6 columns

Filter pass rate: 12 rows after filtering

## Column Summary

| Column | Type | Nulls | Null% | Unique | Details |
|--------|------|-------|-------|--------|---------|
| Category | str | 0 | 0.0% | 6 | Envelope (4); Infiltration (2); Efficiency (2); Retrofit (2); Building (1) |
| SubCategory | str | 0 | 0.0% | 12 | UPC_Decay (1); Wall_Pre_1950 (1); Wall_1951_1980 (1); Wall_1981_2010 (1); Wal... |
| Parameter | str | 0 | 0.0% | 6 | U_Value (5); ACH50 (3); Annual_Net_Rate (1); AFUE (1); HSPF2 (1) |
| Value | float64 | 0 | 0.0% | 12 | min=-0.0119, max=14.0, mean=2.78 |
| Unit | str | 0 | 0.0% | 4 | Btu/hr.sqft.F (5); Ratio (3); AirChanges/hr (3); Multiplier (1) |
| Source | str | 0 | 0.0% | 8 | RBSA_2022 (5); NWN_2025_IRP (1); WA_Energy_Code_2024 (1); Current_Standard (1... |

## Numeric Summary

```
           Value
count  12.000000
mean    2.781092
std     4.440810
min    -0.011900
25%     0.059000
50%     0.600000
75%     3.500000
max    14.000000
```

## Sample Rows (first 5)

| Category   | SubCategory       | Parameter       |   Value | Unit          | Source       |
|:-----------|:------------------|:----------------|--------:|:--------------|:-------------|
| Building   | UPC_Decay         | Annual_Net_Rate | -0.0119 | Ratio         | NWN_2025_IRP |
| Envelope   | Wall_Pre_1950     | U_Value         |  0.25   | Btu/hr.sqft.F | RBSA_2022    |
| Envelope   | Wall_1951_1980    | U_Value         |  0.081  | Btu/hr.sqft.F | RBSA_2022    |
| Envelope   | Wall_1981_2010    | U_Value         |  0.056  | Btu/hr.sqft.F | RBSA_2022    |
| Envelope   | Wall_2011_Current | U_Value         |  0.038  | Btu/hr.sqft.F | RBSA_2022    |