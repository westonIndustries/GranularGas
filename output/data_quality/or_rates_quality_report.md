# Data Quality Report: or_rates
Generated: 2026-04-03T19:43:00.175057

**Shape**: 14 rows × 5 columns

## Column Summary

| Column | Type | Nulls | Null% | Unique | Details |
|--------|------|-------|-------|--------|---------|
| Schedule | str | 0 | 0.0% | 6 | 2 (3); 3 (3); 32 (3); 33 (3); 31 (1) |
| Type | str | 0 | 0.0% | 6 | Residential (3); Basic Firm Sales (3); Large Vol Firm Sales (3); High-Volume ... |
| Description | str | 0 | 0.0% | 11 | Customer Charge (4); Customer Charge (Single Family) (1); Customer Charge (Mu... |
| Rate/Value | float64 | 0 | 0.0% | 12 | min=0.0655, max=38000.0, mean=2806.71 |
| Unit | str | 0 | 0.0% | 3 | Month (7); per therm (6); Charge (1) |

## Numeric Summary

```
         Rate/Value
count     14.000000
mean    2806.710901
std    10131.206004
min        0.065500
25%        1.282825
50%        9.000000
75%      190.000000
max    38000.000000
```

## Sample Rows (first 5)

|   Schedule | Type             | Description                     |   Rate/Value | Unit      |
|-----------:|:-----------------|:--------------------------------|-------------:|:----------|
|          2 | Residential      | Customer Charge (Single Family) |      10      | Month     |
|          2 | Residential      | Customer Charge (Multi Family)  |       8      | Month     |
|          2 | Residential      | Usage Charge                    |       1.4122 | per therm |
|          3 | Basic Firm Sales | Customer Charge                 |      10      | Month     |
|          3 | Basic Firm Sales | Usage Charge (Commercial)       |       1.2397 | per therm |