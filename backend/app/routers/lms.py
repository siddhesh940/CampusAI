"""
LMS Router

Endpoints: activate, check status.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.services.lms_service import LMSService

router = APIRouter()


@router.post(
    "/activate",
    summary="Activate LMS access",
)
async def activate_lms(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Activate Learning Management System access for the student."""
    return await LMSService.activate(db, current_user)


@router.get(
    "/status",
    summary="Check LMS activation status",
)
async def lms_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Check if the student's LMS access is activated."""
    return await LMSService.get_status(db, current_user)
