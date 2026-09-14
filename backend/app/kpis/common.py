from typing import Any, Optional


def display_value(value: Any) -> str:
    """Format raw data values into user-facing bucket labels."""
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


def count_by_field(rows: list[dict[str, Any]], field: str, limit: Optional[int] = None) -> list[dict[str, Any]]:
    """Count rows by a categorical field and return chart-ready points."""
    counts: dict[str, int] = {}
    for row in rows:
        value = display_value(row.get(field))
        counts[value] = counts.get(value, 0) + 1
    points = [{"name": name, "value": value} for name, value in counts.items()]
    points = sorted(points, key=lambda point: point["value"], reverse=True)
    return points[:limit] if limit else points


def monthly_timeseries(
    rows: list[dict[str, Any]],
    date_field: str,
    value_field: str,
    unique_field: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Count records by YYYY-MM month, optionally counting unique IDs instead of rows."""
    counts: dict[str, Any] = {}
    for row in rows:
        raw_date = str(row.get(date_field) or "")
        month = raw_date[:7] if len(raw_date) >= 7 else "Unknown"
        if unique_field:
            counts.setdefault(month, set()).add(row.get(unique_field))
        else:
            counts[month] = int(counts.get(month, 0)) + 1

    return [
        {"month": month, value_field: len(value) if isinstance(value, set) else value}
        for month, value in sorted(counts.items())
    ]

