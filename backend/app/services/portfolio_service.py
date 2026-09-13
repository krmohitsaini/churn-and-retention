from typing import Any, Optional

from backend.app.schemas.common import MetricCard
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
        active = [row for row in episodes if row.get("drop_type") == "Active"]
        active_partners = {row.get("business_partner_id") for row in active}
        all_partners = {row.get("business_partner_id") for row in episodes}
        active_sites = {row.get("Site_id") for row in active}
        all_sites = {row.get("Site_id") for row in episodes}
        digital_partners = {
            row.get("business_partner_id")
            for row in episodes
            if str(row.get("digital_status")).lower() == "true"
        }
        avg_sites = round(len(all_sites) / len(all_partners), 1) if all_partners else 0
        active_share = round(len(active) / len(episodes), 4) if episodes else 0

        metrics = [
            MetricCard(label="Active customers", value=f"{len(active_partners):,}", helper="Business partners").model_dump(),
            MetricCard(label="Active sites", value=f"{len(active_sites):,}", helper="Site contracts").model_dump(),
            MetricCard(label="Active contract share", value=f"{active_share * 100:.1f}%", helper="Of all episodes").model_dump(),
            MetricCard(label="Avg sites per customer", value=avg_sites, helper="Portfolio density").model_dump(),
            MetricCard(label="Digital adoption", value=f"{(len(digital_partners) / len(all_partners) * 100) if all_partners else 0:.1f}%", helper="Business partners").model_dump(),
            MetricCard(label="Total sites", value=f"{len(all_sites):,}", helper="Known site IDs").model_dump(),
        ]

        return {
            "metrics": metrics,
            "by_commodity": self._count_by_field(active, "commodity_type"),
            "by_channel": self._count_by_field(active, "channel", limit=10),
            "by_sales_type": self._count_by_field(active, "sales_type"),
            "by_billing": self._count_by_field(active, "AMB_status"),
            "by_evergreen": self._count_by_field(active, "evergreen_status"),
            "by_surge": self._count_by_field(active, "surge_status"),
            "signups_by_month": self._timeseries(episodes, "sign_up_date", "signed_up_customers", unique_field="business_partner_id"),
            "active_contract_starts": self._timeseries(active, "site_contract_start_date", "active_contract_starts"),
            "site_density": self._site_density(),
        }

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
        return self._timeseries(self.repository.contract_episodes(), "sign_up_date", "signed_up_customers", unique_field="business_partner_id")

    def _count_by_field(self, rows: list[dict[str, Any]], field: str, limit: Optional[int] = None) -> list[dict[str, Any]]:
        counts: dict[str, int] = {}
        for row in rows:
            value = self._display_value(row.get(field))
            counts[value] = counts.get(value, 0) + 1
        points = [{"name": name, "value": value} for name, value in counts.items()]
        points = sorted(points, key=lambda point: point["value"], reverse=True)
        return points[:limit] if limit else points

    def _timeseries(
        self,
        rows: list[dict[str, Any]],
        date_field: str,
        value_field: str,
        unique_field: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        counts: dict[str, Any] = {}
        for row in rows:
            raw_date = str(row.get(date_field) or "")
            month = raw_date[:7] if len(raw_date) >= 7 else "Unknown"
            if unique_field:
                counts.setdefault(month, set()).add(row.get(unique_field))  # type: ignore[union-attr]
            else:
                counts[month] = int(counts.get(month, 0)) + 1  # type: ignore[arg-type]
        return [
            { "month": month, value_field: len(value) if isinstance(value, set) else value }
            for month, value in sorted(counts.items())
        ]

    def _site_density(self) -> list[dict[str, Any]]:
        sites_by_partner: dict[str, set[Any]] = {}
        for row in self.repository.contract_episodes():
            partner = str(row.get("business_partner_id"))
            sites_by_partner.setdefault(partner, set()).add(row.get("Site_id"))
        bands = {"1 site": 0, "2-3 sites": 0, "4-6 sites": 0, "7+ sites": 0}
        for sites in sites_by_partner.values():
            count = len(sites)
            if count == 1:
                bands["1 site"] += 1
            elif count <= 3:
                bands["2-3 sites"] += 1
            elif count <= 6:
                bands["4-6 sites"] += 1
            else:
                bands["7+ sites"] += 1
        return [{"name": name, "value": value} for name, value in bands.items()]

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
