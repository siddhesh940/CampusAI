"""
CampusAI - Reminder Service
Generates and manages automated reminders based on student progress.
"""
from datetime import datetime, timedelta
from database import get_session
from models import Reminder, Student


def generate_reminders(student_id):
    """Generate reminders based on current student status."""
    session = get_session()
    try:
        student = session.query(Student).filter(Student.id == student_id).first()
        if not student:
            return []

        new_reminders = []

        # Check fee status
        if student.fee_status != "paid":
            existing = session.query(Reminder).filter(
                Reminder.student_id == student_id,
                Reminder.category == "fee",
                Reminder.resolved == False
            ).first()
            if not existing:
                reminder = Reminder(
                    student_id=student_id,
                    message="Your admission fee is pending. Pay before the deadline to secure your seat.",
                    category="fee",
                    deadline=datetime.utcnow() + timedelta(days=14),
                    resolved=False
                )
                session.add(reminder)
                new_reminders.append("fee")

        # Check documents
        if not student.documents_verified:
            existing = session.query(Reminder).filter(
                Reminder.student_id == student_id,
                Reminder.category == "documents",
                Reminder.resolved == False
            ).first()
            if not existing:
                reminder = Reminder(
                    student_id=student_id,
                    message="Please submit your documents for verification. Required: 10th marksheet, 12th marksheet, ID proof, photos.",
                    category="documents",
                    deadline=datetime.utcnow() + timedelta(days=21),
                    resolved=False
                )
                session.add(reminder)
                new_reminders.append("documents")

        # Check LMS
        if not student.lms_activated:
            existing = session.query(Reminder).filter(
                Reminder.student_id == student_id,
                Reminder.category == "lms",
                Reminder.resolved == False
            ).first()
            if not existing:
                reminder = Reminder(
                    student_id=student_id,
                    message="Activate your LMS account to access course materials and assignments.",
                    category="lms",
                    deadline=datetime.utcnow() + timedelta(days=7),
                    resolved=False
                )
                session.add(reminder)
                new_reminders.append("lms")

        # Check orientation
        if not student.orientation_completed:
            existing = session.query(Reminder).filter(
                Reminder.student_id == student_id,
                Reminder.category == "orientation",
                Reminder.resolved == False
            ).first()
            if not existing:
                reminder = Reminder(
                    student_id=student_id,
                    message="Don't miss the orientation program. Check the schedule for your batch.",
                    category="orientation",
                    deadline=datetime.utcnow() + timedelta(days=10),
                    resolved=False
                )
                session.add(reminder)
                new_reminders.append("orientation")

        session.commit()
        return new_reminders
    except Exception:
        session.rollback()
        return []
    finally:
        session.close()


def get_active_reminders(student_id):
    """Get all unresolved reminders for a student."""
    session = get_session()
    try:
        reminders = session.query(Reminder).filter(
            Reminder.student_id == student_id,
            Reminder.resolved == False
        ).order_by(Reminder.deadline.asc()).all()

        result = []
        for r in reminders:
            days_left = 0
            if r.deadline:
                delta = r.deadline - datetime.utcnow()
                days_left: int = max(0, delta.days)
            result.append({
                "id": r.id,
                "message": r.message,
                "category": r.category,
                "deadline": str(r.deadline) if r.deadline else "",
                "days_left": days_left,
                "urgent": days_left < 3
            })
        return result
    finally:
        session.close()


def resolve_reminder(reminder_id) -> bool:
    """Mark a reminder as resolved."""
    session = get_session()
    try:
        reminder = session.query(Reminder).filter(Reminder.id == reminder_id).first()
        if reminder:
            reminder.resolved = True
            session.commit()
            return True
        return False
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()


def resolve_category_reminders(student_id, category) -> bool:
    """Resolve all reminders of a specific category for a student."""
    session = get_session()
    try:
        reminders = session.query(Reminder).filter(
            Reminder.student_id == student_id,
            Reminder.category == category,
            Reminder.resolved == False
        ).all()
        for r in reminders:
            r.resolved = True
        session.commit()
        return True
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()
