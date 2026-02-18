"""
Hostel application schemas.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.hostel import ApplicationStatus, RoomType


class HostelApplicationRequest(BaseModel):
    room_type_preference: RoomType
    special_requirements: str | None = None


class HostelAllocationRequest(BaseModel):
    status: ApplicationStatus
    allocated_room_number: str | None = None
    allocated_block: str | None = None
    floor: int | None = None
    admin_notes: str | None = None


class HostelApplicationResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    room_type_preference: RoomType
    status: ApplicationStatus
    allocated_room_number: str | None
    allocated_block: str | None
    floor: int | None
    special_requirements: str | None
    admin_notes: str | None
    processed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
