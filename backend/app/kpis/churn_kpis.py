from collections import defaultdict
from typing import Any


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

