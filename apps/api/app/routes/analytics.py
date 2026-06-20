from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.analytics import (
    ChurnSummaryResponse,
    RegionalChurnResponse,
    RevenueImpactResponse,
    SupportAnalysisResponse,
)
from app.services.analytics_service import (
    get_churn_summary_data,
    get_regional_churn_data,
    get_revenue_impact_data,
    get_support_analysis_data,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/churn-summary", response_model=ChurnSummaryResponse)
def get_churn_summary(db: Session = Depends(get_db)):
    return get_churn_summary_data(db)


@router.get("/revenue-impact", response_model=RevenueImpactResponse)
def get_revenue_impact(db: Session = Depends(get_db)):
    return get_revenue_impact_data(db)


@router.get("/support-analysis", response_model=SupportAnalysisResponse)
def get_support_analysis(db: Session = Depends(get_db)):
    return get_support_analysis_data(db)


@router.get("/regional-churn", response_model=RegionalChurnResponse)
def get_regional_churn(db: Session = Depends(get_db)):
    return get_regional_churn_data(db)