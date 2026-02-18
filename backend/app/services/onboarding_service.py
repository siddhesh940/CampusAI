"""
Onboarding Service

Manages student onboarding progress and checklist items.
"""

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.onboarding import ChecklistItem, OnboardingChecklist
from app.models.user import User
from app.schemas.onboarding import ChecklistItemUpdate, OnboardingProgressResponse

DEFAULT_CHECKLIST_ITEMS = [
    {"title": "Complete Profile", "description": "Fill in your personal information", "category": "profile", "order": 1, "is_required": True},
    {"title": "Upload ID Proof", "description": "Upload a valid government ID (Aadhaar/PAN/Passport)", "category": "documents", "order": 2, "is_required": True},
    {"title": "Upload Marksheet", "description": "Upload your latest academic marksheet", "category": "documents", "order": 3, "is_required": True},
    {"title": "Upload Passport Photo", "description": "Upload a recent passport-size photo", "category": "documents", "order": 4, "is_required": True},
    {"title": "Pay Tuition Fee", "description": "Complete tuition fee payment", "category": "payments", "order": 5, "is_required": True},
    {"title": "Apply for Hostel", "description": "Submit hostel accommodation application", "category": "hostel", "order": 6, "is_required": False},
    {"title": "Activate LMS Access", "description": "Activate your Learning Management System account", "category": "lms", "order": 7, "is_required": True},
    {"title": "Medical Certificate", "description": "Upload medical fitness certificate", "category": "documents", "order": 8, "is_required": False},
]


class OnboardingService:
    """Onboarding progress business logic."""

    @staticmethod
    async def get_progress(
        db: AsyncSession, user: User
    ) -> OnboardingProgressResponse:
        """Get onboarding checklist and progress for a student."""
        result = await db.execute(
            select(OnboardingChecklist).where(OnboardingChecklist.user_id == user.id)
        )
        checklist = result.scalar_one_or_none()

        if not checklist:
            # Auto-create default checklist
            checklist = await OnboardingService.create_default_checklist(db, user)

        # Fetch items
        items_result = await db.execute(
            select(ChecklistItem)
            .where(ChecklistItem.checklist_id == checklist.id)
            .order_by(ChecklistItem.order)
        )
        items = items_result.scalars().all()

        return OnboardingProgressResponse(
            id=checklist.id,
            overall_progress=checklist.overall_progress,
            is_completed=checklist.is_completed,
            completed_at=checklist.completed_at,
            items=items,
            created_at=checklist.created_at,
        )

    @staticmethod
    async def update_item(
        db: AsyncSession, user: User, item_id: uuid.UUID, data: ChecklistItemUpdate
    ) -> OnboardingProgressResponse:
        """Update a single checklist item and recalculate progress."""
        # Get checklist
        result = await db.execute(
            select(OnboardingChecklist).where(OnboardingChecklist.user_id == user.id)
        )
        checklist = result.scalar_one_or_none()
        if not checklist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Onboarding checklist not found.",
            )

        # Get item
        item_result = await db.execute(
            select(ChecklistItem).where(
                ChecklistItem.id == item_id,
                ChecklistItem.checklist_id == checklist.id,
            )
        )
        item = item_result.scalar_one_or_none()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Checklist item not found.",
            )

        item.is_completed = data.is_completed
        item.completed_at = datetime.now(timezone.utc) if data.is_completed else None
        await db.flush()

        # Recalculate progress
        all_items_result = await db.execute(
            select(ChecklistItem).where(ChecklistItem.checklist_id == checklist.id)
        )
        all_items = all_items_result.scalars().all()
        total = len(all_items)
        completed = sum(1 for i in all_items if i.is_completed)
        progress = int((completed / total) * 100) if total > 0 else 0

        checklist.overall_progress = progress
        checklist.is_completed = progress == 100
        checklist.completed_at = datetime.now(timezone.utc) if progress == 100 else None
        await db.flush()

        # Reload items
        items_result = await db.execute(
            select(ChecklistItem)
            .where(ChecklistItem.checklist_id == checklist.id)
            .order_by(ChecklistItem.order)
        )
        items = items_result.scalars().all()

        return OnboardingProgressResponse(
            id=checklist.id,
            overall_progress=checklist.overall_progress,
            is_completed=checklist.is_completed,
            completed_at=checklist.completed_at,
            items=items,
            created_at=checklist.created_at,
        )

    @staticmethod
    async def create_default_checklist(
        db: AsyncSession, user: User
    ) -> OnboardingChecklist:
        """Create default onboarding checklist for a new student."""
        checklist = OnboardingChecklist(
            id=uuid.uuid4(),
            user_id=user.id,
            university_id=user.university_id,
            overall_progress=0,
            is_completed=False,
        )
        db.add(checklist)
        await db.flush()

        for item_data in DEFAULT_CHECKLIST_ITEMS:
            item = ChecklistItem(
                id=uuid.uuid4(),
                checklist_id=checklist.id,
                **item_data,
            )
            db.add(item)

        await db.flush()
        return checklist
