from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_reports: int
    total_analyses: int
    total_patients: int
    abnormal_reports: int


class RiskDistributionItem(BaseModel):
    risk_level: str
    count: int


class RiskDistributionResponse(BaseModel):
    distribution: list[RiskDistributionItem]


class TrendItem(BaseModel):
    period: str
    count: int


class AnalyticsTrendResponse(BaseModel):
    trends: list[TrendItem]