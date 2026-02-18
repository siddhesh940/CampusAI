"""
CampusAI – ORM Models Package

All SQLAlchemy models are imported here for Alembic auto-detection.
"""

from app.models.university import University, SubscriptionPlan
from app.models.user import User, UserRole
from app.models.onboarding import OnboardingChecklist, ChecklistItem
from app.models.document import Document, DocumentStatus
from app.models.payment import Payment, PaymentStatus
from app.models.hostel import HostelApplication, RoomType, ApplicationStatus
from app.models.lms import LMSActivation
from app.models.chat import ChatSession, ChatMessage
from app.models.notification import Notification
from app.models.course import Course, Subject, Enrollment, EnrollmentStatus
from app.models.timetable import SubjectSchedule, DayOfWeek
from app.models.mentor import MentorAssignment, MentorMeeting, MentorMessage, MeetingStatus
from app.models.compliance import ComplianceItem, StudentCompliance, ComplianceType

__all__ = [
    "University",
    "SubscriptionPlan",
    "User",
    "UserRole",
    "OnboardingChecklist",
    "ChecklistItem",
    "Document",
    "DocumentStatus",
    "Payment",
    "PaymentStatus",
    "HostelApplication",
    "RoomType",
    "ApplicationStatus",
    "LMSActivation",
    "ChatSession",
    "ChatMessage",
    "Notification",
    "Course",
    "Subject",
    "Enrollment",
    "EnrollmentStatus",
    "SubjectSchedule",
    "DayOfWeek",
    "MentorAssignment",
    "MentorMeeting",
    "MentorMessage",
    "MeetingStatus",
    "ComplianceItem",
    "StudentCompliance",
    "ComplianceType",
]
