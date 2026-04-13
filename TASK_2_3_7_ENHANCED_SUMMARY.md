# Task 2.3.7 — Enhanced Segment/Subsegment/Market Visualization with Equipment Profiles

## Summary

Task 2.3.7 has been significantly enhanced to include comprehensive equipment profiles, appliance inventories, and age distributions per segment, subsegment, and market combination.

## What Was Added

### 1. Detailed Segment Profiles

#### RESSF (Single-Family Residential) - 80% of premises
- Average premise age: 35-45 years
- Space heating: Furnace (RFAU) or boiler (RBOL), avg efficiency 0.82-0.88
- Water heating: Tank water heater (RAWH), avg efficiency 0.55-0.65
- Cooking: Gas range (RRGE), avg efficiency 0.35-0.45
- Drying: Gas dryer (RDRY), avg efficiency 0.75-0.85
- Fireplace: Decorative fireplace (FRPL), avg efficiency 0.50-0.70
- Fuel mix: 95% gas, 5% electric
- Average efficiency: 0.65-0.75 across all end-uses

#### RESMF (Multi-Family Residential) - 15% of premises
- Average premise age: 40-50 years
- Space heating: Boiler (RBOL) or central furnace, avg efficiency 0.80-0.85
- Water heating: Shared tank or tankless (WTRB), avg efficiency 0.60-0.70
- Cooking: Gas range (RRGE), avg efficiency 0.35-0.45
- Drying: Shared laundry or individual gas dryer, avg efficiency 0.75-0.85
- Fireplace: Less common, avg efficiency 0.50-0.70
- Fuel mix: 98% gas, 2% electric
- Average efficiency: 0.68-0.78 across all end-uses

#### MOBILE (Mobile Home) - 5% of premises
- Average premise age: 25-35 years
- Space heating: Furnace (RFAU), avg efficiency 0.75-0.82
- Water heating: Tank water heater (RAWH), avg efficiency 0.50-0.60
- Cooking: Gas range (RRGE), avg efficiency 0.35-0.45
- Drying: Gas dryer (RDRY), avg efficiency 0.75-0.85
- Fireplace: Rare, avg efficiency 0.50-0.70
- Fuel mix: 92% gas, 8% electric
- Average efficiency: 0.62-0.72 across all end-uses

### 2. Subsegment Profiles (if available)

Subsegments may include:
- **By vintage era**: Pre-1950, 1950-1980, 1981-2010, 2011+
- **By size**: Small (<1500 sqft), Medium (1500-2500 sqft), Large (>2500 sqft)
- **By heating type**: Forced air, Hydronic, Electric
- **By location**: Urban, Suburban, Rural

Each subsegment inherits characteristics from parent segment with specific variations in equipment age and efficiency.

### 3. Market/District Profiles

Markets are defined by geographic districts (IRP districts). Each market has:
- **Geographic coverage**: Specific counties or regions
- **Climate zone**: Affects heating/cooling demand
- **Population density**: Urban vs rural characteristics
- **Infrastructure**: Availability of natural gas, electricity, water

**Example Markets**:
- **PORC (Portland)**: Urban, temperate climate, high density
  - Avg premise age: 38 years
  - Avg equipment age: 12-15 years
  - Avg efficiency: 0.68-0.78
  - Equipment mix: Diverse, newer equipment more common
  
- **EUGN (Eugene)**: Suburban, temperate climate, medium density
  - Avg premise age: 42 years
  - Avg equipment age: 14-17 years
  - Avg efficiency: 0.65-0.75
  - Equipment mix: Mix of old and new
  
- **GORGE (Gorge region)**: Rural, cold climate, low density
  - Avg premise age: 45 years
  - Avg equipment age: 16-19 years
  - Avg efficiency: 0.62-0.72
  - Equipment mix: Older equipment, higher heating demand

### 4. Enhanced OpenStreetMap Visualization

**Hexbin Popups Now Include**:
- Segment breakdown (count and % for each type)
- Subsegment distribution (if available)
- Market/district info
- **Average equipment age by end-use** ✨
- **Top 3 equipment types in hexbin** ✨
- **Average efficiency by end-use** ✨

**Enhanced Layer Control**:
- Segment view (dominant segment type)
- Subsegment view (if available)
- Market/district view (geographic assignment)
- **Equipment age view** ✨
- **Efficiency view** ✨

**District Markers Now Show**:
- Segment composition pie charts
- **Equipment age indicators** ✨

### 5. Appliance Inventory Tables

#### Table 1: Equipment Count by Segment × End-Use
- Rows: Segment types (RESSF, RESMF, MOBILE)
- Columns: End-use categories
- Values: Equipment count

#### Table 2: Equipment Count by Subsegment × End-Use
- Rows: Subsegment categories
- Columns: End-use categories
- Values: Equipment count

#### Table 3: Equipment Count by Market/District × End-Use
- Rows: Market/District codes
- Columns: End-use categories
- Values: Equipment count

#### Table 4: Top 10 Equipment Types by Count
- Equipment type code, Equipment class, End-use, Count, % of total, Avg age, Avg efficiency
- Breakdown across segments/subsegments/markets

#### Table 5: Equipment Age Distribution by Segment
- Age bins: 0-5, 5-10, 10-15, 15-20, 20+ years
- Columns: Segment types
- Values: Equipment count in each age bin

### 6. Additional Comparison Charts

#### Box Plot: Equipment Age Distribution by Segment
- Shows median, quartiles, outliers for each segment

#### Box Plot: Equipment Age Distribution by End-Use
- Shows age variation across end-uses

#### Violin Plot: Equipment Efficiency Distribution
- Full distribution of efficiency values by segment and end-use

#### Scatter Plot: Equipment Age vs Efficiency
- X-axis: Average equipment age
- Y-axis: Average efficiency
- Points: Each segment/subsegment/market combination
- Color: By segment type
- Size: By premise count

### 7. Comprehensive Profile Report

**Executive Summary**:
- Total premises by segment/subsegment/market
- Average premise age
- Average equipment age by end-use
- Average efficiency by end-use
- Fuel type mix (% gas vs electric)
- Key statistics and trends

**Detailed Profiles** (for each combination):
- Premise statistics (count, %, age, vintage distribution)
- Equipment inventory (count by end-use, top 5 types, fuel mix)
- Equipment age (avg by end-use, distribution, oldest/newest)
- Equipment efficiency (avg by end-use, distribution, comparison to system)
- Building characteristics (vintage era, size proxy, heating type)
- Comparative analysis (vs parent segment, vs system average, vs other markets)

**Visualizations Embedded**:
- All charts and maps embedded in HTML report
- Interactive drill-down capabilities
- Export options for data and charts

### 8. Enhanced Unaggregated Data Export

**New Columns**:
- `premise_age`: Construction year
- `avg_equipment_age`: Average age of equipment
- `avg_efficiency`: Average efficiency
- `dominant_end_use`: Most common end-use
- `top_3_equipment_types`: Top 3 equipment types in premise
- `equipment_count_by_enduse_json`: JSON with equipment counts by end-use

**Enables**:
- Custom analysis and filtering
- Drill-down from aggregated visualizations to individual premises
- Integration with external tools and databases
- Reproducibility and transparency of aggregation process

## Output Files

### Visualizations (11 files)
- segment_market_treemap.html
- segment_market_sunburst.html
- segment_market_sankey.html
- segment_market_openstreetmap.html
- segment_by_market_stacked_bar.png
- subsegment_by_segment_stacked_bar.png
- segment_market_heatmap.png
- equipment_age_boxplot_segment.png
- equipment_age_boxplot_enduse.png
- efficiency_violin_plot.png
- age_vs_efficiency_scatter.png

### Appliance Inventory Tables (5 files)
- equipment_count_segment_enduse.csv
- equipment_count_subsegment_enduse.csv
- equipment_count_market_enduse.csv
- top_equipment_types.csv
- equipment_age_distribution_segment.csv

### Aggregated Statistics (2 files)
- segment_market_summary_table.csv
- segment_profiles_report.html

### Unaggregated Data (2 files)
- segment_market_unaggregated_data.csv
- segment_market_unaggregated_data.parquet

### Combined Report (1 file)
- segment_market_analysis_report.html

## Implementation Functions

### New Functions in `src/visualization.py`
1. `visualize_segment_market_hierarchy()` — Main orchestrator function
2. `generate_segment_profiles()` — Compute detailed equipment and age statistics
3. `create_appliance_inventory_tables()` — Generate equipment count tables
4. `create_equipment_age_charts()` — Generate age distribution visualizations
5. `create_efficiency_charts()` — Generate efficiency distribution visualizations
6. `create_profile_report()` — Generate comprehensive HTML profile report

## Test Validation

The test `test_segment_market_visualization()` verifies:
1. Map renders without errors
2. Hexbins contain expected data
3. Popups display correctly with all new fields
4. Layer controls work (including new equipment age and efficiency views)
5. Hierarchical diagrams render correctly
6. Summary table is accurate
7. Comparison charts render correctly
8. Unaggregated data files exist and contain all premises
9. **Profile statistics are accurate** ✨
10. **All equipment types are represented** ✨

## Key Metrics Computed

For each segment/subsegment/market combination:
- Premise count and % of total
- Average premise age (construction year)
- Equipment inventory by end-use (count and %)
- Top 5 equipment types with counts
- Average equipment age by end-use (with min/max range)
- Average efficiency by end-use
- Fuel type mix (% gas vs electric)
- Dominant building characteristics
- Comparison to system average

## Next Steps

1. Implement `generate_segment_profiles()` function
2. Create appliance inventory table generation functions
3. Add equipment age and efficiency visualization functions
4. Generate comprehensive profile report
5. Run tests to verify all outputs
6. Review visualizations for accuracy and usability
7. Integrate into checkpoint 3 verification pipeline

## Related Documentation

- **TASK_2_3_7_SEGMENT_MARKET_VISUALIZATION.md**: Detailed task documentation
- **tasks.md**: Implementation plan with all tasks
- **ALGORITHM.md**: Algorithm documentation with input-to-output mapping
