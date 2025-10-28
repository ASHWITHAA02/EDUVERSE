from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.feedback import Feedback
from schemas.feedback import FeedbackCreate, FeedbackResponse
from routes.auth import get_current_user
from typing import List

router = APIRouter()

@router.post("/submit", response_model=FeedbackResponse)
def submit_feedback(
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit user feedback"""
    
    # Validate category
    valid_categories = ["bug", "feature", "improvement", "general"]
    if feedback_data.category not in valid_categories:
        raise HTTPException(status_code=400, detail=f"Invalid category. Must be one of: {', '.join(valid_categories)}")
    
    # Validate rating if provided
    if feedback_data.rating and (feedback_data.rating < 1 or feedback_data.rating > 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    # Create feedback
    feedback = Feedback(
        user_id=current_user.id,
        category=feedback_data.category,
        subject=feedback_data.subject,
        message=feedback_data.message,
        rating=feedback_data.rating,
        status="pending"
    )
    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return feedback

@router.get("/my-feedback", response_model=List[FeedbackResponse])
def get_my_feedback(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all feedback submitted by current user"""
    
    feedbacks = db.query(Feedback).filter(
        Feedback.user_id == current_user.id
    ).order_by(Feedback.created_at.desc()).all()
    
    return feedbacks

@router.get("/all", response_model=List[FeedbackResponse])
def get_all_feedback(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all feedback (admin feature - for now returns all)"""
    
    feedbacks = db.query(Feedback).order_by(
        Feedback.created_at.desc()
    ).limit(limit).all()
    
    return feedbacks

@router.delete("/{feedback_id}")
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete user's own feedback"""
    
    feedback = db.query(Feedback).filter(
        Feedback.id == feedback_id,
        Feedback.user_id == current_user.id
    ).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    db.delete(feedback)
    db.commit()
    
    return {"message": "Feedback deleted successfully"}