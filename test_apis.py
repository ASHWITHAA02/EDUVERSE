"""
Test script to verify all API endpoints are working
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_games_list():
    """Test games list endpoint"""
    print("\n=== Testing Games List ===")
    try:
        response = requests.get(f"{BASE_URL}/games/list")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_assessment_questions(course_id=1, token=None):
    """Test assessment questions endpoint"""
    print(f"\n=== Testing Assessment Questions for Course {course_id} ===")
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(
            f"{BASE_URL}/assessment/course/{course_id}/questions",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Course: {data.get('course_title')}")
            print(f"Number of questions: {len(data.get('questions', []))}")
            print(f"First question: {data.get('questions', [''])[0]}")
        else:
            print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_games_stats(token=None):
    """Test games stats endpoint"""
    print("\n=== Testing Games Stats ===")
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(f"{BASE_URL}/games/stats", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def login(username="testuser", password="testpass123"):
    """Login and get token"""
    print("\n=== Logging in ===")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"Login successful! Token: {token[:20]}...")
            return token
        else:
            print(f"Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("EduVerse API Testing")
    print("=" * 60)
    
    # Test public endpoints
    test_games_list()
    
    # Try to login
    token = login()
    
    # Test protected endpoints
    if token:
        test_games_stats(token)
        test_assessment_questions(1, token)
    else:
        print("\n⚠️  Skipping protected endpoint tests (no token)")
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)