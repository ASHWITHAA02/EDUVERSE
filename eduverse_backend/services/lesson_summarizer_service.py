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

async def generate_lesson_summary(lesson_title: str, lesson_content: str) -> str:
    """Generate AI summary for a lesson"""
    
    if not model:
        return "AI summarization is not available. Please configure GEMINI_API_KEY."
    
    try:
        prompt = f"""You are an educational AI assistant. Create a concise, informative summary of the following lesson.

Lesson Title: {lesson_title}

Lesson Content:
{lesson_content[:3000]}

Please provide a summary that:
1. Highlights the key concepts and learning objectives
2. Is 3-5 paragraphs long
3. Uses clear, educational language
4. Includes the main takeaways
5. Is engaging and easy to understand

Summary:"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error generating summary: {str(e)}"