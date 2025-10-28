from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Leaderboard(Base):
    __tablename__ = "leaderboard"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    total_xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    rank = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)