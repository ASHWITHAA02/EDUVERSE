"""Direct test of AI services to verify gemini-pro model is working"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'eduverse_backend'))

from services.lesson_summarizer_service import generate_lesson_summary
from services.ai_chatbot_service import get_ai_response

async def test_ai_services():
    print("=" * 60)
    print("🧪 Testing AI Services with gemini-pro model")
    print("=" * 60)
    
    # Test 1: Lesson Summarizer
    print("\n📚 Test 1: Lesson Summarizer")
    print("-" * 60)
    summary = await generate_lesson_summary(
        "Introduction to Python",
        "Python is a high-level programming language. It is easy to learn and widely used."
    )
    print(f"Summary: {summary[:200]}...")
    if "Error" in summary or "404" in summary:
        print("❌ FAILED: Lesson summarizer still has errors")
    else:
        print("✅ PASSED: Lesson summarizer working!")
    
    # Test 2: Chatbot
    print("\n💬 Test 2: AI Chatbot")
    print("-" * 60)
    response = await get_ai_response("What is Python?")
    print(f"Response: {response[:200]}...")
    if "Error" in response or "404" in response or "error" in response:
        print("❌ FAILED: Chatbot still has errors")
    else:
        print("✅ PASSED: Chatbot working!")
    
    print("\n" + "=" * 60)
    print("✨ AI Service Tests Complete")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_ai_services())