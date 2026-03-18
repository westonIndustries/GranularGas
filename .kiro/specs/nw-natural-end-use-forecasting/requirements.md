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
