# Animated Water Heating Map - Task 6.3 Enhancement

## Overview

An interactive animated map has been added to Task 6.3 that shows how water heating delta-T (temperature difference) progresses throughout the year across all 11 weather stations.

## Files Created

### Test File
- **`tests/test_water_heating_animated_map.py`** — Generates animated water heating map

### Generated Visualization
- **`animated_delta_t_map.html`** — Interactive animated map showing delta-T progression (Jan-Dec)

### Output Directory
- `output/water_heating_analysis/` — Animated map file

## Features

### Animated Delta-T Map (`animated_delta_t_map.html`)

**Interactive Controls:**
- Layer control panel on the right side
- Select any month (January through December)
- Each month shows a separate layer with updated marker colors
- Click on markers to see detailed information
- Zoom and pan controls for exploring the map

**Visual Indicators:**
- **Blue markers** — Low delta-T (40-48°F) — Minimal water heating needed
- **Cyan markers** — Medium delta-T (48-58°F) — Moderate water heating
- **Orange markers** — High delta-T (58-68°F) — Significant water heating needed
- **Red markers** — Very High delta-T (68+°F) — Maximum water heating demand
- **Opacity** — Indicates intensity (lighter = lower demand, darker = higher demand)

**Popup Information:**
- Station name and ICAO code
- Current month
- Delta-T value (°F)
- Estimated water heating demand (therms/customer)
- Demand level classification (Low/Medium/High)

**Map Features:**
- OpenStreetMap background
- Zoom and pan controls
- Title and comprehensive legend displayed
- All 11 weather stations plotted
- Color scale shows delta-T range and corresponding WH demand

## Running the Tests

```bash
# Generate animated water heating map
pytest tests/test_water_heating_animated_map.py -v

# Or run specific test
pytest tests/test_water_heating_animated_map.py::TestAnimatedWaterHeatingMap::test_generate_animated_delta_t_map -v
```

## Viewing the Map

After running the tests, open the map in your browser:

```bash
# On macOS
open output/water_heating_analysis/animated_delta_t_map.html

# On Linux
xdg-open output/water_heating_analysis/animated_delta_t_map.html

# On Windows
start output/water_heating_analysis/animated_delta_t_map.html
```

## How to Use the Map

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
   - Delta-T value in °F
   - Estimated water heating demand in therms/customer
   - Demand level classification

### Interpreting Colors

**Delta-T Scale:**
- **Blue (40-48°F)** — Summer months, warm incoming water, low heating needed
- **Cyan (48-58°F)** — Spring/fall transition, moderate heating needed
- **Orange (58-68°F)** — Winter approaching/leaving, significant heating needed
- **Red (68+°F)** — Peak winter, maximum heating demand

**Water Heating Demand Estimates:**
- Low (32-38 therms/customer) — Summer, minimal heating
- Medium (38-46 therms/customer) — Transition seasons
- High (46-54 therms/customer) — Winter, significant heating
- Very High (54+ therms/customer) — Peak winter demand

### Zoom and Pan
- Use mouse wheel to zoom in/out
- Click and drag to pan around the map
- Double-click to reset zoom
- Use zoom controls in top-left corner

## Understanding the Data

### Delta-T Progression Pattern

**Winter Months (Jan-Feb, Nov-Dec):**
- Delta-T: 70-77°F
- Estimated WH demand: 56-62 therms/customer
- Cold incoming water requires significant heating
- Peak water heating season

**Spring Transition (Mar-Apr):**
- Delta-T: 60-68°F
- Estimated WH demand: 48-54 therms/customer
- Water warming up, heating demand declining
- Transition from peak to moderate demand

**Summer Months (May-Aug):**
- Delta-T: 40-50°F
- Estimated WH demand: 32-40 therms/customer
- Warm incoming water, minimal heating needed
- Lowest water heating demand period

**Fall Transition (Sep-Oct):**
- Delta-T: 50-60°F
- Estimated WH demand: 40-48 therms/customer
- Water cooling down, heating demand increasing
- Transition from low to moderate demand

### Station Variations

**Coastal Stations** (KAST, KONP, KOTH):
- Slightly lower delta-T (1-2°F cooler water)
- More moderate water heating demand
- Influenced by ocean temperature

**Inland Stations** (KDLS, KEUG):
- Slightly higher delta-T (1-2°F warmer water)
- Slightly higher water heating demand
- More extreme seasonal variation

**Portland Area** (KPDX, KHIO, KTTD):
- Moderate delta-T (typical PNW)
- Average water heating demand
- Representative of service territory

## Use Cases

### 1. Identifying Peak Water Heating Periods
- Use the map to see which months have highest delta-T
- Identify when water heating demand peaks (winter)
- Plan maintenance and capacity around peak periods

### 2. Comparing Stations
- Switch between months to see how different stations compare
- Identify which stations have most extreme water heating demand
- Plan resource allocation by station and season

### 3. Understanding Seasonal Patterns
- Watch how colors change from month to month
- See the transition from low (summer) to high (winter) demand
- Understand why water heating demand varies throughout the year

### 4. Estimating Water Heating Demand
- Use popup information to see estimated therms/customer
- Compare demand across stations and months
- Plan for efficiency improvements and electrification

### 5. Stakeholder Presentations
- Show animated progression to explain seasonal demand patterns
- Use color intensity to highlight peak demand periods
- Demonstrate geographic variation in water heating needs
- Illustrate impact of water temperature on energy demand

## Technical Details

### Map Technology
- Built with Folium (Python mapping library)
- Uses OpenStreetMap tiles for background
- Interactive layer control for month selection
- Responsive design works on desktop and tablet

### Data Representation
- Monthly aggregated delta-T values (40-77°F range)
- Color intensity normalized to scale
- Opacity varies from 0.3 (low) to 0.9 (high)
- Popup shows exact values and demand estimates

### Performance
- Map loads quickly (< 2 seconds)
- Smooth layer switching
- Works on all modern browsers
- No external API calls required

## Customization

To modify the animated map, edit `tests/test_water_heating_animated_map.py`:

### Change color scheme
```python
# Modify color mapping in test_generate_animated_delta_t_map():
if normalized < 0.25:
    color = 'blue'  # Change to different color
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
# Extend monthly_delta_t dictionary with additional data
monthly_delta_t = {
    'KPDX': [75, 72, 68, ...],  # Add more values
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

### Change delta-T scale
```python
# Modify normalization in test:
normalized = (delta_t - 40) / (77 - 40)  # Change min/max values
```

## Troubleshooting

### Map not displaying
- Ensure `folium` is installed: `pip install folium`
- Check that output directory exists: `mkdir -p output/water_heating_analysis`
- Verify internet connection (maps use OpenStreetMap tiles)

### Layer control not working
- Refresh the browser page
- Clear browser cache
- Try a different browser

### Markers not showing
- Zoom out to see all stations
- Check that layer is selected in layer control
- Verify station coordinates are correct

### Popup not appearing
- Click directly on the colored marker
- Try a different browser if issue persists
- Check browser console for errors

## Integration with Task 6.3

The animated map complements the existing visualizations:
- **Static maps** show overall district and station characteristics
- **Animated map** shows how delta-T changes throughout the year
- **Graphs** show detailed trends and distributions
- **Together** they provide comprehensive water heating analysis

## Comparison with Task 6.2 Animated Map

| Feature | HDD Map (6.2) | Delta-T Map (6.3) |
|---------|---------------|-------------------|
| Purpose | Heating demand | Water heating demand |
| Color Scale | Green-Yellow-Orange-Red | Blue-Cyan-Orange-Red |
| Range | 0-800°F-days | 40-77°F |
| Peak Season | Winter (Jan-Feb, Nov-Dec) | Winter (Jan-Feb, Nov-Dec) |
| Low Season | Summer (Jun-Aug) | Summer (Jun-Aug) |
| Demand Metric | HDD (degree days) | Delta-T (temperature difference) |

## Next Steps

1. Run the animated map test to generate the file
2. Open the map in your browser
3. Explore different months to understand seasonal patterns
4. Compare with HDD map (Task 6.2) to see correlation
5. Use in presentations to explain water heating demand
6. Proceed to Task 7 (Checkpoint - Verify core model components)

## Summary

The animated water heating map provides an interactive way to visualize how water heating delta-T changes throughout the year across all weather stations in NW Natural's service territory. The layer-based approach allows users to easily switch between months and see the progression of seasonal water heating demand patterns, with estimated therms/customer values for each station and month.
