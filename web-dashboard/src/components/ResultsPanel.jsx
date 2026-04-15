import React, { useState } from 'react';
import { exportResultsCSV, exportResultsJSON } from '../api/client';

const ResultsPanel = ({ results }) => {
  const [activeChart, setActiveChart] = useState('summary');
  const [exporting, setExporting] = useState(false);

  const handleExport = async (format) => {
    try {
      setExporting(true);
      const blob = format === 'csv' 
        ? await exportResultsCSV(results.scenario_id)
        : await exportResultsJSON(results.scenario_id);
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `forecast_${results.scenario_id}.${format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error(`Export ${format} failed:`, error);
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="results-panel">
      <h2>Forecast Results</h2>

      <div className="results-toolbar">
        <div className="chart-tabs">
          <button
            className={`chart-tab ${activeChart === 'summary' ? 'active' : ''}`}
            onClick={() => setActiveChart('summary')}
          >
            Summary
          </button>
          <button
            className={`chart-tab ${activeChart === 'trends' ? 'active' : ''}`}
            onClick={() => setActiveChart('trends')}
          >
            Trends
          </button>
          <button
            className={`chart-tab ${activeChart === 'breakdown' ? 'active' : ''}`}
            onClick={() => setActiveChart('breakdown')}
          >
            Breakdown
          </button>
          <button
            className={`chart-tab ${activeChart === 'details' ? 'active' : ''}`}
            onClick={() => setActiveChart('details')}
          >
            Details
          </button>
        </div>

        <div className="export-buttons">
          <button
            className="btn btn-small"
            onClick={() => handleExport('csv')}
            disabled={exporting}
          >
            Export CSV
          </button>
          <button
            className="btn btn-small"
            onClick={() => handleExport('json')}
            disabled={exporting}
          >
            Export JSON
          </button>
        </div>
      </div>

      <div className="results-content">
        {activeChart === 'summary' && (
          <div className="summary-view">
            <div className="metric-card">
              <h3>Total Demand (2035)</h3>
              <p className="metric-value">
                {results.total_demand_2035?.toLocaleString() || 'N/A'} therms
              </p>
            </div>
            <div className="metric-card">
              <h3>Use Per Customer (2035)</h3>
              <p className="metric-value">
                {results.upc_2035?.toFixed(1) || 'N/A'} therms/customer
              </p>
            </div>
            <div className="metric-card">
              <h3>Demand Change</h3>
              <p className="metric-value">
                {results.demand_change_pct?.toFixed(1) || 'N/A'}%
              </p>
            </div>
            <div className="metric-card">
              <h3>Electrification Impact</h3>
              <p className="metric-value">
                {results.electrification_impact?.toFixed(1) || 'N/A'}%
              </p>
            </div>
          </div>
        )}

        {activeChart === 'trends' && (
          <div className="trends-view">
            <p>Trend charts will be displayed here</p>
            <p className="placeholder-text">
              Line charts showing UPC trends, end-use composition over time
            </p>
          </div>
        )}

        {activeChart === 'breakdown' && (
          <div className="breakdown-view">
            <p>Breakdown charts will be displayed here</p>
            <p className="placeholder-text">
              Bar charts and stacked area charts showing demand by segment, district, end-use
            </p>
          </div>
        )}

        {activeChart === 'details' && (
          <div className="details-view">
            <h3>Detailed Results</h3>
            <table className="results-table">
              <thead>
                <tr>
                  <th>Metric</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Zone Number</td>
                  <td>{results.zone_number}</td>
                </tr>
                <tr>
                  <td>Scenario ID</td>
                  <td>{results.scenario_id}</td>
                </tr>
                <tr>
                  <td>Base Year</td>
                  <td>{results.base_year}</td>
                </tr>
                <tr>
                  <td>Forecast Horizon</td>
                  <td>{results.forecast_horizon} years</td>
                </tr>
                <tr>
                  <td>Total Premises</td>
                  <td>{results.total_premises?.toLocaleString()}</td>
                </tr>
                <tr>
                  <td>Total Equipment</td>
                  <td>{results.total_equipment?.toLocaleString()}</td>
                </tr>
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsPanel;
