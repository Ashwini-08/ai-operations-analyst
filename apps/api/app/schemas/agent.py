from pydantic import BaseModel


class ChurnInvestigationRequest(BaseModel):
    question: str


class RetrievedContextItem(BaseModel):
    id: int
    doc_name: str
    section_title: str | None = None
    content: str
    score: float


class ChurnInvestigationAgentResponse(BaseModel):
    question: str
    executive_summary: str
    key_findings: list[str]
    recommended_actions: list[str]
    priority_level: str
    source_metrics: dict
    retrieved_context: list[RetrievedContextItem]