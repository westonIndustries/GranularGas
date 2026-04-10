# Web Dashboard Requirements

## Project Overview

Interactive web-based dashboard for testing and visualizing the NW Natural end-use forecasting model. Users can adjust model parameters ("knobs") and see results in real-time through graphs, charts, and tables.

## Functional Requirements

### 1. Parameter Adjustment Interface

**1.1 Parameter Controls**
- Housing growth rate (0-5% annually) - slider
- Electrification rate (0-100%) - slider
- Efficiency improvement (0-20%) - slider
- Weather assumption (cold/normal/warm) - dropdown
- Forecast horizon (1-30 years) - slider
- Base year (2020-2030) - number input
- Scenario name (optional) - text input

**1.2 Parameter Display**
- Real-time value display for each parameter
- Current configuration summary
- Reset to defaults button
- Run Forecast button

### 2. Results Visualization

**2.1 Summary View**
- Total demand (therms)
- Use per customer (UPC)
- Demand change (%)
- Electrification impact (%)
- Displayed as metric cards

**2.2 Trends View**
- UPC trajectory over forecast period (line chart)
- End-use composition over time (stacked area)
- Segment distribution trends

**2.3 Breakdown View**
- Demand by segment (bar chart)
- Demand by district (bar chart)
- Demand by end-use (stacked bar)
- Equipment distribution

**2.4 Details View**
- Tabular results data
- Detailed statistics
- Downloadable data

### 3. Scenario Management

**3.1 Save Scenarios**
- Save forecast results with custom name
- Store scenario parameters
- Timestamp each scenario

**3.2 Load Scenarios**
- List all saved scenarios
- Display scenario parameters
- Show creation date

**3.3 Compare Scenarios**
- Select up to 3 scenarios for comparison
- Side-by-side parameter comparison
- Overlaid result charts
- Difference analysis

**3.4 Delete Scenarios**
- Remove saved scenarios
- Confirm before deletion

### 4. Run History

**4.1 View Run History**
- Display all forecast runs in paginated table
- Show timestamp, scenario name, duration, key results
- Sort by date, duration, demand, UPC
- Search by scenario name or parameters
- Filter by date range and parameter ranges

**4.2 Load Previous Run**
- Click "Load" to restore parameters and results
- Switch to Forecast tab with loaded data
- Allows re-running with same or modified parameters

**4.3 Compare Historical Runs**
- Select up to 3 runs from history
- Compare parameters side-by-side
- Compare results with overlaid charts
- Show differences between runs

**4.4 Delete Run**
- Remove run from history
- Confirm before deletion
- Bulk delete multiple runs

### 5. Data Export

**5.1 Export Formats**
- CSV export for spreadsheet analysis
- JSON export for programmatic use
- HTML report generation

**5.2 Export Content**
- All forecast results
- Parameter configuration
- Metadata (date, version)

### 6. User Interface

**6.1 Layout**
- Header with title and description
- Tab navigation (Forecast / Scenario Comparison / Run History)
- Two-column layout (parameters left, results right)
- Responsive design for mobile/tablet

**6.2 Navigation**
- Tab-based view switching
- Chart type selection within results
- Scenario list navigation
- Run history table navigation

**6.3 Feedback**
- Loading indicators during API calls
- Error messages for failures
- Success confirmations for actions

## Non-Functional Requirements

### 1. Performance
- API response time < 5 seconds
- Dashboard loads in < 2 seconds
- Smooth chart rendering
- No lag on parameter adjustment

### 2. Reliability
- Graceful error handling
- Retry logic for failed API calls
- Data persistence for saved scenarios
- Session recovery

### 3. Usability
- Intuitive parameter controls
- Clear result visualization
- Responsive design (mobile, tablet, desktop)
- Accessibility (WCAG 2.1 AA)

### 4. Security
- HTTPS for production
- API key authentication (if required)
- Input validation
- XSS protection

### 5. Maintainability
- Clean, documented code
- Component-based architecture
- Consistent naming conventions
- Comprehensive comments

## Technical Requirements

### 1. Frontend Stack
- React 18+
- Axios for HTTP requests
- Plotly.js for charting
- CSS3 for styling
- Create React App for build

### 2. API Integration
- REST API communication
- JSON request/response format
- Error handling and retries
- Timeout management

### 3. Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

### 4. Deployment
- Static file hosting
- Environment variable configuration
- Build optimization
- CDN support

## User Stories

### Story 1: Run a Forecast
As a user, I want to adjust model parameters and run a forecast so I can see how different scenarios affect demand.

**Acceptance Criteria:**
- I can adjust all parameters with sliders and inputs
- I can see current values displayed
- I can click "Run Forecast" to execute
- Results appear in < 5 seconds
- I see loading indicator during execution

### Story 2: Visualize Results
As a user, I want to see forecast results in multiple chart formats so I can understand the data from different perspectives.

**Acceptance Criteria:**
- Summary view shows key metrics
- Trends view shows UPC trajectory
- Breakdown view shows demand by segment
- Details view shows tabular data
- I can switch between views easily

### Story 3: Compare Scenarios
As a user, I want to save and compare multiple scenarios so I can evaluate different strategies.

**Acceptance Criteria:**
- I can save a forecast with a custom name
- I can see list of saved scenarios
- I can select up to 3 scenarios for comparison
- Comparison shows parameter differences
- Comparison shows result differences

### Story 4: Export Results
As a user, I want to export results to CSV/JSON so I can analyze data in other tools.

**Acceptance Criteria:**
- Export button is visible in results panel
- CSV export downloads correctly
- JSON export downloads correctly
- Exported data includes all results
- File naming is clear and descriptive

### Story 5: View and Load Previous Runs
As a user, I want to see all my previous forecast runs and load one to view or modify it.

**Acceptance Criteria:**
- I can see a paginated list of all my forecast runs
- I can search and filter runs by date and parameters
- I can sort runs by date, duration, or results
- I can click "Load" to restore a previous run's parameters and results
- I can compare up to 3 runs side-by-side
- I can delete runs from my history

## Constraints

1. **API Dependency**: Dashboard requires forecasting model API to be running
2. **Data Freshness**: Results depend on current model implementation
3. **Browser Compatibility**: Limited to modern browsers with ES6 support
4. **Performance**: Large datasets may impact chart rendering

## Success Criteria

- ✅ All parameters adjustable with real-time feedback
- ✅ Results visualized in 4+ chart formats
- ✅ Scenarios can be saved and compared
- ✅ Data exportable to CSV and JSON
- ✅ Responsive design works on mobile/tablet/desktop
- ✅ API integration complete and tested
- ✅ Error handling for all failure scenarios
- ✅ Documentation complete and clear

## Future Enhancements

1. Advanced charting (heatmaps, 3D visualizations)
2. Sensitivity analysis
3. Batch scenario execution
4. User authentication and saved workspaces
5. Real-time collaboration
6. Mobile app version
7. API caching for performance
8. Advanced filtering and drill-down
