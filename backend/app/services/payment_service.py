"""
Payment Service

Handles payment initiation, listing, and receipt generation.
"""

import io
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment, PaymentStatus
from app.models.user import User
from app.schemas.payment import PaymentInitiateRequest, PaymentListResponse, PaymentResponse


class PaymentService:
    """Payment processing business logic."""

    @staticmethod
    async def initiate(
        db: AsyncSession, user: User, data: PaymentInitiateRequest
    ) -> PaymentResponse:
        """Create payment record and simulate payment processing."""
        payment = Payment(
            id=uuid.uuid4(),
            user_id=user.id,
            university_id=user.university_id,
            payment_type=data.payment_type,
            amount=data.amount,
            currency=data.currency or "INR",
            status=PaymentStatus.PENDING,
            payment_method=data.payment_method,
            notes=data.notes,
        )
        db.add(payment)
        await db.flush()
        return PaymentResponse.model_validate(payment)

    @staticmethod
    async def verify(
        db: AsyncSession, user: User, payment_id: uuid.UUID
    ) -> PaymentResponse:
        """Simulate payment verification — marks payment as completed."""
        result = await db.execute(
            select(Payment).where(
                Payment.id == payment_id,
                Payment.user_id == user.id,
            )
        )
        payment = result.scalar_one_or_none()
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found.",
            )

        if payment.status != PaymentStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment is already {payment.status.value}.",
            )

        # Simulate successful payment
        payment.status = PaymentStatus.COMPLETED
        payment.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        payment.paid_at = datetime.now(timezone.utc)
        await db.flush()

        return PaymentResponse.model_validate(payment)

    @staticmethod
    async def list_by_user(db: AsyncSession, user: User) -> PaymentListResponse:
        """List all payments for a user."""
        result = await db.execute(
            select(Payment)
            .where(Payment.user_id == user.id)
            .order_by(Payment.created_at.desc())
        )
        payments = result.scalars().all()
        return PaymentListResponse(
            payments=[PaymentResponse.model_validate(p) for p in payments],
            total=len(payments),
        )

    @staticmethod
    async def generate_receipt(
        db: AsyncSession, user: User, payment_id: uuid.UUID
    ) -> StreamingResponse:
        """Generate a PDF receipt for a completed payment."""
        result = await db.execute(
            select(Payment).where(
                Payment.id == payment_id,
                Payment.user_id == user.id,
            )
        )
        payment = result.scalar_one_or_none()
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found.",
            )
        if payment.status != PaymentStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Receipt available only for completed payments.",
            )

        # Generate PDF using reportlab
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        w, h = A4

        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(w / 2, h - 60, "CampusAI — Payment Receipt")

        c.setFont("Helvetica", 12)
        y = h - 120
        details = [
            ("Receipt ID", str(payment.id)),
            ("Transaction ID", payment.transaction_id or "N/A"),
            ("Student", user.full_name),
            ("Email", user.email),
            ("Payment Type", payment.payment_type),
            ("Amount", f"{payment.currency} {payment.amount:,.2f}"),
            ("Status", payment.status.value.upper()),
            ("Payment Method", payment.payment_method or "Online"),
            ("Paid At", payment.paid_at.strftime("%Y-%m-%d %H:%M:%S") if payment.paid_at else "N/A"),
        ]
        for label, value in details:
            c.drawString(60, y, f"{label}:")
            c.drawString(220, y, value)
            y -= 25

        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(w / 2, 40, "This is a computer-generated receipt and does not require a signature.")

        c.save()
        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="receipt-{payment.id}.pdf"'
            },
        )
