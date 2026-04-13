import React, { useState } from 'react';
import { runForecast } from '../api/client';

const ParameterPanel = ({
  onForecastComplete,
  onError,
  onLoadingChange,
  onScenariosUpdate
}) => {
  const [params, setParams] = useState({
    base_year: 2025,
    forecast_horizon: 10,
    housing_growth_rate: 0.01,
    electrification_rate: 0.05,
    efficiency_improvement: 0.02,
    weather_assumption: 'normal'
  });

  const [scenarioName, setScenarioName] = useState('');

  const handleParameterChange = (key, value) => {
    setParams(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleRunForecast = async () => {
    try {
      onLoadingChange(true);
      onError(null);
      const results = await runForecast(params);
      onForecastComplete(results);
    } catch (error) {
      onError(error.message || 'Failed to run forecast');
    } finally {
      onLoadingChange(false);
    }
  };

  const handleReset = () => {
    setParams({
      base_year: 2025,
      forecast_horizon: 10,
      housing_growth_rate: 0.01,
      electrification_rate: 0.05,
      efficiency_improvement: 0.02,
      weather_assumption: 'normal'
    });
  };

  return (
    <div className="parameter-panel">
      <h2>Scenario Parameters</h2>

      <div className="parameter-group">
        <label>Scenario Name (optional)</label>
        <input
          type="text"
          value={scenarioName}
          onChange={(e) => setScenarioName(e.target.value)}
          placeholder="e.g., High Electrification"
        />
      </div>

      <div className="parameter-group">
        <label>Base Year</label>
        <input
          type="number"
          min="2020"
          max="2030"
          value={params.base_year}
          onChange={(e) => handleParameterChange('base_year', parseInt(e.target.value))}
        />
      </div>

      <div className="parameter-group">
        <label>Forecast Horizon (years)</label>
        <input
          type="range"
          min="1"
          max="30"
          value={params.forecast_horizon}
          onChange={(e) => handleParameterChange('forecast_horizon', parseInt(e.target.value))}
        />
        <span className="value-display">{params.forecast_horizon} years</span>
      </div>

      <div className="parameter-group">
        <label>Housing Growth Rate (%)</label>
        <input
          type="range"
          min="0"
          max="0.05"
          step="0.001"
          value={params.housing_growth_rate}
          onChange={(e) => handleParameterChange('housing_growth_rate', parseFloat(e.target.value))}
        />
        <span className="value-display">{(params.housing_growth_rate * 100).toFixed(2)}%</span>
      </div>

      <div className="parameter-group">
        <label>Electrification Rate (%)</label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.01"
          value={params.electrification_rate}
          onChange={(e) => handleParameterChange('electrification_rate', parseFloat(e.target.value))}
        />
        <span className="value-display">{(params.electrification_rate * 100).toFixed(1)}%</span>
      </div>

      <div className="parameter-group">
        <label>Efficiency Improvement (%)</label>
        <input
          type="range"
          min="0"
          max="0.2"
          step="0.01"
          value={params.efficiency_improvement}
          onChange={(e) => handleParameterChange('efficiency_improvement', parseFloat(e.target.value))}
        />
        <span className="value-display">{(params.efficiency_improvement * 100).toFixed(1)}%</span>
      </div>

      <div className="parameter-group">
        <label>Weather Assumption</label>
        <select
          value={params.weather_assumption}
          onChange={(e) => handleParameterChange('weather_assumption', e.target.value)}
        >
          <option value="cold">Cold (High HDD)</option>
          <option value="normal">Normal</option>
          <option value="warm">Warm (Low HDD)</option>
        </select>
      </div>

      <div className="button-group">
        <button className="btn btn-primary" onClick={handleRunForecast}>
          Run Forecast
        </button>
        <button className="btn btn-secondary" onClick={handleReset}>
          Reset to Defaults
        </button>
      </div>

      <div className="parameter-summary">
        <h3>Current Configuration</h3>
        <ul>
          <li><strong>Base Year:</strong> {params.base_year}</li>
          <li><strong>Horizon:</strong> {params.forecast_horizon} years</li>
          <li><strong>Housing Growth:</strong> {(params.housing_growth_rate * 100).toFixed(2)}% annually</li>
          <li><strong>Electrification:</strong> {(params.electrification_rate * 100).toFixed(1)}%</li>
          <li><strong>Efficiency Gain:</strong> {(params.efficiency_improvement * 100).toFixed(1)}%</li>
          <li><strong>Weather:</strong> {params.weather_assumption}</li>
        </ul>
      </div>
    </div>
  );
};

export default ParameterPanel;
