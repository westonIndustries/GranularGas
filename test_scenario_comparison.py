import sys
sys.path.insert(0, '.')

from src.scenario_comparison import generate_scenario_comparison_report

baseline_path = 'output/checkpoint_final/baseline_results.csv'
high_elec_path = 'output/checkpoint_final/high_electrification_results.csv'

results = generate_scenario_comparison_report(baseline_path, high_elec_path)
print("Generated reports:")
for key, path in results.items():
    print(f"  {key}: {path}")
