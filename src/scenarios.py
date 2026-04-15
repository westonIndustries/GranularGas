"""
Scenario management module for NW Natural end-use forecasting model.

Defines scenario configurations, validation logic, and orchestration functions
for running independent forecasting scenarios with different assumptions about
technology adoption, electrification, and efficiency improvements.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import logging
from pathlib import Path
import json

from src.data_ingestion import build_premise_equipment_table
from src.housing_stock import build_baseline_stock, project_stock
from src.equipment import build_equipment_inventory, apply_replacements
from src.simulation import simulate_all_end_uses
from src.aggregation import aggregate_by_end_use, aggregate_by_segment, aggregate_by_district, compute_use_per_customer
from src.config import BASE_YEAR, OUTPUT_DIR

logger = logging.getLogger(__name__)


@dataclass
class ScenarioConfig:
    """
    Configuration for a forecasting scenario.
    
    Attributes:
        name: Scenario identifier (e.g., 'baseline', 'high_electrification')
        base_year: Starting year for projections (typically 2025)
        forecast_horizon: Number of years to project (e.g., 10 for 2025-2035)
        housing_growth_rate: Annual housing unit growth rate (0.0-0.05)
        electrification_rate: Annual rate of gas-to-electric fuel switching (0.0-0.10)
        efficiency_improvement: Annual efficiency improvement rate (0.0-0.05)
        weather_assumption: Weather scenario ('normal', 'warm', 'cold')
    """
    name: str
    base_year: int = BASE_YEAR
    forecast_horizon: int = 10
    housing_growth_rate: float = 0.01
    electrification_rate: float = 0.02
    efficiency_improvement: float = 0.01
    weather_assumption: str = 'normal'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScenarioConfig':
        """Create config from dictionary."""
        return cls(**data)


def validate_scenario(config: ScenarioConfig) -> Dict[str, Any]:
    """
    Validate scenario configuration parameters.
    
    Checks parameter ranges and interdependencies. Returns validation results
    with warnings for out-of-range values and errors for invalid combinations.
    
    Args:
        config: ScenarioConfig object to validate
    
    Returns:
        Dictionary with keys:
            - 'valid': bool, True if all checks pass
            - 'warnings': List[str], non-critical issues
            - 'errors': List[str], critical issues that prevent execution
            - 'details': Dict with per-parameter validation results
    
    Raises:
        TypeError: If config is not a ScenarioConfig instance
    """
    if not isinstance(config, ScenarioConfig):
        raise TypeError(f"config must be ScenarioConfig, got {type(config)}")
    
    warnings = []
    errors = []
    details = {}
    
    # Validate base_year
    if config.base_year < 2000 or config.base_year > 2100:
        errors.append(f"base_year {config.base_year} outside valid range [2000, 2100]")
        details['base_year'] = 'ERROR'
    else:
        details['base_year'] = 'OK'
    
    # Validate forecast_horizon
    if config.forecast_horizon <= 0:
        errors.append(f"forecast_horizon {config.forecast_horizon} must be > 0")
        details['forecast_horizon'] = 'ERROR'
    elif config.forecast_horizon > 100:
        warnings.append(f"forecast_horizon {config.forecast_horizon} is unusually long (>100 years)")
        details['forecast_horizon'] = 'WARNING'
    else:
        details['forecast_horizon'] = 'OK'
    
    # Validate housing_growth_rate
    if not (0.0 <= config.housing_growth_rate <= 0.05):
        warnings.append(f"housing_growth_rate {config.housing_growth_rate} outside typical range [0.0, 0.05]")
        details['housing_growth_rate'] = 'WARNING'
    else:
        details['housing_growth_rate'] = 'OK'
    
    # Validate electrification_rate
    if not (0.0 <= config.electrification_rate <= 0.10):
        warnings.append(f"electrification_rate {config.electrification_rate} outside typical range [0.0, 0.10]")
        details['electrification_rate'] = 'WARNING'
    else:
        details['electrification_rate'] = 'OK'
    
    # Validate efficiency_improvement
    if not (0.0 <= config.efficiency_improvement <= 0.05):
        warnings.append(f"efficiency_improvement {config.efficiency_improvement} outside typical range [0.0, 0.05]")
        details['efficiency_improvement'] = 'WARNING'
    else:
        details['efficiency_improvement'] = 'OK'
    
    # Validate weather_assumption
    valid_weather = {'normal', 'warm', 'cold'}
    if config.weather_assumption not in valid_weather:
        errors.append(f"weather_assumption '{config.weather_assumption}' not in {valid_weather}")
        details['weather_assumption'] = 'ERROR'
    else:
        details['weather_assumption'] = 'OK'
    
    # Check for rate constraints (all rates should be in [0, 1])
    rate_fields = {
        'housing_growth_rate': config.housing_growth_rate,
        'electrification_rate': config.electrification_rate,
        'efficiency_improvement': config.efficiency_improvement,
    }
    for field_name, value in rate_fields.items():
        if not (0.0 <= value <= 1.0):
            errors.append(f"{field_name} {value} outside valid range [0.0, 1.0]")
    
    valid = len(errors) == 0
    
    logger.info(
        f"Validated scenario '{config.name}': "
        f"valid={valid}, warnings={len(warnings)}, errors={len(errors)}"
    )
    
    return {
        'valid': valid,
        'warnings': warnings,
        'errors': errors,
        'details': details,
        'config': config
    }


def run_scenario(
    config: ScenarioConfig,
    premise_equipment: pd.DataFrame,
    weather_data: pd.DataFrame,
    water_temp_data: pd.DataFrame,
    baseload_factors: Dict[str, float],
    output_dir: Optional[str] = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Run a complete forecasting scenario from baseline through projection years.
    
    Orchestrates the full pipeline: load base data, build baseline housing stock,
    then for each year in forecast_horizon: project stock, apply replacements,
    simulate, and aggregate. Stores per-year results with scenario_name label.
    
    Args:
        config: ScenarioConfig object with scenario parameters
        premise_equipment: DataFrame from build_premise_equipment_table
        weather_data: DataFrame with weather data (HDD, etc.) by station and year
        water_temp_data: DataFrame with water temperature data
        baseload_factors: Dict mapping end_use to annual consumption (therms)
        output_dir: Optional directory to save per-year results
    
    Returns:
        Tuple of:
            - results_df: DataFrame with columns:
                year, end_use, scenario_name, total_therms, use_per_customer, premise_count
            - metadata: Dict with scenario metadata and execution summary
    
    Raises:
        ValueError: If config validation fails
        ValueError: If premise_equipment or weather_data is empty
    """
    # Validate scenario
    validation = validate_scenario(config)
    if not validation['valid']:
        raise ValueError(f"Scenario validation failed: {validation['errors']}")
    
    if premise_equipment.empty:
        raise ValueError("premise_equipment DataFrame is empty")
    if weather_data.empty:
        raise ValueError("weather_data DataFrame is empty")
    
    output_dir = Path(output_dir or OUTPUT_DIR) / 'scenarios'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Running scenario '{config.name}' for years {config.base_year}-{config.base_year + config.forecast_horizon}")
    
    # Build baseline housing stock
    baseline_stock = build_baseline_stock(premise_equipment, config.base_year)
    logger.info(f"Built baseline stock: {baseline_stock.total_units} units")
    
    # Build baseline equipment inventory
    baseline_equipment = build_equipment_inventory(premise_equipment)
    logger.info(f"Built baseline equipment inventory: {len(baseline_equipment)} equipment records")
    
    # Collect results for all years
    all_results = []
    
    # Run simulation for each year in forecast horizon
    for year_offset in range(config.forecast_horizon + 1):
        year = config.base_year + year_offset
        
        logger.info(f"Processing year {year} (offset {year_offset})")
        
        # Project housing stock
        if year_offset == 0:
            # Base year: use baseline stock
            stock = baseline_stock
            equipment = baseline_equipment.copy()
        else:
            # Future year: project stock and apply replacements
            stock = project_stock(baseline_stock, year, config.to_dict())
            
            # Build scenario config dict for apply_replacements
            scenario_dict = {
                'electrification_rate': {
                    'space_heating': config.electrification_rate,
                    'water_heating': config.electrification_rate,
                    'cooking': 0.0,
                    'clothes_drying': config.electrification_rate,
                    'fireplace': 0.0,
                    'other': 0.0
                },
                'efficiency_improvement': {
                    'space_heating': config.efficiency_improvement,
                    'water_heating': config.efficiency_improvement,
                    'cooking': config.efficiency_improvement,
                    'clothes_drying': config.efficiency_improvement,
                    'fireplace': 0.0,
                    'other': 0.0
                }
            }
            
            # Apply equipment replacements and fuel switching
            equipment = apply_replacements(
                baseline_equipment.copy(),
                scenario_dict,
                year
            )
        
        # Simulate end-use consumption
        sim_results = simulate_all_end_uses(
            equipment,
            weather_data,
            water_temp_data,
            baseload_factors,
            year=year
        )
        
        # Aggregate by end-use
        agg_results = aggregate_by_end_use(sim_results)
        agg_results['year'] = year
        agg_results['scenario_name'] = config.name
        
        # Compute use-per-customer
        total_demand = agg_results['total_therms'].sum()
        total_customers = stock.total_units
        upc = compute_use_per_customer(total_demand, total_customers)
        agg_results['use_per_customer'] = upc
        
        all_results.append(agg_results)
        
        logger.info(
            f"Year {year}: total_demand={total_demand:.0f} therms, "
            f"UPC={upc:.1f} therms/customer, "
            f"end_uses={len(agg_results)}"
        )
    
    # Combine all years into single results DataFrame
    results_df = pd.concat(all_results, ignore_index=True)
    
    # Reorder columns for consistency
    results_df = results_df[['year', 'end_use', 'scenario_name', 'total_therms', 'use_per_customer', 'premise_count']]
    
    # Create metadata
    metadata = {
        'scenario_name': config.name,
        'base_year': config.base_year,
        'forecast_horizon': config.forecast_horizon,
        'housing_growth_rate': config.housing_growth_rate,
        'electrification_rate': config.electrification_rate,
        'efficiency_improvement': config.efficiency_improvement,
        'weather_assumption': config.weather_assumption,
        'total_rows': len(results_df),
        'years_simulated': config.forecast_horizon + 1,
        'end_uses': results_df['end_use'].nunique(),
    }
    
    logger.info(
        f"Completed scenario '{config.name}': "
        f"{len(results_df)} result rows, "
        f"{config.forecast_horizon + 1} years, "
        f"{results_df['end_use'].nunique()} end-uses"
    )
    
    return results_df, metadata


def compare_scenarios(
    scenario_results: List[Tuple[pd.DataFrame, Dict[str, Any]]],
    output_dir: Optional[str] = None
) -> pd.DataFrame:
    """
    Merge results from multiple scenario runs into a comparison DataFrame.
    
    Combines results from multiple scenarios into a single DataFrame with
    consistent columns for side-by-side comparison.
    
    Args:
        scenario_results: List of (results_df, metadata) tuples from run_scenario
        output_dir: Optional directory to save comparison results
    
    Returns:
        DataFrame with columns:
            - year: Simulation year
            - end_use: End-use category
            - scenario_name: Scenario identifier
            - total_therms: Total demand (therms)
            - use_per_customer: Use per customer (therms/customer)
            - premise_count: Number of premises
        
        Sorted by year, scenario_name, end_use
    
    Raises:
        ValueError: If scenario_results is empty
    """
    if not scenario_results:
        raise ValueError("scenario_results list is empty")
    
    output_dir = Path(output_dir or OUTPUT_DIR) / 'scenarios'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Combine all scenario results, adding scenario_name from metadata if not in results
    all_dfs = []
    for results_df, metadata in scenario_results:
        df = results_df.copy()
        # Add scenario_name from metadata if not already in results
        if 'scenario_name' not in df.columns:
            df['scenario_name'] = metadata.get('scenario_name', 'unknown')
        all_dfs.append(df)
    
    comparison_df = pd.concat(all_dfs, ignore_index=True)
    
    # Ensure consistent column order and types
    required_cols = ['year', 'end_use', 'scenario_name', 'total_therms', 'use_per_customer', 'premise_count']
    # Only select columns that exist
    cols_to_select = [col for col in required_cols if col in comparison_df.columns]
    comparison_df = comparison_df[cols_to_select]
    
    comparison_df['year'] = comparison_df['year'].astype(int)
    comparison_df['total_therms'] = comparison_df['total_therms'].astype(float)
    comparison_df['use_per_customer'] = comparison_df['use_per_customer'].astype(float)
    comparison_df['premise_count'] = comparison_df['premise_count'].astype(int)
    
    # Sort for consistent output
    comparison_df = comparison_df.sort_values(['year', 'scenario_name', 'end_use']).reset_index(drop=True)
    
    logger.info(
        f"Compared {len(scenario_results)} scenarios: "
        f"{len(comparison_df)} total rows, "
        f"years {comparison_df['year'].min()}-{comparison_df['year'].max()}, "
        f"scenarios: {', '.join(comparison_df['scenario_name'].unique())}"
    )
    
    return comparison_df
