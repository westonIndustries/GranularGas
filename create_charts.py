#!/usr/bin/env python3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# Load data
baseline_df = pd.read_csv('output/checkpoint_final/baseline_results.csv')
high_elec_df = pd.read_csv('output/checkpoint_final/high_electrification_results.csv')

output_dir = Path('output/checkpoint_final')

# 1. UPC Comparison Chart
fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(baseline_df['year'], baseline_df['upc'], marker='o', linewidth=2.5, label='Baseline', color='#1f77b4', markersize=6)
ax.plot(high_elec_df['year'], high_elec_df['upc'], marker='s', linewidth=2.5, label='High Electrification', color='#ff7f0e', markersize=6)
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Use Per Customer (therms/year)', fontsize=12, fontweight='bold')
ax.set_title('UPC Trajectories: Baseline vs High Electrification (2025-2035)', fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=11, loc='best', framealpha=0.95)
plt.tight_layout()
plt.savefig(output_dir / 'upc_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("Created: upc_comparison.png")

# 2. End-use Composition Chart
end_uses = ['space_heating', 'water_heating', 'cooking', 'drying', 'fireplace']
colors = ['#d62728', '#2ca02c', '#ff7f0e', '#9467bd', '#8c564b']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

baseline_data = baseline_df[['year'] + end_uses].set_index('year')
baseline_data.plot(kind='bar', stacked=True, ax=ax1, color=colors, width=0.7)
ax1.set_title('Baseline Scenario: End-Use Composition (2025-2035)', fontsize=13, fontweight='bold', pad=15)
ax1.set_xlabel('Year', fontsize=11, fontweight='bold')
ax1.set_ylabel('Annual Demand (therms)', fontsize=11, fontweight='bold')
ax1.legend(title='End-Use', labels=['Space Heating', 'Water Heating', 'Cooking', 'Drying', 'Fireplace'], loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')

high_elec_data = high_elec_df[['year'] + end_uses].set_index('year')
high_elec_data.plot(kind='bar', stacked=True, ax=ax2, color=colors, width=0.7)
ax2.set_title('High Electrification Scenario: End-Use Composition (2025-2035)', fontsize=13, fontweight='bold', pad=15)
ax2.set_xlabel('Year', fontsize=11, fontweight='bold')
ax2.set_ylabel('Annual Demand (therms)', fontsize=11, fontweight='bold')
ax2.legend(title='End-Use', labels=['Space Heating', 'Water Heating', 'Cooking', 'Drying', 'Fireplace'], loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig(output_dir / 'enduse_composition.png', dpi=300, bbox_inches='tight')
plt.close()
print("Created: enduse_composition.png")

# 3. Demand Reduction Chart
fig, ax = plt.subplots(figsize=(12, 7))
demand_reduction = baseline_df['total_therms'] - high_elec_df['total_therms']
reduction_pct = (demand_reduction / baseline_df['total_therms'] * 100)

bars = ax.bar(baseline_df['year'], demand_reduction / 1e6, color='#2ca02c', alpha=0.7, edgecolor='black', linewidth=1.5)

for i, (year, reduction, pct) in enumerate(zip(baseline_df['year'], demand_reduction / 1e6, reduction_pct)):
    ax.text(year, reduction + 0.5, f'{pct:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Demand Reduction (Million therms)', fontsize=12, fontweight='bold')
ax.set_title('Annual Demand Reduction: High Electrification vs Baseline', fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='y', linestyle='--')

plt.tight_layout()
plt.savefig(output_dir / 'demand_reduction.png', dpi=300, bbox_inches='tight')
plt.close()
print("Created: demand_reduction.png")

print("\nAll charts created successfully!")
