# 15.10 Billing Amount Reasonableness
Generated: 2026-04-21T00:45:36.548581

> **Purpose:** Flag billing records with suspiciously low (< 1 therm) or high (> 500 therms) usage per billing period.
>
> **Why it matters:** Extreme billing values distort calibration. A record of 0.01 therms may be a meter read error or an estimated bill for a vacant unit. A record of 500+ therms in a single billing period (typically monthly) is implausible for a residential customer and may indicate a commercial account miscoded as residential, or a data entry error.
>
> **How to read:** The flagged percentage should be low (< 5%). The log-scale histogram shows the full distribution with threshold lines at 1 and 500 therms. The monthly time-series shows seasonal patterns (higher in winter, lower in summer) — anomalies indicate data issues. The box plot by rate schedule reveals whether certain schedules have unusual distributions.
>
> **Recommended action:** If > 5% of records are flagged, investigate the source. Low-therm records may be summer months with minimal gas use (legitimate) or estimated reads (filter out). High-therm records should be cross-checked against the premise's segment — a RESMF premise with 500 therms/month may be a master-metered building (legitimate but needs different treatment in simulation).

## Summary

| metric | value |
| --- | --- |
| Total billing records | 48,675,554 |
| Valid therm values | 0 |
| Flagged records (total) | 0 |
| % flagged | 0.00% |
| Low (< 1 therm) | 0 |
| High (> 500 therms) | 0 |

