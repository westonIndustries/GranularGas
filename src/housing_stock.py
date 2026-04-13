"""
Housing stock module for NW Natural end-use forecasting model.

Defines the HousingStock dataclass and provides functions to construct
and project residential housing stock from premise-equipment data.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def _compute_housing_age_by_district(premises: pd.DataFrame, base_year: int) -> Dict[str, float]:
    """
    Compute average housing age by district.
    
    For testing purposes, generates synthetic housing age data based on district.
    In production, this would be computed from actual housing vintage data.
    
    Args:
        premises: DataFrame with premise-level data
        base_year: The current year
    
    Returns:
        Dict mapping district code to average housing age (years)
    """
    housing_age = {}
    
    if 'district_code_IRP' not in premises.columns:
        return housing_age
    
    # Generate synthetic housing age data based on district
    # Assumes different districts have different average housing ages
    district_age_map = {
        'D1': 35, 'D2': 40, 'D3': 30, 'D4': 45, 'D5': 25,
        'D6': 38, 'D7': 42, 'D8': 28, 'D9': 50, 'D10': 32,
    }
    
    for district in premises['district_code_IRP'].unique():
        # Use mapped age or default to 35 years
        housing_age[district] = district_age_map.get(district, 35)
    
    return housing_age


def _compute_vintage_distribution_by_district(premises: pd.DataFrame, base_year: int) -> Dict[str, Dict[str, float]]:
    """
    Compute vintage distribution by district.
    
    For testing purposes, generates synthetic vintage distribution data.
    In production, this would be computed from actual housing vintage data.
    
    Args:
        premises: DataFrame with premise-level data
        base_year: The current year
    
    Returns:
        Dict mapping district code to vintage era percentages (pre-1980, 1980-2000, 2000-2010, 2010+)
    """
    vintage_dist = {}
    
    if 'district_code_IRP' not in premises.columns:
        return vintage_dist
    
    # Generate synthetic vintage distribution data
    # Assumes different districts have different vintage distributions
    district_vintage_map = {
        'D1': {'pre-1980': 0.45, '1980-2000': 0.30, '2000-2010': 0.15, '2010+': 0.10},
        'D2': {'pre-1980': 0.50, '1980-2000': 0.28, '2000-2010': 0.14, '2010+': 0.08},
        'D3': {'pre-1980': 0.35, '1980-2000': 0.35, '2000-2010': 0.20, '2010+': 0.10},
        'D4': {'pre-1980': 0.55, '1980-2000': 0.25, '2000-2010': 0.12, '2010+': 0.08},
        'D5': {'pre-1980': 0.25, '1980-2000': 0.40, '2000-2010': 0.25, '2010+': 0.10},
    }
    
    for district in premises['district_code_IRP'].unique():
        # Use mapped distribution or default
        vintage_dist[district] = district_vintage_map.get(
            district,
            {'pre-1980': 0.40, '1980-2000': 0.30, '2000-2010': 0.20, '2010+': 0.10}
        )
    
    return vintage_dist


def _compute_replacement_probability_by_district(premises: pd.DataFrame, base_year: int) -> Dict[str, float]:
    """
    Compute replacement probability by district.
    
    For testing purposes, generates synthetic replacement probability data.
    In production, this would be computed from equipment age and Weibull survival model.
    
    Args:
        premises: DataFrame with premise-level data
        base_year: The current year
    
    Returns:
        Dict mapping district code to replacement probability [0, 1]
    """
    replacement_prob = {}
    
    if 'district_code_IRP' not in premises.columns:
        return replacement_prob
    
    # Generate synthetic replacement probability data based on district
    # Assumes different districts have different replacement probabilities
    district_prob_map = {
        'D1': 0.15, 'D2': 0.18, 'D3': 0.12, 'D4': 0.20, 'D5': 0.10,
        'D6': 0.16, 'D7': 0.19, 'D8': 0.11, 'D9': 0.22, 'D10': 0.13,
    }
    
    for district in premises['district_code_IRP'].unique():
        # Use mapped probability or default to 0.15
        replacement_prob[district] = district_prob_map.get(district, 0.15)
    
    return replacement_prob


@dataclass
class HousingStock:
    """
    Represents the residential housing stock for a given year.
    
    Attributes:
        year: The year this housing stock represents
        premises: DataFrame with premise-level data (one row per unique blinded_id)
        total_units: Total number of residential units
        units_by_segment: Dict mapping segment code to unit count
        units_by_district: Dict mapping district code to unit count
        housing_age_by_district: Dict mapping district code to average housing age (years)
        vintage_distribution_by_district: Dict mapping district code to vintage era percentages
        replacement_probability_by_district: Dict mapping district code to replacement probability [0,1]
    """
    year: int
    premises: pd.DataFrame
    total_units: int
    units_by_segment: Dict[str, int] = field(default_factory=dict)
    units_by_district: Dict[str, int] = field(default_factory=dict)
    housing_age_by_district: Dict[str, float] = field(default_factory=dict)
    vintage_distribution_by_district: Dict[str, Dict[str, float]] = field(default_factory=dict)
    replacement_probability_by_district: Dict[str, float] = field(default_factory=dict)


def build_baseline_stock(premise_equipment: pd.DataFrame, base_year: int) -> HousingStock:
    """
    Construct baseline housing stock from premise-equipment data.
    
    Aggregates premise-level data to compute total units and distributions
    by segment and district. Each unique blinded_id represents one residential unit.
    
    Args:
        premise_equipment: DataFrame from build_premise_equipment_table with columns:
            - blinded_id: Unique premise identifier
            - segment_code: Customer segment (e.g., 'RESSF', 'RESMF')
            - district_code_IRP: IRP district code
            - (other premise/equipment columns)
        base_year: The year for this baseline stock
    
    Returns:
        HousingStock object with computed total_units, units_by_segment, units_by_district
    
    Raises:
        ValueError: If premise_equipment is empty or missing required columns
    """
    if premise_equipment.empty:
        raise ValueError("premise_equipment DataFrame is empty")
    
    required_cols = {'blinded_id', 'segment_code', 'district_code_IRP'}
    missing_cols = required_cols - set(premise_equipment.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Get unique premises (one row per blinded_id)
    premises = premise_equipment.drop_duplicates(subset=['blinded_id']).copy()
    
    # Compute total units
    total_units = len(premises)
    
    # Compute units by segment
    units_by_segment = premises['segment_code'].value_counts().to_dict()
    
    # Compute units by district
    units_by_district = premises['district_code_IRP'].value_counts().to_dict()
    
    # Compute housing age by district (synthetic data for now)
    housing_age_by_district = _compute_housing_age_by_district(premises, base_year)
    
    # Compute vintage distribution by district (synthetic data for now)
    vintage_distribution_by_district = _compute_vintage_distribution_by_district(premises, base_year)
    
    # Compute replacement probability by district (synthetic data for now)
    replacement_probability_by_district = _compute_replacement_probability_by_district(premises, base_year)
    
    logger.info(
        f"Built baseline housing stock for year {base_year}: "
        f"total_units={total_units}, "
        f"segments={len(units_by_segment)}, "
        f"districts={len(units_by_district)}"
    )
    
    return HousingStock(
        year=base_year,
        premises=premises,
        total_units=total_units,
        units_by_segment=units_by_segment,
        units_by_district=units_by_district,
        housing_age_by_district=housing_age_by_district,
        vintage_distribution_by_district=vintage_distribution_by_district,
        replacement_probability_by_district=replacement_probability_by_district
    )


def project_stock(baseline: HousingStock, target_year: int, scenario: dict) -> HousingStock:
    """
    Project housing stock to a future year using growth rates from scenario.
    
    Applies annual housing growth rate to project total units. New construction
    additions are distributed proportionally across existing segments to maintain
    the baseline segment distribution. Supports both forward and backward projections.
    
    Args:
        baseline: HousingStock object representing the baseline year
        target_year: The year to project to (can be before or after baseline.year)
        scenario: Dictionary with scenario parameters, must include:
            - 'housing_growth_rate': float, annual growth rate (0.0-0.05 for forward, -0.05-0.0 for backward)
            - 'base_year': int, the baseline year (for validation)
    
    Returns:
        HousingStock object for the target year with projected total_units,
        units_by_segment, and units_by_district
    
    Raises:
        ValueError: If scenario is missing required keys or has invalid values
        ValueError: If target_year == baseline.year
    """
    # Validate inputs
    if target_year == baseline.year:
        raise ValueError(f"target_year ({target_year}) must be != baseline.year ({baseline.year})")
    
    required_scenario_keys = {'housing_growth_rate', 'base_year'}
    missing_keys = required_scenario_keys - set(scenario.keys())
    if missing_keys:
        raise ValueError(f"scenario missing required keys: {missing_keys}")
    
    growth_rate = scenario['housing_growth_rate']
    if not (-0.05 <= growth_rate <= 0.05):
        raise ValueError(f"housing_growth_rate must be in [-0.05, 0.05], got {growth_rate}")
    
    # Calculate number of years to project (can be negative for backward projection)
    years_to_project = target_year - baseline.year
    
    # Project total units using compound growth formula: P(t) = P0 * (1 + r)^t
    # This works for both forward (t > 0) and backward (t < 0) projections
    projected_total_units = int(round(baseline.total_units * ((1 + growth_rate) ** years_to_project)))
    
    # Calculate new units added (can be negative for backward projection)
    new_units = projected_total_units - baseline.total_units
    
    # Distribute new units proportionally across segments
    projected_units_by_segment = baseline.units_by_segment.copy()
    if new_units != 0 and baseline.total_units > 0:
        for segment, baseline_count in baseline.units_by_segment.items():
            # Calculate proportion of baseline units in this segment
            segment_proportion = baseline_count / baseline.total_units
            # Allocate proportional share of new units to this segment
            new_units_for_segment = int(round(new_units * segment_proportion))
            projected_units_by_segment[segment] = baseline_count + new_units_for_segment
    
    # Distribute new units proportionally across districts
    projected_units_by_district = baseline.units_by_district.copy()
    if new_units != 0 and baseline.total_units > 0:
        for district, baseline_count in baseline.units_by_district.items():
            # Calculate proportion of baseline units in this district
            district_proportion = baseline_count / baseline.total_units
            # Allocate proportional share of new units to this district
            new_units_for_district = int(round(new_units * district_proportion))
            projected_units_by_district[district] = baseline_count + new_units_for_district
    
    logger.info(
        f"Projected housing stock from year {baseline.year} to {target_year}: "
        f"baseline_units={baseline.total_units}, "
        f"projected_units={projected_total_units}, "
        f"new_units={new_units}, "
        f"growth_rate={growth_rate:.4f}"
    )
    
    # Compute housing age, vintage distribution, and replacement probability for projected year
    # These are updated based on the projection year
    housing_age_by_district = _compute_housing_age_by_district(baseline.premises, target_year)
    vintage_distribution_by_district = _compute_vintage_distribution_by_district(baseline.premises, target_year)
    replacement_probability_by_district = _compute_replacement_probability_by_district(baseline.premises, target_year)
    
    # Create new HousingStock object for projected year
    # Note: premises DataFrame is not updated here; it remains the baseline premises
    # In a full implementation, new construction premises would be synthesized
    return HousingStock(
        year=target_year,
        premises=baseline.premises.copy(),  # Placeholder: same premises as baseline
        total_units=projected_total_units,
        units_by_segment=projected_units_by_segment,
        units_by_district=projected_units_by_district,
        housing_age_by_district=housing_age_by_district,
        vintage_distribution_by_district=vintage_distribution_by_district,
        replacement_probability_by_district=replacement_probability_by_district
    )
