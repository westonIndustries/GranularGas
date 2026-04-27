# Scenario Results: baseline
Generated: 2026-04-27T12:52:35.531624

## Configuration
- Base Year: 2025
- Forecast Horizon: 10 years
- Temporal Resolution: Annual
- Housing Growth Rate: 1.00%
- Electrification Rate: 2.00%
- Efficiency Improvement: 1.00%
- Weather Assumption: normal
- End-Use Scope: ['space_heating']
- Max Premises: 0 (0=all)
- Vectorized: True

## Yearly Demand Summary

| Year | Total Therms | Model UPC | IRP UPC | Diff % | Premises |
|------|-------------|-----------|---------|--------|----------|
| 2025 | 111,325,053 | 520.9 | 648.0 | -19.6% | 213,725 |
| 2026 | 104,815,570 | 490.4 | 640.3 | -23.4% | 213,725 |
| 2027 | 103,133,061 | 482.6 | 632.7 | -23.7% | 213,725 |
| 2028 | 101,963,814 | 477.1 | 625.1 | -23.7% | 213,725 |
| 2029 | 100,922,647 | 472.2 | 617.7 | -23.6% | 213,725 |
| 2030 | 100,033,142 | 468.0 | 610.3 | -23.3% | 213,725 |
| 2031 | 99,166,878 | 464.0 | 603.1 | -23.1% | 213,725 |
| 2032 | 98,340,635 | 460.1 | 595.9 | -22.8% | 213,725 |
| 2033 | 97,432,592 | 455.9 | 588.8 | -22.6% | 213,725 |
| 2034 | 96,682,360 | 452.4 | 581.8 | -22.2% | 213,725 |
| 2035 | 95,990,414 | 449.1 | 574.9 | -21.9% | 213,725 |

## End-Use Breakdown (All Years)

| End-Use | Total Therms | Share |
|---------|-------------|-------|
| space_heating | 1,109,806,166 | 100.0% |

## Output Files

- `results.csv` — Full results (year x end-use)
- `results.json` — Same data in JSON format
- `yearly_summary.csv` — Year-by-year aggregated summary
- `metadata.json` — Scenario configuration and run metadata
- `baseline.json` — Input configuration (copy)
- `SUMMARY.md` — This file