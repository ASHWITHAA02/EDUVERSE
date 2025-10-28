from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    estimated_hours: Optional[int] = None
    xp_reward: Optional[int] = 0
    thumbnail: Optional[str] = None

class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: Optional[str]
    difficulty: Optional[str]
    estimated_hours: Optional[int]
    xp_reward: int
    thumbnail: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True