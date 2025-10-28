from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GameScoreSubmit(BaseModel):
    game_name: str
    score: int
    time_taken_seconds: Optional[int] = None
    difficulty_level: str = "medium"

class GameScoreResponse(BaseModel):
    id: int
    user_id: int
    game_name: str
    score: int
    time_taken_seconds: Optional[int]
    difficulty_level: str
    xp_earned: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class GameLeaderboardEntry(BaseModel):
    rank: int
    username: str
    score: int
    time_taken_seconds: Optional[int]
    created_at: datetime