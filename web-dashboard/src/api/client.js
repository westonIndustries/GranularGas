import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_KEY = process.env.REACT_APP_API_KEY;

const client = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    ...(API_KEY && { 'X-API-Key': API_KEY })
  }
});

/**
 * Run a forecast with the given parameters
 * @param {Object} params - Scenario parameters
 * @returns {Promise<Object>} Forecast results
 */
export const runForecast = async (params) => {
  try {
    const response = await client.post('/api/forecast', params);
    return response.data;
  } catch (error) {
    console.error('Forecast API error:', error);
    throw error;
  }
};

/**
 * Get list of saved scenarios
 * @returns {Promise<Array>} List of scenarios
 */
export const getSavedScenarios = async () => {
  try {
    const response = await client.get('/api/scenarios');
    return response.data;
  } catch (error) {
    console.error('Get scenarios API error:', error);
    throw error;
  }
};

/**
 * Save a scenario configuration
 * @param {Object} config - Scenario configuration
 * @returns {Promise<Object>} Saved scenario with ID
 */
export const saveScenario = async (config) => {
  try {
    const response = await client.post('/api/scenarios', config);
    return response.data;
  } catch (error) {
    console.error('Save scenario API error:', error);
    throw error;
  }
};

/**
 * Get detailed results for a scenario
 * @param {string} scenarioId - Scenario ID
 * @returns {Promise<Object>} Detailed results
 */
export const getResults = async (scenarioId) => {
  try {
    const response = await client.get(`/api/results/${scenarioId}`);
    return response.data;
  } catch (error) {
    console.error('Get results API error:', error);
    throw error;
  }
};

/**
 * Delete a saved scenario
 * @param {string} scenarioId - Scenario ID
 * @returns {Promise<void>}
 */
export const deleteScenario = async (scenarioId) => {
  try {
    await client.delete(`/api/scenarios/${scenarioId}`);
  } catch (error) {
    console.error('Delete scenario API error:', error);
    throw error;
  }
};

/**
 * Export results to CSV
 * @param {string} scenarioId - Scenario ID
 * @returns {Promise<Blob>} CSV file blob
 */
export const exportResultsCSV = async (scenarioId) => {
  try {
    const response = await client.get(`/api/results/${scenarioId}/export/csv`, {
      responseType: 'blob'
    });
    return response.data;
  } catch (error) {
    console.error('Export CSV API error:', error);
    throw error;
  }
};

/**
 * Export results to JSON
 * @param {string} scenarioId - Scenario ID
 * @returns {Promise<Blob>} JSON file blob
 */
export const exportResultsJSON = async (scenarioId) => {
  try {
    const response = await client.get(`/api/results/${scenarioId}/export/json`, {
      responseType: 'blob'
    });
    return response.data;
  } catch (error) {
    console.error('Export JSON API error:', error);
    throw error;
  }
};

export default client;
