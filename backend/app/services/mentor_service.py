"""
Mentor Service

Handles mentor assignments, meetings, and messages.
"""

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mentor import MentorAssignment, MentorMeeting, MentorMessage, MeetingStatus
from app.models.user import User, UserRole
from app.schemas.mentor import (
    MentorAssignmentCreate, MentorAssignmentResponse, MentorAssignmentListResponse,
    MeetingCreate, MeetingUpdateStatus, MeetingResponse, MeetingListResponse,
    MessageCreate, MessageResponse, MessageListResponse,
    MentorProfileResponse,
)


class MentorService:
    """Mentoring system business logic."""

    # ── Admin: assign mentor ─────────────────
    @staticmethod
    async def assign_mentor(db: AsyncSession, admin: User, data: MentorAssignmentCreate) -> MentorAssignmentResponse:
        # Verify student exists
        student = await db.execute(select(User).where(User.id == data.student_id, User.university_id == admin.university_id))
        student = student.scalar_one_or_none()
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        # Verify mentor exists
        mentor = await db.execute(select(User).where(User.id == data.mentor_id, User.university_id == admin.university_id))
        mentor = mentor.scalar_one_or_none()
        if not mentor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor not found")

        # Check existing active assignment
        existing = await db.execute(
            select(MentorAssignment).where(
                MentorAssignment.student_id == data.student_id,
                MentorAssignment.is_active == True,
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already has an active mentor")

        assignment = MentorAssignment(
            id=uuid.uuid4(),
            student_id=data.student_id,
            mentor_id=data.mentor_id,
            university_id=admin.university_id,
        )
        db.add(assignment)
        await db.flush()
        await db.refresh(assignment)

        resp = MentorAssignmentResponse.model_validate(assignment)
        resp.mentor_name = f"{mentor.first_name} {mentor.last_name}"
        resp.mentor_email = mentor.email
        resp.student_name = f"{student.first_name} {student.last_name}"
        resp.student_email = student.email
        return resp

    @staticmethod
    async def list_assignments(db: AsyncSession, university_id: uuid.UUID) -> MentorAssignmentListResponse:
        result = await db.execute(
            select(MentorAssignment).where(
                MentorAssignment.university_id == university_id,
                MentorAssignment.is_active == True,
            ).order_by(MentorAssignment.assigned_at.desc())
        )
        assignments = result.scalars().all()
        items = []
        for a in assignments:
            resp = MentorAssignmentResponse.model_validate(a)
            if a.student:
                resp.student_name = f"{a.student.first_name} {a.student.last_name}"
                resp.student_email = a.student.email
            if a.mentor:
                resp.mentor_name = f"{a.mentor.first_name} {a.mentor.last_name}"
                resp.mentor_email = a.mentor.email
            items.append(resp)
        return MentorAssignmentListResponse(assignments=items, total=len(items))

    @staticmethod
    async def deactivate_assignment(db: AsyncSession, admin: User, assignment_id: uuid.UUID) -> dict:
        result = await db.execute(
            select(MentorAssignment).where(
                MentorAssignment.id == assignment_id,
                MentorAssignment.university_id == admin.university_id,
            )
        )
        assignment = result.scalar_one_or_none()
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        assignment.is_active = False
        await db.flush()
        return {"detail": "Assignment deactivated"}

    # ── Student: get my mentor ───────────────
    @staticmethod
    async def get_my_mentor(db: AsyncSession, user: User) -> MentorProfileResponse:
        result = await db.execute(
            select(MentorAssignment).where(
                MentorAssignment.student_id == user.id,
                MentorAssignment.is_active == True,
            )
        )
        assignment = result.scalar_one_or_none()
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No mentor assigned yet")

        # Count unread messages
        unread_result = await db.execute(
            select(func.count()).where(
                MentorMessage.assignment_id == assignment.id,
                MentorMessage.sender_id != user.id,
                MentorMessage.is_read == False,
            )
        )
        unread = unread_result.scalar() or 0

        # Upcoming meetings
        upcoming_result = await db.execute(
            select(MentorMeeting).where(
                MentorMeeting.assignment_id == assignment.id,
                MentorMeeting.status.in_([MeetingStatus.REQUESTED, MeetingStatus.APPROVED]),
            ).order_by(MentorMeeting.meeting_date)
        )
        upcoming = upcoming_result.scalars().all()
        meeting_items = []
        for m in upcoming:
            mr = MeetingResponse.model_validate(m)
            if m.mentor:
                mr.mentor_name = f"{m.mentor.first_name} {m.mentor.last_name}"
            if m.student:
                mr.student_name = f"{m.student.first_name} {m.student.last_name}"
            meeting_items.append(mr)

        mentor = assignment.mentor
        return MentorProfileResponse(
            mentor_id=mentor.id,
            mentor_name=f"{mentor.first_name} {mentor.last_name}",
            mentor_email=mentor.email,
            assignment_id=assignment.id,
            is_active=assignment.is_active,
            assigned_at=assignment.assigned_at,
            upcoming_meetings=meeting_items,
            unread_messages=unread,
        )

    # ── Mentor: get assigned students ────────
    @staticmethod
    async def get_my_students(db: AsyncSession, user: User) -> MentorAssignmentListResponse:
        result = await db.execute(
            select(MentorAssignment).where(
                MentorAssignment.mentor_id == user.id,
                MentorAssignment.is_active == True,
            ).order_by(MentorAssignment.assigned_at.desc())
        )
        assignments = result.scalars().all()
        items = []
        for a in assignments:
            resp = MentorAssignmentResponse.model_validate(a)
            if a.student:
                resp.student_name = f"{a.student.first_name} {a.student.last_name}"
                resp.student_email = a.student.email
            if a.mentor:
                resp.mentor_name = f"{a.mentor.first_name} {a.mentor.last_name}"
                resp.mentor_email = a.mentor.email
            items.append(resp)
        return MentorAssignmentListResponse(assignments=items, total=len(items))

    # ── Meetings ─────────────────────────────
    @staticmethod
    async def book_meeting(db: AsyncSession, user: User, data: MeetingCreate) -> MeetingResponse:
        # Get assignment
        result = await db.execute(
            select(MentorAssignment).where(
                MentorAssignment.student_id == user.id,
                MentorAssignment.is_active == True,
            )
        )
        assignment = result.scalar_one_or_none()
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No mentor assigned")

        meeting = MentorMeeting(
            id=uuid.uuid4(),
            assignment_id=assignment.id,
            student_id=user.id,
            mentor_id=assignment.mentor_id,
            university_id=user.university_id,
            title=data.title,
            description=data.description,
            meeting_date=data.meeting_date,
            start_time=data.start_time,
            end_time=data.end_time,
            meeting_link=data.meeting_link,
            status=MeetingStatus.REQUESTED,
        )
        db.add(meeting)
        await db.flush()
        await db.refresh(meeting)
        resp = MeetingResponse.model_validate(meeting)
        return resp

    @staticmethod
    async def update_meeting_status(db: AsyncSession, user: User, meeting_id: uuid.UUID, data: MeetingUpdateStatus) -> MeetingResponse:
        result = await db.execute(
            select(MentorMeeting).where(
                MentorMeeting.id == meeting_id,
                or_(MentorMeeting.mentor_id == user.id, MentorMeeting.student_id == user.id),
            )
        )
        meeting = result.scalar_one_or_none()
        if not meeting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")

        meeting.status = MeetingStatus(data.status)
        if data.notes:
            meeting.notes = data.notes
        if data.meeting_link:
            meeting.meeting_link = data.meeting_link
        await db.flush()
        await db.refresh(meeting)
        resp = MeetingResponse.model_validate(meeting)
        if meeting.mentor:
            resp.mentor_name = f"{meeting.mentor.first_name} {meeting.mentor.last_name}"
        if meeting.student:
            resp.student_name = f"{meeting.student.first_name} {meeting.student.last_name}"
        return resp

    @staticmethod
    async def list_meetings(db: AsyncSession, user: User) -> MeetingListResponse:
        result = await db.execute(
            select(MentorMeeting).where(
                or_(MentorMeeting.mentor_id == user.id, MentorMeeting.student_id == user.id)
            ).order_by(MentorMeeting.meeting_date.desc())
        )
        meetings = result.scalars().all()
        items = []
        for m in meetings:
            resp = MeetingResponse.model_validate(m)
            if m.mentor:
                resp.mentor_name = f"{m.mentor.first_name} {m.mentor.last_name}"
            if m.student:
                resp.student_name = f"{m.student.first_name} {m.student.last_name}"
            items.append(resp)
        return MeetingListResponse(meetings=items, total=len(items))

    # ── Messages ─────────────────────────────
    @staticmethod
    async def send_message(db: AsyncSession, user: User, assignment_id: uuid.UUID, data: MessageCreate) -> MessageResponse:
        # Verify user is part of assignment
        result = await db.execute(
            select(MentorAssignment).where(
                MentorAssignment.id == assignment_id,
                or_(MentorAssignment.student_id == user.id, MentorAssignment.mentor_id == user.id),
            )
        )
        assignment = result.scalar_one_or_none()
        if not assignment:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not part of this assignment")

        message = MentorMessage(
            id=uuid.uuid4(),
            assignment_id=assignment_id,
            sender_id=user.id,
            content=data.content,
        )
        db.add(message)
        await db.flush()
        await db.refresh(message)
        resp = MessageResponse.model_validate(message)
        resp.sender_name = f"{user.first_name} {user.last_name}"
        return resp

    @staticmethod
    async def get_messages(db: AsyncSession, user: User, assignment_id: uuid.UUID) -> MessageListResponse:
        # Verify user is part of assignment
        result = await db.execute(
            select(MentorAssignment).where(
                MentorAssignment.id == assignment_id,
                or_(MentorAssignment.student_id == user.id, MentorAssignment.mentor_id == user.id),
            )
        )
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not part of this assignment")

        # Mark messages as read
        msg_result = await db.execute(
            select(MentorMessage).where(
                MentorMessage.assignment_id == assignment_id,
            ).order_by(MentorMessage.created_at)
        )
        messages = msg_result.scalars().all()

        # Mark others' messages as read
        for m in messages:
            if m.sender_id != user.id and not m.is_read:
                m.is_read = True
        await db.flush()

        items = []
        for m in messages:
            resp = MessageResponse.model_validate(m)
            if m.sender:
                resp.sender_name = f"{m.sender.first_name} {m.sender.last_name}"
            items.append(resp)
        return MessageListResponse(messages=items, total=len(items))
