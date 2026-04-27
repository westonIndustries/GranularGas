# HDD Normalization and Weather Year Handling

## The Problem

The heating factor is calibrated against 2025 billing data and 2025 weather data. But the 2025 weather file (`DailyCalDay1985_Mar2025.csv`) only covers January through March — the data ends at March 2025. This means:

- **Calibration HDD (2025, partial)**: ~1,846 degree-days (3 months, Jan–Mar)
- **Full year HDD (2024, complete)**: ~3,847 degree-days (12 months)

When the simulation falls back to 2024 weather (because 2025 doesn't have all 12 months), it uses roughly 2× the HDD that the heating factor was calibrated against. Without normalization, this produces 2× the therms — a ~60% overestimate vs the IRP.

---

## The Fix

The model automatically normalizes the heating factor when the simulation uses a different weather year than the calibration year:

```
effective_heating_factor = config_heating_factor × (calibration_HDD / actual_HDD)
```

For the 2025 calibration / 2024 simulation case:
```
effective_heating_factor = 0.187502 × (1,846 / 3,847) = 0.089976
```

This ensures that regardless of which weather year the simulation uses, the total annual therms remain consistent with the calibrated billing data.

---

## How It Works

1. The model checks if the target year (2025) has weather data for all 12 months
2. If not, it finds the most recent year with complete 12-month coverage (2024)
3. It computes the weighted average HDD for both years across all weather stations
4. The heating factor is scaled by the ratio of calibration HDD to actual HDD
5. The simulation runs with the adjusted heating factor

---

## Verification

Both annual and monthly simulation paths produce identical annual UPC after normalization:

| Scenario | Weather Year | Raw HDD | Effective HF | 2025 UPC | 2035 UPC |
|----------|-------------|---------|-------------|----------|----------|
| Annual | 2025 (partial) | 1,846 | 0.187502 | 499.2 | 424.8 |
| Monthly | 2024 (full) | 3,847 | 0.089976 | 499.2 | 424.8 |

The annual totals match because the HDD normalization compensates for the different weather year.

---

## Weather Year Selection Logic

The model uses this priority for selecting weather data:

1. **Target year with 12 months** — use as-is, no normalization needed
2. **Target year with < 12 months** — fall back to most recent year with 12 months, apply HDD normalization
3. **No year with 12 months** — use whatever is available, log a warning

For the annual simulation path, the threshold is lower (>100 records) because it sums all available days regardless of month coverage. For the monthly path, all 12 months must be present.

---

## HDD History

The `hdd_history.csv` output shows the weighted average HDD for each year from 1985 to 2025. Typical PNW HDD range: 3,200–4,500 degree-days per year. The 2025 partial value of 1,846 represents only January–March, which is the coldest quarter and accounts for roughly 48% of annual HDD.

**Reference HDD values (NOAA 1991–2020 normals, base 65°F):**

| Station | ICAO | Annual Normal HDD |
|---------|------|------------------|
| Portland | KPDX | 4,850 |
| Eugene | KEUG | 4,650 |
| Salem | KSLE | 4,900 |
| Astoria | KAST | 5,200 |
| The Dalles | KDLS | 5,800 |
| Coos Bay | KOTH | 4,400 |
| Newport | KONP | 4,600 |
| Corvallis | KCVO | 4,750 |
| Hillsboro | KHIO | 4,900 |
| Troutdale | KTTD | 5,100 |
| Vancouver | KVUO | 4,950 |

---

## Output Files

Each scenario folder contains:

- `hdd_info.csv` — calibration year, actual weather year, HDD values, ratio, effective heating factor
- `hdd_history.csv` — annual weighted HDD from 1985 to present

---

## Implications for Scenario Design

When creating new scenarios:

- The `heating_factor` in the JSON is always relative to the calibration year's HDD
- The model automatically adjusts if the simulation uses different weather
- You do not need to manually adjust the heating factor for different weather years
- The `weather_assumption` field (`"normal"`, `"warm"`, `"cold"`) is planned for future work to apply NOAA normals instead of actual weather

---

## Weather Normalization (Future Work)

The NOAA 30-year Climate Normals (1991–2020) are loaded for all 11 weather stations and a weather adjustment factor is computed:

```
weather_adjustment_factor(s, y) = actual_HDD(s, y) / normal_HDD(s)
```

This factor is available in the model output but is not yet applied to scenario projections. Future work would use this to run "normal weather" scenarios that are independent of any particular historical year's weather anomalies.

---

## Related Documentation

- **[FORMULAS.md](FORMULAS.md)** — HDD formula and weather adjustment factor formula
- **[ALGORITHM.md](ALGORITHM.md)** — Where HDD normalization fits in the simulation loop
