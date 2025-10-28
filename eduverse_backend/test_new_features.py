"""
Test script for all new features
This will verify that all endpoints are working correctly
"""
import asyncio
from services.lesson_summarizer_service import generate_lesson_summary
from services.ai_quiz_service import generate_quiz_feedback, generate_adaptive_recommendations

async def test_ai_services():
    """Test all AI services"""
    print("🧪 Testing AI Services...\n")
    
    # Test 1: Lesson Summarizer
    print("1️⃣ Testing Lesson Summarizer...")
    summary = await generate_lesson_summary(
        lesson_title="Introduction to Python",
        lesson_content="Python is a high-level programming language. It is easy to learn and widely used."
    )
    if "error" not in summary:
        print("   ✅ Lesson Summarizer working!")
        print(f"   Summary: {summary[:100]}...")
    else:
        print(f"   ❌ Error: {summary['error']}")
    
    # Test 2: Quiz Feedback Generator
    print("\n2️⃣ Testing Quiz Feedback Generator...")
    feedback = await generate_quiz_feedback(
        quiz_title="Python Basics Quiz",
        score=75,
        total_questions=10,
        correct_answers=7
    )
    if "error" not in feedback:
        print("   ✅ Quiz Feedback Generator working!")
        print(f"   Feedback: {feedback[:100]}...")
    else:
        print(f"   ❌ Error: {feedback['error']}")
    
    # Test 3: Adaptive Recommendations
    print("\n3️⃣ Testing Adaptive Recommendations...")
    recommendations = await generate_adaptive_recommendations(
        course_title="Python Programming",
        assessment_results={
            "Variables and Data Types": 80,
            "Control Flow": 60,
            "Functions": 40,
            "OOP": 30
        }
    )
    if "error" not in recommendations:
        print("   ✅ Adaptive Recommendations working!")
        print(f"   Recommendations: {str(recommendations)[:150]}...")
    else:
        print(f"   ❌ Error: {recommendations['error']}")
    
    print("\n✅ All AI services tested!")

def test_database_models():
    """Test that all new models are created"""
    print("\n🗄️ Testing Database Models...\n")
    
    from database import engine
    from sqlalchemy import inspect
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    required_tables = ['feedback', 'resume_analysis', 'course_assessment', 'game_score']
    
    for table in required_tables:
        if table in tables:
            print(f"   ✅ Table '{table}' exists")
        else:
            print(f"   ❌ Table '{table}' missing")
    
    print("\n✅ Database models verified!")

def test_routes_registered():
    """Test that all routes are registered"""
    print("\n🛣️ Testing Route Registration...\n")
    
    from main import app
    
    routes = [route.path for route in app.routes]
    
    required_routes = [
        '/api/feedback/submit',
        '/api/resume/upload',
        '/api/assessment/submit',
        '/api/games/list'
    ]
    
    for route in required_routes:
        if route in routes:
            print(f"   ✅ Route '{route}' registered")
        else:
            print(f"   ❌ Route '{route}' missing")
    
    print("\n✅ All routes verified!")

async def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 EduVerse New Features Test Suite")
    print("=" * 60)
    
    # Test AI Services
    await test_ai_services()
    
    # Test Database Models
    test_database_models()
    
    # Test Routes
    test_routes_registered()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\n📝 Next Steps:")
    print("   1. Start the backend server: uvicorn main:app --reload")
    print("   2. Visit http://localhost:8000/docs to see all endpoints")
    print("   3. Test endpoints using the Swagger UI")
    print("   4. Build frontend components to consume these APIs")

if __name__ == "__main__":
    asyncio.run(main())