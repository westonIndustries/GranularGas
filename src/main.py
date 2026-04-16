"""
CLI entry point for NW Natural End-Use Forecasting Model.

Provides command-line interface for running scenarios, comparing results,
and generating outputs. Orchestrates the complete pipeline:
  config → ingest → stock → simulate → aggregate → export

Usage:
    python -m src.main scenarios/baseline.json --output-dir output/baseline
    python -m src.main scenarios/baseline.json scenarios/high_electrification.json --compare
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any

import pandas as pd

from src.config import (
    BASE_YEAR, OUTPUT_DIR, PREMISE_DATA, EQUIPMENT_DATA, EQUIPMENT_CODES,
    SEGMENT_DATA, WEATHER_CALDAY, WATER_TEMP
)
from src.data_ingestion import (
    load_premise_data, load_equipment_data, load_equipment_codes,
    load_segment_data, load_weather_data, load_water_temperature,
    build_premise_equipment_table
)
from src.scenarios import ScenarioConfig, run_scenario, compare_scenarios
from src.aggregation import export_results

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_scenario_config(config_path: str) -> ScenarioConfig:
    """
    Load scenario configuration from JSON file.
    
    Args:
        config_path: Path to scenario JSON file
    
    Returns:
        ScenarioConfig object
    
    Raises:
        FileNotFoundError: If config file not found
        json.JSONDecodeError: If JSON is invalid
        ValueError: If required fields missing
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Scenario config not found: {config_path}")
    
    logger.info(f"Loading scenario config: {config_path}")
    
    with open(config_path, 'r') as f:
        data = json.load(f)
    
    # Validate required fields
    required_fields = {'name', 'base_year', 'forecast_horizon'}
    if not required_fields.issubset(data.keys()):
        missing = required_fields - set(data.keys())
        raise ValueError(f"Missing required fields in config: {missing}")
    
    config = ScenarioConfig.from_dict(data)
    logger.info(f"Loaded scenario: {config.name}")
    
    return config


def load_pipeline_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict[str, float]]:
    """
    Load all data required for the pipeline.
    
    Loads premise, equipment, weather, and water temperature data.
    Builds the unified premise-equipment table and prepares baseload factors.
    
    Returns:
        Tuple of:
            - premise_equipment: Unified premise-equipment DataFrame
            - weather_data: Weather data by station and year
            - water_temp_data: Water temperature data
            - baseload_factors: Dict mapping end_use to annual consumption
    
    Raises:
        FileNotFoundError: If any required data file not found
        ValueError: If data loading or joining fails
    """
    logger.info("Loading pipeline data...")
    
    # Load core NW Natural data
    logger.info("Loading premise data...")
    premises = load_premise_data(PREMISE_DATA)
    logger.info(f"  Loaded {len(premises)} premises")
    
    logger.info("Loading equipment data...")
    equipment = load_equipment_data(EQUIPMENT_DATA)
    logger.info(f"  Loaded {len(equipment)} equipment records")
    
    logger.info("Loading equipment codes...")
    codes = load_equipment_codes(EQUIPMENT_CODES)
    logger.info(f"  Loaded {len(codes)} equipment codes")
    
    logger.info("Loading segment data...")
    segments = load_segment_data(SEGMENT_DATA)
    logger.info(f"  Loaded {len(segments)} segment records")
    
    # Build unified premise-equipment table
    logger.info("Building premise-equipment table...")
    premise_equipment = build_premise_equipment_table(premises, equipment, segments, codes)
    logger.info(f"  Built table with {len(premise_equipment)} records")
    
    # Load weather data
    logger.info("Loading weather data...")
    weather_data = load_weather_data(WEATHER_CALDAY)
    logger.info(f"  Loaded weather data: {len(weather_data)} records")
    
    # Load water temperature data
    logger.info("Loading water temperature data...")
    water_temp_data = load_water_temperature(WATER_TEMP)
    logger.info(f"  Loaded water temperature data: {len(water_temp_data)} records")
    
    # Prepare baseload factors (placeholder - can be extended with actual factors)
    baseload_factors = {
        'space_heating': 0.0,      # Weather-driven, not baseload
        'water_heating': 0.0,      # Weather-driven, not baseload
        'cooking': 30.0,           # therms/year
        'clothes_drying': 20.0,    # therms/year
        'fireplace': 55.0,         # therms/year
        'other': 10.0,             # therms/year
    }
    
    logger.info("Pipeline data loaded successfully")
    
    return premise_equipment, weather_data, water_temp_data, baseload_factors


def run_single_scenario(
    config: ScenarioConfig,
    premise_equipment: pd.DataFrame,
    weather_data: pd.DataFrame,
    water_temp_data: pd.DataFrame,
    baseload_factors: Dict[str, float],
    output_dir: str
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Run a single scenario and return results.
    
    Args:
        config: ScenarioConfig object
        premise_equipment: Unified premise-equipment DataFrame
        weather_data: Weather data
        water_temp_data: Water temperature data
        baseload_factors: Baseload consumption factors
        output_dir: Directory to save results
    
    Returns:
        Tuple of (results_df, metadata)
    """
    logger.info(f"Running scenario: {config.name}")
    
    results_df, metadata = run_scenario(
        config,
        premise_equipment,
        weather_data,
        water_temp_data,
        baseload_factors,
        output_dir=output_dir
    )
    
    logger.info(f"Scenario complete: {config.name}")
    logger.info(f"  Total rows: {len(results_df)}")
    logger.info(f"  Years: {config.base_year}-{config.base_year + config.forecast_horizon}")
    logger.info(f"  End-uses: {results_df['end_use'].nunique()}")
    
    return results_df, metadata


def print_summary_statistics(results_df: pd.DataFrame, metadata: Dict[str, Any]) -> None:
    """
    Print summary statistics to stdout.
    
    Args:
        results_df: Results DataFrame
        metadata: Scenario metadata
    """
    print("\n" + "="*70)
    print(f"SCENARIO: {metadata['scenario_name']}")
    print("="*70)
    
    print(f"\nConfiguration:")
    print(f"  Base Year: {metadata['base_year']}")
    print(f"  Forecast Horizon: {metadata['forecast_horizon']} years")
    print(f"  Housing Growth Rate: {metadata['housing_growth_rate']:.2%}")
    print(f"  Electrification Rate: {metadata['electrification_rate']:.2%}")
    print(f"  Efficiency Improvement: {metadata['efficiency_improvement']:.2%}")
    print(f"  Weather Assumption: {metadata['weather_assumption']}")
    
    print(f"\nResults Summary:")
    print(f"  Total Rows: {metadata['total_rows']}")
    print(f"  Years Simulated: {metadata['years_simulated']}")
    print(f"  End-Uses: {metadata['end_uses']}")
    
    # Aggregate by year
    by_year = results_df.groupby('year').agg({
        'total_therms': 'sum',
        'use_per_customer': 'first',
        'premise_count': 'first'
    }).reset_index()
    
    print(f"\nDemand by Year:")
    print(f"  {'Year':<8} {'Total Therms':<18} {'UPC':<12} {'Premises':<12}")
    print(f"  {'-'*50}")
    for _, row in by_year.iterrows():
        print(f"  {int(row['year']):<8} {row['total_therms']:>15,.0f} {row['use_per_customer']:>10.1f} {int(row['premise_count']):>10,}")
    
    # Aggregate by end-use
    by_enduse = results_df.groupby('end_use')['total_therms'].sum().sort_values(ascending=False)
    
    print(f"\nDemand by End-Use (Total across all years):")
    print(f"  {'End-Use':<25} {'Total Therms':<18} {'Share':<10}")
    print(f"  {'-'*53}")
    total = by_enduse.sum()
    for enduse, therms in by_enduse.items():
        share = therms / total if total > 0 else 0
        print(f"  {enduse:<25} {therms:>15,.0f} {share:>8.1%}")
    
    print("\n" + "="*70 + "\n")


def main():
    """
    Main CLI entry point.
    
    Parses arguments, loads data, runs scenario(s), and exports results.
    """
    parser = argparse.ArgumentParser(
        description='NW Natural End-Use Forecasting Model - CLI Entry Point',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run single scenario
  python -m src.main scenarios/baseline.json

  # Run scenario with custom output directory
  python -m src.main scenarios/baseline.json --output-dir output/my_run

  # Run baseline-only (skip comparison)
  python -m src.main scenarios/baseline.json --baseline-only

  # Compare two scenarios
  python -m src.main scenarios/baseline.json scenarios/high_electrification.json --compare
        """
    )
    
    parser.add_argument(
        'scenario_configs',
        nargs='+',
        help='Path(s) to scenario JSON config file(s)'
    )
    
    parser.add_argument(
        '--output-dir',
        default=OUTPUT_DIR,
        help=f'Output directory for results (default: {OUTPUT_DIR})'
    )
    
    parser.add_argument(
        '--baseline-only',
        action='store_true',
        help='Run only the first scenario (baseline), skip comparison'
    )
    
    parser.add_argument(
        '--compare',
        action='store_true',
        help='Compare multiple scenarios (requires 2+ scenario configs)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Load pipeline data once
        logger.info("Initializing pipeline...")
        premise_equipment, weather_data, water_temp_data, baseload_factors = load_pipeline_data()
        
        # Load scenario configs
        logger.info(f"Loading {len(args.scenario_configs)} scenario config(s)...")
        configs = [load_scenario_config(path) for path in args.scenario_configs]
        
        # Run scenarios
        scenario_results = []
        for config in configs:
            results_df, metadata = run_single_scenario(
                config,
                premise_equipment,
                weather_data,
                water_temp_data,
                baseload_factors,
                output_dir=args.output_dir
            )
            scenario_results.append((results_df, metadata))
            
            # Print summary for this scenario
            print_summary_statistics(results_df, metadata)
            
            # Export individual scenario results
            scenario_output_path = Path(args.output_dir) / 'scenarios' / f"{config.name}_results.csv"
            export_results(results_df, str(scenario_output_path), format='csv')
            logger.info(f"Exported scenario results: {scenario_output_path}")
        
        # Compare scenarios if requested and multiple scenarios provided
        if args.compare and len(scenario_results) > 1:
            logger.info(f"Comparing {len(scenario_results)} scenarios...")
            comparison_df = compare_scenarios(scenario_results, output_dir=args.output_dir)
            
            # Export comparison results
            comparison_output_path = Path(args.output_dir) / 'scenarios' / 'comparison_results.csv'
            export_results(comparison_df, str(comparison_output_path), format='csv')
            logger.info(f"Exported comparison results: {comparison_output_path}")
            
            # Print comparison summary
            print("\n" + "="*70)
            print("SCENARIO COMPARISON")
            print("="*70)
            print(f"\nScenarios compared: {', '.join([m['scenario_name'] for _, m in scenario_results])}")
            print(f"Years: {comparison_df['year'].min()}-{comparison_df['year'].max()}")
            print(f"Total rows: {len(comparison_df)}")
            print("\nComparison results exported to:")
            print(f"  {comparison_output_path}")
            print("\n" + "="*70 + "\n")
        
        elif args.baseline_only:
            logger.info("Baseline-only mode: skipping comparison")
        
        elif len(scenario_results) > 1 and not args.compare:
            logger.warning(
                f"Multiple scenarios provided ({len(scenario_results)}) but --compare not specified. "
                "Use --compare to generate comparison results."
            )
        
        logger.info("Pipeline execution completed successfully")
        return 0
    
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
