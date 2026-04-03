"""Load and filter NW Natural segment data to residential customers."""
import os, logging, pandas as pd
from src import config
from src.loaders._helpers import save_diagnostics

logger = logging.getLogger(__name__)

def load_segment_data(path: str = None) -> pd.DataFrame:
    path = path or config.SEGMENT_DATA
    if not os.path.exists(path):
        raise FileNotFoundError(f"Segment data file not found: {path}")
    df = pd.read_csv(path)
    logger.info(f"Loaded {len(df)} segment records from {path}")
    df = df[df['segment'].isin(['RESSF', 'RESMF', 'MOBILE'])].copy()
    logger.info(f"Filtered to {len(df)} residential segment records")
    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    df = load_segment_data()
    print(f"  {len(df)} records, segments: {df['segment'].value_counts().to_dict()}")
    save_diagnostics(df, "segment_data")
