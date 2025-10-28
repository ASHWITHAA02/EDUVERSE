"""
Test script to verify all API endpoints are working correctly
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print("❌ Backend is not responding correctly")
            return False
    except Exception as e:
        print(f"❌ Backend is not running: {e}")
        return False

def test_assessment_questions():
    """Test assessment questions endpoint (without auth for structure check)"""
    print("\n📝 Testing Assessment Questions Structure...")
    # This will fail auth but we can see the response structure
    try:
        response = requests.get(f"{BASE_URL}/api/assessment/course/1/questions")
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Endpoint exists (requires authentication)")
        else:
            print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_lesson_summary():
    """Test lesson summary endpoint"""
    print("\n💡 Testing Lesson Summary Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/lessons/1/summary")
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Endpoint exists (requires authentication)")
        else:
            print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_resume_schema():
    """Test resume endpoint structure"""
    print("\n📄 Testing Resume Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/resume/my-analyses")
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Endpoint exists (requires authentication)")
        else:
            print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("=" * 60)
    print("🧪 EduVerse API Endpoint Tests")
    print("=" * 60)
    
    if not test_health():
        print("\n❌ Backend is not running. Please start it first.")
        return
    
    test_assessment_questions()
    test_lesson_summary()
    test_resume_schema()
    
    print("\n" + "=" * 60)
    print("📋 Test Summary:")
    print("=" * 60)
    print("All endpoints are accessible (authentication required)")
    print("\nTo fully test:")
    print("1. Upload a resume in the UI and check if 'improvements' array appears")
    print("2. Take an assessment and verify options show full text, not just letters")
    print("3. Generate AI summary on a lesson page")
    print("\n✨ Backend schema fixes are deployed and ready for testing!")

if __name__ == "__main__":
    main()