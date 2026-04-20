from pydantic import BaseModel
from typing import List

class PredictionRequest(BaseModel):
    resume_text: str

class PredictionDetails(BaseModel):
    skill_count: int
    word_count: int
    experience_years: int
    graduation_year: int
    skill_experience_ratio: float
    timeline_issue: bool
    too_many_skills: bool

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    issues: List[str]
    details: PredictionDetails
