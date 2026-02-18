"""
University Service

Manages university CRUD operations (used by SuperAdmin).
"""

import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.university import University
from app.schemas.university import UniversityCreate, UniversityResponse, UniversityUpdate


class UniversityService:
    """University management business logic."""

    @staticmethod
    async def create(db: AsyncSession, data: UniversityCreate) -> UniversityResponse:
        university = University(
            id=uuid.uuid4(),
            name=data.name,
            slug=data.slug,
            domain=data.domain,
            logo_url=data.logo_url,
            primary_color=data.primary_color,
            secondary_color=data.secondary_color,
            description=data.description,
            subscription_plan=data.subscription_plan,
            max_students=data.max_students,
            is_active=True,
        )
        db.add(university)
        await db.flush()
        return UniversityResponse.model_validate(university)

    @staticmethod
    async def update(
        db: AsyncSession, university_id: uuid.UUID, data: UniversityUpdate
    ) -> UniversityResponse:
        result = await db.execute(
            select(University).where(University.id == university_id)
        )
        university = result.scalar_one_or_none()
        if not university:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="University not found.",
            )
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(university, field, value)
        await db.flush()
        return UniversityResponse.model_validate(university)

    @staticmethod
    async def get_by_slug(db: AsyncSession, slug: str) -> University | None:
        result = await db.execute(
            select(University).where(University.slug == slug)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_all(db: AsyncSession) -> list[University]:
        result = await db.execute(
            select(University).order_by(University.created_at.desc())
        )
        return list(result.scalars().all())
