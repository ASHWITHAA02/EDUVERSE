from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any

class AssessmentSubmit(BaseModel):
    course_id: int
    answers: Dict[int, Any]  # question_id: answer

class AssessmentResponse(BaseModel):
    id: int
    course_id: int
    user_id: int
    score: float
    recommended_lessons: List[int]
    skill_gaps: List[str]
    ai_feedback: str
    can_skip_basics: bool
    must_retake: bool
    created_at: datetime
    
    class Config:
        from_attributes = True