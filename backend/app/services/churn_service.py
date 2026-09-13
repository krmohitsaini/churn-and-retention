from typing import Any, Optional

from backend.app.schemas.common import MetricCard
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
        active = [row for row in episodes if row.get("drop_type") == "Active"]
        churn = [row for row in episodes if row.get("drop_type") == "Churn"]
        leakage = [row for row in episodes if row.get("drop_type") == "Leakage"]
        tos = [row for row in episodes if row.get("drop_type") == "TOS"]
        churned_partners = {row.get("business_partner_id") for row in churn}
        active_partners = {row.get("business_partner_id") for row in active}
        denominator = len(active) + len(churn)
        site_churn_rate = round(len(churn) / denominator, 4) if denominator else 0
        customer_churn_exposure = round(len(churned_partners) / (len(active_partners | churned_partners) or 1), 4)

        return {
            "metrics": [
                MetricCard(label="Churned sites", value=f"{len(churn):,}", helper="Drop type = Churn").model_dump(),
                MetricCard(label="Site churn rate", value=f"{site_churn_rate * 100:.1f}%", helper="Churn / active plus churn").model_dump(),
                MetricCard(label="Customers touched by churn", value=f"{len(churned_partners):,}", helper=f"{customer_churn_exposure * 100:.1f}% of exposed customers").model_dump(),
                MetricCard(label="Leakage", value=f"{len(leakage):,}", helper="Ended within first 5 days").model_dump(),
                MetricCard(label="TOS exits", value=f"{len(tos):,}", helper="Term-of-service outcomes").model_dump(),
                MetricCard(label="Active sites", value=f"{len(active):,}", helper="Current active contracts").model_dump(),
            ],
            "timeseries": self._timeseries(churn, "site_contract_end_date", "churned_sites"),
            "outcomes": self._count_by_field(episodes, "drop_type"),
            "by_commodity": self._count_by_field(churn, "commodity_type"),
            "by_channel": self._count_by_field(churn, "channel", limit=10),
            "by_sales_type": self._count_by_field(churn, "sales_type"),
            "by_billing": self._count_by_field(churn, "AMB_status"),
            "by_digital": self._count_by_field(churn, "digital_status"),
            "by_agent": self._count_by_field(churn, "agent_name", limit=12),
            "monthly_outcomes": self._monthly_outcomes(episodes),
        }

    def timeseries(self) -> list[dict[str, Any]]:
        churn = [row for row in self.repository.contract_episodes() if row.get("drop_type") == "Churn"]
        return self._timeseries(churn, "site_contract_end_date", "churned_sites")

    def by_segment(self) -> list[dict[str, Any]]:
        churn = [row for row in self.repository.contract_episodes() if row.get("drop_type") == "Churn"]
        return self._count_by_field(churn, "channel")

    def cohorts(self) -> list[dict[str, Any]]:
        return [
            {"cohort": "2023-Q1", "month_1": 0.96, "month_6": 0.9, "month_12": 0.82},
            {"cohort": "2023-Q2", "month_1": 0.95, "month_6": 0.88, "month_12": 0.8},
            {"cohort": "2023-Q3", "month_1": 0.97, "month_6": 0.91, "month_12": 0.84},
        ]

    def reasons(self) -> list[dict[str, Any]]:
        return self._count_by_field(self.repository.contract_episodes(), "drop_type")

    def _count_by_field(self, rows: list[dict[str, Any]], field: str, limit: Optional[int] = None) -> list[dict[str, Any]]:
        counts: dict[str, int] = {}
        for row in rows:
            value = self._display_value(row.get(field))
            counts[value] = counts.get(value, 0) + 1
        points = [{"name": name, "value": value} for name, value in counts.items()]
        points = sorted(points, key=lambda point: point["value"], reverse=True)
        return points[:limit] if limit else points

    def _timeseries(self, rows: list[dict[str, Any]], date_field: str, value_field: str) -> list[dict[str, Any]]:
        counts: dict[str, int] = {}
        for row in rows:
            raw_date = str(row.get(date_field) or "")
            month = raw_date[:7] if len(raw_date) >= 7 else "Unknown"
            counts[month] = counts.get(month, 0) + 1
        return [{ "month": month, value_field: value } for month, value in sorted(counts.items())]

    def _monthly_outcomes(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        months: dict[str, dict[str, int]] = {}
        for row in rows:
            if row.get("drop_type") == "Active":
                continue
            month = str(row.get("site_contract_end_date") or "")[:7]
            if not month:
                month = "Unknown"
            bucket = months.setdefault(month, {"month": month, "Churn": 0, "Auto Renewal": 0, "Positive Renewal": 0, "TOS": 0, "Leakage": 0})
            outcome = str(row.get("drop_type") or "Unknown")
            bucket[outcome] = bucket.get(outcome, 0) + 1
        return [months[month] for month in sorted(months)]

    def _display_value(self, value: Any) -> str:
        if value is True:
            return "Yes"
        if value is False:
            return "No"
        if str(value).lower() == "true":
            return "Yes"
        if str(value).lower() == "false":
            return "No"
        if value in (None, ""):
            return "Unknown"
        return str(value)
