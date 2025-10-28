from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LessonCreate(BaseModel):
    course_id: int
    title: str
    content: Optional[str] = None
    order: Optional[int] = None
    video_url: Optional[str] = None
    duration_minutes: Optional[int] = None
    xp_reward: Optional[int] = 0

class LessonResponse(BaseModel):
    id: int
    course_id: int
    title: str
    content: Optional[str]
    order: Optional[int]
    video_url: Optional[str]
    duration_minutes: Optional[int]
    xp_reward: int
    created_at: datetime
    
    class Config:
        from_attributes = True