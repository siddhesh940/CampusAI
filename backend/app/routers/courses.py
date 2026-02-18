"""
Course Registration Router
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.course import (
    CourseCreate, CourseUpdate, CourseResponse, CourseListResponse,
    SubjectCreate, SubjectUpdate, SubjectResponse, SubjectListResponse,
    EnrollmentCreate, EnrollmentListResponse, EnrollmentDropRequest,
)
from app.services.course_service import CourseService

router = APIRouter()

# ── Admin: Courses ───────────────────────────
@router.post("/", response_model=CourseResponse, dependencies=[Depends(require_role(UserRole.ADMIN))])
async def create_course(data: CourseCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CourseService.create_course(db, current_user, data)

@router.put("/{course_id}", response_model=CourseResponse, dependencies=[Depends(require_role(UserRole.ADMIN))])
async def update_course(course_id: uuid.UUID, data: CourseUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CourseService.update_course(db, current_user, course_id, data)

@router.get("/", response_model=CourseListResponse)
async def list_courses(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CourseService.list_courses(db, current_user.university_id)

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await CourseService.get_course(db, course_id)

# ── Admin: Subjects ──────────────────────────
@router.post("/subjects", response_model=SubjectResponse, dependencies=[Depends(require_role(UserRole.ADMIN))])
async def create_subject(data: SubjectCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CourseService.create_subject(db, current_user, data)

@router.put("/subjects/{subject_id}", response_model=SubjectResponse, dependencies=[Depends(require_role(UserRole.ADMIN))])
async def update_subject(subject_id: uuid.UUID, data: SubjectUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CourseService.update_subject(db, current_user, subject_id, data)

@router.get("/subjects/list", response_model=SubjectListResponse)
async def list_subjects(course_id: Optional[uuid.UUID] = Query(None), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CourseService.list_subjects(db, current_user.university_id, course_id)

# ── Student: Enrollments ─────────────────────
@router.post("/enroll", response_model=EnrollmentListResponse)
async def enroll(data: EnrollmentCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CourseService.enroll(db, current_user, data)

@router.post("/drop", response_model=EnrollmentListResponse)
async def drop_subject(data: EnrollmentDropRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CourseService.drop_subject(db, current_user, data)

@router.get("/enrollments/me", response_model=EnrollmentListResponse)
async def my_enrollments(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CourseService.get_enrollments(db, current_user)
