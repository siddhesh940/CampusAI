"""
Timetable Router
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.timetable import (
    ScheduleCreate, ScheduleUpdate, ScheduleResponse, ScheduleListResponse,
    WeeklyTimetableResponse,
)
from app.services.timetable_service import TimetableService

router = APIRouter()

@router.post("/schedules", response_model=ScheduleResponse, dependencies=[Depends(require_role(UserRole.ADMIN))])
async def create_schedule(data: ScheduleCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await TimetableService.create_schedule(db, current_user, data)

@router.put("/schedules/{schedule_id}", response_model=ScheduleResponse, dependencies=[Depends(require_role(UserRole.ADMIN))])
async def update_schedule(schedule_id: uuid.UUID, data: ScheduleUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await TimetableService.update_schedule(db, current_user, schedule_id, data)

@router.delete("/schedules/{schedule_id}", dependencies=[Depends(require_role(UserRole.ADMIN))])
async def delete_schedule(schedule_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await TimetableService.delete_schedule(db, current_user, schedule_id)

@router.get("/schedules", response_model=ScheduleListResponse)
async def list_schedules(subject_id: Optional[uuid.UUID] = Query(None), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await TimetableService.list_schedules(db, current_user.university_id, subject_id)

@router.get("/weekly", response_model=WeeklyTimetableResponse)
async def weekly_timetable(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await TimetableService.get_weekly_timetable(db, current_user)
