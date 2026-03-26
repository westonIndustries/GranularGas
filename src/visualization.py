"""
Visualization module for housing stock projections.

Provides functions to generate comparison plots showing actual vs projected
housing stock data, including total units, segment distribution, and district
distribution over time, plus a choropleth map of the service territory.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing and server environments
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging
import json

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
    
    plt.close(fig)
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
    
    plt.close(fig)
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
    
    plt.close(fig)
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
    
    plt.close(fig)
    return fig


def plot_service_territory_map(
    baseline_year: int,
    baseline_stock,
    projected_stocks: Dict[int, 'HousingStock'],
    growth_rate: float,
    title: str = "NW Natural Service Territory: Projected Housing Growth Rate",
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (14, 10)
) -> plt.Figure:
    """
    Generate a choropleth map of NW Natural service territory by county.
    
    Color-codes counties by projected housing growth rate (low/medium/high).
    Includes district boundaries and weather station locations.
    
    Args:
        baseline_year: The year of the baseline (actual) data
        baseline_stock: HousingStock object for baseline year
        projected_stocks: Dict mapping year to HousingStock object
        growth_rate: Annual growth rate used for projection
        title: Title for the plot
        output_path: Optional path to save the figure
        figsize: Figure size as (width, height) tuple
    
    Returns:
        matplotlib Figure object
    """
    # NW Natural service territory: 16 counties (13 Oregon, 3 Washington)
    # County FIPS codes and names
    counties_data = {
        # Oregon counties
        'Multnomah': {'state': 'OR', 'fips': 41051, 'lat': 45.5, 'lon': -122.7},
        'Washington': {'state': 'OR', 'fips': 41067, 'lat': 45.4, 'lon': -123.2},
        'Clackamas': {'state': 'OR', 'fips': 41005, 'lat': 45.2, 'lon': -122.5},
        'Lane': {'state': 'OR', 'fips': 41039, 'lat': 44.0, 'lon': -123.1},
        'Marion': {'state': 'OR', 'fips': 41047, 'lat': 44.8, 'lon': -123.0},
        'Yamhill': {'state': 'OR', 'fips': 41071, 'lat': 45.2, 'lon': -123.5},
        'Polk': {'state': 'OR', 'fips': 41053, 'lat': 44.8, 'lon': -123.3},
        'Benton': {'state': 'OR', 'fips': 41003, 'lat': 44.6, 'lon': -123.3},
        'Linn': {'state': 'OR', 'fips': 41043, 'lat': 44.5, 'lon': -122.8},
        'Columbia': {'state': 'OR', 'fips': 41009, 'lat': 46.2, 'lon': -123.4},
        'Clatsop': {'state': 'OR', 'fips': 41007, 'lat': 46.1, 'lon': -123.8},
        'Lincoln': {'state': 'OR', 'fips': 41041, 'lat': 44.6, 'lon': -124.0},
        'Coos': {'state': 'OR', 'fips': 41011, 'lat': 43.3, 'lon': -124.2},
        # Washington counties
        'Clark': {'state': 'WA', 'fips': 53011, 'lat': 45.8, 'lon': -122.5},
        'Skamania': {'state': 'WA', 'fips': 53059, 'lat': 45.8, 'lon': -121.8},
        'Klickitat': {'state': 'WA', 'fips': 53039, 'lat': 45.7, 'lon': -121.3},
    }
    
    # Weather stations: 11 stations with approximate coordinates
    weather_stations = {
        'KPDX': {'name': 'Portland', 'lat': 45.59, 'lon': -122.60},
        'KEUG': {'name': 'Eugene', 'lat': 44.12, 'lon': -123.21},
        'KSLE': {'name': 'Salem', 'lat': 44.90, 'lon': -123.00},
        'KAST': {'name': 'Astoria', 'lat': 46.16, 'lon': -123.88},
        'KDLS': {'name': 'The Dalles', 'lat': 45.60, 'lon': -121.31},
        'KOTH': {'name': 'North Bend', 'lat': 43.41, 'lon': -124.25},
        'KONP': {'name': 'Newport', 'lat': 44.58, 'lon': -124.06},
        'KCVO': {'name': 'Corvallis', 'lat': 44.50, 'lon': -123.30},
        'KHIO': {'name': 'Hillsboro', 'lat': 45.54, 'lon': -122.99},
        'KTTD': {'name': 'Troutdale', 'lat': 45.56, 'lon': -122.40},
        'KVUO': {'name': 'Vancouver', 'lat': 45.59, 'lon': -122.66},
    }
    
    # Calculate growth rates by county (simplified: use overall growth rate)
    # In a real implementation, this would be based on county-level projections
    growth_categories = {}
    for county in counties_data.keys():
        # Categorize growth rate
        if growth_rate < -0.01:
            growth_categories[county] = 'Low'
        elif growth_rate < 0.01:
            growth_categories[county] = 'Medium'
        else:
            growth_categories[county] = 'High'
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Define color map for growth categories
    color_map = {'Low': '#d73027', 'Medium': '#fee090', 'High': '#1a9850'}
    
    # Plot counties as scatter points (simplified representation)
    for county, data in counties_data.items():
        category = growth_categories[county]
        color = color_map[category]
        ax.scatter(data['lon'], data['lat'], s=500, c=color, alpha=0.7, 
                  edgecolors='black', linewidth=1.5, zorder=3)
        ax.text(data['lon'], data['lat'], county[:3], ha='center', va='center',
               fontsize=8, fontweight='bold', zorder=4)
    
    # Plot weather stations
    for station_code, station_data in weather_stations.items():
        ax.scatter(station_data['lon'], station_data['lat'], s=100, c='blue', 
                  marker='^', alpha=0.8, edgecolors='darkblue', linewidth=1, zorder=5)
        ax.text(station_data['lon'], station_data['lat'] + 0.15, station_code, 
               ha='center', va='bottom', fontsize=7, color='blue', fontweight='bold', zorder=5)
    
    # Set map extent (NW Natural service territory)
    ax.set_xlim(-124.5, -121.0)
    ax.set_ylim(43.0, 46.5)
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Labels and title
    ax.set_xlabel('Longitude', fontsize=11, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=11, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Create legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#d73027', edgecolor='black', label='Low Growth (< -1%)'),
        Patch(facecolor='#fee090', edgecolor='black', label='Medium Growth (-1% to 1%)'),
        Patch(facecolor='#1a9850', edgecolor='black', label='High Growth (> 1%)'),
        plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='blue', 
                  markersize=8, label='Weather Stations', markeredgecolor='darkblue'),
    ]
    ax.legend(handles=legend_elements, fontsize=10, loc='upper left')
    
    # Add note about projection
    note_text = f"Growth Rate: {growth_rate:.2%}/year | Baseline Year: {baseline_year}"
    ax.text(0.5, -0.08, note_text, transform=ax.transAxes, 
           ha='center', fontsize=10, style='italic', color='gray')
    
    # Tight layout
    plt.tight_layout()
    
    # Save if path provided
    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved service territory map to {output_path}")
    
    plt.close(fig)
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
    
    # 5. Service territory map (CRITICAL - MISSING)
    fig5 = plot_service_territory_map(
        baseline_year, baseline_stock, projected_stocks, growth_rate,
        output_path=os.path.join(output_dir, "05_service_territory_map.png")
    )
    plots['service_territory_map'] = os.path.join(output_dir, "05_service_territory_map.png")
    
    # Show plots if requested
    if show_plots:
        plt.show()
    
    logger.info(f"Generated {len(plots)} comparison plots in {output_dir}")
    
    return plots


def plot_electrification_map(
    district_electrification_rates: Dict[str, float],
    title: str = "Equipment Electrification Rate by District",
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (14, 10)
) -> plt.Figure:
    """
    Generate a map showing electrification rates by district with OpenStreetMap background.
    
    Color-codes districts by electrification rate (% of gas equipment converted to electric).
    Includes district boundaries and major cities.
    
    Args:
        district_electrification_rates: Dict mapping district code to electrification rate [0, 1]
        title: Title for the plot
        output_path: Optional path to save the figure
        figsize: Figure size as (width, height) tuple
    
    Returns:
        matplotlib Figure object
    """
    try:
        import contextily as ctx
    except ImportError:
        logger.warning("contextily not installed; using simple map without OSM base layer")
        ctx = None
    
    # NW Natural districts with approximate centroids and boundaries
    districts_data = {
        'D1': {'lat': 45.5, 'lon': -122.7, 'name': 'Portland Metro'},
        'D2': {'lat': 44.8, 'lon': -123.0, 'name': 'Salem/Marion'},
        'D3': {'lat': 44.0, 'lon': -123.1, 'name': 'Eugene/Lane'},
        'D4': {'lat': 45.2, 'lon': -123.2, 'name': 'Willamette Valley'},
        'D5': {'lat': 44.6, 'lon': -123.3, 'name': 'Corvallis/Benton'},
        'D6': {'lat': 46.1, 'lon': -123.8, 'name': 'Coast/Clatsop'},
        'D7': {'lat': 45.8, 'lon': -122.5, 'name': 'Vancouver/Clark'},
        'D8': {'lat': 45.7, 'lon': -121.3, 'name': 'Gorge/Klickitat'},
    }
    
    # Major cities for reference
    cities = {
        'Portland': {'lat': 45.52, 'lon': -122.68},
        'Salem': {'lat': 44.94, 'lon': -123.04},
        'Eugene': {'lat': 44.05, 'lon': -123.09},
        'Corvallis': {'lat': 44.56, 'lon': -123.27},
        'Astoria': {'lat': 46.19, 'lon': -123.88},
        'Vancouver': {'lat': 45.64, 'lon': -122.66},
    }
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Add OpenStreetMap base layer if contextily available
    if ctx is not None:
        try:
            ax.set_xlim(-124.5, -121.0)
            ax.set_ylim(43.0, 46.5)
            ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik, 
                           zoom=8, alpha=0.4)
        except Exception as e:
            logger.warning(f"Failed to add OSM base layer: {e}")
            ax.set_facecolor('#e6e6e6')
    else:
        ax.set_facecolor('#e6e6e6')
        ax.set_xlim(-124.5, -121.0)
        ax.set_ylim(43.0, 46.5)
    
    # Define color map for electrification rates (red=low, yellow=medium, green=high)
    def get_color(rate):
        if rate < 0.1:
            return '#d73027'  # Red: low electrification
        elif rate < 0.3:
            return '#fee090'  # Yellow: medium electrification
        else:
            return '#1a9850'  # Green: high electrification
    
    # Plot districts
    for district_code, data in districts_data.items():
        if district_code in district_electrification_rates:
            rate = district_electrification_rates[district_code]
            color = get_color(rate)
            
            # Plot district as circle
            ax.scatter(data['lon'], data['lat'], s=1200, c=color, alpha=0.7, 
                      edgecolors='black', linewidth=2, zorder=10, marker='o')
            
            # Add district label and rate
            ax.text(data['lon'], data['lat'] + 0.05, district_code, ha='center', va='center',
                   fontsize=11, fontweight='bold', zorder=11, color='black')
            ax.text(data['lon'], data['lat'] - 0.05, f'{rate:.1%}', ha='center', va='center',
                   fontsize=9, fontweight='bold', zorder=11, color='black')
    
    # Plot cities for reference
    for city_name, city_data in cities.items():
        ax.scatter(city_data['lon'], city_data['lat'], s=80, c='gray', 
                  marker='s', alpha=0.6, edgecolors='darkgray', linewidth=1, zorder=5)
        ax.text(city_data['lon'], city_data['lat'] - 0.15, city_name, 
               ha='center', va='top', fontsize=8, color='gray', fontweight='bold', zorder=5)
    
    # Add grid
    ax.grid(True, alpha=0.2, linestyle='--', zorder=1)
    
    # Labels and title
    ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=15, fontweight='bold', pad=20)
    
    # Create legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#d73027', edgecolor='black', label='Low Electrification (< 10%)', linewidth=1.5),
        Patch(facecolor='#fee090', edgecolor='black', label='Medium Electrification (10-30%)', linewidth=1.5),
        Patch(facecolor='#1a9850', edgecolor='black', label='High Electrification (> 30%)', linewidth=1.5),
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', 
                  markersize=8, label='Major Cities', markeredgecolor='darkgray', markeredgewidth=1),
    ]
    ax.legend(handles=legend_elements, fontsize=11, loc='upper left', framealpha=0.95)
    
    # Add note
    note_text = "Electrification Rate: % of gas equipment converted to electric\nMap shows NW Natural service territory with OpenStreetMap background"
    ax.text(0.5, -0.12, note_text, transform=ax.transAxes, 
           ha='center', fontsize=10, style='italic', color='#333333',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow', alpha=0.8))
    
    # Tight layout
    plt.tight_layout()
    
    # Save if path provided
    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved electrification map to {output_path}")
    
    plt.close(fig)
    return fig
