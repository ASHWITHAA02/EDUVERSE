"""
Verification script to check database and AI setup
"""
from sqlalchemy.orm import Session
from database import SessionLocal
from models.course import Course
from models.lesson import Lesson
from models.quiz import Quiz
from models.feedback import Feedback
from models.resume_analysis import ResumeAnalysis
from models.course_assessment import CourseAssessment
from models.game_score import GameScore
import os
from dotenv import load_dotenv

load_dotenv()

def verify_database():
    """Check if database has data"""
    db = SessionLocal()
    
    print("=" * 60)
    print("DATABASE VERIFICATION")
    print("=" * 60)
    
    # Check courses
    course_count = db.query(Course).count()
    print(f"✓ Courses: {course_count}")
    
    # Check lessons
    lesson_count = db.query(Lesson).count()
    print(f"✓ Lessons: {lesson_count}")
    
    # Check quizzes
    quiz_count = db.query(Quiz).count()
    print(f"✓ Quizzes: {quiz_count}")
    
    # Check new tables
    feedback_count = db.query(Feedback).count()
    print(f"✓ Feedback entries: {feedback_count}")
    
    resume_count = db.query(ResumeAnalysis).count()
    print(f"✓ Resume analyses: {resume_count}")
    
    assessment_count = db.query(CourseAssessment).count()
    print(f"✓ Course assessments: {assessment_count}")
    
    game_score_count = db.query(GameScore).count()
    print(f"✓ Game scores: {game_score_count}")
    
    db.close()
    
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    if course_count == 0:
        print("⚠️  No courses found! Run: python seed_data.py")
    else:
        print("✅ Database has course data")
    
    return course_count > 0

def verify_ai_setup():
    """Check if AI is configured"""
    print("\n" + "=" * 60)
    print("AI CONFIGURATION VERIFICATION")
    print("=" * 60)
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if gemini_key:
        print(f"✅ GEMINI_API_KEY is set (length: {len(gemini_key)})")
        
        # Test AI import
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            print("✅ Gemini AI model initialized successfully")
            print("✅ Using model: gemini-1.5-flash")
            return True
        except Exception as e:
            print(f"❌ Error initializing AI: {str(e)}")
            return False
    else:
        print("❌ GEMINI_API_KEY not found in .env file")
        print("⚠️  AI features will not work without API key")
        return False

def verify_file_storage():
    """Check if upload directories exist"""
    print("\n" + "=" * 60)
    print("FILE STORAGE VERIFICATION")
    print("=" * 60)
    
    upload_dir = "uploads/resumes"
    if os.path.exists(upload_dir):
        print(f"✅ Upload directory exists: {upload_dir}")
    else:
        print(f"⚠️  Upload directory missing: {upload_dir}")
        print("   Creating directory...")
        os.makedirs(upload_dir, exist_ok=True)
        print(f"✅ Created: {upload_dir}")

if __name__ == "__main__":
    print("\n🔍 EduVerse Backend Verification\n")
    
    has_data = verify_database()
    has_ai = verify_ai_setup()
    verify_file_storage()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if has_data and has_ai:
        print("✅ All systems ready!")
        print("\nYou can start the server with:")
        print("   uvicorn main:app --reload")
    elif has_data and not has_ai:
        print("⚠️  Database ready, but AI not configured")
        print("\nTo enable AI features:")
        print("   1. Get API key from: https://makersuite.google.com/app/apikey")
        print("   2. Add to .env file: GEMINI_API_KEY=your_key_here")
    elif not has_data:
        print("⚠️  Database is empty")
        print("\nTo seed the database:")
        print("   python seed_data.py")
    
    print("\n" + "=" * 60)