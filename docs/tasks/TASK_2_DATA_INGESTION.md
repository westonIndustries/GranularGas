# Task 2: Data Ingestion Module

## Status: 🔶 In Progress

## Overview

Task 2 implements individual data loaders in `src/loaders/` (one file per data source, each runnable standalone) plus validation suites. 36 loader files created, validation scripts built and executed.

## Sub-tasks

| # | Description | Status |
|---|-------------|--------|
| 2.1 | Create `src/loaders/` package (36 individual loader files) | ✅ |
| 2.1.1 | Core NW Natural loaders (7 files: premise, equipment, segment, codes, weather, water temp, snow) | ✅ |
| 2.1.2 | Billing and tariff loaders (6 files: billing, OR/WA rates, WACOG, rate cases, billing→therms) | ✅ |
| 2.1.3 | RBSA building stock loaders (6 files: site detail, HVAC, water heater, distributions, metering, 2017) | ✅ |
| 2.1.4 | ASHRAE loaders (3 files: service life, maintenance cost, useful life table) | ✅ |
| 2.1.5 | IRP/calibration loaders (4 files: load decay, historical UPC, baseload factors, energy proxies) | ✅ |
| 2.1.6 | GBR API loader (1 file) | ✅ |
| 2.1.7 | Census ACS loaders (5 files: FIPS, B25034 API, B25034/B25040/B25024 county) | ✅ |
| 2.1.8 | Population/housing loaders (2 files: PSU forecasts, OFM housing) | ✅ |
| 2.1.9 | NOAA normals loader (1 file) | ✅ |
| 2.1.10 | RECS microdata loader (1 file) | ✅ |
| 2.2 | `build_premise_equipment_table` join function | ✅ |
| 2.3 | Data ingestion validation suite (6 sub-checks) | ✅ |
| 2.3.1 | Per-loader quality reports (HTML + MD) | ✅ 9 reports (public data sources) |
| 2.3.2 | Cross-loader join audit | ✅ (awaits NWN data for blinded_id overlap) |
| 2.3.3 | Sample mismatches export | ✅ (awaits NWN data for full results) |
| 2.3.4 | Column coverage matrix | ✅ |
| 2.3.5 | Date range check | ✅ |
| 2.3.6 | Distribution plots | ✅ (awaits NWN data for equipment/billing/weather plots) |
| 2.4 | Join integrity validation suite (5 sub-checks) | 🔲 Needs NWN data |

## How to Run

```bash
# Run individual loader
python -m src.loaders.load_premise_data

# Run data quality validation suite (task 2.3)
python -m src.validation.data_quality

# Run join integrity checks (task 2.4 — requires NWN data)
python -m src.validation.join_integrity
```

## Output Locations

- `output/loaders/` — per-loader summary txt + sample CSV
- `output/data_quality/` — quality reports (HTML + MD), column coverage, date ranges, join audit, validation failures CSV, distribution plots
- `output/join_integrity/` — join audit, end-use mapping, efficiency validation, dashboard (requires NWN data)

## Notes on NW Natural Data Dependency

Tasks 2.3.2, 2.3.3, and 2.3.6 produce partial output today — the framework runs and writes files, but the blinded_id overlap audit, validation failures CSV, and equipment/billing/weather distribution plots will populate fully once `Data/NWNatural Data/` files are present. All other outputs (tariff, WACOG, rate cases, baseload factors, energy proxies, service territory FIPS) are complete.
