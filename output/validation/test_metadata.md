# Model Execution Metadata
**Run ID:** 74e2bba6c4af
**Scenario:** Test Scenario
**Run Date:** 2026-04-15T18:28:43.302414
**Base Year:** 2025
**Forecast Horizon:** 10 years

## Scenario Parameters
- **housing_growth_rate:** 0.01
- **electrification_rate:** 0.05

## Data Sources
- **NW Natural Premise Data** (loaded): Blinded premise characteristics (location, segment, vintage)
- **NW Natural Equipment Data** (loaded): Equipment inventory by premise (type, efficiency, vintage)
- **NW Natural Billing Data** (loaded): Historical billing data for calibration
- **Weather Data** (loaded): Daily temperature and precipitation (2008-2025)
- **RBSA 2022** (loaded): Residential Building Stock Assessment (NEEA)
- **IRP Forecast** (loaded): NW Natural 2025 IRP 10-year UPC forecast

## Data Gaps
### Equipment Efficiency Ratings
**Description:** Not all equipment has explicit efficiency ratings in NW Natural data
**Impact:** Used RBSA-derived efficiency distributions and defaults
**Mitigation:** Calibrated against billing data

### Building Envelope Characteristics
**Description:** NW Natural data lacks detailed envelope properties (insulation, window type)
**Impact:** Used RBSA 2022 building shell data as proxy
**Mitigation:** Validated against historical UPC trends

### Occupancy and Usage Patterns
**Description:** No detailed occupancy or usage pattern data available
**Impact:** Used RECS national averages and RBSA metering data
**Mitigation:** Calibrated to billing-derived consumption


## Key Assumptions
### Heating Degree Days (HDD) Model
**Description:** Space heating consumption modeled as linear function of HDD (base 65°F)
**Justification:** Standard industry practice; validated against RBSA metering data

### Equipment Replacement via Weibull Survival
**Description:** Equipment replacement timing follows Weibull survival distribution
**Justification:** Empirically grounded in ASHRAE service life data

### Baseload Consumption Factors
**Description:** Non-weather-sensitive end uses (cooking, drying) modeled as constant annual consumption
**Justification:** Derived from RECS 2020 and RBSA metering data

### Weather Station Assignment
**Description:** Premises assigned to nearest weather station by district
**Justification:** Practical approach given limited weather station coverage


## Model Limitations
### Spatial Resolution
**Description:** Model operates at premise level but aggregates to district/system level. No sub-district geographic granularity.
**Scope:** Affects ability to analyze localized demand patterns

### Temporal Resolution
**Description:** Model produces annual demand projections. No monthly or daily profiles.
**Scope:** Limits ability to analyze peak demand or seasonal patterns

### Calibration Scope
**Description:** Calibrated to 2025 baseline year. Historical calibration limited to available billing data.
**Scope:** Projections beyond 2035 increasingly uncertain

### Electrification Modeling
**Description:** Fuel switching rates are scenario parameters, not endogenously determined. No economic optimization or market dynamics.
**Scope:** Electrification projections depend on scenario assumptions

### Data Blinding
**Description:** NW Natural data is blinded (premise IDs anonymized). Cannot validate against specific customer accounts.
**Scope:** Limits ability to identify and correct premise-level errors


## Disclaimer
This model is a prototype framework for academic and illustrative purposes only. Outputs are not suitable for regulatory filings or production forecasting. Results should be interpreted with consideration of documented limitations and data gaps. See limitations section for details.
