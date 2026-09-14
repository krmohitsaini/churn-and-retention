from typing import Any

from backend.app.kpis.common import monthly_timeseries
from backend.app.kpis.portfolio_kpis import build_portfolio_summary
from backend.app.services.app_cache import get_or_set
from backend.app.services.filters import apply_filters


class PortfolioService:
    def __init__(self, repository):
        self.repository = repository

    def summary(self, filters: dict[str, Any]) -> dict[str, Any]:
        return get_or_set(
            "portfolio-summary",
            self.repository.source_version(),
            filters,
            lambda: self._summary(filters),
        )

    def _summary(self, filters: dict[str, Any]) -> dict[str, Any]:
        episodes = apply_filters(self.repository.contract_episodes(), filters)
        return build_portfolio_summary(episodes)

    def segments(self) -> dict[str, list[str]]:
        return get_or_set(
            "portfolio-segments",
            self.repository.source_version(),
            {},
            self._segments,
        )

    def _segments(self) -> dict[str, list[str]]:
        episodes = self.repository.contract_episodes()
        fields = [
            "commodity_type",
            "channel",
            "sales_type",
            "AMB_status",
            "evergreen_status",
            "surge_status",
            "digital_status",
            "dob_status",
            "drop_type",
        ]
        return {
            field: sorted({str(row.get(field)) for row in episodes if row.get(field) not in (None, "")})
            for field in fields
        }

    def timeseries(self) -> list[dict[str, Any]]:
        return monthly_timeseries(
            self.repository.contract_episodes(),
            "sign_up_date",
            "signed_up_customers",
            unique_field="business_partner_id",
        )
