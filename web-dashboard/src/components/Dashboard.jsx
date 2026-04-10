import React, { useState } from 'react';
import ParameterPanel from './ParameterPanel';
import ResultsPanel from './ResultsPanel';
import ScenarioComparison from './ScenarioComparison';
import '../styles/main.css';

const Dashboard = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('forecast');
  const [scenarios, setScenarios] = useState([]);

  const handleForecastComplete = (forecastResults) => {
    setResults(forecastResults);
    setError(null);
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
  };

  const handleLoadingChange = (isLoading) => {
    setLoading(isLoading);
  };

  const handleScenariosUpdate = (updatedScenarios) => {
    setScenarios(updatedScenarios);
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>NW Natural End-Use Forecasting Dashboard</h1>
        <p>Interactive model testing and scenario analysis</p>
      </header>

      <div className="dashboard-tabs">
        <button
          className={`tab-button ${activeTab === 'forecast' ? 'active' : ''}`}
          onClick={() => setActiveTab('forecast')}
        >
          Forecast
        </button>
        <button
          className={`tab-button ${activeTab === 'comparison' ? 'active' : ''}`}
          onClick={() => setActiveTab('comparison')}
        >
          Scenario Comparison
        </button>
      </div>

      {error && (
        <div className="error-banner">
          <strong>Error:</strong> {error}
        </div>
      )}

      {loading && (
        <div className="loading-banner">
          Running forecast... Please wait.
        </div>
      )}

      <div className="dashboard-content">
        {activeTab === 'forecast' && (
          <div className="forecast-view">
            <div className="parameter-section">
              <ParameterPanel
                onForecastComplete={handleForecastComplete}
                onError={handleError}
                onLoadingChange={handleLoadingChange}
                onScenariosUpdate={handleScenariosUpdate}
              />
            </div>
            <div className="results-section">
              {results ? (
                <ResultsPanel results={results} />
              ) : (
                <div className="placeholder">
                  <p>Adjust parameters and click "Run Forecast" to see results</p>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'comparison' && (
          <ScenarioComparison
            scenarios={scenarios}
            onScenariosUpdate={handleScenariosUpdate}
          />
        )}
      </div>

      <footer className="dashboard-footer">
        <p>NW Natural End-Use Forecasting Model v0.1.0</p>
      </footer>
    </div>
  );
};

export default Dashboard;
