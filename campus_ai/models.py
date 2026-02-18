"""
CampusAI - Database Models
SQLAlchemy ORM models for all entities.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """User account model for authentication."""
    __tablename__: str = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="student")
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="user", uselist=False)


class Student(Base):
    """Student profile and onboarding data."""
    __tablename__: str = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    branch = Column(String(100), default="")
    year = Column(Integer, default=1)
    hostel_preference = Column(String(50), default="none")
    fee_status = Column(String(20), default="unpaid")
    documents_verified = Column(Boolean, default=False)
    lms_activated = Column(Boolean, default=False)
    orientation_completed = Column(Boolean, default=False)
    mentor_assigned = Column(String(100), default="")
    phone = Column(String(20), default="")
    address = Column(Text, default="")
    onboarding_stage = Column(Integer, default=1)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="student")
    reminders = relationship("Reminder", back_populates="student")
    chat_history = relationship("ChatHistory", back_populates="student")
    escalations = relationship("Escalation", back_populates="student")


class Reminder(Base):
    """Automated reminder entries."""
    __tablename__: str = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    message = Column(Text, nullable=False)
    category = Column(String(50), default="general")
    deadline = Column(DateTime, nullable=True)
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="reminders")


class ChatHistory(Base):
    """Chat conversation history."""
    __tablename__: str = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    role = Column(String(10), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="chat_history")


class Escalation(Base):
    """Escalation requests from students."""
    __tablename__: str = "escalations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject = Column(String(255), default="General Query")
    message = Column(Text, nullable=False)
    status = Column(String(20), default="pending")
    admin_response = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    student = relationship("Student", back_populates="escalations")
