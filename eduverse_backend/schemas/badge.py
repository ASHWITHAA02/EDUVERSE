from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BadgeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    criteria: str
    xp_reward: int = 0

class BadgeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    icon: Optional[str]
    criteria: str
    xp_reward: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserBadgeResponse(BaseModel):
    id: int
    user_id: int
    badge_id: int
    earned_at: datetime
    badge: BadgeResponse
    
    class Config:
        from_attributes = True