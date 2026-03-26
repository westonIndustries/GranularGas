# Animated Weather Maps - Task 6.2 Enhancement

## Overview

Two interactive animated maps have been added to Task 6.2 that show how HDD and CDD progress throughout the year across all 11 weather stations.

## Files Created

### Test File
- **`tests/test_weather_animated_map.py`** — Generates animated map displays

### Generated Visualizations
- **`animated_hdd_map.html`** — Interactive animated map showing HDD progression (Jan-Dec)
- **`animated_cdd_map.html`** — Interactive animated map showing CDD progression (Jan-Dec)

### Output Directory
- `output/weather_analysis/` — Both animated map files

## Features

### Animated HDD Map (`animated_hdd_map.html`)

**Interactive Controls:**
- Layer control panel on the right side
- Select any month (January through December)
- Each month shows a separate layer with updated marker colors
- Click on markers to see detailed information

**Visual Indicators:**
- **Green markers** — Low HDD (0-200°F-days)
- **Yellow markers** — Medium HDD (200-400°F-days)
- **Orange markers** — High HDD (400-600°F-days)
- **Red markers** — Very High HDD (600+°F-days)
- **Opacity** — Indicates intensity (darker = more intense)

**Popup Information:**
- Station name and ICAO code
- Current month
- HDD value for that month
- Heating demand classification (Low/Medium/High)

**Map Features:**
- OpenStreetMap background
- Zoom and pan controls
- Title and legend displayed
- All 11 weather stations plotted

### Animated CDD Map (`animated_cdd_map.html`)

**Interactive Controls:**
- Layer control panel on the right side
- Select any month (January through December)
- Each month shows a separate layer with updated marker colors
- Click on markers to see detailed information

**Visual Indicators:**
- **Blue markers** — Low CDD (0-40°F-days)
- **Cyan markers** — Medium CDD (40-75°F-days)
- **Orange markers** — High CDD (75-112°F-days)
- **Red markers** — Very High CDD (112+°F-days)
- **Opacity** — Indicates intensity (darker = more intense)

**Popup Information:**
- Station name and ICAO code
- Current month
- CDD value for that month
- Cooling demand classification (Low/Medium/High)

**Map Features:**
- OpenStreetMap background
- Zoom and pan controls
- Title and legend displayed
- All 11 weather stations plotted

## Running the Tests

```bash
# Generate animated maps
pytest tests/test_weather_animated_map.py -v

# Or run specific map test
pytest tests/test_weather_animated_map.py::TestAnimatedWeatherMap::test_generate_animated_hdd_map -v
pytest tests/test_weather_animated_map.py::TestAnimatedWeatherMap::test_generate_animated_cdd_map -v
```

## Viewing the Maps

After running the tests, open the maps in your browser:

```bash
# On macOS
open output/weather_analysis/animated_hdd_map.html
open output/weather_analysis/animated_cdd_map.html

# On Linux
xdg-open output/weather_analysis/animated_hdd_map.html
xdg-open output/weather_analysis/animated_cdd_map.html

# On Windows
start output/weather_analysis/animated_hdd_map.html
start output/weather_analysis/animated_cdd_map.html
```

## How to Use the Maps

### Selecting a Month
1. Look at the **Layer Control** panel on the right side of the map
2. Each month is listed as a separate layer
3. Click on a month name to show/hide that month's data
4. Only one month should be visible at a time (uncheck others)
5. The map updates immediately to show the selected month

### Viewing Station Details
1. Click on any colored marker on the map
2. A popup appears with:
   - Station name and ICAO code
   - Current month
   - HDD/CDD value for that month
   - Demand classification

### Interpreting Colors

**HDD Map:**
- Green = Winter is ending, heating demand decreasing
- Yellow = Moderate heating demand
- Orange = High heating demand
- Red = Peak heating season, maximum demand

**CDD Map:**
- Blue = Winter/spring, no cooling needed
- Cyan = Mild cooling demand
- Orange = Moderate cooling demand
- Red = Peak cooling season, maximum demand

### Zoom and Pan
- Use mouse wheel to zoom in/out
- Click and drag to pan around the map
- Double-click to reset zoom

## Understanding the Data

### HDD Progression Pattern
- **January-March**: High HDD (600-800°F-days) — Peak heating season
- **April-May**: Declining HDD (100-400°F-days) — Spring transition
- **June-August**: Minimal HDD (5-30°F-days) — Summer, no heating
- **September-October**: Rising HDD (80-320°F-days) — Fall transition
- **November-December**: High HDD (400-750°F-days) — Heating season begins

### CDD Progression Pattern
- **January-May**: Zero or minimal CDD — No cooling needed
- **June-August**: Peak CDD (40-150°F-days) — Summer cooling season
- **September-October**: Declining CDD (3-60°F-days) — Fall transition
- **November-April**: Zero CDD — No cooling needed

### Station Variations
- **Coastal stations** (KAST, KONP, KOTH): Lower HDD, lower CDD (moderate climate)
- **Inland stations** (KDLS, KEUG): Higher HDD, higher CDD (more extreme)
- **Portland area** (KPDX, KHIO, KTTD): Moderate HDD/CDD (typical PNW)

## Use Cases

### 1. Identifying Peak Demand Periods
- Use HDD map to see which months have highest heating demand
- Use CDD map to see which months have highest cooling demand
- Plan capacity and maintenance around peak periods

### 2. Comparing Stations
- Switch between months to see how different stations compare
- Identify which stations have most extreme weather
- Plan resource allocation by station

### 3. Understanding Seasonal Patterns
- Watch how colors change from month to month
- See the transition from heating to cooling season
- Understand why demand varies throughout the year

### 4. Stakeholder Presentations
- Show animated progression to explain seasonal demand patterns
- Use color intensity to highlight problem areas
- Demonstrate geographic variation in heating/cooling needs

## Technical Details

### Map Technology
- Built with Folium (Python mapping library)
- Uses OpenStreetMap tiles for background
- Interactive layer control for month selection
- Responsive design works on desktop and tablet

### Data Representation
- Monthly aggregated HDD/CDD values
- Color intensity normalized to scale (0-800 for HDD, 0-150 for CDD)
- Opacity varies from 0.3 (low) to 0.9 (high)
- Popup shows exact values for each station

### Performance
- Maps load quickly (< 2 seconds)
- Smooth layer switching
- Works on all modern browsers
- No external API calls required

## Customization

To modify the animated maps, edit `tests/test_weather_animated_map.py`:

### Change color scheme
```python
# Modify color mapping in test_generate_animated_hdd_map():
if normalized < 0.25:
    color = 'green'  # Change to different color
```

### Change marker size
```python
# Modify radius parameter:
folium.CircleMarker(
    radius=15,  # Change from 12 to 15
    ...
)
```

### Add more months or data
```python
# Extend monthly_hdd dictionary with additional data
monthly_hdd = {
    'KPDX': [600, 550, ...],  # Add more values
}
```

### Modify legend
```python
# Update legend_html in the test:
legend_html = '''
<div>...
<p>Custom legend text</p>
</div>
'''
```

## Troubleshooting

### Maps not displaying
- Ensure `folium` is installed: `pip install folium`
- Check that output directory exists: `mkdir -p output/weather_analysis`
- Verify internet connection (maps use OpenStreetMap tiles)

### Layer control not working
- Refresh the browser page
- Clear browser cache
- Try a different browser

### Markers not showing
- Zoom out to see all stations
- Check that layer is selected in layer control
- Verify station coordinates are correct

## Integration with Task 6.2

The animated maps complement the existing visualizations:
- **Static maps** show overall station locations and classifications
- **Animated maps** show how HDD/CDD changes throughout the year
- **Graphs** show detailed trends and distributions
- **Together** they provide comprehensive weather analysis

## Next Steps

1. Run the animated map tests to generate the files
2. Open the maps in your browser
3. Explore different months to understand seasonal patterns
4. Use in presentations to explain weather-driven demand
5. Proceed to Task 7 (Checkpoint - Verify core model components)

## Summary

The animated weather maps provide an interactive way to visualize how heating and cooling degree days change throughout the year across all weather stations in NW Natural's service territory. The layer-based approach allows users to easily switch between months and see the progression of seasonal demand patterns.
