"""
Schemas for Compliance Training module.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


# ─── Compliance Item (admin creates) ─────────────────
class ComplianceItemCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None = None
    compliance_type: str = Field(..., pattern="^(declaration|video|document|acknowledgement)$")
    content_url: str | None = Field(None, max_length=512)
    order: int = 0
    is_required: bool = True


class ComplianceItemUpdate(BaseModel):
    title: str | None = Field(None, max_length=255)
    description: str | None = None
    compliance_type: str | None = Field(None, pattern="^(declaration|video|document|acknowledgement)$")
    content_url: str | None = None
    order: int | None = None
    is_required: bool | None = None
    is_active: bool | None = None


class ComplianceItemResponse(BaseModel):
    id: uuid.UUID
    university_id: uuid.UUID
    title: str
    description: str | None
    compliance_type: str
    content_url: str | None
    order: int
    is_required: bool
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ComplianceItemListResponse(BaseModel):
    items: list[ComplianceItemResponse]
    total: int


# ─── Student Compliance Status ───────────────────────
class StudentComplianceSubmit(BaseModel):
    compliance_item_id: uuid.UUID


class StudentComplianceResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    compliance_item_id: uuid.UUID
    university_id: uuid.UUID
    is_completed: bool
    completed_at: datetime | None
    # Embedded item info
    item_title: str | None = None
    item_type: str | None = None
    item_description: str | None = None
    content_url: str | None = None
    is_required: bool = True

    model_config = {"from_attributes": True}


class StudentComplianceListResponse(BaseModel):
    items: list[StudentComplianceResponse]
    total: int
    completed: int
    required_total: int
    required_completed: int
    all_required_done: bool
