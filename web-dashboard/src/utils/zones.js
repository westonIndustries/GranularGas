/**
 * Zone Management Utilities
 * Handles loading and managing geographic zones with GeoJSON boundaries
 */

/**
 * Parse zones CSV data
 * @param {string} csvText - CSV text content
 * @returns {Array} Array of zone objects
 */
const parseZonesCSV = (csvText) => {
  const lines = csvText.trim().split('\n');
  if (lines.length < 2) return [];

  // Parse header
  const headers = lines[0].split(',').map(h => h.trim());
  const zones = [];

  // Parse data rows
  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',').map(v => v.trim());
    if (values.length === 0 || !values[0]) continue;

    const zone = {};
    headers.forEach((header, index) => {
      const value = values[index];
      // Convert numeric fields
      if (header === 'zone_number' || header === 'area_sqmi' || header === 'population') {
        zone[header] = value ? parseInt(value) : null;
      } else {
        zone[header] = value;
      }
    });
    zones.push(zone);
  }

  return zones;
};

/**
 * Load zone GeoJSON data
 * @param {number} zoneNumber - Zone number to load
 * @returns {Promise<Object>} GeoJSON FeatureCollection
 */
export const loadZone = async (zoneNumber) => {
  try {
    const response = await fetch(`/zones/zone_${zoneNumber}.geojson`);
    if (!response.ok) {
      throw new Error(`Failed to load zone ${zoneNumber}: ${response.statusText}`);
    }
    const geojson = await response.json();
    return geojson;
  } catch (error) {
    console.error(`Error loading zone ${zoneNumber}:`, error);
    throw error;
  }
};

/**
 * Get zone metadata from GeoJSON
 * @param {Object} geojson - GeoJSON FeatureCollection
 * @returns {Object} Zone metadata
 */
export const getZoneMetadata = (geojson) => {
  if (!geojson || !geojson.features || geojson.features.length === 0) {
    return null;
  }

  const feature = geojson.features[0];
  return {
    zone_number: feature.properties.zone_number,
    zone_name: feature.properties.zone_name,
    description: feature.properties.description,
    area_sqmi: feature.properties.area_sqmi,
    population: feature.properties.population
  };
};

/**
 * Get zone boundary coordinates
 * @param {Object} geojson - GeoJSON FeatureCollection
 * @returns {Array} Coordinates array
 */
export const getZoneBoundary = (geojson) => {
  if (!geojson || !geojson.features || geojson.features.length === 0) {
    return null;
  }

  const feature = geojson.features[0];
  return feature.geometry.coordinates;
};

/**
 * Calculate zone center (centroid)
 * @param {Object} geojson - GeoJSON FeatureCollection
 * @returns {Object} {lat, lng} center coordinates
 */
export const getZoneCenter = (geojson) => {
  const boundary = getZoneBoundary(geojson);
  if (!boundary) return null;

  // For Polygon, get first coordinate array
  const coords = boundary[0];
  
  let sumLat = 0;
  let sumLng = 0;
  
  coords.forEach(([lng, lat]) => {
    sumLng += lng;
    sumLat += lat;
  });

  return {
    lat: sumLat / coords.length,
    lng: sumLng / coords.length
  };
};

/**
 * Get zone bounds (bounding box)
 * @param {Object} geojson - GeoJSON FeatureCollection
 * @returns {Object} {north, south, east, west} bounds
 */
export const getZoneBounds = (geojson) => {
  const boundary = getZoneBoundary(geojson);
  if (!boundary) return null;

  const coords = boundary[0];
  
  let minLat = coords[0][1];
  let maxLat = coords[0][1];
  let minLng = coords[0][0];
  let maxLng = coords[0][0];

  coords.forEach(([lng, lat]) => {
    minLat = Math.min(minLat, lat);
    maxLat = Math.max(maxLat, lat);
    minLng = Math.min(minLng, lng);
    maxLng = Math.max(maxLng, lng);
  });

  return {
    north: maxLat,
    south: minLat,
    east: maxLng,
    west: minLng
  };
};

/**
 * Parse zones CSV data
 * @param {string} csvText - CSV text content
 * @returns {Array} Array of zone objects
 */
const parseZonesCSV = (csvText) => {
  const lines = csvText.trim().split('\n');
  if (lines.length < 2) return [];

  // Parse header
  const headers = lines[0].split(',').map(h => h.trim());
  const zones = [];

  // Parse data rows
  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',').map(v => v.trim());
    if (values.length === 0 || !values[0]) continue;

    const zone = {};
    headers.forEach((header, index) => {
      const value = values[index];
      // Convert numeric fields
      if (header === 'zone_number' || header === 'area_sqmi' || header === 'population') {
        zone[header] = value ? parseInt(value) : null;
      } else {
        zone[header] = value;
      }
    });
    zones.push(zone);
  }

  return zones;
};

/**
 * List available zones from CSV
 * @returns {Promise<Array>} Array of zone objects with metadata
 */
export const listAvailableZones = async () => {
  try {
    const response = await fetch('/zones.csv');
    if (!response.ok) {
      throw new Error(`Failed to load zones.csv: ${response.statusText}`);
    }
    const csvText = await response.text();
    const zones = parseZonesCSV(csvText);
    return zones;
  } catch (error) {
    console.error('Error loading zones from CSV:', error);
    throw error;
  }
};

/**
 * Validate zone number
 * @param {number} zoneNumber - Zone number to validate
 * @returns {boolean} True if zone is valid
 */
export const isValidZoneNumber = (zoneNumber) => {
  return Number.isInteger(zoneNumber) && zoneNumber > 0 && zoneNumber <= 999;
};

/**
 * Format zone info for display
 * @param {Object} metadata - Zone metadata
 * @returns {string} Formatted zone info
 */
export const formatZoneInfo = (metadata) => {
  if (!metadata) return 'Unknown Zone';
  
  let info = `Zone ${metadata.zone_number}: ${metadata.zone_name}`;
  
  if (metadata.area_sqmi) {
    info += ` (${metadata.area_sqmi.toLocaleString()} sq mi)`;
  }
  
  return info;
};

/**
 * Export zone data
 * @param {Object} geojson - GeoJSON FeatureCollection
 * @param {string} format - Export format ('geojson', 'json')
 * @returns {string} Formatted data
 */
export const exportZoneData = (geojson, format = 'geojson') => {
  if (format === 'geojson' || format === 'json') {
    return JSON.stringify(geojson, null, 2);
  }
  
  throw new Error(`Unsupported export format: ${format}`);
};

export default {
  loadZone,
  getZoneMetadata,
  getZoneBoundary,
  getZoneCenter,
  getZoneBounds,
  listAvailableZones,
  isValidZoneNumber,
  formatZoneInfo,
  exportZoneData
};
