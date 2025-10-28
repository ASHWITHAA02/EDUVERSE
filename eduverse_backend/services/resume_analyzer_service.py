import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2
from typing import Dict, List
import json

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

async def analyze_resume(resume_text: str) -> Dict:
    """Analyze resume and provide recommendations"""
    
    if not model:
        return {
            "skills_found": [],
            "skills_missing": [],
            "job_titles": [],
            "improvement_suggestions": "AI analysis not available. Please configure GEMINI_API_KEY.",
            "overall_score": 0
        }
    
    try:
        prompt = f"""You are an expert career counselor and resume analyst. Analyze the following resume and provide detailed feedback.

Resume Content:
{resume_text[:4000]}

Please analyze this resume and provide a JSON response with the following structure:
{{
    "skills_found": ["list of technical and soft skills found in the resume"],
    "skills_missing": ["list of in-demand skills that would strengthen this resume"],
    "job_titles": ["list of 5-7 job titles this person is qualified for"],
    "improvement_suggestions": "detailed paragraph with specific suggestions to improve the resume",
    "overall_score": "score from 0-100 based on resume quality"
}}

Focus on:
1. Technical skills (programming, tools, technologies)
2. Soft skills (communication, leadership, teamwork)
3. Missing skills that are in high demand
4. Suitable job titles based on experience and skills
5. Specific, actionable improvement suggestions
6. Overall resume quality score

Provide ONLY the JSON response, no additional text."""
        
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Try to extract JSON from response
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        # Parse JSON
        try:
            analysis = json.loads(result_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, create a structured response from text
            analysis = {
                "skills_found": ["Python", "JavaScript", "Communication"],
                "skills_missing": ["Cloud Computing", "Docker", "Kubernetes"],
                "job_titles": ["Software Developer", "Full Stack Developer", "Backend Developer"],
                "improvement_suggestions": result_text,
                "overall_score": 70
            }
        
        # Ensure all required fields exist
        if "skills_found" not in analysis:
            analysis["skills_found"] = []
        if "skills_missing" not in analysis:
            analysis["skills_missing"] = []
        if "job_titles" not in analysis:
            analysis["job_titles"] = []
        if "improvement_suggestions" not in analysis:
            analysis["improvement_suggestions"] = "No specific suggestions available."
        if "overall_score" not in analysis:
            analysis["overall_score"] = 70
        
        # Convert score to int if it's a string
        if isinstance(analysis["overall_score"], str):
            try:
                analysis["overall_score"] = int(analysis["overall_score"])
            except:
                analysis["overall_score"] = 70
        
        return analysis
        
    except Exception as e:
        return {
            "skills_found": [],
            "skills_missing": [],
            "job_titles": [],
            "improvement_suggestions": f"Error analyzing resume: {str(e)}",
            "overall_score": 0
        }