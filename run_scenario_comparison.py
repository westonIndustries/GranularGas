#!/usr/bin/env python
"""Run scenario comparison report generation."""

import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from src.scenario_comparison import generate_scenario_comparison_report

if __name__ == '__main__':
    baseline_path = 'output/checkpoint_final/baseline_results.csv'
    high_elec_path = 'output/checkpoint_final/high_electrification_results.csv'
    
    try:
        results = generate_scenario_comparison_report(baseline_path, high_elec_path)
        print("\nGenerated reports:")
        for key, path in results.items():
            print(f"  {key}: {path}")
        print("\nScenario comparison report generation completed successfully!")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
