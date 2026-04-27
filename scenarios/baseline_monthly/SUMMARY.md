# Scenario Results: baseline_monthly
Generated: 2026-04-27T01:02:55.325773

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
| 2026 | 105,701,149 | 489.7 | 640.3 | -23.5% | 213,725 |
| 2027 | 102,392,250 | 469.6 | 632.7 | -25.8% | 213,725 |
| 2028 | 101,271,200 | 459.9 | 625.1 | -26.4% | 213,725 |
| 2029 | 100,864,745 | 453.5 | 617.7 | -26.6% | 213,725 |
| 2030 | 100,708,111 | 448.3 | 610.3 | -26.5% | 213,725 |
| 2031 | 100,477,647 | 442.9 | 603.1 | -26.6% | 213,725 |
| 2032 | 100,527,326 | 438.7 | 595.9 | -26.4% | 213,725 |
| 2033 | 100,190,444 | 432.9 | 588.8 | -26.5% | 213,725 |
| 2034 | 100,417,702 | 429.6 | 581.8 | -26.2% | 213,725 |
| 2035 | 100,691,019 | 426.5 | 574.9 | -25.8% | 213,725 |

## End-Use Breakdown (All Years)

| End-Use | Total Therms | Share |
|---------|-------------|-------|
| space_heating | 1,124,566,646 | 100.0% |

## Output Files

- `results.csv` — Full results (year x end-use)
- `results.json` — Same data in JSON format
- `yearly_summary.csv` — Year-by-year aggregated summary
- `metadata.json` — Scenario configuration and run metadata
- `baseline_monthly.json` — Input configuration (copy)
- `SUMMARY.md` — This file