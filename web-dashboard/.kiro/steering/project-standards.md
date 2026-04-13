# Web Dashboard Project Standards

## Project Overview

This is a React-based web dashboard for the NW Natural End-Use Forecasting Model. It provides an interactive interface for adjusting model parameters and visualizing forecast results.

## Technology Stack

- **Frontend Framework**: React 18+
- **HTTP Client**: Axios
- **Charting**: Plotly.js (to be integrated)
- **Styling**: CSS3 with responsive design
- **Build Tool**: Create React App
- **Package Manager**: npm

## Code Organization

```
src/
├── api/              # API communication
├── components/       # React components
├── styles/          # CSS stylesheets
└── utils/           # Helper functions
```

## Component Structure

### Container Components
- `Dashboard.jsx` - Main app container, manages state and routing

### Presentational Components
- `ParameterPanel.jsx` - Parameter adjustment UI
- `ResultsPanel.jsx` - Results visualization
- `ScenarioComparison.jsx` - Scenario management

## Naming Conventions

- **Components**: PascalCase (e.g., `Dashboard.jsx`)
- **Functions**: camelCase (e.g., `handleForecastComplete`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_URL`)
- **CSS Classes**: kebab-case (e.g., `.parameter-panel`)

## Development Workflow

1. Create feature branch: `git checkout -b feature/feature-name`
2. Make changes following code standards
3. Test locally: `npm start`
4. Build for production: `npm run build`
5. Commit with clear messages
6. Push and create pull request

## API Integration

All API calls go through `src/api/client.js`:

```javascript
import { runForecast, getSavedScenarios } from '../api/client';

// Use in components
const results = await runForecast(params);
```

## Styling Guidelines

- Use CSS Grid for layouts
- Use Flexbox for component alignment
- Mobile-first responsive design
- Breakpoints: 768px (tablet), 1024px (desktop)
- Color scheme: Purple gradient (#667eea to #764ba2)

## State Management

Currently using React hooks (useState). For complex state, consider:
- Context API
- Redux
- Zustand

## Error Handling

- Wrap API calls in try-catch
- Display user-friendly error messages
- Log errors to console for debugging
- Show loading states during async operations

## Performance Considerations

- Lazy load components if needed
- Memoize expensive computations
- Optimize re-renders with React.memo
- Use production build for deployment

## Testing

```bash
npm test
```

Write tests for:
- Component rendering
- User interactions
- API calls (mocked)
- State changes

## Deployment

1. Build: `npm run build`
2. Test build locally: `npx serve -s build`
3. Deploy `build/` directory to web server
4. Set environment variables on server

## Environment Variables

Required:
- `REACT_APP_API_URL` - Forecasting model API endpoint

Optional:
- `REACT_APP_ENVIRONMENT` - development/production
- `REACT_APP_API_KEY` - API authentication key

## Common Tasks

### Add New Parameter
1. Add to state in `ParameterPanel.jsx`
2. Add UI control (slider, input, dropdown)
3. Update parameter summary display

### Add New Chart
1. Create component in `src/components/`
2. Import Plotly or Chart.js
3. Add to `ResultsPanel.jsx`
4. Add tab button for navigation

### Update Styling
1. Edit `src/styles/main.css`
2. Use existing color scheme and spacing
3. Test responsive design at breakpoints

## Resources

- React Docs: https://react.dev
- Plotly.js: https://plotly.com/javascript/
- CSS Grid: https://css-tricks.com/snippets/css/complete-guide-grid/
- Flexbox: https://css-tricks.com/snippets/css/a-guide-to-flexbox/

## Questions?

Refer to:
- `README.md` - Project overview
- `SETUP.md` - Installation guide
- Component docstrings - Implementation details
