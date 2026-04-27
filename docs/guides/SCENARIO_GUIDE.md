# Running Scenarios: NW Natural End-Use Forecasting Model

## Quick Start

```bash
# Run a single scenario
C:\Python312\python.exe -m src.main scenarios/baseline.json

# Run multiple scenarios
C:\Python312\python.exe -m src.main scenarios/baseline.json scenarios/baseline_monthly.json

# Compare two scenarios side-by-side
C:\Python312\python.exe -m src.main scenarios/baseline.json scenarios/high_electrification.json --compare
```

Results go to `scenarios/{scenario_name}/` — a folder matching the `name` field in your JSON config.

---

## Creating a New Scenario

1. Copy an existing config:
   ```bash
   cp scenarios/baseline.json scenarios/my_scenario.json
   ```

2. Edit the JSON file — change the `name` and any parameters you want to test.

3. Run it:
   ```bash
   C:\Python312\python.exe -m src.main scenarios/my_scenario.json
   ```

---

## Scenario Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | string | required | Scenario identifier. Output folder will match this name. |
| `base_year` | int | 2025 | Starting year for the simulation. |
| `forecast_horizon` | int | 10 | Number of years to project forward (e.g., 10 = 2025–2035). |
| `temporal_resolution` | string | "annual" | `"annual"` or `"monthly"`. Monthly produces 12 rows per year with seasonal load shapes. |
| `heating_factor` | float | 0.187502 | Calibrated therms-per-HDD-per-equipment-unit. Derived from billing data. Don't change unless re-calibrating. |
| `weather_assumption` | string | "normal" | `"normal"`, `"warm"`, or `"cold"`. Affects HDD used in simulation. |

### Housing Stock

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `housing_growth_rate` | float | 0.01 | Annual housing unit growth rate (1% = ~2,100 new homes/yr). |
| `demolition_rate` | float | 0.002 | Annual demolition rate (0.2%/yr). Subtracted from growth. |
| `new_construction_mf_share` | float | 0.37 | Share of new construction that is multi-family (37%). |
| `initial_gas_pct` | float | 38.7 | Territory-wide gas heating market share (%) from Census B25040. |

### Equipment & Efficiency

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `electrification_rate` | float | 0.02 | Annual rate of gas-to-electric fuel switching (2%/yr). |
| `efficiency_improvement` | float | 0.01 | Annual equipment efficiency improvement rate (1%/yr). |
| `annual_degradation_rate` | float | 0.005 | Equipment efficiency loss per year from aging (0.5%/yr). |
| `repair_efficiency_recovery` | float | 0.85 | Efficiency recovery when old equipment is repaired (85% of original). |
| `new_equipment_efficiency` | float | 0.92 | AFUE of replacement equipment (92% code minimum). |

### Heating Multipliers

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `vintage_heating_multipliers` | dict | see below | Multiplier on heating demand by building age. Older homes use more heat. |
| `segment_heating_multipliers` | dict | see below | Multiplier by segment type. Multi-family uses less (shared walls). |

Default vintage multipliers:
```json
{"pre-1980": 1.35, "1980-1999": 1.15, "2000-2009": 1.00, "2010-2014": 0.85, "2015+": 0.70}
```

Default segment multipliers:
```json
{"RESSF": 1.05, "RESMF": 0.70, "Unclassified": 1.00}
```

### Data Integration Toggles

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_recs_ratios` | bool | true | Use RECS 1993–2020 survey data to compute non-heating end-use ratios dynamically. If false, uses hardcoded fallback. |
| `use_census_enrichment` | bool | true | Enrich unclassified premises with Census B25024 (segment) and B25034 (vintage) distributions. |

### Simulation Controls

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `end_use_scope` | list | ["space_heating"] | Which end-uses to simulate. Currently only space_heating is implemented. |
| `max_premises` | int | 0 | Limit premises for quick testing (0 = all ~213K). Set to 1000–5000 for fast iteration. |
| `vectorized` | bool | true | Use fast vectorized simulation. Always use true for production. |
| `sample_size` | int | 100 | Number of premises for Weibull replacement rate sampling. |

---

## Example Scenarios

### High Electrification
```json
{
  "name": "high_electrification",
  "base_year": 2025,
  "forecast_horizon": 10,
  "housing_growth_rate": 0.01,
  "electrification_rate": 0.05,
  "efficiency_improvement": 0.02,
  "weather_assumption": "normal",
  "heating_factor": 0.187502,
  "end_use_scope": ["space_heating"],
  "max_premises": 0,
  "vectorized": true,
  "sample_size": 100,
  "initial_gas_pct": 38.7,
  "temporal_resolution": "annual",
  "annual_degradation_rate": 0.005,
  "repair_efficiency_recovery": 0.85,
  "new_equipment_efficiency": 0.95,
  "demolition_rate": 0.002,
  "new_construction_mf_share": 0.45,
  "vintage_heating_multipliers": {"pre-1980": 1.35, "1980-1999": 1.15, "2000-2009": 1.00, "2010-2014": 0.85, "2015+": 0.70},
  "segment_heating_multipliers": {"RESSF": 1.05, "RESMF": 0.70, "Unclassified": 1.00},
  "use_recs_ratios": true,
  "use_census_enrichment": true
}
```

### Cold Winter Stress Test
```json
{
  "name": "cold_winter",
  "base_year": 2025,
  "forecast_horizon": 10,
  "electrification_rate": 0.01,
  "weather_assumption": "cold",
  "heating_factor": 0.187502,
  "vintage_heating_multipliers": {"pre-1980": 1.50, "1980-1999": 1.25, "2000-2009": 1.05, "2010-2014": 0.90, "2015+": 0.75}
}
```
Any parameter you omit uses the default value.

### Quick Test Run
```json
{
  "name": "quick_test",
  "base_year": 2025,
  "forecast_horizon": 3,
  "max_premises": 1000,
  "heating_factor": 0.187502
}
```

---

## Output Files

Each scenario produces a folder at `scenarios/{name}/` containing:

### Core Results
| File | Description |
|------|-------------|
| `results.csv` / `.json` | Full results: year × end-use with total therms, UPC, premise count |
| `yearly_summary.csv` | Year-by-year aggregated demand summary |
| `metadata.json` | Scenario config and run metadata |
| `SUMMARY.md` | Human-readable results summary |
| `{name}.json` | Copy of the input config |

### Equipment & Demand Breakdowns
| File | Description |
|------|-------------|
| `equipment_stats.csv` / `.json` | Gas/electric units, efficiency, replacements, repairs per year |
| `segment_demand.csv` / `.json` | Demand by segment (RESSF/RESMF) per year |
| `vintage_demand.csv` / `.json` | Demand by building vintage era per year |
| `premise_distribution.csv` / `.json` | Per-premise therms distribution (min/max/median/percentiles) |
| `sample_rates.csv` / `.json` | Weibull-derived replacement, repair, efficiency rates per year |

### Comparisons
| File | Description |
|------|-------------|
| `irp_comparison.csv` / `.json` | Model UPC vs NW Natural IRP forecast side-by-side |
| `estimated_total_upc.csv` / `.json` | Estimated total UPC with non-heating end-use breakdown |
| `observed_billing_upc.csv` | Historical billing-derived UPC (2009–2025) |

### Housing Stock
| File | Description |
|------|-------------|
| `housing_stock.csv` | Projected housing units by segment with B25024 shift |
| `territory_household_breakdown.csv` | Territory-wide households by fuel type (4 categories) |

### External Data Integration
| File | Description |
|------|-------------|
| `census_heating_fuel_trend.csv` / `.json` | Census B25040 gas/electric share 2009–2023 |
| `census_b25024_segment_trend.csv` / `.json` | Census B25024 SF/MF/Mobile share 2009–2023 |
| `census_segment_shift_rates.csv` | Annual segment shift rates from B25024 regression |
| `census_segment_distribution.csv` / `.json` | Latest Census SF/MF/Mobile proportions |
| `census_vintage_distribution.csv` / `.json` | Latest Census vintage era proportions |
| `census_vs_model_housing.csv` / `.json` | Census total housing vs model gas customers |
| `recs_enduse_trend.csv` / `.json` | RECS 1993–2020 end-use shares (7 survey years) |
| `recs_non_heating_ratios.csv` / `.json` | Computed non-heating ratios used in this run |

### Weather
| File | Description |
|------|-------------|
| `hdd_history.csv` | Weighted HDD by year (1985–2025) |
| `hdd_info.csv` | HDD normalization details for this run |

### Charts (22 PNG files)
| Chart | What It Shows |
|-------|---------------|
| `chart_upc_trajectory.png` | Model UPC vs NW Natural IRP forecast |
| `chart_fuel_mix.png` | Territory-wide gas/electric split + switching volume |
| `chart_efficiency.png` | Average fleet efficiency over time |
| `chart_replacements.png` | Equipment replacements and repairs per year (grouped bar) |
| `chart_housing_stock.png` | Projected housing stock by segment (stacked area) |
| `chart_premise_distribution.png` | Per-premise therms distribution (box-plot style) |
| `chart_segment_demand.png` | Total demand by segment over time |
| `chart_total_demand.png` | Total system demand with YoY change |
| `chart_cumulative_reduction.png` | Cumulative demand reduction vs base year |
| `chart_territory_electrification.png` | Territory households by fuel (4-category stacked bar) |
| `chart_estimated_total_upc.png` | Estimated total UPC vs IRP (overview + zoom) |
| `chart_enduse_breakdown.png` | End-use breakdown (stacked area + 100% share) |
| `chart_three_way_comparison.png` | Observed billing vs IRP vs model estimate |
| `chart_monthly_seasonal.png` | Monthly demand pattern (monthly resolution only) |
| `chart_hdd_history.png` | Historical HDD trend (1985–2025) |
| `chart_model_vs_irp.png` | 4-panel model vs IRP deep comparison |
| `chart_vintage_demand.png` | Demand by building vintage era |
| `chart_new_stock_type.png` | Housing stock by segment with share shift |
| `chart_census_heating_fuel_trend.png` | Census B25040 gas vs electric trend |
| `chart_census_vs_model_housing.png` | Census housing units vs model gas customers |
| `chart_recs_enduse_trend.png` | RECS end-use shares 1993–2020 |
| `chart_housing_vintage_stock.png` | Housing stock by vintage era over time |

---

## Running via a Web Interface (Future Work)

The model currently runs as a CLI tool. To expose it as a web application, you would:

1. Wrap `run_single_scenario()` in a Flask or FastAPI endpoint that accepts JSON config via POST
2. Serve the scenario output folder as static files (CSVs, PNGs)
3. Build a form UI that maps to the scenario JSON parameters
4. Display charts inline from the generated PNGs

A minimal Flask example:

```python
from flask import Flask, request, jsonify, send_from_directory
from src.main import load_pipeline_data, run_single_scenario, load_scenario_config
from src.scenario_charts import generate_scenario_charts
from pathlib import Path
import json, tempfile

app = Flask(__name__)

# Load pipeline data once at startup (takes ~10s)
pipeline_data = None

@app.before_request
def init_pipeline():
    global pipeline_data
    if pipeline_data is None:
        pipeline_data = load_pipeline_data()

@app.route('/run', methods=['POST'])
def run_scenario():
    config_dict = request.json
    # Write temp config
    config_path = Path('scenarios') / f"{config_dict['name']}.json"
    with open(config_path, 'w') as f:
        json.dump(config_dict, f)
    config = load_scenario_config(str(config_path))
    
    scenario_dir = Path('scenarios') / config.name
    scenario_dir.mkdir(exist_ok=True)
    
    pe, wd, wt, bf, census, recs_trend, recs_ratios, b25024, shift_rates = pipeline_data
    results_df, metadata = run_single_scenario(
        config, pe, wd, wt, bf,
        output_dir=str(scenario_dir),
        non_heating_ratios=recs_ratios if config_dict.get('use_recs_ratios', True) else None
    )
    generate_scenario_charts(scenario_dir)
    
    return jsonify({"status": "complete", "folder": str(scenario_dir)})

@app.route('/scenarios/<name>/<path:filename>')
def serve_output(name, filename):
    return send_from_directory(f'scenarios/{name}', filename)

if __name__ == '__main__':
    app.run(port=5000)
```

Then from a browser or curl:
```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d @scenarios/baseline.json

# View a chart
open http://localhost:5000/scenarios/baseline/chart_upc_trajectory.png
```

A full web UI with interactive parameter sliders and live chart rendering would be a natural next step. The model's ~15 second runtime per scenario makes it feasible for real-time web use.
