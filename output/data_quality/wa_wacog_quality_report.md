# Data Quality Report: wa_wacog
Generated: 2026-04-01T14:28:37.311069

**Shape**: 16 rows × 3 columns

Filter pass rate: 16 rows after filtering

## Column Summary

| Column | Type | Nulls | Null% | Unique | Details |
|--------|------|-------|-------|--------|---------|
| Effective Date | datetime64[us] | 0 | 0.0% | 8 | 2018-11-01 00:00:00 (2); 2019-11-01 00:00:00 (2); 2020-11-01 00:00:00 (2); 20... |
| Rate per Therm | float64 | 0 | 0.0% | 16 | min=0.20291, max=0.56965, mean=0.38 |
| Type | str | 0 | 0.0% | 2 | Annual [cite: 251] (8); Winter [cite: 266] (8) |

## Numeric Summary

```
       Rate per Therm
count       16.000000
mean         0.375238
std          0.113618
min          0.202910
25%          0.264680
50%          0.410570
75%          0.456100
max          0.569650
```

## Sample Rows (first 5)

| Effective Date      |   Rate per Therm | Type               |
|:--------------------|-----------------:|:-------------------|
| 2018-11-01 00:00:00 |          0.22356 | Annual [cite: 251] |
| 2019-11-01 00:00:00 |          0.20291 | Annual [cite: 251] |
| 2020-11-01 00:00:00 |          0.26333 | Annual [cite: 251] |
| 2021-11-01 00:00:00 |          0.34873 | Annual [cite: 251] |
| 2022-11-01 00:00:00 |          0.46972 | Annual [cite: 251] |