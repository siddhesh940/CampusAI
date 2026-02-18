"""
LMS (Learning Management System) activation tracking model.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class LMSActivation(Base):
    __tablename__ = "lms_activations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
        unique=True, nullable=False,
    )
    university_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("universities.id"), nullable=False,
    )
    platform: Mapped[str] = mapped_column(
        String(100), default="Moodle"
    )  # Moodle, Canvas, Blackboard, etc.
    is_activated: Mapped[bool] = mapped_column(Boolean, default=False)
    lms_username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activation_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="lms_activation")

    def __repr__(self) -> str:
        status = "activated" if self.is_activated else "inactive"
        return f"<LMSActivation {self.platform} – {status}>"
