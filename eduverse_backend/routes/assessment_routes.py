from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.course import Course
from models.lesson import Lesson
from models.course_assessment import CourseAssessment
from schemas.assessment import AssessmentSubmit, AssessmentResponse
from routes.auth import get_current_user
from services.ai_quiz_service import generate_adaptive_recommendations, generate_quiz_questions
from typing import List

router = APIRouter()

@router.get("/course/{course_id}/questions")
async def get_assessment_questions(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate assessment questions for a course"""
    
    # Get course
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Generate AI questions based on course
    questions_data = await generate_quiz_questions(
        topic=course.title,
        difficulty=course.difficulty or "Beginner",
        num_questions=10
    )
    
    if "error" in questions_data:
        # Return fallback questions if AI fails
        fallback_questions = [
            {
                "question": f"What is the main purpose of {course.title}?",
                "options": {
                    "A": "To learn programming basics",
                    "B": "To understand core concepts",
                    "C": "To build projects",
                    "D": "All of the above"
                }
            },
            {
                "question": f"Which of the following is a key concept in {course.title}?",
                "options": {
                    "A": "Fundamentals",
                    "B": "Best practices",
                    "C": "Advanced techniques",
                    "D": "All of the above"
                }
            },
            {
                "question": f"How would you apply {course.title} in real-world scenarios?",
                "options": {
                    "A": "Building applications",
                    "B": "Solving problems",
                    "C": "Creating solutions",
                    "D": "All of the above"
                }
            },
            {
                "question": f"What are the fundamental principles of {course.title}?",
                "options": {
                    "A": "Core concepts",
                    "B": "Best practices",
                    "C": "Design patterns",
                    "D": "All of the above"
                }
            },
            {
                "question": f"Which tool is commonly used in {course.title}?",
                "options": {
                    "A": "IDE/Editor",
                    "B": "Framework",
                    "C": "Library",
                    "D": "All of the above"
                }
            },
            {
                "question": f"What is the best practice when working with {course.title}?",
                "options": {
                    "A": "Write clean code",
                    "B": "Follow standards",
                    "C": "Test thoroughly",
                    "D": "All of the above"
                }
            },
            {
                "question": f"How does {course.title} improve development?",
                "options": {
                    "A": "Increases efficiency",
                    "B": "Reduces errors",
                    "C": "Improves quality",
                    "D": "All of the above"
                }
            },
            {
                "question": f"What is the most important skill in {course.title}?",
                "options": {
                    "A": "Problem solving",
                    "B": "Critical thinking",
                    "C": "Continuous learning",
                    "D": "All of the above"
                }
            },
            {
                "question": f"Which approach is recommended for learning {course.title}?",
                "options": {
                    "A": "Hands-on practice",
                    "B": "Reading documentation",
                    "C": "Building projects",
                    "D": "All of the above"
                }
            },
            {
                "question": f"What are the common challenges in {course.title}?",
                "options": {
                    "A": "Understanding concepts",
                    "B": "Applying knowledge",
                    "C": "Debugging issues",
                    "D": "All of the above"
                }
            }
        ]
        return {
            "course_id": course_id,
            "course_title": course.title,
            "questions": fallback_questions,
            "correct_answers": {i: "D" for i in range(10)}  # All answers are D for fallback
        }
    
    # Extract questions with options for frontend
    formatted_questions = []
    correct_answers = {}
    
    for idx, q in enumerate(questions_data.get("questions", [])):
        question_text = q.get("question", "")
        options = q.get("options", [])
        
        # Format question with options
        if options:
            # Create formatted question with options
            formatted_q = {
                "question": question_text,
                "options": {}
            }
            for opt_idx, option in enumerate(options):
                option_letter = chr(65 + opt_idx)  # A, B, C, D
                formatted_q["options"][option_letter] = option.get("text", f"Option {option_letter}")
                if option.get("is_correct", False):
                    correct_answers[idx] = option_letter
            formatted_questions.append(formatted_q)
        else:
            # Fallback: just question text with generic options
            formatted_questions.append({
                "question": question_text,
                "options": {
                    "A": "Option A",
                    "B": "Option B", 
                    "C": "Option C",
                    "D": "Option D"
                }
            })
    
    return {
        "course_id": course_id,
        "course_title": course.title,
        "questions": formatted_questions,
        "correct_answers": correct_answers  # Store for validation
    }

@router.post("/submit")
async def submit_assessment(
    assessment_data: AssessmentSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit course assessment and get AI recommendations"""
    
    # Get course
    course = db.query(Course).filter(Course.id == assessment_data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Calculate score (simplified - in real scenario, validate against correct answers)
    # For now, we'll use the provided answers to calculate a score
    total_questions = len(assessment_data.answers)
    if total_questions == 0:
        raise HTTPException(status_code=400, detail="No answers provided")
    
    # Simulate scoring (in production, you'd validate against correct answers)
    # For demo, we'll use a random-ish score based on answer count
    correct_count = sum(1 for ans in assessment_data.answers.values() if ans)
    score_percentage = (correct_count / total_questions) * 100
    
    # Get course lessons
    lessons = db.query(Lesson).filter(Lesson.course_id == course.id).order_by(Lesson.order).all()
    
    # Identify weak areas (simplified)
    weak_areas = []
    if score_percentage < 50:
        weak_areas = ["Basic concepts", "Fundamentals", "Core principles"]
    elif score_percentage < 70:
        weak_areas = ["Intermediate topics", "Practical application"]
    else:
        weak_areas = ["Advanced concepts"]
    
    # Get AI recommendations
    ai_recommendations = await generate_adaptive_recommendations(
        course_title=course.title,
        assessment_score=score_percentage,
        weak_areas=weak_areas
    )
    
    # Determine recommended lessons based on score
    recommended_lesson_ids = []
    if score_percentage < 50:
        # Recommend all lessons, starting from basics
        recommended_lesson_ids = [lesson.id for lesson in lessons]
    elif score_percentage < 80:
        # Recommend middle to advanced lessons
        mid_point = len(lessons) // 2
        recommended_lesson_ids = [lesson.id for lesson in lessons[mid_point:]]
    else:
        # Recommend advanced lessons only
        advanced_point = int(len(lessons) * 0.7)
        recommended_lesson_ids = [lesson.id for lesson in lessons[advanced_point:]]
    
    # Create assessment record
    assessment = CourseAssessment(
        course_id=course.id,
        user_id=current_user.id,
        score=score_percentage,
        recommended_lessons=recommended_lesson_ids,
        skill_gaps=ai_recommendations.get("skill_gaps", weak_areas),
        ai_feedback=ai_recommendations.get("feedback", "Complete the recommended lessons to improve."),
        can_skip_basics=1 if score_percentage >= 80 else 0,
        must_retake=1 if score_percentage < 50 else 0
    )
    
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    
    # Award XP for taking assessment
    current_user.total_xp += 50
    current_user.level = (current_user.total_xp // 1000) + 1
    db.commit()
    
    # Format response for frontend
    recommendations = [
        ai_recommendations.get("feedback", "Complete the recommended lessons to improve.")
    ]
    
    if score_percentage >= 80:
        recommendations.append("You have a strong foundation! You can skip basic lessons.")
        recommendations.append("Focus on advanced topics to maximize your learning.")
    elif score_percentage >= 50:
        recommendations.append("Good start! Follow the recommended learning path.")
        recommendations.append("Review the focus areas to strengthen your understanding.")
    else:
        recommendations.append("We recommend reviewing the fundamentals before proceeding.")
        recommendations.append("Take your time with each lesson and practice regularly.")
    
    return {
        "score": int(correct_count),
        "total_questions": total_questions,
        "score_percentage": round(score_percentage, 1),
        "xp_earned": 50,
        "recommendations": recommendations,
        "focus_areas": ai_recommendations.get("skill_gaps", weak_areas),
        "can_skip_basics": score_percentage >= 80,
        "must_retake": score_percentage < 50
    }

@router.get("/course/{course_id}/my-assessment", response_model=AssessmentResponse)
def get_my_assessment(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's latest assessment for a course"""
    
    assessment = db.query(CourseAssessment).filter(
        CourseAssessment.course_id == course_id,
        CourseAssessment.user_id == current_user.id
    ).order_by(CourseAssessment.created_at.desc()).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="No assessment found for this course")
    
    return assessment

@router.get("/my-assessments", response_model=List[AssessmentResponse])
def get_all_my_assessments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all assessments for current user"""
    
    assessments = db.query(CourseAssessment).filter(
        CourseAssessment.user_id == current_user.id
    ).order_by(CourseAssessment.created_at.desc()).all()
    
    return assessments