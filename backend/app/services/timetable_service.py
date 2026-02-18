"""
Timetable Service

Manages subject schedules and generates weekly timetable views.
"""

import uuid
from collections import defaultdict

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Enrollment, EnrollmentStatus
from app.models.timetable import SubjectSchedule, DayOfWeek
from app.models.user import User
from app.schemas.timetable import (
    ScheduleCreate, ScheduleUpdate, ScheduleResponse, ScheduleListResponse,
    TimetableEntry, TimetableDayResponse, WeeklyTimetableResponse,
)


class TimetableService:
    """Subject schedule & timetable generation."""

    # ── Admin: manage schedules ──────────────
    @staticmethod
    async def create_schedule(db: AsyncSession, admin: User, data: ScheduleCreate) -> ScheduleResponse:
        schedule = SubjectSchedule(
            id=uuid.uuid4(),
            subject_id=data.subject_id,
            university_id=admin.university_id,
            day_of_week=DayOfWeek(data.day_of_week),
            start_time=data.start_time,
            end_time=data.end_time,
            room=data.room,
            instructor=data.instructor,
        )
        db.add(schedule)
        await db.flush()
        await db.refresh(schedule)
        resp = ScheduleResponse.model_validate(schedule)
        if schedule.subject:
            resp.subject_name = schedule.subject.name
            resp.subject_code = schedule.subject.code
        return resp

    @staticmethod
    async def update_schedule(db: AsyncSession, admin: User, schedule_id: uuid.UUID, data: ScheduleUpdate) -> ScheduleResponse:
        result = await db.execute(
            select(SubjectSchedule).where(
                SubjectSchedule.id == schedule_id,
                SubjectSchedule.university_id == admin.university_id,
            )
        )
        schedule = result.scalar_one_or_none()
        if not schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")

        for field, value in data.model_dump(exclude_unset=True).items():
            if field == "day_of_week" and value:
                value = DayOfWeek(value)
            setattr(schedule, field, value)
        await db.flush()
        await db.refresh(schedule)
        resp = ScheduleResponse.model_validate(schedule)
        if schedule.subject:
            resp.subject_name = schedule.subject.name
            resp.subject_code = schedule.subject.code
        return resp

    @staticmethod
    async def delete_schedule(db: AsyncSession, admin: User, schedule_id: uuid.UUID) -> dict:
        result = await db.execute(
            select(SubjectSchedule).where(
                SubjectSchedule.id == schedule_id,
                SubjectSchedule.university_id == admin.university_id,
            )
        )
        schedule = result.scalar_one_or_none()
        if not schedule:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
        await db.delete(schedule)
        await db.flush()
        return {"detail": "Schedule deleted"}

    @staticmethod
    async def list_schedules(db: AsyncSession, university_id: uuid.UUID, subject_id: uuid.UUID | None = None) -> ScheduleListResponse:
        query = select(SubjectSchedule).where(SubjectSchedule.university_id == university_id)
        if subject_id:
            query = query.where(SubjectSchedule.subject_id == subject_id)
        query = query.order_by(SubjectSchedule.day_of_week, SubjectSchedule.start_time)
        result = await db.execute(query)
        schedules = result.scalars().all()
        items = []
        for s in schedules:
            resp = ScheduleResponse.model_validate(s)
            if s.subject:
                resp.subject_name = s.subject.name
                resp.subject_code = s.subject.code
            items.append(resp)
        return ScheduleListResponse(schedules=items, total=len(items))

    # ── Student: weekly timetable ────────────
    @staticmethod
    async def get_weekly_timetable(db: AsyncSession, user: User) -> WeeklyTimetableResponse:
        # Get enrolled subject IDs
        enroll_result = await db.execute(
            select(Enrollment.subject_id).where(
                Enrollment.user_id == user.id,
                Enrollment.status == EnrollmentStatus.ACTIVE,
            )
        )
        subject_ids = [row[0] for row in enroll_result.all()]

        if not subject_ids:
            days_order = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
            return WeeklyTimetableResponse(
                days=[TimetableDayResponse(day=d, entries=[]) for d in days_order],
                total_subjects=0,
                total_hours=0.0,
            )

        # Get schedules for enrolled subjects
        result = await db.execute(
            select(SubjectSchedule).where(
                SubjectSchedule.subject_id.in_(subject_ids),
                SubjectSchedule.university_id == user.university_id,
            ).order_by(SubjectSchedule.start_time)
        )
        schedules = result.scalars().all()

        # Group by day
        day_map: dict[str, list[TimetableEntry]] = defaultdict(list)
        total_hours = 0.0
        unique_subjects = set()

        for s in schedules:
            day_key = s.day_of_week.value
            subject_name = s.subject.name if s.subject else "Unknown"
            subject_code = s.subject.code if s.subject else "N/A"
            unique_subjects.add(s.subject_id)

            # Calculate hours
            start_minutes = s.start_time.hour * 60 + s.start_time.minute
            end_minutes = s.end_time.hour * 60 + s.end_time.minute
            total_hours += (end_minutes - start_minutes) / 60.0

            day_map[day_key].append(TimetableEntry(
                schedule_id=s.id,
                subject_name=subject_name,
                subject_code=subject_code,
                start_time=s.start_time,
                end_time=s.end_time,
                room=s.room,
                instructor=s.instructor,
            ))

        days_order = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
        days = [
            TimetableDayResponse(day=d, entries=sorted(day_map.get(d, []), key=lambda e: e.start_time))
            for d in days_order
        ]

        return WeeklyTimetableResponse(
            days=days,
            total_subjects=len(unique_subjects),
            total_hours=round(total_hours, 1),
        )
