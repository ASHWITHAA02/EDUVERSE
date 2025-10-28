from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    
    # AI Analysis Results
    skills_found = Column(JSON)  # List of skills found in resume
    skills_missing = Column(JSON)  # List of recommended skills to add
    job_titles = Column(JSON)  # List of suitable job titles
    improvement_suggestions = Column(Text)  # AI suggestions for improvement
    overall_score = Column(Integer)  # 0-100 score
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="resume_analyses")