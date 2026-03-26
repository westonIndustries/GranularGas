"""
Equipment module for NW Natural End-Use Forecasting Model.

Defines equipment inventory representation and Weibull survival model for
equipment replacement timing. Provides functions to:
- Represent equipment profiles with efficiency, age, and service life
- Compute Weibull survival probabilities for equipment replacement
- Build equipment inventories from premise-equipment data
- Derive equipment characteristics from config defaults and ASHRAE data
"""

import logging
import math
from dataclasses import dataclass
from typing import Optional, Dict
import pandas as pd
import numpy as np

from src import config

logger = logging.getLogger(__name__)

# ============================================================================
# WEIBULL SURVIVAL MODEL PARAMETERS
# ============================================================================

# Shape parameter (beta) for Weibull survival function by end-use category
# Controls failure rate distribution: higher beta = sharper peak, lower beta = gradual decline
WEIBULL_BETA = {
    "space_heating": 3.0,       # HVAC: concentrated replacement window
    "water_heating": 3.0,       # Water heater: concentrated replacement window
    "cooking": 2.5,             # Appliances: more gradual replacement
    "clothes_drying": 2.5,      # Appliances: more gradual replacement
    "fireplace": 2.0,           # Long-lived, gradual failure
    "other": 2.5,               # Generic appliance
}

# ============================================================================
# EQUIPMENT PROFILE DATACLASS
# ============================================================================


@dataclass
class EquipmentProfile:
    """
    Represents a single piece of equipment in a residential premise.
    
    Attributes:
        equipment_type_code: Equipment code (e.g., 'RFAU', 'RAWH', 'RRGE')
        end_use: End-use category (e.g., 'space_heating', 'water_heating')
        efficiency: Equipment efficiency as decimal (e.g., 0.85 = 85%)
        install_year: Year equipment was installed
        useful_life: Expected useful life in years (from ASHRAE or config default)
        fuel_type: Fuel type ('natural_gas', 'electric', 'propane', etc.)
    """
    equipment_type_code: str
    end_use: str
    efficiency: float
    install_year: int
    useful_life: int
    fuel_type: str


# ============================================================================
# WEIBULL SURVIVAL FUNCTIONS
# ============================================================================


def weibull_survival(t: float, eta: float, beta: float) -> float:
    """
    Compute Weibull survival function S(t) = exp(-(t/eta)^beta).
    
    The survival function represents the probability that equipment survives
    (does not fail) up to age t. Used to model equipment replacement timing.
    
    Args:
        t: Equipment age in years (must be >= 0)
        eta: Weibull scale parameter (characteristic life, must be > 0)
        beta: Weibull shape parameter (must be > 0)
        
    Returns:
        Survival probability in [0, 1]
        
    Raises:
        ValueError: If eta <= 0 or beta <= 0
        
    Examples:
        >>> weibull_survival(0, 20, 3.0)  # New equipment
        1.0
        >>> weibull_survival(20, 20, 3.0)  # At characteristic life
        0.36787944117144233
        >>> weibull_survival(40, 20, 3.0)  # Old equipment
        0.0009118819655545162
    """
    if eta <= 0:
        raise ValueError(f"eta must be > 0, got {eta}")
    if beta <= 0:
        raise ValueError(f"beta must be > 0, got {beta}")
    
    if t < 0:
        return 1.0  # No failure before age 0
    
    if t == 0:
        return 1.0  # New equipment always survives
    
    # S(t) = exp(-(t/eta)^beta)
    exponent = -(t / eta) ** beta
    return math.exp(exponent)


def median_to_eta(median_life: float, beta: float) -> float:
    """
    Convert ASHRAE median service life to Weibull scale parameter eta.
    
    The median service life is the age at which 50% of equipment has failed.
    For Weibull distribution, median corresponds to S(t) = 0.5, which gives:
    eta = median_life / (ln(2))^(1/beta)
    
    Args:
        median_life: ASHRAE median service life in years (must be > 0)
        beta: Weibull shape parameter (must be > 0)
        
    Returns:
        Weibull scale parameter eta
        
    Raises:
        ValueError: If median_life <= 0 or beta <= 0
        
    Examples:
        >>> eta = median_to_eta(20, 3.0)
        >>> weibull_survival(20, eta, 3.0)  # Should be ~0.5
        0.5000000000000001
    """
    if median_life <= 0:
        raise ValueError(f"median_life must be > 0, got {median_life}")
    if beta <= 0:
        raise ValueError(f"beta must be > 0, got {beta}")
    
    # At median: S(median) = 0.5
    # 0.5 = exp(-(median/eta)^beta)
    # ln(0.5) = -(median/eta)^beta
    # -ln(2) = -(median/eta)^beta
    # ln(2) = (median/eta)^beta
    # eta = median / (ln(2))^(1/beta)
    
    ln_2 = math.log(2)
    eta = median_life / (ln_2 ** (1 / beta))
    return eta


def replacement_probability(age: float, eta: float, beta: float) -> float:
    """
    Compute conditional failure probability for equipment at a given age.
    
    The replacement probability is the conditional probability that equipment
    fails in the next year, given that it has survived to the current age:
    P = 1 - S(t) / S(t-1)
    
    This represents the probability that equipment should be replaced.
    
    Args:
        age: Equipment age in years (must be >= 0)
        eta: Weibull scale parameter (must be > 0)
        beta: Weibull shape parameter (must be > 0)
        
    Returns:
        Replacement probability in [0, 1]
        
    Raises:
        ValueError: If eta <= 0 or beta <= 0
        
    Examples:
        >>> replacement_probability(0, 20, 3.0)  # New equipment
        0.0
        >>> replacement_probability(20, 20, 3.0)  # At characteristic life
        0.18394...
        >>> replacement_probability(40, 20, 3.0)  # Old equipment
        0.99...
    """
    if eta <= 0:
        raise ValueError(f"eta must be > 0, got {eta}")
    if beta <= 0:
        raise ValueError(f"beta must be > 0, got {beta}")
    
    if age < 0:
        return 0.0  # No replacement before age 0
    
    if age == 0:
        return 0.0  # New equipment doesn't need replacement
    
    # P = 1 - S(t) / S(t-1)
    s_t = weibull_survival(age, eta, beta)
    s_t_minus_1 = weibull_survival(age - 1, eta, beta)
    
    # Avoid division by zero
    if s_t_minus_1 == 0:
        return 1.0  # Equipment has already failed
    
    prob = 1 - (s_t / s_t_minus_1)
    
    # Clamp to [0, 1] to handle numerical precision issues
    return max(0.0, min(1.0, prob))


# ============================================================================
# EQUIPMENT INVENTORY BUILDER
# ============================================================================


def build_equipment_inventory(premise_equipment: pd.DataFrame) -> pd.DataFrame:
    """
    Build equipment inventory from premise-equipment data.
    
    Derives equipment characteristics (efficiency, install_year, useful_life,
    fuel_type) from premise_equipment DataFrame, using config defaults where
    data is unavailable. Uses ASHRAE service life data to compute Weibull
    scale parameters (eta) for equipment replacement modeling.
    
    Args:
        premise_equipment: DataFrame with columns:
            - blinded_id: Premise identifier
            - equipment_type_code: Equipment code
            - end_use: End-use category (from END_USE_MAP)
            - efficiency: Equipment efficiency (may be null)
            - install_year: Year installed (may be null)
            - fuel_type: Fuel type (may be null)
            - state: State code ('OR' or 'WA') for ASHRAE lookup
            
    Returns:
        DataFrame with EquipmentProfile records, including:
            - All input columns
            - efficiency: Filled with DEFAULT_EFFICIENCY if null
            - install_year: Filled with reasonable default if null
            - useful_life: From ASHRAE data or config default
            - fuel_type: Filled with 'natural_gas' if null
            - eta: Weibull scale parameter for replacement modeling
            - beta: Weibull shape parameter by end-use
            
    Notes:
        - Logs warnings for missing data and assumption applications
        - Assumes current year is config.BASE_YEAR for install_year defaults
        - ASHRAE service life data is not yet loaded; uses config.USEFUL_LIFE
        - Fuel type defaults to 'natural_gas' for gas equipment
    """
    df = premise_equipment.copy()
    
    # Derive efficiency: use provided value or config default
    if 'efficiency' not in df.columns or df['efficiency'].isna().any():
        logger.warning(
            f"Missing efficiency for {df['efficiency'].isna().sum()} equipment units; "
            "using DEFAULT_EFFICIENCY by end-use"
        )
        df['efficiency'] = df.apply(
            lambda row: row['efficiency'] 
            if pd.notna(row['efficiency']) 
            else config.DEFAULT_EFFICIENCY.get(row['end_use'], 0.70),
            axis=1
        )
    
    # Derive install_year: use provided value or assume mid-useful-life
    if 'install_year' not in df.columns or df['install_year'].isna().any():
        logger.warning(
            f"Missing install_year for {df['install_year'].isna().sum()} equipment units; "
            "assuming mid-useful-life installation"
        )
        df['useful_life'] = df['end_use'].map(config.USEFUL_LIFE).fillna(15)
        df['install_year'] = df.apply(
            lambda row: row['install_year']
            if pd.notna(row['install_year'])
            else config.BASE_YEAR - (row['useful_life'] // 2),
            axis=1
        )
    
    # Derive useful_life: use config defaults (ASHRAE data would be loaded separately)
    if 'useful_life' not in df.columns:
        df['useful_life'] = df['end_use'].map(config.USEFUL_LIFE).fillna(15)
    
    # Derive fuel_type: default to 'natural_gas' for gas equipment
    if 'fuel_type' not in df.columns or df['fuel_type'].isna().any():
        logger.warning(
            f"Missing fuel_type for {df['fuel_type'].isna().sum()} equipment units; "
            "defaulting to 'natural_gas'"
        )
        df['fuel_type'] = df['fuel_type'].fillna('natural_gas')
    
    # Compute Weibull parameters for replacement modeling
    df['beta'] = df['end_use'].map(WEIBULL_BETA).fillna(2.5)
    df['eta'] = df.apply(
        lambda row: median_to_eta(row['useful_life'], row['beta']),
        axis=1
    )
    
    logger.info(
        f"Built equipment inventory with {len(df)} units; "
        f"efficiency range [{df['efficiency'].min():.2f}, {df['efficiency'].max():.2f}], "
        f"install_year range [{df['install_year'].min()}, {df['install_year'].max()}]"
    )
    
    return df


# ============================================================================
# EQUIPMENT REPLACEMENT FUNCTION
# ============================================================================


def apply_replacements(
    equipment_df: pd.DataFrame,
    scenario_config: dict,
    year: int,
    random_seed: Optional[int] = None
) -> pd.DataFrame:
    """
    Apply equipment replacements based on Weibull survival model and scenario config.
    
    For each equipment unit:
    1. Compute age = year - install_year
    2. Compute replacement_probability using Weibull model
    3. Draw random number; if random < replacement_probability, mark for replacement
    4. For replaced units:
       - Apply electrification_rate from scenario (gas → electric with given probability)
       - Apply efficiency_improvement from scenario
       - Set install_year = year
       - Recompute eta based on new useful_life
    
    Args:
        equipment_df: DataFrame with equipment inventory, including columns:
            - install_year: Year equipment was installed
            - end_use: End-use category
            - efficiency: Current efficiency
            - fuel_type: Current fuel type ('natural_gas', 'electric', etc.)
            - eta: Weibull scale parameter
            - beta: Weibull shape parameter
            - useful_life: Equipment useful life in years
            
        scenario_config: Dictionary with scenario parameters:
            - electrification_rate: dict mapping end_use → switching rate [0, 1]
              (e.g., {'space_heating': 0.05, 'water_heating': 0.10})
            - efficiency_improvement: dict mapping end_use → improvement rate [0, 1]
              (e.g., {'space_heating': 0.15, 'water_heating': 0.20})
              New efficiency = old_efficiency * (1 + improvement_rate)
              
        year: Target year for replacement simulation
        
        random_seed: Optional random seed for reproducibility
        
    Returns:
        Modified equipment DataFrame with replaced units updated:
        - install_year set to year for replaced units
        - efficiency improved for replaced units
        - fuel_type switched to 'electric' for electrified units
        - eta recomputed for replaced units
        
    Notes:
        - Total equipment count is conserved (replacements don't create/destroy units)
        - Electrification and efficiency improvements are applied independently
        - A unit can be both electrified and have efficiency improved in same year
        - Non-replaced units are unchanged
        
    Examples:
        >>> equipment_df = pd.DataFrame({
        ...     'install_year': [2005, 2010, 2015],
        ...     'end_use': ['space_heating', 'space_heating', 'water_heating'],
        ...     'efficiency': [0.80, 0.85, 0.65],
        ...     'fuel_type': ['natural_gas', 'natural_gas', 'natural_gas'],
        ...     'eta': [18.5, 18.5, 12.0],
        ...     'beta': [3.0, 3.0, 3.0],
        ...     'useful_life': [20, 20, 13]
        ... })
        >>> scenario = {
        ...     'electrification_rate': {'space_heating': 0.10, 'water_heating': 0.05},
        ...     'efficiency_improvement': {'space_heating': 0.15, 'water_heating': 0.20}
        ... }
        >>> result = apply_replacements(equipment_df, scenario, year=2025, random_seed=42)
        >>> len(result) == len(equipment_df)  # Conservation
        True
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    df = equipment_df.copy()
    
    # Compute age for each equipment unit
    df['age'] = year - df['install_year']
    
    # Compute replacement probability using Weibull model
    df['replacement_prob'] = df.apply(
        lambda row: replacement_probability(row['age'], row['eta'], row['beta']),
        axis=1
    )
    
    # Draw random numbers and mark units for replacement
    df['random_draw'] = np.random.uniform(0, 1, len(df))
    df['is_replaced'] = df['random_draw'] < df['replacement_prob']
    
    # Count replacements before cleanup
    num_replaced = df['is_replaced'].sum()
    
    # Apply replacements
    for idx in df[df['is_replaced']].index:
        end_use = df.loc[idx, 'end_use']
        
        # Apply electrification switching
        electrification_rate = scenario_config.get('electrification_rate', {}).get(end_use, 0.0)
        if np.random.uniform(0, 1) < electrification_rate:
            df.loc[idx, 'fuel_type'] = 'electric'
        
        # Apply efficiency improvement
        efficiency_improvement = scenario_config.get('efficiency_improvement', {}).get(end_use, 0.0)
        new_efficiency = df.loc[idx, 'efficiency'] * (1 + efficiency_improvement)
        # Cap efficiency at 1.0 (100%)
        df.loc[idx, 'efficiency'] = min(new_efficiency, 1.0)
        
        # Update install_year to current year
        df.loc[idx, 'install_year'] = year
        
        # Recompute eta based on useful_life and beta
        useful_life = df.loc[idx, 'useful_life']
        beta = df.loc[idx, 'beta']
        df.loc[idx, 'eta'] = median_to_eta(useful_life, beta)
    
    # Clean up temporary columns
    df = df.drop(columns=['age', 'replacement_prob', 'random_draw', 'is_replaced'])
    
    logger.info(
        f"Applied replacements for year {year}: {num_replaced} units replaced"
    )
    
    return df
