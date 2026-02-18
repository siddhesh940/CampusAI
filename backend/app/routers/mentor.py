"""
Mentor Router
"""
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.mentor import (
    MentorAssignmentCreate, MentorAssignmentResponse, MentorAssignmentListResponse,
    MeetingCreate, MeetingUpdateStatus, MeetingResponse, MeetingListResponse,
    MessageCreate, MessageResponse, MessageListResponse, MentorProfileResponse,
)
from app.services.mentor_service import MentorService

router = APIRouter()

# ── Admin ────────────────────────────────────
@router.post("/assign", response_model=MentorAssignmentResponse, dependencies=[Depends(require_role(UserRole.ADMIN))])
async def assign_mentor(data: MentorAssignmentCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await MentorService.assign_mentor(db, current_user, data)

@router.get("/assignments", response_model=MentorAssignmentListResponse, dependencies=[Depends(require_role(UserRole.ADMIN))])
async def list_assignments(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await MentorService.list_assignments(db, current_user.university_id)

@router.delete("/assignments/{assignment_id}", dependencies=[Depends(require_role(UserRole.ADMIN))])
async def deactivate_assignment(assignment_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await MentorService.deactivate_assignment(db, current_user, assignment_id)

# ── Student ──────────────────────────────────
@router.get("/me", response_model=MentorProfileResponse)
async def get_my_mentor(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await MentorService.get_my_mentor(db, current_user)

# ── Mentor role ──────────────────────────────
@router.get("/students", response_model=MentorAssignmentListResponse)
async def get_my_students(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await MentorService.get_my_students(db, current_user)

# ── Meetings ─────────────────────────────────
@router.post("/meetings", response_model=MeetingResponse)
async def book_meeting(data: MeetingCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await MentorService.book_meeting(db, current_user, data)

@router.put("/meetings/{meeting_id}", response_model=MeetingResponse)
async def update_meeting(meeting_id: uuid.UUID, data: MeetingUpdateStatus, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await MentorService.update_meeting_status(db, current_user, meeting_id, data)

@router.get("/meetings", response_model=MeetingListResponse)
async def list_meetings(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await MentorService.list_meetings(db, current_user)

# ── Messages ─────────────────────────────────
@router.post("/{assignment_id}/messages", response_model=MessageResponse)
async def send_message(assignment_id: uuid.UUID, data: MessageCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await MentorService.send_message(db, current_user, assignment_id, data)

@router.get("/{assignment_id}/messages", response_model=MessageListResponse)
async def get_messages(assignment_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await MentorService.get_messages(db, current_user, assignment_id)
