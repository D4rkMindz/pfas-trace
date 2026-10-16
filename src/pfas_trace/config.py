"""  Handles all static global variables (loaded vom .env and project-interns)
config.py = systemic Defaults + persistend values
.env = Enduser-overridable Settings + dynamische Runtime-Results
"""
import logging
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / 'data'
DATASET_FILE = DATA_DIR / "export.parquet"

DATASET_FILE = DATA_DIR / "export.parquet"

DATASET_PRESUMPTIVE_USERS = DATA_DIR / "extract.presumptive-users.parquet"
DATASET_USERS = DATA_DIR / "extract.users.parquet"

DATASET_MEASUREMENTS = DATA_DIR / "extract.measurements.parquet"
DATASET_MEASUREMENTS_BY_CHEMICAL = DATA_DIR / "extract.pfas-measurements.parquet"
DATASET_MEASUREMENT_DISTANCES = DATA_DIR / "extract.pfas-measurement-distances.parquet"


class Settings(BaseSettings):
    """ All settings that can be defined in .env or have a default value. """
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        extra="forbid"
    )

    # LOGGING
    LOG_LEVEL: Literal["ERROR", "WARNING", "INFO", "DEBUG"] = 'INFO'
    LOG_FORMAT: str = "%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s"

    # PFAS hub
    DATASET_URL: str = "https://pdh.cnrs.fr/download/full.parquet"

    # Google Cloud Platform

    # Google Cloud Storage

    # Agent Configuration


settings = Settings()


def setup_logging():
    """ Configures the logger once at the beginning """
    logging.basicConfig(format=settings.LOG_FORMAT,
                        level=settings.LOG_LEVEL)
