# Web Dashboard Setup Guide

## Quick Start

### 1. Prerequisites
- Node.js 16+ installed
- npm or yarn package manager
- The forecasting model API running (or configured endpoint)

### 2. Installation

```bash
# Navigate to the web-dashboard directory
cd web-dashboard

# Install dependencies
npm install
```

### 3. Configuration

Create a `.env` file in the `web-dashboard` directory:

```bash
cp .env.example .env
```

Edit `.env` and set the API endpoint:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

### 4. Start Development Server

```bash
npm start
```

The dashboard will open at `http://localhost:3000`

## Project Structure

```
web-dashboard/
├── public/              # Static files
├── src/
│   ├── api/            # API client
│   ├── components/     # React components
│   ├── styles/         # CSS stylesheets
│   └── index.js        # Entry point
├── package.json        # Dependencies
└── README.md          # Documentation
```

## Available Scripts

### Development
```bash
npm start
```
Runs the app in development mode with hot reload.

### Build
```bash
npm run build
```
Creates an optimized production build.

### Test
```bash
npm test
```
Runs the test suite.

## Component Overview

### Dashboard.jsx
Main container component that manages:
- Tab navigation (Forecast vs Scenario Comparison)
- Error and loading states
- Communication between panels

### ParameterPanel.jsx
Interactive parameter adjustment UI with:
- Sliders for continuous parameters
- Dropdowns for categorical parameters
- Real-time value display
- Reset to defaults button

### ResultsPanel.jsx
Results visualization with:
- Summary metrics cards
- Multiple chart views (Summary, Trends, Breakdown, Details)
- Export functionality (CSV, JSON)
- Tabular data display

### ScenarioComparison.jsx
Scenario management and comparison:
- List of saved scenarios
- Multi-select for comparison (up to 3)
- Delete scenario functionality
- Comparison visualization placeholder

## API Integration

The dashboard expects the forecasting model API to provide these endpoints:

### POST /api/forecast
Run a forecast with given parameters.

**Request:**
```json
{
  "base_year": 2025,
  "forecast_horizon": 10,
  "housing_growth_rate": 0.01,
  "electrification_rate": 0.05,
  "efficiency_improvement": 0.02,
  "weather_assumption": "normal"
}
```

**Response:**
```json
{
  "scenario_id": "abc123",
  "base_year": 2025,
  "forecast_horizon": 10,
  "total_demand_2035": 1500000,
  "upc_2035": 750,
  "demand_change_pct": -5.2,
  "electrification_impact": -8.5,
  "total_premises": 2000,
  "total_equipment": 5000
}
```

### GET /api/scenarios
Get list of saved scenarios.

**Response:**
```json
[
  {
    "id": "scenario1",
    "name": "High Electrification",
    "created_at": "2026-04-10T12:00:00Z",
    "housing_growth_rate": 0.01,
    "electrification_rate": 0.15,
    "efficiency_improvement": 0.02,
    "weather_assumption": "normal"
  }
]
```

### POST /api/scenarios
Save a scenario configuration.

### GET /api/results/{scenario_id}
Get detailed results for a scenario.

### GET /api/results/{scenario_id}/export/csv
Export results as CSV.

### GET /api/results/{scenario_id}/export/json
Export results as JSON.

## Customization

### Adding New Parameters

1. Add to `ParameterPanel.jsx` state:
```jsx
const [params, setParams] = useState({
  // ... existing params
  new_param: default_value
});
```

2. Add UI control:
```jsx
<div className="parameter-group">
  <label>New Parameter</label>
  <input
    type="range"
    min="0"
    max="100"
    value={params.new_param}
    onChange={(e) => handleParameterChange('new_param', parseFloat(e.target.value))}
  />
</div>
```

### Adding New Charts

1. Create chart component in `src/components/`
2. Import in `ResultsPanel.jsx`
3. Add tab button and render logic

### Styling

All styles are in `src/styles/main.css`. The design uses:
- CSS Grid for layouts
- Flexbox for component alignment
- CSS variables for theming (can be added)
- Responsive breakpoints at 1024px and 768px

## Deployment

### Build for Production
```bash
npm run build
```

This creates an optimized build in the `build/` directory.

### Deploy to Server
```bash
# Copy build directory to your web server
scp -r build/* user@server:/var/www/dashboard/
```

### Environment Variables for Production
```env
REACT_APP_API_URL=https://api.example.com
REACT_APP_ENVIRONMENT=production
```

## Troubleshooting

### API Connection Issues
- Verify API URL in `.env`
- Check CORS settings on API server
- Ensure API is running and accessible

### Build Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use
```bash
# Use different port
PORT=3001 npm start
```

## Next Steps

1. Implement actual chart visualizations (Plotly.js or Chart.js)
2. Add scenario comparison logic
3. Implement data export functionality
4. Add user authentication if needed
5. Deploy to production environment

## Support

For issues or questions:
1. Check the API documentation
2. Review React documentation: https://react.dev
3. Check browser console for errors
4. Verify API endpoint configuration

---

**Last Updated**: April 10, 2026
