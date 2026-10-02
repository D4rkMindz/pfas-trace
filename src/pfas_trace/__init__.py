from pathlib import Path

DATASET_URL = "https://pdh.cnrs.fr/download/full.parquet"
DATASET_PATH = Path(__file__).resolve().parents[2] / "data"
DATASET_FILE = DATASET_PATH / "export.parquet"