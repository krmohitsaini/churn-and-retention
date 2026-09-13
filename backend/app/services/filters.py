from typing import Any


def apply_filters(rows: list[dict[str, Any]], filters: dict[str, Any]) -> list[dict[str, Any]]:
    filtered = rows
    for field, value in filters.items():
        if value in (None, "", "All"):
            continue
        filtered = [row for row in filtered if _normalize(row.get(field)) == _normalize(value)]
    return filtered


def _normalize(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value).strip().lower()


def tenure_band(tenure_months: Any) -> str:
    months = float(tenure_months or 0)
    if months < 12:
        return "0-12 months"
    if months < 36:
        return "1-3 years"
    if months < 60:
        return "3-5 years"
    return "5+ years"
