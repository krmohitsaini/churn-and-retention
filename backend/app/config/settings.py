from functools import lru_cache
import os
from pathlib import Path


class Settings:
    app_name = "Churn and Retention"
    api_prefix = "/api/v1"
    data_source = os.getenv("APP_DATA_SOURCE", "csv")
    sample_data_dir = Path(os.getenv("APP_SAMPLE_DATA_DIR", "data/sample"))
    raw_data_file = Path(os.getenv("APP_RAW_DATA_FILE", "data/raw/synthetic_energy_customer_sites.csv"))
    cors_origins = os.getenv(
        "APP_CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")


@lru_cache
def get_settings() -> Settings:
    return Settings()
