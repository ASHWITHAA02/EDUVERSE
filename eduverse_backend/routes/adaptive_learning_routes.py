from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.quiz_attempt import QuizAttempt
from models.lesson import Lesson
from routes.auth import get_current_user
from services.adaptive_learning_service import get_personalized_recommendations

router = APIRouter()

@router.get("/recommendations")
async def get_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get user's quiz performance
    quiz_attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id
    ).order_by(QuizAttempt.created_at.desc()).limit(10).all()
    
    # Get recommendations
    recommendations = await get_personalized_recommendations(
        user_id=current_user.id,
        quiz_attempts=quiz_attempts,
        db=db
    )
    
    return recommendations

@router.get("/learning-path")
def get_learning_path(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get user's performance data
    quiz_attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id
    ).all()
    
    # Calculate average score
    avg_score = sum(attempt.score for attempt in quiz_attempts) / len(quiz_attempts) if quiz_attempts else 0
    
    # Determine difficulty level
    if avg_score >= 80:
        difficulty = "Advanced"
    elif avg_score >= 60:
        difficulty = "Intermediate"
    else:
        difficulty = "Beginner"
    
    # Get recommended lessons
    recommended_lessons = db.query(Lesson).join(Lesson.course).filter(
        Lesson.course.has(difficulty=difficulty)
    ).limit(5).all()
    
    return {
        "current_level": difficulty,
        "average_score": avg_score,
        "recommended_lessons": recommended_lessons,
        "total_attempts": len(quiz_attempts)
    }