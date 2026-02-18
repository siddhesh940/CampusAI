"""
Hostel Router

Endpoints: apply, check status, admin allocation.
"""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.hostel import (
    HostelAllocationRequest,
    HostelApplicationRequest,
    HostelApplicationResponse,
)
from app.services.hostel_service import HostelService

router = APIRouter()


@router.post(
    "/apply",
    response_model=HostelApplicationResponse,
    summary="Submit hostel application",
)
async def apply_hostel(
    data: HostelApplicationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit a new hostel room application."""
    return await HostelService.apply(db, current_user, data)


@router.get(
    "/status",
    response_model=HostelApplicationResponse,
    summary="Check hostel application status",
)
async def get_hostel_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the current hostel application status."""
    return await HostelService.get_status(db, current_user)


@router.put(
    "/{application_id}/allocate",
    response_model=HostelApplicationResponse,
    summary="Allocate hostel room (Admin)",
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
async def allocate_room(
    application_id: uuid.UUID,
    data: HostelAllocationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Admin: approve/reject and allocate a hostel room."""
    return await HostelService.allocate(db, current_user, application_id, data)
