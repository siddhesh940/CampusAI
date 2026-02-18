"""
Admin Router

Endpoints: student list, analytics, document management, escalations.
Restricted to Admin and SuperAdmin roles.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.document import DocumentListResponse
from app.schemas.user import UserListResponse
from app.services.admin_service import AdminService

router = APIRouter(dependencies=[Depends(require_role(UserRole.ADMIN))])


@router.get(
    "/students",
    response_model=UserListResponse,
    summary="List students",
)
async def list_students(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all students in the admin's university with pagination."""
    return await AdminService.list_students(db, current_user, page, per_page, search)


@router.get(
    "/analytics",
    summary="Onboarding analytics",
)
async def get_analytics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get onboarding analytics for the admin's university."""
    analytics = await AdminService.get_analytics(db, current_user)
    # Flatten for frontend compatibility
    return {
        "total_students": analytics["total_students"],
        "onboarding_completed": analytics["onboarding_completed"],
        "completion_rate": analytics["completion_rate"],
        "pending_documents": analytics["documents"]["pending"],
        "total_revenue": analytics["payments"]["revenue"],
        "pending_hostel": analytics["hostel"]["pending"],
    }


@router.get(
    "/documents/pending",
    response_model=DocumentListResponse,
    summary="Pending document reviews",
)
async def pending_documents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all documents pending review in the admin's university."""
    return await AdminService.get_pending_documents(db, current_user)


@router.get(
    "/documents",
    response_model=DocumentListResponse,
    summary="All documents with filters",
)
async def list_documents(
    status: Optional[str] = Query(None, description="Filter by status: pending, under_review, approved, rejected, or all"),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None, description="Search by student name, email, or document type"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all documents in the admin's university with status filtering, pagination, and student info."""
    return await AdminService.get_documents(db, current_user, status, page, per_page, search)


@router.get(
    "/escalations",
    summary="Get escalated issues",
)
async def get_escalations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get escalated onboarding issues requiring admin attention."""
    return await AdminService.get_escalations(db, current_user)
