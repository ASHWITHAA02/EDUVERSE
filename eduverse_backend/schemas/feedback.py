from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FeedbackCreate(BaseModel):
    category: str  # bug, feature, improvement, general
    subject: str
    message: str
    rating: Optional[int] = None  # 1-5 stars

class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    category: str
    subject: str
    message: str
    rating: Optional[int]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True