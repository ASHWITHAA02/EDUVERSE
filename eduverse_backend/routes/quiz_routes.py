from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.quiz import Quiz, QuizQuestion, QuizOption
from models.lesson import Lesson
from schemas.quiz import QuizCreate, QuizResponse
from services.ai_quiz_service import generate_quiz_questions
from typing import List

router = APIRouter()

@router.get("/lesson/{lesson_id}", response_model=List[QuizResponse])
def get_quizzes_by_lesson(lesson_id: int, db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).filter(Quiz.lesson_id == lesson_id).all()
    return quizzes

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.post("/", response_model=QuizResponse)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    # Create quiz
    quiz_data = quiz.dict(exclude={'questions'})
    new_quiz = Quiz(**quiz_data)
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    
    # Create questions and options
    for question_data in quiz.questions:
        options_data = question_data.pop('options', [])
        question = QuizQuestion(quiz_id=new_quiz.id, **question_data)
        db.add(question)
        db.commit()
        db.refresh(question)
        
        for option_data in options_data:
            option = QuizOption(question_id=question.id, **option_data)
            db.add(option)
        
        db.commit()
    
    db.refresh(new_quiz)
    return new_quiz

@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    db.delete(db_quiz)
    db.commit()
    return {"message": "Quiz deleted successfully"}

@router.get("/{quiz_id}/dynamic-questions")
async def get_dynamic_quiz_questions(
    quiz_id: int,
    num_questions: int = 5,
    db: Session = Depends(get_db)
):
    """Generate dynamic quiz questions using AI (different each time)"""
    
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Get lesson to determine topic
    lesson = db.query(Lesson).filter(Lesson.id == quiz.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Generate dynamic questions
    dynamic_quiz = await generate_quiz_questions(
        topic=lesson.title,
        difficulty="Beginner",  # You can make this dynamic based on user level
        num_questions=num_questions
    )
    
    if "error" in dynamic_quiz:
        raise HTTPException(status_code=500, detail=dynamic_quiz["error"])
    
    return {
        "quiz_id": quiz_id,
        "quiz_title": quiz.title,
        "lesson_title": lesson.title,
        "questions": dynamic_quiz.get("questions", []),
        "note": "These questions are dynamically generated and will be different each time"
    }

@router.post("/lesson/{lesson_id}/generate-ai-quiz")
async def generate_ai_quiz_for_lesson(
    lesson_id: int,
    num_questions: int = 5,
    db: Session = Depends(get_db)
):
    """Generate a complete AI quiz for a lesson"""
    
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Generate questions
    ai_quiz = await generate_quiz_questions(
        topic=lesson.title,
        difficulty="Beginner",
        num_questions=num_questions
    )
    
    if "error" in ai_quiz:
        raise HTTPException(status_code=500, detail=ai_quiz["error"])
    
    return {
        "lesson_id": lesson_id,
        "lesson_title": lesson.title,
        "generated_quiz": ai_quiz,
        "message": "AI quiz generated successfully. You can use this to create a new quiz."
    }