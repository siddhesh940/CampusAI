"""
University schemas.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class UniversityCreate(BaseModel):
    name: str = Field(..., max_length=255)
    slug: str = Field(..., max_length=100)
    domain: str | None = None
    logo_url: str | None = None
    primary_color: str = "#6366F1"
    secondary_color: str = "#8B5CF6"
    description: str | None = None
    subscription_plan: str = "free"
    max_students: int = 100


class UniversityUpdate(BaseModel):
    name: str | None = None
    domain: str | None = None
    logo_url: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None
    description: str | None = None
    is_active: bool | None = None
    subscription_plan: str | None = None
    max_students: int | None = None


class UniversityResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    domain: str | None
    logo_url: str | None
    primary_color: str
    secondary_color: str
    description: str | None
    is_active: bool
    subscription_plan: str
    max_students: int | None
    created_at: datetime

    model_config = {"from_attributes": True}


class UniversityListResponse(BaseModel):
    universities: list[UniversityResponse]
    total: int
