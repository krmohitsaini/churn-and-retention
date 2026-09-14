from typing import Any

from backend.app.kpis.common import count_by_field, monthly_timeseries
from backend.app.schemas.common import MetricCard


def active_customer_count(customers: list[dict[str, Any]]) -> int:
    """Count customers whose current_status is Active."""
    return sum(1 for customer in customers if customer.get("current_status") == "Active")


def total_estimated_annual_value(customers: list[dict[str, Any]]) -> float:
    """Sum estimated annual value across active customers."""
    return sum(
        float(customer.get("estimated_annual_value") or 0)
        for customer in customers
        if customer.get("current_status") == "Active"
    )


def average_tenure_months(customers: list[dict[str, Any]]) -> float:
    """Average tenure in months across active customers."""
    tenures = [
        float(customer.get("tenure_months") or 0)
        for customer in customers
        if customer.get("current_status") == "Active"
    ]
    return round(sum(tenures) / len(tenures), 1) if tenures else 0


def count_active_customers_by_field(customers: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    """Count active customers by a categorical portfolio field."""
    counts: dict[str, int] = {}
    for customer in customers:
        if customer.get("current_status") != "Active":
            continue
        value = str(customer.get(field) or "Unknown")
        counts[value] = counts.get(value, 0) + 1
    return [{"name": name, "value": value} for name, value in sorted(counts.items())]


def active_contract_rows(episodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return site contract episodes that are active as of the data generation date."""
    return [row for row in episodes if row.get("drop_type") == "Active"]


def active_business_partner_count(active_episodes: list[dict[str, Any]]) -> int:
    """Count unique business partners with at least one active site contract."""
    return len({row.get("business_partner_id") for row in active_episodes})


def active_site_count(active_episodes: list[dict[str, Any]]) -> int:
    """Count unique active site IDs."""
    return len({row.get("Site_id") for row in active_episodes})


def total_site_count(episodes: list[dict[str, Any]]) -> int:
    """Count unique site IDs in the selected portfolio."""
    return len({row.get("Site_id") for row in episodes})


def active_contract_share(episodes: list[dict[str, Any]], active_episodes: list[dict[str, Any]]) -> float:
    """Share of selected contract episodes that are currently active."""
    return round(len(active_episodes) / len(episodes), 4) if episodes else 0


def average_sites_per_business_partner(episodes: list[dict[str, Any]]) -> float:
    """Average number of unique sites per selected business partner."""
    partners = {row.get("business_partner_id") for row in episodes}
    sites = {row.get("Site_id") for row in episodes}
    return round(len(sites) / len(partners), 1) if partners else 0


def digital_adoption_rate(episodes: list[dict[str, Any]]) -> float:
    """Share of selected business partners with digital_status = true."""
    partners = {row.get("business_partner_id") for row in episodes}
    digital_partners = {
        row.get("business_partner_id")
        for row in episodes
        if str(row.get("digital_status")).lower() == "true"
    }
    return round(len(digital_partners) / len(partners), 4) if partners else 0


def site_density(episodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Bucket business partners by their number of unique site IDs."""
    sites_by_partner: dict[str, set[Any]] = {}
    for row in episodes:
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


def portfolio_metric_cards(episodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Create the Portfolio page KPI cards from selected contract episodes."""
    active = active_contract_rows(episodes)
    return [
        MetricCard(label="Active customers", value=f"{active_business_partner_count(active):,}", helper="Business partners").model_dump(),
        MetricCard(label="Active sites", value=f"{active_site_count(active):,}", helper="Site contracts").model_dump(),
        MetricCard(label="Active contract share", value=f"{active_contract_share(episodes, active) * 100:.1f}%", helper="Of all episodes").model_dump(),
        MetricCard(label="Avg sites per customer", value=average_sites_per_business_partner(episodes), helper="Portfolio density").model_dump(),
        MetricCard(label="Digital adoption", value=f"{digital_adoption_rate(episodes) * 100:.1f}%", helper="Business partners").model_dump(),
        MetricCard(label="Total sites", value=f"{total_site_count(episodes):,}", helper="Known site IDs").model_dump(),
    ]


def build_portfolio_summary(episodes: list[dict[str, Any]]) -> dict[str, Any]:
    """Create the full Portfolio page response from selected contract episodes."""
    active = active_contract_rows(episodes)
    return {
        "metrics": portfolio_metric_cards(episodes),
        "by_commodity": count_by_field(active, "commodity_type"),
        "by_channel": count_by_field(active, "channel", limit=10),
        "by_sales_type": count_by_field(active, "sales_type"),
        "by_billing": count_by_field(active, "AMB_status"),
        "by_evergreen": count_by_field(active, "evergreen_status"),
        "by_surge": count_by_field(active, "surge_status"),
        "signups_by_month": monthly_timeseries(episodes, "sign_up_date", "signed_up_customers", unique_field="business_partner_id"),
        "active_contract_starts": monthly_timeseries(active, "site_contract_start_date", "active_contract_starts"),
        "site_density": site_density(episodes),
    }
