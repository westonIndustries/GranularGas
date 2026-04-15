# Zone Management Guide

## Overview

The web dashboard supports multi-zone forecasting. Zones are defined in a CSV file (`public/zones.csv`) and can optionally have geographic boundaries defined in GeoJSON format. Users can select a zone when running forecasts, and the zone information is included in all outputs.

## Zone CSV File

### Location

```
public/zones.csv
```

### Format

CSV file with the following columns:

```csv
zone_number,zone_name,description,area_sqmi,population
1,Portland Metro,Portland metropolitan area and surrounding region,4500,2500000
2,Eugene Area,Eugene metropolitan area and surrounding region,3200,400000
3,Gorge Region,Columbia River Gorge and surrounding region,2800,150000
```

### Columns

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `zone_number` | integer | Yes | Unique zone identifier (1-999) |
| `zone_name` | string | Yes | Human-readable zone name |
| `description` | string | Yes | Zone description |
| `area_sqmi` | integer | No | Area in square miles |
| `population` | integer | No | Population estimate |

### Example

```csv
zone_number,zone_name,description,area_sqmi,population
1,Portland Metro,Portland metropolitan area,4500,2500000
2,Eugene Area,Eugene metropolitan area,3200,400000
3,Gorge Region,Columbia River Gorge,2800,150000
4,Salem Area,Salem metropolitan area,2000,300000
5,Bend Area,Bend metropolitan area,1500,200000
```

## Adding New Zones

### Step 1: Edit zones.csv

Add a new row to `public/zones.csv`:

```csv
zone_number,zone_name,description,area_sqmi,population
...
4,Salem Area,Salem metropolitan area,2000,300000
```

### Step 2: (Optional) Create GeoJSON File

If you want geographic boundaries, create `public/zones/zone_4.geojson`:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "zone_number": 4,
        "zone_name": "Salem Area",
        "description": "Salem metropolitan area"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [-123.5, 44.5],
            [-122.5, 44.5],
            [-122.5, 45.0],
            [-123.5, 45.0],
            [-123.5, 44.5]
          ]
        ]
      }
    }
  ]
}
```

### Step 3: Test

1. Start the development server: `npm start`
2. Select the new zone from the Zone dropdown
3. Verify zone information displays correctly
4. Run a forecast to confirm zone is included in output

## Using Zones in Forecasts

### Selecting a Zone

1. Open the dashboard
2. In the Parameter Panel, select a zone from the "Zone Number" dropdown
3. Zone information (name, description, area, population) displays below
4. Adjust other parameters as needed
5. Click "Run Forecast"

### Zone in Output

The zone number is included in all forecast outputs:

**Results Table:**
```
Zone Number: 1
Scenario ID: abc123
Base Year: 2025
...
```

**Exported Data (CSV/JSON):**
```json
{
  "zone_number": 1,
  "scenario_id": "abc123",
  "base_year": 2025,
  ...
}
```

**Saved Scenarios:**
```json
{
  "id": "scenario1",
  "zone_number": 1,
  "name": "High Electrification",
  ...
}
```

## Zone Utilities

The `src/utils/zones.js` module provides utilities for zone management:

### Loading Zones from CSV

```javascript
import { listAvailableZones } from '../utils/zones';

const zones = await listAvailableZones();
// Returns: [
//   { zone_number: 1, zone_name: "Portland Metro", ... },
//   { zone_number: 2, zone_name: "Eugene Area", ... },
//   ...
// ]
```

### Loading a Zone's GeoJSON

```javascript
import { loadZone } from '../utils/zones';

const geojson = await loadZone(1);
```

### Getting Zone Metadata

```javascript
import { getZoneMetadata } from '../utils/zones';

const metadata = getZoneMetadata(geojson);
// Returns: { zone_number, zone_name, description, area_sqmi, population }
```

### Getting Zone Boundary

```javascript
import { getZoneBoundary } from '../utils/zones';

const boundary = getZoneBoundary(geojson);
// Returns: Polygon coordinates array
```

### Getting Zone Center

```javascript
import { getZoneCenter } from '../utils/zones';

const center = getZoneCenter(geojson);
// Returns: { lat, lng }
```

### Getting Zone Bounds

```javascript
import { getZoneBounds } from '../utils/zones';

const bounds = getZoneBounds(geojson);
// Returns: { north, south, east, west }
```

## API Integration

The forecasting model API should accept zone_number in forecast requests:

### Request

```json
POST /api/forecast
{
  "zone_number": 1,
  "base_year": 2025,
  "forecast_horizon": 10,
  "housing_growth_rate": 0.01,
  "electrification_rate": 0.05,
  "efficiency_improvement": 0.02,
  "weather_assumption": "normal"
}
```

### Response

```json
{
  "zone_number": 1,
  "scenario_id": "abc123",
  "base_year": 2025,
  "forecast_horizon": 10,
  "total_demand_2035": 1500000,
  "upc_2035": 750,
  ...
}
```

## Optional: GeoJSON Zone Boundaries

If you want to display zone boundaries on a map, create GeoJSON files in `public/zones/`:

### File Structure

```
public/zones/
├── zone_1.geojson
├── zone_2.geojson
├── zone_3.geojson
└── ...
```

### GeoJSON Format

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "zone_number": 1,
        "zone_name": "Portland Metro",
        "description": "Portland metropolitan area"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [-123.5, 45.0],
            [-122.0, 45.0],
            [-122.0, 46.0],
            [-123.5, 46.0],
            [-123.5, 45.0]
          ]
        ]
      }
    }
  ]
}
```

## Creating GeoJSON Files

### Using Geojson.io

1. Visit http://geojson.io/
2. Draw the zone boundary on the map
3. Add properties (zone_number, zone_name, etc.)
4. Export as GeoJSON
5. Save to `public/zones/zone_N.geojson`

### Using QGIS

1. Open QGIS
2. Create a new polygon layer
3. Draw the zone boundary
4. Add attributes (zone_number, zone_name, etc.)
5. Export as GeoJSON
6. Save to `public/zones/zone_N.geojson`

### Using ArcGIS Online

1. Create a feature service with zone boundaries
2. Export as GeoJSON
3. Save to `public/zones/zone_N.geojson`

## Coordinate System

All coordinates must be in WGS84 (EPSG:4326):
- **Longitude**: -180 to 180 (West to East)
- **Latitude**: -90 to 90 (South to North)

Example: Portland, OR
- Longitude: -122.5 (West)
- Latitude: 45.5 (North)

## Troubleshooting

### Zones Not Appearing in Dropdown

1. Check zones.csv exists: `public/zones.csv`
2. Verify CSV format is correct
3. Check browser console for errors
4. Verify CSV file is readable

### Zone Information Not Displaying

1. Check zones.csv has required columns
2. Verify zone_number is numeric
3. Check browser console for errors
4. Validate CSV syntax

### Forecast Fails with Zone

1. Verify API accepts zone_number parameter
2. Check zone_number is valid (1-999)
3. Verify API returns zone_number in response
4. Check browser console for API errors

## Examples

### zones.csv Example

```csv
zone_number,zone_name,description,area_sqmi,population
1,Portland Metro,Portland metropolitan area and surrounding region,4500,2500000
2,Eugene Area,Eugene metropolitan area and surrounding region,3200,400000
3,Gorge Region,Columbia River Gorge and surrounding region,2800,150000
4,Salem Area,Salem metropolitan area,2000,300000
5,Bend Area,Bend metropolitan area,1500,200000
6,Medford Area,Medford metropolitan area,1200,150000
```

## References

- CSV Format: https://en.wikipedia.org/wiki/Comma-separated_values
- GeoJSON Specification: https://tools.ietf.org/html/rfc7946
- WGS84 Coordinate System: https://en.wikipedia.org/wiki/World_Geodetic_System
- Geojson.io: http://geojson.io/
- QGIS: https://qgis.org/
- ArcGIS Online: https://www.arcgis.com/

---

**Last Updated**: April 10, 2026
