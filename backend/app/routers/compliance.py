"""
Compliance Router
"""
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.compliance import (
    ComplianceItemCreate, ComplianceItemUpdate, ComplianceItemResponse, ComplianceItemListResponse,
    StudentComplianceSubmit, StudentComplianceResponse, StudentComplianceListResponse,
)
from app.services.compliance_service import ComplianceService

router = APIRouter()

# ── Admin ────────────────────────────────────
@router.post("/items", response_model=ComplianceItemResponse, dependencies=[Depends(require_role(UserRole.ADMIN))])
async def create_item(data: ComplianceItemCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ComplianceService.create_item(db, current_user, data)

@router.put("/items/{item_id}", response_model=ComplianceItemResponse, dependencies=[Depends(require_role(UserRole.ADMIN))])
async def update_item(item_id: uuid.UUID, data: ComplianceItemUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ComplianceService.update_item(db, current_user, item_id, data)

@router.get("/items", response_model=ComplianceItemListResponse)
async def list_items(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ComplianceService.list_items(db, current_user.university_id)

# ── Student ──────────────────────────────────
@router.post("/submit", response_model=StudentComplianceResponse)
async def submit_compliance(data: StudentComplianceSubmit, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ComplianceService.submit_compliance(db, current_user, data)

@router.get("/status", response_model=StudentComplianceListResponse)
async def get_compliance_status(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ComplianceService.get_student_compliance(db, current_user)
