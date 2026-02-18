"""
Compliance Service – items and student completion tracking.
"""
import uuid
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.compliance import ComplianceItem, StudentCompliance
from app.models.user import User
from app.schemas.compliance import (
    ComplianceItemCreate, ComplianceItemUpdate, ComplianceItemResponse, ComplianceItemListResponse,
    StudentComplianceSubmit, StudentComplianceResponse, StudentComplianceListResponse,
)

class ComplianceService:
    @staticmethod
    async def create_item(db: AsyncSession, admin: User, data: ComplianceItemCreate) -> ComplianceItemResponse:
        item = ComplianceItem(id=uuid.uuid4(), university_id=admin.university_id, title=data.title, description=data.description, compliance_type=data.compliance_type, content_url=data.content_url, order=data.order, is_required=data.is_required)
        db.add(item)
        await db.flush()
        await db.refresh(item)
        return ComplianceItemResponse.model_validate(item)

    @staticmethod
    async def update_item(db: AsyncSession, admin: User, item_id: uuid.UUID, data: ComplianceItemUpdate) -> ComplianceItemResponse:
        result = await db.execute(select(ComplianceItem).where(ComplianceItem.id == item_id, ComplianceItem.university_id == admin.university_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Compliance item not found")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        await db.flush()
        await db.refresh(item)
        return ComplianceItemResponse.model_validate(item)

    @staticmethod
    async def list_items(db: AsyncSession, university_id: uuid.UUID) -> ComplianceItemListResponse:
        result = await db.execute(select(ComplianceItem).where(ComplianceItem.university_id == university_id, ComplianceItem.is_active == True).order_by(ComplianceItem.order))
        items = result.scalars().all()
        return ComplianceItemListResponse(items=[ComplianceItemResponse.model_validate(i) for i in items], total=len(items))

    @staticmethod
    async def submit_compliance(db: AsyncSession, user: User, data: StudentComplianceSubmit) -> StudentComplianceResponse:
        # Verify item exists
        item_result = await db.execute(select(ComplianceItem).where(ComplianceItem.id == data.compliance_item_id, ComplianceItem.university_id == user.university_id))
        item = item_result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Compliance item not found")
        # Check existing
        existing = await db.execute(select(StudentCompliance).where(StudentCompliance.user_id == user.id, StudentCompliance.compliance_item_id == data.compliance_item_id))
        record = existing.scalar_one_or_none()
        if record:
            if record.is_completed:
                raise HTTPException(status_code=400, detail="Already completed")
            record.is_completed = True
            record.completed_at = datetime.now(timezone.utc)
        else:
            record = StudentCompliance(id=uuid.uuid4(), user_id=user.id, compliance_item_id=data.compliance_item_id, university_id=user.university_id, is_completed=True, completed_at=datetime.now(timezone.utc))
            db.add(record)
        await db.flush()
        await db.refresh(record)
        resp = StudentComplianceResponse.model_validate(record)
        resp.item_title = item.title
        resp.item_type = item.compliance_type.value if hasattr(item.compliance_type, 'value') else item.compliance_type
        resp.item_description = item.description
        resp.content_url = item.content_url
        resp.is_required = item.is_required
        return resp

    @staticmethod
    async def get_student_compliance(db: AsyncSession, user: User) -> StudentComplianceListResponse:
        # Get all items for university
        items_result = await db.execute(select(ComplianceItem).where(ComplianceItem.university_id == user.university_id, ComplianceItem.is_active == True).order_by(ComplianceItem.order))
        all_items = items_result.scalars().all()
        # Get student's completions
        comp_result = await db.execute(select(StudentCompliance).where(StudentCompliance.user_id == user.id))
        completions = {c.compliance_item_id: c for c in comp_result.scalars().all()}

        response_items = []
        required_total = 0
        required_completed = 0
        completed_count = 0

        for item in all_items:
            comp = completions.get(item.id)
            is_done = comp.is_completed if comp else False
            if is_done:
                completed_count += 1
            if item.is_required:
                required_total += 1
                if is_done:
                    required_completed += 1
            response_items.append(StudentComplianceResponse(
                id=comp.id if comp else uuid.uuid4(),
                user_id=user.id,
                compliance_item_id=item.id,
                university_id=user.university_id,
                is_completed=is_done,
                completed_at=comp.completed_at if comp else None,
                item_title=item.title,
                item_type=item.compliance_type.value if hasattr(item.compliance_type, 'value') else item.compliance_type,
                item_description=item.description,
                content_url=item.content_url,
                is_required=item.is_required,
            ))

        return StudentComplianceListResponse(
            items=response_items, total=len(response_items),
            completed=completed_count, required_total=required_total,
            required_completed=required_completed,
            all_required_done=required_completed >= required_total,
        )
