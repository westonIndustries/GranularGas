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
    """
    year: int
    premises: pd.DataFrame
    total_units: int
    units_by_segment: Dict[str, int] = field(default_factory=dict)
    units_by_district: Dict[str, int] = field(default_factory=dict)


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
        units_by_district=units_by_district
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
    
    # Create new HousingStock object for projected year
    # Note: premises DataFrame is not updated here; it remains the baseline premises
    # In a full implementation, new construction premises would be synthesized
    return HousingStock(
        year=target_year,
        premises=baseline.premises.copy(),  # Placeholder: same premises as baseline
        total_units=projected_total_units,
        units_by_segment=projected_units_by_segment,
        units_by_district=projected_units_by_district
    )
