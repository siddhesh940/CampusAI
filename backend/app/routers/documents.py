"""
Documents Router

Endpoints: upload, list, get details, admin review.
"""

import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.document import (
    DocumentListResponse,
    DocumentResponse,
    DocumentReviewRequest,
    DocumentUploadResponse,
)
from app.services.document_service import DocumentService

router = APIRouter()


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    summary="Upload a document",
)
async def upload_document(
    document_type: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload a document to Supabase Storage and create a DB record."""
    return await DocumentService.upload(db, current_user, document_type, file)


@router.get(
    "",
    response_model=DocumentListResponse,
    summary="List user documents",
)
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all documents for the authenticated user."""
    return await DocumentService.list_by_user(db, current_user)


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
    summary="Get document details",
)
async def get_document(
    document_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific document's details."""
    return await DocumentService.get_by_id(db, current_user, document_id)


@router.put(
    "/{document_id}/review",
    response_model=DocumentResponse,
    summary="Review a document (Admin)",
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
async def review_document(
    document_id: uuid.UUID,
    data: DocumentReviewRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Approve or reject a student's document submission."""
    return await DocumentService.review(db, current_user, document_id, data)
