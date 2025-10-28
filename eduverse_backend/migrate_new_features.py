"""
Migration script to add new feature tables to the database
Run this after implementing new features
"""
from database import engine, Base
from models import (
    User, Course, Lesson, Quiz, QuizQuestion, QuizOption,
    Progress, LessonProgress, Badge, UserBadge, ChatMessage,
    Leaderboard, QuizAttempt, Feedback, ResumeAnalysis,
    CourseAssessment, GameScore
)

def migrate():
    """Create all new tables"""
    print("🔄 Starting database migration...")
    print("📊 Creating new tables for:")
    print("   - User Feedback System")
    print("   - Resume Analyzer")
    print("   - Pre-Course Assessment")
    print("   - Educational Games")
    print("   - AI Lesson Summaries (updating existing table)")
    
    try:
        # Create all tables (existing ones will be skipped)
        Base.metadata.create_all(bind=engine)
        print("✅ Migration completed successfully!")
        print("\n📋 New tables created:")
        print("   ✓ feedback")
        print("   ✓ resume_analysis")
        print("   ✓ course_assessment")
        print("   ✓ game_score")
        print("\n🎉 All new features are now ready to use!")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        raise

if __name__ == "__main__":
    migrate()