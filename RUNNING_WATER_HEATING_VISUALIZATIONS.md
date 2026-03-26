# Running Water Heating Visualizations - Task 6.3

## Quick Start

To generate all water heating analysis visualizations:

```bash
# Run the visualization test suite
pytest tests/test_water_heating_delta_visualizations.py -v

# Or run a specific visualization test
pytest tests/test_water_heating_delta_visualizations.py::TestWaterHeatingDeltaProperty::test_generate_delta_t_choropleth_map -v
```

## Output Location

All visualizations are saved to: `output/water_heating_analysis/`

## Generated Files

### Interactive Maps (HTML)
- **delta_t_choropleth_map.html** — District-level delta-T intensity map
- **seasonal_variation_map.html** — Winter vs. summer delta-T comparison
- **station_delta_t_map.html** — Weather station delta-T markers

### Delta-T Analysis (PNG images)
- **daily_delta_t.png** — Daily delta-T patterns (2008-2025)
- **seasonal_delta_t.png** — Seasonal delta-T with confidence bands
- **water_air_temp_scatter.png** — Water vs. air temperature correlation
- **monthly_delta_t_heatmap.png** — Monthly delta-T by station
- **annual_delta_t_boxplot.png** — Annual delta-T distribution (2015-2025)
- **monthly_delta_t_violin.png** — Daily delta-T distribution by month

### Water Heating Demand (PNG images)
- **wh_demand_by_station.png** — Annual WH therms per customer
- **wh_demand_comparison.png** — Baseline vs. high-efficiency scenario
- **monthly_wh_demand_pattern.png** — Seasonal WH demand pattern

## Individual Visualization Tests

Run specific visualizations:

```bash
# Delta-T analysis graphs
pytest tests/test_water_heating_delta_visualizations.py::TestWaterHeatingDeltaProperty::test_generate_daily_delta_graph -v
pytest tests/test_water_heating_delta_visualizations.py::TestWaterHeatingDeltaProperty::test_generate_seasonal_delta_graph -v
pytest tests/test_water_heating_delta_visualizations.py::TestWaterHeatingDeltaProperty::test_generate_water_air_temp_scatter -v
pytest tests/test_water_heating_delta_visualizations.py::TestWaterHeatingDeltaProperty::test_generate_monthly_delta_heatmap -v
pytest tests/test_water_heating_delta_visualizations.py::TestWaterHeatingDeltaProperty::test_generate_annual_delta_boxplot -v
pytest tests/test_water_heating_delta_visualizations.py::TestWaterHeatingDeltaProperty::test_generate_monthly_delta_violin_plot -v

# Water heating demand maps
pytest tests/test_water_heating_delta_visualizations.py::TestWaterHeatingDeltaProperty::test_generate_delta_t_choropleth_map -v
pytest tests/test_water_heating_delta_visualizations.py::TestWaterHeatingDeltaProperty::test_generate_seasonal_variation_map -v
pytest tests/test_water_heating_delta_visualizations.py::TestWaterHeatingDeltaProperty::test_generate_station_delta_t_marker_map -v

# Water heating demand graphs
pytest tests/test_water_heating_delta_visualizations.py::TestWaterHeatingDeltaProperty::test_generate_wh_demand_by_station -v
pytest tests/test_water_heating_delta_visualizations.py::TestWaterHeatingDeltaProperty::test_generate_wh_demand_comparison -v
pytest tests/test_water_heating_delta_visualizations.py::TestWaterHeatingDeltaProperty::test_generate_monthly_wh_demand_pattern -v
```

## Viewing the Interactive Maps

After running the tests, open the maps in your browser:

```bash
# On macOS
open output/water_heating_analysis/delta_t_choropleth_map.html
open output/water_heating_analysis/seasonal_variation_map.html
open output/water_heating_analysis/station_delta_t_map.html

# On Linux
xdg-open output/water_heating_analysis/delta_t_choropleth_map.html
xdg-open output/water_heating_analysis/seasonal_variation_map.html
xdg-open output/water_heating_analysis/station_delta_t_map.html

# On Windows
start output/water_heating_analysis/delta_t_choropleth_map.html
start output/water_heating_analysis/seasonal_variation_map.html
start output/water_heating_analysis/station_delta_t_map.html
```

## Understanding the Visualizations

### Delta-T Choropleth Map
- **Blue markers** = Low delta-T (64-66°F) — Less water heating needed
- **Orange markers** = Medium delta-T (67°F) — Moderate water heating
- **Red markers** = High delta-T (68°F) — More water heating needed
- Popup shows estimated annual WH demand in therms/customer
- Zoom and pan to explore specific districts

### Seasonal Variation Map
- **Purple markers** = Districts with seasonal variation
- Popup shows winter delta-T, summer delta-T, and winter/summer ratio
- Higher ratio = More seasonal variation
- Useful for understanding peak demand periods

### Station Delta-T Marker Map
- **Red markers** = High delta-T (≥68°F)
- **Orange markers** = Med-high delta-T (67°F)
- **Yellow markers** = Medium delta-T (66°F)
- **Blue markers** = Low delta-T (<66°F)
- Popup shows estimated annual WH demand per customer

### Daily Delta-T Graph
- **Blue lines** = Individual years (2008-2025) with transparency
- **Red line** = Average daily delta-T by day of year
- Shows seasonal pattern: higher in winter, lower in summer
- Used to validate water heating demand assumptions

### Seasonal Delta-T Graph
- **Blue shaded area** = Min-max range by month
- **Red line with markers** = Average monthly delta-T
- Shows coldest months (winter) and warmest months (summer)
- Used for monthly demand forecasting

### Water-Air Temperature Scatter
- **Blue dots** = Daily observations
- **Red line** = Linear regression fit
- **R² value** = Strength of correlation
- Shows how water temperature correlates with air temperature

### Monthly Delta-T Heatmap
- **Rows** = Weather stations (11 total)
- **Columns** = Months (Jan-Dec)
- **Color intensity** = Delta-T magnitude (blue=low, red=high)
- Identifies which stations have highest water heating demand

### Annual Delta-T Box Plot
- **Box** = Interquartile range (middle 50% of years)
- **Line in box** = Median year
- **Whiskers** = Min/max years
- **Dots** = Outlier years
- Shows year-to-year variability in water heating demand

### Monthly Delta-T Violin Plot
- **Violin shape** = Full distribution of daily delta-T values
- **Wider sections** = More common values
- **Narrower sections** = Less common values
- Shows seasonal variation in demand distribution

### WH Demand by Station
- **Bar height** = Estimated annual therms per customer
- **Based on** = Delta-T × 0.8 (accounting for efficiency)
- **Assumption** = 64 gallons/day hot water usage
- Identifies stations with highest water heating demand

### WH Demand Comparison
- **Blue bars** = Baseline scenario (current efficiency)
- **Green bars** = High-efficiency scenario (25% more efficient)
- **Difference** = Potential demand reduction from efficiency improvements
- Shows impact of equipment upgrades on demand

### Monthly WH Demand Pattern
- **Line graph** = Monthly demand variation
- **Shaded area** = Demand magnitude
- **Peak months** = Winter (Jan, Feb, Nov, Dec)
- **Low months** = Summer (Jun, Jul, Aug)
- Used for seasonal load forecasting

## Customizing Visualizations

To modify visualizations, edit `tests/test_water_heating_delta_visualizations.py`:

### Change color schemes
```python
# In heatmap tests, modify cmap parameter:
sns.heatmap(df_delta, cmap='RdYlBu_r')  # Different color scheme
```

### Change figure size
```python
# In any test, modify figsize:
fig, ax = plt.subplots(figsize=(16, 8))  # Larger figure
```

### Change district/station data
```python
# In map tests, modify districts/stations dict:
districts = {
    'MULT': {'lat': 45.5, 'lon': -122.7, 'delta_t': 68, 'name': 'Multnomah'},
    # Add or modify districts
}
```

### Change demand assumptions
```python
# In WH demand tests, modify calculation:
wh_demand = [dt * 0.75 for dt in delta_t_values]  # Different efficiency factor
```

## Troubleshooting

### Maps not displaying
- Ensure `folium` is installed: `pip install folium`
- Check that output directory exists: `mkdir -p output/water_heating_analysis`
- Verify internet connection (maps use OpenStreetMap tiles)

### Graphs not saving
- Verify write permissions in `output/water_heating_analysis/` directory
- Check disk space availability
- Ensure `matplotlib` is installed: `pip install matplotlib`

### Missing data in visualizations
- Synthetic data is used for demonstration
- Replace with actual water temperature data from `Data/BullRunWaterTemperature.csv`
- Update data loading in test fixtures

## Integration with Model

These visualizations support:
1. **Model validation** — Verify water heating demand assumptions
2. **Stakeholder communication** — Show water heating drivers of demand
3. **Scenario analysis** — Compare demand across regions and seasons
4. **Documentation** — Include in technical reports and presentations
5. **Capacity planning** — Identify peak demand periods and regions

## Performance Metrics

- **Daily delta-T**: 62-75°F (varies by season and station)
- **Annual average delta-T**: 64-68°F across all stations
- **Annual WH demand**: ~50-60 therms/customer (baseline)
- **Seasonal variation**: 2-3x higher demand in winter vs. summer
- **Efficiency potential**: 25% reduction with high-efficiency equipment

## Next Steps

After generating visualizations:
1. Review delta-T patterns for accuracy and reasonableness
2. Validate water heating demand estimates against historical billing data
3. Confirm seasonal patterns match known water heating behavior
4. Compare station-level demand with utility records
5. Use visualizations in model documentation and stakeholder presentations
6. Proceed to Task 7 (Checkpoint - Verify core model components)
