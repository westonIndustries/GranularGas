# API Documentation

## Overview

The NW Natural End-Use Forecasting Model provides a REST API for scenario management, execution, and results retrieval. This document describes all available endpoints, request/response formats, and usage examples.

**Base URL**: `http://localhost:8000/api/v1` (local development) or `https://api.nwnatural-forecast.example.com/api/v1` (production)

**API Version**: v1

**Authentication**: Optional JWT tokens for multi-user environments

---

## Quick Start

### 1. Create a Scenario

```bash
curl -X POST http://localhost:8000/api/v1/scenarios \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aggressive Electrification 2030",
    "description": "High heat pump adoption with policy incentives",
    "base_year": 2025,
    "forecast_horizon": 10,
    "housing_growth_rate": 0.015,
    "electrification_rates": {
      "space_heating": 0.08,
      "water_heating": 0.12,
      "cooking": 0.02
    },
    "efficiency_improvements": {
      "space_heating": 0.02,
      "water_heating": 0.015,
      "cooking": 0.01
    },
    "weather_assumption": "normal"
  }'
```

**Response**:
```json
{
  "scenario_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Aggressive Electrification 2030",
  "created_at": "2025-03-25T10:30:00Z",
  "status": "created",
  "validation_errors": []
}
```

### 2. Run the Scenario

```bash
curl -X POST http://localhost:8000/api/v1/scenarios/550e8400-e29b-41d4-a716-446655440000/run \
  -H "Content-Type: application/json"
```

**Response** (async mode):
```json
{
  "scenario_id": "550e8400-e29b-41d4-a716-446655440000",
  "run_id": "run-5678",
  "status": "queued",
  "queue_position": 3,
  "estimated_wait_seconds": 120
}
```

### 3. Check Status

```bash
curl http://localhost:8000/api/v1/runs/run-5678
```

**Response**:
```json
{
  "run_id": "run-5678",
  "scenario_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": {
    "current_step": "aggregation",
    "step_progress": 1.0,
    "overall_progress": 1.0,
    "estimated_time_remaining_seconds": 0
  },
  "started_at": "2025-03-25T10:30:00Z",
  "execution_time_seconds": 300
}
```

### 4. Get Results

```bash
curl "http://localhost:8000/api/v1/runs/run-5678/results?level=county&format=json"
```

**Response**:
```json
{
  "run_id": "run-5678",
  "scenario_id": "550e8400-e29b-41d4-a716-446655440000",
  "level": "county",
  "format": "json",
  "data": [
    {
      "year": 2025,
      "area_id": "41051",
      "area_name": "Multnomah County",
      "total_therms": 125000000,
      "upc": 650,
      "customer_count": 192000,
      "end_uses": {
        "space_heating": 75000000,
        "water_heating": 30000000,
        "cooking": 5760000,
        "drying": 3840000,
        "fireplace": 10560000,
        "other": 1920000
      },
      "electrification_rate": 0.15,
      "heat_pump_penetration": 0.12,
      "avg_efficiency": 0.88
    }
  ]
}
```

---

## API Endpoints

### Scenario Management

#### Create Scenario

```
POST /scenarios
```

Creates a new scenario configuration.

**Request Body**:
```json
{
  "name": "string (required, 1-200 chars)",
  "description": "string (optional)",
  "base_year": "integer (2020-2030, default: 2025)",
  "forecast_horizon": "integer (5-50, default: 10)",
  "housing_growth_rate": "float (0.0-0.05, default: 0.012)",
  "electrification_rates": {
    "space_heating": "float (0.0-1.0)",
    "water_heating": "float (0.0-1.0)",
    "cooking": "float (0.0-1.0)"
  },
  "efficiency_improvements": {
    "space_heating": "float (0.0-0.1)",
    "water_heating": "float (0.0-0.1)",
    "cooking": "float (0.0-0.1)"
  },
  "weather_assumption": "string (normal|warm|cold, default: normal)",
  "heat_pump_cop": {
    "ashp_baseline": "float (2.0-4.0, default: 3.0)",
    "gshp_baseline": "float (3.0-5.0, default: 4.0)",
    "gorge_penalty": "float (0.7-1.0, default: 0.85)"
  }
}
```

**Response** (201 Created):
```json
{
  "scenario_id": "uuid",
  "name": "string",
  "created_at": "ISO 8601 timestamp",
  "status": "created",
  "validation_errors": ["array of strings"]
}
```

**Error Responses**:
- `400 Bad Request`: Invalid parameters
- `422 Unprocessable Entity`: Validation failed

---

#### List Scenarios

```
GET /scenarios
```

Lists all scenarios with optional filtering.

**Query Parameters**:
- `limit` (integer, default: 10, max: 100) — Number of results to return
- `offset` (integer, default: 0) — Number of results to skip
- `status` (string) — Filter by status: `created`, `running`, `completed`, `failed`
- `name` (string) — Filter by name (partial match)

**Response** (200 OK):
```json
{
  "scenarios": [
    {
      "scenario_id": "uuid",
      "name": "string",
      "status": "string",
      "created_at": "ISO 8601 timestamp",
      "completed_at": "ISO 8601 timestamp or null",
      "execution_time_seconds": "integer or null"
    }
  ],
  "total": "integer",
  "limit": "integer",
  "offset": "integer"
}
```

---

#### Get Scenario Details

```
GET /scenarios/{scenario_id}
```

Gets detailed information about a specific scenario.

**Path Parameters**:
- `scenario_id` (string, required) — Scenario UUID

**Response** (200 OK):
```json
{
  "scenario_id": "uuid",
  "name": "string",
  "description": "string or null",
  "base_year": "integer",
  "forecast_horizon": "integer",
  "housing_growth_rate": "float",
  "electrification_rates": "object",
  "efficiency_improvements": "object",
  "weather_assumption": "string",
  "status": "string",
  "created_at": "ISO 8601 timestamp",
  "completed_at": "ISO 8601 timestamp or null",
  "execution_time_seconds": "integer or null",
  "validation_errors": ["array of strings"],
  "validation_warnings": ["array of strings"]
}
```

**Error Responses**:
- `404 Not Found`: Scenario does not exist

---

#### Update Scenario

```
PUT /scenarios/{scenario_id}
```

Updates a scenario configuration (only if not running or completed).

**Path Parameters**:
- `scenario_id` (string, required) — Scenario UUID

**Request Body**: Same as Create Scenario (all fields optional)

**Response** (200 OK): Updated scenario object

**Error Responses**:
- `404 Not Found`: Scenario does not exist
- `409 Conflict`: Scenario is running or completed

---

#### Delete Scenario

```
DELETE /scenarios/{scenario_id}
```

Deletes a scenario and associated results.

**Path Parameters**:
- `scenario_id` (string, required) — Scenario UUID

**Response** (204 No Content)

**Error Responses**:
- `404 Not Found`: Scenario does not exist

---

#### Validate Scenario

```
POST /scenarios/{scenario_id}/validate
```

Validates scenario configuration without running.

**Path Parameters**:
- `scenario_id` (string, required) — Scenario UUID

**Response** (200 OK):
```json
{
  "scenario_id": "uuid",
  "is_valid": "boolean",
  "errors": ["array of strings"],
  "warnings": ["array of strings"]
}
```

---

### Scenario Execution

#### Run Scenario

```
POST /scenarios/{scenario_id}/run
```

Submits scenario for execution.

**Path Parameters**:
- `scenario_id` (string, required) — Scenario UUID

**Query Parameters**:
- `async` (boolean, default: true) — Run asynchronously (true) or wait for completion (false)

**Response** (202 Accepted for async, 200 OK for sync):

Async response:
```json
{
  "scenario_id": "uuid",
  "run_id": "string",
  "status": "queued",
  "queue_position": "integer",
  "estimated_wait_seconds": "integer"
}
```

Sync response:
```json
{
  "scenario_id": "uuid",
  "run_id": "string",
  "status": "completed",
  "execution_time_seconds": "integer",
  "results_url": "/api/v1/runs/{run_id}/results"
}
```

**Error Responses**:
- `404 Not Found`: Scenario does not exist
- `400 Bad Request`: Scenario validation failed

---

#### Get Run Status

```
GET /runs/{run_id}
```

Gets execution status and progress.

**Path Parameters**:
- `run_id` (string, required) — Run ID

**Response** (200 OK):
```json
{
  "run_id": "string",
  "scenario_id": "uuid",
  "status": "queued|running|completed|failed|cancelled",
  "progress": {
    "current_step": "string",
    "step_progress": "float (0.0-1.0)",
    "overall_progress": "float (0.0-1.0)",
    "estimated_time_remaining_seconds": "integer"
  },
  "started_at": "ISO 8601 timestamp or null",
  "completed_at": "ISO 8601 timestamp or null",
  "execution_time_seconds": "integer or null",
  "error_message": "string or null"
}
```

**Error Responses**:
- `404 Not Found`: Run does not exist

---

#### Cancel Run

```
POST /runs/{run_id}/cancel
```

Cancels a running scenario.

**Path Parameters**:
- `run_id` (string, required) — Run ID

**Response** (200 OK):
```json
{
  "run_id": "string",
  "status": "cancelled",
  "cancelled_at": "ISO 8601 timestamp"
}
```

**Error Responses**:
- `404 Not Found`: Run does not exist
- `409 Conflict`: Run is not running

---

### Results Retrieval

#### Get Results

```
GET /runs/{run_id}/results
```

Gets aggregated results for a completed run.

**Path Parameters**:
- `run_id` (string, required) — Run ID

**Query Parameters**:
- `level` (string, default: county) — Aggregation level: `county`, `district`, `microclimate`, `microresidential`, `microadoption`, `composite-cell`
- `format` (string, default: json) — Response format: `json`, `csv`, `parquet`
- `year` (integer, optional) — Filter to single year

**Response** (200 OK):
```json
{
  "run_id": "string",
  "scenario_id": "uuid",
  "level": "string",
  "format": "string",
  "data": [
    {
      "year": "integer",
      "area_id": "string",
      "area_name": "string",
      "total_therms": "float",
      "upc": "float",
      "customer_count": "integer",
      "end_uses": {
        "space_heating": "float",
        "water_heating": "float",
        "cooking": "float",
        "drying": "float",
        "fireplace": "float",
        "other": "float"
      },
      "electrification_rate": "float",
      "heat_pump_penetration": "float",
      "avg_efficiency": "float"
    }
  ]
}
```

**Error Responses**:
- `404 Not Found`: Run does not exist
- `400 Bad Request`: Run not completed or invalid parameters

---

#### Download Results

```
GET /runs/{run_id}/results/download
```

Downloads results as file.

**Path Parameters**:
- `run_id` (string, required) — Run ID

**Query Parameters**:
- `level` (string, default: county) — Aggregation level
- `format` (string, default: csv) — File format: `csv`, `parquet`, `excel`

**Response** (200 OK): File download

**Error Responses**:
- `404 Not Found`: Run does not exist
- `400 Bad Request`: Run not completed

---

#### Get Time-Series

```
GET /runs/{run_id}/results/timeseries
```

Gets time-series data for a specific area.

**Path Parameters**:
- `run_id` (string, required) — Run ID

**Query Parameters**:
- `level` (string, required) — Aggregation level
- `area_id` (string, required) — Area ID (county FIPS, district code, etc.)
- `format` (string, default: json) — Response format: `json`, `csv`

**Response** (200 OK):
```json
{
  "run_id": "string",
  "area_id": "string",
  "area_name": "string",
  "level": "string",
  "years": ["array of integers"],
  "total_therms": ["array of floats"],
  "upc": ["array of floats"],
  "customer_count": ["array of integers"],
  "end_uses": {
    "space_heating": ["array of floats"],
    "water_heating": ["array of floats"],
    "cooking": ["array of floats"],
    "drying": ["array of floats"],
    "fireplace": ["array of floats"],
    "other": ["array of floats"]
  },
  "electrification_rate": ["array of floats"],
  "heat_pump_penetration": ["array of floats"],
  "avg_efficiency": ["array of floats"]
}
```

---

#### Compare Areas

```
GET /runs/{run_id}/results/comparison
```

Compares results across multiple areas.

**Path Parameters**:
- `run_id` (string, required) — Run ID

**Query Parameters**:
- `level` (string, required) — Aggregation level
- `area_ids` (string, required) — Comma-separated area IDs
- `metric` (string, default: upc) — Metric to compare: `upc`, `total_therms`, `electrification_rate`, `heat_pump_penetration`
- `format` (string, default: json) — Response format: `json`, `csv`

**Response** (200 OK):
```json
{
  "run_id": "string",
  "level": "string",
  "metric": "string",
  "areas": [
    {
      "area_id": "string",
      "area_name": "string",
      "years": ["array of integers"],
      "values": ["array of floats"]
    }
  ]
}
```

---

#### Get GeoJSON

```
GET /runs/{run_id}/results/geojson
```

Gets results as GeoJSON for map visualization.

**Path Parameters**:
- `run_id` (string, required) — Run ID

**Query Parameters**:
- `level` (string, required) — Aggregation level
- `year` (integer, required) — Year to visualize
- `metric` (string, default: upc) — Metric to display: `upc`, `total_therms`, `electrification_rate`, `heat_pump_penetration`

**Response** (200 OK): GeoJSON FeatureCollection

---

#### Get Metadata

```
GET /runs/{run_id}/metadata
```

Gets execution metadata and summary statistics.

**Path Parameters**:
- `run_id` (string, required) — Run ID

**Response** (200 OK):
```json
{
  "run_id": "string",
  "scenario_id": "uuid",
  "scenario_name": "string",
  "status": "string",
  "created_at": "ISO 8601 timestamp",
  "completed_at": "ISO 8601 timestamp or null",
  "execution_time_seconds": "integer or null",
  "data_version": "ISO 8601 date",
  "model_version": "string",
  "summary_statistics": {
    "total_premises": "integer",
    "total_demand_2025": "float",
    "total_demand_2035": "float",
    "demand_reduction_percent": "float",
    "avg_electrification_rate_2035": "float",
    "avg_heat_pump_penetration_2035": "float"
  }
}
```

---

### Scenario Comparison

#### Create Comparison

```
POST /comparisons
```

Creates a comparison of multiple scenarios.

**Request Body**:
```json
{
  "name": "string (required)",
  "description": "string (optional)",
  "scenario_ids": ["array of scenario UUIDs (required)"],
  "metrics": ["array of metric names (optional)"]
}
```

**Response** (201 Created):
```json
{
  "comparison_id": "uuid",
  "name": "string",
  "scenario_ids": ["array of UUIDs"],
  "status": "created",
  "created_at": "ISO 8601 timestamp"
}
```

---

#### Get Comparison

```
GET /comparisons/{comparison_id}
```

Gets comparison results.

**Path Parameters**:
- `comparison_id` (string, required) — Comparison UUID

**Query Parameters**:
- `level` (string, default: county) — Aggregation level
- `format` (string, default: json) — Response format: `json`, `csv`

**Response** (200 OK):
```json
{
  "comparison_id": "uuid",
  "scenarios": [
    {
      "scenario_id": "uuid",
      "scenario_name": "string",
      "data": ["array of results"]
    }
  ],
  "differences": {
    "2035_upc_difference": "float",
    "2035_electrification_rate_difference": "float",
    "cumulative_demand_reduction": "float"
  }
}
```

---

### Data and Configuration

#### Get Default Parameters

```
GET /config/defaults
```

Gets default scenario parameters.

**Response** (200 OK):
```json
{
  "base_year": 2025,
  "forecast_horizon": 10,
  "housing_growth_rate": 0.012,
  "electrification_rates": {
    "space_heating": 0.02,
    "water_heating": 0.05,
    "cooking": 0.01
  },
  "efficiency_improvements": {
    "space_heating": 0.015,
    "water_heating": 0.01,
    "cooking": 0.005
  },
  "weather_assumption": "normal",
  "heat_pump_cop": {
    "ashp_baseline": 3.0,
    "gshp_baseline": 4.0,
    "gorge_penalty": 0.85
  }
}
```

---

#### Get Parameter Definitions

```
GET /config/parameters
```

Gets all available parameters and their valid ranges.

**Response** (200 OK):
```json
{
  "base_year": {
    "type": "integer",
    "min": 2020,
    "max": 2030,
    "default": 2025,
    "description": "Base year for simulation"
  },
  "forecast_horizon": {
    "type": "integer",
    "min": 5,
    "max": 50,
    "default": 10,
    "description": "Number of years to forecast"
  }
}
```

---

#### Get Geographic Areas

```
GET /data/geographic-areas
```

Gets list of available geographic areas.

**Query Parameters**:
- `level` (string, required) — Aggregation level: `county`, `district`, `microclimate`, `microresidential`, `microadoption`, `composite-cell`

**Response** (200 OK):
```json
{
  "level": "string",
  "areas": [
    {
      "area_id": "string",
      "area_name": "string",
      "state": "string or null",
      "customer_count": "integer",
      "total_demand_2025": "float"
    }
  ]
}
```

---

#### Get Weather Stations

```
GET /data/weather-stations
```

Gets weather station information.

**Response** (200 OK):
```json
{
  "stations": [
    {
      "station_id": "string",
      "station_name": "string",
      "icao_code": "string",
      "location": {
        "lat": "float",
        "lon": "float"
      },
      "annual_hdd": "float",
      "annual_cdd": "float",
      "coverage_area_sqmi": "float"
    }
  ]
}
```

---

### Health and Status

#### Health Check

```
GET /health
```

Health check endpoint.

**Response** (200 OK):
```json
{
  "status": "healthy|degraded|unhealthy",
  "timestamp": "ISO 8601 timestamp",
  "version": "string",
  "database": "connected|disconnected",
  "data_loaded": "boolean",
  "queue_length": "integer"
}
```

---

#### System Status

```
GET /status
```

System status and statistics.

**Response** (200 OK):
```json
{
  "status": "operational|maintenance|error",
  "timestamp": "ISO 8601 timestamp",
  "scenarios_total": "integer",
  "scenarios_completed": "integer",
  "scenarios_running": "integer",
  "scenarios_queued": "integer",
  "avg_execution_time_seconds": "float",
  "uptime_seconds": "integer",
  "last_data_update": "ISO 8601 timestamp"
}
```

---

## Error Handling

All API endpoints return standard error responses:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "optional field-specific details"
    }
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_PARAMETER` | 400 | Request parameter validation failed |
| `SCENARIO_NOT_FOUND` | 404 | Scenario ID does not exist |
| `RUN_NOT_FOUND` | 404 | Run ID does not exist |
| `RUN_NOT_COMPLETED` | 400 | Results not available (run still running) |
| `VALIDATION_FAILED` | 422 | Scenario validation failed |
| `INTERNAL_ERROR` | 500 | Server error during execution |
| `UNAUTHORIZED` | 401 | Authentication required |
| `FORBIDDEN` | 403 | Insufficient permissions |

---

## Authentication (Optional)

For production deployments with multiple users:

### Login

```
POST /auth/login
```

**Request Body**:
```json
{
  "username": "user@example.com",
  "password": "password"
}
```

**Response** (200 OK):
```json
{
  "access_token": "jwt-token",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

### Using Tokens

Include the token in all subsequent requests:

```bash
curl -H "Authorization: Bearer jwt-token" \
  http://localhost:8000/api/v1/scenarios
```

---

## Rate Limiting

API rate limits (production):
- **Authenticated users**: 1000 requests/hour
- **Unauthenticated users**: 100 requests/hour

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640000000
```

---

## Pagination

List endpoints support pagination:

**Query Parameters**:
- `limit` (integer, default: 10, max: 100)
- `offset` (integer, default: 0)

**Response**:
```json
{
  "items": ["array of items"],
  "total": "integer",
  "limit": "integer",
  "offset": "integer"
}
```

---

## Filtering and Sorting

List endpoints support filtering and sorting:

**Query Parameters**:
- `filter[field]` — Filter by field value
- `sort` — Sort by field (prefix with `-` for descending)

**Example**:
```
GET /scenarios?filter[status]=completed&sort=-created_at
```

---

## Webhooks (Optional)

For production deployments, webhooks can notify external systems of run completion:

```
POST /webhooks
```

**Request Body**:
```json
{
  "url": "https://example.com/webhook",
  "events": ["run.completed", "run.failed"],
  "active": true
}
```

Webhook payload:
```json
{
  "event": "run.completed",
  "run_id": "string",
  "scenario_id": "uuid",
  "timestamp": "ISO 8601 timestamp",
  "data": {
    "status": "completed",
    "execution_time_seconds": 300
  }
}
```

---

## SDK Examples

### Python

```python
import requests

# Create scenario
response = requests.post(
    'http://localhost:8000/api/v1/scenarios',
    json={
        'name': 'My Scenario',
        'base_year': 2025,
        'forecast_horizon': 10,
        'electrification_rates': {
            'space_heating': 0.08,
            'water_heating': 0.12,
            'cooking': 0.02
        },
        'efficiency_improvements': {
            'space_heating': 0.02,
            'water_heating': 0.015,
            'cooking': 0.01
        }
    }
)
scenario = response.json()
scenario_id = scenario['scenario_id']

# Run scenario
response = requests.post(
    f'http://localhost:8000/api/v1/scenarios/{scenario_id}/run'
)
run = response.json()
run_id = run['run_id']

# Get results
response = requests.get(
    f'http://localhost:8000/api/v1/runs/{run_id}/results',
    params={'level': 'county', 'format': 'json'}
)
results = response.json()
```

### JavaScript

```javascript
// Create scenario
const response = await fetch('http://localhost:8000/api/v1/scenarios', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'My Scenario',
    base_year: 2025,
    forecast_horizon: 10,
    electrification_rates: {
      space_heating: 0.08,
      water_heating: 0.12,
      cooking: 0.02
    },
    efficiency_improvements: {
      space_heating: 0.02,
      water_heating: 0.015,
      cooking: 0.01
    }
  })
});
const scenario = await response.json();
const scenarioId = scenario.scenario_id;

// Run scenario
const runResponse = await fetch(
  `http://localhost:8000/api/v1/scenarios/${scenarioId}/run`,
  { method: 'POST' }
);
const run = await runResponse.json();
const runId = run.run_id;

// Get results
const resultsResponse = await fetch(
  `http://localhost:8000/api/v1/runs/${runId}/results?level=county&format=json`
);
const results = await resultsResponse.json();
```

---

## OpenAPI/Swagger

The API provides automatic OpenAPI documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

---

## Support

For API issues or questions:
- **Documentation**: https://docs.nwnatural-forecast.example.com
- **Issues**: https://github.com/nwnatural/forecast-model/issues
- **Email**: support@nwnatural-forecast.example.com
