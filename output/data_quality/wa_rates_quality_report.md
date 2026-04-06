# Data Quality Report: wa_rates
Generated: 2026-04-03T19:43:00.228078

**Shape**: 14 rows × 4 columns

## Column Summary

| Column | Type | Nulls | Null% | Unique | Details |
|--------|------|-------|-------|--------|---------|
| Schedule | int64 | 0 | 0.0% | 4 | min=2, max=42, mean=16.57 |
| Type | str | 0 | 0.0% | 4 | Basic Firm (6); Residential (3); Large Volume Firm (3); Non-Residential Sales... |
| Description | str | 0 | 0.0% | 11 | Customer Charge (3); CCA Credit (Com) (2); CCA Credit (1); Usage Charge (per ... |
| Value | str | 0 | 0.0% | 14 | 8.00 [cite: 51] (1); -26.32 [cite: 77] (1); 1.24164 [cite: 45] (1); 5.50 [cit... |

## Numeric Summary

```
        Schedule
count  14.000000
mean   16.571429
std    19.365768
min     2.000000
25%     3.000000
50%     3.000000
75%    41.000000
max    42.000000
```

## Sample Rows (first 5)

|   Schedule | Type        | Description              | Value              |
|-----------:|:------------|:-------------------------|:-------------------|
|          2 | Residential | Customer Charge          | 8.00 [cite: 51]    |
|          2 | Residential | CCA Credit               | -26.32 [cite: 77]  |
|          2 | Residential | Usage Charge (per therm) | 1.24164 [cite: 45] |
|          3 | Basic Firm  | Customer Charge (Res)    | 5.50 [cite: 29]    |
|          3 | Basic Firm  | Customer Charge (Com)    | 7.00 [cite: 32]    |