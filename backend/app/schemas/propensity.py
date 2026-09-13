from typing import Optional, Union

from pydantic import BaseModel, Field

from backend.app.schemas.common import MetricCard


class ChurnDriver(BaseModel):
    driver: Optional[str]
    weight: Optional[Union[float, int]]


class PropensityCustomer(BaseModel):
    customer_id: str
    customer_name: Optional[str] = None
    province: Optional[str] = None
    segment: Optional[str] = None
    product_type: Optional[str] = None
    tenure_months: Optional[Union[int, float]] = None
    estimated_annual_value: Optional[Union[int, float]] = None
    churn_probability: float
    risk_band: str
    prediction_window_days: int
    top_driver: Optional[str] = None
    recommended_action: Optional[str] = None
    recommended_offer: Optional[str] = None
    drivers: list[ChurnDriver] = Field(default_factory=list)


class PropensitySummary(BaseModel):
    metrics: list[MetricCard]
    customers: list[PropensityCustomer]
