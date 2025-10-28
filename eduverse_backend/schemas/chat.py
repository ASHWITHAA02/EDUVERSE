from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None  # course_id, lesson_id, etc.
    lesson_id: Optional[int] = None  # To fetch lesson content

class ChatResponse(BaseModel):
    id: int
    user_id: int
    message: str
    response: str
    context: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True