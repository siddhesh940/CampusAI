"""
Super Admin Router

Endpoints: manage universities, subscription plans.
Restricted to SuperAdmin role only.
"""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.university import UniversityCreate, UniversityListResponse, UniversityResponse, UniversityUpdate
from app.services.superadmin_service import SuperAdminService

router = APIRouter(dependencies=[Depends(require_role(UserRole.SUPERADMIN))])


@router.get(
    "/universities",
    response_model=UniversityListResponse,
    summary="List all universities",
)
async def list_universities(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all registered universities on the platform."""
    return await SuperAdminService.list_universities(db)


@router.post(
    "/universities",
    response_model=UniversityResponse,
    summary="Create a university",
)
async def create_university(
    data: UniversityCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Register a new university on the platform."""
    return await SuperAdminService.create_university(db, data)


@router.put(
    "/universities/{university_id}",
    response_model=UniversityResponse,
    summary="Update a university",
)
async def update_university(
    university_id: uuid.UUID,
    data: UniversityUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update university details."""
    return await SuperAdminService.update_university(db, university_id, data)


@router.get(
    "/subscriptions",
    summary="List subscription plans",
)
async def list_subscriptions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all subscription plans."""
    return await SuperAdminService.list_subscriptions(db)


@router.get(
    "/dashboard",
    summary="Super admin dashboard stats",
)
async def dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get platform-wide statistics for super admin dashboard."""
    return await SuperAdminService.get_dashboard_stats(db)
