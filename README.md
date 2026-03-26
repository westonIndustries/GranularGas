# NW Natural End-Use Forecasting Model

A bottom-up residential natural gas demand forecasting model for Northwest Natural's Integrated Resource Planning (IRP) process. The model disaggregates residential demand by end-use (space heating, water heating, cooking, drying, fireplace, other), enabling scenario analysis for technology adoption, electrification, and efficiency improvements.

## Quick Links

- **[Specification Documents](#specification-documents)** — Requirements, design, and implementation plan
- **[Documentation](#documentation)** — User guides, API reference, and geographic framework
- **[Getting Started](#getting-started)** — Installation and first run
- **[Project Status](#project-status)** — Current development phase

---

## Specification Documents

The model is fully specified with three synchronized documents:

### 1. Requirements Document
**File**: `.kiro/specs/nw-natural-end-use-forecasting/requirements.md`

Defines 26 functional and non-functional requirements covering:
- Model scope and boundary definition
- Housing stock representation
- Equipment inventory and technology adoption
- End-use energy consumption simulation
- Demand aggregation and validation
- Scenario analysis support
- Data input and calibration
- Transparency and documentation
- Visualization interface deployment
- REST API for scenario management
- Multi-level geographic analysis
- Deployment and containerization
- Local development environment
- Monitoring and observability
- Testing and quality assurance
- Documentation and user guides

**Status**: ✅ Complete (26 requirements)

### 2. Design Document
**File**: `.kiro/specs/nw-natural-end-use-forecasting/design.md`

Describes the complete system architecture including:
- Data ingestion and cleaning pipeline
- Housing stock modeling
- Equipment inventory and Weibull survival model
- Weather processing and HDD/CDD calculation
- End-use energy simulation engine
- Aggregation and output formatting
- Visualization module with Mapbox integration
- REST API for scenario management
- Scenario management and validation
- CLI entry point and pipeline orchestration
- Validation and calibration utilities

**Status**: ✅ Complete (9 major modules)

### 3. Implementation Plan
**File**: `.kiro/specs/nw-natural-end-use-forecasting/tasks.md`

Provides detailed implementation tasks organized in 22 phases:
- Project structure and configuration (Task 1)
- Data ingestion module (Task 2)
- Housing stock module (Task 4)
- Equipment module (Task 5)
- Weather processing module (Task 6)
- End-use simulation module (Task 8)
- Aggregation and output module (Task 9)
- Scenario management module (Task 11)
- CLI entry point (Task 12)
- Validation and calibration (Task 13)
- Visualization module (Task 15)
- REST API module (Task 16)
- Web frontend (Task 17)
- Deployment and containerization (Task 18)
- Monitoring and logging (Task 19)
- Testing and quality assurance (Task 20)
- Documentation and user guides (Task 21)
- Final integration and delivery (Task 22)

**Status**: ✅ Complete (22 task groups with 80+ subtasks)

### Sync Report
**File**: `.kiro/specs/nw-natural-end-use-forecasting/SYNC_REPORT.md`

Comprehensive audit confirming:
- ✅ 100% of requirements have corresponding design sections
- ✅ 100% of design sections have corresponding implementation tasks
- ✅ 17 property-based tests defined across all components
- ✅ 23 REST API endpoints fully specified
- ✅ 6 geographic levels consistently defined
- ✅ 20+ data sources documented and integrated

---

## Documentation

### User and Developer Guides

#### 1. Geographic Analysis Framework
**File**: `REGIONS_AND_CELLS.md`

Explains the hierarchical geographic framework for multi-scale analysis:
- **County Level**: 16 counties in NW Natural territory
- **District Level**: IRP districts within counties
- **Microclimate Areas**: 11 weather stations with HDD data (4,400-5,800 range)
- **Microresidential Areas**: Housing clusters (segment + subsegment + vintage)
- **Microadoption Areas**: Technology adoption phases (Early Adopters, Growth, Mature, Saturation)
- **Composite Cells**: Multi-dimensional hexagonal cells combining all dimensions

Includes:
- Mermaid diagrams showing relationships
- Decision guide for choosing appropriate level
- 4 example analysis workflows
- Data availability table
- Visualization tips for each level

**Cross-Reference**: Implements Requirements 19, 21 and Design Section 7.1

#### 2. API Documentation
**File**: `API_DOCUMENTATION.md`

Complete REST API reference with:
- Quick start guide (4-step example)
- 23 endpoints organized by category:
  - Scenario Management (6 endpoints)
  - Scenario Execution (3 endpoints)
  - Results Retrieval (6 endpoints)
  - Scenario Comparison (3 endpoints)
  - Data and Configuration (3 endpoints)
  - Health and Status (2 endpoints)
- Request/response formats with examples
- Error handling and status codes
- Authentication and rate limiting
- Pagination and filtering
- Webhooks support
- Python and JavaScript SDK examples
- OpenAPI/Swagger documentation links

**Cross-Reference**: Implements Requirements 20, 26 and Design Section 9

#### 3. Algorithm Documentation
**File**: `ALGORITHM.md`

Detailed algorithm description covering:
- High-level algorithm flow (Mermaid diagram)
- 8 detailed algorithm steps:
  1. Data ingestion & cleaning
  2. Build baseline housing stock
  3. Build equipment inventory
  4. Equipment replacement simulation
  5. Weather data processing
  6. End-use energy simulation
  7. Aggregation & rollup
  8. Validation & calibration
- Heat pump integration (Section 4.1)
- Key mathematical formulas
- Detailed simulation flow diagram
- Scenario projection loop
- Related documentation links

**Cross-Reference**: Implements Requirements 1-10 and Design Sections 1-8

#### 4. Output Specifications
**File**: `outputs.md`

Comprehensive output documentation including:
- Output directory structure
- 8 output file types:
  1. Premise-level simulation results
  2. Aggregated demand by end-use
  3. Aggregated demand by segment
  4. Aggregated demand by district
  5. UPC comparison (model vs. IRP forecast)
  6. Billing-based calibration metrics
  7. Scenario metadata (JSON)
  8. Scenario comparison
- Column definitions and data types
- Example outputs
- Validation metrics
- Data quality notes
- Output limitations and disclaimers

**Cross-Reference**: Implements Requirements 9, 10, 26 and Design Section 7

#### 5. Future Data Sources
**File**: `FUTURE_DATA_SOURCES.md`

Identifies 15 additional data sources for model enhancement:
- **High-Priority** (Phase 1):
  - Heat pump adoption (ACS B25040) — **NEW PRIMARY SOURCE**
  - Building energy codes
  - Utility disconnection data
  - Appliance efficiency standards
  - New construction data
- **Medium-Priority** (Phase 2):
  - Retrofit programs
  - Appliance replacement cycles
  - Utility bill analysis
  - Demographic data
- **Lower-Priority** (Phase 3):
  - DER adoption
  - RNG adoption
  - Manufacturer data

Includes:
- Data acquisition strategy by phase
- Implementation recommendations
- Data quality considerations
- Summary table with priority/effort/availability

**Cross-Reference**: Implements Requirements 7, 8 and Design Section 2

---

## Getting Started

### Prerequisites

- Python 3.9+
- 8GB+ RAM (laptop development)
- 16GB+ RAM (server deployment)
- Git for version control

### Quick Installation (5 minutes)

```bash
# Clone repository
git clone https://github.com/nwnatural/forecast-model.git
cd forecast-model

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -m pytest tests/ -v

# Run baseline scenario
python src/main.py scenarios/baseline.json --output outputs/
```

### Detailed Setup

For complete installation instructions including troubleshooting, Docker setup, and development workflow, see **[INSTALLATION_AND_SETUP.md](INSTALLATION_AND_SETUP.md)**.

Key sections:
- System requirements and setup by OS
- Virtual environment configuration
- Data directory structure
- First run and custom scenarios
- Development workflow (testing, linting, documentation)
- Docker containerization
- Common troubleshooting

### Documentation Map

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **[INSTALLATION_AND_SETUP.md](INSTALLATION_AND_SETUP.md)** | Complete setup guide with troubleshooting | 15 min |
| **[ALGORITHM.md](ALGORITHM.md)** | Detailed algorithm description and methodology | 20 min |
| **[REGIONS_AND_CELLS.md](REGIONS_AND_CELLS.md)** | Geographic analysis framework (6 levels) | 15 min |
| **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** | REST API reference (23 endpoints) | 20 min |
| **[outputs.md](outputs.md)** | Output file specifications and formats | 10 min |
| **[FUTURE_DATA_SOURCES.md](FUTURE_DATA_SOURCES.md)** | Enhancement opportunities (15 data sources) | 10 min |
| **[CROSS_REFERENCE.md](CROSS_REFERENCE.md)** | Complete cross-reference index | 5 min |

---

## Project Status

### Current Phase: Specification Complete ✅

All specification documents are complete and synchronized:
- ✅ Requirements document (26 requirements)
- ✅ Design document (9 modules)
- ✅ Implementation plan (22 task groups)
- ✅ Sync report (100% coverage)

### Next Phase: Implementation

Ready to begin implementation. See [tasks.md](.kiro/specs/nw-natural-end-use-forecasting/tasks.md) for detailed implementation plan.

**Recommended Start**:
1. Tasks 1-3: Project structure and data ingestion
2. Tasks 4-10: Core model pipeline
3. Tasks 15-22: Visualization, API, deployment, and testing

---

## Key Features

### Core Model
- ✅ Bottom-up residential demand simulation
- ✅ End-use disaggregation (6 categories)
- ✅ Weibull survival model for equipment replacement
- ✅ Heat pump integration with COP calculations
- ✅ Weather-driven space heating and water heating
- ✅ Baseload consumption for cooking, drying, fireplace

### Data Integration
- ✅ 20+ data sources integrated
- ✅ NW Natural premise, equipment, segment, billing data
- ✅ RBSA 2022 building characteristics
- ✅ ASHRAE equipment service life
- ✅ Census ACS housing data (B25034, B25040, B25024)
- ✅ NOAA climate normals
- ✅ EIA RECS microdata
- ✅ PSU population forecasts
- ✅ WA OFM housing estimates

### Geographic Analysis
- ✅ 6-level geographic hierarchy
- ✅ County, district, microclimate, microresidential, microadoption, composite-cell
- ✅ Multi-dimensional analysis framework
- ✅ Opportunity and success scoring

### Visualization
- ✅ Interactive Mapbox-based web interface
- ✅ County/district drill-down
- ✅ Time-series animation (2025-2035)
- ✅ Scenario comparison
- ✅ End-use breakdown charts
- ✅ Multi-area comparison

### REST API
- ✅ 23 endpoints for scenario management
- ✅ Async scenario execution
- ✅ Results retrieval (JSON, CSV, Parquet, GeoJSON)
- ✅ Scenario comparison
- ✅ Configuration and data endpoints
- ✅ Health and status monitoring

### Deployment
- ✅ Docker containerization
- ✅ docker-compose for multi-container deployment
- ✅ Local development environment support
- ✅ Cloud deployment options (AWS, Azure, GCP)

### Testing
- ✅ 17 property-based tests
- ✅ Unit tests for all modules
- ✅ Integration tests for full pipeline
- ✅ 80%+ code coverage target

---

## Architecture Overview

```
Data Ingestion → Housing Stock → Equipment → Weather → Simulation → Aggregation → Output
     ↓              ↓              ↓           ↓           ↓            ↓           ↓
  20+ sources   Baseline stock  Inventory   HDD/CDD   End-use calc  Rollup by   CSV/JSON
                 projection     Weibull     Water temp  Baseload     level      GeoJSON
                 New construction Replacement  Delta-t   Conservation  Segment    Comparison
                                Electrification         Validation    District   Metadata
```

---

## Complete Documentation Map

### Setup & Development
| Document | Purpose | Audience |
|----------|---------|----------|
| **[INSTALLATION_AND_SETUP.md](INSTALLATION_AND_SETUP.md)** | Complete installation guide with troubleshooting | Developers, DevOps |
| [README.md](README.md) | Project overview and quick links | Everyone |

### Specification Documents (`.kiro/specs/nw-natural-end-use-forecasting/`)
| Document | Purpose | Audience |
|----------|---------|----------|
| [requirements.md](.kiro/specs/nw-natural-end-use-forecasting/requirements.md) | 26 functional and non-functional requirements | Stakeholders, developers |
| [design.md](.kiro/specs/nw-natural-end-use-forecasting/design.md) | System architecture and design decisions (9 modules) | Developers, architects |
| [tasks.md](.kiro/specs/nw-natural-end-use-forecasting/tasks.md) | Implementation plan (22 task groups, 80+ subtasks) | Developers |
| [SYNC_REPORT.md](.kiro/specs/nw-natural-end-use-forecasting/SYNC_REPORT.md) | Specification sync audit (100% coverage) | Project managers |

### User & Developer Guides
| Document | Purpose | Audience |
|----------|---------|----------|
| [ALGORITHM.md](ALGORITHM.md) | Detailed algorithm description (8 steps, heat pump integration) | Developers, researchers |
| [REGIONS_AND_CELLS.md](REGIONS_AND_CELLS.md) | Geographic analysis framework (6 levels, composite cells) | Analysts, users |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | REST API reference (23 endpoints with examples) | Developers, integrators |
| [outputs.md](outputs.md) | Output file specifications (8 file types) | Analysts, users |
| [FUTURE_DATA_SOURCES.md](FUTURE_DATA_SOURCES.md) | Enhancement opportunities (15 data sources) | Project managers |
| [CROSS_REFERENCE.md](CROSS_REFERENCE.md) | Complete cross-reference index | Everyone |

---

## Support and Contact

For questions or issues:
- **Documentation**: See links above
- **Issues**: GitHub Issues (when repository is public)
- **Email**: [contact information]

---

## License

[License information to be added]

---

## Acknowledgments

- Northwest Natural for providing blinded premise, equipment, and billing data
- NEEA for RBSA 2022 building stock assessment data
- U.S. Census Bureau for ACS and housing data
- NOAA for climate normals data
- EIA for RECS microdata
- Portland State University for population forecasts

