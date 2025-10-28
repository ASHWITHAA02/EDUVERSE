from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class GameScore(Base):
    """Track user scores in educational games"""
    __tablename__ = "game_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_name = Column(String, nullable=False)  # coding_challenge, memory_match, etc.
    score = Column(Integer, nullable=False)
    time_taken_seconds = Column(Integer)
    difficulty_level = Column(String, default="medium")  # easy, medium, hard
    xp_earned = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="game_scores")