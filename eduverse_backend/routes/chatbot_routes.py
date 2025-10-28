from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.chat_message import ChatMessage
from models.user import User
from models.lesson import Lesson
from schemas.chat import ChatRequest, ChatResponse
from routes.auth import get_current_user
from services.ai_chatbot_service import get_ai_response
from typing import List

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Fetch lesson content if lesson_id is provided
    lesson_content = None
    if request.lesson_id:
        lesson = db.query(Lesson).filter(Lesson.id == request.lesson_id).first()
        if lesson:
            lesson_content = lesson.content
    
    # Get AI response with lesson content
    ai_response = await get_ai_response(request.message, request.context, lesson_content)
    
    # Save chat message
    chat_message = ChatMessage(
        user_id=current_user.id,
        message=request.message,
        response=ai_response,
        context=request.context
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    
    return chat_message

@router.get("/history", response_model=List[ChatResponse])
def get_chat_history(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).order_by(ChatMessage.created_at.desc()).limit(limit).all()
    
    return messages

@router.delete("/history")
def clear_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.query(ChatMessage).filter(ChatMessage.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Chat history cleared successfully"}