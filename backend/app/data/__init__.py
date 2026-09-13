from backend.app.config.settings import get_settings
from backend.app.data.base_repository import BaseRepository
from backend.app.data.csv_repository import CsvRepository
from backend.app.data.databricks_repository import DatabricksRepository


def get_repository() -> BaseRepository:
    settings = get_settings()
    if settings.data_source == "databricks":
        return DatabricksRepository()
    return CsvRepository(settings.sample_data_dir, settings.raw_data_file)
