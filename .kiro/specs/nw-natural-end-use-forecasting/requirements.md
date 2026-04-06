# Requirements Document

## Introduction

This document defines requirements for a bottom-up residential end-use demand forecasting model for Northwest Natural's Integrated Resource Planning (IRP) process. The model will complement existing top-down econometric models by disaggregating residential demand by end use, providing improved visibility into underlying demand drivers including end-use consumption patterns, equipment efficiency, technology adoption, and policy-driven electrification.

The model will be a prototype framework suitable for long-term scenario analysis and planning insight under evolving technology, policy, and market conditions. It will focus exclusively on residential end-use modeling and will not be deployed for production-level forecasting or regulatory filings.

## Glossary

- **NW Natural**: Northwest Natural, a regulated natural gas utility serving approximately 2 million customers across Oregon and Southwest Washington
- **IRP**: Integrated Resource Planning, NW Natural's long-term planning process for evaluating future demand, infrastructure needs, and compliance with regulatory requirements
- **UPC**: Use Per Customer, the current top-down econometric approach for estimating aggregate residential demand
- **End-use**: A specific energy-consuming application within a residential building (e.g., space heating, water heating, cooking, clothes drying, space cooling)
- **Housing stock**: The total number and characteristics of residential units in a service territory
- **Fuel switching**: The transition from one energy source to another (e.g., natural gas to electricity) in residential applications
- **Equipment efficiency**: The energy conversion efficiency of residential appliances and equipment
- **Replacement cycle**: The typical lifespan and replacement timing of residential equipment
- **Scenario analysis**: The evaluation of future demand under alternative assumptions about technology, policy, and market conditions

## Requirements

### Requirement 1: Model Scope and Boundary Definition

**User Story:** As a planning analyst, I want the model to clearly define its scope and boundaries, so that I understand what residential end uses are included and what assumptions govern the modeling approach.

#### Acceptance Criteria

1. THE Model SHALL explicitly define all residential end uses included in the simulation (e.g., space heating, water heating, cooking, clothes drying, space cooling, lighting, plug loads)
2. THE Model SHALL exclude commercial and industrial end uses from the residential simulation
3. WHERE customer segments are defined, THE Model SHALL specify the segmentation criteria (e.g., building type, climate zone, income level)
4. WHILE simulating demand, THE Model SHALL maintain clear boundaries between end uses to prevent double-counting or omission

### Requirement 2: Housing Stock Representation

**User Story:** As a planning analyst, I want the model to represent the residential housing stock accurately, so that demand projections reflect realistic building characteristics and distribution.

#### Acceptance Criteria

1. WHEN historical housing data is available, THE Model SHALL use it to calibrate the initial housing stock representation
2. THE Model SHALL represent housing units by key attributes including: construction year, square footage, number of bedrooms, building type, and climate zone
3. WHILE projecting into future years, THE Model SHALL simulate housing stock dynamics including new construction, demolition, and retrofit activity
4. IF housing data is unavailable for a specific attribute, THEN THE Model SHALL document the data gap and apply reasonable assumptions with clear justification

### Requirement 3: Equipment Inventory and Technology Adoption

**User Story:** As a planning analyst, I want the model to track equipment inventory and technology adoption over time, so that I can evaluate the impact of efficiency improvements and fuel switching.

#### Acceptance Criteriacbilling_data_blinded.csv

1. WHEN equipment data is available, THE Model SHALL use it to establish baseline equipment inventories by end use
2. THE Model SHALL track equipment characteristics including: type (e.g., furnace, boiler, heat pump), efficiency rating, fuel type, and installation year
3. WHILE projecting into future years, THE Model SHALL simulate equipment replacement based on age, remaining useful life, and technology adoption rates
4. WHERE technology adoption data is available, THE Model SHALL incorporate it to project future equipment transitions (e.g., gas furnace to heat pump)

### Requirement 4: End-Use Energy Consumption Simulation

**User Story:** As a planning analyst, I want the model to simulate energy consumption for each end use, so that I can understand how demand is distributed across applications.

#### Acceptance Criteria

1. WHEN weather data is available, THE Model SHALL use it to drive weather-sensitive end uses (e.g., space heating, space cooling)
2. THE Model SHALL calculate end-use energy consumption based on: equipment efficiency, usage patterns, and operating conditions
3. WHILE simulating consumption, THE Model SHALL apply end-use specific load shapes that reflect typical usage patterns
4. IF multiple fuel types are supported, THEN THE Model SHALL track consumption separately by fuel type

### Requirement 5: Demand Aggregation and Validation

**User Story:** As a planning analyst, I want the model to aggregate end-use demand to system-level totals, so that I can compare bottom-up projections to existing forecasts.

#### Acceptance Criteria

1. WHEN end-use demand is simulated, THE Model SHALL aggregate it to system-level totals by year and customer segment
2. THE Model SHALL provide demand outputs in consistent units with existing forecasting tools (e.g., therms per year, peak demand in MW)
3. WHERE historical aggregate demand data is available, THE Model SHALL enable comparison between bottom-up projections and historical trends
4. WHILE aggregating demand, THE Model SHALL maintain traceability from end-use contributions to system totals

### Requirement 6: Scenario Analysis Support

**User Story:** As a planning analyst, I want the model to support multiple scenario definitions, so that I can evaluate demand under alternative assumptions about technology, policy, and market conditions.

#### Acceptance Criteria

1. WHEN a new scenario is defined, THE Model SHALL allow specification of key parameters including: technology adoption rates, efficiency improvement trajectories, and electrification targets
2. THE Model SHALL run each scenario independently and store results separately for comparison
3. WHILE running scenarios, THE Model SHALL maintain consistent baseline assumptions across all scenarios except those explicitly varied
4. WHERE scenario parameters are interdependent, THEN THE Model SHALL validate parameter combinations for consistency

### Requirement 7: Data Input and Calibration

**User Story:** As a planning analyst, I want the model to accept and process relevant data inputs, so that I can calibrate it to NW Natural's service territory.

#### Acceptance Criteria

1. WHEN billing data is available, THE Model SHALL use it to calibrate baseline consumption patterns
2. WHEN weather data is available, THE Model SHALL use it to calibrate weather-sensitive end uses
3. WHEN equipment inventory data is available, THE Model SHALL use it to establish baseline equipment characteristics
4. IF data is incomplete or unavailable, THEN THE Model SHALL document data limitations and apply reasonable assumptions with clear justification
5. EACH data loader SHALL be implemented as a standalone script in `src/loaders/` that can be run independently for debugging (`python -m src.loaders.<name>`)
6. WHEN a loader runs standalone, IT SHALL print a summary to console and save diagnostic output (summary text + sample CSV) to `output/loaders/`
7. THE `data_ingestion.py` module SHALL re-export all individual loaders for backward compatibility with downstream modules

### Requirement 8: Transparency and Documentation

**User Story:** As a planning analyst, I want the model to be transparent about its assumptions and methods, so that I can understand and validate its outputs.

#### Acceptance Criteria

1. THE Model SHALL document all key assumptions including: housing stock dynamics, equipment replacement rates, technology adoption curves, and usage patterns
2. WHEN model outputs are generated, THE Model SHALL provide metadata explaining the scenario, date, and key parameters used
3. WHILE running simulations, THE Model SHALL log significant events including data gaps, assumption applications, and calibration adjustments
4. IF model limitations affect results, THEN THE Model SHALL clearly identify and quantify those limitations

### Requirement 9: Model Output Format and Accessibility

**User Story:** As a planning analyst, I want the model outputs to be accessible and interpretable, so that I can use them for scenario analysis and presentation.

#### Acceptance Criteria

1. WHEN model runs are completed, THE Model SHALL produce outputs in a structured format (e.g., CSV, JSON) suitable for further analysis
2. THE Model SHALL provide outputs at multiple aggregation levels including: end use, customer segment, and system total
3. WHILE generating outputs, THE Model SHALL include time series data for demand projections (e.g., annual totals, monthly profiles)
4. WHERE comparative analysis is requested, THEN THE Model SHALL enable side-by-side comparison with existing aggregate forecasts

### Requirement 10: Model Limitations and Validation

**User Story:** As a planning analyst, I want the model to clearly communicate its limitations, so that I understand when and how to use its outputs appropriately.

#### Acceptance Criteria

1. THE Model SHALL document its limitations including: data availability, spatial resolution, temporal resolution, and calibration scope
2. WHEN validation data is available, THE Model SHALL compare outputs to observed data and quantify discrepancies
3. WHILE running simulations, THE Model SHALL flag results that fall outside expected ranges or indicate potential issues
4. IF model outputs are intended for illustrative purposes only, THEN THE Model SHALL clearly state that limitation

### Requirement 11: Local Development and Testing Environment

**User Story:** As a developer, I want to be able to run and test the model on my laptop, so that I can develop and validate features locally before deployment.

#### Acceptance Criteria

1. THE Model SHALL be installable on a standard laptop (Windows, macOS, Linux) with Python 3.9+ and 8GB+ RAM
2. WHEN dependencies are installed, THE Model SHALL run a complete simulation in under 5 minutes on a laptop with 8GB RAM
3. THE Model SHALL provide a local development server for testing the visualization interface without external dependencies
4. WHILE running locally, THE Model SHALL support all core functionality including: data ingestion, simulation, aggregation, and visualization
5. IF a developer runs the model locally, THEN THE Model SHALL produce identical results to the production deployment (deterministic output)
6. THE Model SHALL include a quick-start guide for local setup and testing (README with step-by-step instructions)
7. WHEN running locally, THE Model SHALL support hot-reload of code changes for rapid iteration during development

### Requirement 12: Deployment Packaging and Distribution

**User Story:** As a deployment engineer, I want the model to be packaged for easy deployment to production environments, so that it can be shared and run reliably across different systems.

#### Acceptance Criteria

1. THE Model SHALL be packaged as a Docker container with all dependencies included
2. WHEN the Docker image is built, IT SHALL be reproducible and deterministic (same image hash for same source code)
3. THE Model SHALL include a docker-compose.yml file for easy multi-container deployment (model + visualization + optional database)
4. WHILE running in Docker, THE Model SHALL support environment variable configuration for scenario parameters, data paths, and API settings
5. THE Model SHALL provide a requirements.txt file for pip installation in non-containerized environments
6. IF the model is deployed to a cloud platform, THEN IT SHALL support common deployment targets (AWS, Azure, GCP, Heroku)
7. THE Model SHALL include deployment documentation covering: Docker setup, environment configuration, data mounting, and troubleshooting
8. WHEN deploying to production, THE Model SHALL support health checks and monitoring endpoints for operational visibility

### Requirement 13: Visualization Interface Deployment

**User Story:** As a stakeholder, I want to access the visualization interface through a web browser, so that I can explore forecast results interactively.

#### Acceptance Criteria

1. THE Visualization interface SHALL be accessible via a web browser (Chrome, Firefox, Safari, Edge)
2. WHEN the model is deployed, THE Visualization SHALL be served via a REST API (Flask or FastAPI)
3. THE Visualization interface SHALL load and render maps with 100+ geographic regions in under 3 seconds
4. WHILE interacting with the visualization, THE Visualization SHALL respond to user actions (slider, dropdown, click) in under 500ms
5. IF the visualization is deployed to a cloud platform, THEN IT SHALL support HTTPS/TLS encryption for secure data transmission
6. THE Visualization SHALL work on desktop (1920x1080+) and tablet (iPad) screen sizes
7. WHEN the visualization loads, IT SHALL display a default scenario (e.g., Business as Usual) without requiring user configuration

### Requirement 14: Data Management and Persistence

**User Story:** As an operator, I want the model to manage data efficiently, so that I can store and retrieve simulation results without manual file management.

#### Acceptance Criteria

1. WHEN simulation results are generated, THE Model SHALL store them in a structured format (CSV, Parquet, or database)
2. THE Model SHALL support both file-based storage (for local development) and database storage (for production)
3. WHILE storing results, THE Model SHALL include metadata (scenario name, date, parameters, version) for traceability
4. IF multiple scenarios are run, THEN THE Model SHALL organize results by scenario for easy comparison
5. THE Model SHALL provide a data export function to download results in common formats (CSV, Excel, JSON)
6. WHEN deploying to production, THE Model SHALL support persistent volumes for data storage across container restarts

### Requirement 15: Performance and Scalability

**User Story:** As an operator, I want the model to perform efficiently, so that I can run multiple scenarios and serve many concurrent users.

#### Acceptance Criteria

1. WHEN running a single scenario on a laptop, THE Model SHALL complete in under 5 minutes
2. WHEN running on a server with 16GB RAM and 4 CPU cores, THE Model SHALL complete in under 2 minutes
3. WHILE serving the visualization interface, THE Model SHALL support at least 10 concurrent users without degradation
4. IF the visualization is accessed by many users, THEN THE Model SHALL cache results to reduce API response times
5. THE Model SHALL support parallel execution of multiple scenarios (if hardware allows)
6. WHEN deploying to production, THE Model SHALL be horizontally scalable (multiple instances behind a load balancer)

### Requirement 16: Monitoring, Logging, and Debugging

**User Story:** As an operator, I want visibility into model execution, so that I can troubleshoot issues and monitor performance.

#### Acceptance Criteria

1. WHEN the model runs, IT SHALL log all significant events (data loading, simulation progress, aggregation, output generation)
2. THE Model SHALL provide structured logging (JSON format) for easy parsing and analysis
3. WHILE running, THE Model SHALL track execution time for each major step (data ingestion, simulation, aggregation)
4. IF an error occurs, THEN THE Model SHALL provide detailed error messages with context (line number, variable state, data sample)
5. THE Model SHALL support debug mode for verbose logging during development
6. WHEN deployed to production, THE Model SHALL integrate with standard monitoring tools (Prometheus, CloudWatch, etc.)
7. THE Model SHALL provide a health check endpoint that returns model status and recent execution metrics

### Requirement 17: Testing and Quality Assurance

**User Story:** As a developer, I want comprehensive tests to ensure model correctness, so that I can confidently deploy changes.

#### Acceptance Criteria

1. THE Model SHALL include unit tests for all core modules (data ingestion, simulation, aggregation, visualization)
2. WHEN tests are run, THEY SHALL achieve at least 80% code coverage for critical paths
3. THE Model SHALL include integration tests that verify end-to-end workflows (data → simulation → output)
4. WHILE running tests, THE Model SHALL complete in under 2 minutes on a standard laptop
5. IF a test fails, THEN THE Model SHALL provide clear error messages indicating the failure reason
6. THE Model SHALL include property-based tests for correctness properties (e.g., conservation of demand, non-negativity)
7. WHEN deploying to production, THE Model SHALL run all tests automatically (CI/CD pipeline)

### Requirement 18: Documentation and User Guides

**User Story:** As a user, I want clear documentation, so that I can understand how to use the model and interpret results.

#### Acceptance Criteria

1. THE Model SHALL include a README with quick-start instructions for local setup and first run
2. THE Model SHALL provide API documentation (OpenAPI/Swagger) for all REST endpoints
3. WHILE using the visualization, THE Model SHALL include tooltips and help text explaining each feature
4. THE Model SHALL include a user guide covering: scenario definition, result interpretation, and common use cases
5. IF the model is deployed to production, THEN IT SHALL include operational documentation (deployment, configuration, troubleshooting)
6. THE Model SHALL include example notebooks (Jupyter) demonstrating common analysis workflows
7. WHEN model outputs are generated, THEY SHALL include a data dictionary explaining all columns and units




### Requirement 19: Interactive Visualization with Geographic Drill-Down

**User Story:** As a stakeholder, I want to explore forecast results interactively on a map, so that I can understand demand patterns across different geographic and demographic segments.

#### Acceptance Criteria

1. WHEN the visualization interface loads, THE Map SHALL display the NW Natural service territory with county boundaries color-coded by demand intensity
2. WHEN a user clicks on a county, THE Map SHALL zoom to that county and display district-level boundaries
3. WHEN a user selects a view option, THE Map SHALL switch between: county, district, microclimate, microresidential, microadoption, and composite-cell views
4. WHILE the user moves the year slider, THE Map colors SHALL update to reflect demand for that year
5. WHEN a user selects a scenario, THE Map SHALL update to show results for that scenario
6. IF a user hovers over a geographic area, THEN THE Visualization SHALL display a tooltip with key metrics (demand, UPC, electrification rate)
7. WHEN a user clicks on an area, THE Visualization SHALL display a detail panel with time-series charts and end-use breakdown
8. IF a user selects multiple areas, THEN THE Visualization SHALL display a comparison chart showing trends for all selected areas

### Requirement 20: REST API for Scenario Management and Results

**User Story:** As a developer, I want to programmatically create scenarios, submit runs, and retrieve results via REST API, so that I can integrate the model with other systems.

#### Acceptance Criteria

1. WHEN a POST request is sent to `/api/v1/scenarios`, THE API SHALL create a new scenario and return a scenario_id
2. WHEN a GET request is sent to `/api/v1/scenarios`, THE API SHALL return a paginated list of all scenarios
3. WHEN a POST request is sent to `/api/v1/scenarios/{scenario_id}/run`, THE API SHALL submit the scenario for execution and return a run_id
4. WHILE a scenario is running, WHEN a GET request is sent to `/api/v1/runs/{run_id}`, THE API SHALL return the current execution status and progress
5. WHEN a scenario completes, WHEN a GET request is sent to `/api/v1/runs/{run_id}/results`, THE API SHALL return aggregated results in JSON, CSV, or Parquet format
6. WHEN a GET request is sent to `/api/v1/runs/{run_id}/results/geojson`, THE API SHALL return results as GeoJSON for map visualization
7. IF a request contains invalid parameters, THEN THE API SHALL return a 400 Bad Request with detailed error message
8. WHEN the API receives a request, IT SHALL validate the request and return appropriate HTTP status codes (200, 201, 400, 404, 500)

### Requirement 21: Multi-Level Geographic Analysis

**User Story:** As an analyst, I want to analyze demand at multiple geographic levels (county, district, microclimate, microresidential, microadoption, composite-cell), so that I can understand demand drivers at different scales.

#### Acceptance Criteria

1. THE Model SHALL support aggregation at six geographic levels: county, district, microclimate, microresidential, microadoption, and composite-cell
2. WHEN results are aggregated at any level, THE Model SHALL maintain conservation of demand (sum of sub-areas equals parent area)
3. WHEN a user requests results at a specific level, THE API SHALL return data with appropriate geographic identifiers and metrics
4. IF a user requests comparison across multiple areas, THEN THE API SHALL return time-series data for all selected areas in a format suitable for charting
5. WHEN composite cells are generated, THEY SHALL combine all microregion dimensions into a single multi-dimensional analytical unit
6. IF a user filters composite cells by attributes, THEN THE API SHALL return only cells matching the filter criteria

### Requirement 22: Deployment and Containerization

**User Story:** As an operator, I want to deploy the model to production using Docker, so that I can run it reliably across different environments.

#### Acceptance Criteria

1. THE Model SHALL be packaged as a Docker container with all dependencies included
2. WHEN the Docker image is built, IT SHALL be reproducible and deterministic (same image hash for same source code)
3. THE Model SHALL include a docker-compose.yml file for easy multi-container deployment
4. WHILE running in Docker, THE Model SHALL support environment variable configuration for scenario parameters and API settings
5. WHEN the container starts, IT SHALL perform health checks and report status via `/api/v1/health` endpoint
6. IF the model is deployed to a cloud platform, THEN IT SHALL support common deployment targets (AWS, Azure, GCP, Heroku)
7. THE Model SHALL include deployment documentation covering: Docker setup, environment configuration, data mounting, and troubleshooting

### Requirement 23: Local Development Environment

**User Story:** As a developer, I want to run and test the model on my laptop, so that I can develop and validate features locally.

#### Acceptance Criteria

1. THE Model SHALL be installable on a standard laptop (Windows, macOS, Linux) with Python 3.9+ and 8GB+ RAM
2. WHEN dependencies are installed via `pip install -r requirements.txt`, THE Model SHALL be ready to run
3. WHEN a developer runs a complete simulation locally, IT SHALL complete in under 5 minutes on a laptop with 8GB RAM
4. THE Model SHALL provide a local development server for testing the visualization interface without external dependencies
5. WHILE running locally, THE Model SHALL support all core functionality including: data ingestion, simulation, aggregation, and visualization
6. IF a developer runs the model locally, THEN THE Model SHALL produce identical results to the production deployment (deterministic output)
7. THE Model SHALL include a quick-start guide (README) with step-by-step instructions for local setup and testing

### Requirement 24: Monitoring and Observability

**User Story:** As an operator, I want visibility into model execution, so that I can troubleshoot issues and monitor performance.

#### Acceptance Criteria

1. WHEN the model runs, IT SHALL log all significant events (data loading, simulation progress, aggregation, output generation)
2. THE Model SHALL provide structured logging in JSON format for easy parsing and analysis
3. WHILE running, THE Model SHALL track execution time for each major step (data ingestion, simulation, aggregation)
4. IF an error occurs, THEN THE Model SHALL provide detailed error messages with context (line number, variable state, data sample)
5. THE Model SHALL support debug mode for verbose logging during development
6. WHEN deployed to production, THE Model SHALL integrate with standard monitoring tools (Prometheus, CloudWatch, etc.)
7. THE Model SHALL provide a health check endpoint that returns model status and recent execution metrics

### Requirement 25: Testing and Quality Assurance

**User Story:** As a developer, I want comprehensive tests to ensure model correctness, so that I can confidently deploy changes.

#### Acceptance Criteria

1. THE Model SHALL include unit tests for all core modules (data ingestion, simulation, aggregation, visualization, API)
2. WHEN tests are run, THEY SHALL achieve at least 80% code coverage for critical paths
3. THE Model SHALL include integration tests that verify end-to-end workflows (data → simulation → output)
4. WHILE running tests, THE Model SHALL complete in under 2 minutes on a standard laptop
5. IF a test fails, THEN THE Model SHALL provide clear error messages indicating the failure reason
6. THE Model SHALL include property-based tests for correctness properties (e.g., conservation of demand, non-negativity)
7. WHEN deploying to production, THE Model SHALL run all tests automatically (CI/CD pipeline)

### Requirement 26: Documentation and User Guides

**User Story:** As a user, I want clear documentation, so that I can understand how to use the model and interpret results.

#### Acceptance Criteria

1. THE Model SHALL include a README with quick-start instructions for local setup and first run
2. THE Model SHALL provide API documentation (OpenAPI/Swagger) for all REST endpoints
3. WHILE using the visualization, THE Model SHALL include tooltips and help text explaining each feature
4. THE Model SHALL include a user guide covering: scenario definition, result interpretation, and common use cases
5. IF the model is deployed to production, THEN IT SHALL include operational documentation (deployment, configuration, troubleshooting)
6. THE Model SHALL include example notebooks (Jupyter) demonstrating common analysis workflows
7. WHEN model outputs are generated, THEY SHALL include a data dictionary explaining all columns and units
8. THE Model SHALL include documentation explaining geographic levels and cells (REGIONS_AND_CELLS.md)
9. THE Model SHALL include comprehensive API documentation (API_DOCUMENTATION.md) with endpoint reference and examples

