"""
Onboarding Router

Endpoints: get progress, update checklist item.
"""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.onboarding import ChecklistItemUpdate, OnboardingProgressResponse
from app.services.onboarding_service import OnboardingService

router = APIRouter()


@router.get(
    "/progress",
    response_model=OnboardingProgressResponse,
    summary="Get onboarding progress",
)
async def get_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return the student's onboarding checklist and overall progress."""
    return await OnboardingService.get_progress(db, current_user)


@router.put(
    "/checklist/{item_id}",
    response_model=OnboardingProgressResponse,
    summary="Update checklist item",
)
async def update_checklist_item(
    item_id: uuid.UUID,
    data: ChecklistItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a checklist item as completed or incomplete."""
    return await OnboardingService.update_item(db, current_user, item_id, data)
