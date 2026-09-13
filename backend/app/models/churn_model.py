from typing import Any


def score_customer(customer: dict[str, Any]) -> dict[str, Any]:
    """Placeholder for future model scoring. Production scoring should run outside the app."""
    tenure = float(customer.get("tenure_months") or 0)
    base_score = 0.32 if tenure < 12 else 0.18
    return {
        "customer_id": customer.get("customer_id"),
        "churn_probability": base_score,
        "model_version": "placeholder-local",
    }

