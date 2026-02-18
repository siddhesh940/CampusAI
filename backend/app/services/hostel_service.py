"""
Hostel Service

Handles hostel applications and admin allocation.
"""

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hostel import ApplicationStatus, HostelApplication
from app.models.user import User
from app.schemas.hostel import (
    HostelAllocationRequest,
    HostelApplicationRequest,
    HostelApplicationResponse,
)


class HostelService:
    """Hostel application business logic."""

    @staticmethod
    async def apply(
        db: AsyncSession, user: User, data: HostelApplicationRequest
    ) -> HostelApplicationResponse:
        """Submit a new hostel application."""
        # Check if already applied
        result = await db.execute(
            select(HostelApplication).where(HostelApplication.user_id == user.id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already submitted a hostel application.",
            )

        application = HostelApplication(
            id=uuid.uuid4(),
            user_id=user.id,
            university_id=user.university_id,
            room_type_preference=data.room_type_preference,
            special_requirements=data.special_requirements,
            status=ApplicationStatus.PENDING,
        )
        db.add(application)
        await db.flush()

        return HostelApplicationResponse.model_validate(application)

    @staticmethod
    async def get_status(
        db: AsyncSession, user: User
    ) -> HostelApplicationResponse:
        """Get current application status."""
        result = await db.execute(
            select(HostelApplication).where(HostelApplication.user_id == user.id)
        )
        application = result.scalar_one_or_none()
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hostel application found. Please apply first.",
            )
        return HostelApplicationResponse.model_validate(application)

    @staticmethod
    async def allocate(
        db: AsyncSession,
        admin: User,
        application_id: uuid.UUID,
        data: HostelAllocationRequest,
    ) -> HostelApplicationResponse:
        """Admin: allocate a room to a student."""
        result = await db.execute(
            select(HostelApplication).where(HostelApplication.id == application_id)
        )
        application = result.scalar_one_or_none()
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found.",
            )

        application.status = data.status
        application.allocated_room_number = data.allocated_room_number
        application.allocated_block = data.allocated_block
        application.floor = data.floor
        application.admin_notes = data.admin_notes
        application.processed_by = admin.id
        application.processed_at = datetime.now(timezone.utc)
        await db.flush()

        return HostelApplicationResponse.model_validate(application)
