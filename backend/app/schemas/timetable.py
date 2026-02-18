"""
Schemas for Timetable module.
"""

import uuid
from datetime import datetime, time

from pydantic import BaseModel, Field


class ScheduleCreate(BaseModel):
    subject_id: uuid.UUID
    day_of_week: str = Field(..., pattern="^(monday|tuesday|wednesday|thursday|friday|saturday)$")
    start_time: time
    end_time: time
    room: str | None = Field(None, max_length=100)
    instructor: str | None = Field(None, max_length=255)


class ScheduleUpdate(BaseModel):
    day_of_week: str | None = Field(None, pattern="^(monday|tuesday|wednesday|thursday|friday|saturday)$")
    start_time: time | None = None
    end_time: time | None = None
    room: str | None = Field(None, max_length=100)
    instructor: str | None = Field(None, max_length=255)


class ScheduleResponse(BaseModel):
    id: uuid.UUID
    subject_id: uuid.UUID
    university_id: uuid.UUID
    day_of_week: str
    start_time: time
    end_time: time
    room: str | None
    instructor: str | None
    subject_name: str | None = None
    subject_code: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ScheduleListResponse(BaseModel):
    schedules: list[ScheduleResponse]
    total: int


class TimetableEntry(BaseModel):
    """Single slot in the timetable grid."""
    schedule_id: uuid.UUID
    subject_name: str
    subject_code: str
    start_time: time
    end_time: time
    room: str | None
    instructor: str | None


class TimetableDayResponse(BaseModel):
    day: str
    entries: list[TimetableEntry]


class WeeklyTimetableResponse(BaseModel):
    """Full weekly timetable for a student."""
    days: list[TimetableDayResponse]
    total_subjects: int
    total_hours: float
