from pydantic import BaseModel


class RagSearchResult(BaseModel):
    id: int
    doc_name: str
    section_title: str | None = None
    content: str
    score: float


class RagSearchResponse(BaseModel):
    query: str
    results: list[RagSearchResult]