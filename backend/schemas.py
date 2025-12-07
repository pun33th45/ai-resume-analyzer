# backend/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Dict, List

class AnalyzeResponse(BaseModel):
    ats_score: float
    jd_match: float
    skills_found: Dict[str, List[str]]
    suggestion: str

class AnalysisRecord(BaseModel):
    name: str
    email: EmailStr
    job_title: str
    ats_score: float
    jd_match: float
    created_at: str
