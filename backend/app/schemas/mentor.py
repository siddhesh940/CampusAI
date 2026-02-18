"""
Schemas for Mentoring System module.
"""

import uuid
from datetime import date, datetime, time

from pydantic import BaseModel, Field


# ─── Mentor Assignment ────────────────────────────────
class MentorAssignmentCreate(BaseModel):
    student_id: uuid.UUID
    mentor_id: uuid.UUID


class MentorAssignmentResponse(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    mentor_id: uuid.UUID
    university_id: uuid.UUID
    is_active: bool
    assigned_at: datetime
    # Nested user info
    mentor_name: str | None = None
    mentor_email: str | None = None
    student_name: str | None = None
    student_email: str | None = None

    model_config = {"from_attributes": True}


class MentorAssignmentListResponse(BaseModel):
    assignments: list[MentorAssignmentResponse]
    total: int


# ─── Mentor Meeting ──────────────────────────────────
class MeetingCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None = None
    meeting_date: date
    start_time: time
    end_time: time | None = None
    meeting_link: str | None = Field(None, max_length=512)


class MeetingUpdateStatus(BaseModel):
    status: str = Field(..., pattern="^(approved|rejected|completed|cancelled)$")
    notes: str | None = None
    meeting_link: str | None = None


class MeetingResponse(BaseModel):
    id: uuid.UUID
    assignment_id: uuid.UUID
    student_id: uuid.UUID
    mentor_id: uuid.UUID
    university_id: uuid.UUID
    title: str
    description: str | None
    meeting_date: date
    start_time: time
    end_time: time | None
    status: str
    meeting_link: str | None
    notes: str | None
    mentor_name: str | None = None
    student_name: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class MeetingListResponse(BaseModel):
    meetings: list[MeetingResponse]
    total: int


# ─── Mentor Messages ─────────────────────────────────
class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)


class MessageResponse(BaseModel):
    id: uuid.UUID
    assignment_id: uuid.UUID
    sender_id: uuid.UUID
    content: str
    is_read: bool
    sender_name: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageListResponse(BaseModel):
    messages: list[MessageResponse]
    total: int


# ─── Mentor Profile (for student view) ───────────────
class MentorProfileResponse(BaseModel):
    mentor_id: uuid.UUID
    mentor_name: str
    mentor_email: str
    assignment_id: uuid.UUID
    is_active: bool
    assigned_at: datetime
    upcoming_meetings: list[MeetingResponse] = []
    unread_messages: int = 0
