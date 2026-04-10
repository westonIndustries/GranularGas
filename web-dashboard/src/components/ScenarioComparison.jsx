import React, { useState, useEffect } from 'react';
import { getSavedScenarios, deleteScenario } from '../api/client';

const ScenarioComparison = ({ scenarios, onScenariosUpdate }) => {
  const [loading, setLoading] = useState(false);
  const [selectedScenarios, setSelectedScenarios] = useState([]);

  useEffect(() => {
    loadScenarios();
  }, []);

  const loadScenarios = async () => {
    try {
      setLoading(true);
      const data = await getSavedScenarios();
      onScenariosUpdate(data);
    } catch (error) {
      console.error('Failed to load scenarios:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectScenario = (scenarioId) => {
    setSelectedScenarios(prev => {
      if (prev.includes(scenarioId)) {
        return prev.filter(id => id !== scenarioId);
      } else if (prev.length < 3) {
        return [...prev, scenarioId];
      }
      return prev;
    });
  };

  const handleDeleteScenario = async (scenarioId) => {
    try {
      await deleteScenario(scenarioId);
      loadScenarios();
    } catch (error) {
      console.error('Failed to delete scenario:', error);
    }
  };

  return (
    <div className="scenario-comparison">
      <h2>Scenario Comparison</h2>

      {loading ? (
        <p>Loading scenarios...</p>
      ) : scenarios.length === 0 ? (
        <p className="placeholder">No saved scenarios yet. Run a forecast to save a scenario.</p>
      ) : (
        <div className="comparison-content">
          <div className="scenarios-list">
            <h3>Available Scenarios</h3>
            <div className="scenarios-grid">
              {scenarios.map(scenario => (
                <div
                  key={scenario.id}
                  className={`scenario-card ${selectedScenarios.includes(scenario.id) ? 'selected' : ''}`}
                >
                  <input
                    type="checkbox"
                    checked={selectedScenarios.includes(scenario.id)}
                    onChange={() => handleSelectScenario(scenario.id)}
                    disabled={selectedScenarios.length >= 3 && !selectedScenarios.includes(scenario.id)}
                  />
                  <div className="scenario-info">
                    <h4>{scenario.name}</h4>
                    <p className="scenario-date">
                      {new Date(scenario.created_at).toLocaleDateString()}
                    </p>
                    <p className="scenario-params">
                      Growth: {(scenario.housing_growth_rate * 100).toFixed(2)}% | 
                      Electrification: {(scenario.electrification_rate * 100).toFixed(1)}%
                    </p>
                  </div>
                  <button
                    className="btn-delete"
                    onClick={() => handleDeleteScenario(scenario.id)}
                    title="Delete scenario"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          </div>

          {selectedScenarios.length > 0 && (
            <div className="comparison-results">
              <h3>Comparison ({selectedScenarios.length} scenarios selected)</h3>
              <p className="placeholder-text">
                Comparison charts and tables will be displayed here
              </p>
              <div className="comparison-placeholder">
                <p>Side-by-side comparison of:</p>
                <ul>
                  <li>Parameter differences</li>
                  <li>UPC trajectories</li>
                  <li>End-use composition</li>
                  <li>Demand by segment</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ScenarioComparison;
