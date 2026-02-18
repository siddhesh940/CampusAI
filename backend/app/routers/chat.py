"""
AI Chat Router

Endpoints: send message, get history, list sessions.
"""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.chat import ChatMessageRequest, ChatSessionListResponse, ChatSessionResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post(
    "/message",
    response_model=ChatSessionResponse,
    summary="Send message to AI assistant",
)
async def send_message(
    data: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Send a message to the AI assistant and get a response."""
    return await ChatService.send_message(db, current_user, data)


@router.get(
    "/history",
    response_model=ChatSessionListResponse,
    summary="Get chat history",
)
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all chat sessions for the authenticated user."""
    return await ChatService.get_history(db, current_user)


@router.get(
    "/session/{session_id}",
    response_model=ChatSessionResponse,
    summary="Get chat session",
)
async def get_session(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific chat session with all messages."""
    return await ChatService.get_session(db, current_user, session_id)
