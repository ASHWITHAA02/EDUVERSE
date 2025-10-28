from pydantic import BaseModel, computed_field
from datetime import datetime
from typing import List, Optional

class ResumeAnalysisResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    skills_found: List[str]
    skills_missing: List[str]
    job_titles: List[str]
    improvement_suggestions: str
    overall_score: int
    created_at: datetime
    
    @computed_field
    @property
    def improvements(self) -> List[str]:
        """Convert improvement_suggestions string to array for frontend"""
        if not self.improvement_suggestions:
            return []
        # Split by periods, newlines, or numbered lists
        text = self.improvement_suggestions.replace('\n', '. ')
        suggestions = [s.strip() for s in text.split('. ') if s.strip()]
        # Limit to 5 items for better UI display
        return suggestions[:5] if len(suggestions) > 5 else suggestions
    
    @computed_field
    @property
    def analyzed_at(self) -> datetime:
        """Alias for created_at for frontend compatibility"""
        return self.created_at
    
    class Config:
        from_attributes = True

class ResumeUploadResponse(BaseModel):
    message: str
    analysis: ResumeAnalysisResponse