# Task 3: Checkpoint — Verify Data Ingestion Pipeline

## Status: 🔲 Not Started (needs NW Natural data files)

## Overview

Task 3 is the first major checkpoint. It verifies the entire data ingestion pipeline works with actual NW Natural data and produces 6 diagnostic reports.

## Sub-tasks

| # | Description | Output | Status |
|---|-------------|--------|--------|
| 3.1 | Pipeline readiness dashboard (53 data sources) | `output/checkpoint_ingestion/pipeline_readiness.html/.md` | 🔲 |
| 3.2 | Data volume summary (row counts, expected vs actual) | `output/checkpoint_ingestion/data_volumes.html/.md` | 🔲 |
| 3.3 | Premise-equipment table profile | `output/checkpoint_ingestion/pet_profile.html/.md` | 🔲 |
| 3.4 | Service territory geographic coverage map | `output/checkpoint_ingestion/service_territory_map.html/.md` | 🔲 |
| 3.5 | Equipment and vintage distribution charts | `output/checkpoint_ingestion/equipment_vintage_charts.html/.md` | 🔲 |
| 3.6 | Cross-validation against Census/RECS benchmarks | `output/checkpoint_ingestion/cross_validation.html/.md` | 🔲 |

## Blocking On

- `Data/NWNatural Data/` folder with proprietary blinded CSV files (premise, equipment, segment, codes, billing, weather)
