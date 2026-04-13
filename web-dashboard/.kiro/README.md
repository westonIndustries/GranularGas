# Web Dashboard - Kiro Configuration

This directory contains Kiro-specific configuration for the NW Natural Web Dashboard project.

## Structure

```
.kiro/
├── settings/
│   └── mcp.json              # MCP server configuration
├── steering/
│   ├── project-standards.md  # Project coding standards
│   └── development-guide.md  # Development workflow guide
├── specs/
│   └── web-dashboard/
│       ├── requirements.md   # Functional requirements
│       ├── design.md         # Technical design
│       └── tasks.md          # Implementation tasks
└── README.md                 # This file
```

## Quick Links

### Getting Started
- **Setup Guide**: See `../SETUP.md`
- **Project README**: See `../README.md`
- **Development Guide**: See `steering/development-guide.md`

### Specifications
- **Requirements**: See `specs/web-dashboard/requirements.md`
- **Design**: See `specs/web-dashboard/design.md`
- **Tasks**: See `specs/web-dashboard/tasks.md`

### Standards
- **Project Standards**: See `steering/project-standards.md`
- **Development Workflow**: See `steering/development-guide.md`

## Project Overview

Interactive web dashboard for the NW Natural end-use forecasting model with:
- Parameter adjustment interface ("knobs")
- Real-time forecast execution
- Multi-format result visualization
- Scenario management and comparison
- Data export capabilities

## Technology Stack

- React 18+
- Axios (HTTP client)
- Plotly.js (charting)
- CSS3 (styling)
- Create React App (build tool)

## Development Commands

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## Key Features

1. **Parameter Adjustment**
   - Housing growth rate
   - Electrification rate
   - Efficiency improvement
   - Weather assumption
   - Forecast horizon
   - Base year

2. **Results Visualization**
   - Summary metrics
   - Trend charts
   - Breakdown charts
   - Detailed tables

3. **Scenario Management**
   - Save scenarios
   - Load scenarios
   - Compare scenarios (up to 3)
   - Delete scenarios

4. **Data Export**
   - CSV export
   - JSON export
   - HTML reports

## API Integration

The dashboard communicates with the forecasting model API:

```
POST /api/forecast          - Run forecast
GET /api/scenarios          - Get saved scenarios
POST /api/scenarios         - Save scenario
GET /api/results/{id}       - Get results
DELETE /api/scenarios/{id}  - Delete scenario
GET /api/results/{id}/export/csv  - Export CSV
GET /api/results/{id}/export/json - Export JSON
```

## Configuration

Create `.env` file:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

## Project Status

**Phase**: Initial Setup ✅
- Project structure created
- Components scaffolded
- API client defined
- Styling framework in place
- Kiro configuration complete

**Next Phase**: Component Implementation
- Implement core components
- Integrate API calls
- Add chart visualizations
- Implement scenario management

## File Organization

```
web-dashboard/
├── .kiro/                    # Kiro configuration (this folder)
├── public/                   # Static assets
├── src/
│   ├── api/                 # API client
│   ├── components/          # React components
│   ├── styles/              # CSS stylesheets
│   ├── utils/               # Helper functions
│   └── index.js             # Entry point
├── package.json             # Dependencies
├── README.md                # Project documentation
└── SETUP.md                 # Setup instructions
```

## Useful Resources

- React Documentation: https://react.dev
- Plotly.js: https://plotly.com/javascript/
- Axios: https://axios-http.com/
- CSS Grid: https://css-tricks.com/snippets/css/complete-guide-grid/
- Flexbox: https://css-tricks.com/snippets/css/a-guide-to-flexbox/

## Support

For questions or issues:
1. Check the development guide: `steering/development-guide.md`
2. Review the design document: `specs/web-dashboard/design.md`
3. Check component docstrings in source code
4. Review browser console for errors

## Next Steps

1. Review requirements: `specs/web-dashboard/requirements.md`
2. Review design: `specs/web-dashboard/design.md`
3. Start implementing tasks from: `specs/web-dashboard/tasks.md`
4. Follow development guide: `steering/development-guide.md`

---

**Created**: April 10, 2026
**Status**: Ready for development
