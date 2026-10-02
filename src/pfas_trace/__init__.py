from pathlib import Path

DATASET_URL = "https://pdh.cnrs.fr/download/full.parquet"
DATASET_FILE = Path(__file__).resolve().parents[2] / "data" / "export.parquet"