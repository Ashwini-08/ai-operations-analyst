from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.agent import (
    ChurnInvestigationAgentResponse,
    ChurnInvestigationRequest,
)
from app.services.agent_service import generate_churn_investigation_response

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.post(
    "/investigate-churn",
    response_model=ChurnInvestigationAgentResponse,
)
def investigate_churn_with_agent(
    request: ChurnInvestigationRequest,
    db: Session = Depends(get_db),
):
    return generate_churn_investigation_response(
        question=request.question,
        db=db,
    )