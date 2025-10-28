from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.lesson import Lesson
from schemas.lesson_schema import LessonCreate, LessonResponse
from services.lesson_summarizer_service import generate_lesson_summary
from typing import List

router = APIRouter()

@router.get("/course/{course_id}", response_model=List[LessonResponse])
def get_lessons_by_course(course_id: int, db: Session = Depends(get_db)):
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).order_by(Lesson.order).all()
    return lessons

@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.post("/", response_model=LessonResponse)
def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    new_lesson = Lesson(**lesson.dict())
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson

@router.put("/{lesson_id}", response_model=LessonResponse)
def update_lesson(lesson_id: int, lesson: LessonCreate, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    for key, value in lesson.dict().items():
        setattr(db_lesson, key, value)
    
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

@router.delete("/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    db.delete(db_lesson)
    db.commit()
    return {"message": "Lesson deleted successfully"}

@router.post("/{lesson_id}/generate-summary")
async def generate_summary(lesson_id: int, db: Session = Depends(get_db)):
    """Generate AI summary for a lesson"""
    
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Generate summary
    summary = await generate_lesson_summary(lesson.title, lesson.content)
    
    # Update lesson with summary
    lesson.ai_summary = summary
    db.commit()
    db.refresh(lesson)
    
    return {
        "message": "Summary generated successfully",
        "summary": summary
    }

@router.get("/{lesson_id}/summary")
def get_lesson_summary(lesson_id: int, db: Session = Depends(get_db)):
    """Get AI summary for a lesson"""
    
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    if not lesson.ai_summary:
        return {
            "message": "Summary not yet generated",
            "summary": None
        }
    
    return {
        "lesson_id": lesson.id,
        "lesson_title": lesson.title,
        "summary": lesson.ai_summary
    }