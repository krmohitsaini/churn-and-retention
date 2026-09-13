from pydantic import BaseModel

from backend.app.schemas.common import ChartPoint, MetricCard


class PortfolioSummary(BaseModel):
    metrics: list[MetricCard]
    by_province: list[ChartPoint]
    by_segment: list[ChartPoint]
    by_product: list[ChartPoint]
    by_tenure: list[ChartPoint]

