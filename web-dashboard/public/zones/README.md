# Zone GeoJSON Files

This directory contains GeoJSON files that define the geographic boundaries for each zone.

## File Structure

Each zone should have a corresponding GeoJSON file:

```
zones/
├── zone_1.geojson
├── zone_2.geojson
├── zone_3.geojson
└── ...
```

## GeoJSON Format

Each file should contain a FeatureCollection with the zone boundary:

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
            [-122.5, 45.4],
            [-122.4, 45.4],
            [-122.4, 45.5],
            [-122.5, 45.5],
            [-122.5, 45.4]
          ]
        ]
      }
    }
  ]
}
```

## Adding New Zones

1. Create a new GeoJSON file: `zone_N.geojson`
2. Define the zone boundary as a Polygon or MultiPolygon
3. Include zone metadata in properties
4. Update the zones list in the application

## Zone Properties

Each zone feature should include:

- `zone_number` (integer) - Unique zone identifier
- `zone_name` (string) - Human-readable zone name
- `description` (string) - Zone description
- `area_sqmi` (number) - Area in square miles (optional)
- `population` (number) - Population estimate (optional)

## Coordinate System

All coordinates should be in WGS84 (EPSG:4326):
- Longitude: -180 to 180
- Latitude: -90 to 90

## Tools for Creating GeoJSON

- **Mapbox Studio**: https://studio.mapbox.com/
- **Geojson.io**: http://geojson.io/
- **QGIS**: https://qgis.org/
- **ArcGIS Online**: https://www.arcgis.com/

## Example Zones

### Zone 1: Portland Metro
- Area: Portland, Oregon metropolitan area
- Coordinates: ~45.5°N, 122.5°W

### Zone 2: Eugene Area
- Area: Eugene, Oregon metropolitan area
- Coordinates: ~44.0°N, 123.1°W

### Zone 3: Gorge Region
- Area: Columbia River Gorge
- Coordinates: ~45.7°N, 121.0°W

## Loading Zones in Application

Zones are loaded dynamically:

```javascript
const loadZone = async (zoneNumber) => {
  const response = await fetch(`/zones/zone_${zoneNumber}.geojson`);
  const geojson = await response.json();
  return geojson;
};
```

## Validation

Validate GeoJSON files using:
- https://geojson.io/
- https://jsonlint.com/

## References

- GeoJSON Specification: https://tools.ietf.org/html/rfc7946
- WGS84 Coordinate System: https://en.wikipedia.org/wiki/World_Geodetic_System
