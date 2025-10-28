"""List available Gemini models"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load from backend directory
load_dotenv('eduverse_backend/.env')

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    
    print("=" * 60)
    print("📋 Available Gemini Models")
    print("=" * 60)
    
    try:
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"\n✅ {model.name}")
                print(f"   Display Name: {model.display_name}")
                print(f"   Description: {model.description[:100]}...")
    except Exception as e:
        print(f"❌ Error listing models: {e}")
else:
    print("❌ GEMINI_API_KEY not found in .env file")