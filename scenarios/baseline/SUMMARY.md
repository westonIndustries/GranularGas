# Scenario Results: baseline
Generated: 2026-04-27T02:26:31.454987

## Configuration
- Base Year: 2025
- Forecast Horizon: 10 years
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
| 2026 | 104,815,570 | 485.6 | 640.3 | -24.2% | 213,725 |
| 2027 | 103,133,061 | 473.0 | 632.7 | -25.2% | 213,725 |
| 2028 | 101,963,814 | 463.0 | 625.1 | -25.9% | 213,725 |
| 2029 | 100,922,647 | 453.8 | 617.7 | -26.5% | 213,725 |
| 2030 | 100,033,142 | 445.3 | 610.3 | -27.0% | 213,725 |
| 2031 | 99,166,878 | 437.1 | 603.1 | -27.5% | 213,725 |
| 2032 | 98,340,635 | 429.2 | 595.9 | -28.0% | 213,725 |
| 2033 | 97,432,592 | 421.0 | 588.8 | -28.5% | 213,725 |
| 2034 | 96,682,360 | 413.6 | 581.8 | -28.9% | 213,725 |
| 2035 | 95,990,414 | 406.6 | 574.9 | -29.3% | 213,725 |

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