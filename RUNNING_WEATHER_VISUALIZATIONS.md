# Running Weather Visualizations - Task 6.2

## Quick Start

To generate all weather analysis visualizations:

```bash
# Run the visualization test suite
pytest tests/test_weather_hdd_property_visualizations.py -v

# Or run a specific visualization test
pytest tests/test_weather_hdd_property_visualizations.py::TestHDDPropertyWithVisualizations::test_generate_weather_station_map -v
```

## Output Location

All visualizations are saved to: `output/weather_analysis/`

## Generated Files

### Interactive Map
- **weather_stations_map.html** — Open in web browser to explore weather stations
  - Click on markers to see station details
  - Zoom and pan to explore the service territory
  - Color-coded by source (blue=NW Natural, green=NOAA, orange=Proxy)

### HDD/CDD Analysis (PNG images)
- **hdd_cdd_daily.png** — Daily heating and cooling degree days
- **cumulative_hdd_cdd.png** — Cumulative degree days over the year
- **monthly_hdd_heatmap.png** — Monthly HDD by station
- **monthly_cdd_heatmap.png** — Monthly CDD by station
- **annual_hdd_boxplot.png** — Annual HDD distribution (2015-2025)
- **annual_cdd_boxplot.png** — Annual CDD distribution (2015-2025)

### Water Temperature Analysis (PNG images)
- **water_temperature_daily.png** — Daily water temperature patterns (2008-2025)
- **water_temperature_seasonal.png** — Seasonal water temperature with min/max bands

## Individual Visualization Tests

Run specific visualizations:

```bash
# Weather station map
pytest tests/test_weather_hdd_property_visualizations.py::TestHDDPropertyWithVisualizations::test_generate_weather_station_map -v

# HDD/CDD graphs
pytest tests/test_weather_hdd_property_visualizations.py::TestHDDPropertyWithVisualizations::test_generate_hdd_cdd_daily_graph -v
pytest tests/test_weather_hdd_property_visualizations.py::TestHDDPropertyWithVisualizations::test_generate_cumulative_hdd_cdd_graph -v

# Heatmaps
pytest tests/test_weather_hdd_property_visualizations.py::TestHDDPropertyWithVisualizations::test_generate_monthly_hdd_heatmap -v
pytest tests/test_weather_hdd_property_visualizations.py::TestHDDPropertyWithVisualizations::test_generate_monthly_cdd_heatmap -v

# Box plots
pytest tests/test_weather_hdd_property_visualizations.py::TestHDDPropertyWithVisualizations::test_generate_annual_hdd_boxplot -v
pytest tests/test_weather_hdd_property_visualizations.py::TestHDDPropertyWithVisualizations::test_generate_annual_cdd_boxplot -v

# Water temperature
pytest tests/test_weather_hdd_property_visualizations.py::TestHDDPropertyWithVisualizations::test_generate_water_temperature_graph -v
pytest tests/test_weather_hdd_property_visualizations.py::TestHDDPropertyWithVisualizations::test_generate_monthly_water_temperature_graph -v
```

## Viewing the Interactive Map

After running the tests, open the weather station map in your browser:

```bash
# On macOS
open output/weather_analysis/weather_stations_map.html

# On Linux
xdg-open output/weather_analysis/weather_stations_map.html

# On Windows
start output/weather_analysis/weather_stations_map.html
```

## Understanding the Visualizations

### Weather Station Map
- **Blue markers** = NW Natural-supplied weather stations (primary data sources)
- **Green markers** = NOAA stations (climate normals reference)
- **Orange markers** = Proxy stations (used when primary data unavailable)
- Hover over markers to see station details
- Zoom to explore specific regions

### HDD/CDD Daily Graph
- **Blue line** = Heating Degree Days (demand for space heating)
- **Red line** = Cooling Degree Days (demand for space cooling)
- Shows seasonal patterns: high HDD in winter, high CDD in summer
- Used to validate weather-driven simulation assumptions

### Cumulative HDD/CDD Graph
- **Blue area** = Cumulative HDD (total heating demand over the year)
- **Red area** = Cumulative CDD (total cooling demand over the year)
- Helps identify when heating/cooling seasons peak
- Used for annual demand forecasting

### Monthly HDD/CDD Heatmaps
- **Rows** = Weather stations (11 total)
- **Columns** = Months (Jan-Dec)
- **Color intensity** = Magnitude of HDD/CDD
- Identifies which stations have highest heating/cooling demand
- Useful for comparing regional climate differences

### Annual HDD/CDD Box Plots
- **Box** = Interquartile range (middle 50% of years)
- **Line in box** = Median year
- **Whiskers** = Min/max years
- **Dots** = Outlier years
- Shows year-to-year variability in heating/cooling demand
- Useful for scenario planning (warm vs. cold years)

### Water Temperature Graphs
- **Daily graph** = Shows seasonal pattern with year-to-year variation
- **Seasonal graph** = Average monthly temperature with confidence bands
- Used to calculate water heating demand (delta-T method)
- Coldest in winter (~42°F), warmest in summer (~58°F)

## Customizing Visualizations

To modify visualizations, edit `tests/test_weather_hdd_property_visualizations.py`:

### Change color schemes
```python
# In heatmap tests, modify cmap parameter:
sns.heatmap(df_hdd, cmap='RdYlBu')  # Different color scheme
```

### Change figure size
```python
# In any test, modify figsize:
fig, ax = plt.subplots(figsize=(16, 8))  # Larger figure
```

### Change station data
```python
# In test_generate_weather_station_map, modify stations dict:
stations = {
    'KPDX': {'lat': 45.5891, 'lon': -122.5975, ...},
    # Add or modify stations
}
```

## Troubleshooting

### Map not displaying
- Ensure `folium` is installed: `pip install folium`
- Check that output directory exists: `mkdir -p output/weather_analysis`

### Graphs not saving
- Verify write permissions in `output/weather_analysis/` directory
- Check disk space availability

### Missing data in visualizations
- Synthetic data is used for demonstration
- Replace with actual weather data from `Data/` directory
- Update data loading in test fixtures

## Integration with Model

These visualizations support:
1. **Model validation** — Verify weather data quality and patterns
2. **Stakeholder communication** — Show weather drivers of demand
3. **Scenario analysis** — Compare heating/cooling demand across regions
4. **Documentation** — Include in technical reports and presentations

## Next Steps

After generating visualizations:
1. Review weather station map for coverage and accuracy
2. Validate HDD/CDD patterns against known climate data
3. Confirm water temperature data matches Bull Run observations
4. Use visualizations in model documentation and presentations
5. Proceed to Task 6.3 (water heating delta property test)
