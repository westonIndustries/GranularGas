"""
Visualization module for housing stock projections.

Provides functions to generate comparison plots showing actual vs projected
housing stock data, including total units, segment distribution, and district
distribution over time.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing and server environments
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def plot_housing_stock_comparison(
    baseline_year: int,
    baseline_total: int,
    projected_data: Dict[int, int],
    title: str = "Housing Stock Projection: Actual vs Projected",
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6)
) -> plt.Figure:
    """
    Generate a line plot comparing baseline (actual) vs projected housing stock.
    
    Args:
        baseline_year: The year of the baseline (actual) data
        baseline_total: Total units in baseline year
        projected_data: Dictionary mapping year to projected total units
        title: Title for the plot
        output_path: Optional path to save the figure (e.g., 'output/projection.png')
        figsize: Figure size as (width, height) tuple
    
    Returns:
        matplotlib Figure object
    
    Example:
        >>> baseline_year = 2025
        >>> baseline_total = 100
        >>> projected = {2026: 102, 2027: 104, 2028: 106}
        >>> fig = plot_housing_stock_comparison(baseline_year, baseline_total, projected)
        >>> fig.savefig('projection.png')
    """
    # Prepare data
    years = sorted([baseline_year] + list(projected_data.keys()))
    totals = [baseline_total] + [projected_data[y] for y in years[1:]]
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot baseline and projected
    baseline_years = [baseline_year]
    baseline_totals = [baseline_total]
    
    projected_years = sorted(projected_data.keys())
    projected_totals = [projected_data[y] for y in projected_years]
    
    # Plot actual baseline as a point
    ax.scatter(baseline_years, baseline_totals, s=100, color='darkblue', 
               label='Actual (Baseline)', zorder=5, marker='o')
    
    # Plot projected line
    ax.plot(projected_years, projected_totals, 'o-', color='darkgreen', 
            linewidth=2, markersize=6, label='Projected')
    
    # Add grid and labels
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Housing Units', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='best')
    
    # Format y-axis as integers
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    # Tight layout
    plt.tight_layout()
    
    # Save if path provided
    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved housing stock comparison plot to {output_path}")
    
    return fig


def plot_segment_distribution_comparison(
    baseline_year: int,
    baseline_segments: Dict[str, int],
    projected_segments: Dict[int, Dict[str, int]],
    title: str = "Housing Stock by Segment: Actual vs Projected",
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (14, 6)
) -> plt.Figure:
    """
    Generate a grouped bar chart comparing segment distribution over time.
    
    Args:
        baseline_year: The year of the baseline (actual) data
        baseline_segments: Dict mapping segment code to unit count (baseline)
        projected_segments: Dict mapping year to dict of segment codes to unit counts
        title: Title for the plot
        output_path: Optional path to save the figure
        figsize: Figure size as (width, height) tuple
    
    Returns:
        matplotlib Figure object
    
    Example:
        >>> baseline_segments = {'RESSF': 70, 'RESMF': 30}
        >>> projected = {
        ...     2026: {'RESSF': 71, 'RESMF': 31},
        ...     2027: {'RESSF': 72, 'RESMF': 32}
        ... }
        >>> fig = plot_segment_distribution_comparison(2025, baseline_segments, projected)
    """
    # Prepare data
    years = sorted([baseline_year] + list(projected_segments.keys()))
    segments = sorted(set(baseline_segments.keys()) | 
                     set().union(*[set(v.keys()) for v in projected_segments.values()]))
    
    # Create data matrix
    data = {}
    for segment in segments:
        data[segment] = []
        for year in years:
            if year == baseline_year:
                data[segment].append(baseline_segments.get(segment, 0))
            else:
                data[segment].append(projected_segments[year].get(segment, 0))
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Set up bar positions
    x = np.arange(len(years))
    width = 0.8 / len(segments)
    colors = plt.cm.Set3(np.linspace(0, 1, len(segments)))
    
    # Plot bars for each segment
    for i, segment in enumerate(segments):
        offset = width * (i - len(segments) / 2 + 0.5)
        ax.bar(x + offset, data[segment], width, label=segment, color=colors[i])
    
    # Add grid and labels
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Housing Units', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend(fontsize=11, loc='best')
    
    # Format y-axis as integers
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    # Tight layout
    plt.tight_layout()
    
    # Save if path provided
    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved segment distribution plot to {output_path}")
    
    return fig


def plot_district_distribution_comparison(
    baseline_year: int,
    baseline_districts: Dict[str, int],
    projected_districts: Dict[int, Dict[str, int]],
    title: str = "Housing Stock by District: Actual vs Projected",
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (14, 6)
) -> plt.Figure:
    """
    Generate a grouped bar chart comparing district distribution over time.
    
    Args:
        baseline_year: The year of the baseline (actual) data
        baseline_districts: Dict mapping district code to unit count (baseline)
        projected_districts: Dict mapping year to dict of district codes to unit counts
        title: Title for the plot
        output_path: Optional path to save the figure
        figsize: Figure size as (width, height) tuple
    
    Returns:
        matplotlib Figure object
    """
    # Prepare data
    years = sorted([baseline_year] + list(projected_districts.keys()))
    districts = sorted(set(baseline_districts.keys()) | 
                      set().union(*[set(v.keys()) for v in projected_districts.values()]))
    
    # Create data matrix
    data = {}
    for district in districts:
        data[district] = []
        for year in years:
            if year == baseline_year:
                data[district].append(baseline_districts.get(district, 0))
            else:
                data[district].append(projected_districts[year].get(district, 0))
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Set up bar positions
    x = np.arange(len(years))
    width = 0.8 / len(districts)
    colors = plt.cm.Set2(np.linspace(0, 1, len(districts)))
    
    # Plot bars for each district
    for i, district in enumerate(districts):
        offset = width * (i - len(districts) / 2 + 0.5)
        ax.bar(x + offset, data[district], width, label=district, color=colors[i])
    
    # Add grid and labels
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Housing Units', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend(fontsize=11, loc='best')
    
    # Format y-axis as integers
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    # Tight layout
    plt.tight_layout()
    
    # Save if path provided
    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved district distribution plot to {output_path}")
    
    return fig


def plot_growth_rate_analysis(
    baseline_year: int,
    baseline_total: int,
    projected_data: Dict[int, int],
    growth_rate: float,
    title: str = "Housing Stock Growth Rate Analysis",
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6)
) -> plt.Figure:
    """
    Generate a plot showing actual vs expected growth based on growth rate.
    
    Args:
        baseline_year: The year of the baseline (actual) data
        baseline_total: Total units in baseline year
        projected_data: Dictionary mapping year to projected total units
        growth_rate: Annual growth rate used for projection
        title: Title for the plot
        output_path: Optional path to save the figure
        figsize: Figure size as (width, height) tuple
    
    Returns:
        matplotlib Figure object
    """
    # Prepare data
    projected_years = sorted(projected_data.keys())
    projected_totals = [projected_data[y] for y in projected_years]
    
    # Calculate expected values based on growth rate
    expected_totals = [
        int(round(baseline_total * ((1 + growth_rate) ** (y - baseline_year))))
        for y in projected_years
    ]
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot projected vs expected
    ax.plot(projected_years, projected_totals, 'o-', color='darkgreen', 
            linewidth=2, markersize=8, label='Projected (from scenario)')
    ax.plot(projected_years, expected_totals, 's--', color='darkred', 
            linewidth=2, markersize=8, label=f'Expected (r={growth_rate:.2%})')
    
    # Add grid and labels
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Housing Units', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='best')
    
    # Format y-axis as integers
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    # Tight layout
    plt.tight_layout()
    
    # Save if path provided
    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved growth rate analysis plot to {output_path}")
    
    return fig


def plot_projection_summary(
    baseline_year: int,
    baseline_stock,
    projected_stocks: Dict[int, 'HousingStock'],
    growth_rate: float,
    output_dir: str = "output",
    show_plots: bool = False
) -> Dict[str, str]:
    """
    Generate a comprehensive set of comparison plots and save to output directory.
    
    Args:
        baseline_year: The year of the baseline (actual) data
        baseline_stock: HousingStock object for baseline year
        projected_stocks: Dict mapping year to HousingStock object
        growth_rate: Annual growth rate used for projection
        output_dir: Directory to save plots
        show_plots: Whether to display plots (plt.show())
    
    Returns:
        Dictionary mapping plot name to file path
    
    Example:
        >>> baseline = HousingStock(year=2025, ...)
        >>> projected = {2026: HousingStock(...), 2027: HousingStock(...)}
        >>> plots = plot_projection_summary(2025, baseline, projected, 0.02, 'output')
    """
    import os
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare data dictionaries
    projected_totals = {year: stock.total_units for year, stock in projected_stocks.items()}
    projected_segments = {year: stock.units_by_segment for year, stock in projected_stocks.items()}
    projected_districts = {year: stock.units_by_district for year, stock in projected_stocks.items()}
    
    # Generate plots
    plots = {}
    
    # 1. Total housing stock comparison
    fig1 = plot_housing_stock_comparison(
        baseline_year, baseline_stock.total_units, projected_totals,
        output_path=os.path.join(output_dir, "01_total_housing_stock.png")
    )
    plots['total_housing_stock'] = os.path.join(output_dir, "01_total_housing_stock.png")
    
    # 2. Segment distribution comparison
    fig2 = plot_segment_distribution_comparison(
        baseline_year, baseline_stock.units_by_segment, projected_segments,
        output_path=os.path.join(output_dir, "02_segment_distribution.png")
    )
    plots['segment_distribution'] = os.path.join(output_dir, "02_segment_distribution.png")
    
    # 3. District distribution comparison
    fig3 = plot_district_distribution_comparison(
        baseline_year, baseline_stock.units_by_district, projected_districts,
        output_path=os.path.join(output_dir, "03_district_distribution.png")
    )
    plots['district_distribution'] = os.path.join(output_dir, "03_district_distribution.png")
    
    # 4. Growth rate analysis
    fig4 = plot_growth_rate_analysis(
        baseline_year, baseline_stock.total_units, projected_totals, growth_rate,
        output_path=os.path.join(output_dir, "04_growth_rate_analysis.png")
    )
    plots['growth_rate_analysis'] = os.path.join(output_dir, "04_growth_rate_analysis.png")
    
    # Show plots if requested
    if show_plots:
        plt.show()
    
    logger.info(f"Generated {len(plots)} comparison plots in {output_dir}")
    
    return plots
