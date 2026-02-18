"""
Schemas for Course Registration module.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


# ─── Course Schemas ────────────────────────────────────
class CourseCreate(BaseModel):
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    description: str | None = None
    duration_years: int = 4
    total_credits: int = 0


class CourseUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    code: str | None = Field(None, max_length=50)
    description: str | None = None
    duration_years: int | None = None
    total_credits: int | None = None
    is_active: bool | None = None


class CourseResponse(BaseModel):
    id: uuid.UUID
    university_id: uuid.UUID
    name: str
    code: str
    description: str | None
    duration_years: int
    total_credits: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class CourseListResponse(BaseModel):
    courses: list[CourseResponse]
    total: int


# ─── Subject Schemas ──────────────────────────────────
class SubjectCreate(BaseModel):
    course_id: uuid.UUID
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    credits: int = 3
    semester: int = 1
    is_elective: bool = False


class SubjectUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    code: str | None = Field(None, max_length=50)
    credits: int | None = None
    semester: int | None = None
    is_elective: bool | None = None
    is_active: bool | None = None


class SubjectResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    university_id: uuid.UUID
    name: str
    code: str
    credits: int
    semester: int
    is_elective: bool
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class SubjectListResponse(BaseModel):
    subjects: list[SubjectResponse]
    total: int


# ─── Enrollment Schemas ───────────────────────────────
class EnrollmentCreate(BaseModel):
    course_id: uuid.UUID
    subject_ids: list[uuid.UUID] = Field(..., min_length=1)


class EnrollmentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    course_id: uuid.UUID
    subject_id: uuid.UUID
    university_id: uuid.UUID
    status: str
    enrolled_at: datetime
    dropped_at: datetime | None
    subject_name: str | None = None
    subject_code: str | None = None
    course_name: str | None = None

    model_config = {"from_attributes": True}


class EnrollmentListResponse(BaseModel):
    enrollments: list[EnrollmentResponse]
    total: int
    course_name: str | None = None


class EnrollmentDropRequest(BaseModel):
    subject_id: uuid.UUID
