"""
Payments Router

Endpoints: initiate payment, verify payment, list payments, download receipt.
"""

import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.payment import PaymentInitiateRequest, PaymentListResponse, PaymentResponse
from app.services.payment_service import PaymentService

router = APIRouter()


@router.post(
    "/initiate",
    response_model=PaymentResponse,
    summary="Initiate a payment",
)
async def initiate_payment(
    data: PaymentInitiateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new payment record and initiate (simulated) payment flow."""
    return await PaymentService.initiate(db, current_user, data)


@router.post(
    "/{payment_id}/verify",
    response_model=PaymentResponse,
    summary="Verify (complete) a payment",
)
async def verify_payment(
    payment_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Simulate payment verification — marks payment as completed."""
    return await PaymentService.verify(db, current_user, payment_id)


@router.get(
    "",
    response_model=PaymentListResponse,
    summary="List user payments",
)
async def list_payments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all payments for the authenticated user."""
    return await PaymentService.list_by_user(db, current_user)


@router.get(
    "/{payment_id}/receipt",
    summary="Download payment receipt",
)
async def download_receipt(
    payment_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """Generate and download a PDF receipt for a completed payment."""
    return await PaymentService.generate_receipt(db, current_user, payment_id)
