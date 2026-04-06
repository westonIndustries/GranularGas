"""Load and filter NW Natural premise data to active residential premises."""
import os, logging, pandas as pd
from src import config
from src.loaders._helpers import save_diagnostics

logger = logging.getLogger(__name__)

def load_premise_data(path: str = None) -> pd.DataFrame:
    path = path or config.PREMISE_DATA
    if not os.path.exists(path):
        raise FileNotFoundError(f"Premise data file not found: {path}")
    df = pd.read_csv(path)
    logger.info(f"Loaded {len(df)} premise records from {path}")
    for c in ['blinded_id', 'custtype', 'status_code']:
        if c not in df.columns:
            raise ValueError(f"Missing required column: {c}")
    df = df[(df['custtype'] == 'R') & (df['status_code'] == 'AC')].copy()
    logger.info(f"Filtered to {len(df)} active residential premises")
    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    print("Loading premise data...")
    df = load_premise_data()
    print(f"  {len(df)} active residential premises")
    save_diagnostics(df, "premise_data")
