# NW Natural End-Use Forecasting - Web Dashboard

Interactive web-based dashboard for testing and visualizing the NW Natural end-use forecasting model API.

## Overview

This is a separate web application that provides:
- Interactive parameter adjustment ("knobs") for model scenarios
- Real-time API calls to the forecasting model
- Dynamic visualization of results (graphs, charts, tables)
- Scenario comparison and export capabilities

## Project Structure

```
web-dashboard/
├── README.md                 # This file
├── package.json             # Node.js dependencies
├── .gitignore              # Git ignore rules
├── public/                 # Static assets
│   ├── index.html         # Main HTML entry point
│   └── favicon.ico        # Favicon
├── src/                    # Source code
│   ├── index.js           # Application entry point
│   ├── api/               # API client
│   │   └── client.js      # Forecasting model API client
│   ├── components/        # React components
│   │   ├── Dashboard.jsx  # Main dashboard component
│   │   ├── ParameterPanel.jsx  # Parameter adjustment UI
│   │   ├── ResultsPanel.jsx    # Results visualization
│   │   └── ScenarioComparison.jsx  # Multi-scenario comparison
│   ├── styles/            # CSS stylesheets
│   │   └── main.css       # Main styles
│   └── utils/             # Utility functions
│       ├── charts.js      # Chart generation helpers
│       └── export.js      # Export functionality
├── server/                # Backend server (optional)
│   └── server.js         # Express server for development
└── .env.example          # Environment variables template
```

## Getting Started

### Prerequisites
- Node.js 16+ and npm
- Access to the forecasting model API (running on localhost:8000 or configured endpoint)

### Installation

```bash
cd web-dashboard
npm install
```

### Development

```bash
npm start
```

This starts the development server at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## Features

### Parameter Adjustment Panel
- **Housing Growth Rate**: Adjust annual housing growth (0-5%)
- **Electrification Rate**: Set electrification adoption rate (0-100%)
- **Efficiency Improvement**: Adjust equipment efficiency gains (0-20%)
- **Weather Assumption**: Select weather scenario (normal, warm, cold)
- **Forecast Horizon**: Set projection years (1-30 years)
- **Base Year**: Select starting year for simulation

### Results Visualization
- **Line Charts**: UPC trends over time, end-use composition
- **Bar Charts**: Demand by segment, district, end-use
- **Stacked Area**: End-use contribution to total demand
- **Heatmaps**: Segment × Market cross-tabulation
- **Tables**: Detailed results by aggregation level

### Scenario Management
- Save and load scenarios
- Compare multiple scenarios side-by-side
- Export results to CSV/JSON
- Share scenario configurations

## API Integration

The dashboard communicates with the forecasting model API via REST endpoints:

```
POST /api/forecast
  - Input: scenario parameters
  - Output: forecast results

GET /api/scenarios
  - Output: list of saved scenarios

POST /api/scenarios
  - Input: scenario configuration
  - Output: saved scenario ID

GET /api/results/{scenario_id}
  - Output: detailed results for scenario
```

## Configuration

Create a `.env` file in the `web-dashboard` directory:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_KEY=your-api-key-here
REACT_APP_ENVIRONMENT=development
```

## Technology Stack

- **Frontend**: React 18+
- **Charting**: Plotly.js or Chart.js
- **Styling**: CSS3 with responsive design
- **HTTP Client**: Axios or Fetch API
- **Build Tool**: Create React App or Vite
- **Backend** (optional): Express.js for development server

## Development Workflow

1. Adjust parameters in the Parameter Panel
2. Click "Run Forecast" to call the API
3. View results in the Results Panel
4. Compare with other scenarios if needed
5. Export results for further analysis

## File Structure Details

### `src/api/client.js`
Handles all API communication with the forecasting model:
- `runForecast(params)` - Execute forecast with given parameters
- `getSavedScenarios()` - Retrieve saved scenarios
- `saveScenario(config)` - Save a scenario configuration
- `getResults(scenarioId)` - Fetch detailed results

### `src/components/ParameterPanel.jsx`
Interactive UI for adjusting model parameters:
- Sliders for continuous parameters
- Dropdowns for categorical parameters
- Input validation and constraints
- Reset to defaults button

### `src/components/ResultsPanel.jsx`
Displays forecast results:
- Multiple chart types
- Tabular data views
- Summary statistics
- Export options

### `src/components/ScenarioComparison.jsx`
Compare multiple scenarios:
- Side-by-side parameter comparison
- Overlaid result charts
- Difference analysis
- Sensitivity analysis

## Next Steps

1. Set up the basic React application structure
2. Implement the API client
3. Create the parameter adjustment UI
4. Add result visualization components
5. Integrate with the forecasting model API
6. Add scenario management features
7. Deploy to production environment

## Notes

- This is a separate project from the forecasting model itself
- It can be developed and deployed independently
- The API endpoint should be configured based on your deployment
- Consider adding authentication if exposing the API publicly

## Support

For issues or questions about the web dashboard, refer to:
- API documentation in the main forecasting model project
- React documentation: https://react.dev
- Plotly.js documentation: https://plotly.com/javascript/

---

**Created**: April 10, 2026
**Status**: Project structure template - ready for implementation
