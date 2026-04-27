# HDD Normalization and Weather Year Handling

## The Problem

The heating factor was calibrated against 2025 billing data and 2025 weather data. But 2025 weather data only covers January through March (the data file ends at March 2025). This means:

- Calibration HDD (2025, partial): ~1,846 degree-days (3 months)
- Full year HDD (2024, complete): ~3,847 degree-days (12 months)

When the monthly simulation falls back to 2024 weather (because 2025 doesn't have all 12 months), it uses roughly 2× the HDD that the heating factor was calibrated against. Without normalization, this produces 2× the therms — a 60% overestimate vs the IRP.

## The Fix

The model now automatically normalizes the heating factor when the simulation uses a different weather year than the calibration year:

```
effective_heating_factor = config_heating_factor × (calibration_HDD / actual_HDD)
```

For the monthly baseline:
```
effective = 0.187502 × (1,846 / 3,847) = 0.089976
```

This ensures that regardless of which weather year the simulation uses, the total annual therms remain consistent with the calibrated billing data.

## How It Works

1. The model checks if the target year (2025) has weather data for all 12 months
2. If not, it finds the most recent year with complete 12-month coverage (2024)
3. It computes the weighted average HDD for both years across all weather stations
4. The heating factor is scaled by the ratio of calibration HDD to actual HDD
5. The simulation runs with the adjusted heating factor

## Verification

Both annual and monthly baselines now produce identical annual UPC:

| Scenario | Weather Year | Raw HDD | Effective HF | 2025 UPC | 2035 UPC |
|----------|-------------|---------|-------------|----------|----------|
| Annual | 2025 (partial) | 1,846 | 0.187502 | 499.2 | 424.8 |
| Monthly | 2024 (full) | 3,847 | 0.089976 | 499.2 | 424.8 |

The annual totals match because the HDD normalization compensates for the different weather year.

## Weather Year Selection Logic

The model uses this priority for selecting weather data:

1. **Target year with 12 months** — use as-is, no normalization needed
2. **Target year with < 12 months** — fall back to most recent year with 12 months, apply HDD normalization
3. **No year with 12 months** — use whatever is available, log a warning

For the annual simulation path, the threshold is lower (>100 records) because it sums all available days regardless of month coverage. For the monthly path, all 12 months must be present.

## HDD History

The `hdd_history.csv` output shows the weighted average HDD for each year from 1985 to 2025. The `chart_hdd_history.png` visualizes this with:

- Bar chart of annual HDD
- 30-year average line
- Calibration year marker (2025, partial)
- Weather proxy year marker (2024, full) if different

Typical PNW HDD range: 3,200–4,500 degree-days per year. The 2025 partial value of 1,846 represents only January–March, which is the coldest quarter and accounts for roughly 48% of annual HDD.

## Output Files

Each scenario folder contains:

- `hdd_info.csv` — calibration year, actual weather year, HDD values, ratio, effective heating factor
- `hdd_history.csv` — annual weighted HDD from 1985 to present
- `chart_hdd_history.png` — visual history with annotations

## Implications for Scenario Design

When creating new scenarios:

- The `heating_factor` in the JSON is always relative to the calibration year's HDD
- The model automatically adjusts if the simulation uses different weather
- You don't need to manually adjust the heating factor for different weather years
- The `weather_assumption` field ("normal", "warm", "cold") is planned for future work to apply NOAA normals instead of actual weather
