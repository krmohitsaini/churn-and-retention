import csv
import io
from typing import Any


class ExportService:
    def propensity_csv(self, customers: list[dict[str, Any]]) -> str:
        fields = [
            "customer_id",
            "customer_name",
            "province",
            "segment",
            "product_type",
            "estimated_annual_value",
            "churn_probability",
            "risk_band",
            "prediction_window_days",
            "top_driver",
            "recommended_action",
            "recommended_offer",
        ]
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(customers)
        return buffer.getvalue()

