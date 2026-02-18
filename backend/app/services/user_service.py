"""
User Service

Handles profile management operations.
"""

import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate


class UserService:
    """User profile business logic."""

    @staticmethod
    async def update_profile(
        db: AsyncSession, user: User, data: UserUpdate
    ) -> UserResponse:
        """Update user profile fields."""
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await db.flush()
        return UserResponse.model_validate(user)

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
        """Get user by ID."""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
