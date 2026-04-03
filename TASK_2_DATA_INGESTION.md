# Task 2: Data Ingestion Module

## Status: 🔶 In Progress

## Overview

Task 2 implements individual data loaders in `src/loaders/` (one file per data source, each runnable standalone) plus validation suites. 36 loader files created, validation scripts built.

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
| 2.3 | Data ingestion validation suite (6 sub-checks) | 🔶 Partial |
| 2.3.1 | Per-loader quality reports (HTML + MD) | ✅ 9 reports |
| 2.3.2 | Cross-loader join audit | 🔲 Needs NWN data |
| 2.3.3 | Sample mismatches export | 🔲 Needs NWN data |
| 2.3.4 | Column coverage matrix | ✅ |
| 2.3.5 | Date range check | ✅ |
| 2.3.6 | Distribution plots | 🔲 Needs NWN data |
| 2.4 | Join integrity validation suite (5 sub-checks) | 🔲 Needs NWN data |

## How to Run

```bash
# Run individual loader
python -m src.loaders.load_premise_data

# Run all validation checks
python -m src.validation.run_all

# Run join integrity checks
python -m src.validation.join_integrity.run_all
```

## Output Locations

- `output/loaders/` — per-loader summary + sample CSV
- `output/data_quality/` — quality reports, column coverage, date ranges, distributions
- `output/join_integrity/` — join audit, end-use mapping, efficiency validation, dashboard
