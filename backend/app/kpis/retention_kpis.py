from typing import Any


def retention_rate(customers: list[dict[str, Any]], churn_events: list[dict[str, Any]]) -> float:
    """Retention rate equals one minus churned customers divided by total known customers."""
    total_customers = len(customers)
    if total_customers == 0:
        return 0
    return round(1 - (len(churn_events) / total_customers), 4)


def net_customer_growth(customers: list[dict[str, Any]], churn_events: list[dict[str, Any]]) -> int:
    """Simple net customer growth proxy using active customers minus churn events."""
    active = sum(1 for customer in customers if customer.get("current_status") == "Active")
    return active - len(churn_events)

