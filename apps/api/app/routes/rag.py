from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.rag import RagSearchResponse
from app.services.retrieval_service import retrieve_relevant_context

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.get("/search", response_model=RagSearchResponse)
def search_knowledge_base(
    query: str = Query(..., min_length=3),
    top_k: int = Query(default=3, ge=1, le=10),
    db: Session = Depends(get_db),
):
    results = retrieve_relevant_context(
        query=query,
        db=db,
        top_k=top_k,
    )

    return {
        "query": query,
        "results": results,
    }