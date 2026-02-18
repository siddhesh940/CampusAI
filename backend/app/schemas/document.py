"""
Document upload and review schemas.
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator

from app.models.document import DocumentStatus


class DocumentUploadResponse(BaseModel):
    id: uuid.UUID
    document_type: str
    file_name: str
    file_url: str
    status: DocumentStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class DocumentReviewRequest(BaseModel):
    status: DocumentStatus = Field(..., description="under_review, approved, or rejected")
    rejection_reason: str | None = None

    @model_validator(mode="after")
    def validate_rejection(self):
        if self.status == DocumentStatus.REJECTED and not self.rejection_reason:
            raise ValueError("rejection_reason is required when rejecting a document")
        if self.status == DocumentStatus.PENDING:
            raise ValueError("Cannot set status back to pending")
        return self


class DocumentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    document_type: str
    file_name: str
    file_url: str
    file_size: int
    mime_type: str
    status: DocumentStatus
    rejection_reason: str | None
    reviewed_by: uuid.UUID | None
    reviewed_at: datetime | None
    created_at: datetime
    # Student info (populated for admin views)
    student_name: str | None = None
    student_email: str | None = None

    model_config = {"from_attributes": True}


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int
