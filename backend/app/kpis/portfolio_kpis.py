from typing import Any


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


def count_by_field(customers: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    """Count active customers by a categorical portfolio field."""
    counts: dict[str, int] = {}
    for customer in customers:
        if customer.get("current_status") != "Active":
            continue
        value = str(customer.get(field) or "Unknown")
        counts[value] = counts.get(value, 0) + 1
    return [{"name": name, "value": value} for name, value in sorted(counts.items())]

