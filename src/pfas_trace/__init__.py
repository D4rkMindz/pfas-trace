from pathlib import Path

DATASET_URL = "https://pdh.cnrs.fr/download/full.parquet"
_DATASET_BASE_PATH = Path(__file__).resolve().parents[2] / "data"
DATASET_FILE = _DATASET_BASE_PATH / "export.parquet"

DATASET_PRESUMPTIVE_USERS = _DATASET_BASE_PATH / "extract.presumptive-users.parquet"
DATASET_USERS = _DATASET_BASE_PATH / "extract.users.parquet"

DATASET_MEASUREMENTS = _DATASET_BASE_PATH / "extract.measurements.parquet"
DATASET_MEASUREMENTS_BY_CHEMICAL = _DATASET_BASE_PATH / "extract.pfas-measurements.parquet"
DATASET_MEASUREMENT_DISTANCES = _DATASET_BASE_PATH / "extract.pfas-measurement-distances.parquet"