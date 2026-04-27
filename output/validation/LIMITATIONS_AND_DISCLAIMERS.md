# Model Limitations and Disclaimers

## Executive Summary

This document describes the limitations, assumptions, and data gaps in the NW Natural End-Use Forecasting Model. This model is a prototype framework for academic and illustrative purposes only and is not suitable for regulatory filings or production forecasting.

## Disclaimer

This model is a prototype framework for academic and illustrative purposes only. Outputs are not suitable for regulatory filings or production forecasting. Results should be interpreted with consideration of documented limitations and data gaps. See limitations section for details.

## Data Gaps and Mitigation

### Equipment Efficiency Ratings

**Description:** Not all equipment has explicit efficiency ratings in NW Natural data

**Impact on Model:** Used RBSA-derived efficiency distributions and defaults

**Mitigation Strategy:** Calibrated against billing data

### Building Envelope Characteristics

**Description:** NW Natural data lacks detailed envelope properties (insulation, window type)

**Impact on Model:** Used RBSA 2022 building shell data as proxy

**Mitigation Strategy:** Validated against historical UPC trends

### Occupancy and Usage Patterns

**Description:** No detailed occupancy or usage pattern data available

**Impact on Model:** Used RECS national averages and RBSA metering data

**Mitigation Strategy:** Calibrated to billing-derived consumption

## Key Assumptions

### Heating Degree Days (HDD) Model

Space heating consumption modeled as linear function of HDD (base 65°F)

**Justification:** Standard industry practice; validated against RBSA metering data

### Equipment Replacement via Weibull Survival

Equipment replacement timing follows Weibull survival distribution

**Justification:** Empirically grounded in ASHRAE service life data

### Baseload Consumption Factors

Non-weather-sensitive end uses (cooking, drying) modeled as constant annual consumption

**Justification:** Derived from RECS 2020 and RBSA metering data

### Weather Station Assignment

Premises assigned to nearest weather station by district

**Justification:** Practical approach given limited weather station coverage

## Model Limitations

### Spatial Resolution

Model operates at premise level but aggregates to district/system level. No sub-district geographic granularity.

**Scope:** Affects ability to analyze localized demand patterns

### Temporal Resolution

Model produces annual demand projections. No monthly or daily profiles.

**Scope:** Limits ability to analyze peak demand or seasonal patterns

### Calibration Scope

Calibrated to 2025 baseline year. Historical calibration limited to available billing data.

**Scope:** Projections beyond 2035 increasingly uncertain

### Electrification Modeling

Fuel switching rates are scenario parameters, not endogenously determined. No economic optimization or market dynamics.

**Scope:** Electrification projections depend on scenario assumptions

### Data Blinding

NW Natural data is blinded (premise IDs anonymized). Cannot validate against specific customer accounts.

**Scope:** Limits ability to identify and correct premise-level errors

## Recommended Use Cases

This model is appropriate for:

- Academic research and capstone projects
- Exploratory scenario analysis
- Understanding end-use demand drivers
- Identifying data gaps and research needs
- Prototyping bottom-up forecasting approaches

## Not Recommended For

This model is NOT appropriate for:

- Regulatory filings or official forecasts
- Production deployment without significant validation
- Long-term forecasts beyond 10 years
- Premise-level billing or rate-setting decisions
- Comparison to historical data without calibration

## Validation Status

The model has been validated against:

- NW Natural's IRP 10-year UPC forecast
- Billing-derived therms per premise
- RBSA building stock characteristics
- EIA RECS end-use consumption benchmarks

See validation reports in `output/validation/` for details.

## Contact and Questions

For questions about model limitations or appropriate use cases, contact the model development team.

**Report Generated:** 2026-04-15T18:28:43.337058
