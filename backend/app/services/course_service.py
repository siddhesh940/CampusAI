"""
Course Registration Service

Handles courses, subjects, and student enrollments.
"""

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course, Subject, Enrollment, EnrollmentStatus
from app.models.user import User
from app.schemas.course import (
    CourseCreate, CourseUpdate, CourseResponse, CourseListResponse,
    SubjectCreate, SubjectUpdate, SubjectResponse, SubjectListResponse,
    EnrollmentCreate, EnrollmentResponse, EnrollmentListResponse, EnrollmentDropRequest,
)


class CourseService:
    """Course & enrollment business logic."""

    # ── Courses ──────────────────────────────
    @staticmethod
    async def create_course(db: AsyncSession, admin: User, data: CourseCreate) -> CourseResponse:
        course = Course(
            id=uuid.uuid4(),
            university_id=admin.university_id,
            name=data.name,
            code=data.code,
            description=data.description,
            duration_years=data.duration_years,
            total_credits=data.total_credits,
        )
        db.add(course)
        await db.flush()
        await db.refresh(course)
        return CourseResponse.model_validate(course)

    @staticmethod
    async def update_course(db: AsyncSession, admin: User, course_id: uuid.UUID, data: CourseUpdate) -> CourseResponse:
        result = await db.execute(
            select(Course).where(Course.id == course_id, Course.university_id == admin.university_id)
        )
        course = result.scalar_one_or_none()
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(course, field, value)
        await db.flush()
        await db.refresh(course)
        return CourseResponse.model_validate(course)

    @staticmethod
    async def list_courses(db: AsyncSession, university_id: uuid.UUID) -> CourseListResponse:
        result = await db.execute(
            select(Course).where(Course.university_id == university_id, Course.is_active == True).order_by(Course.name)
        )
        courses = result.scalars().all()
        return CourseListResponse(
            courses=[CourseResponse.model_validate(c) for c in courses],
            total=len(courses),
        )

    @staticmethod
    async def get_course(db: AsyncSession, course_id: uuid.UUID) -> CourseResponse:
        result = await db.execute(select(Course).where(Course.id == course_id))
        course = result.scalar_one_or_none()
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        return CourseResponse.model_validate(course)

    # ── Subjects ─────────────────────────────
    @staticmethod
    async def create_subject(db: AsyncSession, admin: User, data: SubjectCreate) -> SubjectResponse:
        # Verify course belongs to admin's university
        result = await db.execute(
            select(Course).where(Course.id == data.course_id, Course.university_id == admin.university_id)
        )
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

        subject = Subject(
            id=uuid.uuid4(),
            course_id=data.course_id,
            university_id=admin.university_id,
            name=data.name,
            code=data.code,
            credits=data.credits,
            semester=data.semester,
            is_elective=data.is_elective,
        )
        db.add(subject)
        await db.flush()
        await db.refresh(subject)
        return SubjectResponse.model_validate(subject)

    @staticmethod
    async def update_subject(db: AsyncSession, admin: User, subject_id: uuid.UUID, data: SubjectUpdate) -> SubjectResponse:
        result = await db.execute(
            select(Subject).where(Subject.id == subject_id, Subject.university_id == admin.university_id)
        )
        subject = result.scalar_one_or_none()
        if not subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(subject, field, value)
        await db.flush()
        await db.refresh(subject)
        return SubjectResponse.model_validate(subject)

    @staticmethod
    async def list_subjects(db: AsyncSession, university_id: uuid.UUID, course_id: uuid.UUID | None = None) -> SubjectListResponse:
        query = select(Subject).where(Subject.university_id == university_id, Subject.is_active == True)
        if course_id:
            query = query.where(Subject.course_id == course_id)
        query = query.order_by(Subject.semester, Subject.name)
        result = await db.execute(query)
        subjects = result.scalars().all()
        return SubjectListResponse(
            subjects=[SubjectResponse.model_validate(s) for s in subjects],
            total=len(subjects),
        )

    # ── Enrollments ──────────────────────────
    @staticmethod
    async def enroll(db: AsyncSession, user: User, data: EnrollmentCreate) -> EnrollmentListResponse:
        # Verify course exists
        result = await db.execute(
            select(Course).where(Course.id == data.course_id, Course.university_id == user.university_id)
        )
        course = result.scalar_one_or_none()
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

        enrollments = []
        for subject_id in data.subject_ids:
            # Verify subject belongs to course
            sub_result = await db.execute(
                select(Subject).where(Subject.id == subject_id, Subject.course_id == data.course_id)
            )
            subject = sub_result.scalar_one_or_none()
            if not subject:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Subject {subject_id} not found in course",
                )

            # Check if already enrolled
            existing = await db.execute(
                select(Enrollment).where(
                    Enrollment.user_id == user.id,
                    Enrollment.subject_id == subject_id,
                    Enrollment.status == EnrollmentStatus.ACTIVE,
                )
            )
            if existing.scalar_one_or_none():
                continue  # Skip already enrolled

            enrollment = Enrollment(
                id=uuid.uuid4(),
                user_id=user.id,
                course_id=data.course_id,
                subject_id=subject_id,
                university_id=user.university_id,
                status=EnrollmentStatus.ACTIVE,
            )
            db.add(enrollment)
            enrollments.append(enrollment)

        await db.flush()
        for e in enrollments:
            await db.refresh(e)

        return await CourseService.get_enrollments(db, user)

    @staticmethod
    async def drop_subject(db: AsyncSession, user: User, data: EnrollmentDropRequest) -> EnrollmentListResponse:
        result = await db.execute(
            select(Enrollment).where(
                Enrollment.user_id == user.id,
                Enrollment.subject_id == data.subject_id,
                Enrollment.status == EnrollmentStatus.ACTIVE,
            )
        )
        enrollment = result.scalar_one_or_none()
        if not enrollment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")

        enrollment.status = EnrollmentStatus.DROPPED
        enrollment.dropped_at = datetime.now(timezone.utc)
        await db.flush()

        return await CourseService.get_enrollments(db, user)

    @staticmethod
    async def get_enrollments(db: AsyncSession, user: User) -> EnrollmentListResponse:
        result = await db.execute(
            select(Enrollment).where(
                Enrollment.user_id == user.id,
                Enrollment.status == EnrollmentStatus.ACTIVE,
            ).order_by(Enrollment.enrolled_at)
        )
        enrollments = result.scalars().all()
        items = []
        course_name = None
        for e in enrollments:
            resp = EnrollmentResponse.model_validate(e)
            if e.subject:
                resp.subject_name = e.subject.name
                resp.subject_code = e.subject.code
            if e.course:
                resp.course_name = e.course.name
                course_name = e.course.name
            items.append(resp)
        return EnrollmentListResponse(enrollments=items, total=len(items), course_name=course_name)
