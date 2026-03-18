# Additional Data Sources for Model Enhancement

## Overview

This document identifies additional data sources that would strengthen the NW Natural End-Use Forecasting Model beyond the currently integrated datasets. These sources are organized by priority and include acquisition strategies, expected impact, and implementation recommendations.

---

## High-Priority Data Sources

### 1. Heat Pump Adoption & Sales Data

**Source**: NEEA (Northwest Energy Efficiency Alliance), regional utilities, manufacturer data

**Description**: Track actual heat pump penetration rates in Oregon and Washington residential market

**Data Elements**:
- Annual heat pump sales by region/county
- Installed heat pump capacity (kW)
- Percentage of homes with heat pumps (by vintage, segment)
- Air-source vs. ground-source distribution
- Hybrid heat pump adoption (gas backup)

**Expected Impact**: 
- Validates electrification rate assumptions in scenarios
- Grounds truth for technology adoption curves
- Identifies early adopter patterns and regional variation

**Use in Model**:
- Calibrate `electrification_rate` scenario parameter
- Validate space heating and water heating fuel switching
- Inform policy scenario assumptions

**Availability**: Moderate (NEEA publishes regional data; some proprietary)

**Effort to Integrate**: Medium (requires time-series aggregation by county)

---

### 2. Building Energy Codes & Compliance Data

**Source**: Oregon Department of Energy, Washington State Energy Office, building permit records

**Description**: Track adoption and compliance with energy codes (2006, 2012, 2014, 2017, 2021 updates)

**Data Elements**:
- Code effective dates and stringency levels
- Percentage of new construction meeting each code
- Efficiency requirements by equipment type
- Regional variation in compliance

**Expected Impact**:
- Validates efficiency improvement trajectories by vintage
- Explains step-changes in equipment efficiency
- Improves model credibility for future projections

**Use in Model**:
- Calibrate `efficiency_improvement` scenario parameter
- Model realistic efficiency gains by vintage cohort
- Inform new construction efficiency assumptions

**Availability**: High (publicly available)

**Effort to Integrate**: Low (straightforward lookup table)

---

### 3. Natural Gas Utility Disconnection Data

**Source**: NW Natural internal data (if available), state regulatory filings

**Description**: Track customers switching away from gas (electrification, fuel switching, churn)

**Data Elements**:
- Annual disconnections by county/district
- Reason for disconnection (if available)
- Reconnections (churn rate)
- Trend over time (2015-2025)

**Expected Impact**:
- Validates electrification rate assumptions
- Identifies early adopter regions
- Provides empirical basis for scenario projections

**Use in Model**:
- Calibrate `electrification_rate` by region
- Validate scenario assumptions against observed trends
- Inform policy scenario timing

**Availability**: High (NW Natural has this data)

**Effort to Integrate**: Low (simple time-series analysis)

---

### 4. Appliance Efficiency Standards Timeline

**Source**: DOE Appliance Standards Program, ENERGY STAR database, manufacturer data

**Description**: Historical and projected efficiency standards for furnaces, water heaters, cooking equipment

**Data Elements**:
- Effective dates of efficiency standards
- Minimum efficiency levels (AFUE, EF, etc.) by standard
- Expected market adoption rates
- Regional variation (if any)

**Expected Impact**:
- Models realistic efficiency improvement trajectories
- Explains step-changes in equipment efficiency
- Improves forecast credibility

**Use in Model**:
- Calibrate `efficiency_improvement` scenario parameter
- Model realistic efficiency gains by equipment type
- Inform new equipment efficiency assumptions

**Availability**: High (publicly available)

**Effort to Integrate**: Low (straightforward lookup table)

---

### 5. Residential Solar & Renewable Adoption

**Source**: NREL OpenPV database, state solar incentive programs, utility data

**Description**: Track solar adoption rates by county/region

**Data Elements**:
- Annual solar installations by county
- Installed capacity (kW)
- Percentage of homes with solar
- Trend over time (2015-2025)

**Expected Impact**:
- Indirect indicator of energy efficiency interest
- Correlates with electrification trends
- Identifies early adopter regions

**Use in Model**:
- Validate scenario assumptions (policy-driven adoption)
- Identify regional variation in technology adoption
- Inform policy scenario assumptions

**Availability**: High (NREL OpenPV is public)

**Effort to Integrate**: Medium (requires spatial aggregation)

---

## Medium-Priority Data Sources

### 6. Utility Bill Analysis Data

**Source**: Utility bill benchmarking programs (e.g., ENERGY STAR Portfolio Manager), utility data

**Description**: Anonymized billing data showing consumption patterns by building type/vintage

**Data Elements**:
- Distribution of consumption by building type (SF, MF, mobile)
- Consumption by vintage cohort
- Seasonal variation
- Outliers and anomalies

**Expected Impact**:
- Validates simulated consumption against real-world patterns
- Identifies model biases or systematic errors
- Improves calibration accuracy

**Use in Model**:
- Calibrate baseload assumptions
- Validate space heating and water heating calculations
- Identify premises with unusual consumption

**Availability**: Medium (requires utility cooperation)

**Effort to Integrate**: Medium (requires statistical analysis)

---

### 7. Retrofit & Weatherization Program Data

**Source**: Oregon Weatherization Assistance Program, Washington Community Action Partnership, utility programs

**Description**: Track homes receiving efficiency upgrades (insulation, air sealing, HVAC replacement)

**Data Elements**:
- Annual retrofit count by county
- Types of upgrades (insulation, HVAC, water heater, etc.)
- Pre/post consumption data (if available)
- Estimated savings per retrofit

**Expected Impact**:
- Models realistic retrofit adoption rates
- Validates efficiency improvement assumptions
- Identifies retrofit-driven demand reduction

**Use in Model**:
- Calibrate retrofit adoption rates in scenarios
- Model demand reduction from retrofits
- Inform policy scenario assumptions

**Availability**: Medium (programs track this; may require data sharing agreement)

**Effort to Integrate**: Medium (requires aggregation and analysis)

---

### 8. New Construction Data

**Source**: Building permits (county assessor offices), Census Building Permits Survey, utility data

**Description**: Track new home construction by county, vintage, and efficiency level

**Data Elements**:
- Annual new construction count by county
- Building type (SF, MF, mobile)
- Estimated efficiency level (code compliance)
- Trend over time (2015-2025)

**Expected Impact**:
- Validates housing growth rate assumptions
- Models new construction efficiency
- Improves forecast credibility

**Use in Model**:
- Calibrate `housing_growth_rate` scenario parameter
- Model new construction efficiency (typically higher than existing stock)
- Validate housing stock projections

**Availability**: High (publicly available via Census)

**Effort to Integrate**: Low (straightforward aggregation)

---

### 9. Appliance Replacement Cycle Data

**Source**: RECS microdata (already have), manufacturer sales data, utility data

**Description**: Actual replacement rates and timing for furnaces, water heaters, appliances

**Data Elements**:
- Average equipment age at replacement
- Replacement rate by equipment type
- Seasonal variation in replacements
- Correlation with equipment failure

**Expected Impact**:
- Validates Weibull survival model parameters
- Grounds truth for equipment lifecycle assumptions
- Improves replacement timing accuracy

**Use in Model**:
- Calibrate Weibull `beta` and `eta` parameters
- Validate equipment replacement probabilities
- Improve forecast accuracy

**Availability**: Medium (RECS has some data; manufacturer data proprietary)

**Effort to Integrate**: Medium (requires statistical analysis)

---

### 10. Demographic & Household Data

**Source**: Census Bureau (American Community Survey), ESRI demographic data

**Description**: Household size, income, education, age distribution by county

**Data Elements**:
- Average household size by county
- Median household income
- Education level distribution
- Age distribution of householders

**Expected Impact**:
- Correlates with consumption patterns
- Informs scenario assumptions
- Identifies vulnerable populations

**Use in Model**:
- Correlate demographics with consumption
- Inform scenario assumptions (income-driven adoption)
- Validate segment-level projections

**Availability**: High (publicly available)

**Effort to Integrate**: Low (straightforward lookup)

---

## Lower-Priority Data Sources

### 11. Utility Rate Structure & Tariff Evolution

**Source**: NW Natural historical rate schedules, state regulatory filings

**Description**: Track how rate structures have changed (fixed vs. variable, seasonal rates)

**Data Elements**:
- Historical rate schedules (2010-2025)
- Fixed vs. variable charge evolution
- Seasonal rate variations
- Special rates (low-income, time-of-use)

**Expected Impact**:
- Improves billing-to-therms conversion accuracy
- Models rate impact on demand
- Informs policy scenario assumptions

**Use in Model**:
- Improve historical rate table reconstruction
- Model demand elasticity (if applicable)
- Validate billing calibration

**Availability**: High (NW Natural has this data)

**Effort to Integrate**: Low (straightforward lookup)

---

### 12. Industrial/Commercial Gas Demand

**Source**: NW Natural internal data, state regulatory filings

**Description**: Understand total system demand context

**Data Elements**:
- Annual commercial/industrial demand by segment
- Trend over time (2015-2025)
- Percentage of total utility demand

**Expected Impact**:
- Contextual understanding of total system
- Validates residential as % of total
- Informs long-term planning context

**Use in Model**:
- Contextual analysis only (model is residential-only)
- Validate residential demand as % of total
- Inform IRP integration recommendations

**Availability**: High (NW Natural has this data)

**Effort to Integrate**: Low (informational only)

---

### 13. Renewable Natural Gas (RNG) Adoption

**Source**: NW Natural sustainability reports, state RNG programs, utility data

**Description**: Track RNG blending rates and customer adoption

**Data Elements**:
- Annual RNG blending percentage
- Customer participation in RNG programs
- RNG sourcing and cost
- Trend over time

**Expected Impact**:
- Models low-carbon scenario
- Understands policy drivers
- Informs long-term planning

**Use in Model**:
- Inform policy scenario assumptions
- Model low-carbon pathway
- Validate scenario credibility

**Availability**: Medium (NW Natural publishes some data)

**Effort to Integrate**: Low (informational only)

---

### 14. Distributed Energy Resources (DER) Data

**Source**: NREL, state energy offices, utility data

**Description**: Battery storage, demand response, smart thermostat adoption

**Data Elements**:
- Annual DER installations by type
- Installed capacity
- Adoption rates by region
- Trend over time

**Expected Impact**:
- Models demand flexibility
- Informs scenario assumptions
- Identifies emerging technologies

**Use in Model**:
- Inform advanced scenario assumptions
- Model demand flexibility (future enhancement)
- Validate scenario credibility

**Availability**: Medium (NREL has some data; utility data proprietary)

**Effort to Integrate**: Medium (requires analysis)

---

### 15. Equipment Manufacturer Data

**Source**: AHRI (Air-Conditioning, Heating, and Refrigeration Institute), manufacturer websites

**Description**: Certified efficiency ratings, market share by equipment type

**Data Elements**:
- Certified efficiency ratings by model
- Market share by manufacturer
- Product availability by region
- Trend over time

**Expected Impact**:
- Validates efficiency assumptions
- Tracks market trends
- Improves model credibility

**Use in Model**:
- Validate efficiency assumptions
- Inform scenario assumptions
- Improve forecast credibility

**Availability**: High (AHRI is public)

**Effort to Integrate**: Low (reference data only)

---

## Data Acquisition Strategy

### Phase 1: Immediate (Capstone Project)

**High-Impact, Low-Effort Sources**:
1. Building energy codes timeline (DOE, state energy offices) — **1-2 hours**
2. Appliance efficiency standards (DOE) — **1-2 hours**
3. New construction data (Census Building Permits) — **2-4 hours**
4. Demographic data (Census ACS) — **1-2 hours**

**Recommended NW Natural Requests**:
1. Utility disconnection data (2015-2025) — **High priority**
2. Historical rate schedules (2010-2025) — **Medium priority**
3. Commercial/industrial demand context — **Low priority**

**Estimated Effort**: 8-12 hours total

---

### Phase 2: Enhancement (Post-Capstone)

**Medium-Priority Sources**:
1. Heat pump adoption data (NEEA) — **4-8 hours**
2. Retrofit program data (state programs) — **4-8 hours**
3. Appliance replacement cycle analysis — **8-12 hours**
4. Utility bill analysis (if NW Natural provides data) — **8-12 hours**

**Estimated Effort**: 24-40 hours total

---

### Phase 3: Advanced (Future Enhancements)

**Lower-Priority Sources**:
1. DER adoption data (NREL, utilities) — **4-8 hours**
2. Customer behavior research — **8-16 hours**
3. Regional economic forecasts — **4-8 hours**

**Estimated Effort**: 16-32 hours total

---

## Implementation Recommendations

### For Capstone Project

**Do Integrate**:
- Building energy codes timeline (validates efficiency by vintage)
- Appliance efficiency standards (models realistic improvements)
- New construction data (validates housing growth)
- Demographic data (contextual understanding)

**Consider Requesting from NW Natural**:
- Utility disconnection data (validates electrification assumptions)
- Historical rate schedules (improves billing conversion)

**Document as Future Enhancement**:
- Heat pump adoption data
- Retrofit program data
- Appliance replacement cycles

### For Production Deployment

**Must Have**:
1. Heat pump adoption data (validates electrification)
2. Utility disconnection data (empirical electrification rates)
3. Retrofit program data (models demand reduction)
4. New construction efficiency data (models new stock)

**Should Have**:
1. Appliance replacement cycle data (validates equipment model)
2. Utility bill analysis (calibration and validation)
3. Demographic correlations (scenario assumptions)

**Nice to Have**:
1. DER adoption data (future scenario modeling)
2. Customer behavior research (adoption curves)
3. Regional economic forecasts (scenario context)

---

## Data Quality Considerations

### Validation Checklist

For each new data source, verify:
- [ ] Data completeness (no major gaps)
- [ ] Temporal coverage (aligns with model period)
- [ ] Geographic coverage (includes NW Natural service territory)
- [ ] Data quality (documented methodology, error rates)
- [ ] Licensing/access (can be legally used)
- [ ] Update frequency (current and maintained)

### Integration Checklist

Before integrating new data:
- [ ] Document data source and methodology
- [ ] Validate against existing data (cross-checks)
- [ ] Assess impact on model outputs
- [ ] Update design.md with new data source
- [ ] Update inputs.md with new data specifications
- [ ] Add validation tests for new data

---

## Summary Table

| Priority | Data Source | Impact | Effort | Availability | Recommendation |
|----------|-------------|--------|--------|--------------|-----------------|
| High | Heat pump adoption | High | Medium | Medium | Phase 2 |
| High | Building energy codes | High | Low | High | Phase 1 |
| High | Utility disconnections | High | Low | High | Phase 1 (request NWN) |
| High | Appliance standards | High | Low | High | Phase 1 |
| High | New construction | High | Low | High | Phase 1 |
| Medium | Retrofit programs | Medium | Medium | Medium | Phase 2 |
| Medium | Appliance replacement | Medium | Medium | Medium | Phase 2 |
| Medium | Demographic data | Medium | Low | High | Phase 1 |
| Medium | Utility bill analysis | Medium | Medium | Medium | Phase 2 |
| Low | Rate evolution | Low | Low | High | Phase 1 (request NWN) |
| Low | DER adoption | Low | Medium | Medium | Phase 3 |
| Low | RNG adoption | Low | Low | Medium | Phase 3 |
| Low | Manufacturer data | Low | Low | High | Reference only |

---

## Conclusion

The model currently has a strong foundation with 13+ integrated data sources. The recommended additional sources would:

1. **Validate key assumptions** (electrification, efficiency, housing growth)
2. **Improve forecast accuracy** (calibration, scenario credibility)
3. **Enable advanced scenarios** (policy, technology, market variations)
4. **Support production deployment** (empirical grounding, regulatory credibility)

**For the capstone project**, focus on Phase 1 sources (8-12 hours effort, high impact).

**For production deployment**, integrate Phase 1 + Phase 2 sources (32-52 hours effort, comprehensive model).

**For advanced scenarios**, add Phase 3 sources (48-84 hours effort, full capability).
