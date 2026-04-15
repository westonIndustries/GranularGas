#!/usr/bin/env python
"""
Generate Property 4 validation results with visualizations.

This script:
1. Creates a baseline housing stock
2. Projects it to future years using a scenario
3. Validates the projection formula
4. Generates HTML and Markdown reports with embedded visualizations
"""

import sys
from pathlib import Path
import pandas as pd
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.housing_stock import build_baseline_stock, project_stock
from src.housing_stock_visualizations import (
    create_projection_series,
    generate_html_report,
    generate_markdown_report,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_test_premise_equipment(num_premises: int = 5000) -> pd.DataFrame:
    """Create a test premise-equipment DataFrame."""
    segments = ['RESSF', 'RESMF']
    districts = ['D1', 'D2', 'D3']
    
    data = {
        'blinded_id': range(1, num_premises + 1),
        'segment_code': [segments[i % 2] for i in range(num_premises)],
        'district_code_IRP': [districts[i % 3] for i in range(num_premises)],
        'equipment_type_code': ['FURNACE'] * num_premises,
        'equipment_class': ['HEAT'] * num_premises,
    }
    return pd.DataFrame(data)


def main():
    """Generate Property 4 results."""
    logger.info("Starting Property 4 results generation...")
    
    # Create output directory
    output_dir = Path('output/housing_stock_projections')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create baseline housing stock
    logger.info("Creating baseline housing stock...")
    premise_equipment = create_test_premise_equipment(num_premises=5000)
    baseline = build_baseline_stock(premise_equipment, base_year=2025)
    logger.info(f"Baseline: {baseline.total_units} units in {baseline.year}")
    
    # Define scenario
    scenario = {
        'housing_growth_rate': 0.015,  # 1.5% annual growth
        'base_year': 2025,
    }
    
    # Create projection series
    logger.info("Creating projection series (2025-2035)...")
    projections = create_projection_series(baseline, target_year=2035, scenario=scenario)
    logger.info(f"Generated {len(projections)} projections")
    
    # Validate formula
    logger.info("Validating projection formula...")
    for proj in projections:
        years = proj.year - baseline.year
        expected = int(round(baseline.total_units * ((1 + scenario['housing_growth_rate']) ** years)))
        error = abs(proj.total_units - expected)
        logger.info(f"Year {proj.year}: {proj.total_units} units (expected {expected}, error {error})")
    
    # Generate reports
    logger.info("Generating HTML report...")
    html_path = output_dir / 'property4_results.html'
    generate_html_report(baseline, projections, scenario, html_path)
    logger.info(f"HTML report saved to {html_path}")
    
    logger.info("Generating Markdown report...")
    md_path = output_dir / 'property4_results.md'
    generate_markdown_report(baseline, projections, scenario, md_path, html_path)
    logger.info(f"Markdown report saved to {md_path}")
    
    logger.info("Property 4 results generation complete!")
    logger.info(f"Output directory: {output_dir}")


if __name__ == '__main__':
    main()
