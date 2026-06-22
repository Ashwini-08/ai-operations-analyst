import json
import re

import requests
from sqlalchemy.orm import Session

from app.services.investigation_service import investigate_churn


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"


def call_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["response"]


def extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def build_churn_prompt(question: str, investigation: dict) -> str:
    return f"""
You are an AI Operations Analyst.

User question:
{question}

Use ONLY the following investigation data.
Do not invent numbers.
Do not mention data that is not provided.

Investigation data:
{json.dumps(investigation, indent=2)}

Return ONLY valid JSON with this exact structure:
{{
  "executive_summary": "string",
  "key_findings": ["string", "string", "string"],
  "recommended_actions": ["string", "string", "string"],
  "priority_level": "low | medium | high | critical"
}}

Rules:
- executive_summary must be concise and business-friendly.
- key_findings must be grounded in the provided metrics.
- recommended_actions must be specific and operational.
- priority_level must reflect churn rate and revenue impact.
"""


def fallback_response(question: str, investigation: dict) -> dict:
    metrics = investigation["metrics"]

    priority_level = "medium"

    if metrics["churn_rate_percent"] >= 15:
        priority_level = "high"

    if metrics["lost_annual_revenue"] >= 1_000_000:
        priority_level = "critical"

    return {
        "question": question,
        "executive_summary": investigation["summary"],
        "key_findings": investigation["findings"],
        "recommended_actions": investigation["recommendations"],
        "priority_level": priority_level,
        "source_metrics": metrics,
    }


def generate_churn_investigation_response(question: str, db: Session):
    investigation = investigate_churn(db)
    metrics = investigation["metrics"]

    prompt = build_churn_prompt(question, investigation)

    try:
        raw_output = call_ollama(prompt)
        parsed_output = extract_json(raw_output)

        return {
            "question": question,
            "executive_summary": parsed_output["executive_summary"],
            "key_findings": parsed_output["key_findings"],
            "recommended_actions": parsed_output["recommended_actions"],
            "priority_level": parsed_output["priority_level"],
            "source_metrics": metrics,
        }

    except Exception:
        return fallback_response(question, investigation)