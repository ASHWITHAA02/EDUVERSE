from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class CourseAssessment(Base):
    """Pre-course assessment quiz to determine user's knowledge level"""
    __tablename__ = "course_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Float, nullable=False)  # Percentage score
    
    # AI Recommendations
    recommended_lessons = Column(JSON)  # List of lesson IDs to focus on
    skill_gaps = Column(JSON)  # Areas where user needs improvement
    ai_feedback = Column(Text)  # Personalized AI feedback
    
    can_skip_basics = Column(Integer, default=0)  # 1 if score > 80%, 0 otherwise
    must_retake = Column(Integer, default=0)  # 1 if score < 50%, 0 otherwise
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="assessments")
    user = relationship("User", back_populates="course_assessments")