from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

class QuizOptionCreate(BaseModel):
    option_text: str
    is_correct: bool
    order: Optional[int] = None

class QuizQuestionCreate(BaseModel):
    question_text: str
    question_type: str = "multiple_choice"
    points: int = 10
    order: Optional[int] = None
    options: List[QuizOptionCreate] = []

class QuizCreate(BaseModel):
    lesson_id: int
    title: str
    description: Optional[str] = None
    passing_score: int = 70
    time_limit_minutes: Optional[int] = None
    xp_reward: int = 0
    questions: List[QuizQuestionCreate] = []

class QuizOptionResponse(BaseModel):
    id: int
    option_text: str
    is_correct: bool
    order: Optional[int]
    
    class Config:
        from_attributes = True

class QuizQuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    points: int
    order: Optional[int]
    options: List[QuizOptionResponse] = []
    
    class Config:
        from_attributes = True

class QuizResponse(BaseModel):
    id: int
    lesson_id: int
    title: str
    description: Optional[str]
    passing_score: int
    time_limit_minutes: Optional[int]
    xp_reward: int
    created_at: datetime
    questions: List[QuizQuestionResponse] = []
    
    class Config:
        from_attributes = True

class QuizSubmission(BaseModel):
    quiz_id: int
    answers: Dict[int, int]  # question_id: selected_option_id
    time_taken_minutes: Optional[int] = None