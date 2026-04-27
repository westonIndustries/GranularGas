# Billing Calibration Check

**Generated:** 2026-04-15T13:57:35.662734  
**Base Year:** 2025

## Calibration Metrics

| Metric | Value |
|--------|-------|
| Mean Absolute Error (MAE) | 57.88 therms/premise |
| Root Mean Square Error (RMSE) | 87.96 therms/premise |
| Mean Bias | -2.28 therms/premise |
| R² (Coefficient of Determination) | 0.9637 |
| Correlation Coefficient | 0.9818 |
| Sample Size | 1,000 premises |

## Interpretation

- **MAE:** Average absolute difference between simulated and billed therms per premise. Lower values indicate better calibration.
- **RMSE:** Root mean square error. Penalizes larger errors more heavily than MAE.
- **Mean Bias:** Average signed difference (positive = model overestimates, negative = underestimates). Ideally close to zero.
- **R²:** Proportion of variance in billed therms explained by simulated therms (0-1 scale). Higher values indicate better fit.
- **Correlation:** Pearson correlation coefficient between simulated and billed therms. Values closer to 1.0 indicate stronger positive correlation.

## Scatter Plot

The scatter plot shows simulated therms (y-axis) vs billed therms (x-axis) for each premise. The red dashed line represents perfect agreement (1:1). Points above the line indicate model overestimation; points below indicate underestimation.

## Sample Comparisons (First 30 Premises)

| Premise ID | Simulated Therms | Billed Therms | Difference | % Error |
|------------|------------------|---------------|-----------|---------|
| P000000 | 946.47 | 1002.89 | -56.42 | -5.6% |
| P000001 | 1415.52 | 1392.03 | 23.49 | 1.7% |
| P000002 | 929.77 | 1002.04 | -72.26 | -7.2% |
| P000003 | 706.23 | 835.31 | -129.07 | -15.5% |
| P000004 | 443.39 | 430.93 | 12.46 | 2.9% |
| P000005 | 1888.93 | 1835.86 | 53.07 | 2.9% |
| P000006 | 447.43 | 532.22 | -84.79 | -15.9% |
| P000007 | 215.99 | 235.88 | -19.89 | -8.4% |
| P000008 | 892.08 | 841.82 | 50.26 | 6.0% |
| P000009 | 267.16 | 284.55 | -17.39 | -6.1% |
| P000010 | 360.70 | 340.64 | 20.06 | 5.9% |
| P000011 | 183.43 | 173.18 | 10.25 | 5.9% |
| P000012 | 120.68 | 124.18 | -3.50 | -2.8% |
| P000013 | 165.29 | 127.34 | 37.95 | 29.8% |
| P000014 | 792.60 | 628.54 | 164.06 | 26.1% |
| P000015 | 1337.68 | 1247.42 | 90.26 | 7.2% |
| P000016 | 1550.29 | 1361.87 | 188.42 | 13.8% |
| P000017 | 1071.47 | 1111.88 | -40.40 | -3.6% |
| P000018 | 220.03 | 196.05 | 23.97 | 12.2% |
| P000019 | 209.35 | 173.87 | 35.48 | 20.4% |
| P000020 | 668.76 | 786.38 | -117.62 | -15.0% |
| P000021 | 164.49 | 160.03 | 4.46 | 2.8% |
| P000022 | 1210.77 | 1220.58 | -9.81 | -0.8% |
| P000023 | 1013.74 | 840.42 | 173.32 | 20.6% |
| P000024 | 1467.71 | 1371.83 | 95.88 | 7.0% |
| P000025 | 267.84 | 271.40 | -3.57 | -1.3% |
| P000026 | 436.74 | 376.42 | 60.32 | 16.0% |
| P000027 | 1026.30 | 1072.57 | -46.27 | -4.3% |
| P000028 | 420.31 | 390.02 | 30.29 | 7.8% |
| P000029 | 147.74 | 142.57 | 5.17 | 3.6% |

## Requirements

- **Requirement 7.1 (Data Input and Calibration):** The model accepts billing data and uses it to calibrate baseline consumption patterns.
- **Requirement 10.2 (Model vs IRP Comparison):** The model compares simulated results to external benchmarks (in this case, billing data).

## Notes

- This calibration check validates how well the bottom-up simulation matches actual billing data.
- Discrepancies may be due to: data quality issues, missing equipment records, weather variations, or model assumptions.
- The synthetic billing data is used when real billing data is unavailable for demonstration purposes.
