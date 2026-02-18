"""
Document Service

Handles document upload, listing, and admin review.
Supports status workflow: pending → under_review → approved / rejected.
"""

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.document import Document, DocumentStatus
from app.models.user import User
from app.schemas.document import (
    DocumentListResponse,
    DocumentResponse,
    DocumentReviewRequest,
    DocumentUploadResponse,
)
from app.services.storage_service import StorageService


def _doc_to_response(doc: Document, user: User | None = None) -> DocumentResponse:
    """Convert a Document ORM object to DocumentResponse with optional student info."""
    data = {
        "id": doc.id,
        "user_id": doc.user_id,
        "document_type": doc.document_type,
        "file_name": doc.file_name,
        "file_url": doc.file_url,
        "file_size": doc.file_size,
        "mime_type": doc.mime_type,
        "status": doc.status,
        "rejection_reason": doc.rejection_reason,
        "reviewed_by": doc.reviewed_by,
        "reviewed_at": doc.reviewed_at,
        "created_at": doc.created_at,
    }
    if user:
        data["student_name"] = user.full_name
        data["student_email"] = user.email
    elif hasattr(doc, "user") and doc.user:
        data["student_name"] = doc.user.full_name
        data["student_email"] = doc.user.email
    return DocumentResponse(**data)


class DocumentService:
    """Document management business logic."""

    @staticmethod
    async def upload(
        db: AsyncSession, user: User, document_type: str, file: UploadFile
    ) -> DocumentUploadResponse:
        """Upload document to Supabase Storage and create DB record."""
        # Upload to storage
        path = f"{user.university_id}/{user.id}/documents"
        file_url, file_size = await StorageService.upload_file(file, path)

        # Create DB record
        doc = Document(
            id=uuid.uuid4(),
            user_id=user.id,
            university_id=user.university_id,
            document_type=document_type,
            file_name=file.filename or "unknown",
            file_url=file_url,
            file_size=file_size,
            mime_type=file.content_type or "application/octet-stream",
            status=DocumentStatus.PENDING,
        )
        db.add(doc)
        await db.flush()

        return DocumentUploadResponse(
            id=doc.id,
            document_type=doc.document_type,
            file_name=doc.file_name,
            file_url=doc.file_url,
            status=doc.status,
            created_at=doc.created_at,
        )

    @staticmethod
    async def list_by_user(db: AsyncSession, user: User) -> DocumentListResponse:
        """List all documents belonging to a user."""
        result = await db.execute(
            select(Document)
            .where(Document.user_id == user.id)
            .order_by(Document.created_at.desc())
        )
        docs = result.scalars().all()
        return DocumentListResponse(
            documents=[_doc_to_response(d) for d in docs],
            total=len(docs),
        )

    @staticmethod
    async def get_by_id(
        db: AsyncSession, user: User, document_id: uuid.UUID
    ) -> DocumentResponse:
        """Get a single document by ID."""
        result = await db.execute(
            select(Document).where(Document.id == document_id)
        )
        doc = result.scalar_one_or_none()
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found.",
            )
        # Students can only view their own
        if doc.user_id != user.id and user.role.value == "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )
        return _doc_to_response(doc)

    @staticmethod
    async def review(
        db: AsyncSession,
        admin: User,
        document_id: uuid.UUID,
        data: DocumentReviewRequest,
    ) -> DocumentResponse:
        """Admin: change document status (under_review / approve / reject)."""
        result = await db.execute(
            select(Document).options(selectinload(Document.user)).where(Document.id == document_id)
        )
        doc = result.scalar_one_or_none()
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found.",
            )

        # Workflow enforcement
        valid_transitions = {
            DocumentStatus.PENDING: {DocumentStatus.UNDER_REVIEW, DocumentStatus.APPROVED, DocumentStatus.REJECTED},
            DocumentStatus.UNDER_REVIEW: {DocumentStatus.APPROVED, DocumentStatus.REJECTED},
            DocumentStatus.APPROVED: set(),     # terminal
            DocumentStatus.REJECTED: {DocumentStatus.PENDING},  # allow re-open
        }
        allowed = valid_transitions.get(doc.status, set())
        if data.status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition from '{doc.status.value}' to '{data.status.value}'.",
            )

        doc.status = data.status
        doc.reviewed_by = admin.id
        doc.reviewed_at = datetime.now(timezone.utc)

        if data.status == DocumentStatus.REJECTED:
            doc.rejection_reason = data.rejection_reason
        else:
            doc.rejection_reason = None  # clear on approve/under_review

        await db.flush()
        return _doc_to_response(doc)
