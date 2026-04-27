# Billing Data Cache

## What It Does

The billing CSV (`billing_data_blinded.csv`) has ~48 million raw monthly records and takes ~90 seconds to load. The model only needs the aggregated annual therms per premise (~3.4 million rows).

On the first run, the model processes the full CSV, aggregates it, and saves the result as a cache file next to the original CSV. On subsequent runs, it loads the cache directly (~5 seconds vs ~90 seconds).

## Cache Location

```
Data/NWNatural Data/billing_annual_cache.csv
```

The cache is automatically invalidated if the source CSV is newer than the cache file.

## Rebuilding the Cache

Delete the cache file and run any scenario. The cache will be rebuilt automatically.

```bash
# Delete the cache
del "Data\NWNatural Data\billing_annual_cache.csv"

# Run any scenario — cache rebuilds automatically (~90s one-time cost)
C:\Python312\python.exe -m src.main scenarios/baseline.json
```

Or rebuild it directly without running a full scenario:

```bash
C:\Python312\python.exe -c "from src.calibration import load_annual_billing_therms; load_annual_billing_therms()"
```

## When to Rebuild

Rebuild the cache if:

- The source `billing_data_blinded.csv` is updated with new billing records
- You see stale or unexpected billing UPC values in the `observed_billing_upc.csv` output
- The cache file gets corrupted (delete it and re-run)

The cache auto-detects if the CSV is newer and will rebuild itself, so in most cases you don't need to do anything manually.

## What's in the Cache

| Column | Type | Description |
|--------|------|-------------|
| `blinded_id` | string | Anonymized premise identifier |
| `year` | int | Billing year (2009–2025) |
| `annual_therms` | float | Total therms for that premise in that year |

Rows with annual therms below 10 or above 5,000 are filtered out as unreasonable. Only residential rate class (R1) records are included.
