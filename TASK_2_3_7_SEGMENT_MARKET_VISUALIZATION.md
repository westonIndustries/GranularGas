# Task 2.3.7 — Segment/Subsegment/Market Relationship Visualization with Equipment Profiles

## Overview

Enhanced verification task to create comprehensive visualizations showing how segment (RESSF, RESMF, MOBILE), subsegment, and market (geographic/district) relate to each other. Includes hierarchical diagrams, interactive OpenStreetMap visualization, detailed equipment profiles, appliance inventories, and age distributions per segment/subsegment/market combination.

## Task Details

## Task Details

### Location in Spec
- **File**: `.kiro/specs/nw-natural-end-use-forecasting/tasks.md`
- **Task ID**: 2.3.7
- **Status**: Not started ([ ])
- **Requirements**: 2.1, 2.2, 5.4, 13.1

### Implementation Location
- **Module**: `src/visualization.py`
- **Functions**: 
  - `visualize_segment_market_hierarchy()`
  - `generate_segment_profiles()`
- **Output Directory**: `output/segment_market_analysis/`

## Segment/Subsegment/Market Profiles

### Segment Profiles

#### RESSF (Single-Family Residential)
**Characteristics**:
- Largest segment (~80% of premises)
- Individual detached homes
- Typically larger conditioned area
- More diverse equipment types

**Typical Profile**:
- Average premise age: 35-45 years
- Space heating: Furnace (RFAU) or boiler (RBOL), avg efficiency 0.82-0.88
- Water heating: Tank water heater (RAWH), avg efficiency 0.55-0.65
- Cooking: Gas range (RRGE), avg efficiency 0.35-0.45
- Drying: Gas dryer (RDRY), avg efficiency 0.75-0.85
- Fireplace: Decorative fireplace (FRPL), avg efficiency 0.50-0.70
- Fuel mix: 95% gas, 5% electric
- Average efficiency: 0.65-0.75 across all end-uses

#### RESMF (Multi-Family Residential)
**Characteristics**:
- Medium segment (~15% of premises)
- Apartments, condos, townhomes
- Shared heating/cooling systems common
- More standardized equipment

**Typical Profile**:
- Average premise age: 40-50 years
- Space heating: Boiler (RBOL) or central furnace, avg efficiency 0.80-0.85
- Water heating: Shared tank or tankless (WTRB), avg efficiency 0.60-0.70
- Cooking: Gas range (RRGE), avg efficiency 0.35-0.45
- Drying: Shared laundry or individual gas dryer, avg efficiency 0.75-0.85
- Fireplace: Less common, avg efficiency 0.50-0.70
- Fuel mix: 98% gas, 2% electric
- Average efficiency: 0.68-0.78 across all end-uses

#### MOBILE (Mobile Home)
**Characteristics**:
- Smallest segment (~5% of premises)
- Manufactured housing
- Typically smaller conditioned area
- More standardized equipment

**Typical Profile**:
- Average premise age: 25-35 years
- Space heating: Furnace (RFAU), avg efficiency 0.75-0.82
- Water heating: Tank water heater (RAWH), avg efficiency 0.50-0.60
- Cooking: Gas range (RRGE), avg efficiency 0.35-0.45
- Drying: Gas dryer (RDRY), avg efficiency 0.75-0.85
- Fireplace: Rare, avg efficiency 0.50-0.70
- Fuel mix: 92% gas, 8% electric
- Average efficiency: 0.62-0.72 across all end-uses

### Subsegment Profiles (if available)

Subsegments may include:
- **By vintage era**: Pre-1950, 1950-1980, 1981-2010, 2011+
- **By size**: Small (<1500 sqft), Medium (1500-2500 sqft), Large (>2500 sqft)
- **By heating type**: Forced air, Hydronic, Electric
- **By location**: Urban, Suburban, Rural

Each subsegment inherits characteristics from parent segment but with specific variations in equipment age and efficiency.

### Market/District Profiles

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

## Deliverables

### 1. Hierarchical Relationship Diagrams

#### Treemap
- **Structure**: Segment → Subsegment → Market
- **Color-coding**: By segment type (RESSF, RESMF, MOBILE)
- **Size**: Proportional to premise count
- **Interactive**: Click to drill down through hierarchy
- **Output**: `segment_market_treemap.html`

#### Sunburst Chart
- **Structure**: Same hierarchy as treemap
- **Interactive**: Drill-down by clicking segments
- **Radial layout**: Easier to see proportions
- **Output**: `segment_market_sunburst.html`

#### Sankey Diagram
- **Flow**: Segment → Subsegment → Market
- **Width**: Proportional to premise count
- **Shows**: How premises flow through the hierarchy
- **Output**: `segment_market_sankey.html`

### 2. OpenStreetMap Visualization

#### Base Map
- **Coverage**: NW Natural service territory
- **Boundaries**: County boundaries displayed
- **Background**: OpenStreetMap tiles
- **Zoom/Pan**: Full interactive controls

#### Hexbin Aggregation
- **Cell Size**: 7.5 km hexagons
- **Grouping**: Premises aggregated into hexagonal cells
- **Color-coding**: By dominant segment type
  - Blue: RESSF (Single-Family Residential)
  - Red: RESMF (Multi-Family Residential)
  - Green: MOBILE (Mobile Home)
- **Opacity**: Intensity based on premise density
- **Popup**: Shows:
  - Segment breakdown (count and % for each type)
  - Subsegment distribution
  - Market/district information
  - Total premise count in hexbin

#### Layer Control
- **Toggle Views**:
  - Segment view (dominant segment type)
  - Subsegment view (if available)
  - Market/district view (geographic assignment)
- **Marker Overlay**: District centroids with segment composition pie charts

### 3. Summary Statistics Table

**Rows**: Segment × Subsegment × Market combinations
**Columns**:
- Premise count
- % of total
- Average equipment age
- Average efficiency
- Dominant end-use category

**Sorting**: By premise count (descending)
**Output**: `segment_market_summary_table.csv` and embedded in HTML

### 4. Comparison Charts

#### Stacked Bar Chart 1: Segment Distribution by Market/District
- **X-axis**: Market/District
- **Y-axis**: Premise count
- **Stacks**: RESSF, RESMF, MOBILE
- **Shows**: Geographic variation in segment mix
- **Output**: `segment_by_market_stacked_bar.png`

#### Stacked Bar Chart 2: Subsegment Distribution by Segment
- **X-axis**: Segment type
- **Y-axis**: Premise count
- **Stacks**: Subsegment categories
- **Shows**: Subsegment composition within each segment
- **Output**: `subsegment_by_segment_stacked_bar.png`

#### Heatmap: Segment × Market Cross-Tabulation
- **Rows**: Segment types (RESSF, RESMF, MOBILE)
- **Columns**: Market/District codes
- **Values**: Premise count
- **Color intensity**: Darker = higher count
- **Shows**: Concentration patterns across geography
- **Output**: `segment_market_heatmap.png`

### 5. Appliance Inventory Tables

#### Table 1: Equipment Count by Segment × End-Use
- **Rows**: Segment types (RESSF, RESMF, MOBILE)
- **Columns**: End-use categories (space_heating, water_heating, cooking, drying, fireplace, other)
- **Values**: Equipment count
- **Shows**: Equipment distribution across segments
- **Output**: `equipment_count_segment_enduse.csv`

#### Table 2: Equipment Count by Subsegment × End-Use (if available)
- **Rows**: Subsegment categories
- **Columns**: End-use categories
- **Values**: Equipment count
- **Shows**: Equipment variation within segments
- **Output**: `equipment_count_subsegment_enduse.csv`

#### Table 3: Equipment Count by Market/District × End-Use
- **Rows**: Market/District codes
- **Columns**: End-use categories
- **Values**: Equipment count
- **Shows**: Geographic variation in equipment
- **Output**: `equipment_count_market_enduse.csv`

#### Table 4: Top 10 Equipment Types by Count
- **Columns**: Equipment type code, Equipment class, End-use, Count, % of total, Avg age, Avg efficiency
- **Rows**: Top 10 equipment types (sorted by count descending)
- **Breakdown**: For each equipment type, show distribution across segments/subsegments/markets
- **Output**: `top_equipment_types.csv`

#### Table 5: Equipment Age Distribution by Segment
- **Rows**: Age bins (0-5 years, 5-10 years, 10-15 years, 15-20 years, 20+ years)
- **Columns**: Segment types (RESSF, RESMF, MOBILE)
- **Values**: Equipment count in each age bin
- **Shows**: Age distribution patterns by segment
- **Output**: `equipment_age_distribution_segment.csv`

### 6. Segment/Subsegment/Market Profile Report

#### Executive Summary
- Total premises by segment/subsegment/market
- Average premise age
- Average equipment age by end-use
- Average efficiency by end-use
- Fuel type mix (% gas vs electric)
- Key statistics and trends

#### Detailed Profiles (for each combination)
- **Premise Statistics**:
  - Count and % of total
  - Average premise age (construction year)
  - Vintage era distribution
  
- **Equipment Inventory**:
  - Equipment count by end-use (count and %)
  - Top 5 equipment types with counts
  - Fuel type mix (% gas vs electric)
  
- **Equipment Age**:
  - Average equipment age by end-use (with min/max range)
  - Age distribution histogram
  - Oldest and newest equipment types
  
- **Equipment Efficiency**:
  - Average efficiency by end-use
  - Efficiency distribution (% in each tier: low/medium/high)
  - Comparison to system average
  
- **Building Characteristics**:
  - Dominant vintage era
  - Size proxy (if available)
  - Heating system type distribution
  
- **Comparative Analysis**:
  - Comparison to parent segment
  - Comparison to system average
  - Comparison to other markets

#### Visualizations Embedded
- All charts and maps embedded in HTML report
- Interactive drill-down capabilities
- Export options for data and charts

## Test Validation

The test `test_segment_market_visualization()` verifies:

1. **Map Rendering**: Map renders without errors
2. **Hexbin Data**: Hexbins contain expected data
   - All hexbins have premise counts > 0
   - Segment breakdown sums to total premise count
   - Percentages sum to 100%
3. **Popups**: Popup content displays correctly
   - All required fields present
   - Numbers formatted correctly
   - No missing data
4. **Layer Controls**: Layer toggle functionality works
   - All layers can be toggled on/off
   - Map updates when layers change
5. **Hierarchical Diagrams**: All three diagrams render
   - Treemap, sunburst, and Sankey all present
   - Interactive drill-down works
   - Proportions correct
6. **Summary Table**: Statistics table accurate
   - Row counts match data
   - Percentages sum to 100%
   - Averages calculated correctly
7. **Comparison Charts**: All charts render
   - Stacked bars show correct proportions
   - Heatmap color scale appropriate
   - No missing segments or markets
8. **Unaggregated Data Export**: Data files complete and accurate
   - CSV file exists and is readable
   - Parquet file exists and is readable
   - Row count matches total premises
   - All required columns present
   - No null values in key columns (blinded_id, segment, market)
   - Data sorted correctly by segment, subsegment, market, blinded_id
   - Latitude/longitude values are valid (within service territory bounds)

## Data Requirements

### Input Data
- **Premise-equipment table** with columns:
  - `blinded_id`: Unique premise identifier
  - `segment`: RESSF, RESMF, or MOBILE
  - `subsegment`: (if available in data)
  - `market` or `district_code_IRP`: Geographic market assignment
  - `equipment_age`: For average calculation
  - `efficiency`: For average calculation
  - `end_use`: For dominant end-use determination

### Geographic Data
- **County boundaries**: GeoJSON or shapefile for service territory
- **District boundaries**: (if available)
- **Premise coordinates**: Latitude/longitude for hexbin aggregation

## Output Files

### Visualizations
```
output/segment_market_analysis/
├── segment_market_treemap.html          # Interactive treemap
├── segment_market_sunburst.html         # Interactive sunburst
├── segment_market_sankey.html           # Interactive Sankey diagram
├── segment_market_openstreetmap.html    # Interactive OSM map with hexbins
├── segment_market_summary_table.csv     # Aggregated statistics table
├── segment_by_market_stacked_bar.png    # Stacked bar chart
├── subsegment_by_segment_stacked_bar.png # Stacked bar chart
├── segment_market_heatmap.png           # Heatmap
└── segment_market_analysis_report.html  # Combined report with all visualizations
```

### Unaggregated Data Exports
```
output/segment_market_analysis/
├── segment_market_unaggregated_data.csv      # Premise-level data (CSV format)
└── segment_market_unaggregated_data.parquet  # Premise-level data (Parquet format)
```

**Unaggregated Data Columns**:
- `blinded_id`: Unique premise identifier
- `segment`: RESSF, RESMF, or MOBILE
- `subsegment`: Subsegment category (if available)
- `market`: Market identifier
- `district_code_IRP`: District code
- `latitude`: Premise latitude
- `longitude`: Premise longitude
- `equipment_age`: Average equipment age
- `efficiency`: Average equipment efficiency
- `end_use`: Dominant end-use category
- `premise_count_in_segment_market_combo`: Count of premises in this segment/subsegment/market combination
- `equipment_type_code`: Primary equipment type code

**Sorting**: By segment, subsegment, market, blinded_id

**Purpose**: Enables custom analysis, filtering, and drill-down by users without needing to re-run the aggregation

## Implementation Notes

### Dependencies
- `folium`: For OpenStreetMap visualization
- `plotly`: For interactive treemap, sunburst, Sankey
- `h3`: For hexbin aggregation (or `geopandas` with hexbin)
- `pandas`: For data aggregation
- `matplotlib`/`seaborn`: For static charts

### Key Functions to Implement
1. `aggregate_by_segment_market()` — Group premises by segment/subsegment/market
2. `create_hexbin_layer()` — Generate hexagonal aggregation
3. `create_treemap()` — Generate interactive treemap
4. `create_sunburst()` — Generate interactive sunburst
5. `create_sankey()` — Generate interactive Sankey diagram
6. `create_osm_map()` — Generate OpenStreetMap with hexbins and layers
7. `create_comparison_charts()` — Generate stacked bars and heatmap
8. `generate_summary_table()` — Compute statistics by segment/subsegment/market

### Performance Considerations
- Hexbin aggregation reduces data points for faster rendering
- Layer control allows users to toggle expensive layers
- Summary table pre-computed and cached
- Charts generated once and saved as PNG/HTML
- Unaggregated data exported in both CSV (human-readable) and Parquet (efficient storage/querying)

## Unaggregated Data Export

### Purpose
Export all premise-level data without aggregation to enable:
- Custom filtering and analysis by users
- Drill-down from aggregated visualizations to individual premises
- Integration with external tools and databases
- Reproducibility and transparency of aggregation process

### File Formats

#### CSV Format (`segment_market_unaggregated_data.csv`)
- **Advantages**: Human-readable, compatible with Excel/Sheets, easy to share
- **Disadvantages**: Larger file size, slower to query
- **Use case**: Manual analysis, sharing with non-technical stakeholders

#### Parquet Format (`segment_market_unaggregated_data.parquet`)
- **Advantages**: Compressed, fast to query, efficient storage, supports complex data types
- **Disadvantages**: Requires specialized tools to read
- **Use case**: Data science workflows, large-scale analysis, integration with Python/R

### Data Schema

| Column | Type | Description |
|--------|------|-------------|
| `blinded_id` | string | Unique premise identifier (anonymized) |
| `segment` | string | RESSF, RESMF, or MOBILE |
| `subsegment` | string | Subsegment category (if available in source data) |
| `market` | string | Market identifier |
| `district_code_IRP` | string | NW Natural district code |
| `latitude` | float | Premise latitude (approximate, for mapping) |
| `longitude` | float | Premise longitude (approximate, for mapping) |
| `equipment_age` | float | Average age of equipment (years) |
| `efficiency` | float | Average equipment efficiency (0-1 or >1 for heat pumps) |
| `end_use` | string | Dominant end-use category |
| `premise_count_in_segment_market_combo` | int | Count of premises in this segment/subsegment/market combination |
| `equipment_type_code` | string | Primary equipment type code |

### Sorting
- Primary: `segment` (RESSF, RESMF, MOBILE)
- Secondary: `subsegment` (if available)
- Tertiary: `market` / `district_code_IRP`
- Quaternary: `blinded_id`

### Row Count
- Equals total number of unique premises in premise-equipment table
- One row per premise (not per equipment unit)

### Data Quality Checks
- No duplicate `blinded_id` values
- All `segment` values are valid (RESSF, RESMF, MOBILE)
- All `market` values are non-null
- All `latitude`/`longitude` values are within service territory bounds
- All `efficiency` values are positive
- All `equipment_age` values are non-negative

## Next Steps

1. Implement `visualize_segment_market_hierarchy()` in `src/visualization.py`
2. Create test file `tests/test_segment_market_visualization.py`
3. Run test to verify all outputs are generated correctly
4. Review visualizations for accuracy and usability
5. Integrate into checkpoint 3 verification pipeline

## Related Tasks

- **Task 2.1**: Data ingestion (provides premise-equipment table)
- **Task 2.2**: Join function (provides segment/market data)
- **Task 3.4**: Service territory geographic coverage map (related geographic visualization)
- **Task 15.1**: Visualization module (geographic aggregation functions)


### 5. Appliance Inventory Tables

#### Table 1: Equipment Count by Segment × End-Use
- **Rows**: Segment types (RESSF, RESMF, MOBILE)
- **Columns**: End-use categories (space_heating, water_heating, cooking, drying, fireplace, other)
- **Values**: Equipment count
- **Shows**: Equipment distribution across segments
- **Output**: `equipment_count_segment_enduse.csv`

#### Table 2: Equipment Count by Subsegment × End-Use (if available)
- **Rows**: Subsegment categories
- **Columns**: End-use categories
- **Values**: Equipment count
- **Shows**: Equipment variation within segments
- **Output**: `equipment_count_subsegment_enduse.csv`

#### Table 3: Equipment Count by Market/District × End-Use
- **Rows**: Market/District codes
- **Columns**: End-use categories
- **Values**: Equipment count
- **Shows**: Geographic variation in equipment
- **Output**: `equipment_count_market_enduse.csv`

#### Table 4: Top 10 Equipment Types by Count
- **Columns**: Equipment type code, Equipment class, End-use, Count, % of total, Avg age, Avg efficiency
- **Rows**: Top 10 equipment types (sorted by count descending)
- **Breakdown**: For each equipment type, show distribution across segments/subsegments/markets
- **Output**: `top_equipment_types.csv`

#### Table 5: Equipment Age Distribution by Segment
- **Rows**: Age bins (0-5 years, 5-10 years, 10-15 years, 15-20 years, 20+ years)
- **Columns**: Segment types (RESSF, RESMF, MOBILE)
- **Values**: Equipment count in each age bin
- **Shows**: Age distribution patterns by segment
- **Output**: `equipment_age_distribution_segment.csv`

### 6. Additional Comparison Charts

#### Box Plot: Equipment Age Distribution by Segment
- **X-axis**: Segment types
- **Y-axis**: Equipment age (years)
- **Shows**: Median, quartiles, outliers for each segment
- **Output**: `equipment_age_boxplot_segment.png`

#### Box Plot: Equipment Age Distribution by End-Use
- **X-axis**: End-use categories
- **Y-axis**: Equipment age (years)
- **Shows**: Age variation across end-uses
- **Output**: `equipment_age_boxplot_enduse.png`

#### Violin Plot: Equipment Efficiency Distribution
- **X-axis**: Segment and end-use combinations
- **Y-axis**: Equipment efficiency (0-1 or >1 for heat pumps)
- **Shows**: Full distribution of efficiency values
- **Output**: `efficiency_violin_plot.png`

#### Scatter Plot: Equipment Age vs Efficiency
- **X-axis**: Average equipment age
- **Y-axis**: Average efficiency
- **Points**: Each segment/subsegment/market combination
- **Color**: By segment type
- **Size**: By premise count
- **Shows**: Relationship between age and efficiency
- **Output**: `age_vs_efficiency_scatter.png`

### 7. Segment/Subsegment/Market Profile Report

#### Executive Summary
- Total premises by segment/subsegment/market
- Average premise age
- Average equipment age by end-use
- Average efficiency by end-use
- Fuel type mix (% gas vs electric)
- Key statistics and trends

#### Detailed Profiles (for each combination)
- **Premise Statistics**:
  - Count and % of total
  - Average premise age (construction year)
  - Vintage era distribution
  
- **Equipment Inventory**:
  - Equipment count by end-use (count and %)
  - Top 5 equipment types with counts
  - Fuel type mix (% gas vs electric)
  
- **Equipment Age**:
  - Average equipment age by end-use (with min/max range)
  - Age distribution histogram
  - Oldest and newest equipment types
  
- **Equipment Efficiency**:
  - Average efficiency by end-use
  - Efficiency distribution (% in each tier: low/medium/high)
  - Comparison to system average
  
- **Building Characteristics**:
  - Dominant vintage era
  - Size proxy (if available)
  - Heating system type distribution
  
- **Comparative Analysis**:
  - Comparison to parent segment
  - Comparison to system average
  - Comparison to other markets

#### Visualizations Embedded
- All charts and maps embedded in HTML report
- Interactive drill-down capabilities
- Export options for data and charts

## Output Files

### Visualizations
```
output/segment_market_analysis/
├── segment_market_treemap.html          # Interactive treemap
├── segment_market_sunburst.html         # Interactive sunburst
├── segment_market_sankey.html           # Interactive Sankey diagram
├── segment_market_openstreetmap.html    # Interactive OSM map with hexbins
├── segment_by_market_stacked_bar.png    # Stacked bar chart
├── subsegment_by_segment_stacked_bar.png # Stacked bar chart
├── segment_market_heatmap.png           # Heatmap
├── equipment_age_boxplot_segment.png    # Equipment age by segment
├── equipment_age_boxplot_enduse.png     # Equipment age by end-use
├── efficiency_violin_plot.png           # Efficiency distribution
├── age_vs_efficiency_scatter.png        # Age vs efficiency scatter
└── segment_market_analysis_report.html  # Combined report with all visualizations
```

### Appliance Inventory Tables
```
output/segment_market_analysis/
├── equipment_count_segment_enduse.csv       # Equipment by segment × end-use
├── equipment_count_subsegment_enduse.csv    # Equipment by subsegment × end-use (if available)
├── equipment_count_market_enduse.csv        # Equipment by market × end-use
├── top_equipment_types.csv                  # Top 10 equipment types
└── equipment_age_distribution_segment.csv   # Equipment age distribution
```

### Aggregated Statistics
```
output/segment_market_analysis/
├── segment_market_summary_table.csv     # Aggregated statistics table
└── segment_profiles_report.html         # Detailed segment/subsegment/market profiles
```

### Unaggregated Data Exports
```
output/segment_market_analysis/
├── segment_market_unaggregated_data.csv      # Premise-level data (CSV format)
└── segment_market_unaggregated_data.parquet  # Premise-level data (Parquet format)
```
