# ALGORITHM.md Diagrams Update

## Summary of Changes

Updated `ALGORITHM.md` with improved and new mermaid diagrams to better visualize the algorithm flow and data pipeline.

## Changes Made

### 1. Fixed High-Level Algorithm Flow Diagram
**Location**: Section "High-Level Algorithm Flow"

**Improvements**:
- Fixed the loop logic: Changed from `M -->|Yes| G` to `M -->|Yes| N` then `N --> G`
- Added explicit "Year = Year + 1" step for clarity
- Improved node labels and flow clarity
- Better color coding for different stages

**Before**:
```
M -->|Yes| G  (incorrect - would loop back without incrementing year)
```

**After**:
```
M -->|Yes| N["Year = Year + 1"]
N --> G  (correct - increments year before looping)
```

### 2. New Input-to-Output Mapping Diagram
**Location**: New section "Input-to-Output Mapping" (after High-Level Algorithm Flow)

**Purpose**: Visualize how input data sources flow through the processing pipeline to produce outputs

**Structure**:
- **Left side (📥 INPUT DATA SOURCES)**: 9 major input data sources
  - NW Natural Premise Data
  - Equipment Inventory
  - Billing Data & Rates
  - Weather Data (HDD/CDD)
  - RBSA Building Stock
  - ASHRAE Service Life
  - Census ACS Housing
  - NOAA Climate Normals
  - RECS Microdata Benchmarks

- **Middle (⚙️ PROCESSING PIPELINE)**: 7 processing steps
  - Data Ingestion & Cleaning
  - Housing Stock Construction
  - Equipment Inventory
  - Replacement Simulation
  - End-Use Simulation
  - Aggregation & Rollup
  - Validation & Calibration

- **Right side (📤 OUTPUT RESULTS)**: 8 output deliverables
  - Premise-Level Consumption
  - End-Use Breakdown
  - Segment Analysis
  - District Analysis
  - UPC Projections vs IRP
  - Calibration Metrics
  - Scenario Comparison
  - Segment/Market Visualization

**Data Flow**:
- All 9 inputs feed into Data Ingestion & Cleaning
- Ingestion splits into Housing Stock and Equipment Inventory paths
- Both paths converge at Replacement Simulation
- Replacement Simulation feeds into End-Use Simulation (with weather data)
- End-Use Simulation → Aggregation → Validation
- Validation uses billing data for calibration
- All processing steps produce corresponding outputs

### 3. Fixed Detailed Simulation Flow Diagram
**Location**: Section "Detailed Simulation Flow Diagram"

**Improvements**:
- Reorganized to show all end-use paths converging to a single "Sum All End-Uses" node
- Cleaner flow with all paths leading to final "Premise Total Annual Therms"
- Better visual hierarchy

**Before**: Multiple disconnected paths
**After**: All paths converge at H["Sum All End-Uses"] then to I["Premise Total Annual Therms"]

### 4. Fixed Scenario Projection Loop Diagram
**Location**: Section "Scenario Projection Loop"

**Improvements**:
- Corrected loop logic similar to High-Level Algorithm Flow
- Added explicit year increment step
- Clearer conditional logic

**Before**:
```
H -->|Yes| I["Year = Year + 1"]
I --> B  (but no explicit loop back)
```

**After**:
```
H -->|Yes| I["Year = Year + 1"]
I --> B  (explicit loop back to Project Housing Stock)
```

## Diagram Features

### Color Coding
- **Blue (#e3f2fd)**: Start/Input nodes
- **Orange (#fff3e0)**: Processing/Transformation nodes
- **Green (#e8f5e9)**: Aggregation/Summary nodes
- **Purple (#f3e5f5)**: Output/Result nodes
- **Light Green (#c8e6c9)**: End/Success nodes

### Visual Elements
- **Subgraphs**: Used in Input-to-Output Mapping to group related items
- **Emojis**: Used in subgraph labels for quick visual identification
- **Decision Diamonds**: Used for conditional logic (e.g., "More Years?")
- **Descriptive Labels**: All nodes include clear, descriptive text

## Benefits

1. **Clarity**: Diagrams now clearly show the complete data flow from inputs to outputs
2. **Correctness**: Fixed loop logic ensures proper year iteration
3. **Completeness**: New diagram shows all 9 inputs and 8 outputs
4. **Traceability**: Easy to trace how specific inputs contribute to specific outputs
5. **Documentation**: Serves as visual documentation of the algorithm architecture

## Related Files

- **ALGORITHM.md**: Main algorithm documentation with updated diagrams
- **TASK_2_3_7_SEGMENT_MARKET_VISUALIZATION.md**: Documents the segment/market visualization output
- **tasks.md**: Implementation plan with all tasks

## Next Steps

1. Review diagrams for accuracy and clarity
2. Use diagrams in presentations and documentation
3. Reference diagrams when explaining algorithm to stakeholders
4. Update diagrams if algorithm logic changes
