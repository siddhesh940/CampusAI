"""
Super Admin Service

Platform-level operations: university management, subscriptions, global stats.
"""

import re
import uuid

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment, PaymentStatus
from app.models.university import SubscriptionPlan, University
from app.models.user import User, UserRole
from app.schemas.university import (
    UniversityCreate,
    UniversityListResponse,
    UniversityResponse,
    UniversityUpdate,
)


class SuperAdminService:
    """Super admin business logic."""

    @staticmethod
    async def list_universities(db: AsyncSession) -> UniversityListResponse:
        """List all universities on the platform."""
        result = await db.execute(
            select(University).order_by(University.created_at.desc())
        )
        universities = result.scalars().all()
        return UniversityListResponse(
            universities=[UniversityResponse.model_validate(u) for u in universities],
            total=len(universities),
        )

    @staticmethod
    async def create_university(
        db: AsyncSession, data: UniversityCreate
    ) -> UniversityResponse:
        """Create a new university tenant."""
        # Check slug uniqueness
        existing = await db.execute(
            select(University).where(University.slug == data.slug)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A university with this slug already exists.",
            )

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
    async def update_university(
        db: AsyncSession, university_id: uuid.UUID, data: UniversityUpdate
    ) -> UniversityResponse:
        """Update a university's details."""
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
    async def list_subscriptions(db: AsyncSession) -> list:
        """List all subscription plans."""
        result = await db.execute(
            select(SubscriptionPlan).order_by(SubscriptionPlan.price_monthly)
        )
        plans = result.scalars().all()
        return [
            {
                "id": str(p.id),
                "name": p.name,
                "slug": p.slug,
                "price_monthly": p.price_monthly,
                "price_yearly": p.price_yearly,
                "max_students": p.max_students,
                "max_admins": p.max_admins,
                "features": p.features,
                "is_active": p.is_active,
            }
            for p in plans
        ]

    @staticmethod
    async def get_dashboard_stats(db: AsyncSession) -> dict:
        """Platform-wide statistics for super admin dashboard."""
        total_unis = await db.execute(select(func.count(University.id)))
        total_students = await db.execute(
            select(func.count()).where(User.role == UserRole.STUDENT)
        )
        total_admins = await db.execute(
            select(func.count()).where(User.role == UserRole.ADMIN)
        )
        total_revenue = await db.execute(
            select(func.coalesce(func.sum(Payment.amount), 0)).where(
                Payment.status == PaymentStatus.COMPLETED
            )
        )

        return {
            "total_universities": total_unis.scalar() or 0,
            "total_students": total_students.scalar() or 0,
            "total_admins": total_admins.scalar() or 0,
            "total_revenue": float(total_revenue.scalar() or 0),
        }
