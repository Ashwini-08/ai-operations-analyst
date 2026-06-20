from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.investigations import ChurnInvestigationResponse
from app.services.investigation_service import investigate_churn

router = APIRouter(
    prefix="/investigations",
    tags=["Investigations"],
)


@router.get("/churn", response_model=ChurnInvestigationResponse)
def get_churn_investigation(db: Session = Depends(get_db)):
    return investigate_churn(db)