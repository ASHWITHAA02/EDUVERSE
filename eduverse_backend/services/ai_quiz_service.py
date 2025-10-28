import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None

async def generate_quiz_questions(topic: str, difficulty: str, num_questions: int = 5):
    """Generate quiz questions using AI"""
    
    if not model:
        return {"error": "AI service not configured"}
    
    try:
        prompt = f"""Generate {num_questions} multiple choice quiz questions about {topic} at {difficulty} difficulty level.

Return the response in this exact JSON format:
{{
    "questions": [
        {{
            "question": "Question text here?",
            "options": [
                {{"text": "Option A", "is_correct": false}},
                {{"text": "Option B", "is_correct": true}},
                {{"text": "Option C", "is_correct": false}},
                {{"text": "Option D", "is_correct": false}}
            ],
            "explanation": "Brief explanation of the correct answer"
        }}
    ]
}}

Make sure questions are educational, clear, and appropriate for {difficulty} level learners."""

        response = model.generate_content(prompt)
        
        # Parse JSON response
        try:
            quiz_data = json.loads(response.text)
            return quiz_data
        except json.JSONDecodeError:
            # If response is not valid JSON, return a structured error
            return {
                "questions": [],
                "error": "Failed to parse AI response"
            }
            
    except Exception as e:
        return {"error": str(e)}

async def generate_quiz_feedback(score: float, total_questions: int, correct_answers: int, topic: str) -> str:
    """Generate personalized AI feedback based on quiz performance"""
    
    if not model:
        return "Great effort! Keep practicing to improve your skills."
    
    try:
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        prompt = f"""You are an encouraging educational AI tutor. A student just completed a quiz with the following results:

Topic: {topic}
Score: {correct_answers}/{total_questions} ({percentage:.1f}%)

Provide personalized, encouraging feedback that:
1. Acknowledges their performance (excellent/good/needs improvement)
2. Highlights what they did well
3. Suggests specific areas to focus on for improvement
4. Provides 2-3 actionable study tips
5. Ends with motivation to keep learning

Keep the feedback positive, constructive, and under 150 words.

Feedback:"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Great job completing the quiz! Keep practicing to master {topic}."

async def generate_adaptive_recommendations(course_title: str, assessment_score: float, weak_areas: list) -> dict:
    """Generate AI-powered learning path recommendations based on assessment"""
    
    if not model:
        return {
            "recommended_lessons": [],
            "skill_gaps": [],
            "feedback": "Complete the course lessons to improve your skills."
        }
    
    try:
        prompt = f"""You are an adaptive learning AI. A student took a pre-course assessment for "{course_title}" and scored {assessment_score}%.

Weak areas identified: {', '.join(weak_areas) if weak_areas else 'General understanding'}

Based on this score, provide recommendations in JSON format:
{{
    "skill_gaps": ["list of 3-5 specific skills/concepts they need to work on"],
    "study_approach": "recommended learning strategy (focus on basics/intermediate/advanced)",
    "feedback": "personalized 2-3 sentence feedback on their readiness and what to focus on",
    "must_retake": {str(assessment_score < 50).lower()}
}}

Provide ONLY the JSON response."""
        
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Extract JSON
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        try:
            recommendations = json.loads(result_text)
        except json.JSONDecodeError:
            recommendations = {
                "skill_gaps": weak_areas if weak_areas else ["Basic concepts"],
                "study_approach": "Focus on fundamentals" if assessment_score < 50 else "Build on existing knowledge",
                "feedback": f"You scored {assessment_score}%. " + ("Focus on mastering the basics before moving forward." if assessment_score < 50 else "Good foundation! Focus on strengthening weak areas."),
                "must_retake": assessment_score < 50
            }
        
        return recommendations
        
    except Exception as e:
        return {
            "skill_gaps": weak_areas if weak_areas else [],
            "study_approach": "Complete all lessons",
            "feedback": f"Assessment complete. Focus on learning the course material.",
            "must_retake": assessment_score < 50
        }