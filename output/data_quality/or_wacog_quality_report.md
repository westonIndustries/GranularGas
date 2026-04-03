# Data Quality Report: or_wacog
Generated: 2026-04-01T14:28:37.299472

**Shape**: 16 rows × 3 columns

Filter pass rate: 16 rows after filtering

## Column Summary

| Column | Type | Nulls | Null% | Unique | Details |
|--------|------|-------|-------|--------|---------|
| Effective Date | datetime64[us] | 0 | 0.0% | 8 | 2018-11-01 00:00:00 (2); 2019-11-01 00:00:00 (2); 2020-11-01 00:00:00 (2); 20... |
| Rate per Therm | float64 | 0 | 0.0% | 16 | min=0.23293, max=0.61505, mean=0.38 |
| Type | str | 0 | 0.0% | 2 | Annual (8); Winter (8) |

## Numeric Summary

```
       Rate per Therm
count       16.000000
mean         0.382976
std          0.113325
min          0.232930
25%          0.282615
50%          0.404740
75%          0.455845
max          0.615050
```

## Sample Rows (first 5)

| Effective Date      |   Rate per Therm | Type   |
|:--------------------|-----------------:|:-------|
| 2018-11-01 00:00:00 |          0.24649 | Annual |
| 2019-11-01 00:00:00 |          0.23293 | Annual |
| 2020-11-01 00:00:00 |          0.25644 | Annual |
| 2021-11-01 00:00:00 |          0.31601 | Annual |
| 2022-11-01 00:00:00 |          0.50715 | Annual |