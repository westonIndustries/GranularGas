#!/usr/bin/env python
"""Quick test to build premise_equipment table."""

from src.loaders.load_premise_data import load_premise_data
from src.loaders.load_equipment_data import load_equipment_data
from src.loaders.load_segment_data import load_segment_data
from src.loaders.load_equipment_codes import load_equipment_codes
from src.data_ingestion import build_premise_equipment_table

print("Loading data...")
premises = load_premise_data()
equipment = load_equipment_data()
segments = load_segment_data()
codes = load_equipment_codes()

print(f"Premises: {len(premises)} rows")
print(f"Equipment: {len(equipment)} rows")
print(f"Segments: {len(segments)} rows")
print(f"Codes: {len(codes)} rows")

print("\nBuilding premise_equipment table...")
pet = build_premise_equipment_table(premises, equipment, segments, codes)

print(f"\nPremise-equipment table: {len(pet)} rows, {len(pet.columns)} columns")
print(f"Columns: {list(pet.columns)[:15]}")
print(f"\nUnique segments: {pet['segment_code'].unique()}")
print(f"Unique end_uses: {pet['end_use'].unique()}")
print(f"Unique districts: {pet['district_code_IRP'].unique()[:10]}")
print(f"\nSegment distribution:\n{pet['segment_code'].value_counts()}")
print(f"\nEnd-use distribution:\n{pet['end_use'].value_counts()}")
