# Web Dashboard Development Guide

## Getting Started

### First Time Setup
```bash
cd web-dashboard
npm install
cp .env.example .env
# Edit .env with your API endpoint
npm start
```

### Daily Development
```bash
npm start
```

This starts the dev server at `http://localhost:3000` with hot reload.

## Project Structure

```
web-dashboard/
├── .kiro/                    # Kiro configuration
├── public/                   # Static assets
│   └── index.html           # HTML entry point
├── src/
│   ├── api/
│   │   └── client.js        # API communication
│   ├── components/
│   │   ├── Dashboard.jsx    # Main container
│   │   ├── ParameterPanel.jsx
│   │   ├── ResultsPanel.jsx
│   │   └── ScenarioComparison.jsx
│   ├── styles/
│   │   └── main.css         # All styles
│   ├── utils/               # Helper functions (future)
│   └── index.js             # React entry point
├── package.json
├── README.md
└── SETUP.md
```

## Component Development

### Creating a New Component

1. **Create file** in `src/components/`:
```jsx
import React from 'react';

const MyComponent = ({ prop1, prop2 }) => {
  return (
    <div className="my-component">
      {/* Component content */}
    </div>
  );
};

export default MyComponent;
```

2. **Add styles** to `src/styles/main.css`:
```css
.my-component {
  /* styles */
}
```

3. **Import and use** in parent component:
```jsx
import MyComponent from './MyComponent';

// In JSX
<MyComponent prop1="value" prop2={data} />
```

### Component Props Pattern

```jsx
const MyComponent = ({
  data,           // Required data
  onAction,       // Callback function
  isLoading,      // Boolean state
  className       // Optional CSS class
}) => {
  // Component logic
};
```

## API Integration

### Making API Calls

```jsx
import { runForecast } from '../api/client';

const handleForecast = async () => {
  try {
    setLoading(true);
    const results = await runForecast(params);
    setResults(results);
  } catch (error) {
    setError(error.message);
  } finally {
    setLoading(false);
  }
};
```

### Adding New API Endpoints

1. **Add to** `src/api/client.js`:
```javascript
export const newEndpoint = async (params) => {
  try {
    const response = await client.post('/api/new-endpoint', params);
    return response.data;
  } catch (error) {
    console.error('API error:', error);
    throw error;
  }
};
```

2. **Use in component**:
```jsx
import { newEndpoint } from '../api/client';

const result = await newEndpoint(data);
```

## Styling

### CSS Organization

- Global styles at top of `main.css`
- Component styles grouped by component
- Responsive breakpoints at bottom

### Color Scheme

- Primary: `#667eea` (purple)
- Secondary: `#764ba2` (dark purple)
- Background: `#f5f5f5` (light gray)
- Text: `#333` (dark gray)
- Borders: `#ddd` (light gray)

### Responsive Design

```css
/* Desktop first */
.component {
  display: grid;
  grid-template-columns: 1fr 2fr;
}

/* Tablet */
@media (max-width: 1024px) {
  .component {
    grid-template-columns: 1fr;
  }
}

/* Mobile */
@media (max-width: 768px) {
  .component {
    padding: 1rem;
  }
}
```

## State Management

### Using Hooks

```jsx
import React, { useState, useEffect } from 'react';

const MyComponent = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Side effects
  }, [dependencies]);

  return (
    // JSX
  );
};
```

### Lifting State Up

When multiple components need shared state:

```jsx
// In parent component
const [sharedState, setSharedState] = useState(initialValue);

// Pass to children
<Child1 value={sharedState} onChange={setSharedState} />
<Child2 value={sharedState} />
```

## Common Patterns

### Loading State

```jsx
{loading ? (
  <div className="loading-banner">Loading...</div>
) : (
  <div>{content}</div>
)}
```

### Error Handling

```jsx
{error && (
  <div className="error-banner">
    <strong>Error:</strong> {error}
  </div>
)}
```

### Conditional Rendering

```jsx
{results && (
  <ResultsPanel results={results} />
)}

{!results && (
  <div className="placeholder">No results yet</div>
)}
```

## Testing

### Run Tests
```bash
npm test
```

### Test Structure
```jsx
import { render, screen } from '@testing-library/react';
import MyComponent from './MyComponent';

test('renders component', () => {
  render(<MyComponent />);
  expect(screen.getByText('Expected text')).toBeInTheDocument();
});
```

## Building & Deployment

### Development Build
```bash
npm start
```

### Production Build
```bash
npm run build
```

Creates optimized build in `build/` directory.

### Test Production Build Locally
```bash
npx serve -s build
```

## Debugging

### Browser DevTools
- React DevTools extension
- Network tab for API calls
- Console for errors

### Console Logging
```jsx
console.log('Debug info:', variable);
console.error('Error:', error);
```

### Common Issues

**API Connection Failed**
- Check `.env` API_URL
- Verify API is running
- Check CORS settings

**Styles Not Applying**
- Clear browser cache
- Check CSS class names match
- Verify CSS is imported

**Component Not Rendering**
- Check console for errors
- Verify props are passed correctly
- Check conditional rendering logic

## Performance Tips

1. **Memoize expensive computations**:
```jsx
const memoizedValue = useMemo(() => expensiveFunction(a, b), [a, b]);
```

2. **Lazy load components**:
```jsx
const LazyComponent = React.lazy(() => import('./LazyComponent'));
```

3. **Optimize re-renders**:
```jsx
const MyComponent = React.memo(({ data }) => {
  // Component only re-renders if data changes
});
```

## Next Steps

1. Integrate Plotly.js for charts
2. Implement scenario comparison logic
3. Add data export functionality
4. Set up authentication if needed
5. Deploy to production

## Resources

- React: https://react.dev
- Plotly.js: https://plotly.com/javascript/
- MDN Web Docs: https://developer.mozilla.org/
- CSS Tricks: https://css-tricks.com/

## Questions?

Check:
1. Component docstrings
2. README.md
3. SETUP.md
4. Browser console for errors
