# Scenario Results: policy_ramp_test
Generated: 2026-04-27T02:14:16.607998

## Configuration
- Base Year: 2025
- Forecast Horizon: 10 years
- Housing Growth Rate: curve (see JSON)
- Electrification Rate: curve (see JSON)
- Efficiency Improvement: curve (see JSON)
- Weather Assumption: normal
- End-Use Scope: ['space_heating']
- Max Premises: 0 (0=all)
- Vectorized: True

## Yearly Demand Summary

| Year | Total Therms | Model UPC | IRP UPC | Diff % | Premises |
|------|-------------|-----------|---------|--------|----------|
| 2025 | 111,325,053 | 520.9 | 648.0 | -19.6% | 213,725 |
| 2026 | 104,690,085 | 483.6 | 640.3 | -24.5% | 213,725 |
| 2027 | 102,859,640 | 468.1 | 632.7 | -26.0% | 213,725 |
| 2028 | 100,446,410 | 449.4 | 625.1 | -28.1% | 213,725 |
| 2029 | 98,904,091 | 438.9 | 617.7 | -28.9% | 213,725 |
| 2030 | 97,573,137 | 430.8 | 610.3 | -29.4% | 213,725 |
| 2031 | 96,417,658 | 425.0 | 603.1 | -29.5% | 213,725 |
| 2032 | 95,433,794 | 420.1 | 595.9 | -29.5% | 213,725 |
| 2033 | 94,210,709 | 415.2 | 588.8 | -29.5% | 213,725 |
| 2034 | 93,406,842 | 413.2 | 581.8 | -29.0% | 213,725 |
| 2035 | 92,727,913 | 412.8 | 574.9 | -28.2% | 213,725 |

## End-Use Breakdown (All Years)

| End-Use | Total Therms | Share |
|---------|-------------|-------|
| space_heating | 1,087,995,332 | 100.0% |

## Output Files

- `results.csv` — Full results (year x end-use)
- `results.json` — Same data in JSON format
- `yearly_summary.csv` — Year-by-year aggregated summary
- `metadata.json` — Scenario configuration and run metadata
- `policy_ramp_test.json` — Input configuration (copy)
- `SUMMARY.md` — This file