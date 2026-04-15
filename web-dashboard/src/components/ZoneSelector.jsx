import React, { useState, useEffect } from 'react';
import { loadZone, getZoneMetadata, formatZoneInfo, listAvailableZones } from '../utils/zones';

const ZoneSelector = ({ selectedZone, onZoneChange, disabled }) => {
  const [zones, setZones] = useState([]);
  const [zoneInfo, setZoneInfo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load available zones from CSV on mount
  useEffect(() => {
    loadAvailableZonesFromCSV();
  }, []);

  // Load zone info when selected zone changes
  useEffect(() => {
    if (selectedZone) {
      loadZoneInfo(selectedZone);
    }
  }, [selectedZone]);

  const loadAvailableZonesFromCSV = async () => {
    try {
      setLoading(true);
      const availableZones = await listAvailableZones();
      setZones(availableZones);
      setError(null);
    } catch (err) {
      console.error('Error loading zones:', err);
      setError('Failed to load available zones from zones.csv');
    } finally {
      setLoading(false);
    }
  };

  const loadZoneInfo = async (zoneNumber) => {
    try {
      // Find zone in loaded zones array
      const zone = zones.find(z => z.zone_number === zoneNumber);
      if (zone) {
        setZoneInfo(zone);
        setError(null);
      } else {
        // Try to load from GeoJSON if available
        const geojson = await loadZone(zoneNumber);
        const metadata = getZoneMetadata(geojson);
        setZoneInfo(metadata);
        setError(null);
      }
    } catch (err) {
      console.error('Error loading zone info:', err);
      setError(`Failed to load zone ${zoneNumber} information`);
      setZoneInfo(null);
    }
  };

  return (
    <div className="zone-selector">
      <div className="zone-input-group">
        <label htmlFor="zone-select">Zone Number</label>
        <select
          id="zone-select"
          value={selectedZone || ''}
          onChange={(e) => onZoneChange(parseInt(e.target.value))}
          disabled={disabled || loading || zones.length === 0}
          className="zone-select"
        >
          <option value="">Select a zone...</option>
          {zones.map(zone => (
            <option key={zone.zone_number} value={zone.zone_number}>
              Zone {zone.zone_number}: {zone.zone_name}
            </option>
          ))}
        </select>
        <p className="parameter-help">Select the geographic zone for this forecast</p>
      </div>

      {error && (
        <div className="zone-error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {zoneInfo && (
        <div className="zone-info-card">
          <h4>Zone {zoneInfo.zone_number}: {zoneInfo.zone_name}</h4>
          <p className="zone-description">{zoneInfo.description}</p>
          {zoneInfo.area_sqmi && (
            <p className="zone-stat">
              <strong>Area:</strong> {zoneInfo.area_sqmi.toLocaleString()} sq mi
            </p>
          )}
          {zoneInfo.population && (
            <p className="zone-stat">
              <strong>Population:</strong> {zoneInfo.population.toLocaleString()}
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default ZoneSelector;
