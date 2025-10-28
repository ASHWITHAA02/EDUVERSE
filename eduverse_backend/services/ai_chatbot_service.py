import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None

async def get_ai_response(message: str, context: str = None, lesson_content: str = None) -> str:
    """Get AI response using Google Gemini"""
    
    if not model:
        return "AI chatbot is not configured. Please set GEMINI_API_KEY in your .env file."
    
    try:
        # Build prompt with context and lesson content
        context_info = context if context else 'General question'
        
        if lesson_content:
            prompt = f"""You are an educational AI assistant for EduVerse, a learning management system.

You are helping a student who is currently studying the following lesson content:

{lesson_content[:2000]}  

Context: {context_info}

Student Question: {message}

Provide a helpful, educational response that:
1. Answers the question clearly based on the lesson content
2. Provides examples when relevant
3. References specific concepts from the lesson when applicable
4. Encourages further learning
5. Is friendly and supportive

Response:"""
        else:
            prompt = f"""You are an educational AI assistant for EduVerse, a learning management system.
        
Context: {context_info}

Student Question: {message}

Provide a helpful, educational response that:
1. Answers the question clearly
2. Provides examples when relevant
3. Encourages further learning
4. Is friendly and supportive

Response:"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}. Please try again or rephrase your question."