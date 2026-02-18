"""
Payment schemas.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.payment import PaymentStatus


class PaymentInitiateRequest(BaseModel):
    payment_type: str = Field(..., max_length=100)
    amount: float = Field(..., gt=0)
    currency: str = "INR"
    payment_method: str | None = None
    notes: str | None = None


class PaymentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    payment_type: str
    amount: float
    currency: str
    status: PaymentStatus
    transaction_id: str | None
    payment_method: str | None
    receipt_url: str | None
    paid_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class PaymentListResponse(BaseModel):
    payments: list[PaymentResponse]
    total: int
