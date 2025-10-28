from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProgressCreate(BaseModel):
    user_id: int
    course_id: int

class ProgressResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    completion_percentage: float
    is_completed: bool
    started_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class LessonProgressCreate(BaseModel):
    user_id: int
    lesson_id: int
    time_spent_minutes: Optional[int] = 0

class LessonProgressResponse(BaseModel):
    id: int
    user_id: int
    lesson_id: int
    is_completed: bool
    time_spent_minutes: int
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True