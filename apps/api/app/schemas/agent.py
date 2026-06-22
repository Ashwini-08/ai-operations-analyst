from pydantic import BaseModel


class ChurnInvestigationRequest(BaseModel):
    question: str


class ChurnInvestigationAgentResponse(BaseModel):
    question: str
    executive_summary: str
    key_findings: list[str]
    recommended_actions: list[str]
    priority_level: str
    source_metrics: dict