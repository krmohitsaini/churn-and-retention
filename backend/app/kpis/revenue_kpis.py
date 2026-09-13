from typing import Any


def lost_estimated_annual_value(churn_events: list[dict[str, Any]]) -> float:
    """Sum estimated annual value lost through churn events."""
    return sum(float(event.get("estimated_lost_value") or 0) for event in churn_events)


def revenue_at_risk(scored_customers: list[dict[str, Any]]) -> float:
    """Estimate revenue at risk as value multiplied by churn probability."""
    total = 0.0
    for customer in scored_customers:
        total += float(customer.get("estimated_annual_value") or 0) * float(customer.get("churn_probability") or 0)
    return round(total, 2)

