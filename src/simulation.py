"""
End-use energy simulation module for NW Natural End-Use Forecasting Model.

Provides functions for simulating annual energy consumption by end-use:
- Space heating (weather-driven via HDD)
- Water heating (weather-driven via temperature delta)
- Baseload (flat annual consumption)

Each function takes equipment characteristics and weather data to compute
annual therms consumed for that end-use.
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Tuple
import logging

from src import config
from src.equipment import EquipmentProfile

logger = logging.getLogger(__name__)


def simulate_space_heating(
    equipment: EquipmentProfile,
    annual_hdd: float,
    heating_factor: float = 1.0
) -> float:
    """
    Simulate annual space heating consumption.
    
    Space heating demand is driven by Heating Degree Days (HDD) and equipment efficiency.
    
    Formula:
        annual_therms = (annual_hdd * heating_factor) / efficiency
    
    Where:
    - annual_hdd: Total heating degree days for the year (base 65°F)
    - heating_factor: Scaling factor to convert HDD to therms (accounts for building envelope, etc.)
    - efficiency: Equipment efficiency (AFUE for furnaces, COP for heat pumps)
    
    Args:
        equipment: EquipmentProfile with efficiency and fuel_type
        annual_hdd: Annual HDD total (float, >= 0)
        heating_factor: Scaling factor from HDD to therms (default 1.0)
                       Typical range: 0.5-2.0 depending on building envelope
    
    Returns:
        Annual space heating consumption in therms (float, >= 0)
    
    Raises:
        ValueError: If annual_hdd < 0 or heating_factor <= 0
        TypeError: If equipment is not an EquipmentProfile
    """
    if not isinstance(equipment, EquipmentProfile):
        raise TypeError(f"equipment must be EquipmentProfile, got {type(equipment)}")
    
    if annual_hdd < 0:
        raise ValueError(f"annual_hdd must be >= 0, got {annual_hdd}")
    
    if heating_factor <= 0:
        raise ValueError(f"heating_factor must be > 0, got {heating_factor}")
    
    # Efficiency must be positive
    if equipment.efficiency <= 0:
        logger.warning(
            f"Equipment {equipment.equipment_type_code} has invalid efficiency "
            f"{equipment.efficiency}, using default"
        )
        efficiency = config.DEFAULT_EFFICIENCY.get(equipment.end_use, 0.80)
    else:
        efficiency = equipment.efficiency
    
    # Compute therms: HDD * factor / efficiency
    # Higher efficiency -> lower therms (inverse relationship)
    annual_therms = (annual_hdd * heating_factor) / efficiency
    
    # Ensure non-negative result
    annual_therms = max(0.0, annual_therms)
    
    return float(annual_therms)


def simulate_water_heating(
    equipment: EquipmentProfile,
    delta_t: float,
    gallons_per_day: float = 64.0
) -> float:
    """
    Simulate annual water heating consumption.
    
    Water heating demand is driven by the temperature rise needed to heat
    incoming cold water to target hot water temperature.
    
    Formula:
        annual_therms = (gallons_per_day * delta_t * days_per_year) / (efficiency * BTU_per_therm)
    
    Where:
    - gallons_per_day: Daily hot water consumption (gallons)
    - delta_t: Temperature rise needed (°F) = target_temp - cold_water_temp
    - efficiency: Equipment efficiency (EF for water heaters)
    - BTU_per_therm: 100,000 BTU/therm (standard conversion)
    - days_per_year: 365 days
    
    Simplified formula (using standard conversion factors):
        annual_therms = (gallons_per_day * delta_t * 365) / (efficiency * 100000)
    
    Args:
        equipment: EquipmentProfile with efficiency and fuel_type
        delta_t: Temperature rise in Fahrenheit (float, > 0)
        gallons_per_day: Daily hot water consumption in gallons (default 64.0)
    
    Returns:
        Annual water heating consumption in therms (float, >= 0)
    
    Raises:
        ValueError: If delta_t <= 0 or gallons_per_day <= 0
        TypeError: If equipment is not an EquipmentProfile
    """
    if not isinstance(equipment, EquipmentProfile):
        raise TypeError(f"equipment must be EquipmentProfile, got {type(equipment)}")
    
    if delta_t <= 0:
        raise ValueError(f"delta_t must be > 0, got {delta_t}")
    
    if gallons_per_day <= 0:
        raise ValueError(f"gallons_per_day must be > 0, got {gallons_per_day}")
    
    # Efficiency must be positive
    if equipment.efficiency <= 0:
        logger.warning(
            f"Equipment {equipment.equipment_type_code} has invalid efficiency "
            f"{equipment.efficiency}, using default"
        )
        efficiency = config.DEFAULT_EFFICIENCY.get(equipment.end_use, 0.60)
    else:
        efficiency = equipment.efficiency
    
    # Standard conversion: 1 therm = 100,000 BTU
    # Energy to heat water: BTU = gallons * 8.34 lb/gal * 1 BTU/lb/°F * delta_t
    # Simplified: BTU per gallon per degree = 8.34
    BTU_PER_GALLON_PER_DEGREE = 8.34
    BTU_PER_THERM = 100000.0
    DAYS_PER_YEAR = 365.0
    
    # Compute annual therms
    annual_btu = gallons_per_day * BTU_PER_GALLON_PER_DEGREE * delta_t * DAYS_PER_YEAR
    annual_therms = annual_btu / (efficiency * BTU_PER_THERM)
    
    # Ensure non-negative result
    annual_therms = max(0.0, annual_therms)
    
    return float(annual_therms)


def simulate_baseload(
    equipment: EquipmentProfile,
    annual_consumption: float
) -> float:
    """
    Simulate annual baseload (non-weather-sensitive) consumption.
    
    Baseload end-uses (cooking, drying, fireplaces, other) consume a relatively
    constant amount of energy year-round, independent of weather.
    
    Formula:
        annual_therms = annual_consumption / efficiency
    
    Where:
    - annual_consumption: Base annual consumption in therms (before efficiency adjustment)
    - efficiency: Equipment efficiency
    
    Args:
        equipment: EquipmentProfile with efficiency and fuel_type
        annual_consumption: Base annual consumption in therms (float, >= 0)
    
    Returns:
        Annual baseload consumption in therms (float, >= 0)
    
    Raises:
        ValueError: If annual_consumption < 0
        TypeError: If equipment is not an EquipmentProfile
    """
    if not isinstance(equipment, EquipmentProfile):
        raise TypeError(f"equipment must be EquipmentProfile, got {type(equipment)}")
    
    if annual_consumption < 0:
        raise ValueError(f"annual_consumption must be >= 0, got {annual_consumption}")
    
    # Efficiency must be positive
    if equipment.efficiency <= 0:
        logger.warning(
            f"Equipment {equipment.equipment_type_code} has invalid efficiency "
            f"{equipment.efficiency}, using default"
        )
        efficiency = config.DEFAULT_EFFICIENCY.get(equipment.end_use, 0.70)
    else:
        efficiency = equipment.efficiency
    
    # Compute therms: consumption / efficiency
    # Higher efficiency -> lower therms (inverse relationship)
    annual_therms = annual_consumption / efficiency
    
    # Ensure non-negative result
    annual_therms = max(0.0, annual_therms)
    
    return float(annual_therms)



def simulate_all_end_uses(
    premise_equipment: pd.DataFrame,
    weather_data: pd.DataFrame,
    water_temp_data: pd.DataFrame,
    baseload_factors: Dict[str, float],
    year: int = config.BASE_YEAR,
    heating_factor: float = 1.0,
    target_hot_water_temp: float = config.DEFAULT_HOT_WATER_TEMP,
    gallons_per_day: float = config.DEFAULT_DAILY_HOT_WATER_GALLONS
) -> pd.DataFrame:
    """
    Orchestrate end-use energy simulation for all premises and end-uses.
    
    This function:
    1. Iterates through each premise and its equipment
    2. Assigns weather station based on district
    3. Retrieves weather data (HDD, delta-T) for that station
    4. Dispatches to appropriate simulation function (space_heating, water_heating, baseload)
    5. Returns aggregated results by premise and end-use
    
    Args:
        premise_equipment: DataFrame with columns:
            - blinded_id: Premise identifier
            - equipment_type_code: Equipment code
            - end_use: End-use category (space_heating, water_heating, cooking, etc.)
            - efficiency: Equipment efficiency (0-1 range)
            - install_year: Year installed
            - useful_life: Equipment useful life (years)
            - fuel_type: Fuel type (natural_gas, electric, etc.)
            - district_code_IRP: District code for weather station assignment
        
        weather_data: DataFrame with columns:
            - site_id: Weather station ICAO code (e.g., 'KPDX')
            - date: Date (datetime)
            - daily_avg_temp: Daily average temperature (°F)
        
        water_temp_data: DataFrame with columns:
            - date: Date (datetime)
            - cold_water_temp: Cold water temperature (°F)
        
        baseload_factors: Dictionary mapping end_use -> annual_consumption (therms)
            Example: {'cooking': 30.0, 'clothes_drying': 20.0, 'fireplace': 55.0}
        
        year: Calendar year for simulation (default: BASE_YEAR)
        
        heating_factor: Scaling factor for space heating (default 1.0)
            Accounts for building envelope characteristics
        
        target_hot_water_temp: Target hot water temperature in °F (default 120°F)
        
        gallons_per_day: Daily hot water consumption in gallons (default 64.0)
    
    Returns:
        DataFrame with columns:
            - blinded_id: Premise identifier
            - end_use: End-use category
            - annual_therms: Simulated annual consumption (therms)
            - efficiency: Equipment efficiency used
            - year: Simulation year
        
        One row per premise per end-use (no double-counting).
        Rows with zero therms are included (non-negative constraint).
    
    Raises:
        ValueError: If required columns missing from input DataFrames
        KeyError: If district_code_IRP not found in DISTRICT_WEATHER_MAP
    """
    from src.weather import compute_annual_hdd, compute_water_heating_delta, assign_weather_station
    
    # Validate input DataFrames
    required_premise_cols = {
        'blinded_id', 'equipment_type_code', 'end_use', 'efficiency',
        'install_year', 'useful_life', 'fuel_type', 'district_code_IRP'
    }
    if not required_premise_cols.issubset(premise_equipment.columns):
        missing = required_premise_cols - set(premise_equipment.columns)
        raise ValueError(f"premise_equipment missing columns: {missing}")
    
    required_weather_cols = {'site_id', 'date', 'daily_avg_temp'}
    if not required_weather_cols.issubset(weather_data.columns):
        missing = required_weather_cols - set(weather_data.columns)
        raise ValueError(f"weather_data missing columns: {missing}")
    
    required_water_cols = {'date', 'cold_water_temp'}
    if not required_water_cols.issubset(water_temp_data.columns):
        missing = required_water_cols - set(water_temp_data.columns)
        raise ValueError(f"water_temp_data missing columns: {missing}")
    
    # Ensure date columns are datetime
    weather_data = weather_data.copy()
    water_temp_data = water_temp_data.copy()
    weather_data['date'] = pd.to_datetime(weather_data['date'])
    water_temp_data['date'] = pd.to_datetime(water_temp_data['date'])
    
    results = []
    
    # Group by premise to avoid redundant weather lookups
    for blinded_id, premise_group in premise_equipment.groupby('blinded_id'):
        # Get district code (should be same for all equipment in premise)
        district_code = premise_group['district_code_IRP'].iloc[0]
        
        # Assign weather station
        try:
            weather_station = assign_weather_station(district_code)
        except KeyError as e:
            logger.warning(f"Premise {blinded_id}: {e}")
            continue
        
        # Compute annual HDD for this premise's weather station
        try:
            annual_hdd = compute_annual_hdd(weather_data, weather_station, year)
        except ValueError as e:
            logger.warning(f"Premise {blinded_id} ({weather_station}): {e}")
            annual_hdd = 0.0
        
        # Compute water heating delta-T
        try:
            delta_t = compute_water_heating_delta(water_temp_data, target_hot_water_temp, year)
        except ValueError as e:
            logger.warning(f"Premise {blinded_id}: {e}")
            delta_t = 0.0
        
        # Simulate each end-use for this premise
        for _, row in premise_group.iterrows():
            equipment = EquipmentProfile(
                equipment_type_code=row['equipment_type_code'],
                end_use=row['end_use'],
                efficiency=row['efficiency'],
                install_year=row['install_year'],
                useful_life=row['useful_life'],
                fuel_type=row['fuel_type']
            )
            
            end_use = row['end_use']
            
            # Dispatch to appropriate simulation function
            if end_use == 'space_heating':
                annual_therms = simulate_space_heating(equipment, annual_hdd, heating_factor)
            
            elif end_use == 'water_heating':
                annual_therms = simulate_water_heating(
                    equipment, delta_t, gallons_per_day
                )
            
            elif end_use in baseload_factors:
                # Baseload end-uses: cooking, clothes_drying, fireplace, other
                base_consumption = baseload_factors[end_use]
                annual_therms = simulate_baseload(equipment, base_consumption)
            
            else:
                # Unknown end-use: log warning and skip
                logger.warning(f"Unknown end-use '{end_use}' for premise {blinded_id}")
                continue
            
            # Append result
            results.append({
                'blinded_id': blinded_id,
                'end_use': end_use,
                'annual_therms': annual_therms,
                'efficiency': equipment.efficiency,
                'year': year
            })
    
    # Convert to DataFrame
    results_df = pd.DataFrame(results)
    
    if results_df.empty:
        logger.warning("No simulation results generated")
        return pd.DataFrame(columns=['blinded_id', 'end_use', 'annual_therms', 'efficiency', 'year'])
    
    return results_df
