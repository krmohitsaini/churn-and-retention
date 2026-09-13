from typing import Any, Optional


class CustomerService:
    def __init__(self, repository):
        self.repository = repository

    def detail(self, customer_id: str) -> Optional[dict[str, Any]]:
        customer = next(
            (row for row in self.repository.customers() if str(row.get("customer_id")) == customer_id),
            None,
        )
        if not customer:
            return None

        propensity = next(
            (row for row in self.repository.propensity_scores() if str(row.get("customer_id")) == customer_id),
            None,
        )
        interactions = [
            row for row in self.repository.customer_interactions() if str(row.get("customer_id")) == customer_id
        ]
        return {"customer": customer, "propensity": propensity, "interactions": interactions}
