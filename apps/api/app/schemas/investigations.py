from pydantic import BaseModel


class ChurnInvestigationMetrics(BaseModel):
    total_customers: int
    churned_customers: int
    churn_rate_percent: float
    lost_monthly_revenue: float
    lost_annual_revenue: float
    top_region: str
    top_cancellation_reason: str


class ChurnInvestigationResponse(BaseModel):
    problem: str
    summary: str
    findings: list[str]
    recommendations: list[str]
    metrics: ChurnInvestigationMetrics