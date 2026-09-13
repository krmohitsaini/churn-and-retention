import csv
from functools import lru_cache
from pathlib import Path
from typing import Any

from backend.app.data.base_repository import BaseRepository


class CsvRepository(BaseRepository):
    def __init__(self, data_dir: Path, raw_data_file: Path):
        self.data_dir = data_dir
        self.raw_data_file = raw_data_file

    def customers(self) -> list[dict[str, Any]]:
        if self.raw_data_file.exists():
            return self._customers_from_contract_episodes()
        return self._read_csv("customers.csv")

    def churn_events(self) -> list[dict[str, Any]]:
        if self.raw_data_file.exists():
            return [
                {
                    "customer_id": row.get("business_partner_id"),
                    "churn_date": row.get("site_contract_end_date"),
                    "churn_reason": row.get("drop_type"),
                    "churn_type": "Site contract churn",
                    "product_type": row.get("commodity_type"),
                    "province": "Alberta",
                    "segment": row.get("channel"),
                    "estimated_lost_value": 0,
                    **row,
                }
                for row in self.contract_episodes()
                if row.get("drop_type") == "Churn"
            ]
        return self._read_csv("churn_events.csv")

    def propensity_scores(self) -> list[dict[str, Any]]:
        return self._read_csv("propensity_scores.csv")

    def customer_interactions(self) -> list[dict[str, Any]]:
        return self._read_csv("customer_interactions.csv")

    def offers(self) -> list[dict[str, Any]]:
        return self._read_csv("offers.csv")

    def contract_episodes(self) -> list[dict[str, Any]]:
        if not self.raw_data_file.exists():
            return []
        return self._read_csv_raw_path(str(self.raw_data_file), self.raw_data_file.stat().st_mtime)

    def source_version(self) -> str:
        if self.raw_data_file.exists():
            return f"csv-raw:{self.raw_data_file}:{self.raw_data_file.stat().st_mtime}"

        files = [
            "customers.csv",
            "churn_events.csv",
            "propensity_scores.csv",
            "customer_interactions.csv",
            "offers.csv",
        ]
        parts = []
        for filename in files:
            path = self.data_dir / filename
            if path.exists():
                parts.append(f"{filename}:{path.stat().st_mtime}")
        return "csv-sample:" + "|".join(parts)

    def _read_csv(self, filename: str) -> list[dict[str, Any]]:
        path = self.data_dir / filename
        if not path.exists():
            return []
        return self._read_csv_path(str(path), path.stat().st_mtime)

    @classmethod
    @lru_cache(maxsize=12)
    def _read_csv_path(cls, path_text: str, mtime: float) -> list[dict[str, Any]]:
        path = Path(path_text)
        with path.open(newline="", encoding="utf-8") as handle:
            return [cls._coerce_row(row) for row in csv.DictReader(handle)]

    @classmethod
    @lru_cache(maxsize=3)
    def _read_csv_raw_path(cls, path_text: str, mtime: float) -> list[dict[str, Any]]:
        path = Path(path_text)
        with path.open(newline="", encoding="utf-8") as handle:
            return [dict(row) for row in csv.DictReader(handle)]

    @classmethod
    def _coerce_row(cls, row: dict[str, str]) -> dict[str, Any]:
        return {key: cls._coerce_value(value) for key, value in row.items()}

    @staticmethod
    def _coerce_value(value: str) -> Any:
        if value is None:
            return None
        clean = value.strip()
        if clean == "":
            return None
        if clean.lower() in {"true", "false"}:
            return clean.lower() == "true"
        try:
            if "." in clean:
                return float(clean)
            return int(clean)
        except ValueError:
            return clean

    def _customers_from_contract_episodes(self) -> list[dict[str, Any]]:
        partners: dict[str, dict[str, Any]] = {}
        for row in self.contract_episodes():
            partner_id = str(row.get("business_partner_id"))
            partner = partners.setdefault(
                partner_id,
                {
                    "customer_id": partner_id,
                    "customer_name": partner_id,
                    "province": "Alberta",
                    "city": str(row.get("zipcode") or "")[:3],
                    "customer_type": "Business Partner",
                    "segment": row.get("channel"),
                    "product_type": row.get("commodity_type"),
                    "plan_type": row.get("sales_type"),
                    "contract_status": "Active",
                    "acquisition_channel": row.get("channel"),
                    "signup_date": row.get("sign_up_date"),
                    "tenure_months": 0,
                    "estimated_annual_value": 0,
                    "current_status": "Inactive",
                    "site_count": 0,
                    "active_site_count": 0,
                    "churned_site_count": 0,
                    "digital_status": row.get("digital_status"),
                    "dob_status": row.get("dob_status"),
                },
            )
            partner["site_count"] += 1
            if row.get("drop_type") == "Active":
                partner["active_site_count"] += 1
                partner["current_status"] = "Active"
            if row.get("drop_type") == "Churn":
                partner["churned_site_count"] += 1
        return list(partners.values())
