from collections import defaultdict
from typing import Any

from backend.app.kpis.common import count_by_field, monthly_timeseries
from backend.app.schemas.common import MetricCard


def churned_customer_count(churn_events: list[dict[str, Any]]) -> int:
    """Count customer churn events in the selected period."""
    return len(churn_events)


def gross_churn_rate(churn_events: list[dict[str, Any]], starting_customer_count: int) -> float:
    """Gross churn rate equals churned customers divided by starting customer count."""
    if starting_customer_count == 0:
        return 0
    return round(len(churn_events) / starting_customer_count, 4)


def churn_by_field(churn_events: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    """Count churn events by a categorical churn field."""
    counts: dict[str, int] = {}
    for event in churn_events:
        value = str(event.get(field) or "Unknown")
        counts[value] = counts.get(value, 0) + 1
    return [{"name": name, "value": value} for name, value in sorted(counts.items())]


def churn_timeseries(churn_events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Count churn events by month using the churn_date field."""
    counts: dict[str, int] = defaultdict(int)
    for event in churn_events:
        churn_date = str(event.get("churn_date") or "")
        month = churn_date[:7] if len(churn_date) >= 7 else "Unknown"
        counts[month] += 1
    return [{"month": month, "churned_customers": count} for month, count in sorted(counts.items())]


def rows_by_drop_type(episodes: list[dict[str, Any]], drop_type: str) -> list[dict[str, Any]]:
    """Return contract episodes with a specific drop_type value."""
    return [row for row in episodes if row.get("drop_type") == drop_type]


def site_churn_rate(active_episodes: list[dict[str, Any]], churn_episodes: list[dict[str, Any]]) -> float:
    """Site churn rate equals churned sites divided by active plus churned site episodes."""
    denominator = len(active_episodes) + len(churn_episodes)
    return round(len(churn_episodes) / denominator, 4) if denominator else 0


def customer_churn_exposure_rate(active_episodes: list[dict[str, Any]], churn_episodes: list[dict[str, Any]]) -> float:
    """Share of exposed business partners that have at least one churned site episode."""
    active_partners = {row.get("business_partner_id") for row in active_episodes}
    churned_partners = {row.get("business_partner_id") for row in churn_episodes}
    exposed_partners = active_partners | churned_partners
    return round(len(churned_partners) / len(exposed_partners), 4) if exposed_partners else 0


def monthly_outcomes(episodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Count non-active contract outcomes by site contract end month."""
    months: dict[str, dict[str, int]] = {}
    for row in episodes:
        if row.get("drop_type") == "Active":
            continue
        month = str(row.get("site_contract_end_date") or "")[:7] or "Unknown"
        bucket = months.setdefault(
            month,
            {"month": month, "Churn": 0, "Auto Renewal": 0, "Positive Renewal": 0, "TOS": 0, "Leakage": 0},
        )
        outcome = str(row.get("drop_type") or "Unknown")
        bucket[outcome] = bucket.get(outcome, 0) + 1
    return [months[month] for month in sorted(months)]


def churn_metric_cards(episodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Create the Churn page KPI cards from selected contract episodes."""
    active = rows_by_drop_type(episodes, "Active")
    churn = rows_by_drop_type(episodes, "Churn")
    leakage = rows_by_drop_type(episodes, "Leakage")
    tos = rows_by_drop_type(episodes, "TOS")
    churned_partners = {row.get("business_partner_id") for row in churn}
    exposure_rate = customer_churn_exposure_rate(active, churn)

    return [
        MetricCard(label="Churned sites", value=f"{len(churn):,}", helper="Drop type = Churn").model_dump(),
        MetricCard(label="Site churn rate", value=f"{site_churn_rate(active, churn) * 100:.1f}%", helper="Churn / active plus churn").model_dump(),
        MetricCard(label="Customers touched by churn", value=f"{len(churned_partners):,}", helper=f"{exposure_rate * 100:.1f}% of exposed customers").model_dump(),
        MetricCard(label="Leakage", value=f"{len(leakage):,}", helper="Ended within first 5 days").model_dump(),
        MetricCard(label="TOS exits", value=f"{len(tos):,}", helper="Term-of-service outcomes").model_dump(),
        MetricCard(label="Active sites", value=f"{len(active):,}", helper="Current active contracts").model_dump(),
    ]


def build_churn_summary(episodes: list[dict[str, Any]]) -> dict[str, Any]:
    """Create the full Churn page response from selected contract episodes."""
    churn = rows_by_drop_type(episodes, "Churn")
    return {
        "metrics": churn_metric_cards(episodes),
        "timeseries": monthly_timeseries(churn, "site_contract_end_date", "churned_sites"),
        "outcomes": count_by_field(episodes, "drop_type"),
        "by_commodity": count_by_field(churn, "commodity_type"),
        "by_channel": count_by_field(churn, "channel", limit=10),
        "by_sales_type": count_by_field(churn, "sales_type"),
        "by_billing": count_by_field(churn, "AMB_status"),
        "by_digital": count_by_field(churn, "digital_status"),
        "by_agent": count_by_field(churn, "agent_name", limit=12),
        "monthly_outcomes": monthly_outcomes(episodes),
    }
