from sqlalchemy.orm import Session
from models.course import Course
from models.lesson import Lesson
from typing import List

async def get_personalized_recommendations(user_id: int, quiz_attempts: List, db: Session):
    """Generate personalized learning recommendations based on user performance"""
    
    if not quiz_attempts:
        # New user - recommend beginner courses
        beginner_courses = db.query(Course).filter(
            Course.difficulty == "Beginner"
        ).limit(3).all()
        
        return {
            "message": "Welcome! Here are some beginner courses to get you started.",
            "recommendations": beginner_courses,
            "reason": "new_user"
        }
    
    # Calculate average score
    avg_score = sum(attempt.score for attempt in quiz_attempts) / len(quiz_attempts)
    
    # Determine weak areas (quizzes with score < 70)
    weak_quizzes = [attempt for attempt in quiz_attempts if attempt.score < 70]
    
    if weak_quizzes:
        # Recommend review materials
        weak_quiz_ids = [attempt.quiz_id for attempt in weak_quizzes]
        review_lessons = db.query(Lesson).filter(
            Lesson.quizzes.any(id__in=weak_quiz_ids)
        ).limit(3).all()
        
        return {
            "message": "We noticed you might need some review in these areas.",
            "recommendations": review_lessons,
            "reason": "needs_review",
            "average_score": avg_score
        }
    
    # High performer - recommend advanced content
    if avg_score >= 80:
        advanced_courses = db.query(Course).filter(
            Course.difficulty.in_(["Intermediate", "Advanced"])
        ).limit(3).all()
        
        return {
            "message": "Great job! You're ready for more advanced content.",
            "recommendations": advanced_courses,
            "reason": "high_performer",
            "average_score": avg_score
        }
    
    # Average performer - recommend intermediate content
    intermediate_courses = db.query(Course).filter(
        Course.difficulty == "Intermediate"
    ).limit(3).all()
    
    return {
        "message": "Keep up the good work! Here are some courses to continue your learning.",
        "recommendations": intermediate_courses,
        "reason": "steady_progress",
        "average_score": avg_score
    }