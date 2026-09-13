from typing import Any, Optional

from backend.app.kpis.revenue_kpis import revenue_at_risk
from backend.app.models.explainability import format_drivers
from backend.app.schemas.common import MetricCard
from backend.app.services.filters import apply_filters


class PropensityService:
    def __init__(self, repository):
        self.repository = repository

    def summary(self, filters: dict[str, Any]) -> dict[str, Any]:
        customers = self.customers(filters)
        high_risk = [customer for customer in customers if customer.get("risk_band") in {"High", "Critical"}]
        critical = [customer for customer in customers if customer.get("risk_band") == "Critical"]
        metrics = [
            MetricCard(label="Scored customers", value=len(customers)).model_dump(),
            MetricCard(label="High or critical risk", value=len(high_risk)).model_dump(),
            MetricCard(label="Critical risk", value=len(critical)).model_dump(),
            MetricCard(label="Revenue at risk", value=round(revenue_at_risk(customers), 2)).model_dump(),
        ]
        return {"metrics": metrics, "customers": customers}

    def customers(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        customers_by_id = {str(customer.get("customer_id")): customer for customer in self.repository.customers()}
        rows = []
        for score in self.repository.propensity_scores():
            customer = customers_by_id.get(str(score.get("customer_id")), {})
            row = {
                **customer,
                **score,
                "top_driver": score.get("top_driver_1"),
                "drivers": format_drivers(score),
            }
            rows.append(row)
        rows = apply_filters(rows, filters)
        return sorted(rows, key=lambda row: float(row.get("churn_probability") or 0), reverse=True)

    def customer(self, customer_id: str) -> Optional[dict[str, Any]]:
        for row in self.customers({}):
            if str(row.get("customer_id")) == customer_id:
                return row
        return None

    def drivers(self) -> list[dict[str, Any]]:
        counts: dict[str, float] = {}
        for score in self.repository.propensity_scores():
            for driver in format_drivers(score):
                name = driver.get("driver")
                if not name:
                    continue
                counts[name] = counts.get(name, 0) + float(driver.get("weight") or 0)
        return [{"name": name, "value": round(value, 2)} for name, value in sorted(counts.items())]
