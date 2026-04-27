# Cross-Reference Index: NW Natural End-Use Forecasting Model

This document provides a comprehensive cross-reference between all specification documents and supporting documentation, enabling easy navigation and verification of completeness.

---

## Document Organization

### Specification Documents (`.kiro/specs/nw-natural-end-use-forecasting/`)

1. **requirements.md** — 26 functional and non-functional requirements
2. **design.md** — System architecture and design decisions (9 modules)
3. **tasks.md** — Implementation plan (22 task groups, 80+ subtasks)
4. **SYNC_REPORT.md** — Specification sync audit (100% coverage verification)

### Root-Level Documentation

1. **README.md** — Project overview and quick links
2. **REGIONS_AND_CELLS.md** — Geographic analysis framework (6 levels)
3. **API_DOCUMENTATION.md** — REST API reference (23 endpoints)
4. **ALGORITHM.md** — Detailed algorithm description
5. **outputs.md** — Output specifications (8 file types)
6. **FUTURE_DATA_SOURCES.md** — Additional data sources (15 sources)
7. **CROSS_REFERENCE.md** — This document

---

## Requirements → Design → Tasks Mapping

### Requirement 1: Model Scope and Boundary Definition

**Requirement**: Define all residential end uses included in simulation

**Design Coverage**:
- Section 1: Overview (end-use categories)
- Section 2: data_ingestion.py (END_USE_MAP)
- Section 4: config.py (END_USE_MAP dictionary)

**Task Coverage**:
- Task 1.1: Define END_USE_MAP in config.py
- Task 2.1: Implement load_equipment_codes()
- Task 2.2: Implement build_premise_equipment_table()

**Documentation**:
- ALGORITHM.md: Section 1 (Data Ingestion)
- outputs.md: End-use categories (6 types)

---

### Requirement 2: Housing Stock Representation

**Requirement**: Represent residential housing stock accurately

**Design Coverage**:
- Section 4: housing_stock.py (HousingStock dataclass)
- Section 2: data_ingestion.py (load_premise_data)

**Task Coverage**:
- Task 4.1: Create housing_stock.py with HousingStock dataclass
- Task 4.2: Implement project_stock() for future year projection
- Task 4.3: Property test for housing stock projection

**Documentation**:
- ALGORITHM.md: Section 2 (Build Baseline Housing Stock)
- REGIONS_AND_CELLS.md: County and district levels

---

### Requirement 3: Equipment Inventory and Technology Adoption

**Requirement**: Track equipment inventory and technology adoption over time

**Design Coverage**:
- Section 5: equipment.py (EquipmentProfile, Weibull survival model)
- Section 4.1: Heat pump integration

**Task Coverage**:
- Task 5.1: Create equipment.py with EquipmentProfile and Weibull functions
- Task 5.2: Implement apply_replacements() for equipment transitions
- Task 5.3-5.4: Property tests for equipment replacement logic

**Documentation**:
- ALGORITHM.md: Section 3 (Build Equipment Inventory)
- ALGORITHM.md: Section 4 (Equipment Replacement Simulation)
- ALGORITHM.md: Section 4.1 (Heat Pump Integration)

---

### Requirement 4: End-Use Energy Consumption Simulation

**Requirement**: Simulate energy consumption for each end use

**Design Coverage**:
- Section 6: weather.py (HDD/CDD calculation)
- Section 8: simulation.py (end-use simulation functions)

**Task Coverage**:
- Task 6.1: Create weather.py with HDD/CDD computation
- Task 6.2-6.3: Property tests for weather processing
- Task 8.1: Create simulation.py with per-end-use functions
- Task 8.2: Implement simulate_all_end_uses() orchestrator
- Task 8.3-8.4: Property tests for simulation

**Documentation**:
- ALGORITHM.md: Section 5 (Weather Data Processing)
- ALGORITHM.md: Section 6 (End-Use Energy Simulation)

---

### Requirement 5: Demand Aggregation and Validation

**Requirement**: Aggregate end-use demand to system-level totals

**Design Coverage**:
- Section 7: aggregation.py (rollup and export functions)

**Task Coverage**:
- Task 9.1: Create aggregation.py with rollup functions
- Task 9.2-9.3: Property tests for aggregation conservation

**Documentation**:
- ALGORITHM.md: Section 7 (Aggregation & Rollup)
- outputs.md: Aggregated demand by end-use, segment, district

---

### Requirement 6: Scenario Analysis Support

**Requirement**: Support multiple scenario definitions

**Design Coverage**:
- Section 8: scenarios.py (ScenarioConfig, validation, runner)

**Task Coverage**:
- Task 11.1: Create scenarios.py with ScenarioConfig
- Task 11.2: Implement run_scenario() pipeline orchestrator
- Task 11.3: Implement compare_scenarios()
- Task 11.4-11.5: Property tests for scenario isolation and validation

**Documentation**:
- ALGORITHM.md: Scenario Projection Loop (Mermaid diagram)
- API_DOCUMENTATION.md: Scenario Management endpoints

---

### Requirement 7: Data Input and Calibration

**Requirement**: Accept and process relevant data inputs

**Design Coverage**:
- Section 2: data_ingestion.py (50+ data loading functions)
- Section 1: config.py (40+ file path constants)

**Task Coverage**:
- Task 2.1: Implement all data loading functions
- Task 13.1: Add billing-based calibration

**Documentation**:
- ALGORITHM.md: Section 1 (Data Ingestion & Cleaning)
- FUTURE_DATA_SOURCES.md: 15 additional data sources
- Design Section 1: Data Folder Organization (24 data sources documented)

---

### Requirement 8: Transparency and Documentation

**Requirement**: Document all key assumptions and methods

**Design Coverage**:
- Section 13: Validation and limitation reporting

**Task Coverage**:
- Task 13.3: Add documentation and limitation metadata

**Documentation**:
- ALGORITHM.md: Complete algorithm documentation
- outputs.md: Scenario metadata (JSON) and limitations
- SYNC_REPORT.md: Specification completeness audit

---

### Requirement 9: Model Output Format and Accessibility

**Requirement**: Produce outputs in structured format

**Design Coverage**:
- Section 7: aggregation.py (export_results)

**Task Coverage**:
- Task 9.1: Implement export_results()

**Documentation**:
- outputs.md: 8 output file types with column definitions
- API_DOCUMENTATION.md: Results retrieval endpoints

---

### Requirement 10: Model Limitations and Validation

**Requirement**: Clearly communicate limitations

**Design Coverage**:
- Section 13: Validation and limitation reporting

**Task Coverage**:
- Task 13.1-13.3: Implement validation and limitation reporting

**Documentation**:
- outputs.md: Output limitations and disclaimers
- ALGORITHM.md: Key mathematical formulas and assumptions

---

### Requirement 11: Local Development and Testing Environment

**Requirement**: Run and test model on laptop

**Design Coverage**:
- Section 12: main.py (CLI entry point)

**Task Coverage**:
- Task 12.1: Create main.py as CLI entry point
- Task 18.1-18.4: Create Docker and deployment documentation

**Documentation**:
- README.md: Getting Started section
- FUTURE_DATA_SOURCES.md: Phase 1 data sources

---

### Requirement 12: Deployment Packaging and Distribution

**Requirement**: Package for easy deployment

**Design Coverage**:
- Section 12: main.py (CLI orchestration)

**Task Coverage**:
- Task 18.1-18.5: Create Docker, docker-compose, requirements.txt

**Documentation**:
- README.md: Installation section

---

### Requirement 13: Visualization Interface Deployment

**Requirement**: Access visualization through web browser

**Design Coverage**:
- Section 7.1: visualization.py (Mapbox integration)

**Task Coverage**:
- Task 15.1-15.4: Implement visualization module
- Task 17.1-17.4: Implement web frontend

**Documentation**:
- REGIONS_AND_CELLS.md: Geographic hierarchy and visualization tips
- API_DOCUMENTATION.md: GeoJSON endpoint

---

### Requirement 14: Data Management and Persistence

**Requirement**: Manage data efficiently

**Design Coverage**:
- Section 9: api.py (data storage and retrieval)

**Task Coverage**:
- Task 16.3: Implement results retrieval endpoints

**Documentation**:
- outputs.md: Output directory structure

---

### Requirement 15: Performance and Scalability

**Requirement**: Perform efficiently

**Design Coverage**:
- Section 12: main.py (pipeline orchestration)

**Task Coverage**:
- Task 20.3: Create performance benchmarks

**Documentation**:
- README.md: Prerequisites (8GB+ RAM)

---

### Requirement 16: Monitoring, Logging, and Debugging

**Requirement**: Visibility into model execution

**Design Coverage**:
- Section 13: Validation and logging

**Task Coverage**:
- Task 19.1-19.3: Implement monitoring and logging

**Documentation**:
- outputs.md: Execution logs

---

### Requirement 17: Testing and Quality Assurance

**Requirement**: Comprehensive tests for correctness

**Design Coverage**:
- All sections: Property-based tests defined

**Task Coverage**:
- Task 20.1-20.3: Create test suite and CI/CD

**Documentation**:
- SYNC_REPORT.md: 17 property-based tests documented

---

### Requirement 18: Documentation and User Guides

**Requirement**: Clear documentation

**Design Coverage**:
- Section 21: Documentation

**Task Coverage**:
- Task 21.1-21.5: Create documentation and notebooks

**Documentation**:
- README.md: Documentation map
- REGIONS_AND_CELLS.md: User guide for geographic framework
- API_DOCUMENTATION.md: API reference
- ALGORITHM.md: Algorithm documentation
- outputs.md: Output specifications

---

### Requirement 19: Interactive Visualization with Geographic Drill-Down

**Requirement**: Explore results interactively on map

**Design Coverage**:
- Section 7.1: visualization.py (Mapbox integration, drill-down)

**Task Coverage**:
- Task 15.1-15.4: Implement visualization module
- Task 17.1-17.4: Implement web frontend

**Documentation**:
- REGIONS_AND_CELLS.md: Complete geographic framework
- API_DOCUMENTATION.md: GeoJSON and visualization endpoints

---

### Requirement 20: REST API for Scenario Management and Results

**Requirement**: Programmatically create scenarios and retrieve results

**Design Coverage**:
- Section 9: api.py (23 endpoints)

**Task Coverage**:
- Task 16.1-16.7: Implement REST API module

**Documentation**:
- API_DOCUMENTATION.md: Complete API reference (23 endpoints)

---

### Requirement 21: Multi-Level Geographic Analysis

**Requirement**: Analyze demand at multiple geographic levels

**Design Coverage**:
- Section 7.1: visualization.py (6 geographic levels)

**Task Coverage**:
- Task 15.1-15.3: Implement geographic aggregation functions

**Documentation**:
- REGIONS_AND_CELLS.md: 6 geographic levels with definitions
- API_DOCUMENTATION.md: Geographic areas endpoint

---

### Requirement 22: Deployment and Containerization

**Requirement**: Deploy using Docker

**Design Coverage**:
- Section 12: main.py (CLI orchestration)

**Task Coverage**:
- Task 18.1-18.5: Create Docker configuration

**Documentation**:
- README.md: Installation section

---

### Requirement 23: Local Development Environment

**Requirement**: Run and test on laptop

**Design Coverage**:
- Section 12: main.py (CLI entry point)

**Task Coverage**:
- Task 12.1: Create main.py
- Task 18.1-18.4: Create deployment documentation

**Documentation**:
- README.md: Getting Started section

---

### Requirement 24: Monitoring and Observability

**Requirement**: Visibility into execution

**Design Coverage**:
- Section 13: Validation and logging

**Task Coverage**:
- Task 19.1-19.3: Implement monitoring

**Documentation**:
- outputs.md: Execution logs

---

### Requirement 25: Testing and Quality Assurance

**Requirement**: Comprehensive tests

**Design Coverage**:
- All sections: Property-based tests

**Task Coverage**:
- Task 20.1-20.3: Create test suite

**Documentation**:
- SYNC_REPORT.md: 17 property-based tests

---

### Requirement 26: Documentation and User Guides

**Requirement**: Clear documentation

**Design Coverage**:
- Section 21: Documentation

**Task Coverage**:
- Task 21.1-21.5: Create documentation

**Documentation**:
- README.md: Documentation map
- REGIONS_AND_CELLS.md: Geographic framework
- API_DOCUMENTATION.md: API reference
- ALGORITHM.md: Algorithm documentation
- outputs.md: Output specifications
- FUTURE_DATA_SOURCES.md: Data sources

---

## Data Source Coverage

### Integrated Data Sources (20+)

| Data Source | Design Section | Task | Documentation |
|-------------|----------------|------|-----------------|
| NW Natural premise data | 2 | 2.1 | ALGORITHM.md §1 |
| NW Natural equipment data | 2 | 2.1 | ALGORITHM.md §1 |
| NW Natural segment data | 2 | 2.1 | ALGORITHM.md §1 |
| NW Natural billing data | 2 | 2.1, 13.1 | ALGORITHM.md §1 |
| Weather data (CalDay/GasDay) | 6 | 6.1 | ALGORITHM.md §5 |
| Bull Run water temperature | 6 | 6.1 | ALGORITHM.md §5 |
| Portland snow data | 2 | 2.1 | Design §1 |
| Tariff rates (OR/WA) | 2 | 2.1 | Design §1 |
| RBSA 2022 building data | 2 | 2.1 | Design §1 |
| ASHRAE service life | 2 | 2.1 | Design §1 |
| NW Natural IRP forecast | 2 | 2.1, 13.2 | Design §1 |
| Baseload consumption factors | 2 | 2.1 | Design §1 |
| NW energy proxies | 2 | 2.1 | Design §1 |
| Green Building Registry API | 2 | 2.1 | Design §1 |
| RBSA sub-metered data (RBSAM) | 2 | 2.1 | Design §1 |
| 2017 RBSA-II database | 2 | 2.1 | Design §1 |
| Census ACS B25034 | 2 | 2.1 | Design §1 |
| Census ACS B25040 | 2 | 2.1 | Design §1 |
| Census ACS B25024 | 2 | 2.1 | Design §1 |
| PSU population forecasts | 2 | 2.1 | Design §1 |
| WA OFM housing estimates | 2 | 2.1 | Design §1 |
| NOAA climate normals | 2 | 2.1 | Design §1 |
| EIA RECS microdata | 2 | 2.1 | Design §1 |

### Future Data Sources (15)

| Data Source | Priority | Documentation |
|-------------|----------|-----------------|
| Heat pump adoption (ACS B25040) | High | FUTURE_DATA_SOURCES.md §1 |
| Building energy codes | High | FUTURE_DATA_SOURCES.md §2 |
| Utility disconnection data | High | FUTURE_DATA_SOURCES.md §3 |
| Appliance efficiency standards | High | FUTURE_DATA_SOURCES.md §4 |
| New construction data | High | FUTURE_DATA_SOURCES.md §5 |
| Retrofit programs | Medium | FUTURE_DATA_SOURCES.md §6 |
| Appliance replacement cycles | Medium | FUTURE_DATA_SOURCES.md §7 |
| Utility bill analysis | Medium | FUTURE_DATA_SOURCES.md §8 |
| Demographic data | Medium | FUTURE_DATA_SOURCES.md §9 |
| Rate structure evolution | Low | FUTURE_DATA_SOURCES.md §11 |
| Industrial/commercial demand | Low | FUTURE_DATA_SOURCES.md §12 |
| RNG adoption | Low | FUTURE_DATA_SOURCES.md §13 |
| DER adoption | Low | FUTURE_DATA_SOURCES.md §14 |
| Manufacturer data | Low | FUTURE_DATA_SOURCES.md §15 |
| Equipment service life | Medium | FUTURE_DATA_SOURCES.md §9 |

---

## Geographic Levels Coverage

| Level | Design Section | Task | Documentation |
|-------|----------------|------|-----------------|
| County | 7.1 | 15.1 | REGIONS_AND_CELLS.md §1 |
| District | 7.1 | 15.1 | REGIONS_AND_CELLS.md §2 |
| Microclimate | 7.1 | 15.1 | REGIONS_AND_CELLS.md §3A |
| Microresidential | 7.1 | 15.1 | REGIONS_AND_CELLS.md §3B |
| Microadoption | 7.1 | 15.1 | REGIONS_AND_CELLS.md §3C |
| Composite-cell | 7.1 | 15.1 | REGIONS_AND_CELLS.md §4 |

---

## API Endpoints Coverage

| Endpoint Category | Count | Design Section | Task | Documentation |
|-------------------|-------|----------------|------|-----------------|
| Scenario Management | 6 | 9 | 16.1 | API_DOCUMENTATION.md |
| Scenario Execution | 3 | 9 | 16.2 | API_DOCUMENTATION.md |
| Results Retrieval | 6 | 9 | 16.3 | API_DOCUMENTATION.md |
| Scenario Comparison | 3 | 9 | 16.4 | API_DOCUMENTATION.md |
| Data and Configuration | 3 | 9 | 16.4 | API_DOCUMENTATION.md |
| Health and Status | 2 | 9 | 16.5 | API_DOCUMENTATION.md |

**Total**: 23 endpoints fully specified

---

## Property-Based Tests Coverage

| Component | Property | Task | Documentation |
|-----------|----------|------|-----------------|
| config.py | END_USE_MAP completeness | 1.2 | SYNC_REPORT.md |
| data_ingestion.py | Filtering preserves residential | 2.3 | SYNC_REPORT.md |
| data_ingestion.py | Join integrity | 2.4 | SYNC_REPORT.md |
| housing_stock.py | Stock projection math | 4.3 | SYNC_REPORT.md |
| equipment.py | Weibull survival monotonicity | 5.3 | SYNC_REPORT.md |
| equipment.py | Replacement probability bounds | 5.3 | SYNC_REPORT.md |
| equipment.py | Equipment count conservation | 5.4 | SYNC_REPORT.md |
| weather.py | HDD/CDD computation | 6.2 | SYNC_REPORT.md |
| weather.py | Water heating delta | 6.3 | SYNC_REPORT.md |
| simulation.py | Non-negativity | 8.3 | SYNC_REPORT.md |
| simulation.py | Efficiency impact | 8.4 | SYNC_REPORT.md |
| aggregation.py | Aggregation conservation | 9.2 | SYNC_REPORT.md |
| aggregation.py | UPC computation | 9.3 | SYNC_REPORT.md |
| scenarios.py | Scenario determinism | 11.4 | SYNC_REPORT.md |
| scenarios.py | Scenario validation | 11.5 | SYNC_REPORT.md |
| visualization.py | Composite score bounds | 15.4 | SYNC_REPORT.md |
| visualization.py | Opportunity/Success relationship | 15.4 | SYNC_REPORT.md |

**Total**: 17 property-based tests

---

## Output Files Coverage

| Output File | Design Section | Task | Documentation |
|-------------|----------------|------|-----------------|
| simulation_results_{year}.csv | 7 | 9.1 | outputs.md |
| aggregated_by_enduse_{year}.csv | 7 | 9.1 | outputs.md |
| aggregated_by_segment_{year}.csv | 7 | 9.1 | outputs.md |
| aggregated_by_district_{year}.csv | 7 | 9.1 | outputs.md |
| upc_comparison_{year}.csv | 7 | 9.1, 13.2 | outputs.md |
| calibration_metrics.csv | 13 | 13.1 | outputs.md |
| scenario_metadata.json | 13 | 13.3 | outputs.md |
| scenario_comparison.csv | 7 | 11.3 | outputs.md |

**Total**: 8 output file types

---

## Navigation Guide

### For Requirements Stakeholders
1. Start with [README.md](README.md) for project overview
2. Review [requirements.md](.kiro/specs/nw-natural-end-use-forecasting/requirements.md) for detailed requirements
3. Check [SYNC_REPORT.md](.kiro/specs/nw-natural-end-use-forecasting/SYNC_REPORT.md) for completeness verification

### For Developers
1. Start with [README.md](README.md) for project overview
2. Review [design.md](.kiro/specs/nw-natural-end-use-forecasting/design.md) for architecture
3. Review [tasks.md](.kiro/specs/nw-natural-end-use-forecasting/tasks.md) for implementation plan
4. Reference [ALGORITHM.md](ALGORITHM.md) for detailed methodology
5. Use [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for REST API reference

### For Analysts/Users
1. Start with [README.md](README.md) for project overview
2. Review [REGIONS_AND_CELLS.md](REGIONS_AND_CELLS.md) for geographic framework
3. Review [outputs.md](outputs.md) for output specifications
4. Reference [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API usage

### For Project Managers
1. Start with [README.md](README.md) for project overview
2. Review [tasks.md](.kiro/specs/nw-natural-end-use-forecasting/tasks.md) for implementation plan
3. Check [SYNC_REPORT.md](.kiro/specs/nw-natural-end-use-forecasting/SYNC_REPORT.md) for completeness
4. Reference [FUTURE_DATA_SOURCES.md](FUTURE_DATA_SOURCES.md) for enhancement opportunities

---

## Completeness Verification

### Specification Documents
- ✅ Requirements: 26/26 requirements documented
- ✅ Design: 9/9 modules documented
- ✅ Tasks: 22/22 task groups documented
- ✅ Sync: 100% coverage verified

### Documentation
- ✅ README: Project overview and quick links
- ✅ REGIONS_AND_CELLS: 6 geographic levels
- ✅ API_DOCUMENTATION: 23 endpoints
- ✅ ALGORITHM: 8 algorithm steps
- ✅ outputs: 8 output file types
- ✅ FUTURE_DATA_SOURCES: 15 data sources
- ✅ CROSS_REFERENCE: This document

### Data Sources
- ✅ Integrated: 20+ sources documented
- ✅ Future: 15 sources identified
- ✅ Coverage: 100% of requirements

### Geographic Levels
- ✅ County: Documented
- ✅ District: Documented
- ✅ Microclimate: Documented
- ✅ Microresidential: Documented
- ✅ Microadoption: Documented
- ✅ Composite-cell: Documented

### API Endpoints
- ✅ Scenario Management: 6 endpoints
- ✅ Scenario Execution: 3 endpoints
- ✅ Results Retrieval: 6 endpoints
- ✅ Scenario Comparison: 3 endpoints
- ✅ Data and Configuration: 3 endpoints
- ✅ Health and Status: 2 endpoints
- ✅ Total: 23 endpoints

### Property-Based Tests
- ✅ 17 tests defined across all components
- ✅ 100% of major modules covered

---

## Summary

All specification documents and supporting documentation are complete, synchronized, and properly cross-referenced:

- **26 requirements** fully specified
- **9 design modules** fully documented
- **22 task groups** with 80+ subtasks
- **7 root-level documentation files** providing comprehensive guidance
- **20+ integrated data sources** documented
- **15 future data sources** identified
- **6 geographic levels** defined
- **23 REST API endpoints** specified
- **17 property-based tests** defined
- **8 output file types** documented

The specification is ready for implementation. See [tasks.md](.kiro/specs/nw-natural-end-use-forecasting/tasks.md) for detailed implementation plan.

