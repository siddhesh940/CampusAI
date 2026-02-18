"""
Onboarding progress schemas.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel


class ChecklistItemResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    category: str
    order: int
    is_completed: bool
    is_required: bool
    deadline: datetime | None
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class ChecklistItemUpdate(BaseModel):
    is_completed: bool


class OnboardingProgressResponse(BaseModel):
    id: uuid.UUID
    overall_progress: int
    is_completed: bool
    completed_at: datetime | None
    items: list[ChecklistItemResponse]
    created_at: datetime

    model_config = {"from_attributes": True}
