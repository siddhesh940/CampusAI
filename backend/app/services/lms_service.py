"""
LMS Service

Handles LMS activation and status tracking.
"""

import random
import string
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lms import LMSActivation
from app.models.user import User


def _generate_lms_id() -> str:
    """Generate a random LMS ID like LMS-XXXXXX."""
    chars = string.ascii_uppercase + string.digits
    code = "".join(random.choices(chars, k=6))
    return f"LMS-{code}"


class LMSService:
    """LMS activation business logic."""

    @staticmethod
    async def activate(db: AsyncSession, user: User) -> dict:
        """Activate LMS access for a student."""
        # Check if already activated
        result = await db.execute(
            select(LMSActivation).where(LMSActivation.user_id == user.id)
        )
        existing = result.scalar_one_or_none()

        if existing and existing.is_activated:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="LMS access is already activated.",
            )

        if existing:
            # Re-activate
            existing.is_activated = True
            existing.lms_username = user.email.split("@")[0]
            existing.activation_key = _generate_lms_id()
            existing.activated_at = datetime.now(timezone.utc)
            await db.flush()
            activation = existing
        else:
            activation = LMSActivation(
                id=uuid.uuid4(),
                user_id=user.id,
                university_id=user.university_id,
                platform="Moodle",
                is_activated=True,
                lms_username=user.email.split("@")[0],
                activation_key=_generate_lms_id(),
                activated_at=datetime.now(timezone.utc),
            )
            db.add(activation)
            await db.flush()

        return {
            "id": str(activation.id),
            "user_id": str(activation.user_id),
            "platform": activation.platform,
            "is_activated": activation.is_activated,
            "lms_username": activation.lms_username,
            "lms_id": activation.activation_key,
            "activated_at": activation.activated_at.isoformat() if activation.activated_at else None,
        }

    @staticmethod
    async def get_status(db: AsyncSession, user: User) -> dict:
        """Check LMS activation status."""
        result = await db.execute(
            select(LMSActivation).where(LMSActivation.user_id == user.id)
        )
        activation = result.scalar_one_or_none()
        if not activation:
            return {
                "is_activated": False,
                "platform": "Moodle",
                "lms_username": None,
                "lms_id": None,
                "activated_at": None,
            }

        return {
            "id": str(activation.id),
            "user_id": str(activation.user_id),
            "platform": activation.platform,
            "is_activated": activation.is_activated,
            "lms_username": activation.lms_username,
            "lms_id": activation.activation_key,
            "activated_at": activation.activated_at.isoformat() if activation.activated_at else None,
        }
