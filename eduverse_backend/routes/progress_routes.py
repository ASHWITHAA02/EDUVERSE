from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.progress import Progress, LessonProgress
from models.user import User
from models.lesson import Lesson
from schemas.progress import ProgressResponse, LessonProgressCreate, LessonProgressResponse
from routes.auth import get_current_user
from typing import List
from datetime import datetime

router = APIRouter()

@router.get("/course/{course_id}", response_model=ProgressResponse)
def get_course_progress(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    progress = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.course_id == course_id
    ).first()
    
    if not progress:
        # Create new progress
        progress = Progress(user_id=current_user.id, course_id=course_id)
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    return progress

@router.post("/lesson/complete", response_model=LessonProgressResponse)
def complete_lesson(
    lesson_progress: LessonProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if already completed
    existing = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id == lesson_progress.lesson_id
    ).first()
    
    if existing:
        existing.is_completed = True
        existing.completed_at = datetime.utcnow()
        existing.time_spent_minutes += lesson_progress.time_spent_minutes
        db.commit()
        db.refresh(existing)
        lesson_prog = existing
    else:
        new_progress = LessonProgress(
            user_id=current_user.id,
            lesson_id=lesson_progress.lesson_id,
            is_completed=True,
            time_spent_minutes=lesson_progress.time_spent_minutes,
            completed_at=datetime.utcnow()
        )
        db.add(new_progress)
        db.commit()
        db.refresh(new_progress)
        lesson_prog = new_progress
    
    # Update course progress
    lesson = db.query(Lesson).filter(Lesson.id == lesson_progress.lesson_id).first()
    if lesson:
        course_progress = db.query(Progress).filter(
            Progress.user_id == current_user.id,
            Progress.course_id == lesson.course_id
        ).first()
        
        if not course_progress:
            course_progress = Progress(user_id=current_user.id, course_id=lesson.course_id)
            db.add(course_progress)
        
        # Calculate completion percentage
        total_lessons = db.query(Lesson).filter(Lesson.course_id == lesson.course_id).count()
        completed_lessons = db.query(LessonProgress).filter(
            LessonProgress.user_id == current_user.id,
            LessonProgress.is_completed == True,
            LessonProgress.lesson_id.in_(
                db.query(Lesson.id).filter(Lesson.course_id == lesson.course_id)
            )
        ).count()
        
        course_progress.completion_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
        if course_progress.completion_percentage >= 100:
            course_progress.is_completed = True
            course_progress.completed_at = datetime.utcnow()
        
        # Award XP
        current_user.total_xp += lesson.xp_reward
        current_user.level = (current_user.total_xp // 1000) + 1
        
        db.commit()
    
    return lesson_prog

@router.get("/lessons/user", response_model=List[LessonProgressResponse])
def get_user_lesson_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id
    ).all()
    return progress