from fastapi import APIRouter, HTTPException
from datetime import datetime

from backend.schemas import ChatMessage, ChatResponse
from backend.services.ai_service import ai_service

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Handle chat messages with AI assistant"""
    try:
        response_text = await ai_service.get_response(message.message)
        
        return ChatResponse(
            response=response_text,
            timestamp=datetime.now()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")
