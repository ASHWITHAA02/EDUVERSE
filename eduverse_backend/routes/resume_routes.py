from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.resume_analysis import ResumeAnalysis
from schemas.resume import ResumeAnalysisResponse, ResumeUploadResponse
from routes.auth import get_current_user
from services.resume_analyzer_service import extract_text_from_pdf, analyze_resume
from typing import List
import os
import aiofiles
from datetime import datetime

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload and analyze resume PDF"""
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{current_user.id}_{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Save file
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Extract text from PDF
    try:
        resume_text = extract_text_from_pdf(file_path)
    except Exception as e:
        # Clean up file if extraction fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")
    
    # Analyze resume with AI
    try:
        analysis_result = await analyze_resume(resume_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")
    
    # Save analysis to database
    resume_analysis = ResumeAnalysis(
        user_id=current_user.id,
        filename=file.filename,
        file_path=file_path,
        skills_found=analysis_result.get("skills_found", []),
        skills_missing=analysis_result.get("skills_missing", []),
        job_titles=analysis_result.get("job_titles", []),
        improvement_suggestions=analysis_result.get("improvement_suggestions", ""),
        overall_score=analysis_result.get("overall_score", 0)
    )
    
    db.add(resume_analysis)
    db.commit()
    db.refresh(resume_analysis)
    
    return {
        "message": "Resume analyzed successfully",
        "analysis": resume_analysis
    }

@router.get("/my-analyses", response_model=List[ResumeAnalysisResponse])
def get_my_analyses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all resume analyses for current user"""
    
    analyses = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.user_id == current_user.id
    ).order_by(ResumeAnalysis.created_at.desc()).all()
    
    return analyses

@router.get("/{analysis_id}", response_model=ResumeAnalysisResponse)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific resume analysis"""
    
    analysis = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.id == analysis_id,
        ResumeAnalysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis

@router.delete("/{analysis_id}")
def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete resume analysis"""
    
    analysis = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.id == analysis_id,
        ResumeAnalysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Delete file if it exists
    if os.path.exists(analysis.file_path):
        try:
            os.remove(analysis.file_path)
        except:
            pass
    
    db.delete(analysis)
    db.commit()
    
    return {"message": "Analysis deleted successfully"}