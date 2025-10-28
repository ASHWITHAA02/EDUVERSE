from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.quiz import Quiz, QuizQuestion, QuizOption
from models.quiz_attempt import QuizAttempt
from models.user import User
from schemas.quiz import QuizSubmission
from routes.auth import get_current_user
from services.ai_quiz_service import generate_quiz_feedback
from datetime import datetime

router = APIRouter()

@router.post("/submit")
async def submit_quiz(
    submission: QuizSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get quiz
    quiz = db.query(Quiz).filter(Quiz.id == submission.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Calculate score
    total_points = 0
    earned_points = 0
    correct_count = 0
    
    for question in quiz.questions:
        total_points += question.points
        user_answer = submission.answers.get(question.id)
        
        if user_answer:
            correct_option = db.query(QuizOption).filter(
                QuizOption.question_id == question.id,
                QuizOption.id == user_answer,
                QuizOption.is_correct == True
            ).first()
            
            if correct_option:
                earned_points += question.points
                correct_count += 1
    
    score = (earned_points / total_points * 100) if total_points > 0 else 0
    passed = 1 if score >= quiz.passing_score else 0
    
    # Generate AI feedback
    ai_feedback = await generate_quiz_feedback(
        score=score,
        total_questions=len(quiz.questions),
        correct_answers=correct_count,
        topic=quiz.title
    )
    
    # Save attempt
    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz.id,
        score=score,
        answers=submission.answers,
        time_taken_minutes=submission.time_taken_minutes,
        passed=passed
    )
    db.add(attempt)
    
    # Award XP if passed
    xp_earned = 0
    if passed:
        current_user.total_xp += quiz.xp_reward
        xp_earned = quiz.xp_reward
        # Level up logic (every 1000 XP = 1 level)
        current_user.level = (current_user.total_xp // 1000) + 1
    
    db.commit()
    
    return {
        "score": score,
        "passed": bool(passed),
        "earned_points": earned_points,
        "total_points": total_points,
        "correct_answers": correct_count,
        "total_questions": len(quiz.questions),
        "xp_earned": xp_earned,
        "ai_feedback": ai_feedback,
        "must_retake": score < 50
    }

@router.get("/attempts/{quiz_id}")
def get_quiz_attempts(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.quiz_id == quiz_id,
        QuizAttempt.user_id == current_user.id
    ).order_by(QuizAttempt.created_at.desc()).all()
    
    return attempts