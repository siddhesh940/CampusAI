"""Script to fix user.py model file."""
import os

TARGET: str = os.path.join(os.path.dirname(__file__), "app", "models", "user.py")

CONTENT = '''\
"""
User model with role-based access control.
Users are always scoped to a university (multi-tenant).
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(str, enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.STUDENT, nullable=False
    )

    # Multi-tenant FK - nullable for superadmins (platform-level)
    university_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("universities.id"), nullable=True, index=True
    )

    # Account status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verification_token: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    refresh_token: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    university = relationship("University", back_populates="users", lazy="selectin")
    documents = relationship(
        "Document", back_populates="user",
        foreign_keys="[Document.user_id]", lazy="selectin",
    )
    payments = relationship("Payment", back_populates="user", lazy="selectin")
    hostel_application = relationship(
        "HostelApplication", back_populates="user",
        uselist=False, foreign_keys="[HostelApplication.user_id]", lazy="selectin",
    )
    lms_activation = relationship(
        "LMSActivation", back_populates="user", uselist=False, lazy="selectin",
    )
    onboarding = relationship(
        "OnboardingChecklist", back_populates="user", uselist=False, lazy="selectin",
    )
    chat_sessions = relationship("ChatSession", back_populates="user", lazy="selectin")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role.value})>"
'''

# Delete old file
if os.path.exists(TARGET):
    os.remove(TARGET)
    print(f"Deleted old file: {TARGET}")

# Write new file
with open(TARGET, 'w', encoding='utf-8', newline='\n') as f: os.TextIOWrapper[_WrappedBuffer]:
    f.write(CONTENT)
    f.flush()
    os.fsync(f.fileno())

# Verify
with open(TARGET, 'r', encoding='utf-8') as f: os.TextIOWrapper[_WrappedBuffer]:
    written: str = f.read()

print(f"Written {len(CONTENT)} chars to {TARGET}")
print(f"Verify: '_RelationshipDeclared' in file: {'_RelationshipDeclared' in written}")
print(f"Verify: 'relationship(' in file: {'relationship(' in written}")
print("SUCCESS" if '_RelationshipDeclared' not in written else "FAILED")
