from pathlib import Path

DATASET_URL = "https://pdh.cnrs.fr/download/full.parquet"
DATASET_PATH = Path(__file__).resolve().parents[2] / "data"
DATASET_FILE = DATASET_PATH / "export.parquet"

DATASET_PRESUMPTIVE_USERS = DATASET_PATH / "extract.presumptive-users.parquet"
DATASET_USERS = DATASET_PATH / "extract.users.parquet"

DATASET_MEASUREMENTS = DATASET_PATH / "extract.measurements.parquet"
DATASET_MEASUREMENTS_BY_CHEMICAL = DATASET_PATH / "extract.pfas-measurements.parquet"