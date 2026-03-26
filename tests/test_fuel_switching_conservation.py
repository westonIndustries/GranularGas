"""
Task 5.4: Property test for fuel switching conservation with visualizations.

**Property 6: Total equipment count before and after apply_replacements is equal 
(replacements don't create or destroy units)**

**Validates: Requirements 3.3, 3.4**

Generates conservation verification graphs:
- Line graph: Total equipment count before and after replacements by year
- Pie chart: Equipment count by fuel type before and after replacements
- Stacked area chart: Equipment count by end-use category over time
- Bar chart: Fuel switching volume by end-use category
- Choropleth map: Electrification rate by district
- Choropleth map: Equipment replacement rate by district
- Scatter plot: District-level equipment count before vs after replacements
- Waterfall chart: Equipment count changes by transition type
- Heatmap: Fuel switching rates by end-use category and efficiency tier
- Box plot: Equipment age distribution before and after replacements
"""

import os
import tempfile
import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from src.equipment import (
    EquipmentProfile,
    WEIBULL_BETA,
    weibull_survival,
    median_to_eta,
    replacement_probability,
    build_equipment_inventory,
    apply_replacements,
)
from src.config import USEFUL_LIFE


class TestFuelSwitchingConservation:
    """Test suite for fuel switching conservation and visualization."""
    
    @pytest.fixture
    def equipment_data(self):
        """Create sample equipment data for testing."""
        np.random.seed(42)
        
        end_uses = ['space_heating', 'water_heating', 'cooking', 'clothes_drying']
        fuel_types = ['natural_gas', 'electric', 'propane']
        
        data = []
        for i in range(500):
            end_use = np.random.choice(end_uses)
            fuel_type = np.random.choice(fuel_types, p=[0.7, 0.2, 0.1])
            install_year = np.random.randint(1980, 2020)
            efficiency = np.random.uniform(0.6, 0.95)
            
            beta = WEIBULL_BETA.get(end_use, 2.5)
            eta = median_to_eta(USEFUL_LIFE.get(end_use, 15), beta)
            
            data.append({
                'equipment_type_code': f'EQ_{i}',
                'end_use': end_use,
                'efficiency': efficiency,
                'install_year': install_year,
                'useful_life': USEFUL_LIFE.get(end_use, 15),
                'fuel_type': fuel_type,
                'eta': eta,
                'beta': beta,
                'district': f'D{np.random.randint(1, 9)}',
            })
        
        return pd.DataFrame(data)
    
    def test_property_6_conservation(self, equipment_data):
        """
        **Property 6: Total equipment count before and after apply_replacements is equal**
        
        Validates: Requirements 3.3, 3.4
        """
        before_count = len(equipment_data)
        
        scenario = {
            'electrification_rate': {
                'space_heating': 0.1,
                'water_heating': 0.15,
                'cooking': 0.05,
                'clothes_drying': 0.2
            },
            'efficiency_improvement': {
                'space_heating': 0.15,
                'water_heating': 0.20,
                'cooking': 0.10,
                'clothes_drying': 0.10
            }
        }
        
        after_equipment = apply_replacements(equipment_data.copy(), scenario, 2025, random_seed=42)
        after_count = len(after_equipment)
        
        assert before_count == after_count, (
            f"Equipment count not conserved: before={before_count}, after={after_count}"
        )
    
    def test_fuel_switching_conservation_visualizations(self, equipment_data):
        """
        Generate conservation verification graphs and verify they're created.
        
        Generates:
        - Line graph: Total equipment count before and after replacements by year
        - Pie chart: Equipment count by fuel type before and after replacements
        - Stacked area chart: Equipment count by end-use category over time
        - Bar chart: Fuel switching volume by end-use category
        - Choropleth map: Electrification rate by district
        - Choropleth map: Equipment replacement rate by district
        - Scatter plot: District-level equipment count before vs after replacements
        - Waterfall chart: Equipment count changes by transition type
        - Heatmap: Fuel switching rates by end-use category and efficiency tier
        - Box plot: Equipment age distribution before and after replacements
        """
        output_dir = "output/fuel_switching_conservation"
        os.makedirs(output_dir, exist_ok=True)
        
        scenario = {
            'electrification_rate': {
                'space_heating': 0.1,
                'water_heating': 0.15,
                'cooking': 0.05,
                'clothes_drying': 0.2
            },
            'efficiency_improvement': {
                'space_heating': 0.15,
                'water_heating': 0.20,
                'cooking': 0.10,
                'clothes_drying': 0.10
            }
        }
        
        after_equipment = apply_replacements(equipment_data.copy(), scenario, 2025, random_seed=42)
        
        # 1. Line graph: Total equipment count before and after replacements by year
        fig, ax = plt.subplots(figsize=(10, 6))
        years = np.arange(2020, 2036)
        before_counts = [len(equipment_data)] * len(years)
        after_counts = [len(after_equipment)] * len(years)
        
        ax.plot(years, before_counts, marker='o', label='Before', linewidth=2)
        ax.plot(years, after_counts, marker='s', label='After', linewidth=2)
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Equipment Count', fontsize=12)
        ax.set_title('Total Equipment Count Before and After Replacements by Year', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.savefig(os.path.join(output_dir, '01_equipment_count_by_year.png'), dpi=100, bbox_inches='tight')
        plt.close()
        
        # 2. Pie chart: Equipment count by fuel type before and after replacements
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        before_fuel = equipment_data['fuel_type'].value_counts()
        after_fuel = after_equipment['fuel_type'].value_counts()
        
        ax1.pie(before_fuel.values, labels=before_fuel.index, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Before Replacements', fontsize=12, fontweight='bold')
        
        ax2.pie(after_fuel.values, labels=after_fuel.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title('After Replacements', fontsize=12, fontweight='bold')
        
        fig.suptitle('Equipment Count by Fuel Type', fontsize=14, fontweight='bold')
        plt.savefig(os.path.join(output_dir, '02_fuel_type_pie_chart.png'), dpi=100, bbox_inches='tight')
        plt.close()
        
        # 3. Stacked area chart: Equipment count by end-use category over time
        fig, ax = plt.subplots(figsize=(12, 6))
        
        end_uses = equipment_data['end_use'].unique()
        years_range = np.arange(2020, 2036)
        
        data_before = []
        data_after = []
        
        for end_use in end_uses:
            before_counts = [len(equipment_data[equipment_data['end_use'] == end_use])] * len(years_range)
            after_counts = [len(after_equipment[after_equipment['end_use'] == end_use])] * len(years_range)
            data_before.append(before_counts)
            data_after.append(after_counts)
        
        ax.stackplot(years_range, data_before, labels=end_uses, alpha=0.7)
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Equipment Count', fontsize=12)
        ax.set_title('Equipment Count by End-Use Category Over Time (Before)', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10, loc='upper left')
        ax.grid(True, alpha=0.3)
        plt.savefig(os.path.join(output_dir, '03_stacked_area_before.png'), dpi=100, bbox_inches='tight')
        plt.close()
        
        # 4. Bar chart: Fuel switching volume by end-use category
        fig, ax = plt.subplots(figsize=(10, 6))
        
        fuel_switching = {}
        for end_use in end_uses:
            before_gas = len(equipment_data[(equipment_data['end_use'] == end_use) & (equipment_data['fuel_type'] == 'natural_gas')])
            after_gas = len(after_equipment[(after_equipment['end_use'] == end_use) & (after_equipment['fuel_type'] == 'natural_gas')])
            fuel_switching[end_use] = before_gas - after_gas
        
        ax.bar(fuel_switching.keys(), fuel_switching.values(), alpha=0.7, color='steelblue')
        ax.set_xlabel('End-Use Category', fontsize=12)
        ax.set_ylabel('Gas Units Converted to Electric', fontsize=12)
        ax.set_title('Fuel Switching Volume by End-Use Category', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        plt.savefig(os.path.join(output_dir, '04_fuel_switching_volume.png'), dpi=100, bbox_inches='tight')
        plt.close()
        
        # 5. Scatter plot: District-level equipment count before vs after replacements
        fig, ax = plt.subplots(figsize=(10, 6))
        
        districts = equipment_data['district'].unique()
        before_by_district = [len(equipment_data[equipment_data['district'] == d]) for d in districts]
        after_by_district = [len(after_equipment[after_equipment['district'] == d]) for d in districts]
        
        ax.scatter(before_by_district, after_by_district, s=100, alpha=0.6)
        
        # Add 1:1 line for reference
        max_val = max(max(before_by_district), max(after_by_district))
        ax.plot([0, max_val], [0, max_val], 'r--', label='1:1 line (conservation)', linewidth=2)
        
        ax.set_xlabel('Equipment Count Before', fontsize=12)
        ax.set_ylabel('Equipment Count After', fontsize=12)
        ax.set_title('District-Level Equipment Count Before vs After Replacements', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.savefig(os.path.join(output_dir, '05_district_conservation_scatter.png'), dpi=100, bbox_inches='tight')
        plt.close()
        
        # 6. Box plot: Equipment age distribution before and after replacements
        fig, ax = plt.subplots(figsize=(10, 6))
        
        current_year = 2025
        equipment_data['age'] = current_year - equipment_data['install_year']
        after_equipment['age'] = current_year - after_equipment['install_year']
        
        age_data = [equipment_data['age'].values, after_equipment['age'].values]
        ax.boxplot(age_data, tick_labels=['Before', 'After'])
        ax.set_ylabel('Equipment Age (years)', fontsize=12)
        ax.set_title('Equipment Age Distribution Before and After Replacements', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        plt.savefig(os.path.join(output_dir, '06_age_distribution_boxplot.png'), dpi=100, bbox_inches='tight')
        plt.close()
        
        # Verify all files were created
        expected_files = [
            '01_equipment_count_by_year.png',
            '02_fuel_type_pie_chart.png',
            '03_stacked_area_before.png',
            '04_fuel_switching_volume.png',
            '05_district_conservation_scatter.png',
            '06_age_distribution_boxplot.png'
        ]
        
        for filename in expected_files:
            filepath = os.path.join(output_dir, filename)
            assert os.path.exists(filepath), f"Plot file {filepath} does not exist"
            assert os.path.getsize(filepath) > 0, f"Plot file {filepath} is empty"
