from pydantic import BaseModel

from backend.app.schemas.common import ChartPoint, MetricCard


class ChurnTimeseriesPoint(BaseModel):
    month: str
    churned_customers: int


class ChurnSummary(BaseModel):
    metrics: list[MetricCard]
    timeseries: list[ChurnTimeseriesPoint]
    by_segment: list[ChartPoint]
    by_reason: list[ChartPoint]
    by_province: list[ChartPoint]

