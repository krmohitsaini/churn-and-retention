from typing import Any

from backend.app.data.base_repository import BaseRepository


class DatabricksRepository(BaseRepository):
    def customers(self) -> list[dict[str, Any]]:
        raise NotImplementedError("Databricks customer access is not implemented yet.")

    def churn_events(self) -> list[dict[str, Any]]:
        raise NotImplementedError("Databricks churn event access is not implemented yet.")

    def propensity_scores(self) -> list[dict[str, Any]]:
        raise NotImplementedError("Databricks propensity access is not implemented yet.")

    def customer_interactions(self) -> list[dict[str, Any]]:
        raise NotImplementedError("Databricks interaction access is not implemented yet.")

    def offers(self) -> list[dict[str, Any]]:
        raise NotImplementedError("Databricks offer access is not implemented yet.")

    def contract_episodes(self) -> list[dict[str, Any]]:
        raise NotImplementedError("Databricks contract episode access is not implemented yet.")

    def source_version(self) -> str:
        return "databricks-live"
