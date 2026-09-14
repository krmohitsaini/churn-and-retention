from typing import Any

from backend.app.kpis.churn_kpis import build_churn_summary, rows_by_drop_type
from backend.app.kpis.common import count_by_field, monthly_timeseries
from backend.app.services.app_cache import get_or_set
from backend.app.services.filters import apply_filters


class ChurnService:
    def __init__(self, repository):
        self.repository = repository

    def summary(self, filters: dict[str, Any]) -> dict[str, Any]:
        return get_or_set(
            "churn-summary",
            self.repository.source_version(),
            filters,
            lambda: self._summary(filters),
        )

    def _summary(self, filters: dict[str, Any]) -> dict[str, Any]:
        episodes = apply_filters(self.repository.contract_episodes(), filters)
        return build_churn_summary(episodes)

    def timeseries(self) -> list[dict[str, Any]]:
        churn = rows_by_drop_type(self.repository.contract_episodes(), "Churn")
        return monthly_timeseries(churn, "site_contract_end_date", "churned_sites")

    def by_segment(self) -> list[dict[str, Any]]:
        churn = rows_by_drop_type(self.repository.contract_episodes(), "Churn")
        return count_by_field(churn, "channel")

    def cohorts(self) -> list[dict[str, Any]]:
        return [
            {"cohort": "2023-Q1", "month_1": 0.96, "month_6": 0.9, "month_12": 0.82},
            {"cohort": "2023-Q2", "month_1": 0.95, "month_6": 0.88, "month_12": 0.8},
            {"cohort": "2023-Q3", "month_1": 0.97, "month_6": 0.91, "month_12": 0.84},
        ]

    def reasons(self) -> list[dict[str, Any]]:
        return count_by_field(self.repository.contract_episodes(), "drop_type")
