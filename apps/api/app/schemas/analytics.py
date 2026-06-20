from pydantic import BaseModel


class ChurnSummaryResponse(BaseModel):
    total_customers: int
    churned_customers: int
    churn_rate_percent: float


class RevenueImpactResponse(BaseModel):
    churned_customers: int
    lost_monthly_revenue: float
    lost_annual_revenue: float


class SupportTicketBreakdownItem(BaseModel):
    category: str
    sentiment: str
    ticket_count: int


class SupportAnalysisResponse(BaseModel):
    support_ticket_breakdown: list[SupportTicketBreakdownItem]


class RegionalChurnItem(BaseModel):
    region: str
    churned_customers: int


class RegionalChurnResponse(BaseModel):
    regional_churn: list[RegionalChurnItem]